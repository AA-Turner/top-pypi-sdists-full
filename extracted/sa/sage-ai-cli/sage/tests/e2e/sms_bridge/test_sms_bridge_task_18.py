import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_18(tmp_path):
    """Verify exhaustive task creation via SMS: Generate a basic GitHub Actions workflow...."""
    prompt = "Generate a basic GitHub Actions workflow."
    verify_sms_with_rubric(prompt, tmp_path)
