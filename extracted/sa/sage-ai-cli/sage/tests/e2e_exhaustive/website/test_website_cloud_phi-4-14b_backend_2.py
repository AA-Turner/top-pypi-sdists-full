"""Exhaustive test for website, model cloud:phi-4-14b, domain backend."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_website_cloud_phi_4_14b_backend(tmp_path):
    prompt = "Write a Python script to parse a CSV file and output JSON."
    task_with_model = f"{prompt} Use model cloud:phi-4-14b."
    verify_website_with_rubric(task_with_model, tmp_path)
