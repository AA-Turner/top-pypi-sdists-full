import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_05(tmp_path):
    prompt = "Write a bash script to print the current date."
    verify_website_with_rubric(prompt, tmp_path)
