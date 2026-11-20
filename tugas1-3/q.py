import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

kode = open(sys.argv[1], "rb").read()
pola = open(sys.argv[2]).read()
tree = parser.parse(kode)

# Kita cek dulu apakah kita mau pakai mode 'matches' (untuk relasi antar node) 
# atau 'captures' biasa.
if "matches" in sys.argv:
    for _, cap in QueryCursor(Query(PY, pola)).matches(tree.root_node):
        nama = cap["nama"][0].text.decode() # type: ignore
        # Pakai .get() agar aman jika fungsi tidak punya parameter
        params_node = cap.get("params", [])
        jumlah = params_node[0].named_child_count if params_node else 0
        print(f"Fungsi: {nama}, Jumlah Parameter: {jumlah}")
else:
    hasil = QueryCursor(Query(PY, pola)).captures(tree.root_node)
    for nama, nodes in hasil.items():
        for n in nodes:
            print(f"@{nama}  baris {n.start_point[0] + 1}: {n.text.decode()}") # type: ignore