"""Compact encoder for search_text."""

from .. import schema_driven as sd

TOOLS = ("search_text",)
ENCODING_ID = "st1"

_TABLES = [
    sd.TableSpec(
        key="results",
        tag="t",
        cols=["file", "line", "line_content"],
        intern=["file"],
        types={"line": "int"},
    ),
]
_SCALARS = ("result_count", "query", "repo")
_META = (
    "timing_ms", "files_searched", "truncated",
    "tokens_saved", "total_tokens_saved",
)


def encode(tool: str, response: dict) -> tuple[str, str]:
    return sd.encode(tool, response, ENCODING_ID, _TABLES, _SCALARS, meta_keys=_META)


def decode(payload: str) -> dict:
    return sd.decode(payload, _TABLES, _SCALARS, meta_keys=_META)
