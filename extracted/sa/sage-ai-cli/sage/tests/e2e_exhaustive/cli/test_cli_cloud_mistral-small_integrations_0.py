"""Exhaustive test for cli, model cloud:mistral-small, domain integrations."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_cli_cloud_mistral_small_integrations(tmp_path):
    prompt = "Use a native macOS AppleScript to initiate a FaceTime audio phone call."
    task_with_model = f"{prompt} Use model cloud:mistral-small."
    verify_cli_with_rubric(task_with_model, domain="integrations")
