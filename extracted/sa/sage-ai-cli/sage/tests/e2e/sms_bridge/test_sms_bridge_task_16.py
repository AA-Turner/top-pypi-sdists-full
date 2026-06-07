import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_16(tmp_path):
    """Verify exhaustive task creation via SMS: Create a gitignore file for python projects...."""
    prompt = "Create a gitignore file for python projects."
    verify_sms_with_rubric(prompt, tmp_path)
