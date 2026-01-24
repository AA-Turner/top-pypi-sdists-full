from enum import Enum
from typing import Literal


class CodeScorerLanguage(str, Enum):
    """Supported sandbox languages."""

    python = "python"
    javascript = "javascript"
    typescript = "typescript"

    @property
    def file_extension(self) -> str:
        """Get the executable file extension for this language."""
        extensions = {
            CodeScorerLanguage.python: ".py",
            CodeScorerLanguage.javascript: ".js",
            CodeScorerLanguage.typescript: ".ts",
        }
        return extensions.get(self, "")  # Default to nothing if language isn't recognized

    @classmethod
    def from_file_extension(cls, ext: str) -> "CodeScorerLanguage":
        """Infer the language from the file extension."""
        for lang in cls:
            if lang.file_extension == ext:
                return lang
        raise ValueError(f"Unsupported file extension: {ext}")

    @property
    def default_version(self) -> str:
        """Get the default version of the language."""
        versions = {
            CodeScorerLanguage.python: "3.12",
            CodeScorerLanguage.javascript: "18",
            CodeScorerLanguage.typescript: "5.0",
        }
        return versions.get(self, "")


class ScorerType(str, Enum):
    luna = "luna"
    plus = "plus"


PlusScorerType = Literal[ScorerType.plus]
LunaOrPlusScorerType = Literal[ScorerType.luna, ScorerType.plus]
