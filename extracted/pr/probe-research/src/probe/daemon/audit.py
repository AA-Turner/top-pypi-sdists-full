"""The team-note audit, run by the daemon (daemon-team-note-audit, 2026-10-11).

Machines whose sessions the daemon records lost the weekly team-note audit when
the lean plugin left out `note_audit.py` (#2133): the audit's prompt-hook line
asked the MAIN agent to start it, and in the daemon profile the main agent does
not touch Probe. The daemon runs it instead -- Richard: "whoever records also
audits", "dont ask for approval or anything". He also asked for "a smaller agent":
the model is the server's `auditor` alias for that reason, set to the writer's
model since Haiku 5.5 changed nothing in 3 of 3 bench audits (2026-10-11).

    once per session (`audit_considered`), on the researcher's first prompt (a
    person is there), in a session no program drives (`interactive`), unless a
    failed audit on this machine is backing off (`BACKOFF_S`):
        pull     the team note, in-process, under the RESEARCHER's credential
                 (`team_note_file.pull`, what `probe notes sync --pull-only` runs):
                 due-ness is read off the TEAM's copy, and the daemon's own key
                 would park the researcher's note as another credential's
        due?     `team_note_file.audit_due_for_source`: the stamp is a week old, or
                 the block outgrew its budget; else nothing happens
        claim    `team_note_file.claim_audit_dispatch`: one audit per machine
        draft    the pulled note is copied to the audit's own folder
                 (`draft_dir`), the only place its shell may write
        run      its own agent (`agent.build_audit_agent`) on the `audit` lane, on
                 the server's `auditor` model; the `audit-team-note` and
                 `edit-notes` skills verbatim; it asks nothing (`tools.Deps.audit`)
        guard    a run that opened no evidence cannot write its copy
                 (`agent.EvidenceGate`); one that ends without a look is run ONCE
                 more on the writer's model
        publish  only a run that ENDED (final_result) after a look: its copy is
                 merged into the live note under the note's lock (`merge3` against
                 the pulled text, so a teammate's paragraph synced in meanwhile
                 stays) and pushed (`team_note_file.reconcile`), then rendered
        report   one `[Probe]` message to the main agent (`mailbox.Message.keep`)

Nothing reaches the shared note before publish, so a run cut short -- the
session ending, a limit, a crash -- changes nothing: the note stays due, and the
machine backs off. It never touches the writer's coverage or conversation (its
commands do land in the session's logbook, as the daemon's) and never ends the
worker.
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from probe._compat import StrEnum
from probe.daemon import mailbox
from probe.daemon import trace as trace_mod

if TYPE_CHECKING:  # pragma: no cover
    from probe.daemon.worker import Worker

log = logging.getLogger("probe.daemon.audit")

#: The store fact that says this session has had its one look at the audit.
CONSIDERED = "audit_considered"
#: How many of the transcript's first lines are read to tell a person from a program,
#: the longest line read whole (Codex's `session_meta` carries the instructions:
#: 52 KB on the devbox, more with a long AGENTS.md) and the most read in all.
HEAD_LINES = 20
LINE_CAP_BYTES = 4 * 1024 * 1024
HEAD_CAP_BYTES = 8 * 1024 * 1024
#: What a Claude Code transcript line says when a person is at the keyboard
#: (`team_note_file.INTERACTIVE_ENTRYPOINTS`, the prompt hook's own list).
#: Codex's `codex exec` names itself in the rollout's `session_meta.originator`.
AUTOMATED_ORIGINATORS = frozenset({"codex_exec"})
#: After an audit that changed nothing on the server (failed, cut short, never
#: looked, a conflict), this machine waits this long before the next: the note
#: stays due, and every new session would otherwise try again once the lease ends.
BACKOFF_S = 24 * 3600
BACKOFF_FILE = "audit-backoff.json"


class Outcome(StrEnum):
    """How one audit ended (the trace's `run_end`, the log)."""

    NOT_DUE = "not_due"
    HELD = "held_elsewhere"
    BACKING_OFF = "backing_off"
    PULL_FAILED = "pull_failed"
    DONE = "done"
    NO_LOOK = "no_look"
    STOPPED = "stopped"
    FAILED = "failed"


class Published(StrEnum):
    """What publishing a finished audit's copy came to."""

    PUSHED = "pushed"
    #: Merged into the live note, but the push did not land: the next sync sends it.
    LOCAL = "written_locally"
    UNCHANGED = "unchanged"  # the copy is the note it started from: not even a stamp
    CONFLICT = "conflict"  # the live note moved, or changed hands, and would not merge
    FAILED = "failed"


#: Outcomes after which the note is (or will be, at the next sync) audited.
LANDED = frozenset({Published.PUSHED, Published.LOCAL})


@dataclass
class RunResult:
    outcome: Outcome
    report: str = ""
    evidence: int = 0


def audit_text() -> str:
    """The audit's one instruction file, front matter dropped."""
    from importlib import resources

    text = resources.files("probe.daemon").joinpath("audit_note.md").read_text(encoding="utf-8")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end >= 0:
            text = text[end + 4:]
    return text.strip()


def instructions(due: str, *, today: str, folders: "list[Path]", draft: Path) -> str:
    """The audit's text -- why it is due, today's date (`date` is not on the shell's
    safe list), where its shell may look and the copy it edits -- and the two
    skills whole."""
    from probe.daemon import agent as agent_mod
    from probe.daemon import bite as bite_mod

    from probe import skill_versions

    skills = bite_mod.skills_text(bite_mod.AUDIT_SKILLS, reader=skill_versions.MAIN_AGENT)
    shown = ", ".join(f"`{f}`" for f in folders) or "none yet"
    text = (audit_text().replace("{due}", due).replace("{today}", today).replace("{folders}", shown)
            .replace("{draft}", str(draft)).replace("{report_chars}", f"{agent_mod.AUDIT_REPORT_CHARS:,}"))
    return text + (f"\n\n{skills}" if skills else "")


def interactive(transcript: Path) -> bool:
    """Is a person driving this session? Read off the transcript's first lines:
    Claude Code's `entrypoint` (`cli`, an IDE) and Codex's `session_meta`
    `originator` (`codex_exec` is a program), and a Codex sub-agent's
    `source.subagent`. A DENY-list, as the prompt hook's
    `team_note_file.session_is_automated`: what it cannot tell is a person."""
    from probe.cli.team_note_file import INTERACTIVE_ENTRYPOINTS

    head: list[bytes] = []
    try:
        with open(transcript, "rb") as handle:
            read = 0
            while len(head) < HEAD_LINES and read < HEAD_CAP_BYTES:
                raw = handle.readline(LINE_CAP_BYTES)
                if not raw:
                    break
                read += len(raw)
                head.append(raw)
    except OSError:
        return True
    for raw in head:
        try:
            obj = json.loads(raw)
        except ValueError:
            continue
        if not isinstance(obj, dict):
            continue
        entrypoint = obj.get("entrypoint")
        if isinstance(entrypoint, str) and entrypoint.strip():
            return entrypoint.strip().lower() in INTERACTIVE_ENTRYPOINTS
        payload = obj.get("payload") if obj.get("type") == "session_meta" else None
        if isinstance(payload, dict):
            source = payload.get("source")
            if isinstance(source, dict) and source.get("subagent"):
                return False
            return str(payload.get("originator") or "").strip().lower() not in AUTOMATED_ORIGINATORS
    return True


def draft_dir(session_id: str) -> Path:
    """The audit's own folder: its copy of the note, the one place it may write."""
    from probe.daemon import folders

    return folders._state_base() / "audit" / session_id


def backoff_path() -> Path:
    from probe.cli import team_note_file

    return team_note_file.state_dir() / "team-note" / BACKOFF_FILE


def backing_off(now: float | None = None) -> bool:
    """Is a failed audit on this machine still in its backoff? Unreadable: no."""
    try:
        until = float(json.loads(backoff_path().read_text(encoding="utf-8")).get("until") or 0)
    except (OSError, ValueError, AttributeError, TypeError):
        return False
    return (time.time() if now is None else now) < until


def back_off(why: str, now: float | None = None) -> None:
    from probe.sdk.durable import write_text_atomic

    now = time.time() if now is None else now
    try:
        backoff_path().parent.mkdir(parents=True, exist_ok=True)
        write_text_atomic(backoff_path(), json.dumps({"until": now + BACKOFF_S, "why": why}) + "\n")
    except OSError as exc:
        log.warning("audit: the backoff could not be recorded: %s", exc)


class AuditLane:
    """The team-note audit beside the writer, in the writer's process and event loop."""

    def __init__(self, worker: "Worker", *, model=None) -> None:
        self.w = worker
        self.store = worker.store
        self.sid = worker.session.session_id
        self.trace = trace_mod.TraceFile(self.sid, "audit")
        self._model = model
        self.task: asyncio.Task | None = None
        self.draft = draft_dir(self.sid) / "probe-team-note.md"
        #: The credential and paths the pull used: publish goes to the same note.
        self._synced = None
        #: The live note took the audit's copy (no backoff for a cancel after it).
        self._landed = False

    # -- life ----------------------------------------------------------------
    def maybe_start(self) -> bool:
        """Start the audit once per session: on the researcher's first prompt, in a
        session a person drives. Whether it is due is the task's to find out (it
        pulls first). True when it started."""
        if self.task is not None or self.store.fact(CONSIDERED):
            return False
        if not self.store.has_prompt_after(0):
            return False
        with self.store.tx():
            self.store.set_fact(CONSIDERED, time.time())
        if not interactive(self.w.session.transcript):
            log.info("audit: not in a session a program drives")
            return False
        self.task = asyncio.ensure_future(self.run())
        return True

    async def stop(self) -> None:
        """Cancel and wait: at session end nobody is left to read the report. A run
        cut short has published nothing (only `_publish` writes the live note)."""
        task, self.task = self.task, None
        if task is not None and not task.done():
            task.cancel()
            try:
                await task
            except BaseException:  # noqa: BLE001 -- cancelled, or it had failed: either way it is over
                pass

    async def run(self) -> RunResult:
        try:
            return await self._run()
        except asyncio.CancelledError:
            if not self._landed and self.draft.exists():
                back_off("cancelled: the session ended")
            raise
        except Exception as exc:  # noqa: BLE001 -- the audit never ends the worker
            log.exception("audit failed: %s", exc)
            back_off(f"failed: {type(exc).__name__}")
            return RunResult(Outcome.FAILED)
        finally:
            self._clean_draft()

    def _clean_draft(self) -> None:
        import shutil

        shutil.rmtree(self.draft.parent, ignore_errors=True)

    # -- one audit -------------------------------------------------------------
    def _deps(self):
        d = self.w.deps(None)
        d.audit = True
        # Nothing it does is asked, so nothing rides on bypass mode: the audit's
        # rules are the same in every mode (`tools.Deps.audit`).
        d.bypass = False
        # Its own copy's folder is the one place it writes: never the live note,
        # its sync state, or the writer's checked-out notes.
        d.write_dirs = [self.draft.parent]
        return d

    @staticmethod
    def _client_and_paths():
        """The RESEARCHER's credential and the note's paths, as `probe notes sync`
        and the session hooks use them. None without a credential."""
        from probe.cli import team_note_file
        from probe.sdk.client import Client
        from probe.sdk.config import resolve
        from probe.sdk.surface import Surface

        settings = resolve()
        if not getattr(settings, "token", None):
            return None
        if team_note_file.hidden_by_limit(settings):
            # This computer's workspace limit hides team-wide items: no note to audit.
            return None
        return (Client(settings=settings, async_writes=False, surface=Surface.CLI.value),
                team_note_file.paths_for(settings), settings)

    def _pull_now(self) -> bool:
        from probe.cli import team_note_file

        got = self._client_and_paths()
        if got is None:
            log.warning("audit: no Probe credential on this machine to pull the team note with")
            return False
        client, where, settings = got
        with client:
            team_note_file.pull(client, where)
        self._synced = (where, settings)
        return True

    async def _pull(self) -> bool:
        try:
            return await asyncio.to_thread(self._pull_now)
        except Exception as exc:  # noqa: BLE001
            log.warning("audit: pulling the team note failed: %s: %s", type(exc).__name__, exc)
            return False

    def _due(self):
        from probe.cli import team_note_file
        from probe.sdk.config import resolve

        return team_note_file.audit_due_for_source(self.w.session.source, settings=resolve())

    def _document(self) -> Path:
        from probe.cli import team_note_file
        from probe.sdk.config import resolve

        if self._synced is not None:
            return self._synced[0].document
        return team_note_file.paths_for(resolve()).document

    def _publish_now(self, pulled: str) -> tuple[Published, str]:
        """Merge the audit's copy into the live note and push it. `(what came of it, why)`.

        Into the SAME note the pull read (its credential and paths), under the
        note's lock, only while that credential still owns the file; all three texts
        end in one newline first (`note_sync.merge_into_file` does the same: a
        pulled note has none, a heredoc always has one)."""
        from probe.cli import team_note_file
        from probe.cli.note_sync import one_trailing_newline, read_text, stamp_matches
        from probe.sdk.durable import file_lock, write_text_atomic
        from probe.sdk.merge3 import MergeTooLarge, merge3

        pulled = one_trailing_newline(pulled)
        mine = one_trailing_newline(self.draft.read_text(encoding="utf-8"))
        if mine == pulled:
            return Published.UNCHANGED, "the audit's copy is the note it started from"
        got = self._client_and_paths()
        if got is None or self._synced is None:
            return Published.FAILED, "no Probe credential on this machine"
        client, _where_now, _settings_now = got
        where, settings = self._synced
        with file_lock(where.lock):
            if not stamp_matches(where, read_text(where.stamp)):
                return Published.CONFLICT, "the team note on this machine changed hands during the audit"
            current = one_trailing_newline(read_text(where.document) or "")
            try:
                merged = merge3(pulled, mine, current)
            except MergeTooLarge as exc:
                return Published.CONFLICT, str(exc)
            if merged.conflicted:
                return Published.CONFLICT, (f"the note changed during the audit and {merged.conflict_count} "
                                            "change(s) conflict with it")
            write_text_atomic(where.document, merged.text, mode=0o600)
        self._landed = True
        try:
            with client:
                report, text = team_note_file.reconcile(client, where)
        except Exception as exc:  # noqa: BLE001 -- merged locally: the next sync sends it
            return Published.LOCAL, f"written to this machine's note; the next sync sends it ({type(exc).__name__})"
        if report is not None and getattr(report, "conflicted", False):
            return Published.CONFLICT, getattr(report, "detail", "") or "the server's copy conflicted with it"
        try:
            team_note_file.render_blocks(text, settings=settings)
        except Exception as exc:  # noqa: BLE001 -- the push landed; the next session renders
            log.warning("audit: rendering the team note failed: %s", exc)
        if report is not None and not getattr(report, "pushed", True):
            return Published.LOCAL, getattr(report, "detail", "") or "written to this machine's note; the next sync sends it"
        return Published.PUSHED, ""

    async def _publish(self, pulled: str) -> tuple[Published, str]:
        try:
            return await asyncio.to_thread(self._publish_now, pulled)
        except Exception as exc:  # noqa: BLE001
            log.warning("audit: publishing failed: %s: %s", type(exc).__name__, exc)
            return Published.FAILED, f"{type(exc).__name__}: {exc}"

    async def _run(self) -> RunResult:
        from probe.cli import team_note_file

        if backing_off():
            log.info("audit: backing off after a failed audit on this machine")
            return RunResult(Outcome.BACKING_OFF)
        if not await self._pull():
            return RunResult(Outcome.PULL_FAILED)
        due = self._due()
        if due is None:
            log.info("audit: the team note is not due")
            return RunResult(Outcome.NOT_DUE)
        # Its own holder name: a prompt hook asking for the same session (an older
        # plugin) must not pass as the same claimant and start a second auditor.
        if not team_note_file.claim_audit_dispatch(holder=f"daemon:{self.sid}"):
            log.info("audit: another session on this machine holds it")
            return RunResult(Outcome.HELD)
        pulled = self._document().read_text(encoding="utf-8")
        self._write_draft(pulled)
        deps = self._deps()
        text = instructions(due.brief(), today=time.strftime("%Y-%m-%d"), folders=deps.workdirs, draft=self.draft)
        result = await self._one_run(text, deps, run=1, model_name=None)
        if result.outcome == Outcome.NO_LOOK:
            # D9: a run that never looked publishes nothing; the writer's model gets one more go.
            log.info("audit: the run opened no evidence; once more on the writer's model")
            self._write_draft(pulled)
            result = await self._one_run(text, self._deps(), run=2, model_name=self._writer_model())
        if result.outcome != Outcome.DONE:
            back_off(result.outcome.value)
            return result
        published, why = await self._publish(pulled)
        log.info("audit: %s%s", published.value, f" ({why})" if why else "")
        if published not in LANDED:
            back_off(f"{published.value}: {why}")
            report = f"{result.report}\n(Not published: {why}.)" if result.report else f"Not published: {why}."
        else:
            report = f"{result.report}\n({why}.)" if why and result.report else result.report
        if report:
            self.report(report)
        return result

    def _write_draft(self, text: str) -> None:
        """The audit's copy, private to this user, with the last render's
        measurements beside it (the skill reads `health.json` "beside the
        document")."""
        import os
        import shutil

        from probe.cli import team_note_file

        self.draft.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(self.draft.parent, 0o700)
        fd = os.open(self.draft, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
        health = team_note_file.note_health_path()
        if health.is_file():
            shutil.copyfile(health, self.draft.parent / health.name)

    @staticmethod
    def _writer_model() -> str:
        """What the writer asks for (`PROBE_COMPANION_MODEL` or the server's default)."""
        from probe.daemon import model as model_mod

        return model_mod._lane_model(model_mod.LANE_WRITE)

    def _model_for(self, name: str | None):
        if self._model is not None:
            return self._model
        from probe.daemon import model as model_mod

        return model_mod.build(model_mod.endpoint(), model_mod.LANE_AUDIT, name=name)

    async def _one_run(self, text: str, deps, *, run: int, model_name: str | None) -> RunResult:
        from pydantic_ai.exceptions import UsageLimitExceeded
        from pydantic_ai.usage import UsageLimits

        from probe.daemon import agent as agent_mod
        from probe.daemon import model as model_mod
        from probe.daemon import usage as usage_mod
        from probe.daemon import worker as worker_mod
        from probe.daemon.store import LANE_WRITE

        state = agent_mod.AuditState(started=time.monotonic(), trace=self.trace, draft=str(self.draft))
        spent = {"input_tokens": 0, "cached_tokens": 0, "output_tokens": 0, "usd": 0.0}

        def on_round(response: Any) -> None:
            u = response.usage
            spent["input_tokens"] += int(u.input_tokens or 0)
            spent["cached_tokens"] += int(u.cache_read_tokens or 0)
            spent["output_tokens"] += int(u.output_tokens or 0)
            spent["usd"] += float(usage_mod.response_cost(response) or 0.0)
            # The device counter has a writer and a reader column: the audit counts as the writer.
            worker_mod._count_device_tokens(worker_mod.uncached_tokens(u), LANE_WRITE)

        state.on_round = on_round
        model = self._model_for(model_name)
        named = getattr(model, "model_name", None)
        self.trace.start_run(run, model=named if isinstance(named, str) else (
            model_name or model_mod._lane_model(model_mod.LANE_AUDIT)))
        report, outcome = "", Outcome.DONE
        try:
            async def go():
                agent = agent_mod.build_audit_agent(text, model=model, state=state)
                async with agent_mod.keep_lease(deps):
                    return await agent.run("Run the audit.", deps=deps,
                                           usage_limits=UsageLimits(request_limit=agent_mod.AUDIT_ROUNDS + 2))

            result = await asyncio.wait_for(go(), timeout=agent_mod.AUDIT_WALL_S + agent_mod.AUDIT_GRACE_S)
            report = (result.output.report or "").strip()[:agent_mod.AUDIT_REPORT_CHARS]
        except (UsageLimitExceeded, asyncio.TimeoutError) as exc:
            outcome = Outcome.STOPPED
            log.warning("audit run %s stopped: %s", run, state.limit_why or state.detector.tripped or exc)
        except asyncio.CancelledError:
            self.trace.end_run(run, outcome=Outcome.STOPPED.value, error="cancelled: the session ended",
                               evidence=state.evidence, rounds=state.rounds, **spent)
            raise
        except Exception as exc:  # noqa: BLE001
            outcome = Outcome.FAILED
            log.warning("audit run %s failed: %s: %s", run, type(exc).__name__, exc)
        if deps.stopped or state.limit_why or state.detector.tripped:
            # Stopped by a limit or the loop detector, its copy may be half done (a
            # stamp the skill saves first, and nothing else): never published.
            outcome = Outcome.STOPPED
        elif outcome == Outcome.DONE and state.evidence == 0:
            outcome, report = Outcome.NO_LOOK, ""
        self.trace.end_run(run, outcome=outcome.value, evidence=state.evidence, rounds=state.rounds,
                           error=state.limit_why or state.detector.tripped, **spent)
        log.info("audit run %s: %s (%s looks, %s rounds, $%.4f)", run, outcome.value, state.evidence,
                 state.rounds, spent["usd"])
        return RunResult(outcome, report, state.evidence)

    def report(self, text: str) -> None:
        """One `[Probe]` message to the main agent, kept beside the reader's
        (`mailbox.Message.keep`): it is the only record a person sees of a change
        nobody was asked about."""
        from probe.daemon import agent as agent_mod

        if not mailbox.enabled(source=self.w.session.source):
            # Its length, never its text: worker.log ships in debug logs and
            # diagnostic reports, and the report is about the researcher's work.
            log.info("audit report not delivered (no mailbox for %s): %d characters", self.w.session.source,
                     len(text))
            return
        msg = mailbox.Message(id=mailbox.new_message_id(), session=self.sid, kind=mailbox.Kind.MESSAGE,
                              text=agent_mod.AUDIT_REPORT_PREFIX + text, origin_turn=self.store.current_turn(),
                              keep=True)
        # Beside the reader's own messages, published: the worker shows a claimed
        # message only when this daemon recorded it (`Worker._read_reader_log`).
        with self.store.tx():
            self.store.add_read_message(message_id=msg.id, kind=msg.kind, text=msg.text, origin_turn=msg.origin_turn)
            self.store.mark_read_message_published(msg.id)
        mailbox.publish(msg)
