"""Build call graph by analyzing function calls in Python AST."""

import ast
from typing import List

from ...core.models import FunctionEntity


class CallGraphBuilder:
    """Builds call relationships between functions."""

    def __init__(self, tree: ast.AST, module_name: str):
        """Initialize call graph builder.

        Args:
            tree: Python AST
            module_name: Module name
        """
        self.tree = tree
        self.module_name = module_name

    def build(self, functions: List[FunctionEntity]):
        """Build call graph for all functions.

        Mutates the functions list by populating the `calls` attribute.

        Args:
            functions: List of FunctionEntity objects to analyze
        """
        # Create a mapping from function name to qualified name
        function_map = {func.name: func.qualified_name for func in functions}

        # For each function, analyze its body for calls
        for func in functions:
            func.calls = self._extract_calls(func, function_map)

    def _extract_calls(
        self,
        function: FunctionEntity,
        function_map: dict
    ) -> List[str]:
        """Extract function calls from a function body.

        Args:
            function: FunctionEntity to analyze
            function_map: Mapping of function names to qualified names

        Returns:
            List of qualified names of called functions
        """
        calls = []

        # Find the function node in the AST
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.lineno == function.line_start:
                    # Found the function node
                    calls = self._find_calls_in_node(node, function_map)
                    break

        return calls

    def _find_calls_in_node(
        self,
        node: ast.AST,
        function_map: dict
    ) -> List[str]:
        """Find all function calls within a node.

        Args:
            node: AST node to analyze
            function_map: Mapping of function names to qualified names

        Returns:
            List of called function qualified names
        """
        calls = []

        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                called_name = self._get_call_name(child.func)

                if called_name:
                    # Try to resolve to qualified name
                    if called_name in function_map:
                        calls.append(function_map[called_name])
                    else:
                        # Keep the raw name even if we can't resolve it
                        # In a second pass, we could resolve these across files
                        calls.append(called_name)

        return list(set(calls))  # Remove duplicates

    def _get_call_name(self, node: ast.expr) -> str:
        """Get the name of a called function from a Call node.

        Args:
            node: Function expression node

        Returns:
            Function name or empty string
        """
        if isinstance(node, ast.Name):
            # Direct call: foo()
            return node.id

        elif isinstance(node, ast.Attribute):
            # Method call: obj.foo()
            # We'll track these as "Type.method" if possible
            value_name = self._get_call_name(node.value)
            if value_name:
                return f"{value_name}.{node.attr}"
            else:
                return node.attr

        elif isinstance(node, ast.Call):
            # Chained call: foo()()
            return self._get_call_name(node.func)

        else:
            return ""
