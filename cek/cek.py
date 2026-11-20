import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

# Query untuk fitur
Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNC = Query(PY, '(function_definition name: (identifier) @nama) @fungsi')

# Fungsi rekursif untuk Fitur 3
def cari_error_pertama(node):
    if node.is_error or node.is_missing:
        return node
    for child in node.children:
        hasil = cari_error_pertama(child)
        if hasil:
            return hasil
    return None

def cek_file(path):
    # Abaikan folder berat (venv, node_modules, .git) agar tidak lambat
    if any(part in path.parts for part in ['venv', '.git', 'node_modules']):
        return

    try:
        tree = parser.parse(path.read_bytes())
    except Exception:
        return # Lewati jika file tidak bisa dibaca

    # Fitur 1: komentar TODO/FIXME
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        teks = node.text.decode(errors="replace").strip() # type: ignore
        print(f"[TODO] {path}:{node.start_point[0] + 1}: {teks}")

    # Fitur 2: fungsi yang lebih dari 30 baris
    for pola_idx, tangkapan in QueryCursor(Q_FUNC).matches(tree.root_node):
        if "fungsi" in tangkapan and "nama" in tangkapan:
            node_fungsi = tangkapan["fungsi"][0]
            node_nama = tangkapan["nama"][0]
            
            jumlah_baris = node_fungsi.end_point[0] - node_fungsi.start_point[0] + 1
            if jumlah_baris > 30:
                nama_fungsi = node_nama.text.decode(errors="replace") # type: ignore
                print(f"[FUNGSI PANJANG] {path}:{node_fungsi.start_point[0] + 1}: '{nama_fungsi}' ({jumlah_baris} baris)")

    # Fitur 3: file yang pohonnya mengandung error
    if tree.root_node.has_error:
        node_err = cari_error_pertama(tree.root_node)
        baris = node_err.start_point[0] + 1 if node_err else "unknown"
        print(f"[ERROR SINTAKS] {path}:{baris}: Terdeteksi sintaks rusak")

# Eksekusi CLI
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Penggunaan: python cek.py <folder>")
        sys.exit(1)
        
    for path in Path(sys.argv[1]).rglob("*.py"):
        cek_file(path)