"""Exhaustive test for website, model cloud:phi-4-14b, domain mobile."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_website_cloud_phi_4_14b_mobile(tmp_path):
    prompt = "Create a React Native screen with a flatlist and pull-to-refresh."
    task_with_model = f"{prompt} Use model cloud:phi-4-14b."
    verify_website_with_rubric(task_with_model, tmp_path)
