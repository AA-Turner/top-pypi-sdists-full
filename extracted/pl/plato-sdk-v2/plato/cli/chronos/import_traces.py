"""Import local Claude Code transcripts into a synthetic Chronos session.

Replays an on-disk Claude Code project directory (main ``<session-id>.jsonl``
plus its ``<session-id>/subagents/`` tree) into a freshly created Chronos
session, emitting the exact same ATIF span stream the live ``claude-code``
agent produces — via the shared converter in
``plato.utils.claude_transcripts`` — so the trajectory viewer cannot tell an
imported session from a live one.

Everything under the source trace directory is treated as strictly
read-only.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Annotated, Any

import httpx
import typer
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from plato.chronos.api.sessions import complete_session, create_session
from plato.chronos.models import (
    CompleteSessionRequest,
    CreateSessionRequest,
    CreateSessionResponse,
    Status1,
)
from plato.cli.chronos.settings import get_settings
from plato.cli.chronos.workspace_upload import (
    _read_dvcignore,
    register_git_workspace_ref,
    upload_git_workspace_via_archive,
)
from plato.cli.utils import console
from plato.git_ops.repo import trust_git_directory
from plato.otel import (
    force_flush_tracing,
    get_tracer,
    init_tracing,
    session_span,
    shutdown_tracing,
)
from plato.utils.claude_transcripts import (
    ClaudeTranscriptEmitter,
    PendingClaudeToolCall,
    StreamUsageAccountant,
    SubagentTraceEmitter,
    discover_subagent_transcripts,
    normalize_transcript_record,
    parse_timestamp_ns,
    workflow_results_for,
)

import_app = typer.Typer(help="Import local agent traces into synthetic Chronos sessions.")

# Matches the stub Claude Code writes in place of a large tool output:
#   <persisted-output>
#   Output too large (84.9KB). Full output saved to: /abs/path/tool-results/b150a30vd.txt
#   ...
_PERSISTED_OUTPUT_RE = re.compile(r"Full output saved to: (?P<path>\S+?/tool-results/(?P<name>\S+?\.txt))")

# Emitted spans between force_flush calls during replay. Keyed on spans (not
# input records — one assistant record can emit a span per tool_use block) so
# the BatchSpanProcessor queue (max 10k) stays far from overflow, where it
# would silently drop spans.
_FLUSH_EVERY_SPANS = 500


@dataclass
class ImportStats:
    """Replay accounting used for the end-of-run integrity summary."""

    main_records: int = 0
    main_traced: int = 0
    subagent_files: int = 0
    subagent_records: int = 0
    subagent_traced: int = 0
    persisted_outputs_inlined: int = 0
    persisted_outputs_missing: list[str] = field(default_factory=list)
    flush_failures: int = 0


def select_main_transcript(trace_dir: Path, session_id: str | None) -> Path:
    """Pick the main session JSONL to import from a Claude Code project dir.

    With an explicit ``session_id``, requires ``<session_id>.jsonl``. Otherwise
    prefers the transcript whose sidecar ``<stem>/subagents`` directory exists
    (the real work session — the other JSONLs are typically ``/login`` /
    ``/model`` housekeeping sessions); ties and fallbacks resolve to the
    largest file.
    """
    if session_id:
        path = trace_dir / f"{session_id}.jsonl"
        if not path.is_file():
            raise ValueError(f"No transcript {path} in {trace_dir}")
        return path

    candidates = sorted(trace_dir.glob("*.jsonl"))
    if not candidates:
        raise ValueError(f"No .jsonl transcripts found in {trace_dir}")

    def sort_key(p: Path) -> tuple[int, int]:
        has_subagents = (trace_dir / p.stem / "subagents").is_dir()
        return (1 if has_subagents else 0, p.stat().st_size)

    best = max(candidates, key=sort_key)
    return best


def build_persisted_output_resolver(session_dir: Path, stats: ImportStats) -> Callable[[str], str]:
    """Resolver that inlines full ``tool-results/`` payloads into stub texts.

    Live sessions upload only the stub (that is what the model saw); the
    import inlines the complete persisted output after the stub so nothing is
    lost, clearly marked so a reader can still tell what the model's context
    actually contained. The stale absolute path in the stub is remapped into
    the trace directory's own ``tool-results/``.
    """
    tool_results_dir = session_dir / "tool-results"

    def resolve(text: str) -> str:
        if "tool-results/" not in text:
            return text
        match = _PERSISTED_OUTPUT_RE.search(text)
        if match is None:
            return text
        local = tool_results_dir / Path(match.group("name")).name
        if not local.is_file():
            stats.persisted_outputs_missing.append(match.group("path"))
            return text
        try:
            full = local.read_text(errors="replace")
        except OSError:
            stats.persisted_outputs_missing.append(str(local))
            return text
        stats.persisted_outputs_inlined += 1
        return (
            f"{text}\n\n"
            f"--- Full persisted output ({local.name}, inlined at import; "
            f"the agent saw only the preview above) ---\n{full}"
        )

    return resolve


def _transcript_time_bounds(records: list[dict[str, Any]]) -> tuple[int | None, int | None]:
    first: int | None = None
    last: int | None = None
    for record in records:
        ts = parse_timestamp_ns(record)
        if ts is None:
            continue
        if first is None:
            first = ts
        last = ts
    return first, last


def _file_tail_timestamp_ns(path: Path, *, tail_bytes: int = 16384) -> int | None:
    """Last parseable record timestamp near the end of a JSONL file.

    Reads only the final ``tail_bytes`` so scanning many large sub-agent
    transcripts for the session end bound stays cheap.
    """
    try:
        size = path.stat().st_size
        with path.open("rb") as fh:
            fh.seek(max(0, size - tail_bytes))
            tail = fh.read().decode("utf-8", errors="replace")
    except OSError:
        return None
    for line in reversed(tail.splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            # First line of the tail window is usually a partial record.
            continue
        ts = parse_timestamp_ns(record)
        if ts is not None:
            return ts
    return None


def _detect_model_name(records: list[dict[str, Any]]) -> str:
    for record in records:
        message = record.get("message")
        if isinstance(message, dict):
            model = message.get("model")
            if isinstance(model, str) and model:
                return model
    return "claude-code-import"


def _read_transcript(path: Path) -> list[dict[str, Any]]:
    """Read every well-formed JSON line of a transcript (read-only)."""
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(record, dict):
                records.append(record)
    return records


def _checked_flush(stats: ImportStats) -> None:
    if not force_flush_tracing():
        stats.flush_failures += 1


class _FlushGate:
    """Flush whenever the emitter has opened ``_FLUSH_EVERY_SPANS`` new spans."""

    def __init__(self, emitter: ClaudeTranscriptEmitter, stats: ImportStats):
        self._emitter = emitter
        self._stats = stats
        self._flushed_at = 0

    def maybe_flush(self) -> None:
        if self._emitter.spans_emitted - self._flushed_at >= _FLUSH_EVERY_SPANS:
            self.flush()

    def flush(self) -> None:
        _checked_flush(self._stats)
        self._flushed_at = self._emitter.spans_emitted


class _ReplayProgress:
    """Byte-based progress with ETA for the replay.

    In a terminal, renders a rich progress bar. When output is piped (log
    file / CI), prints a plain progress line at most every ``interval``
    seconds so the log stays readable but still shows percent + ETA.
    """

    def __init__(self, total_bytes: int, *, interval: float = 10.0):
        self.total = max(total_bytes, 1)
        self.done = 0
        self._interval = interval
        self._started = time.monotonic()
        self._last_print = 0.0
        self._rich: Progress | None = None
        self._task_id: TaskID | None = None
        if console.is_terminal:
            self._rich = Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                DownloadColumn(),
                TimeElapsedColumn(),
                TimeRemainingColumn(),
                console=console,
            )
            self._rich.start()
            self._task_id = self._rich.add_task("Replaying transcripts", total=self.total)

    def advance(self, nbytes: int, label: str) -> None:
        self.done += nbytes
        if self._rich is not None and self._task_id is not None:
            self._rich.update(self._task_id, completed=self.done, description=label)
            return
        now = time.monotonic()
        if now - self._last_print < self._interval and self.done < self.total:
            return
        self._last_print = now
        elapsed = now - self._started
        pct = 100.0 * self.done / self.total
        rate = self.done / elapsed if elapsed > 0 else 0
        eta = (self.total - self.done) / rate if rate > 0 else 0
        console.print(
            f"  progress: {pct:5.1f}%  ({self.done / 1e6:.1f}/{self.total / 1e6:.1f} MB)  "
            f"elapsed {elapsed:.0f}s  eta {eta:.0f}s  [{label}]"
        )

    def close(self) -> None:
        if self._rich is not None:
            self._rich.stop()


def replay_trace(
    *,
    trace_dir: Path,
    main_transcript: Path,
    chronos_session_id: str,
    otel_url: str,
    resolve_persisted_outputs: bool,
) -> tuple[ImportStats, StreamUsageAccountant]:
    """Replay one Claude Code session directory into a Chronos session."""
    stats = ImportStats()
    session_dir = trace_dir / main_transcript.stem
    subagents_dir = session_dir / "subagents"

    main_records = _read_transcript(main_transcript)
    stats.main_records = len(main_records)

    # Progress is tracked in source bytes: known upfront, and proportional to
    # both parse and upload work (span payloads mirror transcript content).
    subagent_paths = discover_subagent_transcripts(subagents_dir)
    total_bytes = main_transcript.stat().st_size + sum(p.stat().st_size for p in subagent_paths)
    progress = _ReplayProgress(total_bytes)
    first_ts, last_ts = _transcript_time_bounds(main_records)
    # Sub-agents can outlive the main transcript's last record; the session
    # span must end at the true last activity or nested sub-agent spans would
    # extend past their parent in the timeline.
    subagent_last = [ts for p in subagent_paths if (ts := _file_tail_timestamp_ns(p)) is not None]
    if subagent_last and (last_ts is None or max(subagent_last) > last_ts):
        last_ts = max(subagent_last)
    model_name = _detect_model_name(main_records)

    # cwd recorded in the transcript = the workspace the agent actually ran in.
    workspace_dir = next(
        (r["cwd"] for r in main_records if isinstance(r.get("cwd"), str) and r["cwd"]),
        None,
    )

    init_tracing(
        service_name="claude-code",
        session_id=chronos_session_id,
        otlp_endpoint=otel_url,
    )
    tracer = get_tracer("claude-code")

    resolver = build_persisted_output_resolver(session_dir, stats) if resolve_persisted_outputs else None
    emitter = ClaudeTranscriptEmitter(
        tracer,
        model_name=model_name,
        workspace_dir=workspace_dir,
        cost_fn=None,
        use_transcript_timestamps=True,
        tool_result_text_resolver=resolver,
    )
    accountant = StreamUsageAccountant(cost_fn=lambda **_: None)

    try:
        with session_span(
            tracer,
            agent_name="claude-code",
            agent_version="import",
            model_name=model_name,
            start_time_ns=first_ts,
            end_time_ns=last_ts,
        ) as root_span:
            root_span.set_attribute("plato.import.source", str(trace_dir))
            root_span.set_attribute("plato.import.claude_session_id", main_transcript.stem)

            # ---- main transcript ------------------------------------------
            pending_tool_calls: dict[str, PendingClaudeToolCall] = {}
            # Start at 0 so the first replayed step is atif.step.1: unlike a
            # live run, session_span emitted no step-1 system-context step
            # (the transcript doesn't record the system prompt).
            step_counter = [0]
            flush_gate = _FlushGate(emitter, stats)
            main_bytes = main_transcript.stat().st_size
            for record in main_records:
                event = normalize_transcript_record(record)
                if event is None:
                    continue
                stats.main_traced += 1
                emitter.emit_event(event, pending_tool_calls, step_counter)
                if event.get("type") == "assistant":
                    accountant.record_assistant(event)
                elif event.get("type") == "result":
                    accountant.record_result(event)
                flush_gate.maybe_flush()
            flush_gate.flush()
            progress.advance(main_bytes, "main transcript")

            # ---- sub-agent transcripts -------------------------------------
            # Replayed after the main transcript so every Task/Workflow
            # tool_use span already exists; wrappers parent under the tool
            # span that spawned them via meta toolUseId.
            subagent_emitter = SubagentTraceEmitter(
                emitter,
                root_span,
                expected_session_id=main_transcript.stem,
                parent_resolver=lambda meta: emitter.parent_context_for_tool_use(
                    meta.get("toolUseId") if isinstance(meta, dict) else None
                ),
            )
            stats.subagent_files = len(subagent_paths)
            for file_index, transcript in enumerate(subagent_paths, start=1):
                for record in _read_transcript(transcript):
                    stats.subagent_records += 1
                    if subagent_emitter.feed_record(transcript, record):
                        stats.subagent_traced += 1
                    # The gate counts emitted spans (shared emitter), so one
                    # large sub-agent transcript can't outrun the BSP queue.
                    flush_gate.maybe_flush()
                flush_gate.flush()
                progress.advance(
                    transcript.stat().st_size,
                    f"subagent {file_index}/{len(subagent_paths)}",
                )
            subagent_emitter.finalize_all(workflow_results_for(subagents_dir))

            accountant.apply_to_span(root_span)
    finally:
        progress.close()
        # The final drain covers everything queued after the last periodic
        # flush (sub-agent wrapper ends, the root span, cost spans); a
        # timeout here means those spans may be lost, so it counts as a
        # flush failure and fails the import like any other.
        if not shutdown_tracing():
            stats.flush_failures += 1

    return stats, accountant


_PLATO_GIT_ENV = {
    "GIT_AUTHOR_NAME": "Plato",
    "GIT_AUTHOR_EMAIL": "plato@plato.dev",
    "GIT_COMMITTER_NAME": "Plato",
    "GIT_COMMITTER_EMAIL": "plato@plato.dev",
}


def _git(args: list[str], *, cwd: Path | None = None) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        env={**os.environ, **_PLATO_GIT_ENV},
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip() or result.stdout.strip()}")
    return result.stdout.strip()


def build_git_workspace_payload(project: Path, staging: Path) -> Path:
    """Build a ``repo/`` + ``.git-bare/`` workspace payload from a plain git repo.

    The source ``project`` is only ever read: history is captured with a local
    ``git clone --bare``, the working tree is a fresh clone of that bare, and
    any uncommitted (tracked-modified or untracked-unignored) files are copied
    in on top and committed — so the payload matches the project's working
    tree exactly, minus gitignored artifacts (node_modules, builds, …).

    Returns the payload directory (``staging/payload``).
    """
    project = project.expanduser().resolve()
    if not (project / ".git").is_dir():
        raise ValueError(f"{project} is not a git repository")
    trust_git_directory(project)

    payload_dir = staging / "payload"
    bare_dir = payload_dir / ".git-bare"
    repo_dir = payload_dir / "repo"
    payload_dir.mkdir(parents=True, exist_ok=True)

    _git(["clone", "--bare", str(project), str(bare_dir)])
    trust_git_directory(bare_dir)
    # A --bare clone maps refs verbatim; make HEAD's branch explicit as main so
    # the workspace matches what _sync_repo_to_bare pushes on upload.
    head_branch = _git(["--git-dir", str(bare_dir), "symbolic-ref", "--short", "HEAD"])
    if head_branch != "main":
        _git(["--git-dir", str(bare_dir), "branch", "-f", "main", head_branch])
        _git(["--git-dir", str(bare_dir), "symbolic-ref", "HEAD", "refs/heads/main"])
    _git(["clone", str(bare_dir), str(repo_dir)])
    _git(["remote", "set-url", "origin", "../.git-bare"], cwd=repo_dir)

    # Overlay uncommitted work: tracked modifications and untracked files that
    # are not gitignored (porcelain never lists ignored paths). Raw subprocess
    # (not _git) because _git strips the output, which would eat the leading
    # space of a first entry's two-char status field (" D" -> "D ") and shift
    # the path parse by one character.
    porcelain = subprocess.run(
        ["git", "status", "--porcelain", "-z"],
        cwd=str(project),
        env={**os.environ, **_PLATO_GIT_ENV},
        capture_output=True,
        text=True,
        check=True,
    )
    dirty = porcelain.stdout
    copied = 0

    def _remove(path: Path) -> None:
        """Remove a payload path (file, symlink, or directory) and prune
        now-empty parents.

        Porcelain reports deletions/renames per *file*, so deleting or
        renaming a whole directory arrives as one record per contained file;
        without pruning, the emptied directory itself would survive into the
        uploaded archive.
        """
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
        elif path.exists() or path.is_symlink():
            path.unlink()
        parent = path.parent
        while parent != repo_dir and parent.is_dir() and not any(parent.iterdir()):
            parent.rmdir()
            parent = parent.parent

    entries = iter(dirty.split("\0"))
    for entry in entries:
        if not entry.strip():
            continue
        status, rel = entry[:2], entry[3:]
        if not rel:
            continue
        if "R" in status or "C" in status:
            # Rename/copy records carry two NUL-separated paths: the new path
            # (already in ``rel``) then the original. For a rename the working
            # tree no longer has the original, but the clone still does at its
            # committed location — remove it so the payload matches the tree.
            # Copies keep the original in place.
            orig = next(entries, None)
            if "R" in status and orig:
                _remove(repo_dir / orig)
        src = project / rel
        dest = repo_dir / rel
        if "D" in status or not src.exists():
            _remove(dest)
            continue
        if src.is_dir():
            shutil.copytree(src, dest, dirs_exist_ok=True)
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
        copied += 1
    if copied:
        console.print(f"[dim]Overlaid {copied} uncommitted path(s) from the working tree[/dim]")

    return payload_dir


def upload_project_workspace(
    *,
    project: Path,
    session_id: str,
    repo_name: str,
    dir_name: str,
    step_name: str,
    chronos_url: str,
    api_key: str,
) -> None:
    """Upload a plain git repo as this session's git workspace (source read-only)."""
    with tempfile.TemporaryDirectory(prefix="plato-import-ws-") as staging_str:
        staging = Path(staging_str)
        payload_dir = build_git_workspace_payload(project, staging)
        repo_dir = payload_dir / "repo"
        bare_dir = payload_dir / ".git-bare"

        # Commit the overlay (if any) into the payload's own clone; the source
        # project is untouched.
        _git(["add", "-A"], cwd=repo_dir)
        if _git(["status", "--porcelain"], cwd=repo_dir):
            _git(["commit", "-m", "Import working tree snapshot"], cwd=repo_dir)
        _git(["push", str(bare_dir), "HEAD:refs/heads/main"], cwd=repo_dir)
        head_sha = _git(["--git-dir", str(bare_dir), "rev-parse", "main"])

        ignore_patterns = _read_dvcignore(payload_dir)
        _archive_md5, dvc_yaml = upload_git_workspace_via_archive(
            payload_dir,
            repo_name=repo_name,
            dir_name=dir_name,
            chronos_url=chronos_url,
            api_key=api_key,
            ignore_patterns=ignore_patterns,
        )
        ref = register_git_workspace_ref(
            session_id=session_id,
            repo_name=repo_name,
            head_sha=head_sha,
            dvc_files={dir_name: dvc_yaml},
            step_name=step_name,
            chronos_url=chronos_url,
            api_key=api_key,
        )
        console.print(f"[green]Workspace uploaded[/green] ref={ref.ref_public_id} sha={head_sha[:12]}")


def _create_chronos_session(
    *,
    world_name: str,
    tags: list[str],
    chronos_url: str,
    api_key: str,
) -> CreateSessionResponse:
    with httpx.Client(base_url=chronos_url.rstrip("/"), timeout=30.0) as client:
        return create_session.sync(
            client,
            body=CreateSessionRequest(world_name=world_name, tags=tags),
            x_api_key=api_key,
        )


def _complete_chronos_session(
    *,
    session_id: str,
    chronos_url: str,
    api_key: str,
    failed: bool = False,
    error_message: str | None = None,
) -> None:
    with httpx.Client(base_url=chronos_url.rstrip("/"), timeout=30.0) as client:
        complete_session.sync(
            client,
            public_id=session_id,
            body=CompleteSessionRequest(
                status=Status1.failed if failed else Status1.completed,
                exit_code=1 if failed else 0,
                error_message=error_message[:500] if error_message else None,
            ),
            x_api_key=api_key,
        )


@import_app.command("claude-code")
def import_claude_code(
    trace_dir: Annotated[
        Path,
        typer.Argument(
            help="Claude Code project directory holding <session-id>.jsonl transcripts "
            "(e.g. a copy of ~/.claude/projects/<cwd-slug>). Read-only.",
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
        ),
    ],
    session_id: Annotated[
        str | None,
        typer.Option(
            "--session",
            help="Claude session UUID to import (default: the transcript with a "
            "subagents/ dir, largest wins — the other JSONLs are usually "
            "/login//model housekeeping)",
        ),
    ] = None,
    world_name: Annotated[
        str,
        typer.Option("--world-name", help="World name recorded on the created Chronos session"),
    ] = "webclone",
    project: Annotated[
        Path | None,
        typer.Option(
            "--project",
            help="Plain git repo holding the session's project code; uploaded to the "
            "created session as a git workspace (repo/ + .git-bare/ DVC archive). "
            "Source repo is read-only — history and working tree are cloned/copied "
            "into a scratch payload.",
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
        ),
    ] = None,
    workspace_repo: Annotated[
        str,
        typer.Option("--workspace-repo", help="Chronos workspace repo name for ref registration"),
    ] = "code",
    workspace_dir_name: Annotated[
        str,
        typer.Option("--workspace-dir-name", help="DVC archive dir name / restore target"),
    ] = "data",
    workspace_step: Annotated[
        str,
        typer.Option("--workspace-step", help="Workspace ref step name registered for the upload"),
    ] = "claude-code-import",
    name_tag: Annotated[
        str | None,
        typer.Option("--tag", help="Extra tag for the created session (repeatable via commas)"),
    ] = None,
    resolve_persisted_outputs: Annotated[
        bool,
        typer.Option(
            "--resolve-persisted-outputs/--no-resolve-persisted-outputs",
            help="Inline full tool-results/*.txt payloads after their "
            "<persisted-output> stubs (the stub alone is what a live "
            "session would have uploaded)",
        ),
    ] = True,
    dry_run: Annotated[
        bool,
        typer.Option("--dry-run", help="Parse and summarize without creating a session"),
    ] = False,
    chronos_url: Annotated[
        str | None, typer.Option("--url", "-u", envvar="CHRONOS_URL", help="Chronos API URL")
    ] = None,
    api_key: Annotated[
        str | None,
        typer.Option("--api-key", "-k", envvar="PLATO_API_KEY", help="Plato API key"),
    ] = None,
) -> None:
    """Import a local Claude Code session (main + sub-agent transcripts) into Chronos.

    Creates a synthetic Chronos session and replays the transcripts as ATIF
    spans using the same shared converter the live claude-code agent uses,
    stamped at their original timestamps. The source directory is never
    modified.
    """
    trace_dir = trace_dir.expanduser().resolve()
    try:
        main_transcript = select_main_transcript(trace_dir, session_id)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc

    session_dir = trace_dir / main_transcript.stem
    subagent_count = len(discover_subagent_transcripts(session_dir / "subagents"))
    console.print(f"[bold]Importing Claude Code session[/bold] {main_transcript.stem}")
    console.print(f"  Transcript: {main_transcript} ({main_transcript.stat().st_size:,} bytes)")
    console.print(f"  Sub-agent transcripts: {subagent_count}")

    if dry_run:
        stats = ImportStats()
        records = _read_transcript(main_transcript)
        traced = sum(1 for r in records if normalize_transcript_record(r) is not None)
        console.print(f"  Main records: {len(records)} ({traced} traceable)")
        console.print("[yellow]Dry run: no session created.[/yellow]")
        return

    resolved_api_key = api_key
    if not resolved_api_key:
        console.print("[red]No API key provided[/red] (set PLATO_API_KEY or --api-key)")
        raise typer.Exit(1)
    resolved_chronos_url = chronos_url or get_settings().chronos_url

    tags = ["synthetic", "claude-code-import"]
    if name_tag:
        tags.extend(t.strip() for t in name_tag.split(",") if t.strip())

    session = _create_chronos_session(
        world_name=world_name,
        tags=tags,
        chronos_url=resolved_chronos_url,
        api_key=resolved_api_key,
    )
    otel_url = session.otel_url or f"{resolved_chronos_url.rstrip('/')}/api/otel"
    console.print(f"  Chronos session: [bold]{session.public_id}[/bold]")

    try:
        stats, accountant = replay_trace(
            trace_dir=trace_dir,
            main_transcript=main_transcript,
            chronos_session_id=session.public_id,
            otel_url=otel_url,
            resolve_persisted_outputs=resolve_persisted_outputs,
        )

        if project is not None:
            console.print(f"[dim]Uploading workspace from {project}…[/dim]")
            upload_project_workspace(
                project=project,
                session_id=session.public_id,
                repo_name=workspace_repo,
                dir_name=workspace_dir_name,
                step_name=workspace_step,
                chronos_url=resolved_chronos_url,
                api_key=resolved_api_key,
            )
    except Exception as exc:
        # Never orphan the freshly created session: give it a terminal
        # failed status before surfacing the error. Best-effort — the
        # original exception wins if completion also fails.
        try:
            _complete_chronos_session(
                session_id=session.public_id,
                chronos_url=resolved_chronos_url,
                api_key=resolved_api_key,
                failed=True,
                error_message=f"import failed: {exc}",
            )
        except Exception:
            console.print("[yellow]Could not mark the session failed after the error below.[/yellow]")
        raise

    # A flush timeout means spans were (or may have been) dropped — mark the
    # session failed rather than presenting an incomplete trajectory as done.
    flush_error = (
        f"{stats.flush_failures} span flush(es) timed out during import; trajectory may be incomplete"
        if stats.flush_failures
        else None
    )
    _complete_chronos_session(
        session_id=session.public_id,
        chronos_url=resolved_chronos_url,
        api_key=resolved_api_key,
        failed=stats.flush_failures > 0,
        error_message=flush_error,
    )

    console.print("[green]Import complete[/green]" if not stats.flush_failures else "[red]Import incomplete[/red]")
    console.print(f"  Main records:      {stats.main_records} ({stats.main_traced} traced)")
    console.print(
        f"  Sub-agent records: {stats.subagent_records} across {stats.subagent_files} "
        f"transcripts ({stats.subagent_traced} traced)"
    )
    console.print(f"  Turns: {accountant.turn_count}  Cost: ${accountant.cost_usd:.2f}")
    if stats.persisted_outputs_inlined:
        console.print(f"  Persisted outputs inlined: {stats.persisted_outputs_inlined}")
    if stats.persisted_outputs_missing:
        console.print(
            f"[yellow]  Persisted outputs referenced but not found: {len(stats.persisted_outputs_missing)}[/yellow]"
        )
        for missing in stats.persisted_outputs_missing[:5]:
            console.print(f"[yellow]    {missing}[/yellow]")
    if stats.flush_failures:
        console.print(f"[red]  {flush_error} — the session was marked failed. Re-run the import.[/red]")
        raise typer.Exit(1)
    console.print(f"  View: {resolved_chronos_url.rstrip('/')}/sessions/{session.public_id}")
