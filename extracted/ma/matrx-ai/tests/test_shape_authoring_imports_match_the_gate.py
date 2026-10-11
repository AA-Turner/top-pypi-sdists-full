"""The shape-authoring skill's import list IS the gate's import list.

The ``shape-authoring`` skill (the one rulebook for kind components, attached to
every run holding a kindcomp_* / kind_create tool) tells the author which module
paths exist in its ``<available_imports>`` block. The browser compiler and this
host enforce ``allowedImports`` in ``apps/shared/code-runtime/src/gate-lists.json``.
If the two drift, the skill either teaches an import the save refuses or hides one
the author could use. Lint refusals point at the skill's block instead of
restating the list, so this parity is what keeps that pointer honest.

Reads this repo's synced copy of the skill (common-docs/meta/scripts/sync_skills.py
distributes it here), so the test never skips.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

AIDREAM_ROOT = Path(__file__).resolve().parents[3]
GATE_JSON = AIDREAM_ROOT / "apps/shared/code-runtime/src/gate-lists.json"
SKILL_MD = AIDREAM_ROOT / ".claude/skills/shape-authoring/SKILL.md"

_BLOCK = re.compile(r"<available_imports>(.*?)</available_imports>", re.DOTALL)
_QUOTED = re.compile(r'"([^"\n]+)"')


def skill_import_paths(skill_text: str) -> list[str]:
    match = _BLOCK.search(skill_text)
    assert match, "shape-authoring skill has no <available_imports> block"
    return _QUOTED.findall(match.group(1))


def parity_problems(skill_paths: list[str], gate_paths: list[str]) -> list[str]:
    problems: list[str] = []
    dupes = sorted({p for p in skill_paths if skill_paths.count(p) > 1})
    if dupes:
        problems.append(f"listed twice in the skill: {dupes}")
    only_skill = sorted(set(skill_paths) - set(gate_paths))
    if only_skill:
        problems.append(f"skill teaches imports the gate refuses: {only_skill}")
    only_gate = sorted(set(gate_paths) - set(skill_paths))
    if only_gate:
        problems.append(f"gate allows imports the skill never mentions: {only_gate}")
    return problems


def test_skill_available_imports_equal_the_gate_allowed_imports() -> None:
    gate = json.loads(GATE_JSON.read_text(encoding="utf-8"))["allowedImports"]
    skill = skill_import_paths(SKILL_MD.read_text(encoding="utf-8"))
    problems = parity_problems(skill, gate)
    assert not problems, (
        "shape-authoring <available_imports> drifted from gate-lists.json allowedImports — "
        "edit the canonical skill (common-docs/skills/shape-authoring/SKILL.md), run "
        "sync_skills.py, and keep both lists equal: " + "; ".join(problems)
    )


def test_the_parity_check_goes_red_on_a_planted_mismatch() -> None:
    gate = json.loads(GATE_JSON.read_text(encoding="utf-8"))["allowedImports"]
    text = SKILL_MD.read_text(encoding="utf-8")
    added = text.replace("</available_imports>", '"@/components/ui/not-a-real-part"\n</available_imports>')
    assert parity_problems(skill_import_paths(added), gate)
    removed = text.replace('"recharts"', "", 1)
    assert parity_problems(skill_import_paths(removed), gate)
