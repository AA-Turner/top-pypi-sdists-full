"""Exhaustive test for website, model cloud:yi-1-5-9b, domain web."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_website_cloud_yi_1_5_9b_web(tmp_path):
    prompt = "Build a simple HTML landing page with CSS grid and a contact form."
    task_with_model = f"{prompt} Use model cloud:yi-1-5-9b."
    verify_website_with_rubric(task_with_model, tmp_path)
