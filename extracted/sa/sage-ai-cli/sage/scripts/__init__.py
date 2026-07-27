"""SAGE AI CLI utility scripts."""

# TDD enforcement is now in sage.core.tdd
# This module provides CLI access for manual validation
from sage.scripts.tdd_enforce import main as tdd_main

__all__ = ["tdd_main"]
