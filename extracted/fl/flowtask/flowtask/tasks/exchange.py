"""FEAT-555 — Redis transport for NextTask payloads crossing a process boundary.

NOTE: this module talks to redis-py (``redis.asyncio``) directly and NOT through
asyncdb. The asyncdb Redis driver is constructed with ``decode_responses=True``,
which corrupts the binary Parquet/cloudpickle blob.
"""
from __future__ import annotations

import hashlib
import io
import logging
from typing import Any

import cloudpickle
import orjson
import redis.asyncio as aioredis

from ..conf import (
    NEXTTASK_EXCHANGE_PREFIX,
    NEXTTASK_EXCHANGE_TTL,
    REDIS_URL,
)
from .chain import ChainEncodingError, ChainError, ChainMetadata, ChainPayload

logger = logging.getLogger(__name__)

KIND_NONE = "none"
KIND_PARQUET = "parquet"
KIND_CLOUDPICKLE = "cloudpickle"


def encode_result(obj: Any) -> tuple[bytes, str]:
    """Encode a task result for transport.

    Args:
        obj: The origin task's result: None, a pandas DataFrame, or any object.

    Returns:
        ``(blob, kind)`` where kind is "none", "parquet" or "cloudpickle".

    Raises:
        ChainEncodingError: When every applicable encoder failed.
    """
    # (1) obj is None -> (b"", KIND_NONE)
    if obj is None:
        return b"", KIND_NONE

    # (2) If it is a pandas.DataFrame, try obj.to_parquet(None, engine="pyarrow")
    # -> (blob, KIND_PARQUET); on failure log a warning and FALL THROUGH to
    # cloudpickle rather than raising, because a DataFrame with object columns
    # can be unparquetable yet perfectly picklable.
    try:
        import pandas as pd

        if isinstance(obj, pd.DataFrame):
            try:
                blob = obj.to_parquet(None, engine="pyarrow")
                return blob, KIND_PARQUET
            except Exception as e:  # noqa: BLE001
                logger.warning(
                    "DataFrame could not be encoded as Parquet, falling back "
                    "to cloudpickle: %s",
                    e,
                )
                # Fall through to cloudpickle
    except ImportError:
        # pandas not available, fall through to cloudpickle
        pass

    # (3) Otherwise cloudpickle.dumps(obj) -> (blob, KIND_CLOUDPICKLE)
    try:
        blob = cloudpickle.dumps(obj)
        return blob, KIND_CLOUDPICKLE
    except Exception as e:
        # (4) Wrap a final failure in ChainEncodingError, chaining the original
        raise ChainEncodingError(
            f"Failed to encode result: {e}"
        ) from e


def decode_result(blob: bytes, kind: str) -> Any:
    """Inverse of :func:`encode_result`.

    Args:
        blob: The stored bytes.
        kind: One of "none", "parquet", "cloudpickle".

    Returns:
        The decoded object (None for kind "none").

    Raises:
        ChainEncodingError: Unknown kind, or the blob failed to decode.
    """
    if kind == KIND_NONE:
        return None

    if kind == KIND_PARQUET:
        import pandas as pd

        return pd.read_parquet(io.BytesIO(blob))

    if kind == KIND_CLOUDPICKLE:
        return cloudpickle.loads(blob)

    # Unknown kind
    raise ChainEncodingError(f"Unknown result kind: {kind}")


class ResultExchange:
    """One-shot Redis mailbox for a chain payload.

    Key shape: ``<prefix>:<origin_task_id>:<hop_index>``.
    """

    ENVELOPE_VERSION: int = 1

    def __init__(
        self,
        dsn: str = REDIS_URL,
        ttl: int = NEXTTASK_EXCHANGE_TTL,
        prefix: str = NEXTTASK_EXCHANGE_PREFIX,
    ) -> None:
        """Args:
            dsn: Redis DSN. Defaults to the cache DB (``REDIS_URL``).
            ttl: Seconds a staged payload survives.
            prefix: Key namespace.
        """
        self._dsn = dsn
        self._ttl = ttl
        self._prefix = prefix
        self._redis: aioredis.Redis | None = None
        self.logger = logger

    def _connection(self) -> aioredis.Redis:
        """Return the lazily-created binary-safe Redis client."""
        if self._redis is None:
            self._redis = aioredis.Redis.from_url(
                self._dsn, decode_responses=False
            )
        return self._redis

    def key_for(self, origin_task_id: str, hop_index: int) -> str:
        """Return the mailbox key for one hop of one origin run."""
        return f"{self._prefix}:{origin_task_id}:{hop_index}"

    async def put(
        self, payload: ChainPayload, origin_task_id: str, hop_index: int
    ) -> str:
        """Stage a payload for a remote hop.

        Args:
            payload: The payload to hand off.
            origin_task_id: The finished task's id.
            hop_index: Index of this hop among the origin's continuations.

        Returns:
            The Redis key the hop must be given as ``chain_key``.

        Raises:
            ChainEncodingError: The result could not be encoded (strict; the
                caller must NOT dispatch the hop).
            redis.RedisError: Redis was unreachable or refused the write.
        """
        # Encode the result
        blob, kind = encode_result(payload.result)

        # Compute sha256 of the blob
        digest = hashlib.sha256(blob).hexdigest()

        # Build the envelope mapping
        mapping = {
            "version": str(self.ENVELOPE_VERSION),
            "kind": kind,
            "sha256": digest,
            "origin_task_id": origin_task_id,
            "result": blob,
            "variables": orjson.dumps(payload.variables),
            "metadata": payload.metadata.model_dump_json(),
        }

        # Get the key
        key = self.key_for(origin_task_id, hop_index)

        # Write to Redis: hset then expire
        redis_client = self._connection()
        await redis_client.hset(key, mapping=mapping)
        await redis_client.expire(key, self._ttl)

        self.logger.info(
            "Staged chain payload: key=%s, kind=%s, ttl=%d",
            key,
            kind,
            self._ttl,
        )

        return key

    async def get(self, key: str, delete: bool = True) -> ChainPayload:
        """Read a staged payload back, once.

        Args:
            key: The key returned by :meth:`put`.
            delete: Delete the key after a successful read.

        Returns:
            The reconstructed ChainPayload.

        Raises:
            ChainError: Key missing or expired, unknown envelope version, or a
                checksum mismatch.
            ChainEncodingError: The blob failed to decode.
        """
        redis_client = self._connection()

        # Get all fields from the hash
        raw_data = await redis_client.hgetall(key)

        # Empty dict means key is missing or expired
        if not raw_data:
            raise ChainError(f"Chain payload missing or expired: {key}")

        # Decode bytes keys to strings, and handle bytes values too
        data = {}
        for k, v in raw_data.items():
            field_name = k.decode("utf-8") if isinstance(k, bytes) else k
            # Values can be bytes (result, variables, metadata) or strings (version, kind, sha256)
            if isinstance(v, bytes):
                # For string fields, decode; for binary fields (result), keep as bytes
                if field_name in ("version", "kind", "sha256", "origin_task_id"):
                    value = v.decode("utf-8")
                else:
                    value = v
            else:
                value = v
            data[field_name] = value

        # Verify envelope version
        version = int(data.get("version", "0"))
        if version != self.ENVELOPE_VERSION:
            raise ChainError(
                f"Unknown envelope version: {version} (expected "
                f"{self.ENVELOPE_VERSION})"
            )

        # Verify checksum before decoding
        stored_sha256 = data.get("sha256", "")
        result_blob = data.get("result", b"")
        computed_sha256 = hashlib.sha256(result_blob).hexdigest()
        if computed_sha256 != stored_sha256:
            raise ChainError(
                f"Checksum mismatch for payload {key}: expected {stored_sha256}, "
                f"got {computed_sha256}"
            )

        # Decode the result
        kind = data.get("kind", "")
        try:
            result = decode_result(result_blob, kind)
        except ChainEncodingError as e:
            raise ChainEncodingError(
                f"Failed to decode result for {key}: {e}"
            ) from e

        # Decode variables
        variables = orjson.loads(data.get("variables", b"{}"))

        # Decode metadata
        metadata = ChainMetadata.model_validate_json(data.get("metadata", "{}"))

        # Delete on success if requested
        if delete:
            await redis_client.delete(key)
            self.logger.info("Retrieved and deleted chain payload: key=%s", key)
        else:
            self.logger.info("Retrieved chain payload (no delete): key=%s", key)

        return ChainPayload(
            result=result,
            variables=variables,
            metadata=metadata,
        )

    async def close(self) -> None:
        """Release the Redis connection if one was opened."""
        if self._redis is not None:
            try:
                await self._redis.aclose()
            except AttributeError:
                # Fall back to close() on older redis-py
                try:
                    await self._redis.close()
                except Exception:  # noqa: BLE001, S110
                    pass
            finally:
                self._redis = None