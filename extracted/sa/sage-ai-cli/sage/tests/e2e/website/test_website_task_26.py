import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_26(tmp_path):
    prompt = "Write a Python function to check if a number is prime."
    verify_website_with_rubric(prompt, tmp_path)
