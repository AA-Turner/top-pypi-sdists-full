import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_21(tmp_path):
    prompt = "Create a basic nginx.conf template."
    verify_website_with_rubric(prompt, tmp_path)
