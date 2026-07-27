import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

# Real cloud API calls — integration only.
pytestmark = [
    pytest.mark.timeout(900),
    pytest.mark.integration,
]


@pytest.mark.parametrize("framework", ["react_native", "flutter_bloc", "swiftui"])
def test_mobile_framework_generation_sms(framework, tmp_path):
    """Verify mobile app framework component creation via SMS."""
    prompt = f"Implement a complete {framework} mobile component with lists and navigation."
    verify_sms_with_rubric(prompt, tmp_path)
