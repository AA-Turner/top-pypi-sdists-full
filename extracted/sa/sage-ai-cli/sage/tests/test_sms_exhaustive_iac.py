import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

# Real cloud API calls — integration only.
pytestmark = [
    pytest.mark.timeout(900),
    pytest.mark.integration,
]


def test_sms_exhaustive_iac(tmp_path):
    """Verify exhaustive Terraform AWS ECS deployment IaC creation via SMS."""
    prompt = "Write Terraform IaC to deploy a Node.js app to AWS ECS."
    verify_sms_with_rubric(prompt, tmp_path)
