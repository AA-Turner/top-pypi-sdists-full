import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_08():
    """Verify exhaustive task creation via Website: Create a python function to fetch data from an API..."""
    prompt = "Create a python function to fetch data from an API."
    verify_website_with_rubric(prompt)
