import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_06(tmp_path):
    """Verify exhaustive task creation via SMS: Create a Dockerfile for a node app...."""
    prompt = "Create a Dockerfile for a node app."
    verify_sms_with_rubric(prompt, tmp_path)
