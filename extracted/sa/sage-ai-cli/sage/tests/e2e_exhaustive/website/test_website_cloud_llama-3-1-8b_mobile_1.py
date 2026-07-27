"""Exhaustive test for website, model cloud:llama-3-1-8b, domain mobile."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_website_cloud_llama_3_1_8b_mobile(tmp_path):
    prompt = "Build a Flutter login screen layout with email and password."
    task_with_model = f"{prompt} Use model cloud:llama-3-1-8b."
    verify_website_with_rubric(task_with_model, tmp_path)
