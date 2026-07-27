"""Exhaustive test for website, model cloud:llava-llama-3, domain video_games."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_website_cloud_llava_llama_3_video_games(tmp_path):
    prompt = "Write a Unity C# script for basic player movement."
    task_with_model = f"{prompt} Use model cloud:llava-llama-3."
    verify_website_with_rubric(task_with_model, tmp_path)
