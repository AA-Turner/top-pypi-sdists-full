import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_01(tmp_path):
    prompt = "Write a quick sort algorithm in python."
    verify_website_with_rubric(prompt, tmp_path)
