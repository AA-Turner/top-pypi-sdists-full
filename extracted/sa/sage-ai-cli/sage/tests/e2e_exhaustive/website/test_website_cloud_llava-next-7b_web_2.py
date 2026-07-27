"""Exhaustive test for website, model cloud:llava-next-7b, domain web."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_website_cloud_llava_next_7b_web(tmp_path):
    prompt = "Build a Vite + Vue3 counter application."
    task_with_model = f"{prompt} Use model cloud:llava-next-7b."
    verify_website_with_rubric(task_with_model, tmp_path)
