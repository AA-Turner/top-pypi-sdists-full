"""Exhaustive test for sms, model cloud:llava-llama-3, domain web."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_llava_llama_3_web_sms(tmp_path):
    prompt = "Build a simple HTML landing page with CSS grid and a contact form."
    task_with_model = f"{prompt} Use model cloud:llava-llama-3."
    verify_sms_with_rubric(task_with_model, tmp_path)
