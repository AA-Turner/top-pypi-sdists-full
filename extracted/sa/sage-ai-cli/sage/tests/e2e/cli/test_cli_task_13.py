import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_13(tmp_path):
    prompt = "Create a basic .gitignore file for Python projects."
    verify_cli_with_rubric(prompt, tmp_path)
