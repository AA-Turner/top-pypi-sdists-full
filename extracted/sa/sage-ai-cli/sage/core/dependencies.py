"""Language-agnostic dependency graph for SAGE.

This module provides dependency analysis across all supported languages,
not just Python. It abstracts away language-specific import parsing and
provides a unified interface for understanding code relationships.

This addresses P0 items 12-13:
- Item 12: Remove the Python-only dependency graph assumption
- Item 13: Add a language-agnostic dependency abstraction

Supported languages:
- Python: AST-based import analysis
- JavaScript/TypeScript: import/require parsing
- Go: package imports
- Rust: use/mod statements
- Java/Kotlin: import statements
- Ruby: require statements
- PHP: use/require statements
- C/C++: #include directives
- C#/F#: using statements
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Protocol

from .languages import Language, get_language_for_extension

__all__ = [
    "DependencyGraph",
    "FileNode",
    "ImportInfo",
    "get_exports_for_file",
    "get_imports_for_file",
]


@dataclass
class ImportInfo:
    """Information about a single import/dependency."""

    source: str  # The imported module/package
    alias: str | None = None  # Import alias (if any)
    specific_items: list[str] = field(default_factory=list)  # Specific imported items
    is_relative: bool = False  # Relative import
    is_dynamic: bool = False  # Dynamic import (harder to analyze)
    line_number: int = 0  # Line where import occurs


@dataclass
class FileNode:
    """A node in the dependency graph representing a file."""

    path: str  # Relative path from workspace root
    language: Language = Language.UNKNOWN
    imports: set[str] = field(default_factory=set)  # What this file imports
    imported_by: set[str] = field(default_factory=set)  # Files that import this
    import_details: list[ImportInfo] = field(default_factory=list)  # Detailed import info
    exports: set[str] = field(default_factory=set)  # Exported symbols
    functions: list[str] = field(default_factory=list)  # Defined functions
    classes: list[str] = field(default_factory=list)  # Defined classes
    mtime: float = 0.0  # Last modification time

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "path": self.path,
            "language": self.language.value,
            "imports": list(self.imports),
            "imported_by": list(self.imported_by),
            "exports": list(self.exports),
            "functions": self.functions,
            "classes": self.classes,
            "mtime": self.mtime,
        }

    @classmethod
    def from_dict(cls, data: dict) -> FileNode:
        """Deserialize from dictionary."""
        return cls(
            path=data["path"],
            language=Language(data.get("language", "unknown")),
            imports=set(data.get("imports", [])),
            imported_by=set(data.get("imported_by", [])),
            exports=set(data.get("exports", [])),
            functions=data.get("functions", []),
            classes=data.get("classes", []),
            mtime=data.get("mtime", 0.0),
        )


class ImportParser(Protocol):
    """Protocol for language-specific import parsers."""

    def parse(self, source: str, filepath: str) -> tuple[list[ImportInfo], list[str], list[str]]:
        """Parse imports, functions, and classes from source code.

        Returns:
            Tuple of (imports, functions, classes)
        """
        ...


class PythonImportParser:
    """Parse Python imports using AST."""

    def parse(self, source: str, filepath: str) -> tuple[list[ImportInfo], list[str], list[str]]:
        imports: list[ImportInfo] = []
        functions: list[str] = []
        classes: list[str] = []

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return imports, functions, classes

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(
                        ImportInfo(
                            source=alias.name.split(".")[0],
                            alias=alias.asname,
                            line_number=node.lineno,
                        )
                    )
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    items = [alias.name for alias in node.names]
                    imports.append(
                        ImportInfo(
                            source=node.module.split(".")[0],
                            specific_items=items,
                            is_relative=node.level > 0,
                            line_number=node.lineno,
                        )
                    )
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)

        return imports, functions, classes


class JavaScriptImportParser:
    """Parse JavaScript/TypeScript imports."""

    # import x from 'y'
    _IMPORT_DEFAULT = re.compile(r"import\s+(\w+)\s+from\s+['\"]([^'\"]+)['\"]")
    # import { x, y } from 'z'
    _IMPORT_NAMED = re.compile(r"import\s+\{([^}]+)\}\s+from\s+['\"]([^'\"]+)['\"]")
    # import * as x from 'y'
    _IMPORT_STAR = re.compile(r"import\s+\*\s+as\s+(\w+)\s+from\s+['\"]([^'\"]+)['\"]")
    # import 'x' (side effect)
    _IMPORT_SIDE_EFFECT = re.compile(r"import\s+['\"]([^'\"]+)['\"]")
    # const x = require('y')
    _REQUIRE = re.compile(r"(?:const|let|var)\s+(\w+)\s*=\s*require\(['\"]([^'\"]+)['\"]\)")
    # export function x / export class x
    _EXPORT_FUNCTION = re.compile(r"export\s+(?:async\s+)?function\s+(\w+)")
    _EXPORT_CLASS = re.compile(r"export\s+class\s+(\w+)")
    # function x / class x (non-exported)
    _FUNCTION = re.compile(r"(?:async\s+)?function\s+(\w+)")
    _CLASS = re.compile(r"class\s+(\w+)")

    def parse(self, source: str, filepath: str) -> tuple[list[ImportInfo], list[str], list[str]]:
        imports: list[ImportInfo] = []
        functions: list[str] = []
        classes: list[str] = []

        for i, line in enumerate(source.splitlines(), 1):
            # Default import
            match = self._IMPORT_DEFAULT.search(line)
            if match:
                imports.append(
                    ImportInfo(
                        source=match.group(2),
                        alias=match.group(1),
                        line_number=i,
                    )
                )
                continue

            # Named imports
            match = self._IMPORT_NAMED.search(line)
            if match:
                items = [x.strip().split(" as ")[0].strip() for x in match.group(1).split(",")]
                imports.append(
                    ImportInfo(
                        source=match.group(2),
                        specific_items=items,
                        line_number=i,
                    )
                )
                continue

            # Star import
            match = self._IMPORT_STAR.search(line)
            if match:
                imports.append(
                    ImportInfo(
                        source=match.group(2),
                        alias=match.group(1),
                        line_number=i,
                    )
                )
                continue

            # Side effect import
            match = self._IMPORT_SIDE_EFFECT.search(line)
            if match and "from" not in line:
                imports.append(
                    ImportInfo(
                        source=match.group(1),
                        line_number=i,
                    )
                )
                continue

            # Require
            match = self._REQUIRE.search(line)
            if match:
                imports.append(
                    ImportInfo(
                        source=match.group(2),
                        alias=match.group(1),
                        line_number=i,
                    )
                )
                continue

            # Functions and classes
            for m in self._EXPORT_FUNCTION.finditer(line):
                functions.append(m.group(1))
            for m in self._EXPORT_CLASS.finditer(line):
                classes.append(m.group(1))
            for m in self._FUNCTION.finditer(line):
                if m.group(1) not in functions:
                    functions.append(m.group(1))
            for m in self._CLASS.finditer(line):
                if m.group(1) not in classes:
                    classes.append(m.group(1))

        return imports, functions, classes


class GoImportParser:
    """Parse Go imports."""

    # import "x"
    _IMPORT_SINGLE = re.compile(r'^import\s+"([^"]+)"')
    # import alias "x"
    _IMPORT_ALIAS = re.compile(r'^import\s+(\w+)\s+"([^"]+)"')
    # import ( "x" )
    _IMPORT_BLOCK_START = re.compile(r"^import\s*\(")
    _IMPORT_IN_BLOCK = re.compile(r'^\s*(?:(\w+)\s+)?"([^"]+)"')
    # func x(
    _FUNC = re.compile(r"^func\s+(\w+)\s*\(")
    # func (r Receiver) x(
    _METHOD = re.compile(r"^func\s+\([^)]+\)\s*(\w+)\s*\(")
    # type X struct/interface
    _TYPE = re.compile(r"^type\s+(\w+)\s+(?:struct|interface)")

    def parse(self, source: str, filepath: str) -> tuple[list[ImportInfo], list[str], list[str]]:
        imports: list[ImportInfo] = []
        functions: list[str] = []
        classes: list[str] = []

        lines = source.splitlines()
        in_import_block = False

        for i, line in enumerate(lines, 1):
            line_stripped = line.strip()

            if self._IMPORT_BLOCK_START.match(line_stripped):
                in_import_block = True
                continue

            if in_import_block:
                if line_stripped == ")":
                    in_import_block = False
                    continue
                match = self._IMPORT_IN_BLOCK.match(line_stripped)
                if match:
                    imports.append(
                        ImportInfo(
                            source=match.group(2),
                            alias=match.group(1),
                            line_number=i,
                        )
                    )
                continue

            # Single import
            match = self._IMPORT_ALIAS.match(line_stripped)
            if match:
                imports.append(
                    ImportInfo(
                        source=match.group(2),
                        alias=match.group(1),
                        line_number=i,
                    )
                )
                continue

            match = self._IMPORT_SINGLE.match(line_stripped)
            if match:
                imports.append(
                    ImportInfo(
                        source=match.group(1),
                        line_number=i,
                    )
                )
                continue

            # Functions and types
            match = self._FUNC.match(line_stripped)
            if match:
                functions.append(match.group(1))
                continue

            match = self._METHOD.match(line_stripped)
            if match:
                functions.append(match.group(1))
                continue

            match = self._TYPE.match(line_stripped)
            if match:
                classes.append(match.group(1))

        return imports, functions, classes


class RustImportParser:
    """Parse Rust use statements."""

    # use x::y;
    _USE = re.compile(r"^use\s+([^;{]+)")
    # mod x;
    _MOD = re.compile(r"^mod\s+(\w+)\s*;")
    # fn x(
    _FN = re.compile(r"^(?:pub\s+)?(?:async\s+)?fn\s+(\w+)")
    # struct/enum/trait X
    _TYPE = re.compile(r"^(?:pub\s+)?(?:struct|enum|trait)\s+(\w+)")

    def parse(self, source: str, filepath: str) -> tuple[list[ImportInfo], list[str], list[str]]:
        imports: list[ImportInfo] = []
        functions: list[str] = []
        classes: list[str] = []

        for i, line in enumerate(source.splitlines(), 1):
            line_stripped = line.strip()

            match = self._USE.match(line_stripped)
            if match:
                # Extract the crate/module name
                path = match.group(1).strip()
                crate = path.split("::")[0]
                imports.append(
                    ImportInfo(
                        source=crate,
                        line_number=i,
                    )
                )
                continue

            match = self._MOD.match(line_stripped)
            if match:
                imports.append(
                    ImportInfo(
                        source=match.group(1),
                        line_number=i,
                    )
                )
                continue

            match = self._FN.match(line_stripped)
            if match:
                functions.append(match.group(1))
                continue

            match = self._TYPE.match(line_stripped)
            if match:
                classes.append(match.group(1))

        return imports, functions, classes


class JavaImportParser:
    """Parse Java/Kotlin imports."""

    # import x.y.z;
    _IMPORT = re.compile(r"^import\s+(?:static\s+)?([^;]+);")
    # class X / interface X
    _CLASS = re.compile(r"^(?:public\s+)?(?:abstract\s+)?(?:class|interface|enum)\s+(\w+)")
    # fun/function x(
    _FUNCTION = re.compile(r"^(?:public\s+)?(?:private\s+)?(?:static\s+)?(?:\w+\s+)?(\w+)\s*\(")

    def parse(self, source: str, filepath: str) -> tuple[list[ImportInfo], list[str], list[str]]:
        imports: list[ImportInfo] = []
        functions: list[str] = []
        classes: list[str] = []

        for i, line in enumerate(source.splitlines(), 1):
            line_stripped = line.strip()

            match = self._IMPORT.match(line_stripped)
            if match:
                path = match.group(1).strip()
                package = path.split(".")[0]
                imports.append(
                    ImportInfo(
                        source=package,
                        line_number=i,
                    )
                )
                continue

            match = self._CLASS.match(line_stripped)
            if match:
                classes.append(match.group(1))
                continue

            # Only capture methods with explicit return types to avoid false positives
            if "(" in line_stripped and ")" in line_stripped:
                match = self._FUNCTION.match(line_stripped)
                if match and match.group(1) not in {"if", "for", "while", "switch", "catch"}:
                    functions.append(match.group(1))

        return imports, functions, classes


class RubyImportParser:
    """Parse Ruby require statements."""

    # require 'x' / require "x"
    _REQUIRE = re.compile(r"^require\s+['\"]([^'\"]+)['\"]")
    # require_relative 'x'
    _REQUIRE_RELATIVE = re.compile(r"^require_relative\s+['\"]([^'\"]+)['\"]")
    # def x
    _DEF = re.compile(r"^def\s+(\w+)")
    # class X
    _CLASS = re.compile(r"^class\s+(\w+)")
    # module X
    _MODULE = re.compile(r"^module\s+(\w+)")

    def parse(self, source: str, filepath: str) -> tuple[list[ImportInfo], list[str], list[str]]:
        imports: list[ImportInfo] = []
        functions: list[str] = []
        classes: list[str] = []

        for i, line in enumerate(source.splitlines(), 1):
            line_stripped = line.strip()

            match = self._REQUIRE.match(line_stripped)
            if match:
                imports.append(
                    ImportInfo(
                        source=match.group(1),
                        line_number=i,
                    )
                )
                continue

            match = self._REQUIRE_RELATIVE.match(line_stripped)
            if match:
                imports.append(
                    ImportInfo(
                        source=match.group(1),
                        is_relative=True,
                        line_number=i,
                    )
                )
                continue

            match = self._DEF.match(line_stripped)
            if match:
                functions.append(match.group(1))
                continue

            match = self._CLASS.match(line_stripped)
            if match:
                classes.append(match.group(1))
                continue

            match = self._MODULE.match(line_stripped)
            if match:
                classes.append(match.group(1))

        return imports, functions, classes


class PHPImportParser:
    """Parse PHP use/require statements."""

    # use X\Y\Z;
    _USE = re.compile(r"^use\s+([^;]+);")
    # require 'x' / include 'x'
    _REQUIRE = re.compile(r"^(?:require|include|require_once|include_once)\s+['\"]?([^'\";\s]+)")
    # function x(
    _FUNCTION = re.compile(
        r"^(?:public\s+)?(?:private\s+)?(?:protected\s+)?(?:static\s+)?function\s+(\w+)"
    )
    # class X
    _CLASS = re.compile(r"^(?:abstract\s+)?(?:final\s+)?class\s+(\w+)")
    # interface X
    _INTERFACE = re.compile(r"^interface\s+(\w+)")

    def parse(self, source: str, filepath: str) -> tuple[list[ImportInfo], list[str], list[str]]:
        imports: list[ImportInfo] = []
        functions: list[str] = []
        classes: list[str] = []

        for i, line in enumerate(source.splitlines(), 1):
            line_stripped = line.strip()

            match = self._USE.match(line_stripped)
            if match:
                path = match.group(1).strip()
                namespace = path.split("\\")[0]
                imports.append(
                    ImportInfo(
                        source=namespace,
                        line_number=i,
                    )
                )
                continue

            match = self._REQUIRE.match(line_stripped)
            if match:
                imports.append(
                    ImportInfo(
                        source=match.group(1),
                        line_number=i,
                    )
                )
                continue

            match = self._FUNCTION.match(line_stripped)
            if match:
                functions.append(match.group(1))
                continue

            match = self._CLASS.match(line_stripped)
            if match:
                classes.append(match.group(1))
                continue

            match = self._INTERFACE.match(line_stripped)
            if match:
                classes.append(match.group(1))

        return imports, functions, classes


class CImportParser:
    """Parse C/C++ include directives."""

    # #include <x> or #include "x"
    _INCLUDE = re.compile(r'^#include\s+[<"]([^>"]+)[>"]')
    # Function definition (simplified)
    _FUNCTION = re.compile(r"^(?:static\s+)?(?:inline\s+)?(?:\w+\s+)+(\w+)\s*\([^;]*$")
    # struct/class/enum definition
    _TYPE = re.compile(r"^(?:typedef\s+)?(?:struct|class|enum)\s+(\w+)")

    def parse(self, source: str, filepath: str) -> tuple[list[ImportInfo], list[str], list[str]]:
        imports: list[ImportInfo] = []
        functions: list[str] = []
        classes: list[str] = []

        for i, line in enumerate(source.splitlines(), 1):
            line_stripped = line.strip()

            match = self._INCLUDE.match(line_stripped)
            if match:
                imports.append(
                    ImportInfo(
                        source=match.group(1),
                        line_number=i,
                    )
                )
                continue

            match = self._FUNCTION.match(line_stripped)
            if match:
                name = match.group(1)
                if name not in {"if", "for", "while", "switch", "return"}:
                    functions.append(name)
                continue

            match = self._TYPE.match(line_stripped)
            if match:
                classes.append(match.group(1))

        return imports, functions, classes


class CSharpImportParser:
    """Parse C# using statements."""

    # using X.Y.Z;
    _USING = re.compile(r"^using\s+([^;=]+);")
    # class X / interface X / struct X
    _CLASS = re.compile(
        r"^(?:public\s+)?(?:internal\s+)?(?:abstract\s+)?(?:partial\s+)?(?:class|interface|struct|record)\s+(\w+)"
    )
    # Method (simplified)
    _METHOD = re.compile(
        r"^(?:public|private|protected|internal)?\s*(?:static\s+)?(?:async\s+)?(?:\w+\s+)?(\w+)\s*\("
    )

    def parse(self, source: str, filepath: str) -> tuple[list[ImportInfo], list[str], list[str]]:
        imports: list[ImportInfo] = []
        functions: list[str] = []
        classes: list[str] = []

        for i, line in enumerate(source.splitlines(), 1):
            line_stripped = line.strip()

            match = self._USING.match(line_stripped)
            if match:
                namespace = match.group(1).strip().split(".")[0]
                imports.append(
                    ImportInfo(
                        source=namespace,
                        line_number=i,
                    )
                )
                continue

            match = self._CLASS.match(line_stripped)
            if match:
                classes.append(match.group(1))
                continue

            if "(" in line_stripped:
                match = self._METHOD.match(line_stripped)
                if match and match.group(1) not in {"if", "for", "while", "switch", "catch", "new"}:
                    functions.append(match.group(1))

        return imports, functions, classes


class ElixirImportParser:
    """Parse Elixir import/use/require/alias statements."""

    # import X / use X / require X / alias X
    _IMPORT = re.compile(r"^(?:import|use|require|alias)\s+([A-Z][\w.]*)")
    # def x / defp x
    _DEF = re.compile(r"^(?:def|defp)\s+(\w+)")
    # defmodule X
    _MODULE = re.compile(r"^defmodule\s+([A-Z][\w.]*)")

    def parse(self, source: str, filepath: str) -> tuple[list[ImportInfo], list[str], list[str]]:
        imports: list[ImportInfo] = []
        functions: list[str] = []
        classes: list[str] = []

        for i, line in enumerate(source.splitlines(), 1):
            line_stripped = line.strip()

            match = self._IMPORT.match(line_stripped)
            if match:
                imports.append(
                    ImportInfo(
                        source=match.group(1),
                        line_number=i,
                    )
                )
                continue

            match = self._DEF.match(line_stripped)
            if match:
                functions.append(match.group(1))
                continue

            match = self._MODULE.match(line_stripped)
            if match:
                classes.append(match.group(1))

        return imports, functions, classes


# Language to parser mapping
_PARSERS: dict[Language, ImportParser] = {
    Language.PYTHON: PythonImportParser(),
    Language.JAVASCRIPT: JavaScriptImportParser(),
    Language.TYPESCRIPT: JavaScriptImportParser(),
    Language.GO: GoImportParser(),
    Language.RUST: RustImportParser(),
    Language.JAVA: JavaImportParser(),
    Language.KOTLIN: JavaImportParser(),
    Language.RUBY: RubyImportParser(),
    Language.PHP: PHPImportParser(),
    Language.C: CImportParser(),
    Language.CPP: CImportParser(),
    Language.CSHARP: CSharpImportParser(),
    Language.FSHARP: CSharpImportParser(),
    Language.ELIXIR: ElixirImportParser(),
}


def get_imports_for_file(
    filepath: Path, language: Language | None = None
) -> tuple[list[ImportInfo], list[str], list[str]]:
    """Get imports, functions, and classes from a file.

    Args:
        filepath: Path to the file
        language: Optional language override

    Returns:
        Tuple of (imports, functions, classes)
    """
    if not filepath.exists():
        return [], [], []

    if language is None:
        language = get_language_for_extension(filepath.suffix)

    parser = _PARSERS.get(language)
    if parser is None:
        return [], [], []

    try:
        source = filepath.read_text("utf-8", errors="replace")
        return parser.parse(source, str(filepath))
    except Exception:
        return [], [], []


def get_exports_for_file(filepath: Path, language: Language | None = None) -> set[str]:
    """Get exported symbols from a file.

    Args:
        filepath: Path to the file
        language: Optional language override

    Returns:
        Set of exported symbol names
    """
    _, functions, classes = get_imports_for_file(filepath, language)
    return set(functions + classes)


class DependencyGraph:
    """Language-agnostic dependency graph for a codebase.

    This replaces the Python-only DependencyGraph from main.py with
    a version that supports all configured languages.
    """

    # Directories to skip
    SKIP_DIRS: set[str] = {
        ".git",
        ".svn",
        ".hg",
        ".venv",
        "venv",
        "env",
        ".env",
        "__pycache__",
        "node_modules",
        "dist",
        "build",
        "target",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".tox",
        "vendor",
        "deps",
        "_build",
        ".next",
        ".nuxt",
        ".output",
        "coverage",
        ".coverage",
        "htmlcov",
    }

    # File patterns to index by language
    FILE_PATTERNS: dict[Language, list[str]] = {
        Language.PYTHON: ["**/*.py"],
        Language.JAVASCRIPT: ["**/*.js", "**/*.mjs", "**/*.cjs", "**/*.jsx"],
        Language.TYPESCRIPT: ["**/*.ts", "**/*.tsx", "**/*.mts", "**/*.cts"],
        Language.GO: ["**/*.go"],
        Language.RUST: ["**/*.rs"],
        Language.JAVA: ["**/*.java"],
        Language.KOTLIN: ["**/*.kt", "**/*.kts"],
        Language.RUBY: ["**/*.rb"],
        Language.PHP: ["**/*.php"],
        Language.C: ["**/*.c", "**/*.h"],
        Language.CPP: ["**/*.cpp", "**/*.cc", "**/*.cxx", "**/*.hpp"],
        Language.CSHARP: ["**/*.cs"],
        Language.FSHARP: ["**/*.fs", "**/*.fsx"],
        Language.ELIXIR: ["**/*.ex", "**/*.exs"],
    }

    def __init__(self, cwd: Path) -> None:
        self.cwd = cwd.resolve()
        self.nodes: dict[str, FileNode] = {}
        self._index_cache_file = cwd / ".sage" / "dependency_graph.json"
        self._load_cache()

    def _load_cache(self) -> None:
        """Load cached graph from disk."""
        if self._index_cache_file.exists():
            try:
                import json

                data = json.loads(self._index_cache_file.read_text(encoding="utf-8", errors="replace"))
                for path, node_data in data.get("nodes", {}).items():
                    self.nodes[path] = FileNode.from_dict(node_data)
            except Exception:
                pass

    def _save_cache(self) -> None:
        """Save graph to disk."""
        import json

        self._index_cache_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": 2,
            "nodes": {path: node.to_dict() for path, node in self.nodes.items()},
        }
        self._index_cache_file.write_text(json.dumps(data))

    def _should_skip(self, path: Path) -> bool:
        """Check if a path should be skipped."""
        parts = path.relative_to(self.cwd).parts
        return any(p.startswith(".") or p in self.SKIP_DIRS for p in parts)

    def _path_to_module(self, filepath: str, language: Language) -> str | None:
        """Convert a filepath to a module/package name."""
        path = Path(filepath)

        if language == Language.PYTHON:
            # Remove .py extension and convert path to module
            if path.suffix == ".py":
                parts = list(path.with_suffix("").parts)
                if parts[-1] == "__init__":
                    parts = parts[:-1]
                return ".".join(parts) if parts else None

        if language in {Language.JAVASCRIPT, Language.TYPESCRIPT}:
            # Could be imported as relative or package path
            return filepath.rsplit(".", 1)[0]

        if language == Language.GO:
            # Go uses directory-based packages
            return str(path.parent)

        return filepath

    def index_file(self, filepath: str) -> FileNode | None:
        """Index a single file.

        Args:
            filepath: Relative path to the file

        Returns:
            FileNode if successfully indexed, None otherwise
        """
        full_path = self.cwd / filepath
        if not full_path.exists():
            return None

        try:
            mtime = full_path.stat().st_mtime
        except OSError:
            return None

        # Skip if already indexed and unchanged
        if filepath in self.nodes:
            existing = self.nodes[filepath]
            if existing.mtime >= mtime:
                return existing

        language = get_language_for_extension(full_path.suffix)
        if language == Language.UNKNOWN:
            return None

        imports, functions, classes = get_imports_for_file(full_path, language)

        node = FileNode(
            path=filepath,
            language=language,
            imports={imp.source for imp in imports},
            import_details=imports,
            functions=functions,
            classes=classes,
            mtime=mtime,
        )

        self.nodes[filepath] = node
        return node

    def index_project(
        self,
        limit: int = 1000,
        languages: set[Language] | None = None,
    ) -> int:
        """Index all files in the project.

        Args:
            limit: Maximum number of files to index
            languages: Optional set of languages to index (None = all)

        Returns:
            Number of files indexed
        """
        indexed = 0

        # Determine which extensions to look for
        valid_extensions: set[str] = set()
        for lang, lang_patterns in self.FILE_PATTERNS.items():
            if languages is None or lang in languages:
                for p in lang_patterns:
                    if p.startswith("**/*"):
                        valid_extensions.add(p[4:])

        import os

        # Use os.walk for efficiency and early directory pruning
        for root, dirs, files in os.walk(self.cwd):
            # Prune directories in-place
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in self.SKIP_DIRS]
            
            root_path = Path(root)
            for f in sorted(files):
                if indexed >= limit:
                    break
                
                if f.startswith("."):
                    continue
                    
                ext = os.path.splitext(f)[1].lower()
                if ext in valid_extensions:
                    try:
                        p = root_path / f
                        rel_path = str(p.relative_to(self.cwd))
                        if self.index_file(rel_path):
                            indexed += 1
                    except Exception:
                        continue
            
            if indexed >= limit:
                break

        # Build reverse dependencies
        self._build_reverse_deps()

        self._save_cache()
        return indexed

    def _build_reverse_deps(self) -> None:
        """Build reverse dependency relationships."""
        # Clear existing imported_by
        for node in self.nodes.values():
            node.imported_by.clear()

        # Build module to path mapping
        module_to_path: dict[str, str] = {}
        for filepath, node in self.nodes.items():
            module = self._path_to_module(filepath, node.language)
            if module:
                module_to_path[module] = filepath
                # Also map the base name
                module_to_path[Path(filepath).stem] = filepath

        # Build reverse deps
        for filepath, node in self.nodes.items():
            for imp in node.imports:
                # Try to find the imported module
                if imp in module_to_path:
                    imported_path = module_to_path[imp]
                    if imported_path in self.nodes and imported_path != filepath:
                        self.nodes[imported_path].imported_by.add(filepath)

    def get_affected_files(self, changed_files: list[str]) -> list[str]:
        """Get all files affected by changes to the given files.

        This performs BFS traversal of reverse dependencies.

        Args:
            changed_files: List of changed file paths

        Returns:
            List of all affected file paths (including original files)
        """
        affected = set(changed_files)
        queue = list(changed_files)

        while queue:
            current = queue.pop(0)
            if current not in self.nodes:
                continue
            for dependent in self.nodes[current].imported_by:
                if dependent not in affected:
                    affected.add(dependent)
                    queue.append(dependent)

        return sorted(affected)

    def get_file_context(self, filepath: str) -> str:
        """Get context about a file for the AI.

        Args:
            filepath: Path to the file

        Returns:
            Formatted context string
        """
        if filepath not in self.nodes:
            self.index_file(filepath)

        node = self.nodes.get(filepath)
        if not node:
            return ""

        lines = [f"📊 Dependency context for {filepath} ({node.language.value}):"]

        if node.imports:
            lines.append(f"  Imports: {', '.join(sorted(node.imports)[:10])}")

        if node.imported_by:
            lines.append(f"  Used by: {', '.join(sorted(node.imported_by)[:10])}")

        if node.functions:
            lines.append(f"  Functions: {', '.join(node.functions[:15])}")

        if node.classes:
            lines.append(f"  Classes: {', '.join(node.classes[:10])}")

        return "\n".join(lines)

    def get_impact_summary(self, changed_files: list[str]) -> str:
        """Get a summary of the impact of changes.

        Args:
            changed_files: List of changed file paths

        Returns:
            Formatted impact summary
        """
        affected = self.get_affected_files(changed_files)
        if len(affected) <= len(changed_files):
            return ""

        other_affected = [f for f in affected if f not in changed_files]
        if not other_affected:
            return ""

        return (
            f"⚠️ Impact Analysis: Changes to {len(changed_files)} file(s) may affect "
            f"{len(other_affected)} other file(s):\n  "
            + "\n  ".join(other_affected[:10])
            + (f"\n  ... and {len(other_affected) - 10} more" if len(other_affected) > 10 else "")
        )

    def get_statistics(self) -> dict:
        """Get statistics about the indexed codebase.

        Returns:
            Dictionary with statistics
        """
        stats = {
            "total_files": len(self.nodes),
            "by_language": {},
            "total_functions": 0,
            "total_classes": 0,
            "total_imports": 0,
        }

        for node in self.nodes.values():
            lang = node.language.value
            if lang not in stats["by_language"]:
                stats["by_language"][lang] = 0
            stats["by_language"][lang] += 1
            stats["total_functions"] += len(node.functions)
            stats["total_classes"] += len(node.classes)
            stats["total_imports"] += len(node.imports)

        return stats
