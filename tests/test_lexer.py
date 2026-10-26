"""Test token recognition, ignored comments, line counting, and lexical errors."""

import pytest

from src.mini_lexer.lexer import LexicalError, MiniLexer


def test_empty_input_has_no_tokens() -> None:
    assert list(MiniLexer().tokenize("")) == []


def test_unknown_character_stops_lexer() -> None:
    with pytest.raises(LexicalError, match=r"unexpected character @"):
        list(MiniLexer().tokenize("@"))


# Strings and comments

def test_string_preserves_surrounding_quotes() -> None:
    tokens = list(MiniLexer().tokenize('"Hello World"'))

    assert [(token.type, token.value) for token in tokens] == [
        ("STRING", '"Hello World"'),
    ]


def test_string_with_comment_markers_is_not_a_comment() -> None:
    tokens = list(MiniLexer().tokenize('"http://example.com /* not a comment */"'))

    assert [(token.type, token.value) for token in tokens] == [
        ("STRING", '"http://example.com /* not a comment */"'),
    ]


def test_unterminated_string_is_a_lexical_error() -> None:
    with pytest.raises(LexicalError, match=r'unexpected character "'):
        list(MiniLexer().tokenize('"unterminated'))


def test_newline_inside_string_is_a_lexical_error() -> None:
    with pytest.raises(LexicalError, match=r'unexpected character "'):
        list(MiniLexer().tokenize('"line\nbreak"'))


def test_single_line_comment_is_ignored_at_eof() -> None:
    assert list(MiniLexer().tokenize("// comment at EOF")) == []


def test_single_line_comment_is_ignored_adjacent_to_strings() -> None:
    tokens = list(MiniLexer().tokenize('"before"// comment\n"after"'))

    assert [token.value for token in tokens] == ['"before"', '"after"']


def test_block_comment_is_ignored_and_updates_line_numbers() -> None:
    tokens = list(MiniLexer().tokenize('"before"/* first\nsecond\n*/"after"'))

    assert [token.value for token in tokens] == ['"before"', '"after"']
    assert [token.lineno for token in tokens] == [1, 3]


def test_unterminated_block_comment_is_a_lexical_error() -> None:
    with pytest.raises(LexicalError, match="unterminated block comment"):
        list(MiniLexer().tokenize('/* never closes'))


@pytest.mark.skipif(
    "DIVIDE" not in MiniLexer._master_re.groupindex,
    reason="The DIVIDE token rule is unavailable",
)
def test_regular_division_is_not_treated_as_a_comment() -> None:
    tokens = list(MiniLexer().tokenize("/"))

    assert [(token.type, token.value) for token in tokens] == [("DIVIDE", "/")]


def test_lexical_error_stops_processing_immediately() -> None:
    lexer = MiniLexer()
    tokens = lexer.tokenize('"valid" @ "never reached"')

    assert next(tokens).value == '"valid"'
    with pytest.raises(LexicalError, match=r"unexpected character @"):
        next(tokens)


# Operators and punctuation

def test_single_character_operators() -> None:
    tokens = list(MiniLexer().tokenize("+ - * / = > <"))

    assert [(token.type, token.value) for token in tokens] == [
        ("PLUS", "+"),
        ("MINUS", "-"),
        ("TIMES", "*"),
        ("DIVIDE", "/"),
        ("ASSIGN", "="),
        ("GT", ">"),
        ("LT", "<"),
    ]


def test_long_operators_are_not_split() -> None:
    tokens = list(MiniLexer().tokenize(">= > <= < == = ++ + -- -"))

    assert [(token.type, token.value) for token in tokens] == [
        ("GE", ">="),
        ("GT", ">"),
        ("LE", "<="),
        ("LT", "<"),
        ("EQ", "=="),
        ("ASSIGN", "="),
        ("INCREMENT", "++"),
        ("PLUS", "+"),
        ("DECREMENT", "--"),
        ("MINUS", "-"),
    ]


def test_adjacent_parentheses_and_semicolon() -> None:
    tokens = list(MiniLexer().tokenize("();"))

    assert [(token.type, token.value) for token in tokens] == [
        ("LPAREN", "("),
        ("RPAREN", ")"),
        ("SEMICOLON", ";"),
    ]


def test_division_and_comments_together() -> None:
    source = "/ /* + >= ;\n -- */ / // * == ()\n /"
    tokens = list(MiniLexer().tokenize(source))

    assert [(token.type, token.value) for token in tokens] == [
        ("DIVIDE", "/"),
        ("DIVIDE", "/"),
        ("DIVIDE", "/"),
    ]
# Integers, identifiers, and keywords
def test_integer_tokens() -> None:
    tokens = list(MiniLexer().tokenize("0 123 12345"))

    assert [(token.type, token.value) for token in tokens] == [
        ("INTEGER", "0"),
        ("INTEGER", "123"),
        ("INTEGER", "12345"),
    ]


def test_identifier_tokens() -> None:
    tokens = list(MiniLexer().tokenize("A score id1 student123"))

    assert [(token.type, token.value) for token in tokens] == [
        ("IDENTIFIER", "A"),
        ("IDENTIFIER", "score"),
        ("IDENTIFIER", "id1"),
        ("IDENTIFIER", "student123"),
    ]


def test_lowercase_keywords_are_mapped() -> None:
    tokens = list(
        MiniLexer().tokenize(
            "if then else endif while do endwhile print newline read"
        )
    )

    assert [(token.type, token.value) for token in tokens] == [
        ("IF", "if"),
        ("THEN", "then"),
        ("ELSE", "else"),
        ("ENDIF", "endif"),
        ("WHILE", "while"),
        ("DO", "do"),
        ("ENDWHILE", "endwhile"),
        ("PRINT", "print"),
        ("NEWLINE", "newline"),
        ("READ", "read"),
    ]


def test_keywords_are_case_sensitive() -> None:
    tokens = list(MiniLexer().tokenize("if If IF"))

    assert [(token.type, token.value) for token in tokens] == [
        ("IF", "if"),
        ("IDENTIFIER", "If"),
        ("IDENTIFIER", "IF"),
    ]


def test_keyword_prefix_is_identifier() -> None:
    tokens = list(MiniLexer().tokenize("iffy print1 newline2"))

    assert [(token.type, token.value) for token in tokens] == [
        ("IDENTIFIER", "iffy"),
        ("IDENTIFIER", "print1"),
        ("IDENTIFIER", "newline2"),
    ]


def test_identifier_starting_with_underscore_is_rejected() -> None:
    with pytest.raises(
        LexicalError,
        match="must start with an English letter",
    ):
        list(MiniLexer().tokenize("_score"))


def test_identifier_starting_with_digit_is_rejected() -> None:
    with pytest.raises(LexicalError, match="must not start with a digit"):
        list(MiniLexer().tokenize("1score"))


def test_identifier_with_multiple_leading_digits_is_rejected() -> None:
    with pytest.raises(LexicalError, match="must not start with a digit"):
        list(MiniLexer().tokenize("123abc"))


def test_underscore_inside_identifier_is_rejected() -> None:
    with pytest.raises(LexicalError, match="must not contain underscore"):
        list(MiniLexer().tokenize("student_name"))


def test_integer_followed_by_space_and_identifier_is_valid() -> None:
    tokens = list(MiniLexer().tokenize("123 score"))

    assert [(token.type, token.value) for token in tokens] == [
        ("INTEGER", "123"),
        ("IDENTIFIER", "score"),
    ]


# Line counting and error handling

def test_line_number_increments_across_multiple_lines() -> None:
    tokens = list(MiniLexer().tokenize('"a"\n"b"\n\n"c"'))

    assert [token.lineno for token in tokens] == [1, 2, 4]


def test_crlf_line_endings_do_not_raise_lexical_error() -> None:
    tokens = list(MiniLexer().tokenize('"a"\r\n"b"'))

    assert [token.value for token in tokens] == ['"a"', '"b"']


def test_blank_lines_produce_no_tokens() -> None:
    assert list(MiniLexer().tokenize("\n\n\n")) == []


def test_error_names_the_first_bad_character_only() -> None:
    with pytest.raises(LexicalError, match=r"unexpected character #"):
        list(MiniLexer().tokenize('"ok"\n#\n"never reached"'))
