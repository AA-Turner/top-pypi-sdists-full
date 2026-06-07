import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_25():
    """Verify exhaustive task creation via Website: Create a python script to scrape a webpage...."""
    prompt = "Create a python script to scrape a webpage."
    verify_website_with_rubric(prompt)
