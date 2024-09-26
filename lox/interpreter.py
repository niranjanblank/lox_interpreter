import Expr
from token_type import TokenType
from runtime_error import LoxRuntimeError



class Interpreter(Expr.ExprVisitor):
    pass

    def evaluate(self, expr: Expr.Expr):
        return expr.accept(self)

    def is_truthy(self, value):
        # Handle string representations of 'true' and 'false'
        # false and nil are false, other everything is True
        if isinstance(value, str):
            if value == "false":
                return False
            elif value == "nil":
                return False

        # Everything else is considered truthy
        return True
    def is_equal(self, a,b):
        # checks if the pass arguments are equal
        return a == b

    def stringify(self, object):
        # converts string to value
        if object is None: return "nil"
        if type(object) == float:
            text = str(object)
            if text.endswith(".0"):
                text= text[0:len(text)-2]
            return text

        return str(object)

    def check_number_operand(self, operator, operand):
        from lox import Lox
        # check the type of operand
        if (type(operand) == float): return
        raise LoxRuntimeError(operator, "Operand must be a number.")

    def check_number_operands(self, operator, left,right):
        if type(left) == float and type(right) == float: return
        raise LoxRuntimeError(operator, "Operands must be numbers.")

    def visit_literal_expr(self, expr: 'Expr.Literal'):
        return expr.value

    def visit_grouping_expr(self, expr: 'Expr.Grouping'):
        return self.evaluate(expr.expression)

    def visit_unary_expr(self, expr: 'Expr.Unary'):
        right = self.evaluate(expr.right)
        match expr.operator.type:
            case TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -float(right)
            case TokenType.BANG:
                if self.is_truthy(right):
                    return "false"
                return "true"
                # return not self.is_truthy(right)
        # unreachable
        return None

    def visit_binary_expr(self, expr: 'Expr.Binary'):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                # checking object type
                self.check_number_operands(expr.operator, left,right)
                return float(left) - float(right)
            case TokenType.SLASH:
                self.check_number_operands(expr.operator, left, right)
                return float(left) / float(right)
            case TokenType.STAR:
                self.check_number_operands(expr.operator, left, right)
                return float(left) * float(right)
            case TokenType.PLUS:
                if type(left) == float and type(right) == float:
                    return float(left) + float(right)
                elif type(left) == str and type(right) == str:
                    return str(left) + str(right)
                raise LoxRuntimeError(expr.operator, "Operands must be two numbers or two strings.")
            case TokenType.GREATER:
                self.check_number_operands(expr.operator, left,right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.check_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self.check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)
            case TokenType.BANG_EQUAL:
                return not self.is_equal(left, right)
            case TokenType.EQUAL_EQUAL:
                return self.is_equal(left, right)
            case _:
                pass
        return None

    def interpret(self, expr):
        from lox import Lox
        try:
            value = self.evaluate(expr)
            print(self.stringify(value))
        except RuntimeError as error:
            Lox.runtime_error(error)

