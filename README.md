
# Lox Interpreter in Python

This project is a Python implementation of the Lox programming language from the book *Crafting Interpreters* by Robert Nystrom. It includes lexical scanning, parsing, and interpretation of Lox code. The interpreter supports variables, control flow, and expressions, with plans to extend its functionality.

## Project Structure

The project is organized as follows:

```
lox_interpreter/
│
├── lox/
│   ├── __init__.py           # Package initialization
│   ├── ast_printer.py        # A utility to print the abstract syntax tree (AST)
│   ├── Expr.py               # Expression classes for the AST
│   ├── interpreter.py        # The core interpreter for executing Lox code
│   ├── lox.py                # Main entry point to run the Lox interpreter
│   ├── main.py               # Additional script for running the interpreter
│   ├── parser.py             # Parser to create AST from tokens
│   ├── scanner.py            # Lexical scanner for tokenizing input
│   ├── token_type.py         # Definition of token types used by the scanner
│   ├── tokens.py             # Token class representing individual tokens
│
└── tool/
    ├── __init__.py           # Package initialization for tools
    ├── generate_ast.py       # Script to generate AST classes
```

## Getting Started

### Prerequisites

- Python 3.6 or higher is required.

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/niranjanblank/lox_interpreter
   cd lox_interpreter
   ```

2. Install any necessary dependencies (if applicable). Currently, this project only requires Python's standard libraries.

### Running the Interpreter

To run the Lox interpreter, navigate to the `lox` directory and execute the `main.py` script:

```bash
python main.py [script.lox]
```

If no script is provided, the interpreter will run in REPL mode, allowing you to input Lox code interactively.

### Example

Here’s a sample Lox program that can be run using the interpreter:

```lox
print "Hello, Lox!";
```

## Features

- **Lexical Scanning:** Converts source code into tokens.
- **Parsing:** Builds an Abstract Syntax Tree (AST) from tokens.
- **AST Printer:** Prints the structure of the AST for debugging purposes.
- **Interpretation:** Evaluates the AST to execute Lox code.

## Planned Features

- **Control Flow:** Implement full support for conditional statements and loops.
- **Functions and Classes:** Support for defining and calling functions, along with object-oriented features.

## References

- [Crafting Interpreters](https://craftinginterpreters.com/): The book that this project is based on.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
