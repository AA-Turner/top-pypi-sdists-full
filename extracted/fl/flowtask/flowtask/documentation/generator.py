"""Documentation generator for Flowtask components.

This module provides the ComponentDocGenerator class that orchestrates
the documentation generation process: scanning directories, parsing
docstrings, generating schemas, and writing output files.
"""
import ast
import hashlib
import importlib
import importlib.util
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Type, Any

import orjson

from .models import ComponentDoc, DocumentationIndex
from .parser import DocstringParser
from .schema import SchemaGenerator


class ComponentDocGenerator:
    """Orchestrates component documentation generation.

    This class scans component directories, extracts documentation from
    class docstrings, generates JSON schemas, and writes output files.

    Example usage::

        from pathlib import Path
        from flowtask.documentation import ComponentDocGenerator

        generator = ComponentDocGenerator(output_dir=Path("documentation"))
        index = generator.generate([
            Path("flowtask/components"),
            Path("plugins/components")
        ])
        print(f"Generated docs for {len(index.components)} components")
    """

    # Marker that indicates a documentable docstring
    DOCSTRING_MARKER = ":widths: auto"

    def __init__(self, output_dir: Path):
        """Initialize the documentation generator.

        Args:
            output_dir: Directory where documentation files will be written.
        """
        self.output_dir = Path(output_dir)
        self.parser = DocstringParser()
        self.schema_gen = SchemaGenerator()
        self.logger = logging.getLogger(__name__)
        self._file_hashes: Dict[str, str] = {}

    def scan_components(self, paths: List[Path]) -> List[Type]:
        """Scan directories for component classes.

        Args:
            paths: List of directories to scan for .py files.

        Returns:
            List of component class types found in the directories.
        """
        components = []
        for path in paths:
            path = Path(path)
            if not path.exists():
                self.logger.warning(f"Path does not exist: {path}")
                continue

            self.logger.debug(f"Scanning directory: {path}")
            for py_file in path.glob("*.py"):
                # Skip __init__.py and private modules
                if py_file.name.startswith("_"):
                    continue

                try:
                    classes = self._extract_classes(py_file)
                    components.extend(classes)
                except Exception as e:
                    self.logger.warning(f"Error scanning {py_file}: {e}")
                    continue

        return components

    def _extract_classes(self, py_file: Path) -> List[Type]:
        """Extract component classes from a Python file.

        Uses AST to find class definitions, then dynamically imports
        only those that appear to be FlowComponent subclasses.

        Args:
            py_file: Path to the Python file.

        Returns:
            List of class types that are potential components.
        """
        classes = []

        # First, use AST to find class names (avoids full import)
        try:
            source = py_file.read_text(encoding='utf-8')
            tree = ast.parse(source)
        except (SyntaxError, UnicodeDecodeError) as e:
            self.logger.warning(f"Cannot parse {py_file}: {e}")
            return classes

        # Find all class definitions
        class_names = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_names.append(node.name)

        if not class_names:
            return classes

        # Build module path from file path
        module_path = self._file_to_module(py_file)
        if not module_path:
            return classes

        # Import the module and get classes
        try:
            module = self._import_module(module_path, py_file)
            if module is None:
                return classes

            for class_name in class_names:
                try:
                    cls = getattr(module, class_name, None)
                    if cls is not None and self._is_component_class(cls):
                        classes.append(cls)
                except Exception as e:
                    self.logger.debug(f"Cannot get class {class_name}: {e}")
                    continue

        except Exception as e:
            self.logger.warning(f"Cannot import module {module_path}: {e}")

        return classes

    def _file_to_module(self, py_file: Path) -> Optional[str]:
        """Convert a file path to a module path.

        Args:
            py_file: Path to the Python file.

        Returns:
            Module path string (e.g., 'flowtask.components.DownloadFrom')
            or None if conversion fails.
        """
        # Try to determine the module path
        parts = py_file.parts
        stem = py_file.stem

        # Look for known package markers
        # Search from the end to handle cases like /path/flowtask/flowtask/components
        # where the first "flowtask" is the project dir and second is the package
        parts_list = list(parts)

        # Find the package root (flowtask or plugins followed by components)
        for i in range(len(parts_list) - 1, -1, -1):
            if parts_list[i] == "flowtask" and i + 1 < len(parts_list):
                # Check if next part is a valid subpackage
                if parts_list[i + 1] in ("components", "interfaces", "utils", "hooks"):
                    module_parts = parts_list[i:-1] + [stem]
                    return ".".join(module_parts)
            elif parts_list[i] == "plugins" and i + 1 < len(parts_list):
                if parts_list[i + 1] == "components":
                    module_parts = parts_list[i:-1] + [stem]
                    return ".".join(module_parts)

        # Fallback: try finding just the package names
        for i, part in enumerate(parts_list):
            if part == "flowtask" and "components" in parts_list[i:]:
                module_parts = parts_list[i:-1] + [stem]
                return ".".join(module_parts)

        return None

    def _import_module(self, module_path: str, py_file: Path) -> Optional[Any]:
        """Dynamically import a module.

        Args:
            module_path: Dot-separated module path.
            py_file: Path to the Python file (for direct import fallback).

        Returns:
            The imported module or None if import fails.
        """
        try:
            # Try standard import first
            return importlib.import_module(module_path)
        except ImportError:
            # Fallback: import from file directly
            try:
                spec = importlib.util.spec_from_file_location(module_path, py_file)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_path] = module
                    spec.loader.exec_module(module)
                    return module
            except Exception as e:
                self.logger.debug(f"Fallback import failed for {py_file}: {e}")
                return None
        return None

    def _is_component_class(self, cls: Type) -> bool:
        """Check if a class is a FlowComponent subclass.

        Args:
            cls: The class to check.

        Returns:
            True if the class inherits from FlowComponent.
        """
        try:
            # Import FlowComponent for comparison
            from flowtask.components.flow import FlowComponent
            return (
                isinstance(cls, type) and
                issubclass(cls, FlowComponent) and
                cls is not FlowComponent
            )
        except ImportError:
            # Fallback: check class name in bases
            for base in getattr(cls, '__mro__', []):
                if base.__name__ in ('FlowComponent', 'AbstractFlow'):
                    return True
            return False

    def _is_documentable(self, cls: Type) -> bool:
        """Check if a class has a documentable docstring.

        Args:
            cls: The class to check.

        Returns:
            True if the docstring contains the documentation marker.
        """
        docstring = cls.__doc__
        return docstring is not None and self.DOCSTRING_MARKER in docstring

    def _get_file_hash(self, content: bytes) -> str:
        """Calculate MD5 hash of content for change detection.

        Args:
            content: The content to hash.

        Returns:
            Hex string of the MD5 hash.
        """
        return hashlib.md5(content).hexdigest()

    def generate(
        self,
        paths: List[Path],
        incremental: bool = False
    ) -> DocumentationIndex:
        """Generate documentation for all components.

        Args:
            paths: List of directories to scan for components.
            incremental: If True, only regenerate changed components.

        Returns:
            DocumentationIndex with references to all generated files.
        """
        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        components_dir = self.output_dir / "components"
        components_dir.mkdir(exist_ok=True)

        index_path = self.output_dir / "index.json"

        # Note: incremental parameter reserved for future implementation
        # Currently regenerates all documentation on each run
        _ = incremental  # Suppress unused parameter warning

        # Prepare index data
        index_data: Dict[str, Any] = {
            "updated_at": datetime.now().isoformat(),
            "components": {}
        }

        # Scan and process components
        components = self.scan_components(paths)
        self.logger.info(f"Found {len(components)} component classes")

        processed = 0
        for cls in components:
            if not self._is_documentable(cls):
                continue

            try:
                # Parse docstring
                doc = self.parser.parse(cls.__doc__)
                if not doc:
                    continue

                # Set the class name
                doc.name = cls.__name__

                # Get version if available
                if hasattr(cls, '_version'):
                    doc.version = cls._version

                # Generate schema
                schema = self.schema_gen.generate(doc)

                # Prepare file paths
                schema_path = components_dir / f"{cls.__name__}.schema.json"
                doc_path = components_dir / f"{cls.__name__}.doc.json"

                # Write schema
                schema_data = self.schema_gen.to_dict(schema)
                self._write_json(schema_path, schema_data)

                # Write doc (include version in the output)
                doc_data = doc.model_dump()
                self._write_json(doc_path, doc_data)

                # Add to index
                index_data["components"][cls.__name__] = {
                    "schema": f"components/{cls.__name__}.schema.json",
                    "doc": f"components/{cls.__name__}.doc.json"
                }

                processed += 1
                self.logger.debug(f"Generated docs for {cls.__name__}")

            except Exception as e:
                self.logger.warning(f"Error processing {cls.__name__}: {e}")
                continue

        # Write index
        self._write_json(index_path, index_data)

        self.logger.info(f"Generated documentation for {processed} components")

        return DocumentationIndex(
            updated_at=datetime.fromisoformat(index_data["updated_at"]),
            components=index_data["components"]
        )

    def _write_json(self, path: Path, data: Dict) -> None:
        """Write JSON file with consistent formatting.

        Args:
            path: Path to write the file.
            data: Data to serialize as JSON.
        """
        content = orjson.dumps(data, option=orjson.OPT_INDENT_2)
        path.write_bytes(content)

    def generate_single(self, cls: Type) -> Optional[ComponentDoc]:
        """Generate documentation for a single component class.

        Useful for testing or generating docs for specific components.

        Args:
            cls: The component class to document.

        Returns:
            ComponentDoc if successful, None otherwise.
        """
        if not self._is_documentable(cls):
            return None

        doc = self.parser.parse(cls.__doc__)
        if not doc:
            return None

        doc.name = cls.__name__
        if hasattr(cls, '_version'):
            doc.version = cls._version

        return doc
