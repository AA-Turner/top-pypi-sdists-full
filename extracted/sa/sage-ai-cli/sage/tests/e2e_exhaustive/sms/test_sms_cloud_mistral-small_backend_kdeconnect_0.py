"""Exhaustive test for sms, model cloud:mistral-small, domain backend."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_mistral_small_backend_kdeconnect(tmp_path):
    prompt = "Write a FastAPI server with a single POST route that echoes JSON."
    task_with_model = f"{prompt} Use model cloud:mistral-small."
    verify_sms_with_rubric(task_with_model, tmp_path)
