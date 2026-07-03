"""Exhaustive test for sms, model cloud:phi-4-reasoning, domain media."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_phi_4_reasoning_media_kdeconnect(tmp_path):
    prompt = "Write a script that outputs a valid markdown document with a table."
    task_with_model = f"{prompt} Use model cloud:phi-4-reasoning."
    verify_sms_with_rubric(task_with_model, tmp_path)
