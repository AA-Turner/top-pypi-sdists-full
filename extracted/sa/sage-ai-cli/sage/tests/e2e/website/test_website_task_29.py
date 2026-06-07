import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_29():
    """Verify exhaustive task creation via Website: Generate a basic package.json file...."""
    prompt = "Generate a basic package.json file."
    verify_website_with_rubric(prompt)
