"""Identifier symbol table.

Owner: member 4
"""

from __future__ import annotations


class SymbolTable:
    """Remember identifiers that have already appeared in the input."""

    def __init__(self) -> None:
        self._identifiers: set[str] = set()

    def register(self, name: str) -> bool:
        """Add *name* and return True, or return False when it already exists."""
        if name in self._identifiers:
            return False
        self._identifiers.add(name)
        return True

    def __contains__(self, name: str) -> bool:
        return name in self._identifiers

    def __len__(self) -> int:
        return len(self._identifiers)

