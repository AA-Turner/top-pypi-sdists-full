"""Tests for get_checkpointer factory function."""

import sqlite3
from pathlib import Path
from unittest.mock import patch

import pytest
from langgraph.checkpoint.sqlite import SqliteSaver

from agentic_devtools.orchestration.checkpointing import get_checkpointer


class TestGetCheckpointer:
    """Tests for get_checkpointer()."""

    def test_returns_sqlite_saver_instance(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        saver = get_checkpointer(db_path)
        try:
            assert isinstance(saver, SqliteSaver)
        finally:
            saver.conn.close()

    def test_creates_sqlite_file(self, tmp_path):
        db_path = tmp_path / "test.db"
        saver = get_checkpointer(str(db_path))
        try:
            assert db_path.exists()
        finally:
            saver.conn.close()

    def test_creates_parent_directories(self, tmp_path):
        db_path = tmp_path / "nested" / "dir" / "test.db"
        saver = get_checkpointer(str(db_path))
        try:
            assert db_path.parent.exists()
            assert db_path.exists()
        finally:
            saver.conn.close()

    def test_default_path_uses_get_state_dir(self, tmp_path):
        """Default path resolves via get_state_dir() for worktree-scoped isolation."""
        fake_state_dir = tmp_path / "workflows" / "test" / "worktree"
        fake_state_dir.mkdir(parents=True)
        with patch(
            "agentic_devtools.state.get_state_dir",
            return_value=fake_state_dir,
        ):
            saver = get_checkpointer()
        try:
            expected = fake_state_dir / "orchestration.db"
            assert expected.exists()
        finally:
            saver.conn.close()

    def test_rejects_both_db_path_and_state_dir(self, tmp_path):
        """Supplying both db_path and state_dir is an invalid public API combination."""
        with pytest.raises(ValueError, match="only one of db_path or state_dir"):
            get_checkpointer(
                str(tmp_path / "explicit.db"),
                state_dir=tmp_path / "scoped",
            )

    def test_default_path_rejects_unscoped_fallback(self, tmp_path):
        """Direct default-path calls fail closed on the canonical _unscoped fallback."""
        repo_root = tmp_path
        unscoped_dir = repo_root / ".agdt" / "workflows" / "_unscoped"
        with (
            patch("agentic_devtools.state.get_state_dir", return_value=unscoped_dir),
            patch("agentic_devtools.state.get_repo_root", return_value=repo_root),
        ):
            with pytest.raises(ValueError, match="unscoped fallback path"):
                get_checkpointer()

    def test_state_dir_rejects_agdt_temp_fallback_when_not_in_repo(self, tmp_path, monkeypatch):
        """The non-repo .agdt-temp fallback is rejected for workflow-managed calls."""
        monkeypatch.chdir(tmp_path)
        fallback_dir = tmp_path / ".agdt-temp"
        with patch("agentic_devtools.state.get_repo_root", return_value=None):
            with pytest.raises(ValueError, match="unscoped fallback path"):
                get_checkpointer(state_dir=fallback_dir, worktree_key="FEATURE-42")

    def test_state_dir_rejects_canonical_worktree_mismatch(self, tmp_path):
        """Canonical workflow paths must agree with the active worktree key."""
        repo_root = tmp_path
        mismatched_state_dir = repo_root / ".agdt" / "workflows" / "tester" / "WORKTREE-A"
        mismatched_state_dir.mkdir(parents=True)
        with patch("agentic_devtools.state.get_repo_root", return_value=repo_root):
            with pytest.raises(ValueError, match="active worktree key is 'WORKTREE-B'"):
                get_checkpointer(
                    state_dir=mismatched_state_dir,
                    worktree_key="WORKTREE-B",
                )

    def test_state_dir_allows_noncanonical_workflows_subtree(self, tmp_path):
        """Validated pin paths nested below workflows/ stay caller-authoritative."""
        repo_root = tmp_path
        nested_state_dir = repo_root / ".agdt" / "workflows" / "tester" / "WORKTREE-A" / "nested"
        nested_state_dir.mkdir(parents=True)
        with patch("agentic_devtools.state.get_repo_root", return_value=repo_root):
            saver = get_checkpointer(
                state_dir=nested_state_dir,
                worktree_key="WORKTREE-B",
            )
        try:
            actual = saver.conn.execute("PRAGMA database_list").fetchone()[2]
            assert Path(actual) == nested_state_dir / "orchestration.db"
        finally:
            saver.conn.close()

    def test_state_dir_legacy_root_alias_redirects_and_warns(self, tmp_path, capsys):
        """Workflow-managed legacy-root aliases warn and redirect to canonical scoped storage."""
        repo_root = tmp_path
        legacy_dir = repo_root / ".agdt"
        legacy_dir.mkdir(parents=True)
        legacy_path = legacy_dir / "orchestration.db"
        with sqlite3.connect(legacy_path) as conn:
            conn.execute("CREATE TABLE checkpoints (id INTEGER PRIMARY KEY)")

        with (
            patch("agentic_devtools.state.get_repo_root", return_value=repo_root),
            patch("agentic_devtools.state._get_or_refresh_identity", return_value="tester"),
        ):
            saver = get_checkpointer(
                state_dir=legacy_dir,
                worktree_key="FEATURE-42",
            )
        try:
            redirected = repo_root / ".agdt" / "workflows" / "tester" / "FEATURE-42" / "orchestration.db"
            actual = saver.conn.execute("PRAGMA database_list").fetchone()[2]
            assert Path(actual) == redirected
            assert legacy_path.exists()
        finally:
            saver.conn.close()

        warning = capsys.readouterr().err
        assert f"'{legacy_path}'" in warning
        assert f"'{redirected}'" in warning
        assert "No automatic migration is performed" in warning

    def test_state_dir_legacy_root_alias_warns_when_legacy_db_is_inaccessible(self, tmp_path, capsys):
        """Unreadable legacy files are ignored with the degraded warning path."""
        repo_root = tmp_path
        legacy_dir = repo_root / ".agdt"
        legacy_dir.mkdir(parents=True)
        legacy_path = legacy_dir / "orchestration.db"
        legacy_path.write_text("not sqlite", encoding="utf-8")

        with (
            patch("agentic_devtools.state.get_repo_root", return_value=repo_root),
            patch("agentic_devtools.state._get_or_refresh_identity", return_value="tester"),
        ):
            saver = get_checkpointer(
                state_dir=legacy_dir,
                worktree_key="FEATURE-99",
            )
        try:
            redirected = repo_root / ".agdt" / "workflows" / "tester" / "FEATURE-99" / "orchestration.db"
            actual = saver.conn.execute("PRAGMA database_list").fetchone()[2]
            assert Path(actual) == redirected
        finally:
            saver.conn.close()

        warning = capsys.readouterr().err
        assert "is inaccessible" in warning
        assert "not a valid SQLite database" in warning

    def test_state_dir_canonical_scope_warns_about_legacy_db(self, tmp_path, capsys):
        """Canonical workflow-managed scoped databases still probe legacy root and warn."""
        repo_root = tmp_path
        legacy_dir = repo_root / ".agdt"
        legacy_dir.mkdir(parents=True)
        with sqlite3.connect(legacy_dir / "orchestration.db") as conn:
            conn.execute("CREATE TABLE checkpoints (id INTEGER PRIMARY KEY)")

        scoped_dir = repo_root / ".agdt" / "workflows" / "tester" / "FEATURE-42"
        with patch("agentic_devtools.state.get_repo_root", return_value=repo_root):
            saver = get_checkpointer(state_dir=scoped_dir, worktree_key="FEATURE-42")
        try:
            assert (scoped_dir / "orchestration.db").exists()
            actual = saver.conn.execute("PRAGMA database_list").fetchone()[2]
            assert Path(actual) == scoped_dir / "orchestration.db"
        finally:
            saver.conn.close()

        warning = capsys.readouterr().err
        assert f"'{legacy_dir / 'orchestration.db'}'" in warning
        assert f"'{scoped_dir / 'orchestration.db'}'" in warning
        assert "No automatic migration is performed" in warning

    def test_state_dir_noncanonical_scope_does_not_warn_about_legacy_db(self, tmp_path, capsys):
        """Non-canonical overrides do not emit legacy-root warnings."""
        repo_root = tmp_path
        legacy_dir = repo_root / ".agdt"
        legacy_dir.mkdir(parents=True)
        with sqlite3.connect(legacy_dir / "orchestration.db") as conn:
            conn.execute("CREATE TABLE checkpoints (id INTEGER PRIMARY KEY)")

        override_scope = repo_root / ".agdt" / "workflows" / "tester" / "FEATURE-42" / "nested"
        with patch("agentic_devtools.state.get_repo_root", return_value=repo_root):
            saver = get_checkpointer(state_dir=override_scope, worktree_key="FEATURE-42")
        try:
            assert (override_scope / "orchestration.db").exists()
            actual = saver.conn.execute("PRAGMA database_list").fetchone()[2]
            assert Path(actual) == override_scope / "orchestration.db"
        finally:
            saver.conn.close()

        assert capsys.readouterr().err == ""

    def test_state_dir_legacy_root_alias_uses_bootstrap_worktree_key_when_not_passed(self, tmp_path):
        """Legacy redirect falls back to bootstrap scope when worktree_key is omitted."""
        repo_root = tmp_path
        legacy_dir = repo_root / ".agdt"
        legacy_dir.mkdir(parents=True)

        with (
            patch("agentic_devtools.state.get_repo_root", return_value=repo_root),
            patch("agentic_devtools.state._get_or_refresh_identity", return_value="tester"),
            patch("agentic_devtools.state.get_bootstrap_state", return_value={"worktree_key": "BOOTSTRAP-42"}),
        ):
            saver = get_checkpointer(state_dir=legacy_dir)
        try:
            actual = saver.conn.execute("PRAGMA database_list").fetchone()[2]
            expected = repo_root / ".agdt" / "workflows" / "tester" / "BOOTSTRAP-42" / "orchestration.db"
            assert Path(actual) == expected
        finally:
            saver.conn.close()

    def test_state_dir_legacy_root_alias_requires_valid_worktree_key(self, tmp_path):
        """Legacy redirect fails closed when no valid worktree key can be recovered."""
        repo_root = tmp_path
        legacy_dir = repo_root / ".agdt"
        legacy_dir.mkdir(parents=True)

        with (
            patch("agentic_devtools.state.get_repo_root", return_value=repo_root),
            patch("agentic_devtools.state.get_bootstrap_state", return_value={}),
        ):
            with pytest.raises(ValueError, match="requires a valid worktree key"):
                get_checkpointer(state_dir=legacy_dir)

    def test_state_dir_legacy_root_alias_requires_valid_identity(self, tmp_path):
        """Legacy redirect fails closed when identity resolution is unsafe."""
        repo_root = tmp_path
        legacy_dir = repo_root / ".agdt"
        legacy_dir.mkdir(parents=True)

        with (
            patch("agentic_devtools.state.get_repo_root", return_value=repo_root),
            patch("agentic_devtools.state._get_or_refresh_identity", return_value="bad/name"),
        ):
            with pytest.raises(ValueError, match="requires a valid scoped identity"):
                get_checkpointer(
                    state_dir=legacy_dir,
                    worktree_key="FEATURE-42",
                )

    def test_state_dir_legacy_root_alias_fails_closed_when_redirect_still_aliases_legacy_db(self, tmp_path):
        """Legacy redirect fails closed when canonical target resolves back to legacy DB."""
        repo_root = tmp_path
        legacy_dir = repo_root / ".agdt"
        legacy_dir.mkdir(parents=True)
        legacy_db = legacy_dir / "orchestration.db"
        legacy_db.touch()
        canonical_dir = repo_root / ".agdt" / "workflows" / "tester" / "FEATURE-42"
        canonical_dir.parent.mkdir(parents=True, exist_ok=True)
        canonical_dir.symlink_to(legacy_dir, target_is_directory=True)

        with (
            patch("agentic_devtools.state.get_repo_root", return_value=repo_root),
            patch("agentic_devtools.state._get_or_refresh_identity", return_value="tester"),
        ):
            with pytest.raises(ValueError, match="resolved back to the legacy repository-root database path"):
                get_checkpointer(
                    state_dir=legacy_dir,
                    worktree_key="FEATURE-42",
                )

    def test_state_dir_legacy_root_alias_warns_when_probe_raises_oserror(self, tmp_path, capsys):
        """Probe OS errors use the degraded warning path and still open the scoped database."""
        repo_root = tmp_path
        legacy_dir = repo_root / ".agdt"
        legacy_dir.mkdir(parents=True)
        (legacy_dir / "orchestration.db").write_text("placeholder", encoding="utf-8")
        real_connect = sqlite3.connect

        def _connect(*args, **kwargs):
            if kwargs.get("uri") is True:
                raise OSError("permission denied")
            return real_connect(*args, **kwargs)

        with (
            patch("agentic_devtools.state.get_repo_root", return_value=repo_root),
            patch("agentic_devtools.state._get_or_refresh_identity", return_value="tester"),
            patch("agentic_devtools.orchestration.checkpointing.sqlite3.connect", side_effect=_connect),
        ):
            saver = get_checkpointer(
                state_dir=legacy_dir,
                worktree_key="FEATURE-77",
            )
        try:
            actual = saver.conn.execute("PRAGMA database_list").fetchone()[2]
            expected = repo_root / ".agdt" / "workflows" / "tester" / "FEATURE-77" / "orchestration.db"
            assert Path(actual) == expected
        finally:
            saver.conn.close()

        assert "permission denied" in capsys.readouterr().err.lower()

    def test_state_dir_legacy_root_alias_warns_when_legacy_db_stat_fails(self, tmp_path, capsys):
        """Stat failures are treated as inaccessible legacy DB and still use scoped storage."""
        repo_root = tmp_path
        legacy_dir = repo_root / ".agdt"
        legacy_dir.mkdir(parents=True)
        legacy_path = legacy_dir / "orchestration.db"
        legacy_path.write_text("placeholder", encoding="utf-8")
        real_stat = Path.stat

        def _stat(path_obj, *args, **kwargs):
            if path_obj == legacy_path:
                raise PermissionError("permission denied")
            return real_stat(path_obj, *args, **kwargs)

        with (
            patch("agentic_devtools.state.get_repo_root", return_value=repo_root),
            patch("agentic_devtools.state._get_or_refresh_identity", return_value="tester"),
            patch("pathlib.Path.stat", autospec=True, side_effect=_stat),
        ):
            saver = get_checkpointer(
                state_dir=legacy_dir,
                worktree_key="FEATURE-79",
            )
        try:
            actual = saver.conn.execute("PRAGMA database_list").fetchone()[2]
            expected = repo_root / ".agdt" / "workflows" / "tester" / "FEATURE-79" / "orchestration.db"
            assert Path(actual) == expected
        finally:
            saver.conn.close()

        assert "permission denied" in capsys.readouterr().err

    def test_state_dir_legacy_root_alias_warns_when_probe_raises_generic_database_error(self, tmp_path, capsys):
        """Unexpected SQLite probe errors use the degraded warning path."""
        repo_root = tmp_path
        legacy_dir = repo_root / ".agdt"
        legacy_dir.mkdir(parents=True)
        (legacy_dir / "orchestration.db").write_text("placeholder", encoding="utf-8")
        real_connect = sqlite3.connect

        def _connect(*args, **kwargs):
            if kwargs.get("uri") is True:
                raise sqlite3.DatabaseError("probe failed")
            return real_connect(*args, **kwargs)

        with (
            patch("agentic_devtools.state.get_repo_root", return_value=repo_root),
            patch("agentic_devtools.state._get_or_refresh_identity", return_value="tester"),
            patch("agentic_devtools.orchestration.checkpointing.sqlite3.connect", side_effect=_connect),
        ):
            saver = get_checkpointer(
                state_dir=legacy_dir,
                worktree_key="FEATURE-88",
            )
        try:
            actual = saver.conn.execute("PRAGMA database_list").fetchone()[2]
            expected = repo_root / ".agdt" / "workflows" / "tester" / "FEATURE-88" / "orchestration.db"
            assert Path(actual) == expected
        finally:
            saver.conn.close()

        assert "probe failed" in capsys.readouterr().err

    def test_default_path_env_var_override(self, tmp_path, monkeypatch):
        """AGENTIC_DEVTOOLS_STATE_DIR env var is respected via get_state_dir()."""
        env_dir = tmp_path / "env_override"
        env_dir.mkdir(parents=True)
        monkeypatch.setenv("AGENTIC_DEVTOOLS_STATE_DIR", str(env_dir))
        # get_state_dir() checks env var first, so no additional mocking needed
        # but we patch to ensure isolation from the real environment
        with patch(
            "agentic_devtools.state.get_state_dir",
            return_value=env_dir,
        ):
            saver = get_checkpointer()
        try:
            expected = env_dir / "orchestration.db"
            assert expected.exists()
        finally:
            saver.conn.close()

    def test_different_state_dirs_use_isolated_databases(self, tmp_path):
        """Different worktree state directories receive separate checkpoint databases."""
        first_state_dir = tmp_path / "workflows" / "first"
        second_state_dir = tmp_path / "workflows" / "second"

        with patch(
            "agentic_devtools.state.get_state_dir",
            side_effect=[first_state_dir, second_state_dir],
        ):
            first = get_checkpointer()
            second = get_checkpointer()
        try:
            first_path = first.conn.execute("PRAGMA database_list").fetchone()[2]
            second_path = second.conn.execute("PRAGMA database_list").fetchone()[2]
            assert Path(first_path) == first_state_dir / "orchestration.db"
            assert Path(second_path) == second_state_dir / "orchestration.db"
            assert first_path != second_path
        finally:
            first.conn.close()
            second.conn.close()

    def test_custom_path_overrides_default(self, tmp_path):
        custom = tmp_path / "custom" / "my.db"
        saver = get_checkpointer(str(custom))
        try:
            assert custom.exists()
            default = tmp_path / ".agdt" / "orchestration.db"
            assert not default.exists()
        finally:
            saver.conn.close()

    def test_schema_is_initialized(self, tmp_path):
        db_path = str(tmp_path / "test.db")
        saver = get_checkpointer(db_path)
        try:
            cursor = saver.conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = {row[0] for row in cursor.fetchall()}
            assert "checkpoints" in tables
        finally:
            saver.conn.close()

    def test_existing_directory_no_error(self, tmp_path):
        db_dir = tmp_path / "existing"
        db_dir.mkdir()
        db_path = str(db_dir / "test.db")
        saver = get_checkpointer(db_path)
        try:
            assert isinstance(saver, SqliteSaver)
        finally:
            saver.conn.close()

    def test_custom_path_expands_user_home(self, tmp_path, monkeypatch):
        monkeypatch.setenv("HOME", str(tmp_path))
        monkeypatch.setenv("USERPROFILE", str(tmp_path))
        saver = get_checkpointer("~/custom.db")
        try:
            expected = (tmp_path / "custom.db").resolve()
            actual = saver.conn.execute("PRAGMA database_list").fetchone()[2]
            assert Path(actual) == expected
        finally:
            saver.conn.close()

    def test_state_dir_places_db_in_scoped_directory(self, tmp_path):
        """state_dir parameter uses the pre-resolved scope without further path expansion."""
        scoped_dir = tmp_path / "workflows" / "identity" / "ISSUE-123"
        scoped_dir.mkdir(parents=True)
        saver = get_checkpointer(state_dir=scoped_dir)
        try:
            expected = scoped_dir / "orchestration.db"
            assert expected.exists()
            actual = saver.conn.execute("PRAGMA database_list").fetchone()[2]
            assert Path(actual) == expected
        finally:
            saver.conn.close()

    def test_state_dir_resolves_relative_path(self, tmp_path, monkeypatch):
        """Relative state_dir paths are resolved before SQLite opens the database."""
        monkeypatch.chdir(tmp_path)
        relative_dir = Path("relative-scope")
        saver = get_checkpointer(state_dir=relative_dir)
        try:
            actual = saver.conn.execute("PRAGMA database_list").fetchone()[2]
            assert Path(actual) == (tmp_path / relative_dir / "orchestration.db").resolve()
        finally:
            saver.conn.close()

    def test_state_dir_does_not_call_get_state_dir(self, tmp_path):
        """When state_dir is provided, get_state_dir() is never called (no second resolution)."""
        scoped_dir = tmp_path / "scoped"
        scoped_dir.mkdir()
        with patch(
            "agentic_devtools.state.get_state_dir",
            side_effect=AssertionError("get_state_dir must not be called when state_dir is supplied"),
        ):
            saver = get_checkpointer(state_dir=scoped_dir)
        try:
            assert (scoped_dir / "orchestration.db").exists()
        finally:
            saver.conn.close()

    def test_state_dir_without_repo_root_uses_provided_scope_directly(self, tmp_path):
        """Without a repo root, the provided workflow-managed path remains authoritative."""
        with patch("agentic_devtools.state.get_repo_root", return_value=None):
            saver = get_checkpointer(
                state_dir=tmp_path / "standalone",
                worktree_key="FEATURE-42",
            )
        try:
            actual = saver.conn.execute("PRAGMA database_list").fetchone()[2]
            assert Path(actual) == tmp_path / "standalone" / "orchestration.db"
        finally:
            saver.conn.close()

    def test_state_dir_does_not_expand_user_home(self, tmp_path):
        """state_dir accepts a Path object; tilde expansion is not applied."""
        # A Path object starting with '~' in the stem is treated literally.
        # (A real home-expansion use case should go through db_path instead.)
        literal_dir = tmp_path / "~user" / "scoped"
        literal_dir.mkdir(parents=True)
        saver = get_checkpointer(state_dir=literal_dir)
        try:
            expected = literal_dir / "orchestration.db"
            assert expected.exists()
        finally:
            saver.conn.close()
