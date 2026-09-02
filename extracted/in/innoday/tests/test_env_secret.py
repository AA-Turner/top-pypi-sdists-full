"""The env-file/secret sync tool.

Its whole job is to tell the truth about drift between two stores, so the tests
are about the cases where a sloppier implementation would report agreement it
has not established.
"""

import importlib.util
import json
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location(
    "env_secret", Path(__file__).resolve().parents[1] / "scripts" / "env_secret.py"
)
env_secret = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(env_secret)


@pytest.fixture
def env_file(tmp_path: Path) -> Path:
    path = tmp_path / ".env.dev"
    path.write_text(
        "# A comment worth keeping\n"
        "DATABASE_URL=postgresql://example\n"
        "\n"
        "# Another comment\n"
        "GITHUB_ORG=havilandsoftware\n"
        "EMPTY_ON_PURPOSE=\n"
    )
    return path


def test_reads_keys_and_ignores_comments_and_blanks(env_file: Path):
    values, lines = env_secret.read_env_file(env_file)
    assert values == {
        "DATABASE_URL": "postgresql://example",
        "GITHUB_ORG": "havilandsoftware",
        "EMPTY_ON_PURPOSE": "",
    }
    assert len(lines) == 6


def test_an_empty_value_is_a_key_not_an_absence(env_file: Path):
    """A blank value is a deliberate placeholder -- Google's credentials sit like
    that until someone fills them in. Dropping the key would report it as
    'only in secret' forever."""
    values, _ = env_secret.read_env_file(env_file)
    assert "EMPTY_ON_PURPOSE" in values


def test_a_value_containing_equals_survives(tmp_path: Path):
    # Base64 and connection strings both contain '='. Splitting on every '='
    # instead of the first would silently truncate them.
    path = tmp_path / ".env"
    path.write_text("KEY=abc=def==\n")
    values, _ = env_secret.read_env_file(path)
    assert values["KEY"] == "abc=def=="


def test_diff_reports_every_kind_of_drift(env_file: Path, capsys):
    secret = {
        "DATABASE_URL": "postgresql://example",  # matches
        "GITHUB_ORG": "somewhere-else",  # differs
        "EMPTY_ON_PURPOSE": "",  # matches
        "ONLY_IN_SECRET": "x",  # missing locally
    }
    env, _ = env_secret.read_env_file(env_file)

    assert env_secret.compare(env, secret) == 1  # non-zero: out of step

    out = capsys.readouterr().out
    assert "only in secret   : ONLY_IN_SECRET" in out
    assert "differs          : GITHUB_ORG" in out
    # One extra key and one differing key: two, not three -- the two matching
    # keys are not drift.
    assert "2 keys out of step" in out


def test_diff_never_prints_a_value(env_file: Path, capsys):
    """Its output is meant to be safe in a terminal, a log or a screenshot."""
    env, _ = env_secret.read_env_file(env_file)
    env_secret.compare(env, {"DATABASE_URL": "a-different-secret-value"})

    out = capsys.readouterr().out
    assert "a-different-secret-value" not in out
    assert "postgresql://example" not in out


def test_diff_is_clean_only_when_both_sides_match(env_file: Path, capsys):
    env, _ = env_secret.read_env_file(env_file)
    assert env_secret.compare(env, dict(env)) == 0
    assert "in step" in capsys.readouterr().out


def test_pull_updates_in_place_and_keeps_comments(env_file: Path):
    _, lines = env_secret.read_env_file(env_file)
    env_secret.apply_to_env_file(
        env_file, lines, {"GITHUB_ORG": "changed", "BRAND_NEW": "value"}
    )

    text = env_file.read_text()
    assert "# A comment worth keeping" in text
    assert "GITHUB_ORG=changed" in text
    assert "BRAND_NEW=value" in text
    # An untouched key keeps its value rather than being dropped.
    assert "DATABASE_URL=postgresql://example" in text


def test_pull_then_diff_is_clean(env_file: Path):
    secret = {
        "DATABASE_URL": "new",
        "GITHUB_ORG": "new",
        "EMPTY_ON_PURPOSE": "",
        "EXTRA": "1",
    }
    _, lines = env_secret.read_env_file(env_file)
    env_secret.apply_to_env_file(env_file, lines, secret)

    env, _ = env_secret.read_env_file(env_file)
    assert env_secret.compare(env, secret) == 0


def test_a_missing_env_file_fails_loudly(tmp_path: Path):
    with pytest.raises(SystemExit):
        env_secret.read_env_file(tmp_path / "nope")


def test_non_string_secret_values_are_coerced(monkeypatch):
    """Secrets Manager holds JSON, so a port could arrive as a number. Written
    into an env file as a Python repr it would be a silent corruption."""

    class Result:
        returncode = 0
        stdout = json.dumps({"PORT": 587, "TLS": True})
        stderr = ""

    monkeypatch.setattr(env_secret.subprocess, "run", lambda *a, **k: Result())
    assert env_secret.read_secret("x", "y", "z") == {"PORT": "587", "TLS": "True"}
