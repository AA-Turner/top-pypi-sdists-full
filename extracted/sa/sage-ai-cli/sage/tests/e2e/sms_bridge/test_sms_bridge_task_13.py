import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_13(tmp_path):
    """Verify exhaustive task creation via SMS: Write a regex to match email addresses...."""
    prompt = "Write a regex to match email addresses."
    verify_sms_with_rubric(prompt, tmp_path)
