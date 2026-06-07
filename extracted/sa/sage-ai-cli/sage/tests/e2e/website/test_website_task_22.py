import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_22():
    """Verify exhaustive task creation via Website: Create a simple Flask application...."""
    prompt = "Create a simple Flask application."
    verify_website_with_rubric(prompt)
