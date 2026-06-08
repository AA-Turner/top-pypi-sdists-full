import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_24(tmp_path):
    prompt = "Write a python script to reverse a string."
    verify_cli_with_rubric(prompt, tmp_path)
