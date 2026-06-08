import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_06(tmp_path):
    prompt = "Implement a basic calculator class in Python."
    verify_sms_with_rubric(prompt, tmp_path)
