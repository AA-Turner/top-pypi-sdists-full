import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_16():
    """Verify exhaustive task creation via Website: Create a gitignore file for python projects...."""
    prompt = "Create a gitignore file for python projects."
    verify_website_with_rubric(prompt)
