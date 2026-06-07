import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_23():
    """Verify exhaustive task creation via Website: Generate a basic README template...."""
    prompt = "Generate a basic README template."
    verify_website_with_rubric(prompt)
