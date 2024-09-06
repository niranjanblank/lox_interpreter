from token_type import TokenType
from tokens import Token, KEYWORDS
from typing import List, Optional, Any



class Scanner:

    def __init__(self, source: str):
        self.source = source
        self.tokens: List[Token] = []
        # scans the first character in the lexeme being scanned
        self.start = 0
        # points at the character that is currently being considered
        self.current = 0
        # tracks what source line current is on, so we can produce tokens that know their location
        self.line = 1

    def is_at_end(self) -> bool:
        """
        Helper function to tell us we've consumed all the characters
        """
        return self.current >= len(self.source)

    def advance(self):
        # get the character at current and increase the current
        curr = self.source[self.current]
        self.current += 1
        return curr

    def match(self, expected: str):
        if self.is_at_end(): return False

        if self.source[self.current] != expected: return False

        self.current += 1
        return True

    def add_token(self, type: TokenType, literal: Optional[Any] = None) -> None:
        if literal is None:
            literal = "null"
        text = self.source[self.start: self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def peek(self):
        # this is a lookahead function, it looks at the unconsumed current character
        # "\0" means null character, which indicates end of a string
        if self.is_at_end(): return "\0"
        # if we arent at the end, we return the current character
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source): return '\0'
        return self.source[self.current + 1]

    def string(self):
        from lox import Lox
        # for reading string literals
        # string starts with '"', so now we look for the end of string by finding '"'
        while self.peek() != '"' and not self.is_at_end():
            # if we find new line, we increase the line number
            if self.peek() == "\n": self.line += 1
            # now increase the position of current char
            self.advance()
        # checking if we are at the end of string before finding the closing string "
        if self.is_at_end():
            Lox.error(self.line, "Unterminated string.")
            return
        # if we arent at the end of string, we found the closing string as we are out of the loop
        self.advance()

        # getting the string value between the two ""
        value = self.source[self.start + 1: self.current - 1]
        self.add_token(TokenType.STRING, value)

    def is_digit(self, c):
        # here c is string as we read from the file, its ascii value is compared with '0' and '9'
        # to find out if its number
        return c >= '0' and c <= '9'

    def number(self):
        # if the lookahead is digit, consume it and continue
        while self.is_digit(self.peek()): self.advance()

        # look for a fractional part
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()

            #     continue until we have digit
            while self.is_digit(self.peek()): self.advance()

        num_value = self.source[self.start: self.current]

        self.add_token(TokenType.NUMBER, float(num_value))

    def is_alpha(self, c):
        return ('a' <= c <= 'z') \
            or ('A' <= c <= 'Z') \
            or (c == '_')

    def is_alpha_numeric(self, c):
        return self.is_alpha(c) or self.is_digit(c)

    def identifier(self):
        while self.is_alpha_numeric(self.peek()): self.advance()
        text = self.source[self.start:self.current]
        type = KEYWORDS.get(text, TokenType.IDENTIFIER)

        self.add_token(type)

    def scan_token(self):
        from lox import Lox
        char = self.advance()

        match char:
            case "(":
                self.add_token(TokenType.LEFT_PAREN)
            case ")":
                self.add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.add_token(TokenType.LEFT_BRACE)
            case "}":
                self.add_token(TokenType.RIGHT_BRACE)
            case ',':
                self.add_token(TokenType.COMMA)
            case '.':
                self.add_token(TokenType.DOT)
            case '-':
                self.add_token(TokenType.MINUS)
            case '+':
                self.add_token(TokenType.PLUS)
            case ';':
                self.add_token(TokenType.SEMICOLON)
            case '*':
                self.add_token(TokenType.STAR)
            case "=":
                if self.match("="):
                    self.add_token(TokenType.EQUAL_EQUAL)
                else:
                    self.add_token(TokenType.EQUAL)
            case "!":
                if self.match("="):
                    self.add_token(TokenType.BANG_EQUAL)
                else:
                    self.add_token(TokenType.BANG)
            case "<":
                if self.match("="):
                    self.add_token(TokenType.LESS_EQUAL)
                else:
                    self.add_token(TokenType.LESS)
            case ">":
                if self.match("="):
                    self.add_token(TokenType.GREATER_EQUAL)
                else:
                    self.add_token(TokenType.GREATER)
            case '/':
                if self.match("/"):
                    # this indicates that the comment has started
                    # if its comment we ignore it and all of the comment
                    while self.peek() != "\n" and not self.is_at_end():
                        # until we reach the end of line(which indicates the end of comment)
                        # or we reach end of the file, we keep on looping
                        # and increase the self.current(inside advance())
                        self.advance()
                else:
                    # if its not comments, we append it to the token list
                    self.add_token(TokenType.SLASH)
            # ignoring white space
            case ' ' | '\t' | '\r':
                pass  # do nothing
            case '\n':
                self.line += 1
            case '"':
                self.string()
            case _:
                if self.is_digit(char):
                    self.number()
                elif self.is_alpha(char):
                    self.identifier()
                else:
                    Lox.error(self.line, f"Unexpected character: {char}")

    def scan_tokens(self):
        # go through the source and scan tokens
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        # at the end add EOF token
        self.tokens.append(Token(TokenType.EOF, "", "null", self.line))
