import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_29(tmp_path):
    prompt = "Create a simple HTML form with input fields."
    verify_sms_with_rubric(prompt, tmp_path)
