"""Exhaustive test for website, model cloud:phi-4-reasoning, domain media."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_website_cloud_phi_4_reasoning_media(tmp_path):
    prompt = "Generate a simple SVG logo with a circle and text."
    task_with_model = f"{prompt} Use model cloud:phi-4-reasoning."
    verify_website_with_rubric(task_with_model, tmp_path)
