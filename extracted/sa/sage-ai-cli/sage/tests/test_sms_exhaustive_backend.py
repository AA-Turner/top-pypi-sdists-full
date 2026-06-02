import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_exhaustive_backend(tmp_path):
    """Verify exhaustive FastAPI backend with PostgreSQL and Redis caching via SMS."""
    prompt = "Create a FastAPI backend with PostgreSQL and Redis caching."
    verify_sms_with_rubric(prompt, tmp_path)
