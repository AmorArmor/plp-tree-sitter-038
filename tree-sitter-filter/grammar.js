module.exports = grammar({
  name: 'filter',
  
  extras: $ => [/\s/],
  word: $ => $.identifier,

  rules: {
    query: $ => $._expr,

    _expr: $ => choice(
      $.comparison,
      $.in_expression,
      $.contains_expression,
      $.and_expression,
      $.or_expression,
      $.not_expression,
      $.parenthesized
    ),

    and_expression: $ => prec.left(2, seq(field('left', $._expr), 'and', field('right', $._expr))),
    or_expression: $ => prec.left(1, seq(field('left', $._expr), 'or', field('right', $._expr))),
    not_expression: $ => prec(3, seq('not', field('argument', $._expr))),
    parenthesized: $ => seq('(', $._expr, ')'),

    comparison: $ => seq(
      field('field', $.identifier),
      field('operator', choice('=', '!=', '>', '<', '>=', '<=')),
      field('value', $._value)
    ),

    // Logika IN untuk mengecek nilai dalam array
    in_expression: $ => seq(
      field('field', $.identifier),
      'in',
      field('value', $.list)
    ),

    // Logika CONTAINS untuk mengecek teks
    contains_expression: $ => seq(
      field('field', $.identifier),
      'contains',
      field('value', $.string)
    ),

    // Format array: ["a", "b"] atau [1, 2]
    list: $ => seq(
      '[',
      optional(seq($._value, repeat(seq(',', $._value)))),
      ']'
    ),

    _value: $ => choice($.string, $.number, $.boolean),
    boolean: $ => choice('true', 'false'),
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_.]*/,
    string: $ => /"[^"]*"/,
    number: $ => /\d+(\.\d+)?/
  }
});