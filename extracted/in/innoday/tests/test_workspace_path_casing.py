"""Where `innoday init` puts a workspace, and why the case matters.

Project aliases are conventionally uppercase (`BPCL`, `BPAI`, `PF`), but
workspace directories are lowercase everywhere else on disk -- `~/workspaces/hs/pf`,
`~/workspaces/bp/bp-ai`. Passing the alias through verbatim produced
`~/workspaces/bp/BPCL`, the odd one out, and on a case-insensitive filesystem it
is the same directory as `bpcl` while comparing unequal in code.

An explicit `--path` is the user's call and is left exactly as given.
"""

from pathlib import Path

import pytest

from src.cli.commands import workspace as ws


@pytest.fixture
def home() -> Path:
    """Resolve HOME the same way and at the same time the code under test does.

    This was a module-level `HOME = Path.home()`, bound at import. `_workspace_path`
    resolves `Path.home()` when it is *called*, so the two only agreed as long as
    nothing redirected HOME in between -- and the suite now does, deliberately, so
    that no test can write to the developer's real `~/.innoday`. Binding at import
    made every assertion here compare a pre-redirect home against a post-redirect
    one. What these tests are about is the *casing* of the alias segments, not
    which home directory they hang off.
    """
    return Path.home()


def test_uppercase_project_alias_becomes_lowercase_directory(home):
    assert ws._workspace_path("bp", "BPCL", None) == home / "workspaces/bp/bpcl"


def test_uppercase_org_alias_becomes_lowercase_directory(home):
    assert ws._workspace_path("BP", "BPCL", None) == home / "workspaces/bp/bpcl"


def test_mixed_case_is_normalised(home):
    assert ws._workspace_path("Bp", "BpCl", None) == home / "workspaces/bp/bpcl"


def test_already_lowercase_is_unchanged(home):
    assert ws._workspace_path("hs", "pf", None) == home / "workspaces/hs/pf"


def test_org_only_falls_back_to_lowercased_org(home):
    assert ws._workspace_path("BP", None, None) == home / "workspaces/bp/bp"


def test_hyphenated_alias_keeps_its_hyphens(home):
    assert ws._workspace_path("bp", "BP-Cloud", None) == home / "workspaces/bp/bp-cloud"


def test_explicit_override_is_respected_verbatim():
    """--path is the user's decision -- don't normalise their case away."""
    assert ws._workspace_path("bp", "BPCL", "/tmp/MyWorkspace") == Path(
        "/tmp/MyWorkspace"
    )
