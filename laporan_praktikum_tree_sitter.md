# Eksplorasi Concrete Syntax Tree, Query, dan Grammar dengan Tree-sitter

**Laporan Praktikum & Tugas Awal — Programming Language Pragmatics**

| Keterangan | Detail |
| :--- | :--- |
| **Nama / NIM / Kelas** | Amor Azzam Imani — 251524038 — 2B-D4 |
| **Repositori Proyek** | https://github.com/AmorArmor/plp-tree-sitter-038 |
| **Lingkungan Kerja** | Windows 11/10 Native, VS Code, Python 3.12 (`tree-sitter 0.26.1`, `tree-sitter-python 0.25.0`), Node.js v26 |

---

## 1. Ringkasan Pelaksanaan & Hasil Tugas 1–3 (`tugas1-3/`)

### Tugas 1 — Membaca Pohon Sintaks
Pengujian dilakukan untuk melihat struktur dasar pohon sintaks (AST) pada bahasa Python. Hasil keluaran S-expression menunjukkan bagaimana `tree-sitter` membedakan antara *named node* (seperti `function_definition` atau `identifier`) dengan *anonymous node* (seperti token literal `'def'`, `'('`, atau `':'`). Saat disimulasikan sebuah *error* sintaks, parser terbukti mampu melakukan *error recovery* dengan memunculkan node `ERROR`.

**Inti Keluaran Terminal (`python tugas1.py`):**
```text
=== Output S-Expression ===
(module (function_definition name: (identifier) parameters: (parameters (identifier)) body: (block (return_statement (identifier)))))

Anak langsung dari 'function_definition':
  - 'def' -> anonim
  - 'identifier' -> bernama
  - 'parameters' -> bernama
  - ':' -> anonim
  - 'block' -> bernama

=== Simulasi Syntax Error ===
(module (ERROR (identifier) (parameters (identifier)) (identifier)))
```

### Tugas 2 — Penjelajah Node Rekursif
Skrip rekursif dibangun untuk menelusuri keseluruhan pohon (DFS). Skrip ini memanfaatkan `node.children` dan menyaring token anonim dengan `is_named`. Hasil eksekusi mencetak hierarki fungsi dan ekspresi lengkap dengan informasi posisi (koordinat baris dan kolom) dari kode Python secara bertingkat (ber-indentasi).

**Inti Keluaran Terminal (`python tugas2.py`):**
```text
[0:0] module
  [0:0] function_definition
    [0:4] identifier
    [0:15] parameters
      [0:16] identifier
    [1:4] block
      [1:4] expression_statement
        [1:4] call
          [1:4] identifier
          [1:9] argument_list
            [1:10] string
```

### Tugas 3 — Pattern Matching dengan Query
Eksekusi file query `.scm` berhasil menangkap elemen spesifik menggunakan `QueryCursor.matches()`. Query S-expression mendeteksi fungsi, deklarasi `print`, dan `import` yang berada di dalam berkas pengujian, dan hasilnya terbukti cocok 100% ketika diverifikasi secara manual.

**Inti Keluaran Terminal (`python tugas3.py uji.py`):**
```text
=== Hasil Eksekusi Query ===
[Fungsi Ditemukan] Baris 1: 'hitung_total' dengan 2 parameter
[Fungsi Ditemukan] Baris 15: 'cetak_struk' dengan 1 parameter
[Pemanggilan Print] Baris 17: print("Total harga:", total)
[Pemanggilan Print] Baris 25: print("Terima kasih")
[Import Statement] Baris 1: import os
[Import Statement] Baris 2: from datetime import datetime
```

---

## 2. Ringkasan Pelaksanaan & Hasil Tugas 4–6 (`tree-sitter-filter/` & `cek/`)

### Tugas 4 — Grammar DSL Filter
Membuat *parser* DSL untuk kueri filter dengan `grammar.js`. Tata bahasa mencakup operator logika (`and`, `or`, `not`), perbandingan matematis, serta presedensi (prioritas eksekusi) menggunakan `prec.left(1)` dan `prec.left(2)` agar ekspresi dengan kurung dan operator AND/OR tidak menyebabkan *conflict*. Semua *test case* di folder `corpus/` berhasil lulus `tree-sitter test`.

**Inti Keluaran Terminal (`tree-sitter test`):**
```text
> tree-sitter test
  dasar:
      1. ✓ 1. and lebih kuat dari or
      2. ✓ 2. tanda kurung mengubah prioritas
      3. ✓ 3. operator not dan nilai boolean
      4. ✓ 4. perbandingan string dan field bertitik
      5. ✓ 5. operator in dengan tiga nilai
      6. ✓ 6. operator contains untuk pencarian teks

Total parses: 6; successful parses: 6; failed parses: 0; success percentage: 100.00%; average speed: 1180 bytes/ms
```

### Tugas 5 — Syntax Highlighting DSL Filter
Mengimplementasikan pewarnaan kode di `queries/highlights.scm`. Setiap pola dikaitkan dengan tag Tree-sitter bawaan seperti `@keyword` (untuk *and, or, not*), `@operator`, dan `@property`.

**Inti Keluaran Terminal (`tree-sitter highlight`):**
```text
> tree-sitter highlight contoh.filter
status = "open" and (umur >= 18 or not premium = false) and kategori in ["admin"]
(Teks di atas muncul dengan pewarnaan yang sesuai dengan tag highlight di terminal)
```

### Tugas 6 — Mini Proyek CLI Pendeteksi Kualitas Kode (`cek/cek.py`)
Pembuatan program CLI berbasis Python untuk menganalisis basis kode skala besar. Program berhasil mendeteksi:
1. Komentar `TODO`/`FIXME` menggunakan metode `#match?`.
2. Fungsi dengan body melebihi 30 baris dengan menghitung titik koordinat `end_point[0] - start_point[0] + 1`.
3. Adanya kode bermasalah melalui status `root_node.has_error` secara rekursif.

**Inti Keluaran Terminal pada pengujian lokal (`uji/`):**
```text
> python cek.py uji/
[ERROR SINTAKS] uji\tes_error.py:1: Terdeteksi sintaks rusak
[FUNGSI PANJANG] uji\tes_panjang.py:1: 'fungsi_sangat_panjang' (35 baris)
[TODO] uji\tes_todo.py:1: # TODO: perbaiki fungsi ini
```

**Inti Keluaran Terminal pada repositori nyata (`bottle/`):**
```text
> python cek.py bottle/
[TODO] bottle\bottle.py:1002: # TODO: Handle these explicitly in handle() or make them iterable.
[TODO] bottle\bottle.py:2837: # HTTP Utilities and MISC (TODO) ###############################################
[TODO] bottle\bottle.py:2004: #: Not a plugin, but part of the plugin API. TODO: Find a better place.
[FUNGSI PANJANG] bottle\bottle.py:329: 'add' (75 baris)
[FUNGSI PANJANG] bottle\bottle.py:430: 'match' (34 baris)
[FUNGSI PANJANG] bottle\bottle.py:675: '_mount_wsgi' (35 baris)
[FUNGSI PANJANG] bottle\bottle.py:843: 'route' (50 baris)
```

---

## 3. Kendala Teknis & Cara Mengatasinya

| Tugas | Kendala yang Ditemui | Solusi & Langkah Perbaikan |
| :--- | :--- | :--- |
| **Tugas 1-3** | Pengalihan *output* terminal PowerShell (`>` ke file `.txt`) sering gagal, menghasilkan file kosong, atau mengalami *error encoding*. | Menyelesaikan masalah dengan mengubah pendekatan: penulisan keluaran di-handle langsung secara internal dari dalam skrip Python menggunakan *file handling* standar (`open`, `write`). |
| **Tugas 4** | Muncul *error* `ReferenceError: module is not defined in ES module scope` pada saat eksekusi `tree-sitter generate` di Node.js. | Menyesuaikan standar modul JavaScript dengan mengubah sintaks bawaan `module.exports = grammar(...)` menjadi sintaks ES Module `export default grammar(...)`. |
| **Tugas 4** | Adanya peringatan *Unresolved conflict* dari parser Tree-sitter ketika operator logika `and` dan `or` ditambahkan secara bersamaan. | Menerapkan tingkat presedensi (*precedence*) menggunakan `prec.left(1)` untuk `or` dan `prec.left(2)` untuk `and` agar parser tahu prioritas pembacaannya. |
| **Tugas 5** | Muncul *warning* panjang di terminal mengenai tidak adanya konfigurasi *parser directories* saat menjalankan perintah `tree-sitter highlight`. | Menjalankan perintah `tree-sitter init-config` untuk membuat file konfigurasi global, lalu menambahkan entri `"highlights": "queries/highlights.scm"` di dalam `tree-sitter.json`. |
| **Tugas 6** | Saat menguji coba skrip CLI `cek.py` ke repositori `win-10-virtual-desktop-enhancer`, program tidak mengeluarkan hasil apa-apa di terminal. | Setelah dicek di VS Code, ternyata repositori tersebut berbasis AutoHotkey (`.ahk`), bukan Python. Repo tersebut dihapus, lalu beralih meng-clone repo proyek *framework* Python `bottle`, yang kemudian berhasil dieksekusi. |

---

## 4. Catatan Penggunaan AI Coding Agent & Bukti Verifikasi

Penggunaan model LLM (Gemini) diterapkan selama penugasan dari Tugas 1 hingga Tugas 6 sebagai asisten pemandu sintaks API, *troubleshooting*, dan pemahaman konsep. 

| Bagian | Bantuan yang Diminta dari AI | Bukti Verifikasi & Hasil |
| :--- | :--- | :--- |
| **Tugas 1–3** | AI membantu menjelaskan cara membaca hierarki S-expression dari AST Python, membimbing pembuatan alur rekursif untuk *node traversal*, dan memberi sintaks dasar kueri `.scm`. | Mengecek kecocokan log *output* eksekusi skrip terhadap baris kode asli pada file Python yang diuji. Hierarki baris dan kolom yang dicetak program terbukti akurat dengan kode aslinya. |
| **Tugas 4** | Meminta penjelasan cara mengatur konflik prioritas eksekusi antara operator `and` dan `or` di dalam `grammar.js`. | AI menyarankan penggunaan fungsi tingkat presedensi `prec.left(1)` dan `prec.left(2)`. Setelah diterapkan, `tree-sitter generate` berhasil tanpa *conflict* dan 100% *test case* berlalu. |
| **Tugas 5-6** | Bantuan untuk penulisan tag `.scm` untuk pewarnaan kode, perbaikan *warning parser directory*, serta evaluasi mengapa CLI tidak memunculkan *output* saat menguji repo *Enhancer*. | AI mendeteksi bahwa repo yang di-clone bukan Python. Setelah beralih ke `bottle`, 2 file laporan dicek secara manual di VS Code (mencari baris ber-TODO dan fungsi >30 baris), yang membuktikan akurasi skrip 100%. |