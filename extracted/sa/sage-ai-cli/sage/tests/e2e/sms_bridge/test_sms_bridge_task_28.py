import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_28(tmp_path):
    prompt = "Write a Python script that reads a text file and prints its contents."
    verify_sms_with_rubric(prompt, tmp_path)
