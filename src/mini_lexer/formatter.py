"""Convert SLY tokens to the exact text required by the assignment.

Owners: members 1 and 6
"""

from __future__ import annotations

from typing import Any

from .symbol_table import SymbolTable


KEYWORD_TYPES = {
    "IF",
    "THEN",
    "ELSE",
    "ENDIF",
    "WHILE",
    "DO",
    "ENDWHILE",
    "PRINT",
    "NEWLINE",
    "READ",
}

OPERATOR_TYPES = {
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "ASSIGN",
    "GT",
    "GE",
    "LT",
    "LE",
    "EQ",
    "INCREMENT",
    "DECREMENT",
}


def format_token(token: Any, symbols: SymbolTable) -> str:
    """Return one output line for a token.

    TODO (members 1 and 6): verify every line against the assignment PDF.
    """
    if token.type == "IDENTIFIER":
        if symbols.register(token.value):
            return f"new identifier: {token.value}"
        return f'identifier "{token.value}" already in symbol table'
    if token.type in OPERATOR_TYPES:
        return f"operator: {token.value}"
    if token.type in KEYWORD_TYPES:
        return f"keyword: {token.value}"
    if token.type == "INTEGER":
        return f"integer: {token.value}"
    if token.type == "STRING":
        return f"string: {token.value}"
    if token.type == "LPAREN":
        return "left parenthesis: ("
    if token.type == "RPAREN":
        return "right parenthesis: )"
    if token.type == "SEMICOLON":
        return "semicolon: ;"
    raise ValueError(f"Unsupported token type: {token.type}")

