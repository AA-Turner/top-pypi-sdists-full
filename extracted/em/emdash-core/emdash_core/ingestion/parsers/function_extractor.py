"""Extract function and method definitions from Python AST."""

import ast
from pathlib import Path
from typing import List, Optional

from ...core.models import FunctionEntity


class FunctionExtractor:
    """Extracts function and method definitions from Python AST."""

    def __init__(self, tree: ast.AST, file_path: Path, module_name: str):
        """Initialize function extractor.

        Args:
            tree: Python AST
            file_path: Path to source file
            module_name: Module name
        """
        self.tree = tree
        self.file_path = file_path
        self.module_name = module_name
        self.current_class: Optional[str] = None

    def extract(self) -> List[FunctionEntity]:
        """Extract all function and method definitions.

        Returns:
            List of FunctionEntity objects
        """
        functions = []

        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                # Track current class for method extraction
                self._extract_methods(node, functions)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Only extract top-level functions (not methods)
                # Methods are extracted via _extract_methods
                if not self._is_method(node):
                    function_entity = self._extract_function(node, is_method=False)
                    if function_entity:
                        functions.append(function_entity)

        return functions

    def _extract_methods(self, class_node: ast.ClassDef, functions: List[FunctionEntity]):
        """Extract methods from a class.

        Args:
            class_node: ClassDef AST node
            functions: List to append extracted methods to
        """
        class_qualified_name = f"{self.module_name}.{class_node.name}" if self.module_name else class_node.name

        for item in class_node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_entity = self._extract_function(
                    item,
                    is_method=True,
                    parent_class=class_qualified_name
                )
                if function_entity:
                    functions.append(function_entity)

    def _is_method(self, node: ast.FunctionDef) -> bool:
        """Check if a function node is a method (inside a class).

        This is a simplification - in practice we extract methods separately.
        """
        return False

    def _extract_function(
        self,
        node: ast.FunctionDef,
        is_method: bool = False,
        parent_class: Optional[str] = None
    ) -> FunctionEntity:
        """Extract a single function or method.

        Args:
            node: FunctionDef or AsyncFunctionDef AST node
            is_method: Whether this is a class method
            parent_class: Qualified name of parent class (if method)

        Returns:
            FunctionEntity
        """
        # Qualified name
        if is_method and parent_class:
            qualified_name = f"{parent_class}.{node.name}"
        else:
            qualified_name = f"{self.module_name}.{node.name}" if self.module_name else node.name

        # Docstring
        docstring = ast.get_docstring(node)

        # Parameters
        parameters = self._extract_parameters(node.args)

        # Return annotation
        return_annotation = None
        if node.returns:
            return_annotation = ast.unparse(node.returns)

        # Check if async
        is_async = isinstance(node, ast.AsyncFunctionDef)

        # Decorators
        decorators = []
        is_static = False
        is_classmethod = False

        for dec in node.decorator_list:
            dec_name = self._get_decorator_name(dec)
            decorators.append(dec_name)

            if dec_name == "staticmethod":
                is_static = True
            elif dec_name == "classmethod":
                is_classmethod = True

        # Cyclomatic complexity (simplified - count branches)
        complexity = self._calculate_complexity(node)

        return FunctionEntity(
            name=node.name,
            qualified_name=qualified_name,
            file_path=str(self.file_path),
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            docstring=docstring,
            parameters=parameters,
            return_annotation=return_annotation,
            is_async=is_async,
            is_method=is_method,
            is_static=is_static,
            is_classmethod=is_classmethod,
            decorators=decorators,
            cyclomatic_complexity=complexity,
        )

    def _extract_parameters(self, args: ast.arguments) -> List[str]:
        """Extract parameter names from function arguments.

        Args:
            args: arguments AST node

        Returns:
            List of parameter names with optional type annotations
        """
        parameters = []

        # Regular args
        for arg in args.args:
            param = arg.arg
            if arg.annotation:
                param += f": {ast.unparse(arg.annotation)}"
            parameters.append(param)

        # *args
        if args.vararg:
            param = f"*{args.vararg.arg}"
            if args.vararg.annotation:
                param += f": {ast.unparse(args.vararg.annotation)}"
            parameters.append(param)

        # **kwargs
        if args.kwarg:
            param = f"**{args.kwarg.arg}"
            if args.kwarg.annotation:
                param += f": {ast.unparse(args.kwarg.annotation)}"
            parameters.append(param)

        return parameters

    def _get_decorator_name(self, decorator: ast.expr) -> str:
        """Get the name of a decorator."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return f"{ast.unparse(decorator.value)}.{decorator.attr}"
        elif isinstance(decorator, ast.Call):
            return self._get_decorator_name(decorator.func)
        else:
            return "unknown"

    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity (simplified).

        Counts decision points: if, while, for, except, with, and, or
        """
        complexity = 1  # Base complexity

        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler, ast.With)):
                complexity += 1
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1

        return complexity
