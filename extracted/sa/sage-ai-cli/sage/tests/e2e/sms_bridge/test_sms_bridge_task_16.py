import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_16(tmp_path):
    prompt = "Create a simple CSS grid layout with 3 columns."
    verify_sms_with_rubric(prompt, tmp_path)
