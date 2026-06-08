import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_30(tmp_path):
    prompt = "Write a Python script that calculates the factorial of a number."
    verify_sms_with_rubric(prompt, tmp_path)
