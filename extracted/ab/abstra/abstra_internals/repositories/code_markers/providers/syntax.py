from typing import List

from abstra_internals.controllers.pysa import analyze_python_syntax
from abstra_internals.repositories.code_markers.models import CodeMarker
from abstra_internals.repositories.code_markers.providers.base import CodeMarkerProvider


class SyntaxMarkerProvider(CodeMarkerProvider):
    """
    Provider for Python syntax error markers.

    Wraps the existing Jedi-based syntax analysis to provide
    syntax error markers for the Monaco editor.
    """

    @property
    def name(self) -> str:
        return "syntax"

    def get_markers(self, code: str) -> List[CodeMarker]:
        """
        Analyze Python code for syntax errors.

        Args:
            code: The Python source code to analyze

        Returns:
            List of CodeMarker objects for syntax errors found
        """
        raw_markers = analyze_python_syntax(code)
        return [
            CodeMarker(
                line=m["line"],
                column=m["column"],
                until_line=m["until_line"],
                until_column=m["until_column"],
                message=m["message"],
                severity=m["severity"],
                source=self.name,
            )
            for m in raw_markers
        ]

    def supports_file_type(self, file_type: str) -> bool:
        return file_type == "python"
