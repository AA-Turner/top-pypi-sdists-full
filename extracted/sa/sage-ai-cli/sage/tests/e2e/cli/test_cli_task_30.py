import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_30(tmp_path):
    prompt = "Write a Python script that calculates the factorial of a number."
    verify_cli_with_rubric(prompt, tmp_path)
