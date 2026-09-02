"""`--release` is one flag, and `releases summarize` is the same assembly.

`--scrum --window release` was two flags saying one thing. A release summary is
a team summary -- "what is in this release" is never a question about one
person's slice of it -- so the pair was the only spelling anyone used, and
getting half of it wrong was silent: `--window release` alone answers with the
caller's own tickets, which on a release they hold none of is an empty summary
that looks exactly like a quiet release.

`innoday releases summarize` used to require a version positional and print the
release *row* instead: its stored `summary` string, whatever blastoff last
wrote. Two commands called "summarize", two different answers, one of them
stale by construction. It now proxies to this assembly and defaults to the
release being cut -- the same default `releases content` already had.
"""

from __future__ import annotations

import argparse

import pytest

from src.cli.commands.releases import ReleasesCommands
from src.cli.commands.summary import (
    SummaryCommands,
    _summary_params,
    release_to_scope,
)


@pytest.fixture
def summary_parser():
    parser = argparse.ArgumentParser()
    SummaryCommands.setup_parser(parser)
    return parser


@pytest.fixture
def releases_parser():
    parser = argparse.ArgumentParser()
    ReleasesCommands.setup_parser(parser)
    return parser


class TestReleaseFlag:
    def test_bare_release_means_the_one_being_cut(self, summary_parser):
        """The bare word is the point: no version to look up first."""
        assert summary_parser.parse_args(["--release"]).summary_release is True

    def test_a_version_can_still_be_named(self, summary_parser):
        args = summary_parser.parse_args(["--release", "v1.11.0"])
        assert args.summary_release == "v1.11.0"

    def test_absent_is_not_the_release_scope(self, summary_parser):
        """`None`, not `False` -- `execute` distinguishes "not asked for" from
        "asked for, bare", and `False` would collapse the two."""
        assert summary_parser.parse_args([]).summary_release is None

    def test_the_bare_flag_scopes_to_the_servers_sentinel(self):
        """Never a version resolved here: the CLI computing which release is
        current, from its own rule, is the defect #563 removed."""
        window_spec, release, note = release_to_scope(True)
        assert window_spec is None
        assert release == "current"
        assert "release" in note

    def test_a_named_version_passes_through_untouched(self):
        """Normalising case or prefix would mint a second cache key for one
        release, which is a cache miss every morning."""
        _, release, note = release_to_scope("v1.11.0")
        assert release == "v1.11.0"
        assert "v1.11.0" in note

    def test_the_boundary_note_is_never_dropped(self):
        """The note is the line that states the slice. A release summary printed
        without it is a subset presented as the whole project."""
        for version in (True, None, "v1.11.0"):
            assert release_to_scope(version)[2]

    def test_window_release_still_resolves_the_same_way(self):
        """The older spelling keeps working -- and shares the one code path, so
        it cannot drift into answering differently."""
        assert SummaryCommands.window_to_scope("release") == release_to_scope(True)

    def test_a_release_is_sent_as_a_release_not_a_window(self):
        """Two different scopes; sending both would leave the winner to the
        server and give the reader no way to tell which they got."""
        window_spec, release, _ = release_to_scope(True)
        params = _summary_params(window_spec=window_spec, release=release, scrum=True)
        assert params["release"] == "current"
        assert "window_spec" not in params


class TestReleaseImpliesTheTeam:
    """`--release` needs no `--scrum` beside it."""

    def _scope(self, args: argparse.Namespace) -> bool:
        release_arg = getattr(args, "summary_release", None)
        return bool(getattr(args, "scrum", False)) or release_arg is not None

    def test_release_alone_is_a_team_summary(self, summary_parser):
        assert self._scope(summary_parser.parse_args(["--release"])) is True

    def test_the_redundant_pair_is_accepted_not_rejected(self, summary_parser):
        """It is the spelling this flag replaces, and it says the same thing."""
        assert self._scope(summary_parser.parse_args(["--scrum", "--release"])) is True

    def test_a_plain_summary_is_still_personal(self, summary_parser):
        assert self._scope(summary_parser.parse_args([])) is False

    def test_window_release_can_still_be_personal(self, summary_parser):
        """A personal release view is a real thing to want, and only `--window`
        can express it -- so `--release` not covering it is not a gap."""
        args = summary_parser.parse_args(["--window", "release"])
        assert self._scope(args) is False


class TestSummarizeDefaultsToTheReleaseBeingCut:
    def test_the_version_is_optional(self, releases_parser):
        args = releases_parser.parse_args(["summarize"])
        assert args.version is None

    def test_a_version_may_still_be_passed(self, releases_parser):
        args = releases_parser.parse_args(["summarize", "v1.11.0"])
        assert args.version == "v1.11.0"

    def test_no_version_becomes_the_current_release(self, releases_parser):
        """`None or True` is the proxy's translation, and `release_to_scope`
        turns both into the server's sentinel -- so "omitted" means the same
        thing here as it does for `releases content`."""
        version = releases_parser.parse_args(["summarize"]).version
        assert release_to_scope(version or True)[1] == "current"

    def test_json_survives_the_proxy(self, releases_parser):
        """The skill reads the raw payload; a `--json` that silently rendered
        prose instead would break it."""
        args = releases_parser.parse_args(["summarize", "--json"])
        assert args.summary_json is True

    def test_no_org_id_flag_that_would_be_accepted_and_ignored(self, releases_parser):
        """It selected the org for a release-row fetch that no longer happens.
        The entrypoint's `--organization` is the way to point elsewhere."""
        summarize = releases_parser.parse_args(["summarize"])
        assert not hasattr(summarize, "org_id")
