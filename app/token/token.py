class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        # Format: TYPE lexeme literal
        # For tokens without literals, use "null"
        literal_str = self.literal if self.literal is not None else "null"
        return f"{self.type.value} {self.lexeme} {literal_str}"

    def __repr__(self):
        return self.__str__()