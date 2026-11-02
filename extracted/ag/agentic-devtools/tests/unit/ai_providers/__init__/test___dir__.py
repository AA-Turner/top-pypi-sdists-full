import agentic_devtools.ai_providers as ai_providers


def test_dir_includes_exports_and_module_globals() -> None:
    names = dir(ai_providers)

    assert "AIProvider" in names
    assert "DEFAULT_MODEL_MATRIX" in names
