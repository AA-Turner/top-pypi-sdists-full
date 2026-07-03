"""Exhaustive test for cli, model cloud:mistral-7b, domain web."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_cli_cloud_mistral_7b_web(tmp_path):
    prompt = "Build a Vite + Vue3 counter application."
    task_with_model = f"{prompt} Use model cloud:mistral-7b."
    verify_cli_with_rubric(task_with_model, domain="web")
