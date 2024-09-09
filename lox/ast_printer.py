import Expr
from tokens import Token
from token_type import TokenType


class AstPrinter(Expr.ExprVisitor):
    def print(self, expr: Expr.Expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr: 'Expr'):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: 'Expr'):
        return self.parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: 'Expr'):
        if expr.value is None: return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: 'Expr'):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *exprs):
        string = ''.join(expr.accept(self) for expr in exprs)

        return f'({name} {string})'


if __name__ == '__main__':
    exp = Expr.Binary(
        Expr.Unary(
            Token(TokenType.MINUS, '-', '', 1),
            Expr.Literal(123)
        ),
        Token(TokenType.STAR, '*', '', 1),
        Expr.Grouping(Expr.Literal(45.67))
    )


    printer = AstPrinter()
    print(printer.print(exp))
