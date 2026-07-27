import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_14(tmp_path):
    prompt = "Write a python script to parse a simple CSV file."
    verify_sms_with_rubric(prompt, tmp_path)
