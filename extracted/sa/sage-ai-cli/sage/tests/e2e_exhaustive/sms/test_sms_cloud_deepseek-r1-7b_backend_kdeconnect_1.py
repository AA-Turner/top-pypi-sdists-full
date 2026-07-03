"""Exhaustive test for sms, model cloud:deepseek-r1-7b, domain backend."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_deepseek_r1_7b_backend_kdeconnect(tmp_path):
    prompt = "Create an Express.js server that connects to a mocked Postgres database."
    task_with_model = f"{prompt} Use model cloud:deepseek-r1-7b."
    verify_sms_with_rubric(task_with_model, tmp_path)
