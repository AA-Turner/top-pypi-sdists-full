"""Exhaustive test for website, model cloud:llava-llama-3, domain web."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_website_cloud_llava_llama_3_web(tmp_path):
    prompt = "Build a simple HTML landing page with CSS grid and a contact form."
    task_with_model = f"{prompt} Use model cloud:llava-llama-3."
    verify_website_with_rubric(task_with_model, tmp_path)
