"""Syntax validation for emitted ``replacement_code`` suggestions (FR-014).

Implements the SC-007 guarantee that every emitted ``replacement_code`` is
syntax-valid.  A replacement is validated by substituting it into the reviewed
file's original ``new_line`` range and parsing the *whole* resulting file (not
the fragment in isolation), so fragment-level replacements are validated in
their surrounding context.

Only explicitly supported languages are validated (at minimum Python, via
``compile(..., "exec")`` for full module-level syntax checks).  For
unsupported languages — and for
findings that carry only old-side coordinates — the ``replacement_code`` is
omitted so the suggestion may still be emitted without a concrete fix.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import PurePosixPath

__all__ = [
    "is_supported_language",
    "language_for_path",
    "replacement_is_valid",
    "sanitize_suggestion",
]

# Map file extensions to a language key with a syntax validator.
_PYTHON_EXTENSIONS = frozenset({".py", ".pyi"})


def _validate_python(source: str) -> bool:
    """Return whether ``source`` compiles as valid Python module code."""
    try:
        compile(source, "<string>", "exec")
    except (SyntaxError, ValueError, RecursionError):
        return False
    return True


_VALIDATORS: dict[str, Callable[[str], bool]] = {
    "python": _validate_python,
}


def _split_physical_lines(source: str) -> list[str]:
    """Split only on CR/LF line endings, preserving other Unicode separators."""
    if source == "":
        return []

    normalized = source.replace("\r\n", "\n").replace("\r", "\n")
    lines = normalized.split("\n")
    if source.endswith(("\r\n", "\r", "\n")):
        lines.pop()
    return lines


def language_for_path(file_path: str) -> str | None:
    """Return the supported-language key for ``file_path`` or ``None``."""
    suffix = PurePosixPath(file_path).suffix.lower()
    if suffix in _PYTHON_EXTENSIONS:
        return "python"
    return None


def is_supported_language(file_path: str) -> bool:
    """Return whether ``file_path``'s language has a syntax validator."""
    return language_for_path(file_path) is not None


def replacement_is_valid(
    *,
    file_content: str,
    start_line: int,
    end_line: int,
    replacement_code: str,
    language: str,
) -> bool:
    """Return whether substituting ``replacement_code`` yields valid syntax.

    The replacement is spliced into ``file_content`` over the inclusive 1-based
    ``[start_line, end_line]`` range (post-change coordinates) and the whole
    resulting file is parsed with the validator for ``language``.
    """
    validator = _VALIDATORS.get(language)
    if validator is None:
        return False

    lines = _split_physical_lines(file_content)
    # Range must be within the file and well-formed (1-based, inclusive).
    if start_line < 1 or end_line < start_line or end_line > len(lines):
        return False

    replacement_lines = _split_physical_lines(replacement_code)
    spliced = lines[: start_line - 1] + replacement_lines + lines[end_line:]
    return validator("\n".join(spliced))


def sanitize_suggestion(
    *,
    file_path: str,
    file_content: str,
    diff_side: str,
    start_line: int,
    end_line: int,
    replacement_code: str | None,
) -> str | None:
    """Return ``replacement_code`` if it is safe to emit, else ``None``.

    ``replacement_code`` is dropped when it is absent, when the finding is
    old-side only, when the language is unsupported, or when substituting it
    would produce syntactically invalid code (FR-014 / SC-007).
    """
    if replacement_code is None:
        return None
    if diff_side not in {"new", "context"}:
        return None

    language = language_for_path(file_path)
    if language is None:
        return None

    if replacement_is_valid(
        file_content=file_content,
        start_line=start_line,
        end_line=end_line,
        replacement_code=replacement_code,
        language=language,
    ):
        return replacement_code
    return None
