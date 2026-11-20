"""
SPMB Kota Bogor - Admission Chance Calculator
Jalur Prestasi | Jenjang SMP

Usage:
    python spmb_checker.py

You will be prompted to enter:
    - The school detail URL (paste once, script handles pagination)
    - Your brother's nilai_rapor
    - The school's available seat count (kuota)
"""

import re
import json
import html
import sys

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("[ERROR] Missing libraries. Run this first:")
    print("        pip install requests beautifulsoup4")
    sys.exit(1)


# ── Helpers ──────────────────────────────────────────────────────────────────

def build_url(base: str, page: int) -> str:
    """Replace or append the &page= parameter in the URL."""
    if re.search(r'[&?]page=\d+', base):
        return re.sub(r'([&?]page=)\d+', rf'\g<1>{page}', base)
    separator = '&' if '?' in base else '?'
    return f"{base}{separator}page={page}"


def fetch_page(session: requests.Session, url: str) -> dict | None:
    """Fetch one page and return the parsed data-page JSON, or None on failure."""
    try:
        resp = session.get(url, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"  [!] Request failed: {e}")
        return None

    soup = BeautifulSoup(resp.text, 'lxml')
    app_div = soup.find('div', id='app')
    if not app_div or not app_div.get('data-page'):
        print("  [!] Could not find div#app[data-page]. The site structure may have changed.")
        return None

    raw = html.unescape(app_div['data-page']) # type: ignore
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"  [!] JSON parse error: {e}")
        return None


def find_in_json(obj, target_key, _depth=0):
    """Recursively search for a key anywhere in a nested dict/list. Returns value or None."""
    if _depth > 10:
        return None
    if isinstance(obj, dict):
        if target_key in obj:
            return obj[target_key]
        for v in obj.values():
            result = find_in_json(v, target_key, _depth + 1)
            if result is not None:
                return result
    elif isinstance(obj, list):
        for item in obj:
            result = find_in_json(item, target_key, _depth + 1)
            if result is not None:
                return result
    return None


def extract_scores(data: dict, debug=False) -> tuple[list[float], int]:
    """
    Walk the JSON tree to find the list of applicants.
    Returns (scores_list, total_pages).
    """
    scores: list[float] = []
    last_page = 1

    props = data.get('props', {})

    if debug:
        print("\n  [DEBUG] Top-level props keys:", list(props.keys()))

    # --- Read pagination from the custom 'pagination' key ---
    pagination = props.get('pagination', {})
    if debug:
        print(f"  [DEBUG] pagination object: {pagination}")

    if isinstance(pagination, dict):
        # Try direct last_page first, then calculate from total/per_page
        if 'lastPage' in pagination:
            last_page = int(pagination['lastPage'])
        elif 'last_page' in pagination:
            last_page = int(pagination['last_page'])
        elif 'total' in pagination:
            per = pagination.get('perPage') or pagination.get('per_page') or 20
            import math
            last_page = math.ceil(int(pagination['total']) / int(per))
        if debug:
            print(f"  [DEBUG] Resolved last_page = {last_page}")
    else:
        # Final fallback: recursive search
        found_last_page = find_in_json(props, 'last_page')
        if found_last_page and isinstance(found_last_page, int):
            last_page = found_last_page
            if debug:
                print(f"  [DEBUG] Found last_page (recursive) = {last_page}")
        else:
            if debug:
                print("  [DEBUG] Could not determine last_page, will scrape page by page until empty")

    # --- Find the applicant list containing nilai_rapor ---
    candidate_lists = []
    for key, val in props.items():
        if isinstance(val, dict):
            inner = val.get('data')
            if isinstance(inner, list) and inner:
                candidate_lists.append((key, inner))
            # also check one level deeper
            for subkey, subval in val.items():
                if isinstance(subval, dict):
                    inner2 = subval.get('data')
                    if isinstance(inner2, list) and inner2:
                        candidate_lists.append((f"{key}.{subkey}", inner2))
        elif isinstance(val, list) and val:
            candidate_lists.append((key, val))

    if debug:
        print(f"  [DEBUG] Candidate lists found: {[k for k,_ in candidate_lists]}")

    if not candidate_lists:
        print("  [!] No list found in props. Dumping props keys for debugging:")
        for k, v in props.items():
            print(f"      {k}: {type(v).__name__}")
        return scores, last_page

    chosen_list = None
    for key, lst in candidate_lists:
        if any('nilai_rapor' in str(item) for item in lst[:5]):
            chosen_list = lst
            if debug:
                print(f"  [DEBUG] Using list from key: '{key}' with {len(lst)} items")
            break

    if chosen_list is None:
        print("  [!] 'nilai_rapor' not found in any list. Using first available.")
        chosen_list = candidate_lists[0][1]

    for item in chosen_list:
        if isinstance(item, dict) and 'nilai_rapor' in item:
            try:
                scores.append(float(item['nilai_rapor']))
            except (ValueError, TypeError):
                pass

    return scores, last_page


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  SPMB Kota Bogor — Admission Chance Calculator")
    print("  Jalur Prestasi | Jenjang SMP")
    print("=" * 60)
    print()

    # --- Input ---
    print("Paste the school detail URL (page=1 is fine, script handles the rest):")
    base_url = input("  URL: ").strip()
    if not base_url:
        print("[ERROR] URL cannot be empty.")
        sys.exit(1)

    try:
        bro_score = float(input("\nYour brother's nilai_rapor (e.g. 87.50): ").strip())
    except ValueError:
        print("[ERROR] Score must be a number.")
        sys.exit(1)

    try:
        quota = int(input("School's available seats / kuota (e.g. 32): ").strip())
    except ValueError:
        print("[ERROR] Quota must be a whole number.")
        sys.exit(1)

    # --- Scrape ---
    print("\nFetching data", end="", flush=True)
    session = requests.Session()
    session.headers.update({
        # Mimic a real browser so the server doesn't reject us
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/124.0.0.0 Safari/537.36'
        ),
        'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'id-ID,id;q=0.9,en;q=0.8',
    })

    all_scores: list[float] = []
    page = 1
    total_pages = 1  # updated after first fetch

    while page <= total_pages:
        url = build_url(base_url, page)
        data = fetch_page(session, url)
        if data is None:
            print(f"\n[ERROR] Stopped at page {page}.")
            break

        scores, total_pages = extract_scores(data, debug=(page == 1))
        all_scores.extend(scores)
        print(".", end="", flush=True)
        page += 1

    print(f" done ({page - 1}/{total_pages} pages)\n")

    if not all_scores:
        print("[ERROR] No scores collected. Check the URL or try again later.")
        sys.exit(1)

    # --- Calculate ---
    all_scores.sort(reverse=True)           # highest first
    total_applicants = len(all_scores)

    # Rank: how many applicants scored strictly HIGHER than bro
    rank = sum(1 for s in all_scores if s > bro_score) + 1

    # How many applicants scored the same (ties compete for the same seat)
    tied = sum(1 for s in all_scores if s == bro_score)

    # Safe acceptance: rank is comfortably within quota
    safe = rank <= quota
    # Borderline: rank is within quota but tied scores might push him out
    borderline = (rank <= quota) and (rank + tied - 1 > quota)
    # Chance percentage: what fraction of equally-ranked scenarios get him in
    if rank > quota:
        chance_pct = 0.0
    elif tied <= 1:
        chance_pct = 100.0
    else:
        # Among tied students, only some fit in remaining seats
        seats_left = quota - rank + 1
        chance_pct = min(100.0, (seats_left / tied) * 100)

    # --- Verdict ---
    if chance_pct == 100.0:
        verdict = "✅  LIKELY ACCEPTED"
        detail = f"His rank ({rank}) is safely within the quota ({quota})."
    elif chance_pct > 50.0:
        verdict = "⚠️   BORDERLINE (leaning in)"
        detail = f"His rank ({rank}) is inside quota but {tied} students share the same score."
    elif chance_pct > 0.0:
        verdict = "⚠️   BORDERLINE (leaning out)"
        detail = f"His rank ({rank}) is inside quota but too many ties ({tied}) to be safe."
    else:
        verdict = "❌  UNLIKELY (outside quota)"
        detail = f"His rank ({rank}) exceeds the available seats ({quota})."

    # --- Output ---
    print("=" * 60)
    print("  RESULTS")
    print("=" * 60)
    print(f"  Total applicants scraped : {total_applicants}")
    print(f"  Highest score            : {all_scores[0]:.2f}")
    print(f"  Lowest score             : {all_scores[-1]:.2f}")
    print(f"  Average score            : {sum(all_scores)/total_applicants:.2f}")
    print()
    print(f"  Your brother's score     : {bro_score:.2f}")
    print(f"  His rank                 : #{rank} out of {total_applicants}")
    print(f"  Students with same score : {tied}")
    print(f"  School quota             : {quota} seats")
    print()
    print(f"  Estimated chance         : {chance_pct:.1f}%")
    print(f"  Verdict                  : {verdict}")
    print(f"  Note                     : {detail}")
    print("=" * 60)


if __name__ == '__main__':
    main()
