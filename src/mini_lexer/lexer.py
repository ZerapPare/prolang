"""SLY token rules for operators, values, keywords, and comments."""

from __future__ import annotations

from sly import Lexer


class LexicalError(Exception):
    """Raised when the lexer finds an unexpected character."""


class MiniLexer(Lexer):
    """Convert source text into tokens and reject lexical errors."""

    tokens = {
        # operators
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
        # parentheses and semicolon
        LPAREN,
        RPAREN,
        SEMICOLON,
        # values and words
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
        # string
        STRING,
    }

    # Spaces and tabs are not tokens.
    ignore = " \t"

    # ------------------------------------------------------------------
    # Strings and comments
    #
    # Keep these function rules before operator rules so // and /* are
    # recognized before DIVIDE can match their first slash.
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
    # Operators, parentheses, and semicolon
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
    # Integers, identifiers, and case-sensitive keywords
    # ------------------------------------------------------------------
    # Invalid identifiers
    @_(r"\d+[a-zA-Z][a-zA-Z0-9_]*")
    def INVALID_IDENTIFIER_STARTS_WITH_DIGIT(self, token):
        raise LexicalError(
            f"Lexical error: identifier '{token.value}' "
            "must not start with a digit"
        )

    @_(r"[a-zA-Z][a-zA-Z0-9]*_[a-zA-Z0-9_]*")
    def INVALID_IDENTIFIER_CONTAINS_UNDERSCORE(self, token):
        raise LexicalError(
            f"Lexical error: identifier '{token.value}' "
            "must not contain underscore"
        )

    @_(r"_[a-zA-Z0-9_]*")
    def INVALID_IDENTIFIER_STARTS_WITH_UNDERSCORE(self, token):
        raise LexicalError(
            f"Lexical error: identifier '{token.value}' "
            "must start with an English letter"
        )
    INTEGER = r"\d+"
    IDENTIFIER = r"[a-zA-Z][a-zA-Z0-9]*"
    IDENTIFIER["if"] = IF
    IDENTIFIER["then"] = THEN
    IDENTIFIER["else"] = ELSE
    IDENTIFIER["endif"] = ENDIF
    IDENTIFIER["while"] = WHILE
    IDENTIFIER["do"] = DO
    IDENTIFIER["endwhile"] = ENDWHILE
    IDENTIFIER["print"] = PRINT
    IDENTIFIER["newline"] = NEWLINE
    IDENTIFIER["read"] = READ

    # ------------------------------------------------------------------
    # Line counting and lexical errors
    # Accept both LF and Windows CRLF line endings.
    # ------------------------------------------------------------------
    @_(r"(?:\r?\n)+")
    def ignore_newlines(self, token):
        self.lineno += token.value.count("\n")

    def error(self, token):
        unexpected = token.value[0]
        raise LexicalError(f"Lexical error: unexpected character {unexpected}")

