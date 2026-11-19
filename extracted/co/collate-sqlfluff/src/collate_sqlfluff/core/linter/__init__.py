"""Linter class and helper classes."""

from collate_sqlfluff.core.formatter import FormatterInterface
from collate_sqlfluff.core.linter.common import ParsedString, RenderedFile, RuleTuple
from collate_sqlfluff.core.linter.linted_file import LintedFile
from collate_sqlfluff.core.linter.linter import Linter
from collate_sqlfluff.core.linter.linting_result import LintingResult

__all__ = (
    "FormatterInterface",
    "RuleTuple",
    "ParsedString",
    "LintedFile",
    "LintingResult",
    "Linter",
    "RenderedFile",
)
