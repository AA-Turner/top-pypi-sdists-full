"""Exhaustive test for website, model cloud:qwen3-coder, domain mobile."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_website_cloud_qwen3_coder_mobile(tmp_path):
    prompt = "Create a React Native screen with a flatlist and pull-to-refresh."
    task_with_model = f"{prompt} Use model cloud:qwen3-coder."
    verify_website_with_rubric(task_with_model, tmp_path)
