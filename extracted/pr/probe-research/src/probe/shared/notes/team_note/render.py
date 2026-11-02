"""render the note into every harness's instruction file within its byte budget, remove it, and remember what failed."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from probe.shared.notes import superseded
from probe.foundation.durable.durable import file_lock, write_text_atomic
from probe.shared.updates.version_policy import state_dir


#: The budget one instruction file may occupy, applied to BOTH harnesses.
#:
#: Codex documents 32 KiB (`project_doc_max_bytes`) for its WHOLE instruction
#: chain -- the global AGENTS.md plus every repo's own file walking down -- and
#: it stops adding files once that fills, so an oversized note silently starves
#: a repository's own build and test rules. Claude Code publishes no equivalent
#: cap, but an unbounded note is the same harm paid in tokens instead of missing
#: context, and matching the numbers means the degrade path is exercised on both
#: harnesses rather than being untested code on one.
INSTRUCTION_FILE_MAX_BYTES = 32_768

#: Where a render failure waits to be reported. The render runs in the
#: background off a Stop/SessionEnd hook, which has no channel to the model at
#: the moment it runs -- so "fail loudly" means recording here and letting the
#: NEXT session start say it out loud. Without this the loud failure is silent
#: in practice, which is the bug this whole change exists to stop.
RENDER_FAILURE_FILE = "render-failures.json"

#: Both harnesses, always. One sync renders both, because each harness's local
#: copy otherwise only refreshes when THAT harness runs -- measured on a shared
#: box: the Claude copy 7 hours fresher than the Codex copy and five sections
#: ahead of it, with neither agent able to tell.
def _render_sources() -> tuple[str, ...]:
    from probe.foundation.harness_registry import get_registry

    return tuple(h.id for h in get_registry().all() if h.team_note == "render")


RENDER_SOURCES = _render_sources()


@dataclass(frozen=True, slots=True)
class RenderReport:
    """What one render pass did, per harness."""

    written: tuple[str, ...] = ()
    unchanged: tuple[str, ...] = ()
    pointer_only: tuple[str, ...] = ()
    failures: tuple[str, ...] = ()
    #: Harnesses whose RESEARCH-TRACKING block was older than this CLI and got
    #: rewritten on the way past. Separate from `written`, which is the team
    #: note: the two blocks share a file and a lock but not a lifecycle, and an
    #: operator asking "did the new guidance land?" is asking about this one.
    rules_refreshed: tuple[str, ...] = ()
    #: Harnesses whose file carries no pointer block (the agent-rules opt-out),
    #: so the note was not rendered there; `removed` also took an old note out.
    opted_out: tuple[str, ...] = ()
    removed: tuple[str, ...] = ()
    #: Harnesses whose file carries no team-note block because this computer's
    #: workspace limit hides team-wide items (`hidden_by_limit`); a block that was
    #: there was taken out.
    hidden: tuple[str, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.failures


def hidden_by_limit(settings) -> bool:
    """Does this computer's workspace limit hide team-wide items (the team note
    among them)? Then the note is neither synced nor rendered, and its managed
    block leaves the instruction files; the local document stays on disk and syncs
    again once they show (`probe workspace limit`, `probe.sdk.settings.workspace_limit`)."""
    limit = getattr(settings, "workspace_limit", None)
    return limit is not None and limit.hides_team_items


#: `probe notes sync`'s `detail` while team-wide items are hidden.
HIDDEN_DETAIL = (
    "not synced: this computer's workspace limit hides team-wide items, the team note "
    "among them (`probe workspace limit <workspace> --team-items show` shows them)"
)


def remove_blocks(sources: tuple[str, ...] | None = None) -> list[str]:
    """Take the team-note block out of every harness's instruction file, leaving
    the pointer block and everything else alone. Returns the harnesses whose file
    changed. A damaged or unreadable file is left untouched (the next render
    reports it)."""
    from probe.cli.wizard.apply import agent_rules

    removed: list[str] = []
    for source in RENDER_SOURCES if sources is None else sources:
        try:
            instruction = agent_rules.memory_path(source)
            with file_lock(instruction_lock_path(instruction)):
                if agent_rules.remove(instruction, spec=agent_rules.NOTE_BLOCK):
                    removed.append(source)
        except (agent_rules.DamagedBlock, OSError, UnicodeDecodeError):
            continue
    return removed


def instruction_lock_path(instruction: Path) -> Path:
    """A lock keyed on the FILE being written, not on the credential.

    `Paths.lock` is keyed on origin+identity because the base copy and version
    are per-credential -- correct for the sync, wrong for this. The instruction
    file is user-global: `~/.claude/CLAUDE.md` is the same path whatever
    credential is resolved, so two contexts on one machine take two DIFFERENT
    locks and write the SAME file. The lock has to name what it protects.
    """
    digest = hashlib.sha256(str(instruction.resolve()).encode("utf-8")).hexdigest()[:16]
    return state_dir() / "team-note" / "locks" / f"{digest}.lock"


def render_failure_path() -> Path:
    return state_dir() / "team-note" / RENDER_FAILURE_FILE


def _record_failures(failures: list[str]) -> None:
    """Persist (or clear) what the next session should say out loud."""
    path = render_failure_path()
    try:
        if not failures:
            path.unlink(missing_ok=True)
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        write_text_atomic(path, json.dumps({"failures": failures}, indent=2) + "\n")
    except OSError:
        # Recording the failure must never itself become one.
        pass


def pending_render_failures() -> list[str]:
    """What the last render could not do, for the next session to report."""
    try:
        payload = json.loads(render_failure_path().read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    # A status file that is valid JSON but not an object (a bare list, a string)
    # made `.get` raise AttributeError, which is not a ValueError and so escaped
    # the guard above -- turning "cannot read my own status file" into a crash
    # in the one path whose whole job is to fail open.
    if not isinstance(payload, dict):
        return []
    found = payload.get("failures")
    return [str(item) for item in found] if isinstance(found, list) else []


def _utf8_len(value: str) -> int:
    """BYTES, not code points. `project_doc_max_bytes` is a byte budget and this
    file is full of em-dashes and middots, so measuring `len(str)` under-counts
    every non-ASCII character by one to three bytes -- silently, and in the
    direction that overruns the cap."""
    return len(value.encode("utf-8"))


def _fits(existing: str, block: str, span: tuple[int, int] | None) -> bool:
    """Would `block` fit the budget once it replaces whatever is there now?"""
    replaced = _utf8_len(existing[span[0] : span[1]]) if span else 0
    without = _utf8_len(existing) - replaced
    return without + _utf8_len(block) <= INSTRUCTION_FILE_MAX_BYTES


def render_blocks(text: str, *, settings, sources: tuple[str, ...] | None = None) -> RenderReport:
    """Render the note into every harness's instruction file.

    THE LOCK IS NOT HELD ACROSS THE NETWORK -- the caller has already fetched;
    this function only reads, renders and writes files. `Paths.lock` is keyed on
    origin and credential rather than on harness, so one acquisition genuinely
    covers both files and a half-rendered pair cannot exist.

    Three outcomes per harness, in order: the block already says exactly this
    (skip, no write, no lock contention beyond the read); the full note fits
    (write it); it does not (write a POINTER instead, never a truncated note --
    partial content under a header that calls itself a copy of the team note
    reads as complete, and the reader has no way to tell). If even the pointer
    does not fit, refuse and record it: the file is too full for us, and saying
    so is more use than silently making a repository's own rules disappear.

    A damaged block is left ALONE, never repaired. Auto-repair of a file humans
    also edit destroys edits it did not understand.
    """
    sources = RENDER_SOURCES if sources is None else sources
    from probe.cli.wizard.apply import agent_rules

    body = text.strip()
    # Hidden team items render nothing, so a body that cannot render is moot.
    conflict = None if hidden_by_limit(settings) else agent_rules.note_body_conflict(body)
    if conflict:
        # UNRENDERABLE, not fixable: _find_block counts marker occurrences, so a
        # marker inside the body makes the file unparseable wherever we put it.
        # Refuse for every harness and say why, rather than rewriting the team's
        # own prose without being asked.
        failures = [f"{source}: {conflict}" for source in sources]
        _record_failures(failures)
        return RenderReport(failures=tuple(failures))

    # The FILE keeps its verbatim bytes — edits round-trip against the file, so
    # it must never be normalized. The BLOCK renders the COLLAPSED form: a
    # struck claim stops costing every session's context the moment it is
    # struck, instead of only when someone physically deletes it. Idempotent,
    # and byte-identical to the note when no marker exists.
    display = superseded.collapse(body)

    # NO PRIOR MEASUREMENT IS READ HERE ANY MORE. This render used to load the
    # last one to derive the audit advisory it embedded; the advisory left the
    # block (see below), and `_record_health` reads the file itself for the
    # churn baseline it carries forward. The reason the audit trigger still
    # wants the PREVIOUS render's numbers is unchanged -- a measurement of the
    # block this render is composing cannot describe it -- but that read now
    # happens in `advisory_for_source`, on the hook's side.

    written: list[str] = []
    unchanged: list[str] = []
    pointer_only: list[str] = []
    failures: list[str] = []
    rules_refreshed: list[str] = []
    opted_out: list[str] = []
    removed: list[str] = []
    hidden: list[str] = []
    hide = hidden_by_limit(settings)
    health: dict[str, dict[str, object]] = {}

    for source in sources:
        try:
            where = paths_for(settings)
            instruction = agent_rules.memory_path(source)
            document = str(where.document)
        except Exception as exc:  # noqa: BLE001 - a path we cannot resolve is a failure to report
            failures.append(f"{source}: cannot resolve paths ({exc})")
            continue

        # THE BLOCK CARRIES NO ADVISORY. It used to: the audit line was written
        # in here so the reminder rode the note it was about. But this file is
        # read by every session of this harness -- `claude -p`, `codex exec`, a
        # cron job, a subagent -- and none of those can be asked to spend a
        # background agent on a cleanup, or be trusted to still exist when one
        # finishes. Presence is knowable only where a prompt is submitted, so
        # the line moved to the UserPromptSubmit hook, which asks
        # `probe notes audit-advisory` for exactly this text.
        #
        # `render_note_block` keeps its `advisory` parameter: the pointer form
        # and the hash still have to handle one, and the hook's text is composed
        # from the same function this render used to call.
        full = agent_rules.render_note_block(display, document=document)
        # The POINTER still stamps the source body's hash. Stamping an empty
        # body made `note_block_is_current` -- which hashes the real body --
        # never match, so every sync re-rendered on exactly the machines that
        # are over budget, which is now the common case.
        pointer = agent_rules.render_note_block(
            display, document=document, pointer_only=True
        )

        try:
            with file_lock(instruction_lock_path(instruction)):
                # THE POINTER BLOCK RIDES THIS SYNC, and that is the only thing
                # that keeps it current. It is written once by the wizard and
                # was refreshed only by `probe rules refresh` run BY HAND, so a
                # POINTER_VERSION bump reached nobody: shipping a new CLI left
                # every machine on whatever block its wizard run installed.
                # Observed cost: guidance added in one release was still absent
                # from live sessions days later, and agents did the thing it
                # existed to prevent. This sync already runs on every Stop,
                # already resolves every configured harness, and already holds
                # this file's lock -- so the refresh costs one version read.
                #
                # BEFORE the note render, deliberately: the note is the part
                # that gets degraded or skipped when the file is over budget,
                # and the standing instructions must not be held hostage to a
                # long note.
                # Its OWN handler: a damaged pointer block must not be reported
                # as a damaged team-note block, and must not stop the note from
                # rendering. The two blocks have different markers, so one being
                # unreadable says nothing about the other.
                rules_state = agent_rules.POINTER_CURRENT
                try:
                    rules_state = agent_rules.refresh_pointer(instruction)
                    if rules_state == agent_rules.POINTER_REFRESHED:
                        rules_refreshed.append(source)
                except agent_rules.DamagedBlock as exc:
                    failures.append(
                        f"{source}: {instruction.name} has a damaged research-tracking block "
                        f"({exc}); left untouched"
                    )

                # NO POINTER, NO NOTE. An absent pointer block is the opt-out
                # (`--no-agent-rules`, or Settings unticked), and the note is a
                # managed block in the same global file: rendering it anyway put
                # Probe's text in the CLAUDE.md of a customer who had declined
                # it (2026-10-02), and in an AGENTS.md for a Codex that machine
                # never had. A note left from before the opt-out goes too. A
                # DAMAGED pointer is still someone's opt-in, so it renders.
                if rules_state == agent_rules.POINTER_ABSENT:
                    if agent_rules.remove(instruction, spec=agent_rules.NOTE_BLOCK):
                        removed.append(source)
                    else:
                        opted_out.append(source)
                    continue

                # TEAM ITEMS HIDDEN by this computer's workspace limit: the note
                # is one of them, so its block goes and is not put back until
                # they show again (the pointer above is not a team item: it stays
                # current either way).
                if hide:
                    agent_rules.remove(instruction, spec=agent_rules.NOTE_BLOCK)
                    hidden.append(source)
                    continue

                existing = ""
                if instruction.exists():
                    existing = instruction.read_text(encoding="utf-8")
                span = agent_rules._find_block(existing, agent_rules.NOTE_BLOCK)

                # Measured against the room this file actually has, which is
                # the number the pointer decision below is made from.
                replaced = _utf8_len(existing[span[0] : span[1]]) if span else 0
                available = INSTRUCTION_FILE_MAX_BYTES - (_utf8_len(existing) - replaced)
                health[source] = {
                    "block_bytes": _utf8_len(full),
                    "available_bytes": available,
                    "pct": round(_utf8_len(full) / available, 4) if available > 0 else 999.0,
                }

                if _fits(existing, full, span):
                    block, degraded = full, False
                elif _fits(existing, pointer, span):
                    block, degraded = pointer, True
                else:
                    health[source]["degraded"] = True
                    failures.append(
                        f"{source}: {instruction.name} is too full for the team-note block "
                        f"({len(existing)}B of {INSTRUCTION_FILE_MAX_BYTES}B); compact it and the "
                        f"note will render on the next sync"
                    )
                    continue
                health[source]["degraded"] = degraded

                # ASKED AFTER THE FORM IS CHOSEN, and inside the lock. Before
                # the form was known the check could not tell a current pointer
                # from a stale one; outside the lock it was a time-of-check race
                # against another process replacing the block.
                if agent_rules.note_block_is_current(
                    instruction, display, document, pointer_only=degraded
                ):
                    unchanged.append(source)
                    continue

                agent_rules.install(instruction, spec=agent_rules.NOTE_BLOCK, block=block)
        except agent_rules.DamagedBlock as exc:
            failures.append(f"{source}: {instruction.name} has a damaged team-note block ({exc}); left untouched")
            continue
        except (OSError, UnicodeDecodeError) as exc:
            # UnicodeDecodeError is a ValueError, NOT an OSError -- the same trap
            # `apply_agent_rules` already documents. One latin-1 byte in a
            # researcher's own CLAUDE.md would otherwise escape this handler,
            # skip the failure record, and leave the other harness unrendered.
            failures.append(f"{source}: cannot write {instruction} ({exc})")
            continue

        (pointer_only if degraded else written).append(source)

    _record_failures(failures)
    _record_health(health, body)
    return RenderReport(
        written=tuple(written),
        unchanged=tuple(unchanged),
        pointer_only=tuple(pointer_only),
        failures=tuple(failures),
        rules_refreshed=tuple(rules_refreshed),
        opted_out=tuple(opted_out),
        removed=tuple(removed),
        hidden=tuple(hidden),
    )
from probe.shared.notes.team_note.audit import _record_health  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.notes.team_note.team_note import paths_for  # noqa: E402 -- pieces need each other; the front door loads this one first
