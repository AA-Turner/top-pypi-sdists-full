import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_03(tmp_path):
    prompt = "Generate a simple React functional component that renders a button."
    verify_sms_with_rubric(prompt, tmp_path)
