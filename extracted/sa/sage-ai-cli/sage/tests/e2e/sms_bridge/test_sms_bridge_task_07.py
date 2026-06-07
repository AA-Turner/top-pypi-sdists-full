import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_07(tmp_path):
    """Verify exhaustive task creation via SMS: Write a bash script to backup a directory...."""
    prompt = "Write a bash script to backup a directory."
    verify_sms_with_rubric(prompt, tmp_path)
