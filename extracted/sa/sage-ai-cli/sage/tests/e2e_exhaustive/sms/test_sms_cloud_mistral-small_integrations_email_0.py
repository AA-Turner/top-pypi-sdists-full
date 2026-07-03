"""Exhaustive test for sms, model cloud:mistral-small, domain integrations."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_mistral_small_integrations_email(tmp_path):
    prompt = "Trigger an API call to Twilio to initiate a phone call."
    task_with_model = f"{prompt} Use model cloud:mistral-small."
    verify_sms_with_rubric(task_with_model, tmp_path)
