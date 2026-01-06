# Lox Interpreter

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![Status](https://img.shields.io/badge/Status-Active-success.svg)](STATUS)

A tree-walk interpreter for the Lox programming language, built as part of the [CodeCrafters Interpreter Challenge](https://app.codecrafters.io/courses/interpreter/overview). This implementation follows the book [Crafting Interpreters](https://craftinginterpreters.com/) by Robert Nystrom.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [File Structure](#file-structure)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [License](#license)

## 📘 Overview

This project implements a complete interpreter for the Lox programming language. Lox is a simple scripting language designed to teach programming language implementation concepts. The interpreter follows a tree-walk approach, parsing source code into an Abstract Syntax Tree (AST) and then executing it.

### Key Concepts Implemented
- **Tokenization**: Converting source code into tokens
- **Parsing**: Building Abstract Syntax Trees (ASTs) from tokens
- **Tree-walk Interpretation**: Executing the AST
- **Variable Scoping**: Implementing lexical scoping
- **Control Flow**: Conditional statements and loops
- **Functions**: First-class functions with closures

## ✨ Features

- ✅ Full Lox language support
- ✅ Recursive descent parser
- ✅ Tree-walk interpreter
- ✅ Lexical scoping
- ✅ Native functions
- ✅ Error handling and reporting
- ✅ Object-oriented programming constructs
- ✅ Garbage collection (basic)

## 🚀 Installation

### Prerequisites
- Python 3.12 or higher

### Setup
```bash
# Clone the repository
git clone https://github.com/kunal-1207/interpreter.git

# Navigate to the project directory
cd interpreter

# Install dependencies (if any)
pip install -r requirements.txt  # if requirements file exists
```

## 📖 Usage

### Running the Interpreter
```bash
# Execute the interpreter
python app/main.py

# Or use the provided script
./your_program.sh
```

### Example Usage
```python
# Example Lox code
greet = "Hello, World!"
print greet

# Functions
def square(x) {
  return x * x;
}

print square(4);  # Output: 16
```

## 🏗️ Architecture

The interpreter is structured into several key components:

1. **Scanner (Tokenizer)**: Converts source code into a sequence of tokens
2. **Parser**: Transforms tokens into an Abstract Syntax Tree (AST)
3. **Interpreter**: Executes the AST to produce results
4. **Environment**: Manages variable bindings and scoping

### Core Components
- `app/scanner/`: Tokenization logic
- `app/parser/`: AST generation
- `app/interpreter/`: Execution engine
- `app/ast/`: AST node definitions
- `app/token/`: Token definitions and types

## 📁 File Structure
```
interpreter/
├── app/
│   ├── ast/
│   │   ├── __init__.py
│   │   ├── ast_printer.py
│   │   └── expr.py
│   ├── interpreter/
│   │   ├── __init__.py
│   │   ├── environment.py
│   │   └── interpreter.py
│   ├── parser/
│   │   ├── __init__.py
│   │   └── parser.py
│   ├── scanner/
│   │   ├── __init__.py
│   │   └── scanner.py
│   ├── token/
│   │   ├── __init__.py
│   │   ├── token.py
│   │   └── token_type.py
│   └── main.py
├── README.md
├── requirements.txt
└── your_program.sh
```

## 🧪 Testing

### Test Files
- `simple_test.lox`: Basic functionality tests
- `statement_test.lox`: Statement execution tests
- `error_test.lox`: Error handling tests

### Running Tests
```bash
# Execute the interpreter with test files
python app/main.py simple_test.lox
```

## 🛣️ Roadmap

- [ ] Add performance optimizations
- [ ] Implement more advanced error recovery
- [ ] Add debugging capabilities
- [ ] Create comprehensive test suite
- [ ] Document all public APIs

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Built with ❤️ as part of the [CodeCrafters Interpreter Challenge](https://app.codecrafters.io/courses/interpreter/overview).
