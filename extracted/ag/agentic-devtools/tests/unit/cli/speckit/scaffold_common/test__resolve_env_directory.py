"""Tests for ``_resolve_env_directory``."""

from pathlib import Path

from agentic_devtools.cli.speckit.scaffold_common import _resolve_env_directory


class TestResolveEnvDirectory:
    """_resolve_env_directory maps the SPECIFY_FEATURE_DIRECTORY env value to a path."""

    def test_bare_name_resolves_under_specs_dir(self) -> None:
        specs_dir = Path("/repo/specs")
        result = _resolve_env_directory(specs_dir, Path("/repo"), "042-my-feature")

        assert result == specs_dir / "042-my-feature"

    def test_relative_path_with_separator_resolves_under_repo_root(self) -> None:
        specs_dir = Path("/repo/specs")
        result = _resolve_env_directory(specs_dir, Path("/repo"), "custom/042-my-feature")

        assert result == Path("/repo/custom/042-my-feature")

    def test_absolute_path_used_as_is(self) -> None:
        specs_dir = Path("/repo/specs")
        absolute = Path.cwd() / "abs" / "042-my-feature"
        result = _resolve_env_directory(specs_dir, Path("/repo"), str(absolute))

        assert result == absolute
