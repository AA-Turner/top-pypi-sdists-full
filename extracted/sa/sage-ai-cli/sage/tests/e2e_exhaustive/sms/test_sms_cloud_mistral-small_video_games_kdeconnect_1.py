"""Exhaustive test for sms, model cloud:mistral-small, domain video_games."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_mistral_small_video_games_kdeconnect(tmp_path):
    prompt = "Write a Unity C# script for basic player movement."
    task_with_model = f"{prompt} Use model cloud:mistral-small."
    verify_sms_with_rubric(task_with_model, tmp_path)
