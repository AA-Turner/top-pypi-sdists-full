import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

@pytest.mark.parametrize("framework", ["react_native", "flutter_bloc", "swiftui"])
def test_mobile_framework_generation(framework):
    """Verify mobile framework tasks are written cleanly and comply with the grading rubric."""
    prompt = f"Implement a complete {framework} mobile component with lists and navigation."
    verify_cli_with_rubric(prompt)
