"""classify a folder too big for one prompt: survey slices, name projects, assign rows."""

from __future__ import annotations
import json
from concurrent.futures import ThreadPoolExecutor
from contextvars import copy_context
from pathlib import Path

from ... import folder as bf
from probe.cli.imports.folder import evidence as evidence_mod
from . import plan as plan_mod
from . import plan_tool as tool_mod
from ..structure import projects as projects_mod
from ..agents import prompts as prompts
from ...agent_settings import AgentSettings

#: How many assign slices run at once. Kept lower than the unit count on
#: purpose: a slice holds a 55k-token prompt, and this is the one phase where
#: every worker reads the same evidence set at the same time.
CLASSIFY_CONCURRENCY_DEFAULT = 3


def classify_concurrency() -> int:
    return _env_concurrency("PROBE_CLASSIFY_WORKERS", CLASSIFY_CONCURRENCY_DEFAULT)

# Survey calls are independent, but each has a full model context. Two at a
# time reduces waiting without increasing the context floor or request count.
SURVEY_CONCURRENCY = 2


def _classification_results(worker, numbered, *, workers):
    """Run independent slices; Ctrl-C cancels queued work before leaving."""
    pool = ThreadPoolExecutor(max_workers=max(1, min(workers, len(numbered))))
    futures = []
    try:
        # A Context cannot be entered by two threads simultaneously.
        futures = [pool.submit(copy_context().run, worker, pair) for pair in numbered]
        return sorted(future.result() for future in futures)
    except BaseException:
        progress = _read_progress.get()
        if progress is not None:
            progress.cancelled.set()
        for future in futures:
            future.cancel()
        bf.stop_all()
        raise
    finally:
        # Waiting before stopping the children strands Ctrl-C behind a model
        # turn. Successful futures have already returned above.
        pool.shutdown(wait=False, cancel_futures=True)


#: Tokens the slice summaries may occupy in the naming prompt. Smaller than a
#: chunk budget because this pass is short and its input is prose, and because
#: leaving room matters more here than anywhere else: naming is the ONE step
#: that sees the whole folder, and it only sees it through these.
NAMING_TOKEN_BUDGET = 60_000


def _fit_findings(findings: list[dict]) -> tuple[str, int]:
    """Slice summaries as JSON that fits the naming prompt. Returns (json, dropped).

    WHOLE ENTRIES, measured with the same estimator as everything else. The
    first version cut the encoded string at a fixed 200,000 characters, which
    lands mid-object: the naming pass then saw a malformed tail, silently never
    learned what the last slices contained, and named projects those slices'
    files were afterwards forced into. Dropping entries loses the same
    information but says how many, so the caller can report it.
    """
    kept = list(findings)
    while kept:
        text = json.dumps(kept, indent=1)
        if evidence_mod.estimate_tokens(text) <= NAMING_TOKEN_BUDGET:
            return text, len(findings) - len(kept)
        kept.pop()
    return "[]", len(findings)


def _folder_project(folder: Path) -> dict:
    """The one project a folder is filed into when its projects could not be named."""
    slug = projects_mod.folder_slug(folder)
    return {
        "slug": slug,
        "name": folder.name or slug,
        "description": (f"Everything imported from {folder.name}. The project names could not be "
                        "decided automatically; split or rename it from the review screen or the project."),
    }


def _row_files(line: str, by_key: dict) -> tuple[str, ...]:
    """The walked files one prompt row stands for, looked up by its key."""
    try:
        data = json.loads(line)
    except ValueError:
        return ()
    key = data.get("path") or data.get("dir") if isinstance(data, dict) else None
    row = by_key.get(key)
    return row.files if row is not None else ()


def classify_chunked(
    folder: Path,
    ev: evidence_mod.Evidence,
    *,
    agent: bf.Agent,
    existing: list[str],
    work_dir: Path,
    stream=None,
    feedback: str = "",
    agents: AgentSettings | None = None,
    fixed: dict[str, str] | None = None,
    own=(),
) -> tuple[plan_mod.Plan | None, str]:
    """Classify a folder too big to fit one prompt. Survey -> name -> assign.

    NAMING NAMES NEW PROJECTS ONLY. Its answer is JSON, checked after the
    fact, so it is never shown the workspace's other projects to copy: this
    folder's `own` projects join the list by code, and a named slug that is an
    existing project's is renamed (`backfill_projects.free_slug`) and flagged,
    never merged into it. Reusing another existing project in a chunked folder
    is the reviewer's call (`revise`, `project --reuse`).

    THE SPLIT IS CHOSEN SO NO CHUNK NEEDS ANOTHER CHUNK'S DETAIL. Feeding the
    agent chunks in sequence and letting `--autocompact` absorb the overflow is
    the obvious alternative and it is wrong in a way that does not announce
    itself: compaction is lossy, and what it drops is exactly the evidence the
    classification runs on. Early files would be placed against evidence and
    later ones against a summary of it, with nothing at the review gate able to
    tell the two apart.

    So the one genuinely global decision -- what the projects ARE -- is made
    once, over summaries small enough to fit together. Everything else is
    per-chunk: each slice maps its own rows onto that fixed list, needing
    nothing from its siblings.

    Returns ``(plan, tail)`` like :func:`classify`, so the caller cannot tell
    which route produced the plan. No single failed pass stops the folder: a
    SURVEY slice that fails only leaves its findings out of naming (the slice is
    still filed); a NAMING pass that fails files everything into one project
    named for the folder, flagged on the review screen; an ASSIGN slice that
    fails costs only its own files: they are
    `Plan.excluded`, named on the review screen and left `new` for the next run,
    and the rest of the folder imports. Refusing a whole folder over one slice
    is what turned two typos into 52 lost minutes on 2026-10-25.
    """
    evidence_rows = evidence_mod.rows(ev)
    by_key = {row.key: row for row in evidence_rows}
    jsonl = "\n".join(row.line for row in evidence_rows)
    chunks = evidence_mod.chunk_lines(jsonl)
    n = len(chunks)

    with _ReadProgress(folder, ev.total_files, n, stream):
        # Independent surveys preserve all evidence and the original slice order.
        # Only the naming step depends on seeing every completed survey.
        def survey_one(pair: tuple[int, list[str]]):
            i, chunk = pair
            return i, _run_pass(
                folder,
                git_note
                + prompts.survey(root=folder, evidence_jsonl="\n".join(chunk),
                                 index=i, total=n, work_dir=str(work_dir),
                                 truncated=ev.sample_budget_hit),
                agent=agent, work_dir=work_dir, stream=stream, total=ev.total_files,
                heading=f"Reading {folder.name} — slice {i} of {n}", key="findings",
                agents=agents,
            )

        git_note = _git_note(folder, work_dir)
        numbered = list(enumerate(chunks, start=1))
        findings: list[dict] = []
        surveyed = _classification_results(
            survey_one, numbered, workers=SURVEY_CONCURRENCY,
        )
        # A slice whose survey failed (after its retry) only costs the naming
        # step what that slice would have said: the slice is still FILED, by
        # its own assign session, which reads the same evidence. Only when no
        # slice could be read at all is there nothing to name projects from.
        unread: list[int] = []
        last_detail = ""
        for i, (got, detail) in surveyed:
            if got is None:
                unread.append(i)
                last_detail = detail
                continue
            findings.append({"slice": i, **got})
        if not findings:
            return None, f"no slice could be read: {last_detail}"

        # -- name: the only step that sees the whole folder at once
        findings_json, dropped = _fit_findings(findings)
        own = list(own)
        own_slugs = {spec.slug for spec in own}
        named, detail = _run_pass(
            folder,
            prompts.name_projects(root=folder, findings_json=findings_json,
                                  own=_own_pairs(own), feedback=feedback),
            agent=agent, work_dir=work_dir, stream=stream, total=ev.total_files,
            heading=f"Naming the projects in {folder.name}", key="projects", agents=agents,
            empty_ok=bool(own),
        )
        named_projects = [p for p in ((named or {}).get("projects") or [])
                          if isinstance(p, dict) and p.get("slug")]
        # A failed pass, or an answer with no usable slug (empty is a full
        # answer only when this folder's own projects hold everything).
        naming_fallback = named is None or not _usable_pass(named, "projects", empty_ok=bool(own))
        if naming_fallback:
            # The naming step failed twice. Rather than throw the folder away,
            # file it into ONE project named for the folder: every slice still
            # leaves out what is not research, the review screen says so, and a
            # project can be split or renamed afterwards (artifacts move).
            named = {"projects": [_folder_project(folder)], "summary": ""}
            named_projects = named["projects"]
        taken = set(existing) | own_slugs
        specs = list(own)
        for p in named_projects:
            slug = str(p.get("slug") or "").strip()
            if slug in own_slugs or slug in {s.slug for s in specs}:
                continue  # already on the list (an own project the answer repeated)
            near = ""
            if slug in taken:
                # An existing project's slug, typed into an answer nobody
                # checks: a new project of its own, flagged on review.
                near, slug = slug, projects_mod.free_slug(slug, taken | {s.slug for s in specs})
            specs.append(plan_mod.ProjectSpec(
                slug=slug,
                name=str(p.get("name") or p.get("slug") or "").strip(),
                description=str(p.get("description") or "").strip(),
                # Asked for by `name_projects` and parsed by `_plan_from` on the
                # other route. Dropping them here made the two paths produce
                # different Plans from the same agent answer.
                tags=[str(t) for t in (p.get("tags") or []) if t],
                near=near,
            ))
        listing = "\n".join(f"    {s.slug}  —  {s.description or s.name}" for s in specs)

        # -- assign: independent per chunk, against the fixed list
        #
        # CONCURRENT, and that is the payoff of the whole design rather than a
        # bolted-on optimisation: a slice needs nothing from its siblings, so
        # nothing is serialised except by the worker bound. Bounded by the
        # context floor each slice pays, which is a different bound from the one
        # on `run_units` -- hence a separate number rather than a shared one.
        from .. import structure as structure_mod

        # HOISTED. `mtime_uninformative` walks every file in the folder, and this
        # was inside `file_one` -- so a 200,000-file drive rebuilt a 200,000-element
        # list once per slice, across dozens of slices, all holding the GIL.
        mtime_dead = ev.mtime_uninformative
        fixed = fixed or {}
        slugs = tuple(dict.fromkeys([*(s.slug for s in specs), *fixed.values()]))

        def file_one(pair: tuple[int, list[str]]):
            # The slice OWNS the files of its rows -- a sampled file, or a
            # rollup's exact group -- so a selection can never reach a file
            # another slice owns, and a failed slice's files stay its own.
            i, chunk = pair
            owned = tuple(f for line in chunk for f in _row_files(line, by_key))
            ref = tool_mod.Reference(root=str(folder), mode=tool_mod.Mode.FILE,
                                     files=owned, projects=slugs, **_fixed_seed(owned, fixed))
            return i, _run_tool_pass(
                folder,
                prompts.assign_chunk(root=folder, evidence_jsonl="\n".join(chunk),
                                     projects=listing, index=i, total=n,
                                     work_dir=str(work_dir),
                                     truncated=ev.sample_budget_hit,
                                     mtime_uninformative=mtime_dead, feedback=feedback,
                                     candidates=prompts.run_candidates(
                                         structure_mod.run_candidates(owned))),
                ref, agent=agent, work_dir=work_dir, stream=stream,
                heading=f"Filing slice {i} of {n}", phase="assign",
                key=_session_key("assign", i, ref), agents=agents,
            )

        filed = _classification_results(
            file_one, numbered, workers=classify_concurrency(),
        )
        plan = _plan_from_passes([got for _, got in filed], specs,
                                 summary=str(named.get("summary") or ""))
        plan.fixed = dict(fixed)
        if fixed and not any(got.state.accepted for _, got in filed):
            failed = [got.detail for _, got in filed if got.detail]
            if failed:
                return None, "no slice could be filed: " + failed[-1]
        plan.stats["unread_slices"] = len(unread)
        plan.stats["naming_fallback"] = naming_fallback
        if not plan.assignments and not plan.left_out:
            # An all-empty result is not a plan: `resolve` would return an empty
            # map, `pack` no units, and the run would report "N files found on
            # disk · 0 queued" as a success. A green no-op is the worst possible
            # answer here -- it is the one a reader stops investigating.
            failed = [got.detail for _, got in filed if got.detail]
            return None, "no slice placed a single file" + (f": {failed[-1]}" if failed else "")
        note = f"; {dropped} slice summary(ies) did not fit the naming step" if dropped else ""
        return plan, f"classified in {n} slices{note}"
from probe.cli.imports.folder.classify.classify import _fixed_seed, _git_note, _own_pairs, _session_key  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.folder.classify.context import _ReadProgress, _read_progress  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.folder.classify.passes import _plan_from_passes, _run_pass, _run_tool_pass, _usable_pass  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.imports.folder.upload.units import _env_concurrency  # noqa: E402 -- pieces need each other; the front door loads this one first
