"""Exhaustive test for website, model cloud:mistral-7b, domain video_games."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_website_cloud_mistral_7b_video_games(tmp_path):
    prompt = "Write a Unity C# script for basic player movement."
    task_with_model = f"{prompt} Use model cloud:mistral-7b."
    verify_website_with_rubric(task_with_model, tmp_path)
