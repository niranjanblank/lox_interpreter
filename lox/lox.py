import sys
from sys import argv
from scanner import Scanner


class Lox:
    had_error = False

    @staticmethod
    def error(line: int, message: str):
        Lox.report(line, "", message)

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
        else:
            exit(0)

    @staticmethod
    def run(source):
        if source:
            scanner = Scanner(source)
            scanner.scan_tokens()
            for token in scanner.tokens:
                print(token)
        else:
            print("EOF  null")

    @staticmethod
    def run_prompt():
        while True:
            print('>>> ', end='')
            expr = input()
            first = expr.split(' ')[0]
            if first == 'exit':
                exit()
            else:
                Lox.run(expr)
                Lox.had_error = False

    @staticmethod
    def main(args):
        if len(args) > 1:
            exit(64)
        elif len(args) == 1:
            Lox.run_file(args[0])
        else:
            Lox.run_prompt()
