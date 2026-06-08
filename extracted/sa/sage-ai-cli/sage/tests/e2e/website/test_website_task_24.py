import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_24(tmp_path):
    prompt = "Write a python script to reverse a string."
    verify_website_with_rubric(prompt, tmp_path)
