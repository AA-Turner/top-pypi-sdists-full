import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_04(tmp_path):
    """Verify exhaustive task creation via SMS: Build a basic HTML landing page...."""
    prompt = "Build a basic HTML landing page."
    verify_sms_with_rubric(prompt, tmp_path)
