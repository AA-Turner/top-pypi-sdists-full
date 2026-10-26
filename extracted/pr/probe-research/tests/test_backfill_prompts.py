"""The prompts are the deliverable, so the invariants in them are tested.

The point of the fragments is that a rule cannot drift between passes. So the
tests here mostly assert that the SAME fragment reaches every prompt that needs
it, rather than checking one prompt's wording and letting three others rot.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from probe.cli import backfill_prompts as bp

ROOT = "/workspace/research"
WORK = "/state/probe/backfill-manifests"


def _classify(**kw):
    base = dict(
        root=ROOT,
        evidence_jsonl='{"path":"a.py","tier":"evidence"}',
        existing=[],
        truncated=False,
        work_dir=WORK,
    )
    base.update(kw)
    return bp.classify(**base)


def _import(**kw):
    base = dict(
        root=ROOT, project="odyssey", paths=["a.py", "b/c.csv"], work_dir=WORK
    )
    base.update(kw)
    return bp.import_unit(**base)


# -- shared invariants reach every prompt that needs them --------------------


@pytest.mark.parametrize(
    "prompt,fragment",
    [
        (_import(), bp.DESCRIBE_ARTIFACTS),
        (_import(), bp.GROUPING),
        (_classify(), bp.REUSE),
        (_classify(), bp.DESCRIPTIONS),
    ],
)
def test_the_fragment_arrives_verbatim(prompt, fragment):
    assert fragment in prompt


def test_classify_says_the_question_is_per_file_not_per_folder():
    text = _classify()
    assert "A directory is not a project" in text
    assert "spills across directories" in text


def test_classify_uploads_nothing_and_says_so():
    assert "NOT uploading anything" in _classify()


def test_classify_lists_existing_projects_when_there_are_any():
    text = _classify(existing=["odyssey-infill-v3", "esm3-baseline"])
    assert "odyssey-infill-v3" in text and "esm3-baseline" in text
    assert "Prefer these" in text


def test_classify_says_so_when_nothing_exists_yet():
    assert "naming them for the first time" in _classify(existing=[])


def test_a_truncated_sample_budget_is_disclosed_to_the_agent():
    """An agent that believes it saw everything reports confidence it has not
    earned."""
    assert "sample budget was reached" not in _classify(truncated=False)
    text = _classify(truncated=True)
    assert "sample budget was reached" in text
    assert "low confidence" in text


def test_classify_files_every_file_and_says_when_it_is_done():
    # Placed or left out with a why -- never silently dropped -- and finished
    # by the tool's own count, not by the model's say-so.
    text = _classify()
    assert "probe-backfill-plan status" in text and "0 undecided" in text


def test_classify_asks_for_its_doubts_because_that_is_what_gets_reviewed():
    text = _classify()
    assert "--low" in text
    assert "person checks first" in text


@pytest.mark.parametrize("which", ["classify", "assign", "revise"])
def test_no_filing_prompt_asks_the_model_to_copy_paths_back(which):
    """A model cannot be trusted to copy data (2026-10-25: two mistyped
    random-hex names out of 10,537 rows refused a whole plan). It SELECTS with
    `probe-backfill-plan`; nothing in its answer is read."""
    text = {
        "classify": _classify,
        "assign": lambda: bp.assign_chunk(root=ROOT, evidence_jsonl="{}", projects="  a", index=1,
                                          total=2, work_dir="/w"),
        "revise": lambda: bp.revise(feedback="f", root=ROOT, work_dir="/w", resumed=False,
                                    plan_view="    a/  ->  x  (1 file)"),
    }[which]()
    assert "probe-backfill-plan assign" in text
    assert "nothing you write there is read" in text
    for echo in ("verbatim", "exactly once", '"assignments"', '"left_out"'):
        assert echo not in text, echo


def test_tail_files_must_name_what_decided_them():
    text = _classify()
    assert "TAIL FILES INHERIT" in text
    assert "guess wearing a rule's clothes" in text


def test_classify_carries_the_evidence_verbatim():
    assert '{"path":"zz.py","tier":"tail"}' in _classify(
        evidence_jsonl='{"path":"zz.py","tier":"tail"}'
    )


# -- import a unit -----------------------------------------------------------


def test_the_unit_prompt_pins_the_project_and_forbids_creating_one():
    text = _import(project="esm3-baseline")
    assert "esm3-baseline" in text
    assert "do not create any project" in text


def test_the_unit_prompt_lists_exactly_its_own_files():
    text = _import(paths=["michael/train.py", "shared/rows.csv"])
    assert "michael/train.py" in text and "shared/rows.csv" in text
    assert "and only these, are yours" in text


def test_the_unit_agent_uploads_nothing_and_writes_no_upload_list():
    """Code writes every file of the unit onto the upload list before the agent
    starts; the agent only says what the files are."""
    text = _import()
    assert "THEY ARE ALREADY ON THE UPLOAD LIST" in text
    assert "probe-backfill-plan note --file" in text
    assert "probe artifact add" not in text.split("HOW THIS RUN DIFFERS", 1)[0]


def test_a_file_with_nothing_to_say_is_imported_all_the_same():
    text = _import()
    assert "needs none: it is imported all the same" in text


def test_units_are_told_not_to_write_project_notes():
    text = _import()
    assert "Do NOT write the project's notes" in text
    assert "once, at the end" in text


def test_the_unit_prompt_reports_its_own_row_count():
    assert "2 files" in _import(paths=["a", "b"])


# -- map w&b -----------------------------------------------------------------


def test_wandb_mapping_prefers_projects_that_already_exist():
    text = bp.map_wandb(inventory="{}", projects=["odyssey-infill-v3"])
    assert "already exist" in text and "odyssey-infill-v3" in text
    assert "prefer them, strongly" in text


def test_wandb_mapping_warns_against_splitting_one_line_of_research():
    text = bp.map_wandb(inventory="{}", projects=["a"])
    assert "splits one line of research in half" in text


def test_wandb_mapping_handles_having_no_projects_yet():
    assert "(none yet)" in bp.map_wandb(inventory="{}", projects=[])


def test_wandb_mapping_carries_the_inventory():
    assert '{"entity":"anthrogen"}' in bp.map_wandb(inventory='{"entity":"anthrogen"}', projects=[])


# -- project-level visible summary and hidden notes --------------------------


def test_the_project_writer_uses_visible_markdown_and_append_only_hidden_notes():
    text = bp.write_notes(project="p", root=ROOT, landed=10, manifests=["/tmp/a.jsonl"])
    assert "block INSIDE the Overview" in text and "AI writer may not rewrite" in text
    assert "probe project set p --summary @PROJECT.md" in text
    assert "probe notes checkout --project p" in text
    assert "probe notes push --project p" in text
    assert "hidden notes" in text


def test_the_notes_writer_gets_the_manifests_so_it_knows_what_landed():
    text = bp.write_notes(
        project="p", root=ROOT, landed=3, manifests=["/tmp/a.jsonl", "/tmp/b.jsonl"]
    )
    assert "/tmp/a.jsonl" in text and "/tmp/b.jsonl" in text


def test_the_notes_writer_is_asked_for_gaps_not_just_a_summary():
    text = bp.write_notes(project="p", root=ROOT, landed=3, manifests=[])
    assert "Be honest about gaps" in text
    assert "trust caveats" in text


def test_visible_markdown_edit_is_read_preserve_write_verify():
    text = bp.write_notes(project="p", root=ROOT, landed=3, manifests=[])

    assert text.count("probe project get p") == 2
    assert "document" in text
    assert "preserve useful existing sections" in text
    assert "last-write-wins" in text
    assert "block INSIDE the Overview" in text
    # ...and that the verification is a CONTAINS check, not byte equality:
    # the read answers from the page, which renders the document, so an
    # agent chasing a byte match rewrites a degraded copy every cycle.
    assert "CONTAINS what you meant" in text


def test_the_notes_writer_names_the_files_that_matter_because_files_carry_no_notes():
    """Files no longer carry notes, so the import's per-file lines reach the
    record only through the project's documentation -- the few files a teammate
    would look for, not an inventory."""
    text = bp.write_notes(project="p", root=ROOT, landed=3, manifests=[])
    assert "Files carry no notes of their own" in text
    assert "do not list every file" in text
    assert "already carry their own" not in text


def test_no_import_prompt_puts_a_description_on_the_upload():
    """The manifest's "notes" is the project writer's input and never uploaded;
    no prompt tells an agent to pass `--notes` to `artifact add`."""
    from probe.cli import backfill

    for text in (
        _import(),
        bp.DESCRIBE_ARTIFACTS,
        backfill.build_prompt(folder=Path(ROOT), census=backfill.Census(files=1, bytes=1)),
    ):
        assert "--notes" not in text
    assert "never uploaded" in _import()


# -- no prompt names a door that does not open -------------------------------


@pytest.mark.parametrize(
    "text",
    [
        _classify(),
        bp.assign_chunk(root=ROOT, evidence_jsonl="{}", projects="  a", index=1, total=2, work_dir="/w"),
        bp.revise(feedback="f", root=ROOT, work_dir="/w", resumed=True, plan_view="    a/  ->  x"),
        _import(),
        bp.map_wandb(inventory="{}", projects=["a"]),
        bp.write_notes(project="p", root=ROOT, landed=1, manifests=[]),
    ],
)
def test_every_probe_command_named_in_a_prompt_actually_exists(text):
    """A prompt that names a verb the CLI does not have sends an unattended
    agent into a retry loop it cannot get out of.

    THE SWITCH SKILL IS ALSO CALLED `probe`, and that collision is why the match
    is anchored. A prompt saying `/probe full` or `$probe read-only` is naming a
    SKILL and its argument, not the binary and a subcommand -- `probe full` is
    not a CLI command and never will be. A leading `/`, `$` or `:` is unambiguous
    (the CLI is never invoked that way, and `:` covers pi's `/skill:probe`), so
    those occurrences are skipped and everything else stays exactly as strict as
    it was.

    Anchoring on a word boundary rather than stripping the prefix keeps the real
    case covered: `run probe full` in prose would still fail, because that IS
    someone telling an agent to run a command that does not exist.
    """
    import re

    from typer.main import get_command

    from probe.cli.main import app

    known = set(get_command(app).commands)
    for verb in set(re.findall(r"(?<![/$:\w-])probe ([a-z][a-z-]*)", text)):
        assert verb in known, f"prompt names `probe {verb}`, which does not exist"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("/probe full", []),
        ("$probe read-only", []),
        ("/skill:probe full", []),
        ("probe session status", ["session"]),
        ("run probe full now", ["full"]),
        ("`probe project create`", ["project"]),
    ],
)
def test_the_drift_guard_tells_the_skill_from_the_binary(text, expected):
    """Pinning the anchor, because the collision it handles is permanent.

    The switch skill and the CLI share the name `probe`, so the skill text says
    `/probe full` in prose that the guard above scans. `probe full` is not a CLI
    command and never will be, and before the anchor that read as drift and
    failed CI on a prompt that was perfectly correct.

    The last two cases are the ones that must NOT be skipped: an unprefixed
    `probe <verb>` is someone telling an agent to run a command, which is
    exactly what the guard exists to check.
    """
    import re

    assert sorted(re.findall(r"(?<![/$:\w-])probe ([a-z][a-z-]*)", text)) == sorted(expected)
