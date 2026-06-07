import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_19(tmp_path):
    """Verify exhaustive task creation via SMS: Create a simple CSS grid layout...."""
    prompt = "Create a simple CSS grid layout."
    verify_sms_with_rubric(prompt, tmp_path)
