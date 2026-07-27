import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_02(tmp_path):
    prompt = "Build a basic HTML landing page with a header and footer."
    verify_cli_with_rubric(prompt, tmp_path)
