"""Background worker for generating message embeddings."""

from __future__ import annotations

import asyncio
import hashlib
import logging
from typing import TYPE_CHECKING, Any

from . import storage
from .embeddings import EmbeddingPermanentError, EmbeddingService, EmbeddingTransientError, LocalEmbeddingService

if TYPE_CHECKING:
    from ..db import ThreadSafeConnection

logger = logging.getLogger(__name__)

MIN_CONTENT_LENGTH = 10
DEFAULT_INTERVAL = 30.0
MAX_INTERVAL = 300.0
BACKOFF_MULTIPLIER = 2.0
MAX_CONSECUTIVE_FAILURES = 10
WARNING_THRESHOLD = 7  # Warn when approaching disable threshold
MAX_STORE_RETRIES = 3
RECOVERY_PROBE_INTERVAL = 600.0  # 10 minutes between recovery probes


class EmbeddingWorker:
    def __init__(
        self,
        db: ThreadSafeConnection,
        embedding_service: EmbeddingService | LocalEmbeddingService,
        batch_size: int = 50,
        vec_manager: Any | None = None,
    ) -> None:
        self._db = db
        self._service = embedding_service
        self._batch_size = batch_size
        self._vec_manager = vec_manager
        self._running = False
        self._disabled = False
        self._permanently_disabled = False
        self._disabled_reason: str | None = None
        self._consecutive_failures = 0
        self._current_interval = DEFAULT_INTERVAL
        self._base_interval = DEFAULT_INTERVAL
        self._task: asyncio.Task[None] | None = None
        self._store_failures: dict[str, int] = {}
        self._cycle_count = 0
        self._repair_offset = 0

    @property
    def disabled(self) -> bool:
        return self._disabled

    @property
    def disabled_reason(self) -> str | None:
        return self._disabled_reason

    @property
    def consecutive_failures(self) -> int:
        return self._consecutive_failures

    @property
    def current_interval(self) -> float:
        return self._current_interval

    def _reset_backoff(self) -> None:
        self._consecutive_failures = 0
        self._current_interval = self._base_interval

    def _apply_backoff(self) -> None:
        self._consecutive_failures += 1
        self._current_interval = min(
            self._base_interval * (BACKOFF_MULTIPLIER**self._consecutive_failures),
            MAX_INTERVAL,
        )
        logger.warning(
            "Embedding worker: %d consecutive failures, next interval %.0fs",
            self._consecutive_failures,
            self._current_interval,
        )
        if self._consecutive_failures >= MAX_CONSECUTIVE_FAILURES:
            self._disabled = True
            self._disabled_reason = f"Auto-disabled after {self._consecutive_failures} consecutive failures"
            logger.error("Embedding worker auto-disabled: %s", self._disabled_reason)
        elif self._consecutive_failures >= WARNING_THRESHOLD:
            logger.warning(
                "Embedding worker approaching disable threshold: %d/%d failures",
                self._consecutive_failures,
                MAX_CONSECUTIVE_FAILURES,
            )

    def _disable_permanent(self, reason: str) -> None:
        self._disabled = True
        self._permanently_disabled = True
        self._disabled_reason = reason
        logger.error("Embedding worker permanently disabled: %s", reason)

    def re_enable(self) -> None:
        """Manually re-enable a disabled worker (e.g. after fixing the root cause)."""
        self._disabled = False
        self._permanently_disabled = False
        self._disabled_reason = None
        self._reset_backoff()
        logger.info("Embedding worker re-enabled")

    async def _probe_recovery(self) -> bool:
        """Attempt a single embed call to check if the service has recovered.

        Returns True if the probe succeeded and the worker was re-enabled.
        """
        try:
            result = await self._service.embed("recovery probe")
            if result is not None:
                logger.info("Embedding worker recovery probe succeeded, re-enabling")
                self.re_enable()
                return True
        except EmbeddingPermanentError:
            pass
        except Exception:
            pass
        return False

    async def process_pending(self) -> int:
        """Process unembedded messages, source chunks, and memory artifacts. Returns total count embedded."""
        count = await self._process_pending_messages()
        count += await self._process_pending_source_chunks()
        count += await self._process_pending_memory_artifacts()
        self._cycle_count += 1
        if self._cycle_count % 10 == 0:
            self._repair_stale_embeddings()
        return count

    def _repair_stale_embeddings(self, limit: int = 100) -> None:
        """Detect rows marked 'embedded' but missing from the vector index.

        Sweeps source_chunk_embeddings and memory_artifact_embeddings in each
        pass. Resets missing rows to 'pending' so the normal worker flow
        re-embeds them. Uses an advancing OFFSET cursor so that every embedded
        row is eventually checked, even when the total exceeds ``limit``.
        """
        self._repair_table(
            table="source_chunk_embeddings",
            id_col="chunk_id",
            vec_attr="source_chunks",
            limit=limit,
        )
        self._repair_table(
            table="memory_artifact_embeddings",
            id_col="artifact_id",
            vec_attr="memories",
            limit=limit,
        )

    def _repair_table(self, *, table: str, id_col: str, vec_attr: str, limit: int) -> None:
        """Repair stale rows for one embedding table.

        ``table`` and ``id_col`` are interpolated into DDL/DML but are
        constrained to a hardcoded allowlist below — no user input reaches
        these identifiers.
        """
        # Identifier allowlist — values below are the only permitted combinations.
        # Use a hard guard (not ``assert``) so ``python -O`` cannot suppress it.
        # ASVS V5.2: security controls must not rely on assertions.
        _allowed: dict[str, str] = {
            "source_chunk_embeddings": "chunk_id",
            "memory_artifact_embeddings": "artifact_id",
        }
        if _allowed.get(table) != id_col:
            raise ValueError(f"Disallowed repair table/column pair: {table!r}/{id_col!r}")

        if not self._vec_manager:
            return
        vec_index = getattr(self._vec_manager, vec_attr, None)
        if not vec_index:
            return
        try:
            rows = self._db.execute_fetchall(
                f"SELECT {id_col} FROM {table} WHERE status = 'embedded' ORDER BY {id_col} LIMIT ? OFFSET ?",
                (limit, self._repair_offset),
            )
            if not rows:
                # Wrapped around — reset cursor for next sweep
                self._repair_offset = 0
                return
            missing_ids = [r[id_col] for r in rows if not vec_index.contains(r[id_col])]
            if missing_ids:
                placeholders = ",".join("?" * len(missing_ids))
                self._db.execute(
                    f"UPDATE {table} SET status = 'pending' WHERE {id_col} IN ({placeholders})",
                    tuple(missing_ids),
                )
                self._db.commit()
                logger.warning(
                    "Mid-session repair: reset %d of %d %s to 'pending'",
                    len(missing_ids),
                    len(rows),
                    table,
                )
            # Advance cursor; if we got a full page, there may be more
            if len(rows) < limit:
                self._repair_offset = 0
            else:
                self._repair_offset += limit
        except Exception:
            logger.warning("Failed to repair stale %s", table, exc_info=True)

    async def _process_pending_messages(self) -> int:
        """Process unembedded messages. Returns count of messages embedded."""
        messages = storage.get_unembedded_messages(self._db, limit=self._batch_size)
        if not messages:
            return 0

        # Mark short messages as skipped so they are never re-queried
        eligible = []
        for m in messages:
            if len(m.get("content", "")) < MIN_CONTENT_LENGTH:
                content_hash = hashlib.sha256(m.get("content", "").encode()).hexdigest()
                try:
                    storage.mark_embedding_skipped(
                        self._db, m["id"], m["conversation_id"], content_hash, status="skipped"
                    )
                except Exception:
                    logger.debug("Failed to mark short message %s as skipped", m["id"], exc_info=True)
            else:
                eligible.append(m)

        if not eligible:
            return 0

        texts = [m["content"] for m in eligible]
        embeddings = await self._service.embed_batch(texts, batch_size=self._batch_size)

        count = 0
        for msg, embedding in zip(eligible, embeddings):
            content_hash = hashlib.sha256(msg["content"].encode()).hexdigest()
            if embedding is None:
                logger.warning("Embedding returned None for message %s, marking as skipped", msg["id"])
                try:
                    storage.mark_embedding_skipped(
                        self._db, msg["id"], msg["conversation_id"], content_hash, status="failed"
                    )
                except Exception:
                    logger.debug("Failed to mark message %s as skipped", msg["id"], exc_info=True)
                continue
            try:
                storage.store_embedding(
                    self._db,
                    msg["id"],
                    msg["conversation_id"],
                    embedding,
                    content_hash,
                    vec_index=self._vec_manager.messages if self._vec_manager else None,
                )
                count += 1
                self._store_failures.pop(msg["id"], None)
            except Exception as e:
                fails = self._store_failures.get(msg["id"], 0) + 1
                self._store_failures[msg["id"]] = fails
                if fails >= MAX_STORE_RETRIES:
                    logger.error(
                        "Failed to store embedding for message %s %d times, marking as failed: %s",
                        msg["id"],
                        fails,
                        type(e).__name__,
                    )
                    try:
                        storage.mark_embedding_skipped(
                            self._db, msg["id"], msg["conversation_id"], content_hash, status="failed"
                        )
                    except Exception:
                        logger.debug("Failed to mark message %s as failed", msg["id"], exc_info=True)
                    self._store_failures.pop(msg["id"], None)
                else:
                    logger.error(
                        "Failed to store embedding for message %s (%d/%d): %s",
                        msg["id"],
                        fails,
                        MAX_STORE_RETRIES,
                        type(e).__name__,
                    )

        if count:
            logger.info("Embedded %d messages", count)
        return count

    async def _process_pending_source_chunks(self) -> int:
        """Process unembedded source chunks. Returns count of chunks embedded."""
        chunks = storage.get_unembedded_source_chunks(self._db, limit=self._batch_size)
        if not chunks:
            return 0

        eligible = []
        for c in chunks:
            if len(c.get("content", "")) < MIN_CONTENT_LENGTH:
                try:
                    storage.mark_source_chunk_embedding_skipped(
                        self._db, c["id"], c["source_id"], c["content_hash"], status="skipped"
                    )
                except Exception:
                    logger.debug("Failed to mark short chunk %s as skipped", c["id"], exc_info=True)
            else:
                eligible.append(c)

        if not eligible:
            return 0

        texts = [c["content"] for c in eligible]
        embeddings = await self._service.embed_batch(texts, batch_size=self._batch_size)

        count = 0
        for chunk, embedding in zip(eligible, embeddings):
            if embedding is None:
                logger.warning("Embedding returned None for source chunk %s, marking as skipped", chunk["id"])
                try:
                    storage.mark_source_chunk_embedding_skipped(
                        self._db, chunk["id"], chunk["source_id"], chunk["content_hash"], status="failed"
                    )
                except Exception:
                    logger.debug("Failed to mark chunk %s as skipped", chunk["id"], exc_info=True)
                continue
            try:
                storage.store_source_chunk_embedding(
                    self._db,
                    chunk["id"],
                    chunk["source_id"],
                    embedding,
                    chunk["content_hash"],
                    vec_index=self._vec_manager.source_chunks if self._vec_manager else None,
                )
                count += 1
                self._store_failures.pop(chunk["id"], None)
            except Exception as e:
                fails = self._store_failures.get(chunk["id"], 0) + 1
                self._store_failures[chunk["id"]] = fails
                if fails >= MAX_STORE_RETRIES:
                    logger.error(
                        "Failed to store embedding for chunk %s %d times, marking as failed: %s",
                        chunk["id"],
                        fails,
                        type(e).__name__,
                    )
                    try:
                        storage.mark_source_chunk_embedding_skipped(
                            self._db, chunk["id"], chunk["source_id"], chunk["content_hash"], status="failed"
                        )
                    except Exception:
                        logger.debug("Failed to mark chunk %s as failed", chunk["id"], exc_info=True)
                    self._store_failures.pop(chunk["id"], None)
                else:
                    logger.error(
                        "Failed to store embedding for chunk %s (%d/%d): %s",
                        chunk["id"],
                        fails,
                        MAX_STORE_RETRIES,
                        type(e).__name__,
                    )

        if count:
            logger.info("Embedded %d source chunks", count)
        return count

    async def _process_pending_memory_artifacts(self) -> int:
        """Process unembedded memory artifacts. Returns count embedded.

        Only memory-type artifacts (filtered in storage query) are considered.
        Scope/status filtering is applied at recall time, not at embed time —
        archived/rejected memories remain embedded but are excluded from recall.
        """
        artifacts = storage.get_unembedded_memory_artifacts(self._db, limit=self._batch_size)
        if not artifacts:
            return 0

        eligible = []
        for a in artifacts:
            if len(a.get("content", "")) < MIN_CONTENT_LENGTH:
                try:
                    storage.mark_memory_artifact_embedding_skipped(
                        self._db, a["id"], a["content_hash"], status="skipped"
                    )
                except Exception:
                    logger.debug("Failed to mark short memory %s as skipped", a["id"], exc_info=True)
            else:
                eligible.append(a)

        if not eligible:
            return 0

        texts = [a["content"] for a in eligible]
        embeddings = await self._service.embed_batch(texts, batch_size=self._batch_size)

        count = 0
        for art, embedding in zip(eligible, embeddings):
            if embedding is None:
                logger.warning("Embedding returned None for memory %s, marking as failed", art["id"])
                try:
                    storage.mark_memory_artifact_embedding_skipped(
                        self._db, art["id"], art["content_hash"], status="failed"
                    )
                except Exception:
                    logger.debug("Failed to mark memory %s as failed", art["id"], exc_info=True)
                continue
            try:
                storage.store_memory_artifact_embedding(
                    self._db,
                    art["id"],
                    embedding,
                    art["content_hash"],
                    vec_index=self._vec_manager.memories if self._vec_manager else None,
                )
                count += 1
                self._store_failures.pop(art["id"], None)
            except Exception as e:
                fails = self._store_failures.get(art["id"], 0) + 1
                self._store_failures[art["id"]] = fails
                if fails >= MAX_STORE_RETRIES:
                    logger.error(
                        "Failed to store embedding for memory %s %d times, marking as failed: %s",
                        art["id"],
                        fails,
                        type(e).__name__,
                    )
                    try:
                        storage.mark_memory_artifact_embedding_skipped(
                            self._db, art["id"], art["content_hash"], status="failed"
                        )
                    except Exception:
                        logger.debug("Failed to mark memory %s as failed", art["id"], exc_info=True)
                    self._store_failures.pop(art["id"], None)
                else:
                    logger.error(
                        "Failed to store embedding for memory %s (%d/%d): %s",
                        art["id"],
                        fails,
                        MAX_STORE_RETRIES,
                        type(e).__name__,
                    )

        if count:
            logger.info("Embedded %d memory artifacts", count)
        return count

    async def embed_source(self, source_id: str) -> int:
        """Embed all chunks of a source inline. Returns count of chunks embedded."""
        chunks = storage.list_source_chunks(self._db, source_id)
        if not chunks:
            return 0

        eligible = [c for c in chunks if len(c.get("content", "")) >= MIN_CONTENT_LENGTH]
        if not eligible:
            return 0

        texts = [c["content"] for c in eligible]
        try:
            embeddings = await self._service.embed_batch(texts, batch_size=self._batch_size)
        except (EmbeddingPermanentError, EmbeddingTransientError):
            logger.warning("Embedding failed for source %s, will be retried by worker", source_id)
            return 0

        count = 0
        for chunk, embedding in zip(eligible, embeddings):
            if embedding is None:
                continue
            try:
                storage.store_source_chunk_embedding(
                    self._db,
                    chunk["id"],
                    source_id,
                    embedding,
                    chunk["content_hash"],
                    vec_index=self._vec_manager.source_chunks if self._vec_manager else None,
                )
                count += 1
            except Exception as e:
                logger.error("Failed to store embedding for source chunk %s: %s", chunk["id"], type(e).__name__)

        if count > 0 and self._vec_manager:
            try:
                self._vec_manager.save_all()
            except Exception:
                logger.warning("Failed to flush vector index after inline embed", exc_info=True)

        return count

    async def embed_message(self, message_id: str, content: str, conversation_id: str) -> None:
        """Embed a single message (called inline after message creation).

        Unlike ``embed_source()``, this does NOT call ``save_all()`` because it
        is only invoked from within the background worker cycle where
        ``run_forever()`` handles flushing after ``process_pending()``.
        """
        if len(content) < MIN_CONTENT_LENGTH:
            return

        content_hash = hashlib.sha256(content.encode()).hexdigest()
        try:
            embedding = await self._service.embed(content)
        except (EmbeddingPermanentError, EmbeddingTransientError):
            logger.warning("Embedding failed for message %s, will be retried by worker", message_id)
            return
        if embedding is None:
            return

        try:
            storage.store_embedding(
                self._db,
                message_id,
                conversation_id,
                embedding,
                content_hash,
                vec_index=self._vec_manager.messages if self._vec_manager else None,
            )
        except Exception as e:
            logger.error("Failed to store embedding for message %s: %s", message_id, type(e).__name__)

    async def run_forever(self, interval: float = 30.0) -> None:
        """Poll for unembedded messages at a regular interval with exponential backoff."""
        self._running = True
        self._base_interval = interval
        self._current_interval = interval
        logger.info("Embedding worker started (interval=%.0fs)", interval)
        while self._running:
            if self._disabled:
                logger.debug("Embedding worker is disabled: %s", self._disabled_reason)
                if self._permanently_disabled:
                    # Permanent errors (e.g. invalid API key, model not found)
                    # should not be auto-probed -- use re_enable() explicitly.
                    await asyncio.sleep(RECOVERY_PROBE_INTERVAL)
                    continue
                await asyncio.sleep(RECOVERY_PROBE_INTERVAL)
                await self._probe_recovery()
                continue
            try:
                await self.process_pending()
                if self._vec_manager:
                    self._vec_manager.save_all()
                if self._consecutive_failures > 0:
                    self._reset_backoff()
            except EmbeddingPermanentError as e:
                self._disable_permanent(f"Permanent API error: {e} (status={e.status_code})")
            except EmbeddingTransientError:
                self._apply_backoff()
            except Exception as e:
                logger.error("Embedding worker unexpected error: %s", type(e).__name__)
                self._apply_backoff()
            await asyncio.sleep(self._current_interval)

    def start(self, interval: float = 30.0) -> None:
        """Start the background polling loop."""
        self._task = asyncio.ensure_future(self.run_forever(interval))

    def stop(self) -> None:
        """Stop the background polling loop."""
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()
