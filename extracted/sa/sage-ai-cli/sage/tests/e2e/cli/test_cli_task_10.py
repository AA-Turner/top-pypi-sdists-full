import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_10(tmp_path):
    prompt = "Write a Python regex to match valid email addresses."
    verify_cli_with_rubric(prompt, tmp_path)
