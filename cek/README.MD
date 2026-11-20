# Mini Proyek: Pendeteksi TODO, Fungsi Panjang, dan Error Sintaks

Program CLI (`cek.py`) ini menggunakan `tree-sitter` dan `tree-sitter-python` untuk melakukan analisis statis pada kumpulan kode sumber Python. Program ini akan mendeteksi:
1. Komentar yang mengandung TODO atau FIXME.
2. Fungsi yang panjangnya lebih dari 30 baris (termasuk fungsi di dalam kelas atau bersarang).
3. File yang memiliki *error* atau kerusakan sintaks.

## Cara Memasang Dependensi

Pastikan Python sudah terinstal, lalu jalankan perintah berikut di terminal untuk memasang modul `tree-sitter` beserta *binding* untuk bahasa Python:

```bash
pip install tree-sitter tree-sitter-python
```

## Cara Menjalankan
Gunakan terminal dan panggil skrip cek.py diikuti dengan lokasi folder repositori atau proyek Python yang ingin dianalisis. 

```bash
python cek.py <nama_folder_target>
```

Contoh eksekusi pada pengujian lokal:

```bash
python cek.py uji/
```
## Contoh Output
Berikut adalah contoh hasil eksekusi program ketika dijalankan pada repositori nyata (misal: repositori bottle):

[TODO] bottle\bottle.py:1002: # TODO: Handle these explicitly in handle() or make them iterable.
[TODO] bottle\bottle.py:2837: # HTTP Utilities and MISC (TODO) ###############################################
[TODO] bottle\bottle.py:2004: #: Not a plugin, but part of the plugin API. TODO: Find a better place.
[FUNGSI PANJANG] bottle\bottle.py:329: 'add' (75 baris)
[FUNGSI PANJANG] bottle\bottle.py:430: 'match' (34 baris)
[FUNGSI PANJANG] bottle\bottle.py:675: '_mount_wsgi' (35 baris)
[FUNGSI PANJANG] bottle\bottle.py:843: 'route' (50 baris)
[FUNGSI PANJANG] bottle\bottle.py:939: '_handle' (40 baris)
[FUNGSI PANJANG] bottle\bottle.py:980: '_cast' (72 baris)
[FUNGSI PANJANG] bottle\bottle.py:1053: 'wsgi' (31 baris)
[FUNGSI PANJANG] bottle\bottle.py:1343: 'POST' (32 baris)
[FUNGSI PANJANG] bottle\bottle.py:1761: 'set_cookie' (80 baris)
[FUNGSI PANJANG] bottle\bottle.py:2444: '_make_overlay' (34 baris)
[FUNGSI PANJANG] bottle\bottle.py:2725: 'static_file' (110 baris)
[FUNGSI PANJANG] bottle\bottle.py:2908: '_parse_http_header' (31 baris)
[FUNGSI PANJANG] bottle\bottle.py:3142: '_lineiter' (36 baris)
[FUNGSI PANJANG] bottle\bottle.py:3179: 'parse' (58 baris)
[FUNGSI PANJANG] bottle\bottle.py:3783: 'run' (107 baris)
[FUNGSI PANJANG] bottle\bottle.py:4274: 'read_code' (52 baris)
[FUNGSI PANJANG] bottle\bottle.py:4506: '_main' (52 baris)
[FUNGSI PANJANG] bottle\test\test_config.py:106: 'test_overlay' (61 baris)
[FUNGSI PANJANG] bottle\test\test_environ.py:320: 'test_multipart' (39 baris)
[FUNGSI PANJANG] bottle\test\test_environ.py:512: 'test_set_status' (75 baris)
[TODO] bottle\test\test_html_helper.py:8: # TODO: Move more of the low level http stuff here.
[FUNGSI PANJANG] bottle\test\test_sendfile.py:118: 'test_etag' (35 baris)
[FUNGSI PANJANG] bottle\test\tools.py:89: 'urlopen' (33 baris)
