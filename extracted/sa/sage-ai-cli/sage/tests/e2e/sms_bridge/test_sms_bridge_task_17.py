import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_17(tmp_path):
    """Verify exhaustive task creation via SMS: Write a script to parse a CSV file...."""
    prompt = "Write a script to parse a CSV file."
    verify_sms_with_rubric(prompt, tmp_path)
