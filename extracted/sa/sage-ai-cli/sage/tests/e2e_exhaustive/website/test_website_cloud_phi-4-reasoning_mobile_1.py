"""Exhaustive test for website, model cloud:phi-4-reasoning, domain mobile."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_website_cloud_phi_4_reasoning_mobile(tmp_path):
    prompt = "Build a Flutter login screen layout with email and password."
    task_with_model = f"{prompt} Use model cloud:phi-4-reasoning."
    verify_website_with_rubric(task_with_model, tmp_path)
