import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_21(tmp_path):
    prompt = "Create a basic nginx.conf template."
    verify_cli_with_rubric(prompt, tmp_path)
