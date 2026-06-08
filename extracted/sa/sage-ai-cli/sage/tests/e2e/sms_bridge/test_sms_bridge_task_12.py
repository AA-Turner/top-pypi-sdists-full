import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_12(tmp_path):
    prompt = "Implement binary search in Python."
    verify_sms_with_rubric(prompt, tmp_path)
