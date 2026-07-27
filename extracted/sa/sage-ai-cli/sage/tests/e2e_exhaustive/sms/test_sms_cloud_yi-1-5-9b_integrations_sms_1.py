"""Exhaustive test for sms, model cloud:yi-1-5-9b, domain integrations."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_yi_1_5_9b_integrations_sms(tmp_path):
    prompt = "Send an email using smtplib to a test address."
    task_with_model = f"{prompt} Use model cloud:yi-1-5-9b."
    verify_sms_with_rubric(task_with_model, tmp_path)
