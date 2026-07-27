"""Exhaustive test for cli, model cloud:qwen-coder-7b, domain media."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_cli_cloud_qwen_coder_7b_media(tmp_path):
    prompt = "Write a script that outputs a valid markdown document with a table."
    task_with_model = f"{prompt} Use model cloud:qwen-coder-7b."
    verify_cli_with_rubric(task_with_model, domain="media")
