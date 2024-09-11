import Expr
from tokens import Token
from token_type import TokenType


class Parser:
    def __init__(self, tokens: list[Token]):
        # consumes a flat input sequence of tokens
        # current points to the next token waiting to be parsed
        self.current = 0
        self.tokens = tokens

    # rule 1: experssions -> equality
    def expression(self):
        return self.equality()

    # rule 2: equality → comparison ( ( "!=" | "==" ) comparison )*
    def equality(self):
        expr: Expr.Expr = self.comparison()

        while(self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)):
            operator: Token = self.previous()
            right: Expr.Expr = self.comparison()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr.Expr:
        pass