"""Starter tests for member 4's symbol table."""

from src.mini_lexer.symbol_table import SymbolTable


def test_registers_new_identifier() -> None:
    table = SymbolTable()

    assert table.add("score") is True
    assert table.contains("score") is True


def test_rejects_duplicate_identifier() -> None:
    table = SymbolTable()
    table.add("score")

    assert table.add("score") is False
    assert len(table.get_all()) == 1


def test_contains_returns_false_for_unknown_identifier() -> None:
    table = SymbolTable()

    assert table.contains("missing") is False


def test_get_all_returns_identifiers_in_sorted_order() -> None:
    table = SymbolTable()
    table.add("zebra")
    table.add("apple")

    assert table.get_all() == ["apple", "zebra"]

