"""Main Python AST parser - coordinates all entity extraction."""

import ast
import hashlib
from pathlib import Path
from typing import List, Optional

from ...core.exceptions import ParsingError
from ...core.models import FileEntity, FileEntities
from .base_parser import BaseLanguageParser
from .class_extractor import ClassExtractor
from .function_extractor import FunctionExtractor
from .import_analyzer import ImportAnalyzer
from .call_graph_builder import CallGraphBuilder
from ...utils.logger import log


class PythonParser(BaseLanguageParser):
    """Parses Python files and extracts code entities."""

    def __init__(self, file_path: Path, repo_root: Optional[Path] = None):
        """Initialize Python parser.

        Args:
            file_path: Path to Python file
            repo_root: Root directory of repository (for resolving qualified names)
        """
        super().__init__(file_path, repo_root)
        self.tree: Optional[ast.AST] = None
        self.content: Optional[str] = None

    @classmethod
    def get_supported_extensions(cls) -> List[str]:
        """Return list of supported file extensions.

        Returns:
            List containing '.py'
        """
        return ['.py']

    def parse(self) -> FileEntities:
        """Parse the file and extract all entities.

        Returns:
            FileEntities containing all extracted entities

        Raises:
            ParsingError: If file cannot be parsed
        """
        try:
            # Read file content
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                self.content = f.read()

            # Parse AST
            try:
                self.tree = ast.parse(self.content, filename=str(self.file_path))
            except SyntaxError as e:
                log.warning(f"Syntax error in {self.file_path}: {e}")
                # Return empty entities for files with syntax errors
                return FileEntities()

            # Calculate module name
            self.module_name = self._calculate_module_name()

            # Extract file metadata
            file_entity = self._extract_file_entity()

            # Extract entities using specialized extractors
            class_extractor = ClassExtractor(
                self.tree, self.file_path, self.module_name
            )
            classes = class_extractor.extract()

            function_extractor = FunctionExtractor(
                self.tree, self.file_path, self.module_name
            )
            functions = function_extractor.extract()

            import_analyzer = ImportAnalyzer(
                self.tree, self.file_path, self.module_name
            )
            imports, modules = import_analyzer.extract()

            call_graph_builder = CallGraphBuilder(
                self.tree, self.module_name
            )
            call_graph_builder.build(functions)

            return FileEntities(
                file=file_entity,
                classes=classes,
                functions=functions,
                modules=modules,
                imports=imports,
            )

        except Exception as e:
            raise ParsingError(f"Failed to parse {self.file_path}: {e}")

    def _extract_file_entity(self) -> FileEntity:
        """Extract file metadata."""
        content_hash = hashlib.sha256(self.content.encode()).hexdigest()
        return FileEntity.from_path(self.file_path, content_hash)


def parse_file(file_path: Path, repo_root: Optional[Path] = None) -> FileEntities:
    """Convenience function to parse a single file.

    Args:
        file_path: Path to Python file
        repo_root: Root directory of repository

    Returns:
        FileEntities containing all extracted entities
    """
    parser = PythonParser(file_path, repo_root)
    return parser.parse()


# Auto-register Python parser with registry
from .registry import ParserRegistry
ParserRegistry.register(PythonParser)
