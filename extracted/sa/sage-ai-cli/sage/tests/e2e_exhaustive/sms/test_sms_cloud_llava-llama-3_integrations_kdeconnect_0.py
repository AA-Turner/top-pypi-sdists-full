"""Exhaustive test for sms, model cloud:llava-llama-3, domain integrations."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_llava_llama_3_integrations_kdeconnect(tmp_path):
    prompt = "Trigger an API call to Twilio to initiate a phone call."
    task_with_model = f"{prompt} Use model cloud:llava-llama-3."
    verify_sms_with_rubric(task_with_model, tmp_path)
