import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

def jelajah(node, kedalaman=0, field=None):
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")
    
    # BAGIAN TODO YANG SUDAH DIISI:
    # Menelusuri semua anak node untuk mencari yang bernama
    for i, child in enumerate(node.children):
        if child.is_named:
            # Ambil nama field berdasarkan indeks child aslinya
            nama_field = node.field_name_for_child(i)
            # Panggil rekursif dengan kedalaman ditambah 1
            jelajah(child, kedalaman + 1, nama_field)

# Membaca file dari argumen terminal
with open(sys.argv[1], "rb") as f:
    tree = parser.parse(f.read())
    
jelajah(tree.root_node)