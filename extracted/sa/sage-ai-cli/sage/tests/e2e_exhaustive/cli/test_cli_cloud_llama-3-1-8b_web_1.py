"""Exhaustive test for cli, model cloud:llama-3-1-8b, domain web."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_cli_cloud_llama_3_1_8b_web(tmp_path):
    prompt = "Create a React to-do list component with state management."
    task_with_model = f"{prompt} Use model cloud:llama-3-1-8b."
    verify_cli_with_rubric(task_with_model, domain="web")
