"""Exhaustive test for cli, model cloud:phi-4-reasoning, domain backend."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_cli_cloud_phi_4_reasoning_backend(tmp_path):
    prompt = "Write a FastAPI server with a single POST route that echoes JSON."
    task_with_model = f"{prompt} Use model cloud:phi-4-reasoning."
    verify_cli_with_rubric(task_with_model, domain="backend")
