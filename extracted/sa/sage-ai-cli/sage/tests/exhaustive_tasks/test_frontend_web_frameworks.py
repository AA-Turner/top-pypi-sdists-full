import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

@pytest.mark.parametrize("framework", ["react_tailwind", "vue_pinia", "svelte_kanban"])
def test_frontend_framework_generation(framework):
    """Verify frontend framework tasks are written cleanly and comply with the grading rubric."""
    prompt = f"Implement a complete {framework} application with state management and layouts."
    verify_cli_with_rubric(prompt)
