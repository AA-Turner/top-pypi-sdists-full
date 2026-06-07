import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_11(tmp_path):
    """Verify exhaustive task creation via SMS: Create a fast API server with one route...."""
    prompt = "Create a fast API server with one route."
    verify_sms_with_rubric(prompt, tmp_path)
