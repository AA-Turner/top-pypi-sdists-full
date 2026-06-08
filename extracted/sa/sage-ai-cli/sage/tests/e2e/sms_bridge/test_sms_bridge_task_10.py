import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_10(tmp_path):
    prompt = "Write a Python regex to match valid email addresses."
    verify_sms_with_rubric(prompt, tmp_path)
