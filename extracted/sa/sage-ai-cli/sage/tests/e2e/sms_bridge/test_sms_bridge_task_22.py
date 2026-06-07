import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_22(tmp_path):
    """Verify exhaustive task creation via SMS: Create a simple Flask application...."""
    prompt = "Create a simple Flask application."
    verify_sms_with_rubric(prompt, tmp_path)
