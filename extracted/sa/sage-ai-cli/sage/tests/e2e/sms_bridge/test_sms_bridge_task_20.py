import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_20(tmp_path):
    """Verify exhaustive task creation via SMS: Implement a stack data structure in Python...."""
    prompt = "Implement a stack data structure in Python."
    verify_sms_with_rubric(prompt, tmp_path)
