"""Documentation generator for Flowtask components.

This module provides the ComponentDocGenerator class that orchestrates
the documentation generation process: scanning directories, parsing
docstrings, generating schemas, and writing output files.
"""
import ast
import hashlib
import importlib
import importlib.util
import inspect
import logging
import sys
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Type, Any

import orjson

from .models import ComponentDoc, DocumentationIndex
from .parser import DocstringParser
from .schema import SchemaGenerator


def _self_attr(node: ast.AST) -> Optional[str]:
    """Return the attribute name if ``node`` is ``self.<name>``, else None."""
    if (
        isinstance(node, ast.Attribute)
        and isinstance(node.value, ast.Name)
        and node.value.id == "self"
    ):
        return node.attr
    return None


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

    # Marker that indicates an interface/abstract base class (excluded from docs)
    INTERFACE_MARKER = ":interface:"

    # Default category for components not listed in categories.json
    DEFAULT_CATEGORY = "Other"

    # Path to the curated category mapping, relative to this module
    CATEGORIES_FILE = Path(__file__).parent / "categories.json"

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
        self._category_map: Dict[str, str] = self._load_category_map()

    def _load_category_map(self) -> Dict[str, str]:
        """Load the component-to-category mapping.

        Reads ``categories.json`` (a category -> list-of-component-names mapping)
        and inverts it into a flat ``{component: category}`` lookup.

        Side effect: also populates ``self._category_meta`` with the
        ``_meta`` block (per-category default I/O contracts).

        Returns:
            Dict mapping each component name to its category. Empty if the
            mapping file is missing or unreadable.
        """
        self._category_meta: Dict[str, Dict[str, str]] = {}

        path = self.CATEGORIES_FILE
        if not path.exists():
            self.logger.warning(f"Category map not found: {path}")
            return {}
        try:
            data = orjson.loads(path.read_bytes())
        except (orjson.JSONDecodeError, OSError) as e:
            self.logger.warning(f"Failed to load category map {path}: {e}")
            return {}

        # Side-load the dataflow-contract defaults (`_meta`). The validator
        # and the toolkit need them at runtime so they ship in doc.json /
        # schema.json — applied per-component in `generate()` after the
        # docstring parser runs.
        meta = data.get("_meta")
        if isinstance(meta, dict):
            for cat, entry in meta.items():
                if (
                    isinstance(entry, dict)
                    and isinstance(entry.get("consumes"), str)
                    and isinstance(entry.get("produces"), str)
                ):
                    self._category_meta[cat] = {
                        "consumes": entry["consumes"],
                        "produces": entry["produces"],
                    }

        mapping: Dict[str, str] = {}
        for category, names in data.items():
            if category.startswith("_") or not isinstance(names, list):
                continue
            for name in names:
                if isinstance(name, str):
                    mapping[name] = category
        return mapping

    def scan_components(self, paths: List[Path]) -> List[Type]:
        """Scan directories for component classes.

        Recurses into subdirectories so components organized into their own
        package (e.g. ``components/tMap/tMap.py``) are picked up. Files inside
        ``__pycache__`` and modules whose name starts with ``_`` are skipped;
        the AST + ``_is_component_class`` filters guard against pulling in
        unrelated classes.

        Args:
            paths: List of directories to scan for .py files.

        Returns:
            List of component class types found in the directories.
        """
        components = []
        seen: set[int] = set()
        for path in paths:
            path = Path(path)
            if not path.exists():
                self.logger.warning(f"Path does not exist: {path}")
                continue

            self.logger.debug(f"Scanning directory: {path}")
            for py_file in path.rglob("*.py"):
                # Skip __init__.py and private modules
                if py_file.name.startswith("_"):
                    continue
                # Skip cache and other private package directories
                if "__pycache__" in py_file.parts:
                    continue

                try:
                    classes = self._extract_classes(py_file)
                except Exception as e:
                    self.logger.warning(f"Error scanning {py_file}: {e}")
                    continue

                # De-duplicate in case the same class is reachable from
                # multiple scan roots.
                for cls in classes:
                    if id(cls) in seen:
                        continue
                    seen.add(id(cls))
                    components.append(cls)

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

        # No recognisable package root found — return None and let the caller
        # fall back to file-based import.  The previous forward-scan fallback
        # was fragile: a path like /home/user/flowtask-project/flowtask/components/Foo.py
        # would produce "flowtask-project.flowtask.components.Foo" instead of
        # "flowtask.components.Foo" because it matched the first "flowtask" token.
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
            from flowtask.interfaces.flow import FlowComponent
            return (
                isinstance(cls, type) and
                issubclass(cls, FlowComponent) and
                cls is not FlowComponent
            )
        except ImportError:
            # Fallback: check MRO for a class literally named 'FlowComponent'.
            # We intentionally exclude 'AbstractFlow' here — AbstractFlow is the
            # ABC root and is itself not a concrete-component base.  Including it
            # would over-accept interface classes that happen to be ABC descendants
            # without being proper FlowComponent subclasses.
            return any(
                base.__name__ == "FlowComponent"
                for base in getattr(cls, "__mro__", [])
                if base is not cls
            )

    def _is_documentable(self, cls: Type) -> bool:
        """Check if a class has a documentable docstring.

        A class is documentable when ALL of:
          - It has a docstring.
          - The docstring contains DOCSTRING_MARKER.
          - It is NOT marked as an interface (via INTERFACE_MARKER in docstring
            or by living under the ``flowtask.interfaces.*`` namespace).

        Args:
            cls: The class to check.

        Returns:
            True if the class should be emitted as a component doc.
        """
        docstring = cls.__doc__
        if docstring is None:
            return False
        if self.INTERFACE_MARKER in docstring:
            return False
        module = getattr(cls, "__module__", "") or ""
        if module.startswith("flowtask.interfaces."):
            return False
        return self.DOCSTRING_MARKER in docstring

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
    ) -> DocumentationIndex:
        """Generate documentation for all components.

        Always performs a full regeneration — all component docs are rebuilt
        on every call.  A future ``incremental`` mode (skip unchanged files)
        may be added, but is not yet implemented.

        Args:
            paths: List of directories to scan for components.

        Returns:
            DocumentationIndex with references to all generated files.
        """
        # Create output directories
        self.output_dir.mkdir(parents=True, exist_ok=True)
        components_dir = self.output_dir / "components"
        components_dir.mkdir(exist_ok=True)

        index_path = self.output_dir / "index.json"

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

                # Assign category from the curated mapping
                doc.category = self._category_map.get(
                    cls.__name__, self.DEFAULT_CATEGORY
                )

                # Resolve the dataflow contract via cascade:
                #   docstring override  →  category default in `_meta`  →  "any".
                # Always end with concrete strings on disk so consumers don't
                # have to repeat the cascade.
                cat_meta = self._category_meta.get(doc.category, {})
                if doc.consumes is None:
                    doc.consumes = cat_meta.get("consumes", "any")
                if doc.produces is None:
                    doc.produces = cat_meta.get("produces", "any")

                # Trust the class over the docstring: any attribute that has a
                # default somewhere in the MRO (class-level or assigned inside
                # __init__) is NOT required, regardless of the "Yes" the
                # docstring may declare. This is the single source of the
                # ground-truth `required` list and keeps the validator from
                # firing false positives on production tasks.
                self._reconcile_required_with_class(doc, cls)

                # Generate schema and embed it into the doc — single file on
                # disk carries both the prose and the JSON Schema.
                schema = self.schema_gen.generate(doc)
                doc.schema_ = self.schema_gen.to_dict(schema)

                # Write the merged doc.json (schema is embedded under the
                # "schema" key by virtue of the field alias).
                doc_path = components_dir / f"{cls.__name__}.doc.json"
                doc_data = doc.model_dump(by_alias=True)
                self._write_json(doc_path, doc_data)

                # Add to index — duplicate `category` and `description` here so
                # the API list endpoint can avoid re-reading every doc file.
                index_data["components"][cls.__name__] = {
                    "file": f"components/{cls.__name__}.doc.json",
                    "category": doc.category,
                    "description": doc.description,
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

    # ------------------------------------------------------------------
    # Required-field reconciliation
    # ------------------------------------------------------------------

    def _reconcile_required_with_class(
        self, doc: "ComponentDoc", cls: Type
    ) -> None:
        """Override ``required=True`` for attributes the class actually defaults.

        Walks ``cls.__mro__`` and collects every attribute name that is
        defaulted either as a class-level assignment OR via
        ``self.<name> = <expr>`` inside any ``__init__``. Any attribute in that
        set has its ``required`` flag cleared on ``doc``. Best-effort: if the
        source for a base class can't be read (C-extension, dynamic class),
        that base is skipped without aborting.
        """
        try:
            defaulted = self._collect_defaulted_attrs(cls)
        except Exception as exc:  # pragma: no cover — defensive
            self.logger.debug(
                "Default introspection failed for %s: %s", cls.__name__, exc
            )
            return

        if not defaulted:
            return

        for attr in doc.attributes:
            if attr.name in defaulted:
                attr.required = False

    def _collect_defaulted_attrs(self, cls: Type) -> set[str]:
        """Return the set of attribute names that have a default in the MRO."""
        defaulted: set[str] = set()

        for klass in cls.__mro__:
            if klass is object:
                continue
            try:
                src = inspect.getsource(klass)
            except (OSError, TypeError):
                # Builtins, C extensions, or interactively-defined classes.
                continue
            try:
                # Dedent in case the class lives inside a function (tests,
                # factories, etc.) — `inspect.getsource` preserves indentation
                # and `ast.parse` rejects a leading indent at top level.
                tree = ast.parse(textwrap.dedent(src))
            except (SyntaxError, IndentationError):
                continue

            for node in ast.walk(tree):
                if not isinstance(node, ast.ClassDef):
                    continue
                if node.name != klass.__name__:
                    continue
                defaulted.update(self._defaults_from_class_body(node))

        return defaulted

    @staticmethod
    def _defaults_from_class_body(node: ast.ClassDef) -> set[str]:
        """Pull defaulted attribute names from a single class body AST."""
        names: set[str] = set()

        for body_item in node.body:
            # Class-level assignment: `foo = 1` or `foo: int = 1`.
            if isinstance(body_item, ast.Assign):
                for target in body_item.targets:
                    if isinstance(target, ast.Name):
                        names.add(target.id)
            elif isinstance(body_item, ast.AnnAssign):
                target = body_item.target
                if isinstance(target, ast.Name) and body_item.value is not None:
                    names.add(target.id)
            # __init__: walk for `self.foo = ...` / `self.foo: T = ...`.
            elif isinstance(body_item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if body_item.name != "__init__":
                    continue
                for inner in ast.walk(body_item):
                    if isinstance(inner, ast.Assign):
                        for target in inner.targets:
                            attr = _self_attr(target)
                            if attr is not None:
                                names.add(attr)
                    elif isinstance(inner, ast.AnnAssign):
                        attr = _self_attr(inner.target)
                        if attr is not None and inner.value is not None:
                            names.add(attr)

        return names

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
