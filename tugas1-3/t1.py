import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

kode = b"""
def sapa(nama):
    return nama

if x > 5:
    print("besar")
else:
    print("kecil")

class Hewan:
    def suara(self):
        return "..."
"""
tree = parser.parse(kode)
print(tree.root_node)

print("\n--- Node Anak dari Anak Pertama ---")
# Menelusuri anak dari node pertama di dalam root
for c in tree.root_node.children[0].children:
    print(c.type, "->", "bernama" if c.is_named else "anonim")