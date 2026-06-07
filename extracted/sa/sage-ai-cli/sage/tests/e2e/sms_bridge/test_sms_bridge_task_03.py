import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_03(tmp_path):
    """Verify exhaustive task creation via SMS: Write a quick sort algorithm in python...."""
    prompt = "Write a quick sort algorithm in python."
    verify_sms_with_rubric(prompt, tmp_path)
