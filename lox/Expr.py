from typing import List, Any
from tokens import Token


class Expr:
    pass


class Binary(Expr):
    def __init__(self, left: Expr, right: Expr):
        self.left = left
        self.right = right
        pass


class Grouping(Expr):
    def __init__(self, expression: Expr):
        self.expression = expression
        pass


class Literal(Expr):
    def __init__(self, value: Any):
        self.value = value
        pass


class Unary(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right
        pass


