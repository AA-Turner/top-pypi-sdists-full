"""Exhaustive test for sms, model cloud:llava-llama-3, domain backend."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_llava_llama_3_backend_email(tmp_path):
    prompt = "Write a FastAPI server with a single POST route that echoes JSON."
    task_with_model = f"{prompt} Use model cloud:llava-llama-3."
    verify_sms_with_rubric(task_with_model, tmp_path)
