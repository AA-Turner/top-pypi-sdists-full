"""Exhaustive test for cli, model cloud:llama-3-1-8b, domain backend."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_cli_cloud_llama_3_1_8b_backend(tmp_path):
    prompt = "Write a FastAPI server with a single POST route that echoes JSON."
    task_with_model = f"{prompt} Use model cloud:llama-3-1-8b."
    verify_cli_with_rubric(task_with_model, domain="backend")
