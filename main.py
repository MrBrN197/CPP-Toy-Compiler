# c++ compiler
from enum import Enum

class TokenType(Enum):
    PLUS = '+'
    MINUS = '-'
    MULTIPLY = '*'
    DIV = '/'
    ASIGN = '='
    LPAREN = '('
    RPAREN = ')'
    LSQUARE = '['
    RSQUARE = ']'
    LCURLY = '{'
    RCURLY = '}'
    SEMI = ';'
    ID = 'ID'
    INTEGER = 'INTEGER'

class Token:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value
    def __str__(self):
        return f'<Token>: {self.token_type:<20} Value: {self.value}'

    __repr__ = __str__


class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def advance(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def get_integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isnumeric():
            result += self.current_char
            self.advance()
        value = int(result)
        return Token(TokenType('INTEGER'), value)

    def get_id(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return Token(TokenType('ID'), result)


    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isnumeric():
                return self.get_integer()
            if self.current_char.isalpha():
                return self.get_id()
            token_type = TokenType(self.current_char)
            self.advance()
            return Token(token_type)

with open("test.cpp") as fp:
    text = fp.read()
    tokenizer = Tokenizer(text)
    token = tokenizer.get_next_token()
    while token is not None:
        print(token)
        token = tokenizer.get_next_token()
    