from typing import List

from abstra_internals.controllers.language_server import analyze_python_syntax
from abstra_internals.repositories.code_markers.models import CodeMarker, MarkerSeverity
from abstra_internals.repositories.code_markers.providers.base import CodeMarkerProvider

LSP_SEVERITY_MAP: dict[int, MarkerSeverity] = {
    1: "error",
    2: "warning",
    3: "info",
    4: "hint",
}


class SyntaxMarkerProvider(CodeMarkerProvider):
    @property
    def name(self) -> str:
        return "syntax"

    def get_markers(self, code: str) -> List[CodeMarker]:
        result = analyze_python_syntax(code)
        diagnostics = result["diagnostics"]
        return [
            CodeMarker(
                line=d["range"]["start"]["line"] + 1,
                column=d["range"]["start"]["character"] + 1,
                until_line=d["range"]["end"]["line"] + 1,
                until_column=d["range"]["end"]["character"] + 1,
                message=d.get("message", ""),
                severity=LSP_SEVERITY_MAP.get(d.get("severity", 1), "error"),
                source=self.name,
            )
            for d in diagnostics
        ]

    def supports_file_type(self, file_type: str) -> bool:
        return file_type == "python"
