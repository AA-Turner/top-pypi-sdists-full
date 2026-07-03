"""Exhaustive test for website, model cloud:deepseek-r1-7b, domain backend."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_website_cloud_deepseek_r1_7b_backend(tmp_path):
    prompt = "Write a FastAPI server with a single POST route that echoes JSON."
    task_with_model = f"{prompt} Use model cloud:deepseek-r1-7b."
    verify_website_with_rubric(task_with_model, tmp_path)
