import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

@pytest.mark.parametrize("framework", ["react_tailwind", "vue_pinia", "svelte_kanban"])
def test_frontend_framework_generation(framework):
    """Verify frontend framework tasks are written cleanly and comply with the grading rubric."""
    prompt = f"Implement a complete {framework} application with state management and layouts."
    verify_cli_with_rubric(prompt)


@pytest.mark.parametrize("framework", ["react_tailwind", "vue_pinia", "svelte_kanban"])
def test_frontend_framework_generation_sms(framework, tmp_path):
    """Verify frontend framework tasks via SMS bridge."""
    prompt = f"Implement a complete {framework} application with state management and layouts."
    verify_sms_with_rubric(prompt, tmp_path)


@pytest.mark.parametrize("framework", ["react_tailwind", "vue_pinia", "svelte_kanban"])
def test_frontend_framework_generation_website(framework):
    """Verify frontend framework tasks via website backend."""
    prompt = f"Implement a complete {framework} application with state management and layouts."
    verify_website_with_rubric(prompt)
