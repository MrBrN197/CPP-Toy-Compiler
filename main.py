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
    TYPE = 'TYPE'
    INTEGER = 'INTEGER'
    ASSIGN = '='
    COMMA = ','

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
        if result in ("int", "double", "float"): # TODO: deal with all type variations
            return Token(TokenType('TYPE'), result)
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

class Block:
    def __init__(self, exprs):
        self.exprs = exprs

class Var:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class Function:
    def __init__(self, name, params=None, block=None):
        self.name = name
        self.param_nodes = params
        self.block_node = block

class Assignment:
    def __init__(self, var, expr):
        self.var_node = var
        self.expr_node = expr


class Symbol:
    def __init__(self, name):
        self.name = name
    
class BuiltInType(Symbol):
    def __init__(self, name):
        super().__init__(name)

class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name)
        self.type = type

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def lookup(self, type):
        return self.symbols.get(type, None)

    def _init_built_in_types():
        self.insert(BuiltInType('void'))
        self.insert(BuiltInType('int'))
        self.insert(BuiltInType('float'))
        self.insert(BuiltInType('double'))
    def insert(self, symbol):
        self.symbols[symbol.name] = symbol


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, type):
        if self.current_token.type != type:
            raise Exception(f"Syntax Error: {type}")
        self.current_token = self.lexer.get_next_token()

    def term(self):
        """ term: factor ((MULTIPLY|DIV) factor)* """
        node = self.factor()
        while self.current_token.type in (TokenType.MULTIPLY, TokenType.DIV):
            op = self.current_token.value
            if self.current_token.type == TokenType.MULTIPLY:
                self.eat(TokenType.MULTIPLY)
            else:
                self.eat(TokenType.DIV)
            node = BinOp(node, op, self.factor())
        return node

    def factor(self):
        """factor: INTEGER"""
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

    def assignment(self):
        """ assignment: TYPE ID ASSIGN expr """
        var_type = self.current_token.value 
        self.eat(TokenType.TYPE)
        var_name = self.current_token.value 
        self.eat(TokenType.ID)
        self.eat(TokenType.ASSIGN)
        expression = self.expr()
        return Assignment(Var(var_name, var_type), expression)

    def scope(self):
        """ scope: LCURLY (expr|assignment)* RCULRY """
        self.eat(TokenType.LCURLY)
        expressions = []
        while self.current_token and self.current_token.type in (TokenType.INTEGER, TokenType.TYPE):
            if self.current_token.type == TokenType.INTEGER:
                expressions.append(self.expr())
            else:
                expressions.append(self.assignment())
        self.eat(TokenType.RCURLY)
        return expressions

    def function(self):
        """ function: TYPE ID LPAREN (parameter-list)? RPAREN LCURLY scope RCURLY """
        self.eat(TokenType.TYPE)
        name = self.current_token.value
        self.eat(TokenType.ID)
        self.eat(TokenType.LPAREN)
        param_list = []
        if(self.current_token.type == TokenType.TYPE):
            param_list = self.parameter_list()
        self.eat(TokenType.RPAREN)
        block = Block(self.scope())
        return Function(name, params=param_list, block=block)

    def parameter(self):
        """ parameter: TYPE ID """
        self.eat(TokenType.TYPE)
        self.eat(TokenType.ID)
        return None

    def parameter_list(self):
        """ parameter-list: parameter (COMMA parameter)* """
        param_list = [self.parameter()]
        while self.current_token.type == TokenType.COMMA:
            self.eat(TokenType.COMMA)
            param_list.append(self.parameter())
        return None

    def parser(self):
        """ gramar rules """
        """
        function: TYPE ID LPAREN (parameter-list)? RPAREN LCURLY scope RCURLY
        parameter-list: parameter (COMMA parameter)*
        parameter: TYPE ID
        scope: LCURLY (expr|assignment)* RCULRY
        assignment: TYPE ID ASSIGN expr
        expr: term ((PLUS|MINUS) term)* SEMI
        factor: INTEGER
        """ 
        return self.function()



with open("test.cpp") as fp:
    text = fp.read()
    tokenizer = Tokenizer(text)

    parser = Parser(tokenizer)

    main_function = parser.parser()

    print(main_function)
