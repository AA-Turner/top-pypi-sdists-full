"""Exhaustive test for sms, model cloud:gemma-2-9b, domain video_games."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_gemma_2_9b_video_games_sms(tmp_path):
    prompt = "Write a Unity C# script for basic player movement."
    task_with_model = f"{prompt} Use model cloud:gemma-2-9b."
    verify_sms_with_rubric(task_with_model, tmp_path)
