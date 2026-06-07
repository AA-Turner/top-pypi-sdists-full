import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_14():
    """Verify exhaustive task creation via CLI: Create a simple Makefile for a C program...."""
    prompt = "Create a simple Makefile for a C program."
    verify_cli_with_rubric(prompt)
