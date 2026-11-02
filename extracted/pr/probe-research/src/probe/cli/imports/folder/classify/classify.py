"""run the classification agent over a folder and revise its plan from a reviewer's correction."""

from __future__ import annotations
import hashlib
import json
import uuid
import functools
from pathlib import Path

from ... import folder as bf
from probe.cli.imports.folder import evidence as evidence_mod
from . import plan as plan_mod
from . import plan_tool as tool_mod
from ..agents import prompts as prompts
from ...agent_settings import AgentSettings


def new_session_id() -> str:
    """A session id Claude Code will accept.

    `str(uuid4())`, NOT `uuid4().hex`. `--session-id` validates the DASHED
    canonical form and rejects the 32-char hex with "Invalid session ID. Must be
    a valid UUID" -- which kills the agent before it reads a single file, so the
    classify pass returns no plan and the import stops having done nothing.

    Caught by the first real end-to-end run and by nothing before it: every test
    fakes `launch_agent`, so the id never reached the binary that validates it.
    """
    return str(uuid.uuid4())


@functools.lru_cache(maxsize=8)
def _git_note(folder: Path, work_dir: Path) -> str:
    """The GIT_HISTORY prompt fragment for this run, or "".

    Cached so the digest is written once per (folder, work_dir) however many
    prompts ask for it; best-effort because an import must never fail over a
    broken .git directory.
    """
    authorized = work_dir / "github-context.txt"
    extra = ""
    try:
        if authorized.is_file() and authorized.stat().st_size <= 128 * 1024:
            extra = "\n\n" + authorized.read_text(encoding="utf-8")
    except OSError:
        pass
    try:
        context = bf.git_context(folder)
        if context is None:
            return extra
        history = bf.write_git_history(context, work_dir)
        if history is None:
            return extra
        return prompts.git_history(
            history_path=str(history), repo=context.repo, branch=context.branch
        ) + extra
    except Exception:
        return extra


def classify(
    folder: Path,
    ev: evidence_mod.Evidence,
    *,
    agent: bf.Agent,
    existing: list[str],
    work_dir: Path,
    stream=None,
    agents: AgentSettings | None = None,
    fixed: dict[str, str] | None = None,
    own=(),
) -> tuple[plan_mod.Plan | None, str, str | None]:
    """Run the classification agent. Returns ``(plan, tail, session_id)``.

    `fixed` names files imported before (path -> their project): the agent
    sees them already decided and may only name experiments and runs over
    them (`backfill_structure.restructure_candidates`).

    `own` is this folder's own projects (`ProjectSpec`s code chose,
    `backfill_projects.load`): files may go into them without a declaration.
    `existing` is every OTHER project's slug: never a destination by being
    named, only through a checked `project --reuse` a person confirms.

    `agents` carries the import's settings and meter to every launch in the
    `classify` lane (`import_agent_settings`); without it, launches are as
    they always were.

    The session comes back so the review gate can RESUME it to apply a
    correction. That is the difference between a revision costing one turn and
    costing the whole folder again: the evidence is already in that session's
    context. `None` for Codex, which has no resume here, and the caller falls
    back to a cold re-classify that carries the correction in its prompt.

    Batched by construction rather than by chunking the evidence: the prompt
    carries the whole evidence set and `--autocompact auto` handles the rest.
    The one thing that must not happen quietly is compaction eating the evidence
    mid-decision, so :func:`probe.cli.imports.folder.agents.prompts.classify` is told when
    the sample budget truncated the input and instructs the agent to mark those
    placements low confidence.
    """
    jsonl = evidence_mod.to_jsonl(ev)
    if evidence_mod.needs_chunking(ev):
        # TOO BIG FOR ONE PROMPT. Not a slow path -- a rejected one: the whole
        # evidence set is a single message, so `--autocompact` cannot help
        # (it compacts across TURNS and there are none yet) and the request
        # fails outright. The chunked route is a genuinely different shape,
        # so it lives in its own function; see `classify_chunked`.
        #
        # Single-shot stays the DEFAULT because it is the better
        # classification when it is possible: every file judged against every
        # other, in one decision, with no summary in between.
        plan, tail = classify_chunked(
            folder, ev, agent=agent, existing=existing,
            work_dir=work_dir, stream=stream, agents=agents, fixed=fixed, own=own,
        )
        # No session to hand back: the chunked route runs many, and resuming
        # "the" one would resume whichever ran last. A correction after this is
        # one fresh session that starts from the plan (`revise`).
        return plan, tail, None

    from .. import structure as structure_mod

    fixed = fixed or {}
    own_slugs = [spec.slug for spec in own]
    others = [slug for slug in existing if slug not in own_slugs]
    files = tuple(plan_mod.relative_paths(ev))
    prompt = prompts.classify(
        root=folder,
        evidence_jsonl=jsonl,
        existing=others,
        truncated=ev.sample_budget_hit,
        work_dir=str(work_dir),
        mtime_uninformative=ev.mtime_uninformative,
        imported=len(fixed),
        own=_own_pairs(own),
        candidates=prompts.run_candidates(structure_mod.run_candidates(files)),
    ) + _git_note(folder, work_dir)
    heading = f"Reading {folder.name} — {ev.total_files:,} files"
    ref = tool_mod.Reference(
        root=str(folder), mode=tool_mod.Mode.CLASSIFY,
        files=files, projects=tuple(dict.fromkeys([*own_slugs, *fixed.values()])),
        existing=tuple(dict.fromkeys([*others, *own_slugs])),
        **_fixed_seed(files, fixed),
    )
    got = _run_tool_pass(
        folder, prompt, ref, agent=agent, work_dir=work_dir, heading=heading,
        phase="classify", key=_session_key("classify", 0, ref), stream=stream,
        session_id=new_session_id() if agent is bf.Agent.CLAUDE else None,
        board=(folder, ev.total_files, 0), agents=agents,
    )
    if not got.state.decided or (fixed and not got.state.accepted and got.detail):
        # Nothing decided -- or, over files imported before (decided from the
        # start), an agent that failed before naming anything: no plan, so
        # the next import tries again instead of settling on an empty one.
        return None, got.detail or got.tail, got.session
    plan = _plan_from_passes([got], [], summary=_final_message(got.tail))
    plan.fixed = dict(fixed)
    return plan, got.tail, got.session


#: The decision a file imported before is seeded with: its own project.
IMPORTED_WHY = "already imported"


def _own_pairs(own) -> list[tuple[str, str]]:
    """This folder's own projects as the prompts list them: slug, name and why."""
    return [(spec.slug, f"{spec.name or spec.slug} ({spec.reason})" if spec.reason
             else (spec.name or spec.slug)) for spec in own]


def _fixed_seed(files, fixed: dict[str, str]) -> dict:
    """`Reference` keyword arguments pinning the already-imported `files`."""
    mine = [f for f in files if f in fixed]
    return {
        "fixed": tuple(mine),
        "seed": {f: {"kind": tool_mod.Kind.ASSIGNED.value, "project": fixed[f],
                     "why": IMPORTED_WHY} for f in mine},
    }


def _session_key(phase: str, index: int, ref: tool_mod.Reference, salt: str = "") -> str:
    """Stable for the same files, projects and seed; new when any of them moves.

    A re-run over an unchanged slice finds its own log and continues it; a
    slice whose evidence changed starts clean instead of replaying decisions
    made about different files.
    """
    digest = hashlib.sha256((ref.to_json() + "\0" + salt).encode()).hexdigest()[:12]
    return f"{phase}-{index:03d}-{digest}"


def _final_message(tail: str) -> str:
    """The agent's closing sentence, for the review screen. Never a decision."""
    for line in reversed(tail.splitlines()):
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict):
            continue
        text = event.get("result") if event.get("type") == "result" else None
        item = event.get("item") if isinstance(event.get("item"), dict) else None
        if text is None and item is not None and item.get("type") == "agent_message":
            text = item.get("text")
        if isinstance(text, str) and text.strip():
            last = [ln.strip() for ln in text.strip().splitlines() if ln.strip()][-1]
            return last[:300]
    return ""


def revise(
    folder: Path,
    ev: evidence_mod.Evidence,
    feedback: str,
    *,
    agent: bf.Agent,
    session_id: str | None,
    work_dir: Path,
    plan: plan_mod.Plan,
    existing: list[str] = (),
    stream=None,
    agents: AgentSettings | None = None,
    own=(),
) -> tuple[plan_mod.Plan | None, str, str | None]:
    """Apply a reviewer's correction to `plan`. Returns ``(plan, tail, session)``.

    The plan's projects and this folder's `own` ones take files directly; any
    other existing project is selected with `project --reuse`, so "put these
    in the benchmark project" reaches it through a checked call.

    ONE session over the whole folder, whichever route classified it, seeded
    with the plan the reviewer read: every file already carries its decision,
    so the agent changes only what the correction reaches and nothing it does
    not mention can fall out of an answer. A chunked folder used to re-run every
    slice for a correction -- another hour on a 144k-file drive.

    Resumes the classifying session when there is one (single-shot Claude), so
    the evidence is still in context. The prompt never carries the evidence
    itself -- a chunked folder's does not fit -- but a compact view of the
    plan, and the tool's `show`/`status` to look closer.

    A failed revision returns no plan and the CALLER KEEPS THE OLD ONE. Losing
    a good-enough plan because the correction round-tripped badly would make
    typing anything at the gate a gamble, which is the opposite of the point.
    """
    # Seeded from what the reviewer SAW: `resolve`'s placements, inherited
    # files included. Seeding only the explicit assignments let a correction
    # that moved a directory's scripts re-inherit its untouched checkpoints
    # into a different project.
    left_out: dict[str, str] = {}
    shown, _ = plan_mod.resolve(ev, plan, left_out=left_out)
    why = {a.path: a for a in plan.assignments}
    seed: dict[str, dict] = {
        path: {"kind": tool_mod.Kind.LEFT_OUT.value, "why": reason or "left out"}
        for path, reason in left_out.items()
    }
    for path, project in shown.items():
        a = why.get(path)
        seed[path] = {"kind": tool_mod.Kind.ASSIGNED.value, "project": project,
                      "why": a.why if a else "placed with its neighbours",
                      "low": bool(a and a.confidence != "high")}
    own_slugs = [spec.slug for spec in own]
    projects = list(dict.fromkeys([*own_slugs, *(p.slug for p in plan.projects),
                                   *(a.project for a in plan.assignments),
                                   *plan.fixed.values()]))
    files = tuple(plan_mod.relative_paths(ev))
    pinned = _fixed_seed(files, plan.fixed)
    ref = tool_mod.Reference(
        root=str(folder), mode=tool_mod.Mode.REVISE,
        files=files, projects=tuple(projects), seed={**seed, **pinned["seed"]},
        fixed=pinned["fixed"], existing=tuple(dict.fromkeys([*existing, *own_slugs])),
        structure={"experiments": plan.experiments, "runs": plan.runs},
    )
    prompt = prompts.revise(
        feedback=feedback, root=folder, work_dir=str(work_dir),
        resumed=session_id is not None, plan_view=plan_view(plan),
        can_reuse=any(slug not in projects for slug in existing),
    )
    got = _run_tool_pass(
        folder, prompt, ref, agent=agent, work_dir=work_dir,
        heading=f"Revising the plan for {folder.name}", phase="revise",
        key=_session_key("revise", 0, ref, salt="\0".join(
            [feedback, session_id or "", hashlib.sha256(evidence_mod.to_jsonl(ev).encode()).hexdigest()])),
        stream=stream, attempts=1,
        resume=session_id,
        session_id=None if session_id else (new_session_id() if agent is bf.Agent.CLAUDE else None),
        revision=True, agents=agents,
    )
    if got.outcome is SessionOutcome.FAILED:
        return None, got.detail or got.tail, got.session
    revised = _plan_from_passes([got], list(plan.projects), summary=_final_message(got.tail) or plan.summary)
    # Files nobody has classified yet stay excluded unless the correction filed them.
    revised.excluded = sorted(set(plan.excluded) - set(got.state.decided))
    revised.fixed = dict(plan.fixed)
    return revised, got.tail, got.session
from probe.cli.imports.folder.classify.chunked import classify_chunked  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.folder.classify.passes import SessionOutcome, _plan_from_passes, _run_tool_pass  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.folder.classify.plan_view import plan_view  # noqa: E402 -- pieces need each other; the front door loads this one first
