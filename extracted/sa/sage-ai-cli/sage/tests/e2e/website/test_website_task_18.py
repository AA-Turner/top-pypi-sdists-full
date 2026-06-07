import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_18():
    """Verify exhaustive task creation via Website: Generate a basic GitHub Actions workflow...."""
    prompt = "Generate a basic GitHub Actions workflow."
    verify_website_with_rubric(prompt)
