"""The importing agent is told about the same commands a live session is.

The prompt used to carry a hand-written list of eight commands. It had drifted:
`probe project create --parent` has existed for a while and the list never
mentioned it, so an import could not file into a subproject even though the
agent could already run the command. A second copy of a vocabulary is a copy
that goes stale, so the prompt now loads the skill documents themselves. These
tests are what stops the copy coming back.
"""

from __future__ import annotations

import re

import pytest

from probe.cli import backfill as bf


def test_this_installation_can_read_its_own_skill_documents():
    text = bf.vocabulary_text()
    assert text, "no skill text found; a source tree and a wheel both ship it"
    for name in bf.VOCABULARY_SKILLS:
        assert f"--- reference: {name} ---" in text


def test_the_import_overrides_are_stated_before_the_shared_text():
    """A live session is told to register projects as it goes. This one is not."""
    text = bf.vocabulary_text()
    preamble, _, rest = text.partition("--- reference:")
    assert "The project list is FIXED" in preamble
    assert "Do not create projects or subprojects" in preamble
    assert "invented experiment" in preamble
    assert "not attributed to a session" in preamble or "attributed to a session" in preamble
    assert rest, "the shared text must follow the overrides, not replace them"


def test_every_probe_command_the_text_names_exists_on_this_cli():
    """The drift guard. A renamed command fails here, not in a folder import."""
    from typer.main import get_command

    from probe.cli.main import app

    root = get_command(app)

    def resolve(parts):
        command = root
        for part in parts:
            group = getattr(command, "commands", None)
            if not group or part not in group:
                return None
            command = group[part]
        return command

    text = bf.vocabulary_text()
    named = set()
    for match in re.finditer(r"\bprobe ((?:[a-z][a-z0-9-]*)(?: [a-z][a-z0-9-]*)?)", text):
        named.add(tuple(match.group(1).split()))

    missing = []
    for parts in sorted(named):
        if resolve(parts) is not None:
            continue
        # A one-word miss may be the first word of a two-word command that the
        # regex split, or ordinary prose ("probe knows", "probe research").
        if len(parts) == 1 and any(p[0] == parts[0] for p in named if len(p) == 2):
            continue
        if len(parts) == 2 and resolve(parts[:1]) is not None:
            missing.append(" ".join(parts))
    assert missing == [], f"skill text names commands this CLI does not have: {missing}"


def test_subprojects_are_reachable_now_that_the_list_is_not_hand_written():
    """The specific gap that motivated this: --parent was never mentioned."""
    text = bf.vocabulary_text()
    assert "--parent" in text or "subproject" in text.lower()


def test_the_prompt_carries_the_reference_and_stays_within_budget():
    """Loading whole documents is a deliberate cost. Make it visible when it grows."""
    from pathlib import Path

    prompt = bf.build_prompt(folder=Path("/tmp/folder"), census=bf.Census(files=10, bytes=100))
    assert "--- reference: track-work ---" in prompt
    # ~60k characters is roughly 19k tokens per unit turn. Well inside a modern
    # context window and well outside "nobody noticed it doubled".
    assert len(prompt) < 60_000, (
        f"the unit prompt is now {len(prompt):,} characters and is paid once per "
        "unit turn; re-measure before raising this"
    )


def test_a_build_without_the_shared_data_still_imports(monkeypatch):
    """Empty is a valid answer: the importer's own rules do not depend on this."""
    monkeypatch.setattr(bf, "_skills_root", lambda: None)
    bf.vocabulary_text.cache_clear()
    try:
        assert bf.vocabulary_text() == ""
        from pathlib import Path

        prompt = bf.build_prompt(folder=Path("/tmp/folder"), census=bf.Census(files=1, bytes=1))
        assert "probe artifact add" in prompt, "the importer's own instructions must survive"
    finally:
        bf.vocabulary_text.cache_clear()


@pytest.mark.parametrize("name", bf.VOCABULARY_SKILLS)
def test_each_named_skill_is_present_in_the_tree(name):
    root = bf._skills_root()
    assert root is not None
    assert (root / name / "SKILL.md").is_file()
