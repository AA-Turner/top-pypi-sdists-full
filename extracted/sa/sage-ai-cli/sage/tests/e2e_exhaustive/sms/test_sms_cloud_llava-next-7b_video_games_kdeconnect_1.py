"""Exhaustive test for sms, model cloud:llava-next-7b, domain video_games."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_llava_next_7b_video_games_kdeconnect(tmp_path):
    prompt = "Write a Unity C# script for basic player movement."
    task_with_model = f"{prompt} Use model cloud:llava-next-7b."
    verify_sms_with_rubric(task_with_model, tmp_path)
