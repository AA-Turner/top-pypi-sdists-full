"""Exhaustive test for cli, model cloud:qwen3-coder, domain integrations."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_cli_cloud_qwen3_coder_integrations(tmp_path):
    prompt = "Trigger an API call to Twilio to initiate a phone call."
    task_with_model = f"{prompt} Use model cloud:qwen3-coder."
    verify_cli_with_rubric(task_with_model, domain="integrations")
