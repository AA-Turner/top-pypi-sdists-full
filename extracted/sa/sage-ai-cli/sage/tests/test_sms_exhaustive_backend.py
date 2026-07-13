import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

# Real cloud API calls — integration only.
pytestmark = [
    pytest.mark.timeout(900),
    pytest.mark.integration,
]


def test_sms_exhaustive_backend(tmp_path):
    """Verify exhaustive FastAPI backend with PostgreSQL and Redis caching via SMS."""
    prompt = "Create a FastAPI backend with PostgreSQL and Redis caching."
    verify_sms_with_rubric(prompt, tmp_path)
