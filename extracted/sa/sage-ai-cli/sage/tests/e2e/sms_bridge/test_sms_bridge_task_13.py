import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_13(tmp_path):
    prompt = "Create a basic .gitignore file for Python projects."
    verify_sms_with_rubric(prompt, tmp_path)
