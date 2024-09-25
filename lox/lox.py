import sys
from sys import argv
from scanner import Scanner
from tokens import  Token
from token_type import TokenType
from parser import Parser
from ast_printer import AstPrinter
from interpreter import Interpreter
class Lox:
    had_error = False
    had_runtime_error = False
    interpreter = Interpreter()

    @staticmethod
    def scanner_error(line: int, message: str):
        Lox.report(line, "", message)

    @staticmethod
    def error(token: Token, message: str):
        if token.type == TokenType.EOF:
            Lox.report(token.line, ' at end', message)
        else:
            Lox.report(token.line,f" at '{token.lexeme}'", message)

    @staticmethod
    def runtime_error(error):
        print(f"{error}\n[line {error.token.line}]")
        Lox.had_runtime_error = True

    @staticmethod
    def report(line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        Lox.had_error = True

    @staticmethod
    def run_file(filename):
        with open(filename) as file:
            file_contents = file.read()

        Lox.run(file_contents)

        if Lox.had_error:
            exit(65)
        elif Lox.had_runtime_error:
            exit(70)
        else:
            exit(0)

    @staticmethod
    def run(source):
        if source:
            scanner = Scanner(source)
            scanner.scan_tokens()
            # for token in scanner.tokens:
            #     print(token)
            parser = Parser(scanner.tokens)
            expression = parser.parse()

            # stop if there is syntax error
            if Lox.had_error: return

            Lox.interpreter.interpret(expression)
            printer = AstPrinter()
            print(printer.print(expression))
        else:
            print("EOF  null")

    @staticmethod
    def run_prompt():
        while True:
            try:
                print('>>> ', end='')
                expr = input()
                if expr.strip() == 'exit':
                    exit()
                else:
                    Lox.run(expr)
                    Lox.had_error = False
            except Exception as e:
                print(f"Error: {e}")

    @staticmethod
    def main(args):
        if len(args) > 1:
            exit(64)
        elif len(args) == 1:
            Lox.run_file(args[0])
        else:
            Lox.run_prompt()
