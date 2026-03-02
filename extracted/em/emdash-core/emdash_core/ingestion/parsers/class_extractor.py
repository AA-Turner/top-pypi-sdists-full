"""Extract class definitions from Python AST."""

import ast
from pathlib import Path
from typing import List

from ...core.models import ClassEntity


class ClassExtractor:
    """Extracts class definitions from Python AST."""

    def __init__(self, tree: ast.AST, file_path: Path, module_name: str):
        """Initialize class extractor.

        Args:
            tree: Python AST
            file_path: Path to source file
            module_name: Module name (e.g., "src.module")
        """
        self.tree = tree
        self.file_path = file_path
        self.module_name = module_name

    def extract(self) -> List[ClassEntity]:
        """Extract all class definitions.

        Returns:
            List of ClassEntity objects
        """
        classes = []

        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                class_entity = self._extract_class(node)
                if class_entity:
                    classes.append(class_entity)

        return classes

    def _extract_class(self, node: ast.ClassDef) -> ClassEntity:
        """Extract a single class definition.

        Args:
            node: ClassDef AST node

        Returns:
            ClassEntity
        """
        # Qualified name
        qualified_name = f"{self.module_name}.{node.name}" if self.module_name else node.name

        # Docstring
        docstring = ast.get_docstring(node)

        # Check if abstract
        is_abstract = self._is_abstract(node)

        # Decorators
        decorators = [self._get_decorator_name(dec) for dec in node.decorator_list]

        # Base classes
        base_classes = []
        for base in node.bases:
            base_name = self._get_name(base)
            if base_name:
                base_classes.append(base_name)

        # Extract attributes (class variables)
        attributes = []
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                attributes.append(item.target.id)
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attributes.append(target.id)

        # Extract method names (will be populated later with qualified names)
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef) or isinstance(item, ast.AsyncFunctionDef):
                method_qualified_name = f"{qualified_name}.{item.name}"
                methods.append(method_qualified_name)

        return ClassEntity(
            name=node.name,
            qualified_name=qualified_name,
            file_path=str(self.file_path),
            line_start=node.lineno,
            line_end=node.end_lineno or node.lineno,
            docstring=docstring,
            is_abstract=is_abstract,
            decorators=decorators,
            base_classes=base_classes,
            attributes=attributes,
            methods=methods,
        )

    def _is_abstract(self, node: ast.ClassDef) -> bool:
        """Check if a class is abstract (has ABC or abstractmethod)."""
        # Check if inherits from ABC
        for base in node.bases:
            base_name = self._get_name(base)
            if base_name in ["ABC", "abc.ABC"]:
                return True

        # Check if any method has @abstractmethod
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for dec in item.decorator_list:
                    dec_name = self._get_decorator_name(dec)
                    if "abstractmethod" in dec_name:
                        return True

        return False

    def _get_decorator_name(self, decorator: ast.expr) -> str:
        """Get the name of a decorator.

        Args:
            decorator: Decorator AST node

        Returns:
            Decorator name as string
        """
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return f"{self._get_name(decorator.value)}.{decorator.attr}"
        elif isinstance(decorator, ast.Call):
            return self._get_decorator_name(decorator.func)
        else:
            return "unknown"

    def _get_name(self, node: ast.expr) -> str:
        """Get the name from an expression node.

        Args:
            node: AST expression node

        Returns:
            Name as string
        """
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            value_name = self._get_name(node.value)
            return f"{value_name}.{node.attr}" if value_name else node.attr
        elif isinstance(node, ast.Subscript):
            # For generics like List[int]
            return self._get_name(node.value)
        else:
            return ""
