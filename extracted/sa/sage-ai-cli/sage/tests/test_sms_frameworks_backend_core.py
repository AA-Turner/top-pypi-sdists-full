import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

# Real cloud API calls — integration only.
pytestmark = [
    pytest.mark.timeout(900),
    pytest.mark.integration,
]


@pytest.mark.parametrize("framework", ["fastapi_redis", "express_postgres", "django_rest"])
def test_backend_framework_generation_sms(framework, tmp_path):
    """Verify backend framework service setup via SMS."""
    prompt = f"Implement a complete {framework} backend service with routing and DB persistence."
    verify_sms_with_rubric(prompt, tmp_path)
