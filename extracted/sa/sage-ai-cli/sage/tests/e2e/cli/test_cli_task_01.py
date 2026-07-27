import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_01(tmp_path):
    prompt = "Write a quick sort algorithm in python."
    verify_cli_with_rubric(prompt, tmp_path)
