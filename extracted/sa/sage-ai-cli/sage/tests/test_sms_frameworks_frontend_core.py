import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

@pytest.mark.parametrize("framework", ["react_tailwind", "vue_pinia", "svelte_kanban"])
def test_frontend_framework_generation_sms(framework, tmp_path):
    """Verify frontend framework application setup via SMS."""
    prompt = f"Implement a complete {framework} application with state management and layouts."
    verify_sms_with_rubric(prompt, tmp_path)
