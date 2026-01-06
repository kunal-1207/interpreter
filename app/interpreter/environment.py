class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        
        # If we don't find it in this environment, check the enclosing one
        if self.enclosing is not None:
            return self.enclosing.get(name)
            
        raise RuntimeError(f"Undefined variable '{name.lexeme}'.")

    def assign(self, name, value):
        # If the variable exists in this environment, update it
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
            
        # If not found in this environment, try the enclosing one
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
            
        raise RuntimeError(f"Undefined variable '{name.lexeme}'.")