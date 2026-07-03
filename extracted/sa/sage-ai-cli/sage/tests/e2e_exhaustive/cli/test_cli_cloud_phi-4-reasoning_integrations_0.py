"""Exhaustive test for cli, model cloud:phi-4-reasoning, domain integrations."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_cli_cloud_phi_4_reasoning_integrations(tmp_path):
    prompt = "Trigger an API call to Twilio to initiate a phone call."
    task_with_model = f"{prompt} Use model cloud:phi-4-reasoning."
    verify_cli_with_rubric(task_with_model, domain="integrations")
