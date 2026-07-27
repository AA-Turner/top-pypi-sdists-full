import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_27(tmp_path):
    prompt = "Implement a Fibonacci sequence generator in Python."
    verify_website_with_rubric(prompt, tmp_path)
