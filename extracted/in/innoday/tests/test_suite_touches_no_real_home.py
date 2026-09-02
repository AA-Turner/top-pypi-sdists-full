"""The suite must not read or write the developer's own ~/.innoday.

This guards the fixture, not a feature. Running `pytest tests/cli/` used to
rewrite the real `~/.innoday/config.json`: `CLIConfig()` built without an
explicit path defaults to `Path.home() / ".innoday" / "config.json"`, and
`PlatformCommands`' start path used to stamp `platform_server.last_started` and
save.

The write happened to be a single timestamp, so nothing broke. That was the
blast radius of what that code path wrote *then*, not a property of the
arrangement -- which is the reason to close it rather than note it. The point
has since been made for us: that caller is gone (#729) and
`CLIConfig.__init__` now rewrites the file it loads all by itself.
"""

from pathlib import Path

from tests.conftest import REAL_HOME


class TestTheSuiteCannotReachTheRealHome:
    def test_home_is_redirected_away_from_the_real_one(self):
        """`Path.home()` inside a test must not be the developer's home.

        `REAL_HOME` is captured at conftest import, before any fixture runs, so
        this compares against the genuine value rather than the redirected one.
        """
        assert Path.home() != REAL_HOME, (
            "HOME still points at the developer's real home during tests, so "
            "any CLIConfig() built without an explicit path writes to their "
            "actual ~/.innoday/config.json"
        )

    def test_the_default_config_path_lands_in_the_throwaway_home(self):
        """The path CLIConfig would choose on its own is inside the fake home.

        Asserting on `Path.home()` alone would pass even if CLIConfig resolved
        its default some other way (an env var, a hardcoded path); this pins the
        thing that actually gets written.
        """
        from src.cli.config import CLIConfig

        default_path = Path(CLIConfig()._get_config_path(None))

        assert REAL_HOME not in default_path.parents, (
            f"CLIConfig's default path {default_path} is under the real home "
            f"{REAL_HOME} -- a test that builds one would write there"
        )
        assert default_path.name == "config.json"

    def test_writing_through_a_default_config_leaves_the_real_file_alone(self):
        """The end-to-end property: a default-path save cannot touch the real file.

        Written as a *behavioural* check rather than a path assertion, because
        the original bug was a real `save()` -- so this exercises the same
        motion (construct with no path, mutate, save) and then reads the real
        file's bytes back.
        """
        from src.cli.config import CLIConfig

        real_config = REAL_HOME / ".innoday" / "config.json"
        before = real_config.read_bytes() if real_config.exists() else None

        cfg = CLIConfig()
        cfg.set_api_url("https://example.invalid")
        cfg.save()

        after = real_config.read_bytes() if real_config.exists() else None
        assert after == before, (
            "a CLIConfig() built with no explicit path wrote to the real "
            f"{real_config} -- the suite is not isolated from the developer's machine"
        )
