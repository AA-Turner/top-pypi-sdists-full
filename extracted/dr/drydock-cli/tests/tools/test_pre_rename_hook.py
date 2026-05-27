"""Pre-LLM rename scaffolding for surgery walls.

The hook fires when a user prompt says "rename X to Y" and X appears as
a word-bounded token in 2+ .py files of the current package. Drydock
performs the rename itself before the LLM turn and injects a system
note telling the model to make any remaining contextual fixes (CSV
headers, docs, places where the old name must intentionally survive).

Targets P4-S1 (units→quantity rename) and partially P6-S1 (ItemRepo
extract) — surgery cases where the model historically fails to
propagate a rename across all callsites despite multiple nudges
recommending mechanical_rename.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from drydock.core.agent_loop import AgentLoop


# --- regex sanity ---


@pytest.mark.parametrize(
    "text,expected_old,expected_new",
    [
        # Real P4-S1 prompt language.
        (
            "Rename the internal field `units` to `quantity` everywhere in the code",
            "units", "quantity",
        ),
        # Arrow form.
        (
            "Rename internal field units→quantity (keep CSV header)",
            "units", "quantity",
        ),
        # ASCII arrow.
        ("rename units->quantity", "units", "quantity"),
        # Bare verb.
        ("rename units to quantity", "units", "quantity"),
        # Asterisks (markdown emphasis sometimes wraps identifiers).
        ("Rename *units* to *quantity*", "units", "quantity"),
        # Negative: "renaming" is a different word, must not match.
        ("Renaming files is hard work", None, None),
    ],
)
def test_pre_rename_regex(text: str, expected_old: str | None, expected_new: str | None):
    """Pure regex behavior. The full hook has an additional English-word
    denylist that rejects matches like ('feature', 'the') — that's tested
    end-to-end via _StubLoop below, not here."""
    m = AgentLoop._PRE_RENAME_PATTERN.search(text)
    if expected_old is None:
        assert m is None, f"regex unexpectedly matched: {m and m.groupdict()}"
    else:
        assert m is not None, f"regex should have matched: {text!r}"
        assert m.group("old") == expected_old
        assert m.group("new") == expected_new


# --- end-to-end via stub ---


class _StubLoop:
    """Minimal AgentLoop stub to exercise _maybe_pre_rename without the
    full async + tool registry construction."""

    def __init__(self, cwd: Path) -> None:
        self.cwd = str(cwd)
        self.notes: list[str] = []

    _PRE_RENAME_PATTERN = AgentLoop._PRE_RENAME_PATTERN
    _maybe_pre_rename = AgentLoop._maybe_pre_rename

    def _inject_system_note(self, note: str) -> None:
        self.notes.append(note)


@pytest.fixture(autouse=True)
def _enable_hook(monkeypatch):
    monkeypatch.setenv("DRYDOCK_PRE_RENAME", "1")
    # _maybe_pre_rename short-circuits when PYTEST_CURRENT_TEST is set
    # (to avoid messing with the harness's own tmp dirs). For these
    # tests we explicitly want it to run — unset the marker for the
    # duration of each test.
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)


def _build_pkg(root: Path, name: str, files: dict[str, str]) -> Path:
    """Create a package with files mapping {relpath: content}."""
    pkg = root / name
    pkg.mkdir()
    (pkg / "__init__.py").write_text("")
    for rel, content in files.items():
        p = pkg / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    return pkg


def test_p4_s1_style_multifile_rename_fires(tmp_path):
    """P4-S1 reproduction: a four-file pipeflow package needs the
    identifier `units` renamed to `quantity` everywhere in code, with
    a hint that the CSV header is special and must stay."""
    pkg = _build_pkg(tmp_path, "pipeflow", {
        "schema.py": "FIELDS = {'units': int, 'price': float}\n",
        "transforms.py": "def total(row): return row['units'] * row['price']\n",
        "aggregate.py": "def by_units(rows):\n    return {r['units'] for r in rows}\n",
        "pipeline.py": "from .schema import FIELDS\n# pipe processes units\n",
    })

    loop = _StubLoop(tmp_path)
    loop._maybe_pre_rename(
        "Rename the internal field `units` to `quantity` everywhere in the code "
        "- BUT the CSV column header still uses `units` and must not be edited."
    )

    assert len(loop.notes) == 1, f"expected one injected note, got {len(loop.notes)}"
    note = loop.notes[0]
    assert "units" in note and "quantity" in note
    assert "Pre-rename complete" in note
    # Hook tells the model what's left for IT to do.
    assert "REMAINING" in note or "contextual" in note

    # And the actual rename landed on disk.
    for fname in ("schema.py", "transforms.py", "aggregate.py", "pipeline.py"):
        text = (pkg / fname).read_text()
        assert "quantity" in text, f"{fname}: rename should have introduced `quantity`"


def test_skip_when_old_not_multifile(tmp_path):
    """If the old token only exists in 1 file, leave it to the model —
    single-file renames don't need the heavy hook."""
    _build_pkg(tmp_path, "tinypkg", {
        "only.py": "def widget(): pass\n",
    })
    loop = _StubLoop(tmp_path)
    loop._maybe_pre_rename("rename widget to gadget")
    assert loop.notes == [], "should not fire on single-file rename"


def test_skip_when_new_already_present(tmp_path):
    """If the new token already shows up across roughly half the files,
    skip — rename is partially done or tokens are coincidentally common."""
    _build_pkg(tmp_path, "halfdone", {
        "a.py": "old_name = 1\nnew_name = 2\n",
        "b.py": "x = old_name\ny = new_name\n",
    })
    loop = _StubLoop(tmp_path)
    loop._maybe_pre_rename("rename old_name to new_name")
    assert loop.notes == [], (
        "should skip when new_name is already pervasive — avoid corruption"
    )


def test_skip_when_disabled_by_env(tmp_path, monkeypatch):
    """DRYDOCK_PRE_RENAME=0 hard-disables the hook."""
    monkeypatch.setenv("DRYDOCK_PRE_RENAME", "0")
    _build_pkg(tmp_path, "disabled", {
        "a.py": "units = 1\n",
        "b.py": "x = units\n",
    })
    loop = _StubLoop(tmp_path)
    loop._maybe_pre_rename("rename units to quantity")
    assert loop.notes == [], "env disable should block the hook entirely"


def test_skip_when_no_rename_intent(tmp_path):
    """Innocent messages must never trigger a rename."""
    _build_pkg(tmp_path, "innocent", {
        "a.py": "units = 1\n", "b.py": "x = units\n",
    })
    loop = _StubLoop(tmp_path)
    loop._maybe_pre_rename(
        "Add a CSV import that uses the units field from the schema."
    )
    assert loop.notes == [], "no rename verb → no hook fire"


def test_skip_when_short_identifiers(tmp_path):
    """`rename it to that` matches the regex but should be filtered by
    the 3-char minimum length check — too many false positives on
    pronouns and articles."""
    _build_pkg(tmp_path, "short", {
        "a.py": "it = 1\n", "b.py": "x = it\n",
    })
    loop = _StubLoop(tmp_path)
    loop._maybe_pre_rename("rename it to that")
    assert loop.notes == [], "2-char names blocked"


def test_skip_when_match_is_english_prose(tmp_path):
    """The regex matches 'Add a rename feature to the CLI' with
    old='feature' new='the' — both common English filler words. The
    caller's identifier-denylist must reject this so we don't rename
    every occurrence of `feature` to `the` in random codebases."""
    _build_pkg(tmp_path, "english", {
        "a.py": "feature = 1\nthe = 2\n",
        "b.py": "x = feature\ny = the\n",
    })
    loop = _StubLoop(tmp_path)
    loop._maybe_pre_rename("Add a rename feature to the CLI dispatcher")
    assert loop.notes == [], (
        "must not fire when matched tokens are English filler words"
    )
    # And no file should have been touched.
    assert "feature = 1" in (tmp_path / "english" / "a.py").read_text()
