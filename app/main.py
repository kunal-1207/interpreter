import sys

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    # Tokenize the input for parentheses
    tokens = []
    for char in file_contents:
        if char == '(':
            tokens.append("LEFT_PAREN  ( null")
        elif char == ')':
            tokens.append("RIGHT_PAREN  ) null")

    # Print tokens or EOF if no tokens are found
    if tokens:
        for token in tokens:
            print(token)
    else:
        print("EOF  null")

if __name__ == "__main__":
    main()
