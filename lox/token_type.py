from enum import Enum

class TokenType(Enum):
    #single-character tokens
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'
    COMMA = ','
    DOT = '.'
    MINUS = '-'
    PLUS = '+'
    SEMICOLON = ';'
    STAR = '*'
    SLASH = '/'

    # one or two character token
    EQUAL = '='
    EQUAL_EQUAL = '=='
    BANG = "!"
    BANG_EQUAL = "!="
    LESS = "<"
    LESS_EQUAL = "<="
    GREATER = ">"
    GREATER_EQUAL = ">="

    # literals
    STRING = '"'
    # end-of-file
    EOF = ''

    # identifiers
    IDENTIFIER = 'identifier'
    NUMBER ='number'

    #keywords
    AND = 'and'
    CLASS = 'class'
    ELSE = 'else'
    FALSE = 'false'
    FOR = 'for'
    FUN = 'fun'
    IF = 'if'
    NIL = 'nil'
    OR = 'or'
    PRINT = 'print'
    RETURN = 'return'
    SUPER = 'super'
    THIS = 'this'
    TRUE = 'true'
    VAR = 'var'
    WHILE = 'while'


