"""Exhaustive test for sms, model cloud:yi-coder-9b, domain integrations."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_yi_coder_9b_integrations_sms(tmp_path):
    prompt = "Trigger an API call to Twilio to initiate a phone call."
    task_with_model = f"{prompt} Use model cloud:yi-coder-9b."
    verify_sms_with_rubric(task_with_model, tmp_path)
