import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_15(tmp_path):
    """Verify exhaustive task creation via SMS: Implement binary search in Python...."""
    prompt = "Implement binary search in Python."
    verify_sms_with_rubric(prompt, tmp_path)
