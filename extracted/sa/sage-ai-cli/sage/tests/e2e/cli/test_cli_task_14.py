import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_14(tmp_path):
    prompt = "Write a python script to parse a simple CSV file."
    verify_cli_with_rubric(prompt, tmp_path)
