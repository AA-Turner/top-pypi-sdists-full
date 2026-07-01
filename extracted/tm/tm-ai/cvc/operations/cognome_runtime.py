"""
cvc.operations.cognome_runtime — Single shared memory interception point.

This module is the *only* place in CVC that knows how to turn a message list
into a memory-augmented message list.  Every LLM call in CVC — whether it
originates from the CLI agent, the proxy, the gateway, or a sub-agent —
goes through :meth:`CognomeRuntime.resolve_messages`.

The goal: the developer never types a memory command.  Memory is a
property of "using CVC", not a feature the user has to opt into.

Design invariants
-----------------
* **One runtime per workspace.**  Keyed by the absolute workspace root
  path.  Switching directories gives you a different runtime, rebuilt
  from that workspace's ``.cvc/`` state.  No cross-contamination.
* **Never raise.**  If memory resolution fails for any reason, the
  original messages are returned unchanged.  Memory is an enhancement,
  never a blocker.
* **Layer fallthrough.**  L2/L3 are additive refiners.  If they fail or
  are disabled, L1 still ships a correct Engram.  This runtime hides
  the layer selection from callers — they only see an Engram (or None).
* **Fast.**  L1 path is sub-millisecond on a 500-commit DAG.  Hard p95
  budget of 15ms is enforced by tests.
"""

from __future__ import annotations

import asyncio
import atexit
import logging
import threading
import time
import weakref
from pathlib import Path
from typing import TYPE_CHECKING, Any

from cvc.operations.cognome import CompiledEngram
from cvc.operations.engram_injectors import select_injector
from cvc.operations.handoff import DEFAULT_FILENAME, HandoffPackage, HandoffTurn
from cvc.operations.session_scratchpad import SessionScratchpad

if TYPE_CHECKING:
    from cvc.operations.cognome_manager import CognomeManager
    from cvc.operations.engine import CVCEngine

logger = logging.getLogger("cvc.operations.cognome_runtime")


class CognomeRuntime:
    """
    The single shared memory interception point for CVC.

    Obtain an instance via :meth:`for_engine` — it's keyed by workspace
    root path and reused across surfaces (CLI, proxy, gateway).

    Typical use (all surfaces call the same method)::

        runtime = CognomeRuntime.for_engine(engine)
        messages, engram = await runtime.resolve_messages(
            messages, workspace_id=str(workspace), provider=provider, model=model,
        )
        response = await adapter.complete(messages=messages, ...)
    """

    # Workspace root (resolved) → CognomeRuntime.  WeakValueDictionary so
    # runtimes for closed workspaces are GC'd.  Guarded by a lock so two
    # concurrent CLI instances on the same repo don't each build their own.
    _REGISTRY: "weakref.WeakValueDictionary[str, CognomeRuntime]" = weakref.WeakValueDictionary()
    _REGISTRY_LOCK = threading.Lock()

    # ------------------------------------------------------------------
    # Construction / registry
    # ------------------------------------------------------------------

    def __init__(self, engine: CVCEngine) -> None:
        self._engine = engine
        self._workspace_key = _workspace_key(engine)
        # Auto-init the CognomeManager — no manual `cvc cognome init` ever.
        try:
            mgr = engine.cognome
            if not mgr.is_initialised:
                mgr.init()
        except Exception as exc:  # pragma: no cover — defensive
            logger.debug("CognomeRuntime: init deferred (%s)", exc)
        # Phase 3: lazy session scratchpad — one per runtime (one
        # workspace == one session until process exit).
        self._scratchpad: SessionScratchpad | None = None
        # Phase 4: pending incoming handoff.  When set, the next
        # resolve_messages prepends a single synthetic system message
        # rendered from the package (one-shot — consumed on first use).
        self._pending_handoff: HandoffPackage | None = None
        # Phase 4 auto-wiring: check for an inbound handoff file and
        # stage it automatically.  Developers should never need to type
        # `cvc handoff import` for the common cases:
        #   1. CVC restart in the SAME workspace → picks up
        #      ``.cvc/last-handoff.json`` written by the previous exit.
        #   2. Drop-in file at the workspace root — ``.cvc-handoff.json``
        #      — typically copied over from another machine/workspace.
        self._auto_resume_handoff()
        # Register an at-exit hook that writes the session state back
        # to ``.cvc/last-handoff.json`` so the next CVC start in this
        # workspace resumes where the developer left off.
        self._atexit_registered = False
        self._register_auto_export()

    @classmethod
    def for_engine(cls, engine: CVCEngine) -> "CognomeRuntime":
        """Return the runtime for *engine*'s workspace (creating if needed)."""
        key = _workspace_key(engine)
        with cls._REGISTRY_LOCK:
            existing = cls._REGISTRY.get(key)
            if existing is not None:
                return existing
            runtime = cls(engine)
            cls._REGISTRY[key] = runtime
            return runtime

    @classmethod
    def _reset_registry_for_tests(cls) -> None:
        """Test hook: drop all cached runtimes."""
        with cls._REGISTRY_LOCK:
            cls._REGISTRY.clear()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def workspace_id(self) -> str:
        """Opaque, stable identifier for this runtime's workspace."""
        return self._workspace_key

    @property
    def manager(self) -> CognomeManager:
        """The underlying CognomeManager (L1 today; L2/L3 tomorrow)."""
        return self._engine.cognome

    @property
    def scratchpad(self) -> SessionScratchpad:
        """Lazy per-runtime session scratchpad (JSONL under .cvc/sessions)."""
        if self._scratchpad is None:
            try:
                root = self._engine.config.cvc_root
            except Exception:
                root = Path(self._workspace_key)
            self._scratchpad = SessionScratchpad(root)
            logger.debug(
                "scratchpad: session=%s ws=%s",
                self._scratchpad.session_id,
                self._workspace_key[:12],
            )
        return self._scratchpad

    def record_response_event(
        self,
        text: str,
        *,
        engram_hash: str | None = None,
        usage: dict[str, Any] | None = None,
        duration_ms: float | None = None,
    ) -> None:
        """
        Fire-and-forget observer hook for assistant responses.

        Safe to call from sync or async code.  Never raises.
        """
        try:
            sp = self.scratchpad
        except Exception:
            return
        payload = {
            "text": text[:2000],
            "engram_hash": engram_hash,
            "usage": usage or {},
            "duration_ms": duration_ms,
        }
        try:
            # If an event loop is running, schedule async.
            loop = asyncio.get_running_loop()
            loop.create_task(sp.record_response(**payload))
        except RuntimeError:
            # No running loop — write synchronously.
            sp.record_event_sync("assistant", **payload)
        except Exception as exc:  # pragma: no cover — defensive
            logger.debug("record_response_event failed: %s", exc)

    def is_active(self) -> bool:
        """
        True if memory injection should happen for this runtime.

        Considers both enable-state and the auto-inject config flag.
        """
        try:
            mgr = self._engine.cognome
            cfg = self._engine.config
            return bool(mgr.is_enabled and getattr(cfg, "cognome_auto_inject", True))
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Phase 4 — handoff export / import
    # ------------------------------------------------------------------

    def export_handoff(
        self,
        *,
        brief: str = "",
        max_turns: int = 20,
        max_commits: int = 10,
    ) -> HandoffPackage:
        """
        Build a :class:`HandoffPackage` from recent scratchpad turns and
        recent commits on the active branch.

        Safe to call with an empty scratchpad (returns a package with
        just the brief and commit list).  Never raises.
        """
        turns: list[HandoffTurn] = []
        try:
            events = self.scratchpad.read_all() if self._scratchpad_exists() else []
        except Exception as exc:  # pragma: no cover — defensive
            logger.debug("handoff: scratchpad read failed: %s", exc)
            events = []
        for ev in events:
            if ev.get("kind") != "user":
                continue
            turns.append(
                HandoffTurn(
                    query=str(ev.get("query", ""))[:400],
                    engram_hash=ev.get("engram_hash"),
                    engram_tokens=ev.get("engram_tokens"),
                    noeme_count=ev.get("noeme_count"),
                    provider=str(ev.get("provider", "")),
                    model=str(ev.get("model", "")),
                    ts=float(ev.get("ts", 0.0) or 0.0),
                )
            )
        turns = turns[-max_turns:]

        commits: list[str] = []
        branch_name: str | None = None
        try:
            branch_name = getattr(self._engine, "_active_branch", None)
            if branch_name:
                # Newest-first CognitiveCommit objects on the branch.
                rows = self._engine.db.index.list_commits(branch=branch_name, limit=max_commits)
                commits = [(c.message or "")[:200] for c in rows if c.message]
        except Exception as exc:  # pragma: no cover — best-effort
            logger.debug("handoff: commit enumeration failed: %s", exc)

        engram_hashes: list[str] = []
        try:
            rows = self._engine.db.index.list_cached_engrams(limit=5)
            engram_hashes = [r["engram_hash"] for r in rows]
        except Exception:  # pragma: no cover
            engram_hashes = []

        stats: dict[str, Any] = {}
        try:
            s = self._engine.cognome.status()
            stats = {
                "total_compiles": s.total_compiles,
                "total_tokens_saved": s.total_tokens_saved,
                "cached_engrams": s.cached_engrams,
                "version": s.version,
            }
        except Exception:  # pragma: no cover
            stats = {}

        return HandoffPackage(
            source_workspace=self._workspace_key,
            source_branch=branch_name,
            brief=brief,
            recent_turns=turns,
            recent_commits=commits,
            engram_hashes=engram_hashes,
            stats=stats,
        )

    def import_handoff(self, package: HandoffPackage) -> None:
        """
        Stage *package* for injection into the next ``resolve_messages``.

        Also writes a ``handoff`` event to the local scratchpad so the
        import is traceable.  Consumed on first use (one-shot).
        """
        self._pending_handoff = package
        try:
            self.scratchpad.record_event_sync(
                "handoff_import",
                source_workspace=package.source_workspace,
                source_branch=package.source_branch,
                turns=len(package.recent_turns),
                brief=package.brief[:400],
            )
        except Exception as exc:  # pragma: no cover — defensive
            logger.debug("handoff import scratchpad write failed: %s", exc)

    @property
    def pending_handoff(self) -> HandoffPackage | None:
        """The staged incoming handoff, if any (consumed on next resolve)."""
        return self._pending_handoff

    def _scratchpad_exists(self) -> bool:
        return self._scratchpad is not None or (self._engine.config.cvc_root / "sessions").exists()

    # ------------------------------------------------------------------
    # Phase 4 auto-wiring — zero-command developer UX
    # ------------------------------------------------------------------

    def _auto_resume_path(self) -> Path:
        """Per-workspace last-session handoff path (inside ``.cvc/``)."""
        return self._engine.config.cvc_root / "last-handoff.json"

    def _dropin_handoff_path(self) -> Path:
        """Root-level drop-in handoff file (sibling of ``.cvc/``)."""
        try:
            return self._engine.config.cvc_root.parent / DEFAULT_FILENAME
        except Exception:
            return Path.cwd() / DEFAULT_FILENAME

    def _auto_resume_handoff(self) -> None:
        """
        Auto-stage a handoff if one is sitting in either of the
        well-known locations.  Never raises.

        Precedence: drop-in root file > per-workspace last-handoff.
        Consumed files are renamed (not deleted) so the user can
        still inspect them if something went wrong.
        """
        # 1. Drop-in file at the workspace root (cross-workspace transport).
        try:
            dropin = self._dropin_handoff_path()
            if dropin.is_file():
                try:
                    pkg = HandoffPackage.read_from(dropin)
                    self._pending_handoff = pkg
                    archived = dropin.with_suffix(dropin.suffix + ".applied")
                    # Overwrite any stale archive so consecutive drops work.
                    if archived.exists():
                        archived.unlink()
                    dropin.rename(archived)
                    logger.info(
                        "cognome: auto-imported drop-in handoff (%s) — archived to %s",
                        dropin.name,
                        archived.name,
                    )
                    return
                except Exception as exc:
                    logger.warning(
                        "cognome: ignoring malformed drop-in handoff %s: %s", dropin, exc
                    )
        except Exception as exc:  # pragma: no cover — defensive
            logger.debug("auto-resume drop-in check failed: %s", exc)

        # 2. Same-workspace resume from prior session exit.
        try:
            last = self._auto_resume_path()
            if last.is_file():
                try:
                    pkg = HandoffPackage.read_from(last)
                    self._pending_handoff = pkg
                    # Keep the file — it's a recovery artefact; next exit
                    # will overwrite it with the newer session summary.
                    logger.info(
                        "cognome: auto-resumed last session (%d turns)",
                        len(pkg.recent_turns),
                    )
                except Exception as exc:
                    logger.debug("cognome: stale last-handoff %s (%s)", last, exc)
        except Exception as exc:  # pragma: no cover — defensive
            logger.debug("auto-resume last-handoff check failed: %s", exc)

    def _register_auto_export(self) -> None:
        """Install an ``atexit`` hook that writes ``last-handoff.json``."""
        if self._atexit_registered:
            return
        try:
            atexit.register(self._auto_export_on_exit)
            self._atexit_registered = True
        except Exception as exc:  # pragma: no cover — defensive
            logger.debug("atexit register failed: %s", exc)

    def _auto_export_on_exit(self) -> None:
        """
        Write a session snapshot to ``.cvc/last-handoff.json`` on exit.

        Skips writing if the session had no user activity at all
        (nothing to resume).  Never raises — exit path must be clean.
        """
        try:
            # Short-circuit if scratchpad has no user turns.
            if self._scratchpad is None:
                return
            had_activity = False
            try:
                for ev in self._scratchpad.read_all():
                    if ev.get("kind") == "user":
                        had_activity = True
                        break
            except Exception:
                return
            if not had_activity:
                return
            pkg = self.export_handoff(
                brief=f"Auto-resumed session (exited {time.strftime('%Y-%m-%d %H:%M:%S')})",
            )
            pkg.write_to(self._auto_resume_path())
            logger.debug("cognome: wrote last-handoff.json for next session")
        except Exception as exc:  # pragma: no cover — never break exit
            logger.debug("auto-export-on-exit failed: %s", exc)

    async def resolve_messages(
        self,
        messages: list[dict[str, Any]],
        *,
        workspace_id: str | None = None,
        provider: str = "",
        model: str = "",
        budget_tokens: int | None = None,
        branch: str | None = None,
        query: str | None = None,
    ) -> tuple[list[dict[str, Any]], CompiledEngram | None]:
        """
        Return ``(messages_with_memory, engram)`` for an LLM call.

        This is the only function every CVC surface needs.  The provider
        and model are accepted for future provider-specific injectors
        (Phase 2); today they are recorded for telemetry only.

        *messages*  — standard OpenAI-format message list (role/content).
        *query*     — optional explicit query.  If omitted, derived from
                      the last user message(s) via the manager's heuristic.

        Returns the original *messages* unchanged (and ``None``) if
        memory is disabled, the workspace mismatches, or any error
        occurs.  Never raises.
        """
        # Workspace guard — if a caller passes an explicit workspace_id
        # that doesn't match this runtime, refuse to inject.  Prevents
        # cross-workspace leaks in multi-tenant gateway flows.
        if workspace_id and workspace_id != self._workspace_key:
            logger.debug(
                "resolve_messages: workspace mismatch (runtime=%s, call=%s); skipping",
                self._workspace_key,
                workspace_id,
            )
            return messages, None

        if not messages:
            return messages, None

        # Phase 4: if an incoming handoff is staged, prepend its rendered
        # summary as a one-shot system message.  Consumed here so later
        # turns in the same session don't re-inject it.
        if self._pending_handoff is not None:
            try:
                handoff_text = self._pending_handoff.render_system_message()
                if handoff_text.strip():
                    messages = [
                        {"role": "system", "content": handoff_text},
                        *messages,
                    ]
            except Exception as exc:  # pragma: no cover — defensive
                logger.debug("handoff render failed: %s", exc)
            finally:
                self._pending_handoff = None

        if not self.is_active():
            return messages, None

        try:
            mgr = self._engine.cognome
            # Derive query if caller didn't pass one.
            resolved_query = (query or "").strip() or mgr.derive_query_from_messages(messages)
            if not resolved_query:
                return messages, None

            # Compile once, inject via provider-specific strategy.
            engram = mgr.compile(
                resolved_query,
                budget_tokens=budget_tokens,
                branch=branch,
            )
            if engram is None or not engram.preamble:
                return messages, None

            injector = select_injector(provider)
            updated = injector.inject(messages, engram)

            # Phase 3: fire-and-forget user-turn + engram event.  Any
            # failure here is swallowed — the scratchpad is instrumentation.
            try:
                asyncio.get_running_loop().create_task(
                    self.scratchpad.record_user(
                        resolved_query,
                        engram_hash=engram.engram_hash,
                        engram_tokens=engram.token_estimate,
                        noeme_count=engram.noeme_count,
                        provider=provider,
                        model=model,
                        branch=branch,
                    )
                )
            except RuntimeError:
                # Not inside an event loop — write inline.
                self.scratchpad.record_event_sync(
                    "user",
                    query=resolved_query,
                    engram_hash=engram.engram_hash,
                    engram_tokens=engram.token_estimate,
                    noeme_count=engram.noeme_count,
                    provider=provider,
                    model=model,
                    branch=branch,
                )
            except Exception as exc:  # pragma: no cover — defensive
                logger.debug("scratchpad record_user failed: %s", exc)

            logger.debug(
                "cognome.resolve_messages: +%d tok engram (provider=%s model=%s injector=%s) ws=%s",
                engram.token_estimate,
                provider or "-",
                model or "-",
                injector.name,
                self._workspace_key[:12],
            )
            return updated, engram
        except Exception as exc:
            # Memory must never break an LLM call.
            logger.warning("CognomeRuntime.resolve_messages failed (non-fatal): %s", exc)
            return messages, None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _workspace_key(engine: CVCEngine) -> str:
    """Stable key for a CVC workspace — resolved absolute CVC root."""
    try:
        root: Path = engine.config.cvc_root
        return str(root.resolve())
    except Exception:
        return str(getattr(engine.config, "cvc_root", "unknown"))
