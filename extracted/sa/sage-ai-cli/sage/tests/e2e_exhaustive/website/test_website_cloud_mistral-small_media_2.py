"""Exhaustive test for website, model cloud:mistral-small, domain media."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_website_cloud_mistral_small_media(tmp_path):
    prompt = "Write a script that outputs a valid markdown document with a table."
    task_with_model = f"{prompt} Use model cloud:mistral-small."
    verify_website_with_rubric(task_with_model, tmp_path)
