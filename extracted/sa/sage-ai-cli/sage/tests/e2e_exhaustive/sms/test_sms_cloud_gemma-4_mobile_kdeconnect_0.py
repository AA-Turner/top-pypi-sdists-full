"""Exhaustive test for sms, model cloud:gemma-4, domain mobile."""
import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

def test_sms_cloud_gemma_4_mobile_kdeconnect(tmp_path):
    prompt = "Create a React Native screen with a flatlist and pull-to-refresh."
    task_with_model = f"{prompt} Use model cloud:gemma-4."
    verify_sms_with_rubric(task_with_model, tmp_path)
