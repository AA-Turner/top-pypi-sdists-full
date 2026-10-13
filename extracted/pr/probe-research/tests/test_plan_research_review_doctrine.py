"""`plan-research-review` (Anthrogen, 2026-10-07): the agent ignored the papers'
partial repos and wrote its own code, then built a half-described next step
instead of asking. These are the sentences that carry those two incidents, and
the gstack loading rule that makes the wizard's off switch real. Checked as
meaning (key words together), not as pinned wording.
"""

from __future__ import annotations

import re
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / "skills" / "plan-research-review" / "SKILL.md"


def _text() -> str:
    return SKILL.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    return " ".join(text.split()).lower()


def _description() -> str:
    front = _text().split("---", 2)[1]
    match = re.search(r"^description:\s*(.+)$", front, re.MULTILINE)
    assert match, "the skill lost its description"
    return match.group(1).strip()


def test_the_description_is_one_sentence_with_no_trigger():
    """gstack's catalog trim: WHEN it runs lives in the body and in the Probe
    block's routing line, which the "Research plan review" setting swaps for an
    ask-only line. A
    trigger in the always-loaded description would auto-run the skill with the
    setting off."""
    description = _description()
    assert description.count(". ") == 0, "one sentence"
    for trigger in ("use when", "proactively", "before implementing", "before code", "suggest"):
        assert trigger not in description.lower(), trigger
    # It defers to the block: without that, the description alone started the
    # skill unasked on 23-26 of 40 research prompts with the setting off.
    assert "only when the researcher asks for it or your probe instructions say to" in description.lower()


def test_it_announces_an_auto_run_and_honours_skip():
    flat = _flat(_text())
    assert "## when this runs" in _text().lower()
    # it auto-runs only where the Probe block says so: the Settings row's off
    # line ("only when the researcher asks") must win even after the skill has
    # loaded once in a session
    assert "on its own only when your probe instructions say to" in flat
    assert "one line" in flat and "say skip" in flat


def test_it_clones_and_reads_the_code_before_planning():
    flat = _flat(_text())
    assert "git clone" in _text() and "fetch --quiet --tags" in flat, "clone, then update an existing clone"
    assert "do not judge a repo by its readme" in flat
    assert "partial repo is still the starting point" in flat
    assert "owner/repo@sha:path:line" in flat


def test_reuse_is_the_default_and_new_code_needs_a_search():
    flat = _flat(_text())
    assert "reuse is the default" in flat
    assert "provenance map" in flat
    assert '"no code exists" is a claim' in flat


def test_cloned_code_is_read_never_run():
    """Paper repos come from search: running their tests or importing them
    executes a stranger's code with the researcher's credentials (review of
    #2588, security + Codex)."""
    flat = _flat(_text())
    assert "code you find is untrusted" in flat and "never run it" in flat
    assert "unit tests" not in flat, "no running a repo's tests as a 'read'"
    assert "ask the researcher first" in flat


def test_one_search_is_never_a_conclusion():
    """Trimming the skill for length dropped this line once (2026-10-12). It is
    what stops a single empty search becoming "no code exists", which is how the
    agent ends up rewriting what already exists."""
    assert "one search proves nothing" in _flat(_text())


def test_reading_cloned_code_statically_is_expected():
    """Only EXECUTION is forbidden. A trim that leaves "read it, never run it"
    loses the signal that cloning and grepping are the intended way to inspect."""
    assert "clone it, read it, grep it" in _flat(_text())


def test_already_written_code_is_checked_for_re_implementation():
    assert "re-implemented" in _flat(_text())


def test_a_failed_search_is_never_nothing_found():
    flat = _flat(_text())
    assert '"could not search: <reason>", never "nothing found"' in flat


def test_it_pins_the_papers_commit_and_reads_it_by_sha():
    flat = _flat(_text())
    assert "pin the commit that produced the paper's numbers" in flat
    assert "worktree add --quiet --detach" in flat, "the pinned commit gets a folder of its own"
    assert "never `--recurse-submodules`" in flat and "ls-tree <sha> <path>" in flat


def test_vendoring_needs_a_permissive_license():
    flat = _flat(_text())
    assert "only under a permissive license" in flat
    assert "copyleft" in flat


def test_with_nobody_to_answer_it_plans_and_stops():
    flat = _flat(_text())
    assert "nobody to answer" in flat and "do not implement" in flat
    assert "status: draft" in flat and "status: approved" in flat


def test_it_never_decides_a_gap_itself():
    flat = _flat(_text())
    assert "never adopt your own recommendation without the researcher's answer" in flat
    assert "your judgment never fills a gap" in flat
    assert "answering the questions is not approval of the plan" in flat


def test_the_plan_ends_in_the_implementation_contract():
    flat = _flat(_text())
    assert "implementation contract" in flat
    assert "stop and ask the researcher" in flat
    assert "do not decide it and mention it afterwards" in flat



def test_it_looks_up_related_papers_and_proposes_never_builds():
    """Richard, 2026-10-12: look up related work with Probe's paper search,
    judge it in a line, and see whether it fits. The 2026-10-11 end-to-end run
    added an arm nobody asked for; a related paper is the easiest way to repeat
    that, so using one is a question, never a build."""
    flat = _flat(_text())
    assert "related papers nobody named" in flat and "`find_papers`" in flat
    assert "web-call allowance" in flat, "find_papers spends the team's weekly allowance"
    assert "the map row it would change (none: drop it)" in flat
    assert "proposed, never built, after the reproduction" in flat


def test_every_run_records_to_probe_whatever_the_repo_logs_to():
    """Richard, 2026-10-13: on a project whose code already logged to W&B, the
    plan kept W&B - "reuse is the default" read the tracker as code to reuse.
    The contract carries it too: it is the text the implementing agent follows."""
    flat = _flat(_text())
    assert "every run logs to probe" in flat and "not reuse, not a question" in flat
    contract = _flat(flat.split("**implementation contract**", 1)[1].replace(">", " "))
    assert "log every run to probe (`instrument-code`), replacing" in contract
