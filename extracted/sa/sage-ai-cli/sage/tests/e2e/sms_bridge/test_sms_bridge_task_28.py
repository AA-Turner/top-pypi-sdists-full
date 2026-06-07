import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_28(tmp_path):
    """Verify exhaustive task creation via SMS: Implement a queue data structure in Python...."""
    prompt = "Implement a queue data structure in Python."
    verify_sms_with_rubric(prompt, tmp_path)
