"""one classification turn: a JSON pass or a filing tool session, cached and retried, read back into a Plan of walked files."""

from __future__ import annotations

import contextlib
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path

from ... import folder as bf
from . import plan as plan_mod
from . import plan_tool as tool_mod
from ...agent_settings import AgentSettings, Lane, cached, launch_kwargs
from probe.foundation.compat.compat import StrEnum

#: The classify pass gets its own, larger deadline: it reads the whole evidence
#: set in one turn and there is exactly one of it.
CLASSIFY_TIMEOUT_S = 90 * 60


def _usable_pass(data: dict, key: str, *, empty_ok: bool = False) -> bool:
    rows = data.get(key)
    if not isinstance(rows, list):
        return False
    if key == "projects":
        # Empty is a full answer only when the folder's own projects hold all
        # of its work (`name_projects` is told so).
        return (empty_ok and not rows) or any(isinstance(row, dict) and row.get("slug")
                                              for row in rows)
    if key == "assignments":
        # A slice that is ALL left out (a web app's source) is a real answer.
        return any(isinstance(row, dict) and (row.get("path") or row.get("dir"))
                   for row in rows) or bool(plan_mod.parse_left_out(data.get("left_out")))
    return bool(rows) and all(isinstance(row, dict) for row in rows)

#: Attempts per chunked pass. A pass is a whole agent turn over a slice, and
#: the failures that hit it are overwhelmingly transient -- a dropped
#: connection, a turn that ended in prose without its closing JSON. Losing a
#: forty-slice run to one of those, after an hour of successful slices, is the
#: expensive outcome; a second attempt costs one slice.
PASS_ATTEMPTS = 2


def _run_pass(
    folder: Path, prompt: str, *, agent: bf.Agent, heading: str, work_dir: Path,
    total: int, stream=None, key: str, attempts: int = PASS_ATTEMPTS,
    agents: AgentSettings | None = None, empty_ok: bool = False,
) -> tuple[dict | None, str]:
    """One agent turn that answers with JSON. Returns ``(object, detail)``.

    The DETAIL is returned, not swallowed. Discarding it and substituting
    "slice 3 of 9 could not be read" hid every message worth acting on --
    "`claude` is not on PATH", the parenthesis-in-path refusal, "the agent did
    not finish in time" -- behind a sentence naming only where it happened.

    Each chunked pass gets its OWN session. They are deliberately independent --
    that is the whole design -- so sharing one would reintroduce the carry-over
    the chunking exists to avoid, and would put the earlier chunks' evidence
    back in the context that has to hold the later ones. A retry is a fresh
    session for the same reason.
    """
    phase = {"findings": "survey", "projects": "name", "assignments": "assign"}.get(key, key)
    _classification_progress(heading, phase)
    progress = _read_progress.get()
    if progress is not None:
        progress.begin(phase, heading)
    cache = _classification_cache_path(
        work_dir, agent=agent, prompt=prompt, phase=phase, extra={"key": key},
    )
    saved = _read_classification_cache(cache)
    if saved is not None and _usable_pass(saved, key, empty_ok=empty_ok):
        cached(agents, Lane.CLASSIFY)
        _classification_progress(heading, phase, cached=True)
        if progress is not None:
            progress.finish(phase, heading, success=True, cached=True)
        return saved, ""
    detail = ""
    for attempt in range(max(1, attempts)):
        if progress is not None and progress.cancelled.is_set():
            return None, "scan cancelled"
        ok, tail = bf.launch_agent(
            folder, prompt, agent=agent, workdir=work_dir, heading=heading,
            # The whole evidence sample is already in the prompt. Extra
            # tool reads are activity, not a count of files classified.
            total=0, timeout=CLASSIFY_TIMEOUT_S, stream=stream,
            session_id=new_session_id() if agent is bf.Agent.CLAUDE else None,
            paint_to=progress.activity(phase, heading) if progress is not None else None,
            cancel_event=progress.cancelled if progress is not None else None,
            **launch_kwargs(agents, Lane.CLASSIFY),
        )
        last = tail.splitlines()[-1] if tail.strip() else "no output"
        if ok:
            # Last wins: an agent that restates its answer means the later one.
            found = None
            for line in tail.splitlines():
                if key not in line:
                    continue
                for data in bf._embedded_summaries(line.strip(), key=key):
                    found = data
            if found is not None:
                usable = _usable_pass(found, key, empty_ok=empty_ok)
                if usable:
                    _write_classification_cache(cache, found)
                if progress is not None:
                    progress.finish(phase, heading, success=usable)
                return found, ""
            detail = f"answered without a usable `{key}` object ({last})"
        else:
            detail = last
        if attempt + 1 < max(1, attempts):
            detail += "  (retried)"
    if progress is not None:
        progress.finish(phase, heading, success=False)
    return None, detail


# -- filing by selection -------------------------------------------------------
#
# Every pass that decides where files go -- single-shot classify, one chunked
# slice, a reviewer's correction -- is ONE agent session with
# `probe-backfill-plan` on its PATH. The result is read from that session's
# decisions log, replayed through the tool's own `apply` against the reference
# THIS process holds, never parsed out of the agent's reply: the agent selects,
# code keeps the data. See `backfill_plan_tool` for why.

#: A session that decided at least this share of its files is kept, and the
#: rest follow their neighbours, as `missing` files always have. Below it the
#: session counts as failed: inheriting most of a slice from its neighbours is a
#: guess at scale, so those files are excluded and wait for the next run.
INHERIT_FLOOR = 0.8


class SessionOutcome(StrEnum):
    COMPLETE = "complete"
    INCOMPLETE = "incomplete"
    FAILED = "failed"


@dataclass
class ToolPass:
    """One filing session, as the log says it went."""

    ref: tool_mod.Reference
    state: tool_mod.State
    outcome: SessionOutcome
    detail: str = ""
    refused: int = 0
    session: str | None = None
    tail: str = ""

    @property
    def undecided(self) -> list[str]:
        return [f for f in self.ref.files if f not in self.state.decided]


#: What a retry is told. The log survives a dead turn, so a retry continues
#: the slice rather than starting it over.
CONTINUE_NOTE = """

SOME OF THIS IS ALREADY DONE. An earlier attempt filed part of it before it
stopped, and those decisions are kept. Run `probe-backfill-plan status` first
and file only what it lists as undecided."""


def _plan_state(work_dir: Path, key: str) -> bf.PlanTool:
    """Where one session's state lives.

    The reference sits BESIDE the work dir, not in it: the agent may write
    anywhere in its work dir, and the list it is checked against must not be
    one of those places. The log sits IN it, because Codex's sandbox confines
    the tool's writes as well as the agent's.
    """
    return bf.PlanTool(
        ref_dir=work_dir.parent / f"{work_dir.name}.plan-ref" / key,
        log=work_dir / "plan" / key / "decisions.jsonl",
    )


def _outcome(ref: tool_mod.Reference, state: tool_mod.State) -> SessionOutcome:
    # Over the files this session had to DECIDE: ones imported before arrive
    # decided, and counting them would pass a session that filed nothing.
    files = [f for f in ref.files if not ref.is_fixed(f)]
    total = len(files)
    decided = sum(1 for f in files if f in state.decided)
    if decided == total:
        return SessionOutcome.COMPLETE
    if decided and decided / total >= INHERIT_FLOOR:
        return SessionOutcome.INCOMPLETE
    return SessionOutcome.FAILED


def _run_tool_pass(
    folder: Path,
    prompt: str,
    ref: tool_mod.Reference,
    *,
    agent: bf.Agent,
    work_dir: Path,
    heading: str,
    phase: str,
    key: str,
    stream=None,
    attempts: int = PASS_ATTEMPTS,
    session_id: str | None = None,
    resume: str | None = None,
    revision: bool = False,
    board: tuple[Path, int, int] | None = None,
    agents: AgentSettings | None = None,
) -> ToolPass:
    """Run one filing session (retrying once) and read what it decided.

    The outcome comes from VALIDATED DECISIONS, never from the exit code: an
    agent that could not reach the tool can explain itself and exit 0, and a
    session that decided nothing has failed however it ended.

    `revision` sessions start from a seeded plan, so "every file decided" is
    true before they begin; theirs succeeds when it changed something.
    """
    _classification_progress(heading, phase)

    def done(state: tool_mod.State) -> bool:
        return state.accepted > 0 if revision else _outcome(ref, state) is SessionOutcome.COMPLETE

    def judged(state: tool_mod.State) -> SessionOutcome:
        if not revision:
            return _outcome(ref, state)
        # A revision that changed something is kept whatever share of the
        # folder it touched: its undecided files are the ones the reviewed
        # plan had left to inheritance or exclusion, and they stay that way.
        if state.accepted == 0:
            return SessionOutcome.FAILED
        decided = all(f in state.decided for f in ref.files)
        return SessionOutcome.COMPLETE if decided else SessionOutcome.INCOMPLETE

    cache = _classification_cache_path(
        work_dir, agent=agent, prompt=prompt, phase=phase, extra={"plan_tool": key},
    )
    saved = _read_classification_cache(cache)
    if saved is not None and isinstance(saved.get("ops"), list):
        state = tool_mod.replay(ref, saved["ops"])
        if done(state):
            cached(agents, Lane.CLASSIFY)
            _classification_progress(heading, phase, cached=True)
            progress = _read_progress.get()
            if progress is not None:
                progress.begin(phase, heading)
                progress.finish(phase, heading, success=True, cached=True)
            return ToolPass(ref, state, judged(state),
                            session=saved.get("session") if isinstance(saved.get("session"), str) else None,
                            tail=saved.get("tail") if isinstance(saved.get("tail"), str) else "")

    with (_ReadProgress(*board, stream) if board and _read_progress.get() is None else contextlib.nullcontext()):
        return _launch_tool_pass(
            folder, prompt, ref, agent=agent, work_dir=work_dir, heading=heading, phase=phase,
            key=key, stream=stream, attempts=attempts, session_id=session_id, resume=resume,
            revision=revision, done=done, judged=judged, cache=cache, agents=agents,
        )


def _launch_tool_pass(folder, prompt, ref, *, agent, work_dir, heading, phase, key, stream,
                      attempts, session_id, resume, revision, done, judged, cache,
                      agents=None) -> ToolPass:
    """The launching half of `_run_tool_pass`, once no cached result applies.

    The state is THIS call's: a fresh log per invocation, so a retry inside the
    call continues the slice while a later run starts clean. Reuse across runs
    is the prep cache's job, under the identity that proves the files did not
    change (`classification_context`).
    """
    progress = _read_progress.get()
    if progress is not None:
        progress.begin(phase, heading)
    state_paths = _plan_state(work_dir, f"{key}-{uuid.uuid4().hex[:8]}")
    ref.write(state_paths.ref_dir)
    state_paths.log.parent.mkdir(parents=True, exist_ok=True)

    detail = ""
    tail = ""
    session = resume or session_id
    state = tool_mod.replay(ref, tool_mod.read_log(state_paths.log))
    for attempt in range(max(1, attempts)):
        if progress is not None and progress.cancelled.is_set():
            detail = "scan cancelled"
            break
        # Files imported before arrive DECIDED (their project is kept), so a
        # session of only those is "complete" before it starts -- but it exists
        # to name their experiments and runs, which only the agent can do.
        if done(state) and (attempt or not ref.fixed or state.accepted):
            break
        text = prompt + (CONTINUE_NOTE if state.accepted and not revision else "")
        if attempt == 0:
            use_resume, use_session = resume, (None if resume else session_id)
        else:
            use_resume, use_session = None, (new_session_id() if agent is bf.Agent.CLAUDE else None)
        # A refused setting relaunches under a fresh session (`launch_agent`):
        # that one holds the evidence a revision resumes, not the refused one.
        relaunched: list[str | None] = []
        with bf.plan_tool_launcher(state_paths) as bin_dir:
            ok, tail = bf.launch_agent(
                folder, text, agent=agent, workdir=work_dir, heading=heading,
                # The whole evidence sample is already in the prompt. Extra
                # tool reads are activity, not a count of files classified.
                total=0, timeout=CLASSIFY_TIMEOUT_S, stream=stream,
                session_id=use_session, resume=use_resume,
                paint_to=progress.activity(phase, heading) if progress is not None else None,
                cancel_event=progress.cancelled if progress is not None else None,
                path_prepend=bin_dir,
                on_relaunch=relaunched.append,
                **launch_kwargs(agents, Lane.CLASSIFY),
            )
        if relaunched:
            use_resume, use_session = None, relaunched[-1]
        session = use_resume or use_session or session
        state = tool_mod.replay(ref, tool_mod.read_log(state_paths.log))
        last = tail.splitlines()[-1] if tail.strip() else "no output"
        detail = "" if ok else last
        if not ok and attempt + 1 < max(1, attempts):
            detail += "  (retried)"

    # The reference is only for the session's own calls; the log stays as the
    # record of what was decided (and is small), the reference may be a 10 MB
    # file list.
    shutil.rmtree(state_paths.ref_dir, ignore_errors=True)
    outcome = judged(state)
    if revision and outcome is SessionOutcome.FAILED:
        detail = detail or "the agent changed nothing"
    elif outcome is SessionOutcome.FAILED and not detail:
        detail = (f"filed {len(ref.files) - len([f for f in ref.files if f not in state.decided]):,} "
                  f"of {len(ref.files):,} files")
    # Not for a session over files imported before whose agent failed before
    # choosing anything: decided from the start, it would cache as finished,
    # and the next import would replay the failure instead of asking again.
    if done(state) and not (ref.fixed and not state.accepted and detail):
        _write_classification_cache(cache, {"ops": tool_mod.read_log(state_paths.log),
                                            "session": session, "tail": tail})
    if progress is not None:
        progress.finish(phase, heading, success=outcome is not SessionOutcome.FAILED)
    return ToolPass(ref, state, outcome, detail=detail,
                    refused=tool_mod.refused_count(state_paths.log), session=session, tail=tail)


def _plan_from_passes(
    passes: list[ToolPass], specs: list[plan_mod.ProjectSpec], *, summary: str = "",
) -> plan_mod.Plan:
    """A `Plan` of walked FILES, from what each session validly decided.

    File-level on purpose: no `dir` row reaches `resolve`, so no prefix
    expansion can let one session's directory claim a file another owns. A
    failed session's undecided files become `excluded` -- not missing, never
    inherited -- while an incomplete one's follow their neighbours.
    """
    assignments: list[plan_mod.Assignment] = []
    left_out: list[plan_mod.LeftOut] = []
    excluded: list[str] = []
    unsure: list[str] = []
    declared: dict[str, dict] = {}
    experiments: dict[str, dict] = {}
    runs: dict[str, dict] = {}
    stats = {"refused_selectors": 0, "invalid_decisions": 0, "undecided_files": 0,
             "incomplete_sessions": 0, "failed_sessions": 0, "unclassified_files": 0}
    for got in passes:
        stats["refused_selectors"] += got.refused
        stats["invalid_decisions"] += got.state.invalid
        for path, decision in got.state.decided.items():
            if decision.kind is tool_mod.Kind.LEFT_OUT:
                left_out.append(plan_mod.LeftOut(path=path, why=decision.why))
            else:
                assignments.append(plan_mod.Assignment(
                    path=path, project=decision.project or "",
                    confidence="low" if decision.low else "high", why=decision.why,
                ))
        undecided = got.undecided
        if got.outcome is SessionOutcome.FAILED:
            stats["failed_sessions"] += 1
            stats["unclassified_files"] += len(undecided)
            excluded.extend(undecided)
        elif got.outcome is SessionOutcome.INCOMPLETE:
            stats["incomplete_sessions"] += 1
            stats["undecided_files"] += len(undecided)
        unsure.extend(got.state.unsure)
        declared.update(got.state.declared)
        # A slice that names an experiment again for the SAME folder names the
        # same one (later wins, as for declared projects). Two slices that chose
        # one slug for DIFFERENT folders made two experiments: the later one
        # gets a numbered slug, and its own runs follow it.
        renamed: dict[str, str] = {}
        for slug, spec in got.state.experiments.items():
            final = slug
            n = 1
            while final in experiments and experiments[final].get("under") != spec.get("under"):
                n += 1
                suffix = f"-{n}"
                final = slug[:63 - len(suffix)] + suffix
            renamed[slug] = final
            experiments[final] = {**spec, "slug": final}
        for under, spec in got.state.runs.items():
            runs[under] = ({**spec, "experiment": renamed.get(spec["experiment"], spec["experiment"])}
                           if spec.get("experiment") else dict(spec))
    # A declaration wins over the spec it names: a correction may rename or
    # re-describe a project as well as add one.
    def spec(slug: str, d: dict) -> plan_mod.ProjectSpec:
        if d.get("reuse"):
            # A checked selection of an existing project: code fills its name
            # and marks it EXISTING (`backfill_projects.settle`).
            return plan_mod.ProjectSpec(slug=slug, name=slug, origin=plan_mod.Origin.MODEL.value)
        return plan_mod.ProjectSpec(slug=slug, name=d.get("name") or slug,
                                    description=d.get("description") or "", tags=list(d.get("tags") or []))

    known = {s.slug for s in specs}
    projects = [spec(s.slug, declared[s.slug]) if s.slug in declared else s for s in specs] + [
        spec(slug, d) for slug, d in declared.items() if slug not in known
    ]
    return plan_mod.Plan(
        projects=projects, assignments=assignments, unsure=list(dict.fromkeys(unsure)),
        summary=summary, left_out=left_out, excluded=sorted(set(excluded)), stats=stats,
        experiments=experiments, runs=runs,
    )
from probe.cli.imports.folder.classify.classify import new_session_id  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.folder.classify.context import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _ReadProgress,
    _classification_cache_path,
    _classification_progress,
    _read_classification_cache,
    _read_progress,
    _write_classification_cache,
)
