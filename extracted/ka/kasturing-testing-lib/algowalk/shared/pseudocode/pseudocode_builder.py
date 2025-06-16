import ast
import inspect
import textwrap


class PseudocodeBuilder(ast.NodeVisitor):
    def __init__(self):
        self.lines = []
        self.indent_level = 0
        self.generated_code = ""

    def indent(self):
        self.indent_level += 1

    def dedent(self):
        self.indent_level = max(0, self.indent_level - 1)

    def add_line(self, line):
        indent = "    " * self.indent_level
        self.lines.append(f"{indent}{line}")

    def visit_FunctionDef(self, node):
        args = ", ".join(arg.arg for arg in node.args.args)
        self.add_line(f"FUNCTION {node.name}({args})")
        self.indent()
        self.generic_visit(node)
        self.dedent()

    def visit_For(self, node):
        iter_src = ast.unparse(node.iter) if hasattr(ast, "unparse") else "<loop>"
        target_src = node.target.id if isinstance(node.target, ast.Name) else "<target>"
        self.add_line(f"FOR {target_src} IN {iter_src}")
        self.indent()
        self.generic_visit(node)
        self.dedent()

    def visit_If(self, node):
        condition = ast.unparse(node.test) if hasattr(ast, "unparse") else "<condition>"
        self.add_line(f"IF {condition}")
        self.indent()
        self.generic_visit(node)
        self.dedent()

    def visit_Return(self, node):
        value = ast.unparse(node.value) if hasattr(ast, "unparse") else "..."
        self.add_line(f"RETURN {value}")

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call):
            call = ast.unparse(node.value) if hasattr(ast, "unparse") else "..."
            self.add_line(f"CALL {call}")
        else:
            self.generic_visit(node)

    def get_pseudocode(self):
        return "\n".join(self.lines)

    def print_pseudocode(self):
        print("\n\033[1;34m>>> Pseudocode <<<\033[0m\n")
        print(self.generated_code)

    def bundle_generation(self, fn):
        source = inspect.getsource(fn)
        filtered_source = textwrap.dedent(source)
        tree = ast.parse(textwrap.dedent(filtered_source))
        self.visit(tree)

        lines = self.get_pseudocode()
        filtered_lines = [
            line for line in lines.splitlines()
            if 'tracker.' not in line.strip()
        ]
        self.generated_code = "\n".join(filtered_lines)
