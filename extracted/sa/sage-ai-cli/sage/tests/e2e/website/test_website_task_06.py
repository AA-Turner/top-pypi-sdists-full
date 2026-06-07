import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_06():
    """Verify exhaustive task creation via Website: Create a Dockerfile for a node app...."""
    prompt = "Create a Dockerfile for a node app."
    verify_website_with_rubric(prompt)
