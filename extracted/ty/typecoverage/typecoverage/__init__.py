"""
Typecoverage - Python Type Annotation Analyzer.

A comprehensive static analysis tool for detecting missing type annotations
in Python code.
"""

from .core import (  # pragma: no cover
    VERSION,
    Colors,
    DemoClass,
    Issue,
    IssueType,
    Scope,
    Stats,
    TypeCoverage,
    analyze_targets,
    demo_func,
    detect_untyped,
    parse_and_run,
)

__version__ = "0.1.8"
__author__ = "Joao Lopes"
__email__ = "joaoslopes@gmail.com"

__all__ = [
    "VERSION",
    "Colors",
    "TypeCoverage",
    "Issue",
    "IssueType",
    "Scope",
    "Stats",
    "detect_untyped",
    "parse_and_run",
    "analyze_targets",
    "demo_func",
    "DemoClass",
    "analyze_targets",
    "demo_func",
    "DemoClass",
    "parse_and_run",
]
