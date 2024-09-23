import Expr
from token_type import TokenType


class Interpreter(Expr.ExprVisitor):
    pass

    def evaluate(self, expr: Expr.Expr):
        return expr.accept(self)

    def isTruthy(self, object):
        # false and null are false, everything else is truth
        if object is None or bool(object) is False:
            return False
        return True

    def visit_literal_expr(self, expr: 'Expr.Literal'):
        return expr.value

    def visit_grouping_expr(self, expr: 'Expr.Grouping'):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: 'Expr.Unary'):
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                return -float(right)
            case TokenType.BANG:
                return not self.isTruthy(right)
        # unreachable
        return None

    def visit_binary_expr(self, expr: 'Expr.Binary'):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                return float(left) - float(right)
            case TokenType.SLASH:
                return float(left) / float(right)
            case TokenType.STAR:
                return float(left) * float(right)
            case TokenType.PLUS:
                if type(left) == float and type(right) == float:
                    return float(left) + float(right)
                elif type(left) == str and type(right) == str:
                    return str(left) + str(right)
            case TokenType.GREATER:
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                return float(left) >= float(right)
            case TokenType.LESS:
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL:
                return float()
            case _:
                pass
        return None
