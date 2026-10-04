"""SLY lexer rules shared by members 2, 3, 5, and 6.

Keep each member's rules inside the marked section to reduce merge conflicts.
"""

from __future__ import annotations

from sly import Lexer


class LexicalError(Exception):
    """Raised when the lexer finds an unexpected character."""


class MiniLexer(Lexer):
    """Tokenize the simulated language described in TermReport1-2569."""

    tokens = {
        # Member 2: operators and punctuation
        PLUS,
        MINUS,
        TIMES,
        DIVIDE,
        ASSIGN,
        GT,
        GE,
        LT,
        LE,
        EQ,
        INCREMENT,
        DECREMENT,
        LPAREN,
        RPAREN,
        SEMICOLON,
        # Member 3: values and words
        INTEGER,
        IDENTIFIER,
        IF,
        THEN,
        ELSE,
        ENDIF,
        WHILE,
        DO,
        ENDWHILE,
        PRINT,
        NEWLINE,
        READ,
        # Member 5: string
        STRING,
    }

    # Spaces and tabs are not tokens.
    ignore = " \t"

    # ------------------------------------------------------------------
    # MEMBER 2: operators, parentheses, and semicolon
    # TODO: Put longer operators before their shorter prefixes.
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # MEMBER 3: integer, identifier, and case-sensitive keywords
    # TODO: Add the integer/identifier rules and keyword mapping.
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # MEMBER 5: string and comments
    # TODO: Ignore // comments and /* ... */ comments, including multiline.
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # MEMBER 6: line counting and lexical errors
    # This newline rule makes the starter class buildable before token rules
    # are added. Expand its tests as the lexer is implemented.
    # ------------------------------------------------------------------
    @_(r"\n+")
    def ignore_newlines(self, token):
        self.lineno += token.value.count("\n")

    def error(self, token):
        unexpected = token.value[0]
        raise LexicalError(f"Lexical error: unexpected character {unexpected}")

