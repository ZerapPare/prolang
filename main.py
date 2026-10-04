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


def run(source: str, out=print) -> int:
    """แยก token จาก source แล้วแสดงผลทีละบรรทัด คืน 0 ถ้าสำเร็จ, 1 ถ้าเจอ error"""
    lexer = MiniLexer()
    symbols = SymbolTable()

    try:
        for token in lexer.tokenize(source):
            out(format_token(token, symbols))
    except LexicalError as error:
        # แสดงอักขระที่ผิดแล้วหยุดทันที
        out(str(error))
        return 1

    return 0


def main(argv: list[str] | None = None) -> int:
    """รับชื่อไฟล์จาก command line อ่านไฟล์ แล้วส่งให้ run()"""
    parser = argparse.ArgumentParser(description="Analyze tokens in a source file")
    parser.add_argument("input_file", type=Path, help="path to a .txt source file")
    input_file = parser.parse_args(argv).input_file

    # โจทย์กำหนดให้รับเฉพาะไฟล์ .txt
    if input_file.suffix.lower() != ".txt":
        print("Error: input file must have a .txt extension")
        return 1

    try:
        # utf-8-sig ตัด BOM ที่ Notepad อาจใส่ไว้ต้นไฟล์
        source = input_file.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as error:
        print(f"Error: cannot read {input_file}: {error}")
        return 1

    return run(source)


if __name__ == "__main__":
    raise SystemExit(main())