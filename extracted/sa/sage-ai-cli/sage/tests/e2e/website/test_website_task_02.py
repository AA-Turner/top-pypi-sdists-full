import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_02(tmp_path):
    prompt = "Build a basic HTML landing page with a header and footer."
    verify_website_with_rubric(prompt, tmp_path)
