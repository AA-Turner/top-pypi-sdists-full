"""Exhaustive test for cli, model cloud:qwen-coder-7b, domain video_games."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_cli_cloud_qwen_coder_7b_video_games(tmp_path):
    prompt = "Write a Unity C# script for basic player movement."
    task_with_model = f"{prompt} Use model cloud:qwen-coder-7b."
    verify_cli_with_rubric(task_with_model, domain="video_games")
