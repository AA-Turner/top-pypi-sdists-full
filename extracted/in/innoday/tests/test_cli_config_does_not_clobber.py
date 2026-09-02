"""A config file that cannot be READ must never be overwritten by a WRITE.

`CLIConfig._load_raw` falls back to `DEFAULT_CONFIG` when the file exists but
cannot be parsed. That is the right answer for reading -- the command can still
run. It was the wrong answer for writing: `save()` then wrote those defaults
back over the whole file, and `~/.innoday/config.json` holds *every* profile,
each with its api_url, identity and org list.

So a single unreadable read turned the very next `innoday config set <one key>`
into total data loss. That is not hypothetical -- it destroyed a working `dev`
profile, and the 401s that followed read as an auth problem rather than as the
data loss they actually were. The only signal was a yellow warning, which
disappears the moment output is redirected.

A *missing* file is a different case and must still save normally: that is a
legitimate first run, and defaults are correct.
"""

import json

import pytest

from src.cli.config import CLIConfig


def _write(path, payload):
    path.write_text(payload)
    return path


@pytest.fixture
def config_path(tmp_path):
    return tmp_path / "config.json"


def _two_profile_config():
    return {
        "current_profile": "dev",
        "profiles": {
            # NOT one of _STALE_DEFAULT_API_URLS -- those are deliberately
            # migrated on load, which would confuse "was it left alone?".
            "default": {"platform": {"api_url": "http://localhost:9999"}},
            "dev": {
                "platform": {"api_url": "https://innoday-dev.example"},
                "user": {"id": "u-1", "email": "someone@example.com"},
            },
        },
    }


class TestAnUnreadableConfigIsNotOverwritten:
    def test_save_refuses_when_the_file_could_not_be_parsed(self, config_path):
        original = "{ this is not json"
        _write(config_path, original)

        cfg = CLIConfig(config_path=str(config_path))

        with pytest.raises(RuntimeError, match="Refusing to overwrite"):
            cfg.save()

        # The unreadable file is still byte-for-byte intact -- the whole point.
        assert config_path.read_text() == original

    def test_a_real_profile_survives_a_set_on_a_corrupt_file(self, config_path):
        # The exact shape of the incident: a file holding several profiles that
        # has become unparseable, followed by a command that sets one key.
        corrupt = json.dumps(_two_profile_config())[:-20]  # truncated mid-object
        _write(config_path, corrupt)

        cfg = CLIConfig(config_path=str(config_path))
        cfg.set_team_secret("a-secret")

        with pytest.raises(RuntimeError):
            cfg.save()
        assert config_path.read_text() == corrupt

    def test_reading_still_degrades_gracefully(self, config_path):
        """The fallback itself is kept -- only the write is blocked."""
        _write(config_path, "{ not json")
        cfg = CLIConfig(config_path=str(config_path))
        # Usable defaults, no exception on construction.
        assert cfg.get_current_profile() == "default"


class TestNormalWritesAreUnaffected:
    def test_a_missing_file_still_saves(self, config_path):
        """First run: no file is not a degraded read."""
        assert not config_path.exists()

        cfg = CLIConfig(config_path=str(config_path))
        cfg.set_team_secret("first-run")
        cfg.save()

        assert json.loads(config_path.read_text())["profiles"]

    def test_a_readable_file_still_saves_and_keeps_other_profiles(self, config_path):
        _write(config_path, json.dumps(_two_profile_config()))

        cfg = CLIConfig(config_path=str(config_path))
        cfg.set_team_secret("rotated")
        cfg.save()

        written = json.loads(config_path.read_text())
        # Both profiles survive, and the one not being edited is untouched.
        assert set(written["profiles"]) == {"default", "dev"}
        assert (
            written["profiles"]["default"]["platform"]["api_url"]
            == "http://localhost:9999"
        )
