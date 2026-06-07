import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_09(tmp_path):
    """Verify exhaustive task creation via SMS: Implement a simple calculator class in python...."""
    prompt = "Implement a simple calculator class in python."
    verify_sms_with_rubric(prompt, tmp_path)
