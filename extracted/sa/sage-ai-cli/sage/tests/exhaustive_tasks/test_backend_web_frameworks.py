import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

@pytest.mark.parametrize("framework", ["fastapi_redis", "express_postgres", "django_rest"])
def test_backend_framework_generation(framework):
    """Verify backend framework tasks are written cleanly and comply with the grading rubric."""
    prompt = f"Implement a complete {framework} backend service with routing and DB persistence."
    verify_cli_with_rubric(prompt)
