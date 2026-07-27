"""Exhaustive test for sms, model cloud:yi-coder-9b, domain video_games."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_yi_coder_9b_video_games_kdeconnect(tmp_path):
    prompt = "Create a simple Pygame script that draws a moving square."
    task_with_model = f"{prompt} Use model cloud:yi-coder-9b."
    verify_sms_with_rubric(task_with_model, tmp_path)
