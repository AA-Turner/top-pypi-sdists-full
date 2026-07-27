import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

@pytest.mark.parametrize("framework", ["react_native", "flutter_bloc", "swiftui"])
def test_mobile_framework_generation(framework):
    """Verify mobile framework tasks are written cleanly and comply with the grading rubric."""
    prompt = f"Implement a complete {framework} mobile component with lists and navigation."
    verify_cli_with_rubric(prompt)


@pytest.mark.parametrize("framework", ["react_native", "flutter_bloc", "swiftui"])
def test_mobile_framework_generation_sms(framework, tmp_path):
    """Verify mobile framework tasks via SMS bridge."""
    prompt = f"Implement a complete {framework} mobile component with lists and navigation."
    verify_sms_with_rubric(prompt, tmp_path)


@pytest.mark.parametrize("framework", ["react_native", "flutter_bloc", "swiftui"])
def test_mobile_framework_generation_website(framework):
    """Verify mobile framework tasks via website backend."""
    prompt = f"Implement a complete {framework} mobile component with lists and navigation."
    verify_website_with_rubric(prompt)
