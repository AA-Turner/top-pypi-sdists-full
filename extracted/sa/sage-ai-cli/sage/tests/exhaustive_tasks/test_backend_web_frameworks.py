import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

@pytest.mark.parametrize("framework", ["fastapi_redis", "express_postgres", "django_rest"])
def test_backend_framework_generation(framework):
    """Verify backend framework tasks are written cleanly and comply with the grading rubric."""
    prompt = f"Implement a complete {framework} backend service with routing and DB persistence."
    verify_cli_with_rubric(prompt)


@pytest.mark.parametrize("framework", ["fastapi_redis", "express_postgres", "django_rest"])
def test_backend_framework_generation_sms(framework, tmp_path):
    """Verify backend framework tasks via SMS bridge."""
    prompt = f"Implement a complete {framework} backend service with routing and DB persistence."
    verify_sms_with_rubric(prompt, tmp_path)


@pytest.mark.parametrize("framework", ["fastapi_redis", "express_postgres", "django_rest"])
def test_backend_framework_generation_website(framework):
    """Verify backend framework tasks via website backend."""
    prompt = f"Implement a complete {framework} backend service with routing and DB persistence."
    verify_website_with_rubric(prompt)
