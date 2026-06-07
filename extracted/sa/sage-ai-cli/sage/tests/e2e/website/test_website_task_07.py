import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_07():
    """Verify exhaustive task creation via Website: Write a bash script to backup a directory...."""
    prompt = "Write a bash script to backup a directory."
    verify_website_with_rubric(prompt)
