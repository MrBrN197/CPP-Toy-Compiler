# c++ compiler

class Token:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f'<Token>: {self.name}'

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
        
    def get_alphanumeric(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return Token(result)


    def get_next_token(self):
        result = ''
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isalnum():
                return self.get_alphanumeric()
            if self.current_char == '=':
                self.advance()
                return Token('=')
            if self.current_char == '+':
                self.advance()
                return Token('+')
            if self.current_char == '-':
                self.advance()
                return Token('-')
            if self.current_char == '*':
                self.advance()
                return Token('*')
            if self.current_char == '/':
                self.advance()
                return Token('/')
            assert False


tokenizer = Tokenizer("int a = b + c")
token = tokenizer.get_next_token()
while token is not None:
    print(token)
    token = tokenizer.get_next_token()
