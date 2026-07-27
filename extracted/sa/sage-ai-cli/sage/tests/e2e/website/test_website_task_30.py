import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_30(tmp_path):
    prompt = "Write a Python script that calculates the factorial of a number."
    verify_website_with_rubric(prompt, tmp_path)
