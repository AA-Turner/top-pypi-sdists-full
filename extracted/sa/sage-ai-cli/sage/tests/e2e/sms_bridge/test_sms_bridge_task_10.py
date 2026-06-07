import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_10(tmp_path):
    """Verify exhaustive task creation via SMS: Write a SQL query to join two tables...."""
    prompt = "Write a SQL query to join two tables."
    verify_sms_with_rubric(prompt, tmp_path)
