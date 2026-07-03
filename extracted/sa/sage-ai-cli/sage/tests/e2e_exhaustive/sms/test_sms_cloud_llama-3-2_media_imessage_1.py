"""Exhaustive test for sms, model cloud:llama-3-2, domain media."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_llama_3_2_media_imessage(tmp_path):
    prompt = "Create an HTML5 canvas animation of a bouncing ball."
    task_with_model = f"{prompt} Use model cloud:llama-3-2."
    verify_sms_with_rubric(task_with_model, tmp_path)
