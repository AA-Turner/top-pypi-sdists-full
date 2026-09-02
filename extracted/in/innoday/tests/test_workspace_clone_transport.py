"""How `innoday init` decides to clone, and why the order matters.

The original preference was `clone_url` (HTTPS) first. On a machine
authenticated by SSH key -- the normal setup for anyone cloning private repos
by hand -- git has no credential helper and nothing to prompt, so every clone
died with `could not read Username for 'https://github.com'`. Onboarding a
whole workspace produced `0 cloned, 7 errored`.

These pin the order and the URL parsing so it cannot silently regress.
"""

from pathlib import Path

import pytest

from src.cli.commands import workspace as ws

TARGET = Path("/tmp/target")

SSH = "git@github.com:havilandsoftware/bps-api.git"
HTTPS = "https://github.com/havilandsoftware/bps-api.git"


@pytest.fixture(autouse=True)
def _no_cached_gh():
    """`_gh_can_clone` is lru_cached; a stale answer would leak between tests.

    Hold the real cached function rather than looking it up again on the way
    out: tests here monkeypatch `ws._gh_can_clone` with a plain function, and
    monkeypatch does not undo that until *after* this fixture's teardown -- so
    the exit path used to call `cache_clear()` on the replacement and raise
    `AttributeError: 'function' object has no attribute 'cache_clear'`. Every
    test in this class errored at teardown while still reporting as passed,
    so the suite showed `15 passed, 5 errors` and nobody looked.
    """
    cached = ws._gh_can_clone
    cached.cache_clear()
    yield
    cached.cache_clear()


class TestOwnerRepo:
    """`gh repo clone` wants `owner/repo`, and the payload never carries it.

    Owner is the GitHub org attached to the project's InnoDay org; repo is its
    own name. Both are on hand at clone time, so no URL is parsed -- an earlier
    version parsed the clone URL and turned `file:///srv/mirror.git` into
    `srv/mirror`, which `gh` cannot address.
    """

    def test_it_joins_the_org_and_the_repo_name(self):
        assert ws._owner_repo("havilandsoftware", "bps-api") == (
            "havilandsoftware/bps-api"
        )

    def test_stray_slashes_do_not_double_up(self):
        assert ws._owner_repo("havilandsoftware/", "/bps-api") == (
            "havilandsoftware/bps-api"
        )

    @pytest.mark.parametrize(
        "org,name", [(None, "r"), ("", "r"), ("o", None), ("o", ""), (None, None)]
    )
    def test_a_missing_half_is_none_so_the_git_path_is_used(self, org, name):
        assert ws._owner_repo(org, name) is None


class TestCloneTransport:
    def test_gh_is_preferred_when_installed_and_authenticated(self, monkeypatch):
        """gh resolves auth itself, so it works on SSH and HTTPS machines alike."""
        monkeypatch.setattr(ws, "_gh_can_clone", lambda: True)
        command = ws._clone_command(
            {"name": "bps-api", "ssh_url": SSH, "clone_url": HTTPS},
            TARGET,
            "havilandsoftware",
        )
        assert command[:4] == ["gh", "repo", "clone", "havilandsoftware/bps-api"]

    def test_ssh_beats_https_without_gh(self, monkeypatch):
        """The regression itself: HTTPS-first broke every clone on this machine."""
        monkeypatch.setattr(ws, "_gh_can_clone", lambda: False)
        command = ws._clone_command({"ssh_url": SSH, "clone_url": HTTPS}, TARGET)
        assert command == ["git", "clone", SSH, str(TARGET)]

    def test_https_is_used_when_it_is_all_there_is(self, monkeypatch):
        """A container or CI box with a credential helper and no key."""
        monkeypatch.setattr(ws, "_gh_can_clone", lambda: False)
        command = ws._clone_command({"clone_url": HTTPS}, TARGET)
        assert command == ["git", "clone", HTTPS, str(TARGET)]

    def test_gh_is_skipped_when_the_org_is_unknown(self, monkeypatch):
        """Falling back beats handing `gh` something it cannot address."""
        monkeypatch.setattr(ws, "_gh_can_clone", lambda: True)
        command = ws._clone_command({"name": "r", "ssh_url": SSH}, TARGET, None)
        assert command == ["git", "clone", SSH, str(TARGET)]

    def test_no_url_at_all_is_none_so_the_caller_can_report_it(self, monkeypatch):
        monkeypatch.setattr(ws, "_gh_can_clone", lambda: False)
        assert ws._clone_command({"name": "x"}, TARGET) is None


class TestGhAvailability:
    def test_absent_gh_is_not_usable(self, monkeypatch):
        monkeypatch.setattr(ws.shutil, "which", lambda _: None)
        assert ws._gh_can_clone() is False

    def test_installed_but_logged_out_is_not_usable(self, monkeypatch):
        """The trap: presence alone would make `gh repo clone` fail like HTTPS did."""
        monkeypatch.setattr(ws.shutil, "which", lambda _: "/usr/bin/gh")

        class _Failed:
            returncode = 1

        monkeypatch.setattr(ws.subprocess, "run", lambda *a, **k: _Failed())
        assert ws._gh_can_clone() is False

    def test_installed_and_authenticated_is_usable(self, monkeypatch):
        monkeypatch.setattr(ws.shutil, "which", lambda _: "/usr/bin/gh")

        class _Ok:
            returncode = 0

        monkeypatch.setattr(ws.subprocess, "run", lambda *a, **k: _Ok())
        assert ws._gh_can_clone() is True
