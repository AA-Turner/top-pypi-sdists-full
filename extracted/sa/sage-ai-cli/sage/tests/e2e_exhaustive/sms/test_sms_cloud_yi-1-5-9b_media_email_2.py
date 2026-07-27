"""Exhaustive test for sms, model cloud:yi-1-5-9b, domain media."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_yi_1_5_9b_media_email(tmp_path):
    prompt = "Write a script that outputs a valid markdown document with a table."
    task_with_model = f"{prompt} Use model cloud:yi-1-5-9b."
    verify_sms_with_rubric(task_with_model, tmp_path)
