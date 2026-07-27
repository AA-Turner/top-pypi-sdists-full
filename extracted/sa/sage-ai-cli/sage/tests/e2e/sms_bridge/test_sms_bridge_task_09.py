import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_09(tmp_path):
    prompt = "Generate a JSON schema for a simple user profile."
    verify_sms_with_rubric(prompt, tmp_path)
