import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_05(tmp_path):
    prompt = "Write a bash script to print the current date."
    verify_sms_with_rubric(prompt, tmp_path)
