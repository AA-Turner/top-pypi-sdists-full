import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_exhaustive_iac(tmp_path):
    """Verify exhaustive Terraform AWS ECS deployment IaC creation via SMS."""
    prompt = "Write Terraform IaC to deploy a Node.js app to AWS ECS."
    verify_sms_with_rubric(prompt, tmp_path)
