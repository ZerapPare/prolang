"""Starter tests for member 4's symbol table."""

from src.mini_lexer.symbol_table import SymbolTable


def test_registers_new_identifier() -> None:
    table = SymbolTable()

    assert table.register("score") is True
    assert "score" in table


def test_rejects_duplicate_identifier() -> None:
    table = SymbolTable()
    table.register("score")

    assert table.register("score") is False
    assert len(table) == 1

