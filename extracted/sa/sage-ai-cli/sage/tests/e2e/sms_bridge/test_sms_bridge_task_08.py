import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_08(tmp_path):
    """Verify exhaustive task creation via SMS: Create a python function to fetch data from an API..."""
    prompt = "Create a python function to fetch data from an API."
    verify_sms_with_rubric(prompt, tmp_path)
