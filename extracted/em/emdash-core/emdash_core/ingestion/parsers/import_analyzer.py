"""Analyze import statements from Python AST."""

import ast
from pathlib import Path
from typing import List, Tuple

from ...core.models import ImportStatement, ModuleEntity


class ImportAnalyzer:
    """Analyzes import statements and builds module dependency graph."""

    def __init__(self, tree: ast.AST, file_path: Path, module_name: str):
        """Initialize import analyzer.

        Args:
            tree: Python AST
            file_path: Path to source file
            module_name: Module name
        """
        self.tree = tree
        self.file_path = file_path
        self.module_name = module_name

    def extract(self) -> Tuple[List[ImportStatement], List[ModuleEntity]]:
        """Extract all import statements and create module entities.

        Returns:
            Tuple of (import_statements, module_entities)
        """
        import_statements = []
        modules = {}  # Dict to avoid duplicates

        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    stmt = ImportStatement(
                        file_path=str(self.file_path),
                        line_number=node.lineno,
                        module=alias.name,
                        imported_names=[alias.name],
                        alias=alias.asname,
                        import_type="import",
                    )
                    import_statements.append(stmt)

                    # Create module entity
                    if alias.name not in modules:
                        modules[alias.name] = self._create_module_entity(alias.name)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported_names = [alias.name for alias in node.names]

                    stmt = ImportStatement(
                        file_path=str(self.file_path),
                        line_number=node.lineno,
                        module=node.module,
                        imported_names=imported_names,
                        alias=None,
                        import_type="from_import",
                    )
                    import_statements.append(stmt)

                    # Create module entity
                    if node.module not in modules:
                        modules[node.module] = self._create_module_entity(node.module)

        return import_statements, list(modules.values())

    def _create_module_entity(self, module_name: str) -> ModuleEntity:
        """Create a module entity from an import.

        Args:
            module_name: Name of imported module

        Returns:
            ModuleEntity
        """
        # Determine if module is external (stdlib or third-party)
        is_external = self._is_external_module(module_name)

        # Extract package name (first component)
        package = module_name.split('.')[0] if '.' in module_name else module_name

        return ModuleEntity(
            name=module_name,
            import_path=module_name,
            is_external=is_external,
            package=package,
        )

    def _is_external_module(self, module_name: str) -> bool:
        """Check if a module is external (not part of current codebase).

        Args:
            module_name: Module name

        Returns:
            True if external, False if internal
        """
        # Simple heuristic: if the module starts with a well-known package, it's external
        # In a more sophisticated version, we'd check against the actual codebase structure

        common_stdlib = {
            'os', 'sys', 'json', 're', 'math', 'datetime', 'collections',
            'itertools', 'functools', 'pathlib', 'typing', 'abc', 'asyncio',
            'unittest', 'logging', 'argparse', 'dataclasses', 'enum',
        }

        common_third_party = {
            'numpy', 'pandas', 'requests', 'flask', 'django', 'fastapi',
            'sqlalchemy', 'pydantic', 'pytest', 'click', 'rich', 'boto3',
            'tensorflow', 'torch', 'sklearn', 'matplotlib', 'seaborn',
        }

        root_package = module_name.split('.')[0]

        return root_package in common_stdlib or root_package in common_third_party
