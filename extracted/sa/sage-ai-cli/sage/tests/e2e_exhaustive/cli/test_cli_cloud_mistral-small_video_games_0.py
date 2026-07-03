"""Exhaustive test for cli, model cloud:mistral-small, domain video_games."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_cli_cloud_mistral_small_video_games(tmp_path):
    prompt = "Create a simple Pygame script that draws a moving square."
    task_with_model = f"{prompt} Use model cloud:mistral-small."
    verify_cli_with_rubric(task_with_model, domain="video_games")
