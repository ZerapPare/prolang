"""Shared lexer tests. Each member should add at least four test cases here."""

import pytest

from src.mini_lexer.lexer import LexicalError, MiniLexer


def test_empty_input_has_no_tokens() -> None:
    assert list(MiniLexer().tokenize("")) == []


def test_unknown_character_stops_lexer() -> None:
    with pytest.raises(LexicalError, match=r"unexpected character @"):
        list(MiniLexer().tokenize("@"))


# TODO member 2: operator and punctuation tests
# TODO member 3: integer, identifier, and keyword tests
# TODO member 5: string and comment tests
# TODO member 6: line counting and stop-on-error tests

