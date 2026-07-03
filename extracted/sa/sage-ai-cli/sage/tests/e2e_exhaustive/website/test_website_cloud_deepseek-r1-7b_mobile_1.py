"""Exhaustive test for website, model cloud:deepseek-r1-7b, domain mobile."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_website_cloud_deepseek_r1_7b_mobile(tmp_path):
    prompt = "Build a Flutter login screen layout with email and password."
    task_with_model = f"{prompt} Use model cloud:deepseek-r1-7b."
    verify_website_with_rubric(task_with_model, tmp_path)
