import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_29(tmp_path):
    """Verify exhaustive task creation via SMS: Generate a basic package.json file...."""
    prompt = "Generate a basic package.json file."
    verify_sms_with_rubric(prompt, tmp_path)
