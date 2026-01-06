import sys
from app.token.token_type import TokenType
from app.token.token import Token


class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        
        self.keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE,
            "not": TokenType.BANG
        }

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self):
        return self.current >= len(self.source)

    def scan_token(self):
        char = self.advance()
        
        # Single-character tokens
        if char == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif char == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif char == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif char == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif char == ',':
            self.add_token(TokenType.COMMA)
        elif char == '.':
            self.add_token(TokenType.DOT)
        elif char == '-':
            self.add_token(TokenType.MINUS)
        elif char == '+':
            self.add_token(TokenType.PLUS)
        elif char == ';':
            self.add_token(TokenType.SEMICOLON)
        elif char == '*':
            self.add_token(TokenType.STAR)
        # One or two character tokens
        elif char == '!':
            self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif char == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif char == '<':
            self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif char == '>':
            self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
        # Slash could be a comment or division operator
        elif char == '/':
            if self.match('/'):
                # A comment goes until the end of the line
                while self.peek() != '\n' and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        # Whitespace
        elif char == ' ' or char == '\r' or char == '\t':
            pass  # Ignore whitespace
        elif char == '\n':
            self.line += 1
        # String literals
        elif char == '"':
            self.string()
        else:
            # Number literals
            if self.is_digit(char):
                self.number()
            # Identifier or keyword
            elif self.is_alpha(char):
                self.identifier()
            else:
                self.error(self.line, "Unexpected character.")

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        
        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.error(self.line, "Unterminated string.")
            return

        # The closing ".
        self.advance()

        # Trim the surrounding quotes.
        value = self.source[self.start + 1:self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        while self.is_digit(self.peek()):
            self.advance()

        # Look for a fractional part.
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            # Consume the "."
            self.advance()

            while self.is_digit(self.peek()):
                self.advance()
        
        value = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, value)

    def identifier(self):
        while self.is_alphanumeric(self.peek()):
            self.advance()
        
        text = self.source[self.start:self.current]
        type = self.keywords.get(text)
        if type is None:
            type = TokenType.IDENTIFIER
        
        self.add_token(type)

    def is_digit(self, char):
        return char >= '0' and char <= '9'

    def is_alpha(self, char):
        return (char >= 'a' and char <= 'z') or \
               (char >= 'A' and char <= 'Z') or \
               char == '_'

    def is_alphanumeric(self, char):
        return self.is_alpha(char) or self.is_digit(char)

    def add_token(self, type, literal=None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def error(self, line, message):
        self.report(line, "", message)

    def report(self, line, where, message):
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        sys.exit(1)