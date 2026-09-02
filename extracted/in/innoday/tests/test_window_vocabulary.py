"""One window vocabulary across the CLI, the engine and the MCP tool.

The divergence this pins: `--window` accepted `day | week | 3d | release` while
the engine accepted only the duration grammar. So `--window day` was legal at
the CLI and a 422 at the engine, and `2w` -- fine to the engine -- was rejected
by the CLI. Two vocabularies for one concept, disagreeing in both directions.

The subtler half is the cache. `window_spec` *is* the summary cache key, and
`WINDOW_RE` is case-insensitive and whitespace-tolerant, so `'3D'`, `' 3d '` and
`'day'` all parse to the same timedelta while storing three different keys. A
read under one spelling then misses a row written under another -- which looks
exactly like a cold cache, never like a bug. Canonicalising on the way in is
what makes the module's own "one grammar" comment true.
"""

from __future__ import annotations

import argparse

import pytest

from src.cli.commands.summary import (
    DEFAULT_WINDOW,
    SummaryWindow,
    parse_window_arg,
)
from src.services.summary_service import (
    InvalidWindowSpec,
    canonical_window_spec,
    parse_window_spec,
)
from src.utils.time_windows import (
    WINDOW_ALIASES,
    WINDOW_GRAMMAR_HINT,
    normalize_window,
)

# --------------------------------------------------------------- normalisation


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("3d", "3d"),
        ("3D", "3d"),  # the cache-key case: same window, was a second key
        (" 3d ", "3d"),
        ("3 d", "3d"),
        ("03d", "3d"),
        ("12h", "12h"),
        ("2w", "2w"),
        ("day", "1d"),
        ("WEEK", "1w"),
    ],
)
def test_every_spelling_of_one_window_normalises_to_one_key(raw, expected):
    assert normalize_window(raw) == expected


@pytest.mark.parametrize("raw", ["", None, "release", "yesterday", "3", "d", "3m"])
def test_non_windows_are_not_windows(raw):
    """`release` included: it is resolved against a release, not parsed."""
    assert normalize_window(raw) is None


def test_a_window_covering_nothing_raises_rather_than_normalising():
    with pytest.raises(ValueError, match="at least one unit"):
        normalize_window("0d")


# ---------------------------------------------------------------- the engine


@pytest.mark.parametrize("alias,spec", sorted(WINDOW_ALIASES.items()))
def test_the_engine_accepts_the_aliases_the_cli_offers(alias, spec):
    """The exact 422 that started this: `window_spec='day'` was unsupported."""
    assert parse_window_spec(alias) == parse_window_spec(spec)


def test_canonical_window_spec_is_what_gets_stored():
    assert canonical_window_spec("day") == "1d"
    assert canonical_window_spec(" 3D ") == "3d"


@pytest.mark.parametrize("bad", ["", "yesterday", "3m"])
def test_canonical_window_spec_refuses_a_non_window(bad):
    with pytest.raises(InvalidWindowSpec):
        canonical_window_spec(bad)


def test_a_zero_window_is_a_422_not_a_500():
    """`normalize_window` raises bare ValueError; the routers catch only
    InvalidWindowSpec, so letting it through would be a 500."""
    with pytest.raises(InvalidWindowSpec, match="at least one unit"):
        canonical_window_spec("0d")


# ------------------------------------------------------------------- the CLI


@pytest.mark.parametrize("value", ["3d", "12h", "2w", "1h", "day", "week"])
def test_the_cli_accepts_everything_the_engine_accepts(value):
    """`2w` and `12h` were rejected by the old fixed `choices` list."""
    assert parse_window_arg(value) == normalize_window(value)


def test_release_survives_the_cli_untranslated():
    """It has no duration until the server answers, so it must pass through."""
    assert parse_window_arg("release") == SummaryWindow.RELEASE.value


@pytest.mark.parametrize("bad", ["yesterday", "3m", "", "sprint"])
def test_the_cli_rejects_a_non_window_as_an_argparse_error(bad):
    with pytest.raises(argparse.ArgumentTypeError):
        parse_window_arg(bad)


def test_the_default_window_is_already_canonical():
    """argparse does not pass `default` through `type=`, so a non-canonical
    default would reach the engine unnormalised -- the one value that skips
    every check above."""
    assert normalize_window(DEFAULT_WINDOW) == DEFAULT_WINDOW


def test_the_grammar_is_described_in_exactly_one_place():
    """Three surfaces quote this string. A second copy is how they drifted."""
    for alias in WINDOW_ALIASES:
        assert alias in WINDOW_GRAMMAR_HINT
    assert "3d" in WINDOW_GRAMMAR_HINT
