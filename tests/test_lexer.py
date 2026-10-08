"""Shared lexer tests. Each member should add at least four test cases here."""

import pytest

from src.mini_lexer.lexer import LexicalError, MiniLexer


def test_empty_input_has_no_tokens() -> None:
    assert list(MiniLexer().tokenize("")) == []


def test_unknown_character_stops_lexer() -> None:
    with pytest.raises(LexicalError, match=r"unexpected character @"):
        list(MiniLexer().tokenize("@"))


# Member 5: strings and comments

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
    reason="Member 2 DIVIDE rule is not implemented",
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


# TODO member 2: operator and punctuation tests
# TODO member 3: integer, identifier, and keyword tests
# TODO member 6: line counting and stop-on-error tests

