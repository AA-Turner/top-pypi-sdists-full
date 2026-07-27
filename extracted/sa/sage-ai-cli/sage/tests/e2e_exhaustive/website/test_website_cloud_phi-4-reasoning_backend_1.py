"""Exhaustive test for website, model cloud:phi-4-reasoning, domain backend."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_website_cloud_phi_4_reasoning_backend(tmp_path):
    prompt = "Create an Express.js server that connects to a mocked Postgres database."
    task_with_model = f"{prompt} Use model cloud:phi-4-reasoning."
    verify_website_with_rubric(task_with_model, tmp_path)
