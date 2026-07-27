"""Exhaustive test for sms, model cloud:qwen3-coder, domain mobile."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_qwen3_coder_mobile_email(tmp_path):
    prompt = "Build a Flutter login screen layout with email and password."
    task_with_model = f"{prompt} Use model cloud:qwen3-coder."
    verify_sms_with_rubric(task_with_model, tmp_path)
