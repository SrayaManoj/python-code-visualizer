import ast
import os

class CodeParser(ast.NodeVisitor):
    def __init__(self):
        self.items = []  # To store (type, name)
        self.edges = []  # To store caller -> callee
        self.nodes = set()  # Unique function/class names
        self.current_function = None
        self.current_class = None

    def visit_Call(self, node):
        caller = self.current_function or self.current_class
        callee = None

        if isinstance(node.func, ast.Name):
            callee = node.func.id
        elif isinstance(node.func, ast.Attribute):
            callee = node.func.attr

        if caller and callee:
            self.edges.append((caller, callee))

        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        prev_function = self.current_function
        self.current_function = node.name
        self.nodes.add(node.name)
        self.items.append(('function', node.name))
        self.generic_visit(node)
        self.current_function = prev_function

    def visit_ClassDef(self, node):
        prev_class = self.current_class
        self.current_class = node.name
        self.nodes.add(node.name)
        self.items.append(('class', node.name))
        self.generic_visit(node)
        self.current_class = prev_class

def parse_directory(directory):
    parser = CodeParser()

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                try:
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        tree = ast.parse(f.read(), filename=file)
                        parser.visit(tree)
                except Exception as e:
                    print(f"Failed to parse {file}: {e}")
                    continue

    return parser.items, parser.edges
