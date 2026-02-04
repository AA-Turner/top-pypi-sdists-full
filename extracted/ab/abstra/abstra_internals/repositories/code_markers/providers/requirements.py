from typing import List

from abstra_internals.repositories.code_markers.models import CodeMarker
from abstra_internals.repositories.code_markers.providers.base import CodeMarkerProvider
from abstra_internals.services.requirements import get_requirements_lint_markers


class RequirementsMarkerProvider(CodeMarkerProvider):
    """
    Provider for missing requirements markers.

    Analyzes Python code for imports that are not listed in
    requirements.txt and provides warning markers.
    """

    @property
    def name(self) -> str:
        return "requirements"

    def get_markers(self, code: str) -> List[CodeMarker]:
        """
        Analyze Python code for missing requirements.

        Args:
            code: The Python source code to analyze

        Returns:
            List of CodeMarker objects for imports missing from requirements.txt
        """
        raw_markers = get_requirements_lint_markers(code)
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
