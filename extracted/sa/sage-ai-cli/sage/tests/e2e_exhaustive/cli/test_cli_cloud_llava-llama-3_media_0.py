"""Exhaustive test for cli, model cloud:llava-llama-3, domain media."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_cli_cloud_llava_llama_3_media(tmp_path):
    prompt = "Generate a simple SVG logo with a circle and text."
    task_with_model = f"{prompt} Use model cloud:llava-llama-3."
    verify_cli_with_rubric(task_with_model, domain="media")
