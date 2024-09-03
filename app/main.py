import sys

class Token:
    def __init__(self, type, value, literal):
        self.type = type
        self.value = value
        self.literal = literal
    
    def __str__(self):
        return f"{self.type} {self.value} {self.literal}"

def main():
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    try:
        with open(filename) as file:
            file_contents = file.read()
    except IOError:
        print(f"Could not open or read file: {filename}", file=sys.stderr)
        exit(1)

    # Tokenize the input for parentheses
    tokens = []
    for char in file_contents:
        if char == '(':
            tokens.append(Token("LEFT_PAREN", "(", "null"))
        elif char == ')':
            tokens.append(Token("RIGHT_PAREN", ")", "null"))

    # Print tokens or EOF if no tokens are found
    if tokens:
        for token in tokens:
            print(token)
    else:
        print("EOF  null")  # Ensure there's a space between EOF and null

if __name__ == "__main__":
    main()
