"""Exhaustive test for cli, model cloud:yi-1-5-9b, domain backend."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_cli_cloud_yi_1_5_9b_backend(tmp_path):
    prompt = "Create an Express.js server that connects to a mocked Postgres database."
    task_with_model = f"{prompt} Use model cloud:yi-1-5-9b."
    verify_cli_with_rubric(task_with_model, domain="backend")
