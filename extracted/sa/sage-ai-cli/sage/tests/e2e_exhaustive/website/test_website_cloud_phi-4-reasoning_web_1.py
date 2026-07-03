"""Exhaustive test for website, model cloud:phi-4-reasoning, domain web."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_website_cloud_phi_4_reasoning_web(tmp_path):
    prompt = "Create a React to-do list component with state management."
    task_with_model = f"{prompt} Use model cloud:phi-4-reasoning."
    verify_website_with_rubric(task_with_model, tmp_path)
