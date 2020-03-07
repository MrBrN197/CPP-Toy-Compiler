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
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
    def __str__(self):
        return f'<Token>: {self.type:<20} Value: {self.value}'

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
            return Token(token_type, token_type.value)


class Constant():
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f'<Constant>: {self.value}'
    __repr__ = __str__
        
class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, type):
        if self.current_token.type != type:
            raise Exception(f"Syntax Error: {type}")
        self.current_token = self.lexer.get_next_token()

    def term(self):
        """term: INTEGER"""
        value = self.current_token.value
        self.eat(TokenType.INTEGER)
        return Constant(value)

    def expr(self):
        """expr: term ((PLUS|MINUS) term)* SEMI """

        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current_token.value
            if self.current_token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            else:
                self.eat(TokenType.MINUS)
            node = BinOp(node, op, self.term())
        self.eat(TokenType.SEMI)
        return node

    def scope(self):
        """ scope: LCURLY expr* RCULRY """
        self.eat(TokenType.LCURLY)
        expressions = []
        while self.current_token and self.current_token.type == TokenType.INTEGER:
            expressions.append(self.expr())
        self.eat(TokenType.RCURLY)
        return expressions

    def parser(self):
        """ gramar rules """
        """
        scope: expr*
        expr: term ((PLUS|MINUS) term)* SEMI
        factor: INTEGER
        """ 
        return self.scope()



with open("test.cpp") as fp:
    text = fp.read()
    tokenizer = Tokenizer(text)

    tokenizer.get_next_token() # skip int
    tokenizer.get_next_token() # skip main
    tokenizer.get_next_token() # skip LPAREN
    tokenizer.get_next_token() # skip RPAREN

    parser = Parser(tokenizer)

    block = parser.parser()

    print(len(block))
