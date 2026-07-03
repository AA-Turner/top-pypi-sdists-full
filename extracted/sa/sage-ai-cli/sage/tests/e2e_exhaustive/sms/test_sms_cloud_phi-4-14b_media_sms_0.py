"""Exhaustive test for sms, model cloud:phi-4-14b, domain media."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_phi_4_14b_media_sms(tmp_path):
    prompt = "Generate a simple SVG logo with a circle and text."
    task_with_model = f"{prompt} Use model cloud:phi-4-14b."
    verify_sms_with_rubric(task_with_model, tmp_path)
