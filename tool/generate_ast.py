from argparse import ArgumentParser
import os
from typing import TextIO, Dict

# for taking arguments from command line
arg_parser = ArgumentParser()
arg_parser.add_argument('output',
                        help="Director where the result be stored")

args = arg_parser.parse_args()

# Define the indentation level globally
INDENT = " " * 4  # 4 spaces for indentation

# Expressions
EXPRESSIONS: Dict = {
    "Binary": ("left: Expr", 'operator: Token', "right: Expr"),
    "Grouping": ("expression: Expr",),
    "Literal": ("value: Any",),
    "Unary": ("operator: Token", "right: Expr")
}


def define_ast(output_dir, base_name: str, types: Dict):
    # define the path to the output file
    path = os.path.join(output_dir, f"{base_name}.py")

    visitor_class = f'{base_name}Visitor'

    with open(path, 'w', encoding='utf-8') as writer:
        writer.write("from typing import List, Any\n")
        writer.write("from tokens import Token\n")
        writer.write("from abc import ABC, abstractmethod\n")
        # generates the visitor abstract class of Expr

        define_visitor(writer, base_name, types.keys())

        # this will generate the expr class with accept
        writer.write("\n\n")
        writer.write(f"class {base_name}(ABC):\n")
        writer.write(f"{INDENT}@abstractmethod\n")
        writer.write(f"{INDENT}def accept(self, visitor: {visitor_class}):\n")
        writer.write(f"{INDENT * 2}pass\n")
        writer.write(f"\n\n")
        # other methods or fields need to be added here
        # ast classes
        for class_name, fields in types.items():
            define_type(writer, base_name, class_name, fields)
            writer.write("\n\n")


def define_visitor(writer: TextIO, base_name: str, types: list[str]):
    # this will create the visitor class for the visitor pattern
    name = base_name.lower()

    visitor_class = f'{base_name}Visitor'

    writer.write("\n\n")
    writer.write(f"class {visitor_class}(ABC):")
    for typ in types:
        writer.write("\n")
        writer.write(f"{INDENT}@abstractmethod")
        writer.write("\n")
        writer.write(f"{INDENT}def visit_{typ.lower()}_{name}(self, expr: '{base_name}'):")
        writer.write("\n")
        writer.write(f"{INDENT * 2}pass")
        writer.write("\n")


def define_type(writer: TextIO, base_name: str, class_name: str, field_list: str):
    visitor_class = f'{base_name}Visitor'
    writer.write(f"class {class_name}({base_name}):")
    writer.write(f"\n")
    writer.write(f'{INDENT}def __init__(self, {", ".join(field_list)}):')
    writer.write("\n")
    for field in field_list:
        writer.write(f"{INDENT * 2}self.{field.split(':')[0]} = {field.split(':')[0]}")
        writer.write(f"\n")

    # crearte the accept class
    writer.write(f"\n")
    writer.write(f"{INDENT}def accept(self, visitor: {visitor_class}):")
    writer.write("\n")
    writer.write(f"{INDENT*2}return visitor.visit_{class_name.lower()}_{base_name.lower()}(self)")
    writer.write("\n")
def main():
    output_dir = args.output
    base_name = "Expr"

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Call the define_ast function to generate the file
    define_ast(output_dir, base_name, EXPRESSIONS)


if __name__ == '__main__':
    main()
