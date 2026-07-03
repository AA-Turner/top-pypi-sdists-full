"""Exhaustive test for sms, model cloud:gemma-4, domain backend."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_gemma_4_backend_sms(tmp_path):
    prompt = "Create an Express.js server that connects to a mocked Postgres database."
    task_with_model = f"{prompt} Use model cloud:gemma-4."
    verify_sms_with_rubric(task_with_model, tmp_path)
