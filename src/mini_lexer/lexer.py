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
    # MEMBER 5: string and comments
    #
    # Keep these function rules before operator rules so // and /* are
    # recognized before a future DIVIDE rule can match their first slash.
    # ------------------------------------------------------------------
    @_(r'"[^"\n]*"')
    def STRING(self, token):
        """Match a double-quoted string and preserve its quotes."""
        return token

    @_(r'//[^\n]*')
    def LINE_COMMENT(self, token):
        """Ignore a single-line comment, including one ending at EOF."""
        pass

    @_(r'/\*[\s\S]*?\*/')
    def BLOCK_COMMENT(self, token):
        """Ignore a block comment and account for its newlines."""
        self.lineno += token.value.count("\n")

    @_(r'/\*(?:(?!\*/)[\s\S])*\Z')
    def UNTERMINATED_BLOCK_COMMENT(self, token):
        """Reject a block comment that has no closing delimiter."""
        raise LexicalError("Lexical error: unterminated block comment")

    # ------------------------------------------------------------------
    # MEMBER 2: operators, parentheses, and semicolon
    # Two-character operators must appear before single-character operators.
    # ------------------------------------------------------------------
    GE = r'>='
    LE = r'<='
    EQ = r'=='
    INCREMENT = r'\+\+'
    DECREMENT = r'--'
    
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    ASSIGN = r'='
    GT = r'>'
    LT = r'<'
    
    LPAREN = r'\('
    RPAREN = r'\)'
    SEMICOLON = r';'
    
    # ------------------------------------------------------------------
    # MEMBER 3: integer, identifier, and case-sensitive keywords
    # TODO: Add the integer/identifier rules and keyword mapping.
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

