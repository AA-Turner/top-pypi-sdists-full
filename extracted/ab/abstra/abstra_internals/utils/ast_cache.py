import ast
from pathlib import Path
from typing import Dict, Tuple


class ASTCache:
    # Cache stores: (ast_tree, content, last_modified_time)
    _cache: Dict[str, Tuple[ast.Module, str, float]] = {}

    @classmethod
    def _update(cls, path: Path, cache_key: str, last_modified_time: float):
        content = path.read_text(encoding="utf-8")
        ast_tree = ast.parse(content)

        cls._cache[cache_key] = (ast_tree, content, last_modified_time)

        return ast_tree, content

    @classmethod
    def clear(cls):
        """
        Clear the internal cache.

        This method resets the internal cache to an empty state.
        It is intended for use **only in tests** to ensure a clean
        environment between test runs.

        Warning:
            This should not be called in production code, as it may
            lead to unexpected behavior or performance issues.
        """
        cls._cache = {}

    @classmethod
    def get(cls, path: Path) -> ast.Module:
        """
        Get the cached AST for a file.

        Args:
            path: Path to the Python file

        Returns:
            The parsed AST module

        Raises:
            FileNotFoundError: If the file doesn't exist
            SyntaxError: If the file has syntax errors
            UnicodeDecodeError: If the file has encoding issues
        """
        ast_tree, _ = cls.get_with_content(path)
        return ast_tree

    @classmethod
    def get_with_content(cls, path: Path) -> Tuple[ast.Module, str]:
        """
        Get the cached AST and file content for a file.

        This method is useful when you need both the AST and the original
        source code (e.g., to get line numbers or source lines).

        Args:
            path: Path to the Python file

        Returns:
            Tuple of (ast_tree, content)

        Raises:
            FileNotFoundError: If the file doesn't exist
            SyntaxError: If the file has syntax errors
            UnicodeDecodeError: If the file has encoding issues
        """
        cache_key = path.absolute().as_posix()
        last_modified_time = path.stat().st_mtime

        if cache_key not in cls._cache:
            return cls._update(path, cache_key, last_modified_time)

        ast_tree, content, cached_mtime = cls._cache[cache_key]
        if cached_mtime != last_modified_time:
            return cls._update(path, cache_key, last_modified_time)

        return ast_tree, content
