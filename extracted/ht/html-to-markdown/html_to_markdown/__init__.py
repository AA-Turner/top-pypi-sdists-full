"""html-to-markdown: Convert HTML to Markdown using Rust backend.

This package provides high-performance HTML to Markdown conversion
powered by Rust with a clean Python API.

API:
    from html_to_markdown import convert, ConversionOptions

    result = convert("<h1>Hello</h1>")
    print(result["content"])  # "# Hello\n"
"""

from html_to_markdown.api import (
    ConversionResult,
    convert,
)
from html_to_markdown.exceptions import (
    ConflictingOptionsError,
    EmptyHtmlError,
    HtmlToMarkdownError,
    InvalidParserError,
    MissingDependencyError,
)
from html_to_markdown.options import ConversionOptions, OutputFormat, PreprocessingOptions

__all__ = [
    "ConflictingOptionsError",
    "ConversionOptions",
    "ConversionResult",
    "EmptyHtmlError",
    "HtmlToMarkdownError",
    "InvalidParserError",
    "MissingDependencyError",
    "OutputFormat",
    "PreprocessingOptions",
    "convert",
]

__version__ = "3.0.0"
