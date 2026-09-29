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


def _backups(config_path):
    """Set-aside copies live in <dir>/archive/ (PF-467), not beside the config."""
    return sorted((config_path.parent / "archive").glob(config_path.name + ".*"))


class TestAnUnreadableConfigIsNotOverwritten:
    """The unreadable file is never destroyed -- it is set aside intact, and
    the CLI carries on (PF-466). It used to be kept by refusing every save,
    which left login, upgrade and init all failing until someone hand-edited
    the JSON."""

    def test_the_unreadable_file_is_set_aside_byte_for_byte(self, config_path):
        original = "{ this is not json"
        _write(config_path, original)

        CLIConfig(config_path=str(config_path))

        [backup] = _backups(config_path)
        assert backup.read_text() == original
        assert not config_path.exists()

    def test_a_real_profile_survives_a_set_on_a_corrupt_file(self, config_path):
        # The exact shape of the incident: a file holding several profiles that
        # has become unparseable, followed by a command that sets one key.
        corrupt = json.dumps(_two_profile_config())[:-20]  # truncated mid-object
        _write(config_path, corrupt)

        cfg = CLIConfig(config_path=str(config_path))
        cfg.set_team_secret("a-secret")
        cfg.save()  # no longer refused: the original is safe in the backup

        [backup] = _backups(config_path)
        assert backup.read_text() == corrupt
        assert json.loads(config_path.read_text())["profiles"]

    def test_a_second_bad_file_does_not_overwrite_the_first_backup(self, config_path):
        _write(config_path, "{ first")
        CLIConfig(config_path=str(config_path))
        _write(config_path, "{ second")
        CLIConfig(config_path=str(config_path))

        assert sorted(b.read_text() for b in _backups(config_path)) == [
            "{ first",
            "{ second",
        ]

    def test_if_it_cannot_be_moved_saving_is_still_refused(
        self, config_path, monkeypatch
    ):
        """The old guarantee stays as the fallback."""
        from pathlib import Path

        original = "{ not json"
        _write(config_path, original)

        def no_move(self, target):
            raise PermissionError("read-only")

        monkeypatch.setattr(Path, "rename", no_move)
        cfg = CLIConfig(config_path=str(config_path))
        with pytest.raises(RuntimeError, match="Refusing to overwrite"):
            cfg.save()
        assert config_path.read_text() == original

    def test_reading_still_degrades_gracefully(self, config_path):
        _write(config_path, "{ not json")
        cfg = CLIConfig(config_path=str(config_path))
        assert cfg.get_current_profile() == "default"


class TestSavesAreAtomic:
    def test_a_save_never_leaves_a_half_written_file(self, config_path, monkeypatch):
        """Another innoday process (the MCP server, a second terminal) reading
        mid-save used to see a truncated file -- the same 'Expecting ,' error."""
        import json as _json

        _write(config_path, _json.dumps(_two_profile_config()))
        cfg = CLIConfig(config_path=str(config_path))
        cfg.set_team_secret("x")

        real_dump = _json.dump

        def dump_then_fail(obj, f, **kw):
            f.write('{"half": ')
            raise OSError("disk full")

        monkeypatch.setattr("src.cli.config.json.dump", dump_then_fail)
        with pytest.raises(Exception):
            cfg.save()
        monkeypatch.setattr("src.cli.config.json.dump", real_dump)

        # The file on disk is still the complete old one.
        assert _json.loads(config_path.read_text())["current_profile"] == "dev"


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


class TestTheFreshFileIsPrivate:
    def test_a_config_rebuilt_after_set_aside_is_owner_only(self, config_path):
        """It can hold the team secret; the rebuilt file was world-readable."""
        _write(config_path, "{ not json")
        config_path.chmod(0o600)
        cfg = CLIConfig(config_path=str(config_path))
        cfg.set_team_secret("s")
        cfg.save()
        assert config_path.stat().st_mode & 0o777 == 0o600

    def test_a_file_that_becomes_valid_is_not_set_aside(self, config_path, monkeypatch):
        """An older CLI writing in place can be caught mid-write: re-read once."""
        import src.cli.config as mod

        _write(config_path, "{ half")

        def finish_writing(_path, _seen):
            _write(config_path, json.dumps(_two_profile_config()))
            return False

        monkeypatch.setattr(mod, "_still_unparseable", finish_writing)
        cfg = CLIConfig(config_path=str(config_path))
        assert cfg.get_current_profile() == "dev"
        assert not _backups(config_path)


class TestTheArchiveIsTidy:
    def test_nothing_is_left_beside_the_config(self, config_path):
        _write(config_path, "{ not json")
        CLIConfig(config_path=str(config_path))
        assert sorted(p.name for p in config_path.parent.iterdir()) == ["archive"]

    def test_the_archived_copy_is_owner_only(self, config_path):
        _write(config_path, "{ not json")
        config_path.chmod(0o644)
        CLIConfig(config_path=str(config_path))
        [backup] = _backups(config_path)
        assert backup.stat().st_mode & 0o777 == 0o600

    def test_copies_older_than_30_days_are_pruned(self, config_path):
        archive = config_path.parent / "archive"
        archive.mkdir()
        old = archive / "config.json.20200101-000000"
        recent_name = "config.json." + __import__("datetime").datetime.now(
            __import__("datetime").timezone.utc
        ).strftime("%Y%m%d-%H%M%S")
        old.write_text("old")
        (archive / recent_name).write_text("recent")
        _write(config_path, json.dumps(_two_profile_config()))

        CLIConfig(config_path=str(config_path))

        assert not old.exists()
        assert (archive / recent_name).exists()

    def test_copies_left_beside_it_by_0_1_372_are_swept_in(self, config_path):
        """PF-466 wrote config.json.broken-<time> next to the config."""
        stray = config_path.parent / "config.json.broken-20260928-090605"
        stray.write_text("{ old broken")
        _write(config_path, json.dumps(_two_profile_config()))

        CLIConfig(config_path=str(config_path))

        assert not stray.exists()
        [moved] = _backups(config_path)
        assert moved.read_text() == "{ old broken"
