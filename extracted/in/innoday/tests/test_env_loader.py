"""Tests for src/env_loader.py -- `load_env()` and `get_environment()`."""

import pytest

from src.env_loader import EnvironmentNotSetError, get_environment, load_env


@pytest.fixture
def isolated_env(monkeypatch):
    """Remove ENVIRONMENT so each test controls it explicitly."""
    monkeypatch.delenv("ENVIRONMENT", raising=False)


def test_unset_with_no_local_env_file_raises(tmp_path, isolated_env):
    with pytest.raises(
        EnvironmentNotSetError, match="Cannot start with ambiguous environment"
    ):
        load_env(root=tmp_path)


def test_unset_with_local_env_file_warns_and_loads(tmp_path, isolated_env, capsys):
    (tmp_path / ".env.local").write_text("FROM_LOCAL_FILE=yes\n")

    result = load_env(root=tmp_path)

    assert result == str(tmp_path / ".env.local")
    captured = capsys.readouterr()
    assert "defaulting to 'local'" in captured.err


def test_environment_production_does_not_raise_and_loads_nothing(
    tmp_path, monkeypatch, isolated_env
):
    monkeypatch.setenv("ENVIRONMENT", "production")

    result = load_env(root=tmp_path)

    assert result == "(none — environment variables injected by platform)"


def test_environment_invalid_value_raises(tmp_path, monkeypatch, isolated_env):
    monkeypatch.setenv("ENVIRONMENT", "prod")

    with pytest.raises(EnvironmentNotSetError, match="got 'prod'"):
        load_env(root=tmp_path)


def test_environment_dev_loads_env_dev_file(tmp_path, monkeypatch, isolated_env):
    monkeypatch.setenv("ENVIRONMENT", "dev")
    (tmp_path / ".env.dev").write_text("FROM_DEV_FILE=yes\n")

    result = load_env(root=tmp_path)

    assert result == str(tmp_path / ".env.dev")


class TestGetEnvironment:
    """`get_environment()` -- the read side of ENVIRONMENT, and the one resolver
    behind both /health and /api/v1/public/status (#619)."""

    def test_returns_the_configured_environment(self, monkeypatch, isolated_env):
        monkeypatch.setenv("ENVIRONMENT", "dev")

        assert get_environment() == "dev"

    def test_defaults_to_production_when_unset(self, isolated_env):
        assert get_environment() == "production"

    def test_blank_is_treated_as_unset(self, monkeypatch, isolated_env):
        monkeypatch.setenv("ENVIRONMENT", "   ")

        assert get_environment() == "production"

    def test_does_not_validate(self, monkeypatch, isolated_env):
        """`load_env` rejects an unknown value; this must not. It reports on a
        running process, so it can never be the thing that fails a request --
        and reporting a wrong-looking value beats reporting a wrong one.
        """
        monkeypatch.setenv("ENVIRONMENT", "staging")

        assert get_environment() == "staging"

    def test_ignores_debug(self, monkeypatch, isolated_env):
        """DEBUG is a different question. Answering it under the name
        `environment` is the whole of the /health bug."""
        monkeypatch.setenv("ENVIRONMENT", "dev")
        monkeypatch.setenv("DEBUG", "True")

        assert get_environment() == "dev"


def test_no_router_resolves_the_environment_for_itself():
    """One resolver, enforced. #619 was three endpoints answering "which
    environment is this?" from three local `os.getenv` calls with two different
    defaults (and, in /health's case, from DEBUG instead) -- so they disagreed
    with each other in the same process. Reading ENVIRONMENT to *report* it
    belongs in `get_environment()`; nothing under src/api or src/routers should
    read the variable directly again.
    """
    import re
    from pathlib import Path

    src = Path(__file__).resolve().parent.parent / "src"
    pattern = re.compile(r"""(getenv|environ(\.get)?)\(\s*["']ENVIRONMENT["']""")
    offenders = [
        f"{path.relative_to(src.parent)}:{lineno}"
        for directory in ("api", "routers")
        for path in sorted((src / directory).rglob("*.py"))
        for lineno, line in enumerate(path.read_text().splitlines(), start=1)
        if pattern.search(line)
    ]

    assert not offenders, (
        "read ENVIRONMENT through src.env_loader.get_environment() instead: "
        f"{offenders}"
    )
