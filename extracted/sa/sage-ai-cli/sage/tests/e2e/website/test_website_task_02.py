import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_02():
    """Verify exhaustive task creation via Website: Create a python script that prints 'hello world'...."""
    prompt = "Create a python script that prints 'hello world'."
    verify_website_with_rubric(prompt)
