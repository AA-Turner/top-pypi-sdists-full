import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_30():
    """Verify exhaustive task creation via Website: Write a python script to send an email...."""
    prompt = "Write a python script to send an email."
    verify_website_with_rubric(prompt)
