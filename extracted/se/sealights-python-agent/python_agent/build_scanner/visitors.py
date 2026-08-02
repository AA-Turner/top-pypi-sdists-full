import ast
import os
import sys

from python_agent.build_scanner import ast_utils
from python_agent.build_scanner.method_hasher import MethodHasher


class SealightsVisitor(ast.NodeVisitor):
    def __init__(self, file_data):
        self.file_data = file_data
        self.method_hasher = MethodHasher(MethodCleanerVisitor)
        self.current_method_lines_stack = []  # Stack to manage nested scopes
        self._ignore_overloads = (
            os.environ.get("SL_IGNORE_OVERLOADS", "true").lower() != "false"
        )

    def _is_overload_stub(self, node):
        if not self._ignore_overloads:
            return False
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == "overload":
                return True
            if isinstance(decorator, ast.Attribute) and decorator.attr == "overload":
                return True
        return False

    def push_new_scope(self):
        self.current_method_lines_stack.append([])

    def pop_scope(self):
        if self.current_method_lines_stack:
            return self.current_method_lines_stack.pop()
        return []

    def current_scope(self):
        if not self.current_method_lines_stack:
            self.push_new_scope()  # Ensure there's always a scope
        return self.current_method_lines_stack[-1]

    def visit_FunctionDef(self, node):
        if self._is_overload_stub(node):
            return

        # Push a new scope for this function definition
        self.push_new_scope()

        # Add the function's starting line number, ensuring it's the 'def' line
        self.current_scope().append(node.lineno)

        # Visit all child nodes (body of the function) but not decorators
        for n in ast.iter_child_nodes(node):
            if n not in node.decorator_list:
                self.visit(n)

        # Once done, capture the lines and finalize this function's scope
        method_lines = self.pop_scope()
        self.file_data.methods.append(
            self.method_hasher.build_method(
                self.file_data, node.name, node, method_lines
            )
        )

    def visit_Lambda(self, node):
        if not hasattr(node, "name"):
            node.name = "(Anonymous)"
        # Lambdas are treated as part of the current scope
        self.current_scope().append(node.lineno)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        if self._is_overload_stub(node):
            return

        if tuple(sys.version_info) >= (3, 7) and node.col_offset == 0:
            node.col_offset = 6
        self.push_new_scope()

        # Add the function's starting line number, ensuring it's the 'def' line
        self.current_scope().append(node.lineno)

        # Visit all child nodes (body of the function) but not decorators
        for n in ast.iter_child_nodes(node):
            if n not in node.decorator_list:
                self.visit(n)

        # Once done, capture the lines and finalize this function's scope
        method_lines = self.pop_scope()
        self.file_data.methods.append(
            self.method_hasher.build_method(
                self.file_data, node.name, node, method_lines
            )
        )

    def visit_Assign(self, node):
        if isinstance(node.value, ast.Lambda):
            if node.targets and hasattr(node.targets[-1], "id"):
                setattr(node.value, "name", node.targets[-1].id)
        # Assignments are part of the current scope
        self.current_scope().append(node.lineno)
        self.generic_visit(node)

    def generic_visit(self, node):
        """Override generic_visit to capture line numbers of all nodes."""
        if hasattr(node, "lineno"):
            self.current_scope().append(node.lineno)
        super().generic_visit(node)


class MethodCleanerVisitor(ast.NodeVisitor):
    def __init__(self):
        self.traverse_node = None

    def visit_FunctionDef(self, node):
        if not self.traverse_node:
            self.traverse_node = node
        if node != self.traverse_node:
            ast_utils.clean_functiondef_body(node)
        self.generic_visit(node)

    def visit_Lambda(self, node):
        if not self.traverse_node:
            self.traverse_node = node
        if node != self.traverse_node:
            ast_utils.clean_lambda_body(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        if not self.traverse_node:
            self.traverse_node = node
        if node != self.traverse_node:
            ast_utils.clean_functiondef_body(node)
        self.generic_visit(node)
