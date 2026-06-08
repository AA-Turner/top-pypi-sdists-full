import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_15(tmp_path):
    prompt = "Generate a basic GitHub Actions workflow YAML."
    verify_cli_with_rubric(prompt, tmp_path)
