import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_14():
    """Verify exhaustive task creation via Website: Create a simple Makefile for a C program...."""
    prompt = "Create a simple Makefile for a C program."
    verify_website_with_rubric(prompt)
