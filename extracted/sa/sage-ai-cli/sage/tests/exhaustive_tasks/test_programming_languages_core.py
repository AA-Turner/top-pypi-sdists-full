import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

@pytest.mark.parametrize("lang_spec", ["python_pandas", "go_concurrency", "rust_tokio"])
def test_core_language_generation(lang_spec):
    """Verify core language tasks are written cleanly and comply with the grading rubric."""
    prompt = f"Implement a complete, production-ready {lang_spec} module for concurrency or data management."
    verify_cli_with_rubric(prompt)


@pytest.mark.parametrize("lang_spec", ["python_pandas", "go_concurrency", "rust_tokio"])
def test_core_language_generation_sms(lang_spec, tmp_path):
    """Verify core language tasks via SMS bridge."""
    prompt = f"Implement a complete, production-ready {lang_spec} module for concurrency or data management."
    verify_sms_with_rubric(prompt, tmp_path)


@pytest.mark.parametrize("lang_spec", ["python_pandas", "go_concurrency", "rust_tokio"])
def test_core_language_generation_website(lang_spec):
    """Verify core language tasks via website backend."""
    prompt = f"Implement a complete, production-ready {lang_spec} module for concurrency or data management."
    verify_website_with_rubric(prompt)
