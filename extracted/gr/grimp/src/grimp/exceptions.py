from __future__ import annotations

import warnings
from typing import Any


def __getattr__(name: str) -> Any:
    if name == "NamespacePackageEncountered":
        warnings.warn(
            f"{_NamespacePackageEncountered.__name__} is deprecated; graphs can now be built from "
            f"namespace packages starting from Grimp 3.14. This exception will not be "
            f"raised by Grimp anymore, and will be removed in Grimp 3.16.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _NamespacePackageEncountered
    raise AttributeError


class GrimpException(Exception):
    """
    Base exception for all custom Grimp exceptions to inherit.
    """


class ModuleNotPresent(GrimpException):
    """
    Indicates that a module was not present in a graph.
    """


class NoSuchContainer(GrimpException):
    """
    Indicates that a passed container was not found as a module in the graph.
    """


class _NamespacePackageEncountered(GrimpException):
    """
    Deprecated.
    """

    # See `__getattr__` above.
    # https://github.com/python-grimp/grimp/issues/272


class NotATopLevelModule(GrimpException):
    """
    Indicates when a child module was encountered unexpectedly.
    """


class SourceSyntaxError(GrimpException):
    """
    Indicates a syntax error in code that was being statically analysed.
    """

    def __init__(self, filename: str, lineno: int | None, text: str | None) -> None:
        """
        Args:
            filename: The file which contained the error.
            lineno: The line number containing the error.
            text: The text containing the error.
        """
        self.filename = filename
        self.lineno = lineno
        self.text = text

    def __str__(self) -> str:
        lineno = self.lineno or "?"
        text = self.text or "<unavailable>"
        return f"Syntax error in {self.filename}, line {lineno}: {text}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SourceSyntaxError):
            return NotImplemented

        return (self.filename, self.lineno, self.text) == (
            other.filename,
            other.lineno,
            other.text,
        )

    def __reduce__(self) -> tuple[type[SourceSyntaxError], tuple[str, int | None, str | None]]:
        # Implement __reduce__ to make this exception pickleable,
        # allowing it to be sent between processes.
        return SourceSyntaxError, (self.filename, self.lineno, self.text)


class InvalidModuleExpression(GrimpException):
    pass


class InvalidImportExpression(GrimpException):
    pass
