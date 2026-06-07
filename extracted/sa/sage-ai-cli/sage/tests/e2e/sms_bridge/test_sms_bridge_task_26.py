import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_26(tmp_path):
    """Verify exhaustive task creation via SMS: Write a simple unit test using pytest...."""
    prompt = "Write a simple unit test using pytest."
    verify_sms_with_rubric(prompt, tmp_path)
