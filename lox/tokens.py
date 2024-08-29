from app.token_type import TokenType
from typing import Any, Tuple, Dict

_keywords: Tuple[str] = (
    'and', 'class', 'else', 'false', 'for', 'fun', 'if', 'nil',
    'or', 'print', 'super', 'this', 'true', 'var', 'while', 'return'
)

KEYWORDS: Dict[str, TokenType] = {key: TokenType(key) for key in _keywords}


class Token:
    def __init__(self,
                 type: TokenType,
                 lexeme: str,
                 literal: Any,
                 line: int
                 ):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        return f"{self.type.name} {self.lexeme} {self.literal}"
