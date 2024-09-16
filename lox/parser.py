import Expr
from tokens import Token
from token_type import TokenType

"""
The rules for lox are:

expression     → equality ;
equality       → comparison ( ( "!=" | "==" ) comparison )* ;
comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
term           → factor ( ( "-" | "+" ) factor )* ;
factor         → unary ( ( "/" | "*" ) unary )* ;
unary          → ( "!" | "-" ) unary
               | primary ;
primary        → NUMBER | STRING | "true" | "false" | "nil"
               | "(" expression ")" ;

"""


class ParseError(RuntimeError):
    def __init__(self, token: Token, message: str) -> None:
        super().__init__(message)
        self.token = token


class Parser:
    """
    We are using recursive descent technique for parsing
    Recursive descent is considered a top-down parser because it starts from the top or outermost grammar
     rule (here expression) and works its way down into the nested subexpressions before finally reaching the
     leaves of the syntax tree.
    """

    def __init__(self, tokens: list[Token]):
        # consumes a flat input sequence of tokens
        # current points to the next token waiting to be parsed
        self.current = 0
        self.tokens = tokens

    def is_at_end(self) -> bool:
        """
        Helper function to tell us we've consumed all the characters
        """
        return self.peek().type == TokenType.EOF
    def peek(self):
        # peek the current token value without consuming
        return self.tokens[self.current]

    def previous(self):
        # return the previous consumed token
        return self.tokens[self.current - 1]

    def advance(self):
        # consumes the current token and returns it
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def check(self, type: TokenType):
        # see if we are at the end, dont proceed if we are at the end
        if self.is_at_end(): return False
        return self.peek().type == type

    def match(self, *types) -> bool:
        # all the types passed through the match are checked
        for token_type in types:
            # check if the current token has any of the given types
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, type, message):
        # if the next token is of the expected type
        if self.check(type): return self.advance()
        return self.error(self.peek(), message)

    @staticmethod
    def error(token, message) -> ParseError:
        from lox import Lox
        Lox.error(token, message)
        return ParseError(token, message)

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            if self.peek().type in (
                    TokenType.CLASS,
                    TokenType.FUN,
                    TokenType.VAR,
                    TokenType.FOR,
                    TokenType.IF,
                    TokenType.WHILE,
                    TokenType.PRINT,
                    TokenType.RETURN):
                return
            self.advance()

    # rule 1: expressions -> equality
    def expression(self):
        return self.equality()

    # rule 2: equality → comparison ( ( "!=" | "==" ) comparison )*
    def equality(self):
        expr: Expr.Expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator: Token = self.previous()
            right: Expr.Expr = self.comparison()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def comparison(self) -> Expr.Expr:
        expr: Expr.Expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator: Token = self.previous()
            right: Expr.Expr = self.term()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def term(self):
        expr: Expr.Expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator: Token = self.previous()
            right: Expr.Expr = self.factor()
            expr: Expr.Expr = Expr.Binary(expr, operator, right)

        return expr

    def factor(self):
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator: Token = self.previous()
            right: Expr.Expr = self.unary()
            expr: Expr.Expr = Expr.Binary(expr, operator, right)

        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator: Token = self.previous()
            right: Expr.Expr = self.unary()
            return Expr.Unary(operator, right)

        # if we dont have - or !, it must be primary
        return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE): return Expr.Literal("false")
        if self.match(TokenType.TRUE): return Expr.Literal("true")
        if self.match(TokenType.NIL): return Expr.Literal("nil")

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Expr.Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr: Expr.Expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)

        raise self.error(self.peek(), "Expect expression.")

    def parse(self):
        try:
            return self.expression()
        except ParseError:
            return None

