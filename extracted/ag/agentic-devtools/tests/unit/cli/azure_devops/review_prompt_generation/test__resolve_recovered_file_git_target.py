"""Tests for _resolve_recovered_file_git_target."""

from agentic_devtools.cli.azure_devops.review_prompt_generation import _resolve_recovered_file_git_target


def test_uses_both_paths_for_a_renamed_file() -> None:
    target, original_path = _resolve_recovered_file_git_target(
        "/src/new.py",
        "src/new.py",
        "rename",
        {"src/new.py": "/src/old.py"},
    )

    assert target == ["src/old.py", "src/new.py"]
    assert original_path == "/src/old.py"
