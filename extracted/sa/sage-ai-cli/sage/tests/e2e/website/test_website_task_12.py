import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_12():
    """Verify exhaustive task creation via Website: Generate a JSON schema for a user profile...."""
    prompt = "Generate a JSON schema for a user profile."
    verify_website_with_rubric(prompt)
