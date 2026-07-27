"""Exhaustive test for cli, model cloud:yi-coder-9b, domain mobile."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_cli_cloud_yi_coder_9b_mobile(tmp_path):
    prompt = "Build a Flutter login screen layout with email and password."
    task_with_model = f"{prompt} Use model cloud:yi-coder-9b."
    verify_cli_with_rubric(task_with_model, domain="mobile")
