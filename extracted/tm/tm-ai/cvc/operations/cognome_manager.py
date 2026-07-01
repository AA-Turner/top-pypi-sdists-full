"""
cvc.operations.cognome_manager — Full COGNOME lifecycle management.

This module owns the lifecycle of the COGNOME substrate: initialisation,
enable/disable, status reporting, Engram caching, injection orchestration,
and audit trail.  It sits between the compiler (:mod:`cvc.operations.cognome`)
and the consumer layers (proxy, gateway, MCP, CLI).

The manager is workspace-scoped — each CVC workspace has at most one active
COGNOME.  State is persisted in the ``cognome_state`` SQLite table so it
survives process restarts.

Layer architecture:

    L1 (heuristic compiler)   — pure code, deterministic, always available
    L2 (learned soft-prompt)  — tiny model trained during idle time (future)
    L3 (LoRA delta)           — optional GPU fine-tune (future)

L2 and L3 are additive refinements on top of L1's selection.  This manager
coordinates all layers but currently only L1 is active.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field

from cvc.operations.cognome import CognomeCompiler, CompiledEngram

if TYPE_CHECKING:
    from cvc.core.database import ContextDatabase
    from cvc.core.models import CVCConfig

logger = logging.getLogger("cvc.operations.cognome_manager")


# ---------------------------------------------------------------------------
# State keys stored in cognome_state table
# ---------------------------------------------------------------------------

_K_ENABLED = "enabled"  # "true" / "false"
_K_VERSION = "version"  # monotonic int, bumped on each train epoch
_K_LAST_COMPILE_AT = "last_compile_at"
_K_LAST_TRAIN_AT = "last_train_at"
_K_TOTAL_COMPILES = "total_compiles"
_K_TOTAL_TOKENS_SAVED = "total_tokens_saved"
_K_ACTIVE_LAYER = "active_layer"  # "L1" | "L2" | "L3"
_K_INIT_AT = "init_at"


# ---------------------------------------------------------------------------
# Status model
# ---------------------------------------------------------------------------


class CognomeStatus(BaseModel):
    """Snapshot of the COGNOME's current state, suitable for CLI/MCP display."""

    initialised: bool = False
    enabled: bool = True
    active_layer: str = "L1"
    version: int = 0
    total_compiles: int = 0
    total_tokens_saved: int = 0
    cached_engrams: int = 0
    last_compile_at: float | None = None
    last_train_at: float | None = None
    init_at: float | None = None
    budget_tokens: int = 1200


class CognomeAuditEntry(BaseModel):
    """One row in the COGNOME audit trail."""

    engram_hash: str
    query: str
    token_estimate: int
    baseline_tokens: int
    compression: float
    source_commits: list[str] = Field(default_factory=list)
    created_at: float = 0.0
    use_count: int = 0


# ---------------------------------------------------------------------------
# Manager
# ---------------------------------------------------------------------------


class CognomeManager:
    """
    Full lifecycle manager for the COGNOME substrate.

    Create one per workspace via :meth:`CVCEngine.cognome_manager` (or
    directly for testing).

    Usage::

        mgr = CognomeManager(db, config)
        mgr.init()                     # bootstrap state (idempotent)

        engram = mgr.compile("fix the auth bug", budget_tokens=800)
        # → CompiledEngram ready for injection

        status = mgr.status()
        mgr.disable()
        mgr.enable()
    """

    def __init__(self, db: ContextDatabase, config: CVCConfig) -> None:
        self.db = db
        self.config = config
        self._compiler: CognomeCompiler | None = None

    # ------------------------------------------------------------------
    # Init / teardown
    # ------------------------------------------------------------------

    def init(self) -> CognomeStatus:
        """
        Bootstrap the COGNOME for this workspace (idempotent).

        Sets default state keys if they don't already exist.  Returns
        the current status.
        """
        idx = self.db.index
        if idx.get_cognome_state(_K_INIT_AT) is None:
            now = str(time.time())
            idx.set_cognome_state(_K_INIT_AT, now)
            idx.set_cognome_state(_K_ENABLED, "true")
            idx.set_cognome_state(_K_VERSION, "0")
            idx.set_cognome_state(_K_ACTIVE_LAYER, "L1+L2+L3")
            idx.set_cognome_state(_K_TOTAL_COMPILES, "0")
            idx.set_cognome_state(_K_TOTAL_TOKENS_SAVED, "0")
            logger.info("COGNOME initialised for workspace %s", self.config.cvc_root)
        return self.status()

    @property
    def is_initialised(self) -> bool:
        return self.db.index.get_cognome_state(_K_INIT_AT) is not None

    @property
    def is_enabled(self) -> bool:
        if not self.is_initialised:
            return False
        val = self.db.index.get_cognome_state(_K_ENABLED)
        return val != "false"

    # ------------------------------------------------------------------
    # Enable / disable
    # ------------------------------------------------------------------

    def enable(self) -> CognomeStatus:
        """Enable COGNOME injection."""
        self._ensure_init()
        self.db.index.set_cognome_state(_K_ENABLED, "true")
        logger.info("COGNOME enabled")
        return self.status()

    def disable(self) -> CognomeStatus:
        """Disable COGNOME injection (no Engrams compiled or injected)."""
        self._ensure_init()
        self.db.index.set_cognome_state(_K_ENABLED, "false")
        logger.info("COGNOME disabled")
        return self.status()

    # ------------------------------------------------------------------
    # Compile
    # ------------------------------------------------------------------

    def compile(
        self,
        query: str,
        *,
        budget_tokens: int | None = None,
        branch: str | None = None,
        use_cache: bool = True,
    ) -> CompiledEngram:
        """
        Compile an Engram for *query*.

        If the COGNOME is disabled or uninitialised, returns an empty Engram.
        Checks the SQLite cache first if *use_cache* is True.
        """
        budget = budget_tokens or self.config.cognome_budget_tokens

        if not self.is_enabled:
            return _empty_engram(query, budget)

        # Cache invalidation is implicit via the version counter — every
        # time a new commit lands we bump _K_VERSION, which changes the
        # cache key for every query+budget+branch combo.  No explicit
        # DELETE required; stale rows are pruned lazily by prune_cache().
        version = int(self.db.index.get_cognome_state(_K_VERSION) or "0")

        # Check cache: hash(query + budget + branch + version) → cached preamble
        if use_cache:
            cache_key = self._cache_key(query, budget, branch, version)
            cached = self.db.index.get_cached_engram(cache_key)
            if cached is not None:
                logger.debug("cognome cache HIT for %r", query)
                return CompiledEngram(
                    preamble=cached["preamble"],
                    query=query,
                    source_commits=json.loads(cached["source_commits"]),
                    noeme_count=cached["noeme_count"],
                    token_estimate=cached["token_estimate"],
                    baseline_token_estimate=cached["baseline_tokens"],
                    compression_ratio=cached["compression"],
                    budget_tokens=cached["budget_tokens"],
                    engram_hash=cached["engram_hash"],
                    created_at=cached["created_at"],
                )

        # Compile fresh
        compiler = self._get_compiler()
        engram = compiler.compile(query, budget_tokens=budget, branch=branch)

        # Update stats
        self._bump_stats(engram)

        # Cache the result
        if use_cache and engram.preamble:
            self.db.index.cache_engram(
                engram_hash=self._cache_key(query, budget, branch, version),
                query=query,
                preamble=engram.preamble,
                source_commits=engram.source_commits,
                noeme_count=engram.noeme_count,
                token_estimate=engram.token_estimate,
                baseline_tokens=engram.baseline_token_estimate,
                compression=engram.compression_ratio,
                budget_tokens=engram.budget_tokens,
                branch=branch,
            )

        return engram

    # ------------------------------------------------------------------
    # Commit hook
    # ------------------------------------------------------------------

    def on_commit(self, commit_hash: str | None = None) -> None:
        """
        Called by :meth:`CVCEngine.commit` immediately after a new
        commit advances HEAD.

        Bumps the COGNOME version counter, which invalidates every
        cached Engram on the next compile.  This is the unified,
        deterministic cache-invalidation hook — no surgical queries,
        no stale noemata.
        """
        if not self.is_initialised:
            return
        try:
            current = int(self.db.index.get_cognome_state(_K_VERSION) or "0")
            self.db.index.set_cognome_state(_K_VERSION, str(current + 1))
            logger.debug(
                "cognome: cache invalidated for commit %s (v=%d)",
                (commit_hash or "")[:12],
                current + 1,
            )
        except Exception as exc:  # pragma: no cover — defensive
            logger.debug("on_commit bump failed: %s", exc)

    # ------------------------------------------------------------------
    # Status & audit
    # ------------------------------------------------------------------

    def status(self) -> CognomeStatus:
        """Return the current COGNOME status snapshot."""
        idx = self.db.index
        if not self.is_initialised:
            return CognomeStatus(
                initialised=False,
                budget_tokens=self.config.cognome_budget_tokens,
            )

        cached_count = len(idx.list_cached_engrams(limit=1000))

        # Report the *runtime-effective* layer stack rather than the
        # value persisted at init time, so existing workspaces upgraded
        # to a newer CVC reflect the new layers without any re-init.
        active_parts = ["L1"]
        if getattr(self.config, "cognome_l2_enabled", True):
            active_parts.append("L2")
        if getattr(self.config, "cognome_l3_enabled", True):
            active_parts.append("L3")
        active_layer = "+".join(active_parts)

        return CognomeStatus(
            initialised=True,
            enabled=self.is_enabled,
            active_layer=active_layer,
            version=int(idx.get_cognome_state(_K_VERSION) or "0"),
            total_compiles=int(idx.get_cognome_state(_K_TOTAL_COMPILES) or "0"),
            total_tokens_saved=int(idx.get_cognome_state(_K_TOTAL_TOKENS_SAVED) or "0"),
            cached_engrams=cached_count,
            last_compile_at=_float_or_none(idx.get_cognome_state(_K_LAST_COMPILE_AT)),
            last_train_at=_float_or_none(idx.get_cognome_state(_K_LAST_TRAIN_AT)),
            init_at=_float_or_none(idx.get_cognome_state(_K_INIT_AT)),
            budget_tokens=self.config.cognome_budget_tokens,
        )

    def audit(self, limit: int = 20) -> list[CognomeAuditEntry]:
        """Return recent Engram compilations from the cache."""
        rows = self.db.index.list_cached_engrams(limit=limit)
        return [
            CognomeAuditEntry(
                engram_hash=r["engram_hash"],
                query=r["query"],
                token_estimate=r["token_estimate"],
                baseline_tokens=r["baseline_tokens"],
                compression=r["compression"],
                source_commits=json.loads(r["source_commits"])
                if isinstance(r["source_commits"], str)
                else r["source_commits"],
                created_at=r["created_at"],
                use_count=r["use_count"],
            )
            for r in rows
        ]

    def prune_cache(self, max_age_days: int = 7, max_entries: int = 200) -> int:
        """Evict stale or excess cached Engrams."""
        return self.db.index.prune_engram_cache(
            max_age_seconds=max_age_days * 86400,
            max_entries=max_entries,
        )

    # ------------------------------------------------------------------
    # Injection helpers (used by proxy/gateway)
    # ------------------------------------------------------------------

    def inject_engram_into_messages(
        self,
        messages: list[dict[str, Any]],
        query: str,
        *,
        budget_tokens: int | None = None,
        branch: str | None = None,
    ) -> tuple[list[dict[str, Any]], CompiledEngram | None]:
        """
        Compile an Engram and prepend it as a system message.

        Returns ``(updated_messages, engram)`` where *engram* is ``None``
        if COGNOME is disabled or the Engram is empty.

        This is the primary hook for proxy.py and gateway.py — call it
        before ``adapter.complete()`` and pass the updated messages through.
        """
        if not self.is_enabled or not self.config.cognome_auto_inject:
            return messages, None

        engram = self.compile(query, budget_tokens=budget_tokens, branch=branch)
        if not engram.preamble:
            return messages, None

        # Insert the Engram as the first system message (position 0 or
        # after an existing system message).
        engram_msg: dict[str, Any] = {
            "role": "system",
            "content": engram.preamble,
        }

        # Find where to insert: after the last system message, or at index 0.
        insert_at = 0
        for i, m in enumerate(messages):
            if m.get("role") == "system":
                insert_at = i + 1
            else:
                break

        updated = list(messages)
        updated.insert(insert_at, engram_msg)

        logger.info(
            "COGNOME injected: %d tokens (%.0f%% compression), hash=%s",
            engram.token_estimate,
            engram.compression_ratio * 100,
            engram.engram_hash[:12],
        )
        return updated, engram

    def derive_query_from_messages(self, messages: list[dict[str, Any]]) -> str:
        """
        Extract a compilation query from the most recent user message(s).

        This heuristic takes the last user message (or last two if the
        latest is very short) and uses it as the COGNOME query.
        Supports multimodal content (list of parts) in addition to plain text.
        """
        def _extract_text(content: Any) -> str:
            """Extract text from either a plain string or a multimodal list."""
            if isinstance(content, str):
                return content.strip()
            if isinstance(content, list):
                parts = []
                for item in content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        parts.append(item.get("text", "").strip())
                return " ".join(parts).strip()
            return ""

        user_msgs = [m for m in messages if m.get("role") == "user"]
        if not user_msgs:
            return ""
        last = _extract_text(user_msgs[-1].get("content") or "")
        if len(last) < 20 and len(user_msgs) >= 2:
            prev = _extract_text(user_msgs[-2].get("content") or "")
            return f"{prev} {last}".strip()
        return last[:500]

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    def _get_compiler(self) -> CognomeCompiler:
        if self._compiler is None:
            self._compiler = CognomeCompiler(
                self.db,
                default_budget_tokens=self.config.cognome_budget_tokens,
                enable_l2=getattr(self.config, "cognome_l2_enabled", True),
                enable_l3=getattr(self.config, "cognome_l3_enabled", True),
                l3_overflow_fraction=getattr(self.config, "cognome_l3_overflow_fraction", 0.15),
            )
        return self._compiler

    def _ensure_init(self) -> None:
        if not self.is_initialised:
            self.init()

    def _bump_stats(self, engram: CompiledEngram) -> None:
        idx = self.db.index
        now = str(time.time())
        idx.set_cognome_state(_K_LAST_COMPILE_AT, now)

        total = int(idx.get_cognome_state(_K_TOTAL_COMPILES) or "0")
        idx.set_cognome_state(_K_TOTAL_COMPILES, str(total + 1))

        saved = max(0, engram.baseline_token_estimate - engram.token_estimate)
        total_saved = int(idx.get_cognome_state(_K_TOTAL_TOKENS_SAVED) or "0")
        idx.set_cognome_state(_K_TOTAL_TOKENS_SAVED, str(total_saved + saved))

    @staticmethod
    def _cache_key(query: str, budget: int, branch: str | None, version: int = 0) -> str:
        """Deterministic hash for cache lookups.

        Includes a monotonic *version* so new commits in the workspace
        (which change what L1 would select) automatically invalidate
        every cached Engram without needing a table-wide DELETE.
        """
        payload = f"{query}|{budget}|{branch or ''}|v{version}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _float_or_none(val: str | None) -> float | None:
    if val is None:
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def _empty_engram(query: str, budget: int) -> CompiledEngram:
    return CompiledEngram(
        preamble="",
        query=query,
        source_commits=[],
        noeme_count=0,
        token_estimate=0,
        baseline_token_estimate=0,
        compression_ratio=0.0,
        budget_tokens=max(0, budget),
        engram_hash=hashlib.sha256(b"").hexdigest(),
    )
