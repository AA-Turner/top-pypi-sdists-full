"""Exhaustive test for cli, model cloud:yi-coder-9b, domain integrations."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_cli_cloud_yi_coder_9b_integrations(tmp_path):
    prompt = "Send an email using smtplib to a test address."
    task_with_model = f"{prompt} Use model cloud:yi-coder-9b."
    verify_cli_with_rubric(task_with_model, domain="integrations")
