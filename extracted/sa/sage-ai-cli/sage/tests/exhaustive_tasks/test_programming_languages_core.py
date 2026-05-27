import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

@pytest.mark.parametrize("lang_spec", ["python_pandas", "go_concurrency", "rust_tokio"])
def test_core_language_generation(lang_spec):
    """Verify core language tasks are written cleanly and comply with the grading rubric."""
    prompt = f"Implement a complete, production-ready {lang_spec} module for concurrency or data management."
    verify_cli_with_rubric(prompt)
