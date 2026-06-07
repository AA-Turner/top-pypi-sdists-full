import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_12(tmp_path):
    """Verify exhaustive task creation via SMS: Generate a JSON schema for a user profile...."""
    prompt = "Generate a JSON schema for a user profile."
    verify_sms_with_rubric(prompt, tmp_path)
