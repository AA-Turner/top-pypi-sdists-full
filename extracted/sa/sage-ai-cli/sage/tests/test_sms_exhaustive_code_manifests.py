import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

# Real cloud API calls — integration only.
pytestmark = [
    pytest.mark.timeout(900),
    pytest.mark.integration,
]


def test_sms_exhaustive_code_manifests(tmp_path):
    """Verify exhaustive multi-file script, JSON config and YAML manifest creation via SMS."""
    prompt = "Write a complex Python script, a JSON config, and a YAML manifest."
    verify_sms_with_rubric(prompt, tmp_path)
