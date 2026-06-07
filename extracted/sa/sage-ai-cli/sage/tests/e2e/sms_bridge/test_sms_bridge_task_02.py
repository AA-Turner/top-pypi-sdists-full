import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_02(tmp_path):
    """Verify exhaustive task creation via SMS: Create a python script that prints 'hello world'...."""
    prompt = "Create a python script that prints 'hello world'."
    verify_sms_with_rubric(prompt, tmp_path)
