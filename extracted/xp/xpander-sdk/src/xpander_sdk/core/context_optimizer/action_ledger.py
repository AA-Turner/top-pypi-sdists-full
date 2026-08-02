"""Durable, append-only record of every tool call's outcome.

The ledger is the load-bearing piece of the L2 robustness fix. Three
production failure modes — compaction loops, restart-after-finish, and
token starvation — all share a common cause: the LLM-generated
``<work_completed>`` block can omit durable side-effects (DB inserts,
file writes), and once the conversation is summarized the resuming agent
loses the only authoritative record of what already happened.

This module solves that by recording every tool call's *outcome* (write?
verify? what target? what result signature?) into a per-task ledger that:

* lives on ``task._xp_action_ledger`` (not on the optimizer — the optimizer
  is replaced on every retry, so optimizer-owned ledgers vanish across
  the very retry boundary Mode 2 needs to recover from);
* mirrors itself to the workspace as encrypted JSONL at
  ``CONTEXT_OPTIMIZATION/ledger_<task_id>.xp`` for cross-process
  recovery, reusing the same ``derive_key`` + ``encrypt`` pipeline as the
  session backup. Each ledger entry is encrypted independently so a
  partial / truncated file still yields recoverable lines;
* re-injects a compact ``<authoritative_ledger>`` block into the
  post-compaction continuation message so the resuming agent reads the
  list of confirmed writes/verifies as ground truth — the
  ``CONTINUATION_MESSAGE_TEMPLATE`` carries a binding rule forbidding
  re-invocation against ledger-confirmed targets.

The classifier (``ActionLedger.classify``) is intentionally conservative:
unknown tools default to ``READ``. That degrades to current behavior — the
detector simply finds no evidence — instead of risking a false-positive
finalize.
"""

from __future__ import annotations

import asyncio
import json
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from loguru import logger

from xpander_sdk.consts.api_routes import APIRoute
from xpander_sdk.core.context_optimizer.encryption import decrypt, derive_key, encrypt
from xpander_sdk.core.context_optimizer.helpers.secrets import (
    _redact_sensitive_payload,
    _redact_sensitive_text,
)
from xpander_sdk.core.context_optimizer.helpers.tool_result import (
    _head_tail_preview,
    unwrap_tool_result_content,
)
from xpander_sdk.core.context_optimizer.helpers.xml_safety import (
    _strip_illegal_xml_chars,
    _xml_attr_escape,
)
from xpander_sdk.core.xpander_api_client import APIClient
from xpander_sdk.models.action_ledger import LedgerEntry, LedgerEntryClass
from xpander_sdk.utils.event_loop import run_sync

# Inline preview budget for ledger entries — head/tail snippet keeps the
# salient bits at both ends (where the discriminating values usually live
# — leading identifiers, trailing status/signature) and elides the
# middle. 500 each side gives the resuming agent enough to identify the
# call without re-bloating context with multi-KB tool results.
_ARGS_HEAD = 500
_ARGS_TAIL = 500
_RESULT_HEAD = 500
_RESULT_TAIL = 500

# Cap on entries rendered into the authoritative-ledger block injected
# into the post-compaction continuation. Writes/verifies are preferred
# over reads, then most-recent-first.
_MAX_RENDERED_ENTRIES = 12
# Larger cap for high-context-window models (≥ 400K). On a 1M-window run
# we can afford to keep more individual ledger entries before falling back
# to per-tool group summaries, which avoids "agent restarts" symptoms on
# long bulk-classification jobs (PRO-1298 / Mercury).
_MAX_RENDERED_ENTRIES_LARGE_CONTEXT = 40
_LARGE_CONTEXT_THRESHOLD = 400_000
# When a (tool_name, status) group has more entries than this fraction of
# the per-render cap, collapse the tail into a single ``<entry_summary>``
# row stating total count + sample targets. Keeps the "I already did this
# for 47 targets" signal even when individual entries would otherwise be
# evicted.
_GROUP_DEDUP_FRACTION = 4

# Regex that pulls a numeric signature out of a tool result. Used by the
# default classifier to populate ``result_signature`` so the detector can
# cross-check write+verify counts. Tolerates plain ``key=N``, ``key: N``,
# and JSON ``"key": N`` shapes (the quote between the key and ``:`` is
# the common case for structured tool results once unwrapped to JSON).
_SIGNATURE_PATTERN = re.compile(
    r"(?i)[\"']?\b(rows?(?:[_-]?inserted|[_-]?affected)?|inserted|written|"
    r"created|deleted|count|total|exit(?:[_-]?code)?|status(?:[_-]?code)?|http)"
    r"[\"']?\s*[=:]\s*(\d+)"
)

# Tool-name patterns. Matched against the function name (lower-cased) and
# any ``operation`` field in the args. Order matters — first match wins.
# Custom tools that don't match fall through to READ, which is the safe
# default (see module docstring).
_WRITE_NAME_PATTERNS = (
    re.compile(r"insert", re.I),
    re.compile(r"write|create|update|patch|delete", re.I),
    re.compile(r"_post(?:_|$)|^post_|http[_-]?post", re.I),
    re.compile(r"file[_-]?write", re.I),
    re.compile(r"exec|run[_-]?sql", re.I),
)
_VERIFY_NAME_PATTERNS = (
    re.compile(r"^count|select[_-]?count|row[_-]?count", re.I),
    re.compile(r"head[_-]?", re.I),
    re.compile(r"file[_-]?stat|file[_-]?exists", re.I),
    re.compile(r"^get[_-]?|describe|show[_-]?tables|list[_-]?", re.I),
    re.compile(r"verify|validate|check", re.I),
)
_PLAN_TOOLS = frozenset(
    {
        "xpcreate_agent_plan",
        "xpget_agent_plan",
        "xpadd_new_agent_plan_item",
        "xpupdate_agent_plan_item",
        "xpdelete_agent_plan_item",
        "xpcomplete_agent_plan_items",
        "xpask_for_information",
        "xpstart_execution_plan",
    }
)
_INTERNAL_TOOLS = frozenset({"xpcompact_context", "xpfinalize_task"})


class ActionLedger:
    """Per-task append-only ledger of tool-call outcomes.

    Not threadsafe — agno tool hooks run serially per turn on a single
    asyncio loop. Mirror it for re-binding (via ``rebind(task)``) when a
    retry replaces the optimizer instance: the ledger lives on ``task``.
    """

    def __init__(self, agent: Any, task: Any) -> None:
        self.agent = agent
        self.task = task
        self._entries: List[LedgerEntry] = []
        self._next_seq: int = 1
        self._loaded: bool = False
        # Per-entry append queue — same non-blocking pattern Layer 1 uses
        # via ``WorkspaceCache``. Each ``aappend`` queues a single-line
        # ``file_write(mode="a")`` POST and returns immediately; the
        # actual HTTP round-trip happens in the background. ``aflush``
        # awaits all in-flight writes and surfaces the first failure.
        self._pending_writes: List[asyncio.Task] = []
        self._errors: List[BaseException] = []

    # ------------------------------------------------------------------ #
    #  Properties
    # ------------------------------------------------------------------ #

    @property
    def _workspace_enabled(self) -> bool:
        """Whether workspace persistence is allowed for this agent.

        Driven by ``Agent.workspace_tools_enabled``. When False, the in-memory
        ledger still works (it backs the authoritative continuation block) but
        no entries are persisted to / loaded from the workspace.
        """
        return bool(getattr(self.agent, "workspace_tools_enabled", True))

    @property
    def seq(self) -> int:
        """Highest assigned sequence number — used by the token-floor guard
        to detect "no new ledger entries since last compaction"."""
        return self._next_seq - 1

    @property
    def entries(self) -> List[LedgerEntry]:
        return list(self._entries)

    def writes(self) -> List[LedgerEntry]:
        return [e for e in self._entries if e.entry_class == LedgerEntryClass.WRITE]

    def verifies(self) -> List[LedgerEntry]:
        return [e for e in self._entries if e.entry_class == LedgerEntryClass.VERIFY]

    # ------------------------------------------------------------------ #
    #  Mutation
    # ------------------------------------------------------------------ #

    async def aappend(self, entry: LedgerEntry) -> None:
        """Append *entry* in memory and queue a background workspace write.

        Memory is authoritative for the current process. Workspace
        persistence runs via a per-entry ``file_write(mode="a")`` POST
        — mono's ``FileWriteTool`` exposes mode="a" for append (see
        ``agent_containers_images/agent_sandbox/tools/file_write_tool.py``).
        The write is enqueued through the optimizer's ``WorkspaceCache``
        so it shares the SAME barrier-flush semantics as L1 offload
        writes — any subsequent ``xpworkspace-*`` op that calls
        ``WorkspaceCache.aflush()`` will see ledger writes settle
        before bash/exec observes the workspace.
        """
        if entry.seq <= 0:
            entry = entry.model_copy(update={"seq": self._next_seq})
        self._next_seq = max(self._next_seq, entry.seq + 1)
        self._entries.append(entry)

        # Workspace disabled — in-memory append is authoritative; skip the POST.
        if not self._workspace_enabled:
            return

        try:
            payload = json.dumps(
                entry.model_dump_safe(), default=str, ensure_ascii=False
            )
            ciphertext = encrypt(payload, self._derive_key())
        except Exception as exc:
            logger.warning(f"[action-ledger] encrypt failed seq={entry.seq}: {exc}")
            return

        if not self.agent or not self.task:
            return
        cache = self._workspace_cache()
        if cache is not None:
            try:
                cache.enqueue_writeback(
                    name=f"action-ledger-append:{self.task.id}:{entry.seq}",
                    do_write_async=lambda c=ciphertext: self._do_workspace_append(c),
                )
                return
            except RuntimeError:
                # No running loop — caller is in sync context. Fall back
                # below; next ``aflush`` from an async context will retry.
                pass
        # Fallback (no optimizer cache reachable): own pending list.
        try:
            t = asyncio.create_task(
                self._do_workspace_append(ciphertext),
                name=f"action-ledger-append:{entry.seq}",
            )
            self._pending_writes.append(t)
        except RuntimeError:
            pass

    def append(self, entry: LedgerEntry) -> None:
        """Sync wrapper around :meth:`aappend`."""
        run_sync(self.aappend(entry))

    async def _do_workspace_append(self, ciphertext_line: str) -> None:
        """POST a single encrypted line to the ledger workspace file.

        Uses ``file_write`` with ``mode="a"`` — the canonical append
        path on mono's workspace sandbox. Each line is one independent
        encrypted entry so a partial-read recovery still yields
        well-formed entries.
        """
        if not self.agent or not self.task:
            return
        path = self._workspace_path()
        line = ciphertext_line + "\n"
        client = APIClient(configuration=self.agent.configuration)
        try:
            await client.make_request(
                path=str(APIRoute.WorkspaceToolInvoke).format(
                    agent_id=self.agent.id,
                    tool_name="file_write",
                ),
                method="POST",
                payload={"path": path, "content": line, "mode": "a"},
            )
        except BaseException as exc:
            self._errors.append(exc)
            logger.warning(f"[action-ledger] queued append failed: {exc}")

    # ------------------------------------------------------------------ #
    #  Load / drain
    # ------------------------------------------------------------------ #

    async def aload(self) -> None:
        """Rehydrate the in-memory list from the workspace JSONL file.

        No-op when the file is missing or empty — a fresh task. Errors are
        logged and suppressed so a corrupt workspace blob never blocks a
        task from running.

        Cross-process recovery only: same-process retries already have
        the ledger in ``task._xp_action_ledger``. The caller is expected
        to gate this on a prior-existence hint (compacted_context marker
        on task.additional_context, restart event, etc.) — calling on a
        fresh task triggers an unnecessary file_read round-trip that
        mono responds to with HTTP 500 (its missing-file shape).
        """
        if self._loaded or not self.agent or not self.task:
            return
        if not self._workspace_enabled:
            # No workspace file to rehydrate from.
            return
        # Don't flip ``_loaded`` until after a SUCCESSFUL read. Setting
        # it before the round-trip would suppress every later reload
        # attempt for the rest of the task on a single transient
        # failure (workspace cold start, network blip, auth hiccup),
        # silently dropping authoritative history on a restarted run.
        path = self._workspace_path()
        client = APIClient(configuration=self.agent.configuration)
        try:
            resp = await client.make_request(
                path=str(APIRoute.WorkspaceToolInvoke).format(
                    agent_id=self.agent.id,
                    tool_name="file_read",
                ),
                method="POST",
                payload={"path": path},
            )
        except Exception as exc:
            # Missing-ledger is the expected case on every fresh task —
            # stay silent and ALSO mark loaded so we don't retry the
            # 404 every turn. Higher-severity faults log at debug AND
            # leave ``_loaded`` False so a future attempt can retry.
            text = str(exc).lower()
            is_missing = "404" in text or "file not found" in text
            if is_missing:
                self._loaded = True
            else:
                logger.debug(f"[action-ledger] load skipped: {exc}")
            return
        self._loaded = True
        content = ""
        if isinstance(resp, dict):
            content = resp.get("content") or resp.get("result", "") or ""
        elif isinstance(resp, str):
            content = resp
        if not content:
            return
        key = self._derive_key()
        recovered = 0
        for raw_line in content.splitlines():
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            try:
                plaintext = decrypt(raw_line, key)
                obj = json.loads(plaintext)
                entry = LedgerEntry.model_validate(obj)
            except Exception as exc:
                logger.debug(f"[action-ledger] skip corrupt entry: {exc}")
                continue
            self._entries.append(entry)
            self._next_seq = max(self._next_seq, entry.seq + 1)
            recovered += 1
        if recovered:
            # Workspace appends are fire-and-forget so disk order is not
            # guaranteed to match seq order. Sort to restore chronology
            # so ``render_recent`` and evidence pairing observe the
            # correct sequence.
            self._entries.sort(key=lambda e: e.seq)
            logger.info(f"[action-ledger] rehydrated {recovered} entries from {path}")

    def load(self) -> None:
        run_sync(self.aload())

    async def aflush(self) -> None:
        """Drain queued workspace writes.

        Called from compaction barriers and task close. Each queued
        ``file_write(mode="a")`` task runs to completion or surfaces
        its error via ``_errors``. Mirrors ``WorkspaceCache.aflush``
        semantics — the first queued failure is re-raised exactly once
        per barrier, then the buffer is cleared.
        """
        if self._pending_writes:
            pending = self._pending_writes
            self._pending_writes = []
            await asyncio.gather(*pending, return_exceptions=True)

        if self._errors:
            err = self._errors[0]
            self._errors.clear()
            raise err

    async def aclose(self) -> None:
        try:
            await self.aflush()
        except BaseException as exc:
            logger.warning(f"[action-ledger] flush failed at close: {exc}")

    def close(self) -> None:
        run_sync(self.aclose())

    # ------------------------------------------------------------------ #
    #  Rendering
    # ------------------------------------------------------------------ #

    def render_authoritative_block(
        self,
        max_entries: Optional[int] = None,
        *,
        context_window: Optional[int] = None,
    ) -> str:
        """Render the ``<authoritative_ledger>`` block injected into the
        post-compaction continuation.

        Rendering invariants (PR #511 review):

        * **WRITE/VERIFY entries are never evicted.** They are the
          binding-rule referent — losing them lets the agent re-run a
          destructive op against the same target. They render in full,
          uncapped by ``max_entries``.
        * **Per-tool dedup groups by ``(tool_name, entry_class, status)``**
          — never merges semantically different operations (e.g. a
          ``sql_query`` that READ and a ``sql_query`` that UPDATEd stay
          in separate groups).
        * **``<entry_summary>`` always renders and carries ``class=``** so
          the resuming agent can tell whether the collapsed mass-operation
          was destructive.
        * ``max_entries`` is a soft cap on READ/PLAN/INTERNAL detail rows
          only. WRITE/VERIFY rows + summary rows render in addition.

        When more than ``max_entries // _GROUP_DEDUP_FRACTION`` entries
        share the same ``(tool_name, entry_class, status)``, the tail is
        collapsed into a single ``<entry_summary>`` row stating total
        count + sample targets. Preserves the "I already did this for
        N targets" signal on bulk-classification jobs.

        ``context_window`` bumps the soft cap to
        ``_MAX_RENDERED_ENTRIES_LARGE_CONTEXT`` for models with
        ``≥ _LARGE_CONTEXT_THRESHOLD`` tokens — 1M-window runs have
        plenty of room to keep more individual entries before falling
        back to compressed group rows.
        """
        if not self._entries:
            return ""
        if max_entries is None:
            if (
                context_window is not None
                and context_window >= _LARGE_CONTEXT_THRESHOLD
            ):
                max_entries = _MAX_RENDERED_ENTRIES_LARGE_CONTEXT
            else:
                max_entries = _MAX_RENDERED_ENTRIES
        # Priority within non-WRITE/VERIFY classes: internal/plan over reads.
        # WRITE/VERIFY are handled outside this priority map — they always
        # render in full and never compete for ``max_entries`` slots.
        priority: Dict[LedgerEntryClass, int] = {
            LedgerEntryClass.INTERNAL: 0,
            LedgerEntryClass.PLAN: 0,
            LedgerEntryClass.READ: 1,
        }
        write_verify_classes = {LedgerEntryClass.WRITE, LedgerEntryClass.VERIFY}

        # ---- Per-tool dedup ------------------------------------------- #
        # Group successful entries by (tool_name, entry_class, status).
        # Class is part of the key so ``ActionLedger.classify`` decisions
        # (which can give the same tool_name a WRITE class on one call and
        # a READ class on the next based on the operation arg) survive
        # rendering — a 30-READ + 1-WRITE batch must not collapse into a
        # single summary that hides the WRITE.
        dedup_threshold = max(2, max_entries // _GROUP_DEDUP_FRACTION)
        groups: Dict[Tuple[str, LedgerEntryClass, str], List[LedgerEntry]] = {}
        for e in self._entries:
            groups.setdefault((e.tool_name, e.entry_class, e.status), []).append(e)

        summary_rows: List[Tuple[int, str]] = []  # (anchor_seq, rendered_xml)
        eligible_entries: List[LedgerEntry] = []
        for (tool_name, entry_class, status), group in groups.items():
            if len(group) > dedup_threshold:
                # Keep first + last as representatives; collapse the
                # middle into a summary row anchored at the last seq.
                group_sorted = sorted(group, key=lambda e: e.seq)
                first = group_sorted[0]
                last = group_sorted[-1]
                eligible_entries.append(first)
                if last.seq != first.seq:
                    eligible_entries.append(last)
                # Sample up to 5 representative targets (deduped).
                seen_targets: List[str] = []
                for entry in group_sorted:
                    t = entry.target or ""
                    if t and t not in seen_targets:
                        seen_targets.append(t)
                    if len(seen_targets) >= 5:
                        break
                summary_rows.append(
                    (
                        last.seq,
                        f'<entry_summary tool="{_xml_attr_escape(tool_name)}" '
                        f'class="{entry_class.value}" '
                        f'status="{_xml_attr_escape(status)}" '
                        f'count="{len(group)}" '
                        f'first_seq="{first.seq}" '
                        f'last_seq="{last.seq}" '
                        f'sample_targets="{_xml_attr_escape("|".join(seen_targets))}"/>',
                    )
                )
            else:
                eligible_entries.extend(group)

        # ---- WRITE/VERIFY get unconditional render ------------------- #
        # These rows always emit in full; they're the binding-rule
        # referent and losing them masks destructive ops. ``max_entries``
        # bounds only the remaining detail (READ/PLAN/INTERNAL).
        wv_entries = [
            e for e in eligible_entries if e.entry_class in write_verify_classes
        ]
        other_entries = [
            e for e in eligible_entries if e.entry_class not in write_verify_classes
        ]
        # Soft cap applies to non-WRITE/VERIFY detail only.
        sortable = sorted(
            other_entries,
            key=lambda e: (priority.get(e.entry_class, 2), -e.seq),
        )
        chosen_other = sortable[:max_entries]
        chosen = wv_entries + chosen_other
        chosen.sort(key=lambda e: e.seq)  # render chronologically

        # Interleave entry rows + summary rows by seq order.
        rendered: List[Tuple[int, str]] = []
        for e in chosen:
            sig = e.result_signature or ""
            target = e.target or "—"
            rendered.append(
                (
                    e.seq,
                    f'<entry seq="{e.seq}" '
                    f'class="{e.entry_class.value}" '
                    f'tool="{_xml_attr_escape(e.tool_name)}" '
                    f'target="{_xml_attr_escape(target)}" '
                    f'status="{e.status}" '
                    f'signature="{_xml_attr_escape(sig)}" '
                    f'ts="{_xml_attr_escape(e.ts)}">'
                    f"<args>{_strip_illegal_xml_chars(e.args_preview)}</args>"
                    f"<result>{_strip_illegal_xml_chars(e.result_preview)}</result>"
                    f"</entry>",
                )
            )
        rendered.extend(summary_rows)
        rendered.sort(key=lambda row: row[0])
        rows = [xml for _, xml in rendered]
        return (
            "\n<authoritative_ledger>\n"
            "Verified record of tool calls executed earlier in this task.\n"
            'Treat WRITE entries with status="ok" as completed for that\n'
            "specific recorded operation - do NOT re-invoke the same tool\n"
            "with the same arguments against the same target. Distinct,\n"
            "plan-required mutations on the same target are still allowed.\n"
            "Use VERIFY entries to confirm a write succeeded before\n"
            "composing the final answer.\n"
            'An ``<entry_summary class="..." count="N" ...>`` row means the\n'
            "same tool ran N times with that class — treat all those calls\n"
            "as already completed for the listed sample_targets and any\n"
            "equivalents. Pay attention to ``class``: a summary with\n"
            'class="write" represents N destructive operations.\n'
            f"{chr(10).join(rows)}\n"
            "</authoritative_ledger>"
        )

    def render_recent(self, n: int = 5) -> str:
        """Compact narrative block for the ``<recent_actions>`` slot."""
        if not self._entries:
            return ""
        recent = self._entries[-n:]
        rows = []
        for idx, e in enumerate(recent, 1):
            rows.append(
                f'<action index="{idx}" tool="{_xml_attr_escape(e.tool_name)}" '
                f'status="{e.status}" timestamp="{_xml_attr_escape(e.ts)}">'
                f"<args>{_strip_illegal_xml_chars(e.args_preview)}</args>"
                f"<result>{_strip_illegal_xml_chars(e.result_preview)}</result>"
                f"</action>"
            )
        return (
            "\n<recent_actions>\n"
            f"The {len(rows)} most recent tool invocations (from action ledger).\n"
            f"{chr(10).join(rows)}\n"
            "</recent_actions>"
        )

    # ------------------------------------------------------------------ #
    #  Classification
    # ------------------------------------------------------------------ #

    @classmethod
    def classify(
        cls,
        tool_name: str,
        arguments: Any,
        result: Any,
    ) -> Tuple[LedgerEntryClass, Optional[str], Optional[str]]:
        """Map a tool call to ``(entry_class, target, result_signature)``.

        Conservative defaults: unknown tools → READ. The detector requires
        BOTH a WRITE and a matching VERIFY to declare evidence, so a
        misclassified write degrades to "no evidence found" rather than
        a false-positive finalize.
        """
        name = (tool_name or "").lower()
        if name in _INTERNAL_TOOLS:
            return LedgerEntryClass.INTERNAL, None, _extract_signature(result)
        if name in _PLAN_TOOLS:
            target = _extract_target_from_args(arguments) or _extract_plan_target(
                arguments
            )
            return LedgerEntryClass.PLAN, target, _extract_signature(result)

        target = _extract_target_from_args(arguments)
        signature = _extract_signature(result)

        op_field = _extract_op_field(arguments)
        haystacks = [name, op_field or ""]

        for hay in haystacks:
            for pat in _WRITE_NAME_PATTERNS:
                if pat.search(hay):
                    return LedgerEntryClass.WRITE, target, signature
        for hay in haystacks:
            for pat in _VERIFY_NAME_PATTERNS:
                if pat.search(hay):
                    return LedgerEntryClass.VERIFY, target, signature
        return LedgerEntryClass.READ, target, signature

    # ------------------------------------------------------------------ #
    #  Internals
    # ------------------------------------------------------------------ #

    def _derive_key(self) -> bytes:
        return derive_key(
            org_id=self.agent.configuration.organization_id,
            agent_id=self.agent.id,
            task_id=self.task.id,
        )

    def _workspace_cache(self) -> Any:
        """Return the optimizer's ``WorkspaceCache`` if reachable.

        Routes ledger writes through the shared write-queue/barrier so
        ledger flushes and L1 flushes settle in the same drain.
        """
        optimizer = getattr(self.task, "_xp_context_optimizer", None)
        if optimizer is None:
            return None
        cache = getattr(optimizer, "_workspace_cache", None)
        if cache is None:
            return None
        return cache

    def _workspace_path(self) -> str:
        # ``.xp`` matches ``is_context_optimization_file`` so the agno
        # tool hook auto-decrypts on agent reads. Internally still
        # encrypted JSONL — one ciphertext line per ledger entry.
        return f"CONTEXT_OPTIMIZATION/ledger_{self.task.id}.xp"


# ---------------------------------------------------------------------- #
#  Module helpers
# ---------------------------------------------------------------------- #


def attach_to_task(task: Any, agent: Any) -> ActionLedger:
    """Attach a fresh ledger to *task* (idempotent).

    Lives on ``task._xp_action_ledger`` so it survives optimizer
    replacement across plan retries (see ``events_module.py:486-492`` —
    the optimizer is detached on retry, but the task is not).
    """
    existing = getattr(task, "_xp_action_ledger", None)
    if isinstance(existing, ActionLedger):
        return existing
    ledger = ActionLedger(agent=agent, task=task)
    # Use ``object.__setattr__`` to bypass any Pydantic
    # extra-field restrictions on ``Task`` (matches the pattern used
    # for ``_xp_context_optimizer`` in ``_configure_context_optimizer``).
    # Falls back to plain ``setattr`` for non-pydantic stand-ins
    # (test SimpleNamespace etc.).
    try:
        object.__setattr__(task, "_xp_action_ledger", ledger)
    except (AttributeError, TypeError):
        try:
            setattr(task, "_xp_action_ledger", ledger)
        except Exception as exc:
            logger.warning(f"[action-ledger] attach failed: {exc}")
    return ledger


def get_attached_ledger(task: Any) -> Optional[ActionLedger]:
    ledger = getattr(task, "_xp_action_ledger", None)
    if isinstance(ledger, ActionLedger):
        return ledger
    return None


def build_entry_from_call(
    tool_name: str,
    arguments: Any,
    result: Any,
    *,
    status: str = "ok",
    tool_call_id: Optional[str] = None,
    workspace_offload_path: Optional[str] = None,
) -> LedgerEntry:
    """Build a fully-classified LedgerEntry from a tool invocation.

    Centralizes the redaction + head/tail trimming so callers (the agno
    hook, the SDK direct-invoke path) all produce identically-shaped
    entries. Sequence number is assigned on append.
    """
    # Unwrap the result so the classifier and signature extractor see
    # the actual payload, not the ToolInvocationResult / agno wrapper
    # ``tool_id=... result=...`` repr. Without this, structured returns
    # like ``{"count": 107}`` or ``ToolInvocationResult(result="rows_inserted=107")``
    # never expose the bare ``count=107`` / ``rows_inserted=107`` shape
    # to ``_extract_signature``, so ``result_signature`` stays empty
    # and the evidence detector misses valid WRITE/VERIFY pairs.
    unwrapped = unwrap_tool_result_content(result)
    entry_class, target, signature = ActionLedger.classify(
        tool_name, arguments, unwrapped
    )
    args_text = _safe_json(_redact_sensitive_payload(arguments))
    result_text = _redact_sensitive_text(_safe_str(unwrapped))
    return LedgerEntry(
        seq=0,
        ts=datetime.now(timezone.utc).isoformat(),
        tool_call_id=tool_call_id,
        tool_name=tool_name or "<unknown>",
        entry_class=entry_class,
        target=target,
        args_preview=_head_tail_preview(args_text, _ARGS_HEAD, _ARGS_TAIL),
        status="error" if status == "error" else "ok",
        result_preview=_head_tail_preview(result_text, _RESULT_HEAD, _RESULT_TAIL),
        result_signature=signature,
        workspace_offload_path=workspace_offload_path,
    )


# ---------------------------------------------------------------------- #
#  Private helpers
# ---------------------------------------------------------------------- #


def _safe_json(obj: Any) -> str:
    try:
        return json.dumps(obj, default=str, ensure_ascii=False)
    except Exception:
        return _safe_str(obj)


def _safe_str(obj: Any) -> str:
    if obj is None:
        return ""
    if isinstance(obj, str):
        return obj
    try:
        return json.dumps(obj, default=str, ensure_ascii=False)
    except Exception:
        return str(obj)


def _extract_op_field(arguments: Any) -> Optional[str]:
    """Pull a hint field from common arg shapes (``operation``, ``method``,
    ``action``, ``query``).  Used by the classifier for tools whose name
    is generic but whose args spell out the side effect."""
    if not isinstance(arguments, dict):
        return None
    payload = arguments.get("payload")
    if isinstance(payload, dict):
        body = payload.get("body_params")
        if isinstance(body, dict):
            for k in ("operation", "method", "action", "query"):
                v = body.get(k)
                if isinstance(v, str) and v:
                    return v
    for k in ("operation", "method", "action", "query"):
        v = arguments.get(k)
        if isinstance(v, str) and v:
            return v
    return None


def _extract_target_from_args(arguments: Any) -> Optional[str]:
    """Best-effort canonicalization of the call's target identifier.

    Looks at the most common arg shapes: ``path`` / ``file`` / ``filename``
    for filesystem ops, ``table`` / ``into`` for SQL, ``url`` / ``endpoint``
    for HTTP, then any ``id``/``name`` field for ID-based ops. Returns
    ``None`` when nothing canonical is found — a missing target just
    means the entry won't pair for evidence detection."""
    if not isinstance(arguments, dict):
        return None
    candidates = [arguments]
    payload = arguments.get("payload")
    if isinstance(payload, dict):
        candidates.append(payload)
        body = payload.get("body_params")
        if isinstance(body, dict):
            candidates.append(body)
    for src in candidates:
        for key in (
            "path",
            "file",
            "filename",
            "table",
            "into",
            "table_name",
            "url",
            "endpoint",
            "uri",
            "resource",
            "id",
            "name",
        ):
            v = src.get(key)
            if isinstance(v, str) and v:
                return v
    # Last resort: SQL-like body that names a table after INSERT INTO.
    for src in candidates:
        for key in ("query", "sql", "statement"):
            v = src.get(key)
            if isinstance(v, str) and v:
                m = re.search(
                    r"(?i)(?:into|from|update|table)\s+([\w\.\"`]+)",
                    v,
                )
                if m:
                    return m.group(1).strip('"`')
    return None


def _extract_plan_target(arguments: Any) -> Optional[str]:
    """For plan-management tools, target = first plan-item id mentioned."""
    if not isinstance(arguments, dict):
        return None
    for key in ("item_ids", "ids", "task_ids"):
        v = arguments.get(key)
        if isinstance(v, list) and v:
            first = v[0]
            if isinstance(first, str):
                return first
    payload = arguments.get("payload")
    if isinstance(payload, dict):
        body = payload.get("body_params")
        if isinstance(body, dict):
            for key in ("item_ids", "ids", "task_ids"):
                v = body.get(key)
                if isinstance(v, list) and v:
                    first = v[0]
                    if isinstance(first, str):
                        return first
    return None


def _extract_signature(result: Any) -> Optional[str]:
    """Pull a numeric signature out of the result text for evidence
    cross-checking. Returns ``"<key>=<int>"`` format strings."""
    text = _safe_str(result)
    if not text:
        return None
    # Take the first match — usually the most salient (e.g. "rows_written=N").
    m = _SIGNATURE_PATTERN.search(text)
    if not m:
        return None
    return f"{m.group(1).lower()}={m.group(2)}"
