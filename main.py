"""Command-line entry point for the Mini Lexical Analyzer.

Owner: member 1
Run with: python main.py samples/valid_basic.txt
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.mini_lexer.formatter import format_token
from src.mini_lexer.lexer import LexicalError, MiniLexer
from src.mini_lexer.symbol_table import SymbolTable


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze tokens in a source file")
    parser.add_argument("input_file", type=Path, help="path to a .txt source file")
    return parser.parse_args()


def analyze_file(input_file: Path) -> int:
    """Read one source file, tokenize it, and print the required output."""
    if input_file.suffix.lower() != ".txt":
        print("Error: input file must have a .txt extension")
        return 1

    try:
        source = input_file.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Error: cannot read {input_file}: {error}")
        return 1

    lexer = MiniLexer()
    symbols = SymbolTable()

    try:
        for token in lexer.tokenize(source):
            print(format_token(token, symbols))
    except LexicalError as error:
        print(error)
        return 1

    return 0


def main() -> int:
    return analyze_file(parse_args().input_file)


if __name__ == "__main__":
    raise SystemExit(main())

