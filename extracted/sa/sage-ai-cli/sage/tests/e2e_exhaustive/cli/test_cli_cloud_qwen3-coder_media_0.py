"""Exhaustive test for cli, model cloud:qwen3-coder, domain media."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_cli_cloud_qwen3_coder_media(tmp_path):
    prompt = "Generate a simple SVG logo with a circle and text."
    task_with_model = f"{prompt} Use model cloud:qwen3-coder."
    verify_cli_with_rubric(task_with_model, domain="media")
