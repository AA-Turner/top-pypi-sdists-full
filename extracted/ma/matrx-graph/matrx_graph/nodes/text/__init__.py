"""Text extraction + manipulation node pack.

Covers the "LLM output → structured value" gap in workflows. An LLM returns a
string; downstream nodes need a field, a number, a list. Without these, every
workflow ends up writing the same ``data.transform`` expression, which the
sandbox intentionally can't handle (no ``re``, no ``json.loads``, no string
methods beyond subscription).

Nodes:
- ``text.regex_extract``  — pull groups out of a string
- ``text.regex_replace``  — substitute by pattern
- ``text.json_path``      — read JSON/dict values by dotted/indexed path
- ``text.custom_extract`` — run restricted Python for arbitrary reshaping
- ``text.sections.patch``  — edit a markdown document by section key
"""

from matrx_graph.nodes.text.custom_extract import CustomExtractExecutor
from matrx_graph.nodes.text.json_path import JsonPathExecutor
from matrx_graph.nodes.text.manipulate import (
    JoinExecutor,
    SlugExecutor,
    SplitExecutor,
    TemplateExecutor,
    WordCountExecutor,
)
from matrx_graph.nodes.text.regex import RegexExtractExecutor, RegexReplaceExecutor
from matrx_graph.nodes.text.render_list import RenderListExecutor
from matrx_graph.nodes.text.sections import SectionsPatchExecutor
from matrx_graph.nodes.text.repeated_lines import RemoveRepeatedLinesExecutor

__all__ = [
    "CustomExtractExecutor",
    "JoinExecutor",
    "JsonPathExecutor",
    "RegexExtractExecutor",
    "RegexReplaceExecutor",
    "RemoveRepeatedLinesExecutor",
    "RenderListExecutor",
    "SectionsPatchExecutor",
    "SlugExecutor",
    "SplitExecutor",
    "TemplateExecutor",
    "WordCountExecutor",
]
