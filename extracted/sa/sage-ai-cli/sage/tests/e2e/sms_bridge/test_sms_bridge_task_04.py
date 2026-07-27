import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_04(tmp_path):
    prompt = "Create a Dockerfile for a basic Node.js application."
    verify_sms_with_rubric(prompt, tmp_path)
