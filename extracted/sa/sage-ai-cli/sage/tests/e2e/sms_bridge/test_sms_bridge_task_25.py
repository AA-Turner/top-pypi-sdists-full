import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_25(tmp_path):
    """Verify exhaustive task creation via SMS: Create a python script to scrape a webpage...."""
    prompt = "Create a python script to scrape a webpage."
    verify_sms_with_rubric(prompt, tmp_path)
