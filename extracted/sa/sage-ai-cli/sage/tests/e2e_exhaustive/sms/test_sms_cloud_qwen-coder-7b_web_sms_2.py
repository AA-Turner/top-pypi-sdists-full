"""Exhaustive test for sms, model cloud:qwen-coder-7b, domain web."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_qwen_coder_7b_web_sms(tmp_path):
    prompt = "Build a Vite + Vue3 counter application."
    task_with_model = f"{prompt} Use model cloud:qwen-coder-7b."
    verify_sms_with_rubric(task_with_model, tmp_path)
