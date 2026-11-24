"""Per-block parser functions for the server-side markdown processing pipeline."""

from matrx_ai.processing.blocks.parsers.diff_parser import detect_diff_style, looks_like_diff
from matrx_ai.processing.blocks.parsers.table_parser import parse_table

__all__ = [
    "parse_table",
    "looks_like_diff",
    "detect_diff_style",
]
