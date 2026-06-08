import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_25(tmp_path):
    prompt = "Create a simple bash loop that counts from 1 to 5."
    verify_sms_with_rubric(prompt, tmp_path)
