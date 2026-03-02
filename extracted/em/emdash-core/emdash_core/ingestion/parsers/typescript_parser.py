"""TypeScript/JavaScript parser using external TypeScript compiler."""

import json
import subprocess
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional

from .base_parser import BaseLanguageParser
from ...core.models import (
    FileEntity, FileEntities, ClassEntity, FunctionEntity,
    ModuleEntity, ImportStatement
)
from ...core.exceptions import ParsingError
from ...utils.logger import log


class TypeScriptParser(BaseLanguageParser):
    """Parses TypeScript/JavaScript files using TypeScript compiler API."""

    def __init__(self, file_path: Path, repo_root: Optional[Path] = None):
        """Initialize TypeScript parser.

        Args:
            file_path: Path to TypeScript/JavaScript file
            repo_root: Root directory of repository (for resolving qualified names)
        """
        super().__init__(file_path, repo_root)
        self.content: Optional[str] = None

    @classmethod
    def get_supported_extensions(cls) -> List[str]:
        """Return list of supported file extensions.

        Returns:
            List containing '.ts', '.tsx', '.js', '.jsx'
        """
        return ['.ts', '.tsx', '.js', '.jsx']

    def parse(self) -> FileEntities:
        """Parse TypeScript/JavaScript file and extract entities.

        Returns:
            FileEntities containing all extracted entities

        Raises:
            ParsingError: If file cannot be parsed
        """
        try:
            # Read file content
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                self.content = f.read()

            # Parse using TypeScript compiler (via Node.js)
            ast = self._parse_typescript_ast()

            if not ast:
                log.warning(f"Failed to parse TypeScript AST for {self.file_path}")
                return FileEntities()

            # Extract file metadata
            file_entity = self._extract_file_entity()

            # Extract entities from AST
            classes, class_methods = self._extract_classes(ast)
            functions = self._extract_functions(ast)
            # Add class methods to functions list
            functions.extend(class_methods)
            imports, modules = self._extract_imports(ast)

            return FileEntities(
                file=file_entity,
                classes=classes,
                functions=functions,
                modules=modules,
                imports=imports,
            )

        except Exception as e:
            log.warning(f"Failed to parse TypeScript file {self.file_path}: {e}")
            return FileEntities()

    def _parse_typescript_ast(self) -> Optional[Dict]:
        """Parse TypeScript using ts-node parser script.

        Returns:
            Dictionary containing AST data or None if parsing fails
        """
        # Call Node.js script that uses TypeScript compiler API
        parser_script = Path(__file__).parent / "ts_ast_parser.js"

        if not parser_script.exists():
            log.warning(f"TypeScript parser script not found: {parser_script}")
            return None

        try:
            result = subprocess.run(
                ['node', str(parser_script), str(self.file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                log.warning(f"TypeScript parser failed for {self.file_path}: {result.stderr}")
                return None

            return json.loads(result.stdout)

        except subprocess.TimeoutExpired:
            log.warning(f"TypeScript parsing timeout for {self.file_path}")
            return None
        except json.JSONDecodeError as e:
            log.warning(f"Failed to parse TypeScript AST JSON: {e}")
            return None
        except FileNotFoundError:
            log.warning("Node.js not found. Please install Node.js to parse TypeScript/JavaScript files.")
            return None

    def _extract_file_entity(self) -> FileEntity:
        """Extract file metadata.

        Returns:
            FileEntity with file metadata
        """
        content_hash = hashlib.sha256(self.content.encode()).hexdigest()
        return FileEntity.from_path(self.file_path, content_hash)

    def _extract_classes(self, ast: Dict) -> tuple[List[ClassEntity], List[FunctionEntity]]:
        """Extract class/interface definitions from TypeScript AST.

        Args:
            ast: Parsed AST dictionary

        Returns:
            Tuple of (ClassEntity list, FunctionEntity list for methods)
        """
        classes = []
        all_methods = []

        for cls_data in ast.get('classes', []):
            try:
                # Build qualified name
                class_qualified_name = f"{self.module_name}.{cls_data['name']}" if self.module_name else cls_data['name']

                class_entity = ClassEntity(
                    name=cls_data['name'],
                    qualified_name=class_qualified_name,
                    file_path=str(self.file_path),
                    line_start=cls_data.get('line_start', 0),
                    line_end=cls_data.get('line_end', 0),
                    docstring=cls_data.get('docstring'),
                    is_abstract=cls_data.get('is_abstract', False),
                    decorators=cls_data.get('decorators', []),
                    base_classes=cls_data.get('base_classes', []),
                    attributes=cls_data.get('properties', []),
                    methods=cls_data.get('methods', []),
                )
                classes.append(class_entity)

                # Extract method entities with calls
                for method_data in cls_data.get('method_entities', []):
                    try:
                        method_qualified_name = f"{class_qualified_name}.{method_data['name']}"
                        method_entity = FunctionEntity(
                            name=method_data['name'],
                            qualified_name=method_qualified_name,
                            file_path=str(self.file_path),
                            line_start=method_data.get('line_start', 0),
                            line_end=method_data.get('line_end', 0),
                            docstring=method_data.get('docstring'),
                            parameters=method_data.get('parameters', []),
                            return_annotation=method_data.get('return_type'),
                            is_async=method_data.get('is_async', False),
                            is_method=True,
                            is_static=method_data.get('is_static', False),
                            is_classmethod=False,
                            decorators=method_data.get('decorators', []),
                            cyclomatic_complexity=0,
                            calls=method_data.get('calls', []),
                        )
                        all_methods.append(method_entity)
                    except Exception as e:
                        log.warning(f"Failed to extract method {method_data.get('name', 'unknown')}: {e}")

            except Exception as e:
                log.warning(f"Failed to extract class {cls_data.get('name', 'unknown')}: {e}")

        return classes, all_methods

    def _extract_functions(self, ast: Dict) -> List[FunctionEntity]:
        """Extract function/method definitions from TypeScript AST.

        Args:
            ast: Parsed AST dictionary

        Returns:
            List of FunctionEntity objects
        """
        functions = []

        for func_data in ast.get('functions', []):
            try:
                # Build qualified name
                qualified_name = f"{self.module_name}.{func_data['name']}" if self.module_name else func_data['name']

                function_entity = FunctionEntity(
                    name=func_data['name'],
                    qualified_name=qualified_name,
                    file_path=str(self.file_path),
                    line_start=func_data.get('line_start', 0),
                    line_end=func_data.get('line_end', 0),
                    docstring=func_data.get('docstring'),
                    parameters=func_data.get('parameters', []),
                    return_annotation=func_data.get('return_type'),
                    is_async=func_data.get('is_async', False),
                    is_method=func_data.get('is_method', False),
                    is_static=func_data.get('is_static', False),
                    is_classmethod=False,  # TypeScript doesn't have classmethods like Python
                    decorators=func_data.get('decorators', []),
                    cyclomatic_complexity=0,  # TODO: Calculate complexity
                    calls=func_data.get('calls', []),
                )
                functions.append(function_entity)
            except Exception as e:
                log.warning(f"Failed to extract function {func_data.get('name', 'unknown')}: {e}")

        return functions

    def _extract_imports(self, ast: Dict) -> tuple[List[ImportStatement], List[ModuleEntity]]:
        """Extract import statements from TypeScript AST.

        Args:
            ast: Parsed AST dictionary

        Returns:
            Tuple of (import_statements, module_entities)
        """
        imports = []
        modules = {}

        for import_data in ast.get('imports', []):
            try:
                module_name = import_data['module']
                line_number = import_data.get('line_number', 0)

                # Determine if module is external (from node_modules)
                is_external = not module_name.startswith('.') and not module_name.startswith('/')

                # Create import statement
                import_stmt = ImportStatement(
                    module=module_name,
                    file_path=str(self.file_path),
                    line_number=line_number,
                    import_type='import',  # TypeScript uses 'import'
                    alias=import_data.get('alias'),
                    imported_names=import_data.get('imported_names', []),
                )
                imports.append(import_stmt)

                # Create module entity if not already exists
                if module_name not in modules:
                    modules[module_name] = ModuleEntity(
                        name=module_name,
                        import_path=module_name,
                        is_external=is_external,
                        package=module_name.split('/')[0] if '/' in module_name else module_name,
                    )

            except Exception as e:
                log.warning(f"Failed to extract import: {e}")

        return imports, list(modules.values())


# Auto-register TypeScript parser with registry
from .registry import ParserRegistry
ParserRegistry.register(TypeScriptParser)
