import sys
from app.scanner.scanner import Scanner
from app.parser.parser import Parser
from app.ast.ast_printer import AstPrinter
from app.interpreter.interpreter import Interpreter


def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize" and command != "parse" and command != "ast-print" and command != "interpret":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()
    
    scanner = Scanner(file_contents)
    tokens = scanner.scan_tokens()
    
    if command == "tokenize":
        for token in tokens:
            print(token)
    elif command == "parse" or command == "ast-print" or command == "interpret":
        parser = Parser(tokens)
        statements = parser.parse()
        if command == "parse":
            for statement in statements:
                print(statement)
        elif command == "ast-print":
            # For simplicity, we'll just print the first statement's expression
            if statements:
                printer = AstPrinter()
                if hasattr(statements[0], 'expression'):
                    print(printer.print(statements[0].expression))
        else:
            interpreter = Interpreter()
            interpreter.interpret(statements)


if __name__ == "__main__":
    main()