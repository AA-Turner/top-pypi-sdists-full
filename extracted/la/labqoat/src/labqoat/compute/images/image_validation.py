"""Validate declarative image values without touching the filesystem or network."""

import re
from pathlib import PurePosixPath


class ImageValidation:
    """Reject ambiguous image inputs before immutable operations are constructed."""

    @staticmethod
    def reference(value: str) -> str:
        """Require an explicit content-addressed registry base."""
        if re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9._/:-]*@sha256:[0-9a-f]{64}", value) is None:
            raise ValueError("Image references must include an immutable sha256 digest")
        return value

    @staticmethod
    def text(value: str) -> str:
        """Bound UTF-8 values and reject NUL bytes unsupported by build engines."""
        if not value or len(value.encode()) > 16_384 or "\0" in value:
            raise ValueError("Image values must contain 1..16384 UTF-8 bytes without NUL")
        return value

    @classmethod
    def path(cls, value: str) -> str:
        """Require normalized absolute container paths with literal Dockerfile spelling."""
        cls.text(value)
        path = PurePosixPath(value)
        if not path.is_absolute() or ".." in path.parts or str(path) != value:
            raise ValueError("Image destinations must be normalized absolute paths")
        if any(character in value for character in ("\n", "\r", "$", "\\")):
            raise ValueError("Image paths must not contain expansion or control characters")
        return value

    @classmethod
    def commands(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        """Keep command boundaries and execution order while enforcing operation bounds."""
        if not 1 <= len(values) <= 128:
            raise ValueError("Image operations require 1..128 values")
        return tuple(cls.text(value) for value in values)

    @staticmethod
    def environment(key: str, value: str) -> tuple[str, str]:
        """Retain literal string values while reserving managed worker authority."""
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key) is None or key.startswith("LABQOAT_WORKER_"):
            raise ValueError("Invalid or reserved image environment name")
        if len(value.encode()) > 16_384 or any(character in value for character in ("\0", "\n", "\r")):
            raise ValueError("Invalid image environment value")
        return key, value
