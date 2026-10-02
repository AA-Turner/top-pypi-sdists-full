"""The routing doctrine is complete, on every surface that teaches it.

Two surfaces teach agents what goes where: the always-loaded pointer block
(`cli/agent_rules.POINTER_BODY`, one literal since 2026-09-13) and the
track-work skill markdown, which cannot import Python. Since 2026-09-17 the
block ROUTES to the skill instead of restating it, so the census here reads the
skill alone (the block's own contract is pinned in test_agent_rules.py) — and
it is a FEATURE census: every write surface the platform ships must be
taught, with the phrase an agent needs to actually use it.

The MCP instruction sheet was a third carrier until 2026-09-05 and is now
deliberately NOT one: everything the write doctrine prescribes is actioned
through the CLI/SDK, not the read-only MCP tools, and plugin users received
it twice (the pointer block is uncapped and always loaded). The sheet keeps
only tool relationships, the evidence guard, and the summary/notes data
contract — guarded by tests/test_mcp.py and test_mcp_description_budget.py,
not by the census here. The cost accepted: an MCP-with-CLI-but-no-plugin
session loses write prompting.

Why a census: the failure this repairs was measured, not imagined. A tenant's
agents wrote 140k characters of notes and uploaded zero files, because every
destination the prompts enumerated was prose — the artifact anchors existed,
worked, and were never mentioned where the agent could see them. A platform
feature with no prompt phrase is unreachable by an agent (the fence-shape
rule), so an unprompted feature IS a bug, and this test is where it fails.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

AGENT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(AGENT_ROOT / "src"))
from probe import doctrine  # noqa: E402


#: 0151 narrowed the offered vocabulary to four. Written out rather than
#: imported from the backend: the agent tree ships on its own release train
#: and must not silently follow a backend edit it has not been rebuilt for.
_KIND_VOCABULARY = {"training", "inference", "research", "general", "experiment"}


def _skill_text(name: str) -> str:
    """The skill as the MAIN AGENT reads it: a skill with `versions/` is its
    main-agent render (skill_versions), plus its other files."""
    import importlib.util

    root = AGENT_ROOT / "skills" / name
    spec = importlib.util.spec_from_file_location("_skill_versions", AGENT_ROOT / "src" / "probe" / "skill_versions.py")
    versions = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(versions)
    return "\n".join(
        versions.render(root, versions.MAIN_AGENT) if p.name == "SKILL.md" else p.read_text(encoding="utf-8")
        for p in sorted(root.glob("*.md"))
    )


def _rendered(constant: str, path: str) -> str:
    """A Python prompt surface, read from SOURCE rather than imported.

    Path-honest on purpose: in a worktree `import probe` can resolve to another
    checkout's editable install, and scoring that tree's words would pass a test
    about text the agents here never see.
    """
    text = (AGENT_ROOT / path).read_text(encoding="utf-8")
    m = re.search(constant + r' = """(.*?)"""', text, re.DOTALL)
    assert m, f"could not extract {constant} from {path}"
    return m.group(1)


#: The census surfaces. Since 2026-09-17 the pointer block ROUTES to the
#: track-work skill instead of restating its doctrine (it names the three doors
#: and when to read; the skill says what goes where), so the destination census
#: reads the skill alone. The block's own contract is pinned in
#: tests/test_agent_rules.py.
SURFACES = {
    "track-work": lambda: _skill_text("track-work"),
}
def POINTER() -> str:
    return _rendered("POINTER_BODY", "src/probe/cli/agent_rules.py")


def test_every_surface_names_every_core_destination() -> None:
    missing = []
    for surface, read in SURFACES.items():
        text = read()
        low = text.lower()
        for token in doctrine.CORE_DESTINATIONS:
            # Case-blind: the skill shouts "NEVER UPLOAD SECRETS".
            if token.lower() not in low:
                missing.append(f"{surface}: {token!r}")
    assert not missing, "doctrine drifted — destinations unnamed: " + "; ".join(missing)


def test_detail_destinations_reach_the_skill() -> None:
    missing = []
    text = SURFACES["track-work"]()
    for token in doctrine.DETAIL_DESTINATIONS:
        if token not in text:
            missing.append(f"track-work: {token!r}")
    assert not missing, "detail destinations unnamed: " + "; ".join(missing)


def test_the_four_load_bearing_rules_survive_on_every_surface() -> None:
    """The rules the Anthrogen investigation produced. Each is one sentence,
    and each dies silently if a surface drops it."""
    rules = {
        "files routed at all": "file",
        "consent, not curation": "everything is recorded",
        "the scope axis": "lowest entity",
        "the catch-all": "Drop nothing",
        "transcripts automatic": "Automatically tracked",
    }
    missing = []
    for surface, read in SURFACES.items():
        text = read()
        for label, phrase in rules.items():
            if phrase not in text:
                missing.append(f"{surface}: {label} ({phrase!r})")
    assert not missing, "load-bearing rule missing: " + "; ".join(missing)


# ---------------------------------------------------------------------------
# The feature census: every write surface the platform ships, and the phrase
# the skill must carry for an agent to reach it. Keyed by feature so a failure
# names what became unreachable, not just which string vanished.
# ---------------------------------------------------------------------------

_FEATURE_PHRASES: dict[str, tuple[str, ...]] = {
    # artifacts — all five anchors, byte and reference uploads
    "artifact: run anchor": ("probe artifact add RUN",),
    "artifact: experiment anchor": ("--experiment",),
    "artifact: project anchor": ("--project",),
    "artifact: personal workspace anchor": ("--workspace",),
    "artifact: team shared folder": ("--shared",),
    "artifact: reference instead of bytes": ("--reference",),
    "artifact: registry versions": ("version-add", 'view="versions"'),
    "artifact: producer lineage": ("probe edge", "produces"),
    "artifact: safety boundary": ("SECRETS", "credentials"),
    # numbers
    "metrics: curves": ("step=",),
    "metrics: dimensions vs labels": ("dimensions", "labels"),
    "metrics: declared aggregation": ('agg="mean"',),
    "metrics: derived": ("--derived", "producer"),
    "metrics: expression views": ("views create",),
    "metrics: shape assertions": ("run_series", "has_labeled_points"),
    "spans": ("run.span", "probe span add"),
    # prose
    # `--description` left every create/set verb in 0.171.0 (the server writes
    # the description once a run finishes); the skill says so instead.
    "description": ("description itself",),
    "question": ("--question",),
    # The authored Markdown is the researcher's by policy since 2026-09-17 (the
    # `--summary` flag still exists); the skill names the document and says whose it is.
    "visible Markdown": ("summary_markdown", "the RESEARCHER's - never write it"),
    "entity notes": ("notes checkout", "notes push"),
    "team note": ("probe-team-note.md", "`edit-notes`"),
    "group notes": ("group",),
    # runs and lifecycle
    "run open": ("run start",),
    "run close with status": ("run end", "--status"),
    "run claim gate": ("run check",),
    "run reproduce": ("run reproduce",),
    "experiment freeze": ("freeze",),
    "publishing": ("version create",),
    "external ids": ("--external-id", "probe link"),
    "tags, incl. invalid": ("--tag", "invalid"),
    "sub-runs": ("run child",),
    # inputs
    "snapshot": ("probe snapshot",),
    "snapshot includes": ("--include",),
    "snapshot verify": ("--verify-only",),
    "inputs decision record": ("inputs-decision.json",),
    # session and delivery
    "tracking switch": ("probe session status", "`/probe`"),
    "outbox": ("outbox status",),
    "dashboard url handback": ("End with the dashboard URL",),
}


def test_every_platform_write_feature_is_prompted_in_the_skill() -> None:
    text = _skill_text("track-work")
    missing = []
    for feature, phrases in _FEATURE_PHRASES.items():
        for phrase in phrases:
            if phrase not in text:
                missing.append(f"{feature}: {phrase!r}")
    assert not missing, (
        "platform features unreachable by prompt (fence-shape rule): "
        + "; ".join(missing)
    )


def test_the_status_skill_reads_and_never_writes() -> None:
    """visualize-progress renders state. Its NEXT line may NAME a write
    command for the researcher; the skill itself must stay declared read-only
    and keep every read the status block is derived from."""
    text = _skill_text("visualize-progress")
    for phrase in ("probe session status", "browse", "outbox status"):
        assert phrase in text, f"status skill lost its read: {phrase!r}"
    assert "Not a write" in text, "the read-only declaration is gone"
    assert "track-work" in text, "it must route the writes it surfaces to track-work"


def test_the_skill_never_names_a_removed_skill() -> None:
    removed = (
        "start-research-work",
        "track-research-work",
        "toggle-research-tracking",
        "capture-run-inputs",
        "show-research-timeline",
        # Renamed to visualize-progress; "status" collided with `probe session
        # status`, a CLI read the skill itself calls.
        "show-research-status",
    )
    for name in ("track-work", "visualize-progress", "instrument-training-runs"):
        text = _skill_text(name)
        for old in removed:
            assert old not in text, f"{name} names removed skill {old}"


def test_the_vocabulary_cannot_quietly_shrink() -> None:
    """The census iterates these tuples; an emptied tuple would disarm every
    assertion above with zero failures. Shrinking is a deliberate test edit."""
    assert len(doctrine.CORE_DESTINATIONS) >= 10
    assert len(doctrine.DETAIL_DESTINATIONS) >= 2


def test_no_skill_markdown_carries_an_arguments_line() -> None:
    """The guard reads a trailing `ARGUMENTS:` line as the invocation's
    direction. A doc line in an expanded skill body starting with it would
    re-arm bare invocations with whatever word follows."""
    for md in (AGENT_ROOT / "skills").rglob("*.md"):
        for i, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
            assert not line.startswith("ARGUMENTS:"), f"{md}:{i} starts with ARGUMENTS:"


def test_marketplace_description_names_only_live_skills() -> None:
    """The marketplace description is prose; this diff itself proved prose
    drifts (two plugin.json descriptions shipped stale). Pin it to disk."""
    import json

    desc = json.loads((AGENT_ROOT / ".claude-plugin" / "marketplace.json").read_text())
    text = json.dumps(desc)
    for removed in (
        "start-research-work",
        "track-research-work",
        "toggle-research-tracking",
        "capture-run-inputs",
        "show-research-timeline",
        # Renamed to visualize-progress; "status" collided with `probe session
        # status`, a CLI read the skill itself calls.
        "show-research-status",
    ):
        assert removed not in text, f"marketplace names removed skill {removed}"
    for live in ("track-work", "visualize-progress"):
        assert live in text, f"marketplace omits live skill {live}"
    for manifest in (
        AGENT_ROOT / "plugins" / "probe-research" / ".claude-plugin" / "plugin.json",
        AGENT_ROOT / "plugins" / "probe-research" / ".codex-plugin" / "plugin.json",
    ):
        body = manifest.read_text(encoding="utf-8")
        for stale in (
            "timeline",
            "start-research-work",
            "track-research-work",
            "show-research-status",
        ):
            assert stale not in body, f"{manifest.name} still says {stale!r}"


def test_every_skill_on_disk_is_counted_by_telemetry() -> None:
    """telemetry.RESEARCH_SKILLS is the one slug list nothing derived: an
    unlisted slug silently stops counting (the set's own comment). Census it
    against the skills directory, reading the hook file by path — the plugin
    hooks are stdlib-only and not importable as a package."""
    hook = (
        AGENT_ROOT / "plugins" / "probe-research" / "hooks" / "telemetry.py"
    ).read_text(encoding="utf-8")
    m = re.search(r"RESEARCH_SKILLS = \{(.*?)\}", hook, re.DOTALL)
    assert m, "could not extract RESEARCH_SKILLS"
    listed = set(re.findall(r'"([a-z0-9-]+)"', m.group(1)))
    on_disk = {d.name for d in (AGENT_ROOT / "skills").iterdir() if d.is_dir()}
    missing = on_disk - listed
    assert not missing, f"skills invisible to telemetry: {sorted(missing)}"


def test_subprojects_are_taught_where_a_new_project_gets_registered() -> None:
    """THE MEASURED FAILURE: four Odyssey-3 phase projects were registered as
    flat top-level siblings, by an agent with a CLI that had `--parent`, on the
    day the feature shipped. Nothing it could see said projects nest.

    `--parent` in the skill body was not enough: a skill is read only once
    SELECTED, while the decision "is this a new project or a phase of one?" is
    made at registration time from the always-loaded block. So the block keeps
    ONE line on it (restored 2026-09-17 after the rewrite dropped it), and the
    skill carries the kind vocabulary with its tie-breaks.
    """
    register = " ".join(POINTER().split())
    assert "SUBPROJECT of it (`project create --parent`), never a new top-level sibling" in register
    assert "(training|inference|research|general|experiment)" in register

    skill = " ".join(_skill_text("track-work").split())
    assert "A phase of a bigger effort is a SUBPROJECT of it, never a new top-level sibling" in skill
    for kind in _KIND_VOCABULARY:
        assert f"`{kind}`" in skill, kind
    assert "weights MOVE" in skill
    assert "A sweep is an experiment, not a project" in skill


def test_kind_vocabulary_is_identical_across_the_agent_tree() -> None:
    """0151 parity: CLI enum == generated SDK enum == pointer == skill.

    kinds.py:23 documents that the vocabulary has more copies than the parity
    tests pin. This is that gap closed on the AGENT side -- one narrowing that
    reaches four of the copies and misses the fifth ships a CLI whose own
    `--kind` values the server refuses. The MCP sheet stopped carrying the
    vocabulary in the 2026-09-15 rewrite (a project's `kind` arrives as DATA on
    every browse node), so the always-loaded copy is the pointer block.
    """
    from probe._generated.models import ProjectKind as GeneratedProjectKind
    from probe.cli.main import ProjectKind as CliProjectKind

    assert {k.value for k in CliProjectKind} == _KIND_VOCABULARY
    assert {k.value for k in GeneratedProjectKind} == _KIND_VOCABULARY
    assert "(training|inference|research|general|experiment)" in " ".join(POINTER().split())

    skill = " ".join(_skill_text("track-work").split())
    for kind in _KIND_VOCABULARY:
        assert f"| `{kind}` |" in skill, kind
    for retired in ("evaluation", "survey", "engineering"):
        assert f"--kind {retired}" not in skill, retired


