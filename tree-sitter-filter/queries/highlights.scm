; Tipe data
(string) @string
(number) @number
(boolean) @boolean

; Field yang sedang difilter (sebelah kiri) akan diberi warna seperti properti
(comparison field: (identifier) @property)
(in_expression field: (identifier) @property)
(contains_expression field: (identifier) @property)

; Operator pembanding
[
  "="
  "!="
  ">"
  "<"
  ">="
  "<="
] @operator

; Kata kunci logika dan operasi
[
  "and"
  "or"
  "not"
  "in"
  "contains"
] @keyword

; Tanda kurung dan kurung siku
[
  "("
  ")"
  "["
  "]"
] @punctuation.bracket