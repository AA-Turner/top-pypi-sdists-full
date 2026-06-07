import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_05(tmp_path):
    """Verify exhaustive task creation via SMS: Generate a simple react component...."""
    prompt = "Generate a simple react component."
    verify_sms_with_rubric(prompt, tmp_path)
