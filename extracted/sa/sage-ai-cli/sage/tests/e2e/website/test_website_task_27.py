import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_27():
    """Verify exhaustive task creation via Website: Create a basic nginx configuration file...."""
    prompt = "Create a basic nginx configuration file."
    verify_website_with_rubric(prompt)
