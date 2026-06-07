import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_19():
    """Verify exhaustive task creation via Website: Create a simple CSS grid layout...."""
    prompt = "Create a simple CSS grid layout."
    verify_website_with_rubric(prompt)
