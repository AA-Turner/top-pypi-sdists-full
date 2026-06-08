import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_08(tmp_path):
    prompt = "Create a fast API server with a single GET route."
    verify_sms_with_rubric(prompt, tmp_path)
