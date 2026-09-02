"""`innoday upgrade` must not report success while changing nothing.

Measured 2026-08-27: `0.1.326b0` had been on PyPI for some minutes, the command
printed "Reinstall complete", and the binary was still `0.1.325b0`. Both halves
were wrong and each hid the other -- uv resolved from a cached index, so the new
release was invisible; and the success line was printed unconditionally, so
nothing noticed. The next report is always about a fix that "did not ship".
"""

from __future__ import annotations

from src.cli.commands.upgrade import (
    _build_reinstall_command,
    _versions_equal,
    installed_version_from_uv,
)


class TestTheIndexIsRefetched:
    def test_reinstall_asks_pypi_again(self):
        """`--reinstall` rebuilds the environment; it does not re-ask PyPI what
        exists. Without uv's `--refresh` the command reinstalls the version
        already present and calls that an upgrade."""
        assert "--refresh" in _build_reinstall_command(None)
        assert "--reinstall" in _build_reinstall_command(None)

    def test_a_pinned_version_still_refreshes(self):
        cmd = _build_reinstall_command("0.1.300b0")
        assert "innoday==0.1.300b0" in cmd
        assert "--refresh" in cmd


class TestWhatUvSaysItInstalled:
    """The only statement of what actually landed.

    `get_version()` cannot answer it: this process *is* the binary being
    replaced, so it reports the version on its way out.
    """

    def test_it_reads_the_version_out_of_uvs_summary(self):
        assert installed_version_from_uv(" ~ innoday==0.1.326b0") == "0.1.326b0"
        assert installed_version_from_uv(" + innoday==0.1.326b0") == "0.1.326b0"

    def test_a_sibling_package_is_not_mistaken_for_the_cli(self):
        """uv prints `innoday-blastoff==0.7.1` on the very next line of the same
        summary. Reading that as the CLI's version would compare a package that
        did not change against the release that was expected, and warn on every
        successful upgrade."""
        summary = " ~ innoday-blastoff==0.7.1\n ~ yarl==1.24.5"
        assert installed_version_from_uv(summary) is None

    def test_it_finds_the_line_among_the_others(self):
        summary = (
            "Installed 109 packages in 37ms\n"
            " ~ innoday==0.1.326b0\n"
            " ~ innoday-blastoff==0.7.1\n"
            "Installed 2 executables: innoday, mcp-server-innoday"
        )
        assert installed_version_from_uv(summary) == "0.1.326b0"

    def test_silence_is_could_not_tell_rather_than_failed(self):
        """uv's output format is not a contract. A parser that guessed would
        turn a working upgrade into a warning the next time it shifts."""
        assert installed_version_from_uv("") is None
        assert installed_version_from_uv("Installed 2 executables") is None


class TestTheComparisonThatDecidesWhetherToWarn:
    def test_the_landed_version_is_compared_to_the_expected_one(self):
        assert _versions_equal("0.1.326b0", "0.1.326b0")
        assert not _versions_equal("0.1.325b0", "0.1.326b0")
