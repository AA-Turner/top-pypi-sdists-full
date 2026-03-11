"""
Face Recognition with Local Embedding Search Optimization

This module uses local similarity search for face recognition to achieve high performance:

Performance Optimization Strategy:
1. EmbeddingManager loads all staff embeddings from API at startup (~1 API call)
2. Embeddings are cached in memory as a normalized numpy matrix
3. Face recognition uses fast local cosine similarity search (~1-5ms per face)
4. API calls are avoided during normal operation (2000x speedup vs API calls)
5. Background refresh updates embeddings periodically (configurable TTL)

Processing Flow:
1. TemporalIdentityManager receives face embedding from detection
2. Uses EmbeddingManager._find_best_local_match() for fast local similarity search
3. Returns best match if similarity >= threshold, otherwise returns "Unknown"
4. Only falls back to API if EmbeddingManager unavailable (rare)

Configuration options:
- enable_track_id_cache: Enable/disable track-level caching
- cache_max_size: Maximum number of cached track IDs (default: 3000)
- cache_ttl: Cache time-to-live in seconds (default: 3600)
 - background_refresh_interval: Embedding refresh interval (default: 43200s = 12h)
- similarity_threshold: Minimum similarity for recognition (default: 0.45)
"""
import subprocess
import logging
import asyncio
import json
import os
import re
from pathlib import Path
log_file = open("pip_jetson_btii.log", "w")
cmd = ["pip", "install", "httpx"]
subprocess.run(
        cmd,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        #preexec_fn=os.setpgrp   
    )
log_file.close()

from typing import Any, Dict, List, Optional, Tuple, NamedTuple
import time
import base64
import cv2
import numpy as np
import threading
from datetime import datetime, timezone
from collections import deque

try:
    from matrice_common.session import Session
    HAS_MATRICE_SESSION = True
except ImportError:
    Session = None
    HAS_MATRICE_SESSION = False

try:
    import redis.asyncio as aioredis
    HAS_AIREDIS = True
except ImportError:
    aioredis = None
    HAS_AIREDIS = False

try:
    import redis as redis_sync
    HAS_REDIS_SYNC = True
except ImportError:
    redis_sync = None  # type: ignore[assignment]
    HAS_REDIS_SYNC = False

from ..core.base import (
    BaseProcessor,
    ProcessingContext,
    ProcessingResult,
    ConfigProtocol,
)
from ..utils import (
    filter_by_confidence,
    filter_by_categories,
    apply_category_mapping,
    calculate_counting_summary,
    match_results_structure,
)
from dataclasses import dataclass, field
from ..core.config import BaseConfig, AlertConfig
from .face_recognition_client import FacialRecognitionClient
from .people_activity_logging import PeopleActivityLogging
from .embedding_manager import EmbeddingManager, EmbeddingConfig

# Cache for location names to avoid repeated API calls
_location_name_cache: Dict[str, str] = {}


# ---- Lightweight identity tracking and temporal smoothing (adapted from compare_similarity.py) ---- #
from collections import deque, defaultdict
from matrice_common.session import Session




def _normalize_embedding(vec: List[float]) -> List[float]:
    """Normalize an embedding vector to unit length (L2). Returns float32 list."""
    arr = np.asarray(vec, dtype=np.float32)
    if arr.size == 0:
        return []
    n = np.linalg.norm(arr)
    if n > 0:
        arr = arr / n
    return arr.tolist()


class RedisFaceMatchResult(NamedTuple):
    staff_id: Optional[str]
    person_name: str
    confidence: float
    employee_id: Optional[str]
    raw: Dict[str, Any]


class RedisFaceMatcher:
    """Handles Redis-based face similarity search."""

    ACTION_ID_PATTERN = re.compile(r"^[0-9a-f]{8,}$", re.IGNORECASE)
    # Shared sync Redis client per-process (avoids asyncio loop binding issues when caller uses asyncio.run per frame)
    _shared_sync_client = None
    _shared_sync_client_sig: Optional[Tuple[Any, ...]] = None
    _shared_sync_client_lock = threading.Lock()
    # Shared app_deployment_id cache per-process (once resolved, reused across all instances/frames)
    _shared_app_dep_id: Optional[str] = None
    _shared_app_dep_id_lock = threading.Lock()

    def __init__(
        self,
        session=None,
        logger: Optional[logging.Logger] = None,
        redis_url: Optional[str] = None,
        face_client=None,
    ) -> None:
        self.logger = logger or logging.getLogger(__name__)
        self._session = session
        self.face_client = face_client
        self.redis_url = (
            redis_url
            or os.getenv("FACE_RECOG_REDIS_URL")
            or os.getenv("REDIS_URL")
        )
        self.stream_name = os.getenv(
            "FACE_RECOG_REDIS_STREAM", "facial_detection_stream"
        )
        self.default_min_confidence = float(
            os.getenv("FACE_RECOG_REDIS_MIN_CONFIDENCE", "0.01")
        )
        self.response_timeout = (
            float(os.getenv("FACE_RECOG_REDIS_RESPONSE_TIMEOUT_MS", "200")) / 1000.0  # Reduced from 600ms to 200ms for faster failure
        )
        self.poll_interval = (
            float(os.getenv("FACE_RECOG_REDIS_POLL_INTERVAL_MS", "5")) / 1000.0  # Reduced from 20ms to 5ms for faster polling
        )
        self.stream_maxlen = int(
            os.getenv("FACE_RECOG_REDIS_STREAM_MAXLEN", "5000")
        )
        self._redis_client = None  # type: ignore[assignment]
        self._redis_client_loop_id: Optional[int] = None  # Track which event loop owns the client
        self._redis_sync_client = None  # sync redis client (loop-agnostic)
        self._redis_connection_params: Optional[Dict[str, Any]] = None
        self._app_deployment_id = os.getenv("APP_DEPLOYMENT_ID")
        self._action_id = (
            os.getenv("ACTION_ID")
            or os.getenv("MATRISE_ACTION_ID")
            or self._discover_action_id()
        )
        self._redis_server_id = os.getenv("REDIS_SERVER_ID")
        # Locks will be created per-loop to avoid cross-loop issues
        self._app_dep_lock: Optional[asyncio.Lock] = None
        self._session_lock: Optional[asyncio.Lock] = None
        self._redis_lock: Optional[asyncio.Lock] = None
        self._locks_loop_id: Optional[int] = None
        self._redis_warning_logged = False

    def _get_current_loop_id(self) -> int:
        """Get a unique identifier for the current running event loop."""
        try:
            loop = asyncio.get_running_loop()
            return id(loop)
        except RuntimeError:
            return 0

    def _ensure_locks_for_current_loop(self) -> None:
        """Ensure locks are created for the current event loop."""
        current_loop_id = self._get_current_loop_id()
        if self._locks_loop_id != current_loop_id:
            # Create new locks for this event loop
            self._app_dep_lock = asyncio.Lock()
            self._session_lock = asyncio.Lock()
            self._redis_lock = asyncio.Lock()
            self._locks_loop_id = current_loop_id

    def is_available(self) -> bool:
        return HAS_REDIS_SYNC or HAS_AIREDIS

    def _get_app_dep_id_sync(self) -> Optional[str]:
        """
        Get app_deployment_id from env vars or class-level cache (SYNC - no async calls).
        
        This avoids async operations that would fail when asyncio.run() creates a new loop per frame.
        """
        # Check instance cache first
        if self._app_deployment_id:
            return self._app_deployment_id
        
        # Check class-level cache (shared across instances in this process)
        with self.__class__._shared_app_dep_id_lock:
            if self.__class__._shared_app_dep_id:
                self._app_deployment_id = self.__class__._shared_app_dep_id
                return self._app_deployment_id
        
        # Try env var
        env_app_dep_id = os.getenv("APP_DEPLOYMENT_ID")
        if env_app_dep_id:
            self._app_deployment_id = env_app_dep_id
            with self.__class__._shared_app_dep_id_lock:
                self.__class__._shared_app_dep_id = env_app_dep_id
            return self._app_deployment_id
        
        return None

    def _get_redis_sync_client(self) -> Optional[Any]:
        """
        Get a **synchronous** redis client (SYNC method - no async at all).

        Why sync and why no async calls?
        - The py_inference worker calls `asyncio.run()` per frame, creating/closing a new event loop each call.
        - `redis.asyncio` clients (and asyncio locks) are bound to the loop they were created on.
        - Any cached async objects become invalid when the loop changes, causing:
          - "Future attached to a different loop"
          - "Event loop is closed"

        This method is COMPLETELY SYNC:
        - Uses only env vars for Redis connection (no async RPC to fetch params)
        - Uses threading.Lock (not asyncio.Lock) for thread-safety
        - Creates a sync redis client that is loop-agnostic and safe across frames
        
        Required env vars (set at least one):
        - FACE_RECOG_REDIS_URL or REDIS_URL: Full Redis URL
        - OR: FACE_RECOG_REDIS_HOST + FACE_RECOG_REDIS_PORT
        """
        if not HAS_REDIS_SYNC or redis_sync is None:
            return None

        # Fast path: already have a cached client for this instance
        if self._redis_sync_client is not None:
            return self._redis_sync_client

        # Resolve URL from env vars (NO async calls)
        redis_url = self.redis_url
        if not redis_url:
            redis_url = os.getenv("FACE_RECOG_REDIS_URL") or os.getenv("REDIS_URL")
        if not redis_url:
            host = os.getenv("FACE_RECOG_REDIS_HOST")
            port = os.getenv("FACE_RECOG_REDIS_PORT")
            if host and port:
                redis_url = f"redis://{host}:{port}/0"

        if not redis_url:
            # Cannot create sync client without connection info from env
            # This will fall back to async path (which may fail, but that's expected)
            self.logger.debug(
                "No Redis URL/host available from env vars for sync client. "
                "Set FACE_RECOG_REDIS_URL or FACE_RECOG_REDIS_HOST+FACE_RECOG_REDIS_PORT."
            )
            return None

        # Cache the URL for future use
        self.redis_url = redis_url

        def _env_float(name: str, default: float) -> float:
            raw = os.getenv(name)
            if raw is None or raw == "":
                return float(default)
            try:
                return float(raw)
            except Exception:
                return float(default)

        # Socket timeouts: keep bounded so a bad redis doesn't stall the worker
        socket_connect_timeout = max(
            0.2, _env_float("FACE_RECOG_REDIS_CONNECT_TIMEOUT_S", 1.0)
        )
        socket_timeout = max(
            0.2,
            _env_float(
                "FACE_RECOG_REDIS_SOCKET_TIMEOUT_S", float(max(1.0, self.response_timeout))
            ),
        )

        sig = ("url", str(redis_url))

        # Use threading.Lock (NOT asyncio.Lock) for process-level sharing
        with self.__class__._shared_sync_client_lock:
            if (
                self.__class__._shared_sync_client is not None
                and self.__class__._shared_sync_client_sig == sig
            ):
                self._redis_sync_client = self.__class__._shared_sync_client
                return self._redis_sync_client

            # Create new shared client
            try:
                client = redis_sync.Redis.from_url(
                    str(redis_url),
                    decode_responses=True,
                    health_check_interval=30,
                    socket_connect_timeout=socket_connect_timeout,
                    socket_timeout=socket_timeout,
                    retry_on_timeout=True,
                )
                self.logger.info(
                    "[SYNC] Created sync Redis client for face matcher: %s",
                    redis_url,
                )
            except Exception as exc:
                self.logger.error(
                    "[SYNC] Failed to create sync Redis client for face matcher: %s",
                    exc,
                    exc_info=True,
                )
                return None

            self.__class__._shared_sync_client = client
            self.__class__._shared_sync_client_sig = sig
            self._redis_sync_client = client
            return self._redis_sync_client

    async def match_embedding(
        self,
        embedding: List[float],
        search_id: Optional[str],
        location: str = "",
        min_confidence: Optional[float] = None,
    ) -> Optional[RedisFaceMatchResult]:
        """Send embedding to Redis stream and wait for match result."""
        if not (HAS_REDIS_SYNC or HAS_AIREDIS):
            if not self._redis_warning_logged:
                self.logger.warning(
                    "redis client not available; skipping Redis face matcher flow"
                )
                self._redis_warning_logged = True
            return None

        embedding_list = self._prepare_embedding_list(embedding)
        if not embedding_list:
            self.logger.warning(f"Empty embedding list for search_id={search_id}, cannot send to Redis")
            print(f"WARNING: Empty embedding list for search_id={search_id}, cannot send to Redis")
            return None
        
        if len(embedding_list) == 0:
            self.logger.warning(f"Embedding list has zero length for search_id={search_id}")
            print(f"WARNING: Embedding list has zero length for search_id={search_id}")
            return None

        resolved_search_id = str(search_id or self._generate_search_id())

        # ============================================================
        # Preferred: SYNC redis client (loop-agnostic, safe when caller
        # uses asyncio.run() per frame and closes the loop each call).
        # This method is COMPLETELY SYNC - no async calls at all.
        # ============================================================
        redis_client_sync = None
        if HAS_REDIS_SYNC:
            try:
                redis_client_sync = self._get_redis_sync_client()
            except Exception:
                redis_client_sync = None

        # Get app_dep_id - for SYNC path, use only cached/env values (no async calls)
        app_dep_id: Optional[str] = None
        if redis_client_sync is not None:
            # SYNC path: get app_dep_id from cache or env only (no async)
            app_dep_id = self._get_app_dep_id_sync()
            if not app_dep_id:
                self.logger.warning(
                    "[SYNC] Cannot get app_deployment_id from env/cache. "
                    "Set APP_DEPLOYMENT_ID env var or ensure it was resolved previously."
                )
                # Fall back to async path below
                redis_client_sync = None

        # If we don't have sync client (or couldn't get app_dep_id sync), use async path
        if redis_client_sync is None:
            app_dep_id = await self._ensure_app_deployment_id()
            if not app_dep_id:
                return None
            # Cache for future sync calls
            with self.__class__._shared_app_dep_id_lock:
                if self.__class__._shared_app_dep_id is None:
                    self.__class__._shared_app_dep_id = app_dep_id

        payload = {
            "appDepId": app_dep_id,
            "searchId": resolved_search_id,
            "embedding": embedding_list,
            "location": location or "",
            "minConfidence": float(
                min_confidence if min_confidence is not None else self.default_min_confidence
            ),
        }

        if redis_client_sync is not None:
            try:
                self.logger.debug(
                    f"[SYNC] Sending embedding to Redis stream {self.stream_name} with search_id={resolved_search_id}, "
                    f"embedding_len={len(embedding_list)}, minConfidence={payload.get('minConfidence')}"
                )
                redis_client_sync.xadd(
                    self.stream_name,
                    {"data": json.dumps(payload, separators=(",", ":"))},
                    maxlen=self.stream_maxlen,
                    approximate=True,
                )
                self.logger.debug(
                    f"[SYNC] Successfully sent embedding to Redis stream for search_id={resolved_search_id}"
                )
            except Exception as exc:
                self.logger.error(
                    "[SYNC] Failed to enqueue face embedding to Redis stream %s: %s",
                    self.stream_name,
                    exc,
                    exc_info=True,
                )
                return None

            result_key = f"{resolved_search_id}_{app_dep_id}"
            deadline = time.monotonic() + self.response_timeout
            poll_count = 0
            start_poll_time = time.monotonic()

            self.logger.debug(
                f"[SYNC] Waiting for Redis response with key={result_key}, timeout={self.response_timeout:.3f}s"
            )

            while time.monotonic() < deadline:
                try:
                    raw_value = redis_client_sync.get(result_key)
                    poll_count += 1
                except Exception as exc:
                    self.logger.error(
                        "[SYNC] Failed to read Redis result for key %s: %s",
                        result_key,
                        exc,
                        exc_info=True,
                    )
                    return None

                if raw_value:
                    try:
                        redis_client_sync.delete(result_key)
                    except Exception:
                        pass

                    try:
                        parsed = json.loads(raw_value)
                    except Exception as exc:
                        self.logger.error(
                            "[SYNC] Unable to parse Redis face match response: %s",
                            exc,
                            exc_info=True,
                        )
                        return None

                    # Log and print the raw Redis response for debugging
                    self.logger.info(
                        f"[SYNC] Redis raw response for search_id={resolved_search_id}: {parsed}"
                    )

                    match_data = None
                    if isinstance(parsed, list) and parsed:
                        match_data = parsed[0]
                    elif isinstance(parsed, dict):
                        match_data = parsed
                    else:
                        self.logger.warning(
                            "[SYNC] Redis response is neither list nor dict: %s, value: %s",
                            type(parsed),
                            parsed,
                        )

                    if not isinstance(match_data, dict):
                        self.logger.warning(
                            "[SYNC] match_data is not a dict after extraction: %s, value: %s",
                            type(match_data),
                            match_data,
                        )
                        return None

                    staff_id = match_data.get("staffId") or match_data.get("staff_id")
                    if not staff_id:
                        self.logger.warning(
                            "[SYNC] No staffId found in match_data: %s", match_data
                        )
                        return None

                    person_name = str(match_data.get("name") or "Unknown")
                    confidence = float(
                        match_data.get("conf") or match_data.get("confidence") or 0.0
                    )
                    employee_id = match_data.get("employeeId") or match_data.get(
                        "embeddingId"
                    )

                    min_conf = float(
                        min_confidence
                        if min_confidence is not None
                        else self.default_min_confidence
                    )
                    if confidence < min_conf:
                        self.logger.debug(
                            "[SYNC] Redis match confidence %.3f below threshold %.3f, rejecting",
                            confidence,
                            min_conf,
                        )
                        return None

                    result = RedisFaceMatchResult(
                        staff_id=str(staff_id),
                        person_name=person_name,
                        confidence=round(confidence, 3),
                        employee_id=str(employee_id) if employee_id else None,
                        raw=match_data,
                    )

                    poll_time = (time.monotonic() - start_poll_time) * 1000.0
                    self.logger.info(
                        "[SYNC] Redis match result created (polls=%d, poll_time=%.2fms): staff_id=%s, name=%s, conf=%.3f",
                        poll_count,
                        poll_time,
                        result.staff_id,
                        result.person_name,
                        result.confidence,
                    )
                    return result

                time.sleep(self.poll_interval)

            poll_time = (time.monotonic() - start_poll_time) * 1000.0
            self.logger.warning(
                "[SYNC] Timed out waiting for Redis face match result for key %s (timeout=%.3fs, polls=%d, poll_time=%.2fms)",
                result_key,
                self.response_timeout,
                poll_count,
                poll_time,
            )
            return None

        # ============================================================
        # Fallback: ASYNC redis client (kept for environments where
        # sync redis is unavailable).
        # ============================================================
        if not HAS_AIREDIS:
            return None

        redis_client = await self._ensure_redis_client()
        if redis_client is None:
            return None

        try:
            self.logger.debug(
                f"Sending embedding to Redis stream {self.stream_name} with search_id={resolved_search_id}, "
                f"embedding_len={len(embedding_list)}, minConfidence={payload.get('minConfidence')}"
            )
            await redis_client.xadd(
                self.stream_name,
                {"data": json.dumps(payload, separators=(",", ":"))},
                maxlen=self.stream_maxlen,
                approximate=True,
            )
            self.logger.debug(f"Successfully sent embedding to Redis stream for search_id={resolved_search_id}")
        except RuntimeError as exc:
            # Handle event loop closed/mismatch errors - invalidate client and retry once
            exc_str = str(exc).lower()
            if "event loop" in exc_str or "different loop" in exc_str or "closed" in exc_str:
                self.logger.warning(
                    "Redis client event loop error detected, invalidating client and retrying: %s", exc
                )
                # Invalidate the client so next call recreates it
                self._redis_client = None
                self._redis_client_loop_id = None
                # Retry once with fresh client
                try:
                    redis_client = await self._ensure_redis_client()
                    if redis_client:
                        await redis_client.xadd(
                            self.stream_name,
                            {"data": json.dumps(payload, separators=(",", ":"))},
                            maxlen=self.stream_maxlen,
                            approximate=True,
                        )
                        self.logger.info(f"Successfully sent embedding after client refresh for search_id={resolved_search_id}")
                    else:
                        self.logger.error("Failed to recreate Redis client after event loop error")
                        return None
                except Exception as retry_exc:
                    self.logger.error(
                        "Retry also failed after Redis client refresh: %s", retry_exc, exc_info=True
                    )
                    return None
            else:
                self.logger.error(
                    "Failed to enqueue face embedding to Redis stream %s: %s",
                    self.stream_name,
                    exc,
                    exc_info=True,
                )
                print(f"ERROR: Failed to send to Redis stream {self.stream_name}: {exc}")
                return None
        except Exception as exc:
            self.logger.error(
                "Failed to enqueue face embedding to Redis stream %s: %s",
                self.stream_name,
                exc,
                exc_info=True,
            )
            print(f"ERROR: Failed to send to Redis stream {self.stream_name}: {exc}")
            return None

        result_key = f"{resolved_search_id}_{app_dep_id}"
        deadline = time.monotonic() + self.response_timeout
        poll_count = 0
        start_poll_time = time.monotonic()
        
        self.logger.debug(f"Waiting for Redis response with key={result_key}, timeout={self.response_timeout:.3f}s")

        # Poll loop - check immediately first, then with intervals
        while time.monotonic() < deadline:
            try:
                raw_value = await redis_client.get(result_key)
                poll_count += 1
            except RuntimeError as exc:
                # Handle event loop errors - invalidate client and return
                exc_str = str(exc).lower()
                if "event loop" in exc_str or "different loop" in exc_str or "closed" in exc_str:
                    self.logger.warning(
                        "Redis client event loop error in poll loop, invalidating client: %s", exc
                    )
                    self._redis_client = None
                    self._redis_client_loop_id = None
                    return None
                self.logger.error(
                    "Failed to read Redis result for key %s: %s",
                    result_key,
                    exc,
                    exc_info=True,
                )
                print(f"ERROR: Failed to read Redis result for key {result_key}: {exc}")
                return None
            except Exception as exc:
                self.logger.error(
                    "Failed to read Redis result for key %s: %s",
                    result_key,
                    exc,
                    exc_info=True,
                )
                print(f"ERROR: Failed to read Redis result for key {result_key}: {exc}")
                return None

            if raw_value:
                await redis_client.delete(result_key)
                try:
                    parsed = json.loads(raw_value)
                except Exception as exc:
                    parsed = json.loads(raw_value)
                    self.logger.error(
                        "Unable to parse Redis face match response: %s",
                        exc,
                        exc_info=True,
                    )
                    print(f"ERROR: Unable to parse Redis face match response: {exc}")
                    #return None

                # Log and print the raw Redis response for debugging
                self.logger.info(f"Redis raw response for search_id={resolved_search_id}: {parsed}")
                print(f"Redis raw response for search_id={resolved_search_id}: {parsed}")

                match_data = None
                if isinstance(parsed, list) and parsed:
                    match_data = parsed[0]
                    self.logger.info(f"Redis response is array, extracted first element: {match_data}")
                    print(f"Redis response is array, extracted first element: {match_data}")
                elif isinstance(parsed, dict):
                    match_data = parsed
                    self.logger.info(f"Redis response is dict: {match_data}")
                    print(f"Redis response is dict: {match_data}")
                else:
                    self.logger.warning(f"Redis response is neither list nor dict: {type(parsed)}, value: {parsed}")
                    print(f"WARNING: Redis response is neither list nor dict: {type(parsed)}, value: {parsed}")

                if not isinstance(match_data, dict):
                    self.logger.warning(f"match_data is not a dict after extraction: {type(match_data)}, value: {match_data}")
                    print(f"WARNING: match_data is not a dict after extraction: {type(match_data)}, value: {match_data}")
                    return None

                staff_id = match_data.get("staffId") or match_data.get("staff_id")
                if not staff_id:
                    self.logger.warning(f"No staffId found in match_data: {match_data}")
                    print(f"WARNING: No staffId found in match_data: {match_data}")
                    return None
                person_name = str(match_data.get("name") or "Unknown")
                confidence = float(match_data.get("conf") or match_data.get("confidence") or 0.0)
                employee_id = match_data.get("employeeId") or match_data.get("embeddingId")

                # Log the extracted values
                self.logger.info(
                    f"Redis match extracted - staff_id={staff_id}, person_name={person_name}, "
                    f"confidence={confidence}, employee_id={employee_id}"
                )
                print(
                    f"Redis match extracted - staff_id={staff_id}, person_name={person_name}, "
                    f"confidence={confidence}, employee_id={employee_id}"
                )

                # Check confidence threshold before returning
                min_conf = float(min_confidence if min_confidence is not None else self.default_min_confidence)
                if confidence < min_conf:
                    self.logger.debug(
                        f"Redis match confidence {confidence:.3f} below threshold {min_conf:.3f}, rejecting"
                    )
                    print(f"Redis match confidence {confidence:.3f} below threshold {min_conf:.3f}, rejecting")
                    return None

                result = RedisFaceMatchResult(
                    staff_id=str(staff_id),
                    person_name=person_name,
                    confidence=round(confidence, 3),
                    employee_id=str(employee_id) if employee_id else None,
                    raw=match_data,
                )
                
                poll_time = (time.monotonic() - start_poll_time) * 1000.0
                self.logger.info(
                    f"Redis match result created (polls={poll_count}, poll_time={poll_time:.2f}ms): "
                    f"staff_id={result.staff_id}, name={result.person_name}, conf={result.confidence}"
                )
                print(
                    f"Redis match result created (polls={poll_count}, poll_time={poll_time:.2f}ms): "
                    f"staff_id={result.staff_id}, name={result.person_name}, conf={result.confidence}"
                )
                
                return result

            # Use shorter sleep for faster response (already reduced poll_interval to 5ms)
            await asyncio.sleep(self.poll_interval)

        poll_time = (time.monotonic() - start_poll_time) * 1000.0
        self.logger.warning(
            "Timed out waiting for Redis face match result for key %s (timeout=%.3fs, polls=%d, poll_time=%.2fms)",
            result_key,
            self.response_timeout,
            poll_count,
            poll_time,
        )
        print(
            f"WARNING: Redis timeout for search_id={resolved_search_id} "
            f"(timeout={self.response_timeout:.3f}s, polls={poll_count}, poll_time={poll_time:.2f}ms)"
        )
        return None

    def _prepare_embedding_list(self, embedding: List[float]) -> List[float]:
        if isinstance(embedding, np.ndarray):
            return embedding.astype(np.float32).tolist()
        prepared = []
        try:
            for value in embedding:
                prepared.append(float(value))
        except Exception:
            self.logger.debug("Failed to convert embedding to float list", exc_info=True)
            return []
        return prepared

    def _generate_search_id(self) -> str:
        return f"face_{int(time.time() * 1000)}"

    async def _ensure_app_deployment_id(self) -> Optional[str]:
        if self._app_deployment_id:
            return self._app_deployment_id

        # Ensure locks are valid for the current event loop
        self._ensure_locks_for_current_loop()

        async with self._app_dep_lock:
            if self._app_deployment_id:
                return self._app_deployment_id

            action_id = self._action_id or self._discover_action_id()
            if not action_id:
                self.logger.warning(
                    "Unable to determine action_id for Redis face matcher"
                )
                return None

            session = await self._ensure_session()
            if session is None:
                return None

            # Use run_in_executor for Python 3.8 compatibility (asyncio.to_thread requires 3.9+)
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(
                None, self._fetch_action_details_sync, session, action_id
            )
            if not response or not response.get("success", False):
                self.logger.warning(
                    "Failed to fetch action details for action_id=%s", action_id
                )
                return None

            action_doc = response.get("data", {})
            action_details = action_doc.get("actionDetails", {})
            app_dep_id = (
                action_details.get("app_deployment_id")
                or action_details.get("appDepId")
            )
            redis_server_id = (
                action_details.get("redis_server_id")
                or action_details.get("redisServerId")
                or action_details.get("redis_serverid")
                or action_details.get("redisServerID")
            )
            if not app_dep_id:
                self.logger.warning(
                    "app_deployment_id missing in action details for action_id=%s",
                    action_id,
                )
                return None

            self._app_deployment_id = str(app_dep_id)
            # Also cache at class level for sync path to use
            with self.__class__._shared_app_dep_id_lock:
                if self.__class__._shared_app_dep_id is None:
                    self.__class__._shared_app_dep_id = self._app_deployment_id
            if redis_server_id:
                self._redis_server_id = str(redis_server_id)
            self.logger.info(
                "Resolved app deployment id %s for action_id=%s",
                self._app_deployment_id,
                action_id,
            )
            return self._app_deployment_id

    async def _ensure_session(self):
        if self._session or not HAS_MATRICE_SESSION:
            if not self._session and not HAS_MATRICE_SESSION:
                self.logger.warning(
                    "matrice_common.session unavailable; cannot create RPC session for Redis matcher"
                )
            return self._session

        # Ensure locks are valid for the current event loop
        self._ensure_locks_for_current_loop()

        async with self._session_lock:
            if self._session:
                return self._session

            access_key = os.getenv("MATRICE_ACCESS_KEY_ID")
            secret_key = os.getenv("MATRICE_SECRET_ACCESS_KEY")
            account_number = os.getenv("MATRICE_ACCOUNT_NUMBER", "")

            if not access_key or not secret_key:
                self.logger.warning(
                    "Missing Matrice credentials; cannot initialize session for Redis matcher"
                )
                return None

            try:
                self._session = Session(
                    account_number=account_number,
                    access_key=access_key,
                    secret_key=secret_key,
                )
                self.logger.info("Initialized Matrice session for Redis face matcher")
            except Exception as exc:
                self.logger.error(
                    "Failed to initialize Matrice session for Redis matcher: %s",
                    exc,
                    exc_info=True,
                )
                self._session = None

            return self._session

    async def _ensure_redis_client(self):
        # Ensure locks are valid for the current event loop
        self._ensure_locks_for_current_loop()
        
        current_loop_id = self._get_current_loop_id()
        
        # Check if we have a client but it was created in a different event loop
        if self._redis_client is not None and self._redis_client_loop_id != current_loop_id:
            self.logger.warning(
                "Redis client was created in a different event loop (old=%s, current=%s). Recreating client.",
                self._redis_client_loop_id,
                current_loop_id,
            )
            # Close old client safely (ignore errors since the loop may be closed)
            try:
                await self._redis_client.close()
            except Exception:
                pass
            self._redis_client = None
            self._redis_client_loop_id = None

        if self._redis_client:
            return self._redis_client

        async with self._redis_lock:
            # Double-check after acquiring lock
            if self._redis_client is not None and self._redis_client_loop_id == current_loop_id:
                return self._redis_client
            
            # Reset client if loop mismatch detected inside lock
            if self._redis_client is not None and self._redis_client_loop_id != current_loop_id:
                try:
                    await self._redis_client.close()
                except Exception:
                    pass
                self._redis_client = None
                self._redis_client_loop_id = None

            if not self.redis_url:
                host = os.getenv("FACE_RECOG_REDIS_HOST")
                port = os.getenv("FACE_RECOG_REDIS_PORT")
                if host and port:
                    self.redis_url = f"redis://{host}:{port}/0"

            if self.redis_url:
                try:
                    self._redis_client = aioredis.from_url(
                        self.redis_url,
                        decode_responses=True,
                        health_check_interval=30,
                    )
                    self._redis_client_loop_id = current_loop_id
                    self.logger.info(
                        "Connected Redis face matcher client to %s (stream=%s, loop_id=%s)",
                        self.redis_url,
                        self.stream_name,
                        current_loop_id,
                    )
                    return self._redis_client
                except Exception as exc:
                    self.logger.error(
                        "Failed to connect to Redis at %s: %s",
                        self.redis_url,
                        exc,
                        exc_info=True,
                    )
                    self._redis_client = None
                    self._redis_client_loop_id = None

            conn_params = await self._ensure_redis_connection_params()
            if not conn_params:
                self.logger.error(
                    "Redis connection parameters unavailable. Configure FACE_RECOG_REDIS_URL or ensure redis_server_id is set."
                )
                return None

            try:
                self._redis_client = aioredis.Redis(
                    host=conn_params.get("host"),
                    port=conn_params.get("port", 6379),
                    username=conn_params.get("username"),
                    password=conn_params.get("password") or None,
                    db=conn_params.get("db", 0),
                    ssl=conn_params.get("ssl", False),
                    decode_responses=True,
                    socket_connect_timeout=conn_params.get("connection_timeout", 120),
                    socket_timeout=conn_params.get("socket_timeout", 120),
                    retry_on_timeout=True,
                    health_check_interval=30,
                )
                self._redis_client_loop_id = current_loop_id
                self.logger.info(
                    "Connected Redis face matcher client to %s:%s (db=%s, stream=%s, loop_id=%s)",
                    conn_params.get("host"),
                    conn_params.get("port"),
                    conn_params.get("db"),
                    self.stream_name,
                    current_loop_id,
                )
            except Exception as exc:
                self.logger.error(
                    "Failed to create Redis client with fetched parameters: %s",
                    exc,
                    exc_info=True,
                )
                self._redis_client = None
                self._redis_client_loop_id = None

            return self._redis_client

    async def _ensure_redis_connection_params(self) -> Optional[Dict[str, Any]]:
        if self._redis_connection_params:
            return self._redis_connection_params

        if not self.face_client:
            self.logger.warning(
                "Cannot fetch Redis connection parameters without face_client"
            )
            return None

        await self._ensure_app_deployment_id()

        try:
            response = await self.face_client.get_redis_details()
        except Exception as exc:
            self.logger.error(
                "Failed to fetch Redis details from facial recognition server: %s",
                exc,
                exc_info=True,
            )
            return None

        if not response or not response.get("success", False):
            self.logger.warning(
                "Redis details API returned failure: %s",
                response,
            )
            return None

        data = response.get("data", {})
        host = data.get("REDIS_IP")
        port = data.get("REDIS_PORT")
        password = data.get("REDIS_PASSWORD")

        if not host or not port:
            self.logger.warning(
                "Redis details missing REDIS_IP or REDIS_PORT"
            )
            return None

        try:
            params = {
                "host": host,
                "port": int(port),
                "password": password or None,
                "username": None,
                "db": 0,
                "connection_timeout": 120,
                "socket_timeout": 120,
                "ssl": False,
            }
        except Exception as exc:
            self.logger.error(
                "Invalid Redis connection config: %s",
                exc,
                exc_info=True,
            )
            return None

        self._redis_connection_params = params
        return self._redis_connection_params

    @classmethod
    def _discover_action_id(cls) -> Optional[str]:
        candidates: List[str] = []
        try:
            cwd = Path.cwd()
            candidates.append(cwd.name)
            for parent in cwd.parents:
                candidates.append(parent.name)
        except Exception:
            pass

        try:
            usr_src = Path("/usr/src")
            if usr_src.exists():
                for child in usr_src.iterdir():
                    if child.is_dir():
                        candidates.append(child.name)
        except Exception:
            pass

        for candidate in candidates:
            if candidate and len(candidate) >= 8 and cls.ACTION_ID_PATTERN.match(candidate):
                return candidate
        return None

    def _fetch_action_details_sync(self, session, action_id: str) -> Optional[Dict[str, Any]]:
        url = f"/v1/actions/action/{action_id}/details"
        try:
            return session.rpc.get(url)
        except Exception as exc:
            self.logger.error(
                "Failed to fetch action details for action_id=%s: %s",
                action_id,
                exc,
                exc_info=True,
            )
            return None


## Removed FaceTracker fallback (using AdvancedTracker only)


class TemporalIdentityManager:
    """
    Maintains stable identity labels per tracker ID using temporal smoothing and embedding history.

    Adaptation for production: _compute_best_identity uses EmbeddingManager for local similarity
    search first (fast), then falls back to API only if needed (slow).
    """

    def __init__(
        self,
        face_client: FacialRecognitionClient,
        embedding_manager=None,
        redis_matcher: Optional[RedisFaceMatcher] = None,
        recognition_threshold: float = 0.15,
        history_size: int = 20,
        unknown_patience: int = 7,
        switch_patience: int = 5,
        fallback_margin: float = 0.05,
    ) -> None:
        self.logger = logging.getLogger(__name__)
        self.face_client = face_client
        self.embedding_manager = embedding_manager
        self.redis_matcher = redis_matcher
        self.threshold = float(recognition_threshold)
        self.history_size = int(history_size)
        self.unknown_patience = int(unknown_patience)
        self.switch_patience = int(switch_patience)
        self.fallback_margin = float(fallback_margin)
        self.tracks: Dict[Any, Dict[str, object]] = {}
        self.emb_run=False

    def _ensure_track(self, track_id: Any) -> None:
        if track_id not in self.tracks:
            self.tracks[track_id] = {
                "stable_staff_id": None,
                "stable_person_name": None,
                "stable_employee_id": None,
                "stable_score": 0.0,
                "stable_staff_details": {},
                "label_votes": defaultdict(int),  # staff_id -> votes
                "embedding_history": deque(maxlen=self.history_size),
                "unknown_streak": 0,
                "streaks": defaultdict(int),  # staff_id -> consecutive frames
            }

    async def _compute_best_identity(
        self,
        emb: List[float],
        location: str = "",
        timestamp: str = "",
        search_id: Optional[str] = None,
    ) -> Tuple[Optional[str], str, float, Optional[str], Dict[str, Any], str]:
        """
        Find best identity match using local similarity search (fast) with optional API fallback.
        Returns (staff_id, person_name, score, employee_id, staff_details, detection_type).
        
        Performance optimization: Uses EmbeddingManager for local similarity search to avoid
        slow API calls (~2000ms). Only falls back to API if local search is unavailable.
        """
        if not emb or not isinstance(emb, list):
            return None, "Unknown", 0.0, None, {}, "unknown"

        #--------------  New Redis API Fast Call Start------------------------------------------------------------------------------------------------------------------------------
        # ALWAYS attempt Redis match for every detection (required for every frame)
        if self.redis_matcher:
            try:
                self.logger.debug(f"Attempting Redis match for search_id={search_id}, embedding_len={len(emb) if emb else 0}")
                redis_start_time = time.time()
                redis_match = await self.redis_matcher.match_embedding(
                    embedding=emb,
                    search_id=search_id,
                    location=location or "",
                    min_confidence=self.threshold,  # Use recognition threshold instead of default_min_confidence
                )
                redis_latency_ms = (time.time() - redis_start_time) * 1000.0
                
                if redis_match:
                    self.logger.info(
                        f"Redis match found in {redis_latency_ms:.2f}ms - staff_id={redis_match.staff_id}, "
                        f"person_name={redis_match.person_name}, confidence={redis_match.confidence:.3f}"
                    )
                    print(
                        f"Redis match found in {redis_latency_ms:.2f}ms - staff_id={redis_match.staff_id}, "
                        f"person_name={redis_match.person_name}, confidence={redis_match.confidence:.3f}"
                    )
                    
                    if redis_match.staff_id:
                        staff_details = (
                            dict(redis_match.raw) if isinstance(redis_match.raw, dict) else {}
                        )
                        if redis_match.person_name and not staff_details.get("name"):
                            staff_details["name"] = redis_match.person_name
                        
                        # Check if confidence meets threshold
                        if float(redis_match.confidence) >= self.threshold:
                            self.logger.info(
                                "Redis embedding match ACCEPTED - staff_id=%s, person_name=%s, score=%.3f (threshold=%.3f)",
                                redis_match.staff_id,
                                redis_match.person_name,
                                float(redis_match.confidence),
                                self.threshold,
                            )
                            print(
                                f"Redis embedding match ACCEPTED - staff_id={redis_match.staff_id}, "
                                f"person_name={redis_match.person_name}, score={redis_match.confidence:.3f} "
                                f"(threshold={self.threshold:.3f})"
                            )
                            return (
                                str(redis_match.staff_id),
                                redis_match.person_name or "Unknown",
                                float(redis_match.confidence),
                                redis_match.employee_id,
                                staff_details,
                                "known",
                            )
                        else:
                            self.logger.debug(
                                "Redis embedding match REJECTED - confidence %.3f below threshold %.3f",
                                float(redis_match.confidence),
                                self.threshold,
                            )
                            print(
                                f"Redis embedding match REJECTED - confidence {redis_match.confidence:.3f} "
                                f"below threshold {self.threshold:.3f}"
                            )
                    else:
                        self.logger.warning("Redis match returned but staff_id is None/empty")
                        print("WARNING: Redis match returned but staff_id is None/empty")
                else:
                    self.logger.debug(f"No Redis match found for search_id={search_id} (took {redis_latency_ms:.2f}ms)")
                    print(f"No Redis match found for search_id={search_id} (took {redis_latency_ms:.2f}ms)")
            except Exception as exc:
                self.logger.warning(
                    "Redis face match flow failed; falling back to local search: %s",
                    exc,
                    exc_info=True,
                )
                print(f"Redis face match flow failed: {exc}")
        #--------------  New Redis API Fast Call END------------------------------------------------------------------------------------------------------------------------------
        # PRIMARY PATH: Local similarity search using EmbeddingManager (FAST - ~1-5ms)
        if self.embedding_manager and self.emb_run:
            # Defensive check: ensure embeddings are loaded before attempting search
            if not self.embedding_manager.is_ready():
                status = self.embedding_manager.get_status()
                self.logger.error(f"EmbeddingManager not ready for search - status: {status}")
                print(f"ERROR: _compute_best_identity - embeddings not ready. Status: {status}")
                return None, "Unknown", 0.0, None, {}, "unknown"
                
            try:
                local_match = self.embedding_manager._find_best_local_match(emb)
                
                if local_match:
                    staff_embedding, similarity_score = local_match
                    
                    # Extract person name from staff details
                    person_name = "Unknown"
                    staff_details = staff_embedding.staff_details if isinstance(staff_embedding.staff_details, dict) else {}
                    
                    if staff_details:
                        first_name = staff_details.get("firstName")
                        last_name = staff_details.get("lastName")
                        name = staff_details.get("name")
                        if name:
                            person_name = str(name)
                        elif first_name or last_name:
                            person_name = f"{first_name or ''} {last_name or ''}".strip() or "Unknown"
                    
                    
                    self.logger.info(f"Local embedding match - staff_id={staff_embedding.staff_id}, person_name={person_name}, score={similarity_score:.3f}")
                    
                    return (
                        str(staff_embedding.staff_id),
                        person_name,
                        float(similarity_score),
                        str(staff_embedding.employee_id),
                        staff_details,
                        "known"
                    )
                else:
                    # No local match found; log best similarity for observability
                    best_sim = 0.0
                    try:
                        best_sim = float(self.embedding_manager.get_best_similarity(emb))
                    except Exception:
                        pass
                    self.logger.debug(f"No local match found - best_similarity={best_sim:.3f}, threshold={self.threshold:.3f}")
                    
                    return None, "Unknown", 0.0, None, {}, "unknown"
                    
            except Exception as e:
                self.logger.warning(f"Local similarity search failed, falling back to API: {e}")
                # Fall through to API call below
        
#---------------------------------BACKUP MONGODB API SLOW CALL--------------------------------------------------------------------------------------
        # FALLBACK PATH: API call (SLOW - ~2000ms) - only if embedding manager not available
        # This path should rarely be used in production
        # try:
        #     self.logger.warning("Using slow API fallback for identity search - consider checking embedding manager initialization")
        #     resp = await self.face_client.search_similar_faces(
        #         face_embedding=emb,
        #         threshold=0.01,  # low threshold to always get top-1
        #         limit=1,
        #         collection="staff_enrollment",
        #         location=location,
        #         timestamp=timestamp,
        #     )
            

        # except Exception as e:
        #     self.logger.error(f"API ERROR: Failed to search similar faces in _compute_best_identity: {e}", exc_info=True)
        #     return None, "Unknown", 0.0, None, {}, "unknown"

        # try:
        #     results: List[Any] = []
        #     self.logger.debug('API Response received for identity search')
        #     if isinstance(resp, dict):
        #         if isinstance(resp.get("data"), list):
        #             results = resp.get("data", [])
        #         elif isinstance(resp.get("results"), list):
        #             results = resp.get("results", [])
        #         elif isinstance(resp.get("items"), list):
        #             results = resp.get("items", [])
        #     elif isinstance(resp, list):
        #         results = resp

        #     if not results:
        #         self.logger.debug("No identity match found from API")
        #         return None, "Unknown", 0.0, None, {}, "unknown"

        #     item = results[0] if isinstance(results, list) else results
        #     self.logger.debug(f'Top-1 match from API: {item}')
        #     # Be defensive with keys and types
        #     staff_id = item.get("staffId") if isinstance(item, dict) else None
        #     employee_id = str(item.get("_id")) if isinstance(item, dict) and item.get("_id") is not None else None
        #     score = float(item.get("score", 0.0)) if isinstance(item, dict) else 0.0
        #     detection_type = str(item.get("detectionType", "unknown")) if isinstance(item, dict) else "unknown"
        #     staff_details = item.get("staffDetails", {}) if isinstance(item, dict) else {}
        #     # Extract a person name from staff_details
        #     person_name = "Unknown"
        #     if isinstance(staff_details, dict) and staff_details:
        #         first_name = staff_details.get("firstName")
        #         last_name = staff_details.get("lastName")
        #         name = staff_details.get("name")
        #         if name:
        #             person_name = str(name)
        #         else:
        #             if first_name or last_name:
        #                 person_name = f"{first_name or ''} {last_name or ''}".strip() or "UnknowNN" #TODO:ebugging change to normal once done
        #     # If API says unknown or missing staff_id, treat as unknown
        #     if not staff_id: #or detection_type == "unknown"
        #         self.logger.debug(f"API returned unknown or missing staff_id - score={score}, employee_id={employee_id}")
        #         return None, "Unknown", float(score), employee_id, staff_details if isinstance(staff_details, dict) else {}, "unknown"
        #     self.logger.info(f"API identified face - staff_id={staff_id}, person_name={person_name}, score={score:.3f}")
        #     return str(staff_id), person_name, float(score), employee_id, staff_details if isinstance(staff_details, dict) else {}, "known"
        # except Exception as e:
        #     self.logger.error(f"Error parsing API response in _compute_best_identity: {e}", exc_info=True)
        #     return None, "Unknown", 0.0, None, {}, "unknown"
#---------------------------------BACKUP MONGODB API SLOW CALL--------------------------------------------------------------------------------------

        # If we reach here, no match was found through any method
        self.logger.debug("No identity match found - returning unknown")
        return None, "Unknown", 0.0, None, {}, "unknown"

    async def _compute_best_identity_from_history(
        self,
        track_state: Dict[str, object],
        location: str = "",
        timestamp: str = "",
        search_id: Optional[str] = None,
    ) -> Tuple[Optional[str], str, float, Optional[str], Dict[str, Any], str]:
        hist: deque = track_state.get("embedding_history", deque())  # type: ignore
        if not hist:
            return None, "Unknown", 0.0, None, {}, "unknown"
        try:
            self.logger.debug(f"Computing identity from embedding history - history_size={len(hist)}")
            proto = np.mean(np.asarray(list(hist), dtype=np.float32), axis=0)
            proto_list = proto.tolist() if isinstance(proto, np.ndarray) else list(proto)
        except Exception as e:
            self.logger.error(f"Error computing prototype from history: {e}", exc_info=True)
            proto_list = []
        return await self._compute_best_identity(
            proto_list,
            location=location,
            timestamp=timestamp,
            search_id=search_id,
        )

    async def update(
        self,
        track_id: Any,
        emb: List[float],
        eligible_for_recognition: bool,
        location: str = "",
        timestamp: str = "",
        search_id: Optional[str] = None,
    ) -> Tuple[Optional[str], str, float, Optional[str], Dict[str, Any], str]:
        """
        Update temporal identity state for a track and return a stabilized identity.
        Returns (staff_id, person_name, score, employee_id, staff_details, detection_type).
        """
        st7=time.time()
        self._ensure_track(track_id)
        s = self.tracks[track_id]

        # Update embedding history
        if emb:
            try:
                history: deque = s["embedding_history"]  # type: ignore
                history.append(_normalize_embedding(emb))
            except Exception:
                pass

        # Defaults for return values
        stable_staff_id = s.get("stable_staff_id")
        stable_person_name = s.get("stable_person_name")
        stable_employee_id = s.get("stable_employee_id")
        stable_score = float(s.get("stable_score", 0.0))
        stable_staff_details = s.get("stable_staff_details", {}) if isinstance(s.get("stable_staff_details"), dict) else {}
        
        # print("------------------FACE RECOG TEMPORAL IDENTITY MANAGER UPDATE - STABLE VALUES----------------------------")
        # print("LATENCY:",(time.time() - st7)*1000,"| Throughput fps:",(1.0 / (time.time() - st7)) if (time.time() - st7) > 0 else None)
        # print("------------------FACE RECOG TEMPORAL IDENTITY MANAGER UPDATE - STABLE VALUES----------------------------")

        if eligible_for_recognition and emb:
            st8=time.time()
            staff_id, person_name, inst_score, employee_id, staff_details, det_type = await self._compute_best_identity(
                emb, location=location, timestamp=timestamp, search_id=search_id
            )
            # print("------------------FACE RECOG TEMPORAL IDENTITY MANAGER UPDATE - COMPUTE BEST IDENTITY_I----------------------------")
            # print("LATENCY:",(time.time() - st8)*1000,"| Throughput fps:",(1.0 / (time.time() - st8)) if (time.time() - st8) > 0 else None)
            # print("------------------FACE RECOG TEMPORAL IDENTITY MANAGER UPDATE - COMPUTE BEST IDENTITY_I----------------------------")

            is_inst_known = staff_id is not None and inst_score >= self.threshold
            if is_inst_known:
                s["label_votes"][staff_id] += 1  # type: ignore
                s["streaks"][staff_id] += 1  # type: ignore
                s["unknown_streak"] = 0

                # Initialize stable if not set
                if stable_staff_id is None:
                    s["stable_staff_id"] = staff_id
                    s["stable_person_name"] = person_name
                    s["stable_employee_id"] = employee_id
                    s["stable_score"] = float(inst_score)
                    s["stable_staff_details"] = staff_details
                    return staff_id, person_name, float(inst_score), employee_id, staff_details, "known"

                # If same as stable, keep it and update score
                if staff_id == stable_staff_id:
                    s["stable_score"] = float(inst_score)
                    # prefer latest name/details if present
                    if person_name and person_name != stable_person_name:
                        s["stable_person_name"] = person_name
                    if isinstance(staff_details, dict) and staff_details:
                        s["stable_staff_details"] = staff_details
                    if employee_id:
                        s["stable_employee_id"] = employee_id
                    return staff_id, s.get("stable_person_name") or person_name, float(inst_score), s.get("stable_employee_id") or employee_id, s.get("stable_staff_details", {}), "known"

                # Competing identity: switch only if sustained and with margin & votes ratio (local parity)
                if s["streaks"][staff_id] >= self.switch_patience:  # type: ignore
                    try:
                        prev_votes = s["label_votes"].get(stable_staff_id, 0) if stable_staff_id is not None else 0  # type: ignore
                        cand_votes = s["label_votes"].get(staff_id, 0)  # type: ignore
                    except Exception:
                        prev_votes, cand_votes = 0, 0
                    if cand_votes >= max(2, 0.75 * prev_votes) and float(inst_score) >= (self.threshold + 0.02):
                        s["stable_staff_id"] = staff_id
                        s["stable_person_name"] = person_name
                        s["stable_employee_id"] = employee_id
                        s["stable_score"] = float(inst_score)
                        s["stable_staff_details"] = staff_details
                        # reset other streaks
                        try:
                            for k in list(s["streaks"].keys()):  # type: ignore
                                if k != staff_id:
                                    s["streaks"][k] = 0  # type: ignore
                        except Exception:
                            pass
                        return staff_id, person_name, float(inst_score), employee_id, staff_details, "known"

                # Do not switch yet; keep stable but return instant score/name
                return stable_staff_id, stable_person_name or person_name, float(inst_score), stable_employee_id or employee_id, stable_staff_details, "known" if stable_staff_id else "unknown"

            # Instantaneous is unknown or low score
            s["unknown_streak"] = int(s.get("unknown_streak", 0)) + 1
            if stable_staff_id is not None and s["unknown_streak"] <= self.unknown_patience:  # type: ignore
                return stable_staff_id, stable_person_name or "Unknown", float(inst_score), stable_employee_id, stable_staff_details, "known"

            # Fallback: use prototype from history
            st9=time.time()
            history_search_id = f"{search_id}_hist" if search_id else None
            fb_staff_id, fb_name, fb_score, fb_employee_id, fb_details, fb_type = await self._compute_best_identity_from_history(
                s, location=location, timestamp=timestamp, search_id=history_search_id
            )
            # print("------------------FACE RECOG TEMPORAL IDENTITY MANAGER UPDATE - COMPUTE BEST IDENTITY FROM HISTORY----------------------------")
            # print("LATENCY:",(time.time() - st9)*1000,"| Throughput fps:",(1.0 / (time.time() - st9)) if (time.time() - st9) > 0 else None)
            # print("------------------FACE RECOG TEMPORAL IDENTITY MANAGER UPDATE - COMPUTE BEST IDENTITY FROM HISTORY----------------------------")

            if fb_staff_id is not None and fb_score >= max(0.0, self.threshold - self.fallback_margin):
                s["label_votes"][fb_staff_id] += 1  # type: ignore
                s["stable_staff_id"] = fb_staff_id
                s["stable_person_name"] = fb_name
                s["stable_employee_id"] = fb_employee_id
                s["stable_score"] = float(fb_score)
                s["stable_staff_details"] = fb_details
                s["unknown_streak"] = 0
                return fb_staff_id, fb_name, float(fb_score), fb_employee_id, fb_details, "known"

            # No confident identity
            s["stable_staff_id"] = stable_staff_id
            s["stable_person_name"] = stable_person_name
            s["stable_employee_id"] = stable_employee_id
            s["stable_score"] = float(stable_score)
            s["stable_staff_details"] = stable_staff_details
            return None, "Unknown", float(inst_score), None, {}, "unknown"

        # Not eligible or no embedding; keep stable if present
        if stable_staff_id is not None:
            return stable_staff_id, stable_person_name or "Unknown", float(stable_score), stable_employee_id, stable_staff_details, "known"
        return None, "Unknown", 0.0, None, {}, "unknown"


@dataclass
class FaceRecognitionEmbeddingConfig(BaseConfig):
    """Configuration for face recognition with embeddings use case."""

    # Smoothing configuration
    enable_smoothing: bool = False
    smoothing_algorithm: str = "observability"  # "window" or "observability"
    smoothing_window_size: int = 20
    smoothing_cooldown_frames: int = 5
    smoothing_confidence_range_factor: float = 0.5

    # Base confidence threshold (separate from embedding similarity threshold)
    similarity_threshold: float = 0.45  # 0.3 Lowered to match local code - 0.45 was too conservative
    # Base confidence threshold (separate from embedding similarity threshold)
    confidence_threshold: float = 0.2  # 0.06  Detection confidence threshold
    
    # Face recognition optional features
    enable_face_tracking: bool = True  # Enable BYTE TRACKER advanced face tracking -- KEEP IT TRUE ALWAYS


    enable_auto_enrollment: bool = False  # Enable auto-enrollment of unknown faces
    enable_face_recognition: bool = (
        True  # Enable face recognition (requires credentials)
    )
    enable_unknown_face_processing: bool = (
        False  # TODO: Unable when we will be saving unkown faces # Enable unknown face cropping/uploading (requires frame data)
    )
    enable_people_activity_logging: bool = True  # Enable logging of known face activities

    usecase_categories: List[str] = field(default_factory=lambda: ["face"])

    target_categories: List[str] = field(default_factory=lambda: ["face"])

    alert_config: Optional[AlertConfig] = None

    index_to_category: Optional[Dict[int, str]] = field(
        default_factory=lambda: {0: "face"}
    )

    facial_recognition_server_id: str = ""
    session: Any = None  # Matrice session for face recognition client
    deployment_id: Optional[str] = None  # deployment ID for update_deployment call
    
    # Embedding configuration
    embedding_config: Optional[Any] = None  # Will be set to EmbeddingConfig instance
    
    
    # Track ID cache optimization settings
    enable_track_id_cache: bool = True
    cache_max_size: int = 3000
    cache_ttl: int = 3600  # Cache time-to-live in seconds (1 hour)
    
    # Search settings
    search_limit: int = 5
    search_collection: str = "staff_enrollment"


class FaceRecognitionEmbeddingUseCase(BaseProcessor):
    # Human-friendly display names for categories
    CATEGORY_DISPLAY = {"face": "face"}

    def __init__(self, config: Optional[FaceRecognitionEmbeddingConfig] = None):
        super().__init__("face_recognition")
        self.category = "security"

        self.CASE_TYPE: Optional[str] = "face_recognition"
        self.CASE_VERSION: Optional[str] = "1.0"
        # List of categories to track
        self.target_categories = ["face"]

        # Initialize smoothing tracker
        self.smoothing_tracker = None

        # Initialize advanced tracker (will be created on first use)
        self.tracker = None
        # Initialize tracking state variables
        self._total_frame_counter = 0
        self._global_frame_offset = 0

        # Track start time for "TOTAL SINCE" calculation
        self._tracking_start_time = datetime.now(
            timezone.utc
        )  # Store as datetime object for UTC

        self._track_aliases: Dict[Any, Any] = {}
        self._canonical_tracks: Dict[Any, Dict[str, Any]] = {}
        # Tunable parameters – adjust if necessary for specific scenarios
        self._track_merge_iou_threshold: float = 0.05  # IoU ≥ 0.05 →
        self._track_merge_time_window: float = 7.0  # seconds within which to merge

        self._ascending_alert_list: List[int] = []
        self.current_incident_end_timestamp: str = "N/A"

        # Session totals tracked per unique internal track id (thread-safe)
        self._recognized_track_ids = set()
        self._unknown_track_ids = set()
        self._tracking_lock = threading.Lock()

        # Person tracking: {person_id: [{"camera_id": str, "timestamp": str}, ...]}
        self.person_tracking: Dict[str, List[Dict[str, str]]] = {}

        self.face_client = None

        # Initialize PeopleActivityLogging without face client initially
        self.people_activity_logging = None

        # Initialize EmbeddingManager - will be configured in process method
        self.embedding_manager = None
        self.redis_face_matcher = None
        # Temporal identity manager for API-based top-1 identity smoothing
        self.temporal_identity_manager = None
        # Removed lightweight face tracker fallback; we always use AdvancedTracker
        # Optional gating similar to compare_similarity
        self._track_first_seen: Dict[int, int] = {}
        self._probation_frames: int = 30  # Reduced from 260 - only for "Unknown" label suppression, not recognition
        self._min_face_w: int = 30
        self._min_face_h: int = 30

        self.start_timer = None
        
        # Store config for async initialization
        self._default_config = config
        self._initialized = False
        
        # Don't call asyncio.run() in __init__ - it will fail if called from async context
        # Initialization must be done by calling await initialize(config) after instantiation
        # This is handled in PostProcessor._get_use_case_instance()

    async def initialize(self, config: Optional[FaceRecognitionEmbeddingConfig] = None, emb:bool=False) -> None:
        """
        Async initialization method to set up face client and all components.
        Must be called after __init__ before process() can be called.
        
        CRITICAL INITIALIZATION SEQUENCE:
        1. Initialize face client and update deployment
        2. Create EmbeddingManager (does NOT load embeddings yet)
        3. Synchronously load embeddings with _load_staff_embeddings() - MUST succeed
        4. Verify embeddings are actually loaded (fail-fast if not)
        5. Start background refresh thread (only after successful load)
        6. Initialize TemporalIdentityManager with loaded EmbeddingManager
        7. Final verification of all components
        
        This sequence ensures:
        - No race conditions between main load and background thread
        - Fail-fast behavior if embeddings can't be loaded
        - All components have verified embeddings before use
        
        Args:
            config: Optional config to use. If not provided, uses config from __init__.
            emb: Optional boolean to indicate if embedding manager should be loaded. If True, embedding manager will be loaded.
        Raises:
            RuntimeError: If embeddings fail to load or verification fails
        """
        print("=============== INITIALIZE() CALLED ===============")
        if self._initialized:
            self.logger.debug("Use case already initialized, skipping")
            print("=============== ALREADY INITIALIZED, SKIPPING ===============")
            return
            
        # Use provided config or fall back to default config from __init__
        init_config = config or self._default_config
        
        if not init_config:
            raise ValueError("No config provided for initialization - config is required")
            
        # Validate config type
        if not isinstance(init_config, FaceRecognitionEmbeddingConfig):
            raise TypeError(f"Invalid config type for initialization: {type(init_config)}, expected FaceRecognitionEmbeddingConfig")
            
        self.logger.info("Initializing face recognition use case with provided config")
        # print("=============== STEP 1: INITIALIZING FACE CLIENT ===============")
        
        # Initialize face client (includes deployment update)
        try:
            self.face_client = await self._get_facial_recognition_client(init_config)
            # print(f"=============== FACE CLIENT INITIALIZED: {self.face_client is not None} ===============")
            
            # Initialize People activity logging if enabled
            if init_config.enable_people_activity_logging:
                self.people_activity_logging = PeopleActivityLogging(self.face_client)
                # PeopleActivityLogging starts its background thread in __init__
                self.logger.info("People activity logging enabled and started")

            # Initialize Redis face matcher for fast remote similarity search
            try:
                redis_session = getattr(self.face_client, "session", None)
            except Exception:
                redis_session = None
            self.redis_face_matcher = RedisFaceMatcher(
                session=redis_session,
                logger=self.logger,
                face_client=self.face_client,
            )
            
            # Initialize EmbeddingManager
            if not init_config.embedding_config:
                    
                    init_config.embedding_config = EmbeddingConfig(
                        similarity_threshold=init_config.similarity_threshold,
                        confidence_threshold=init_config.confidence_threshold,
                        enable_track_id_cache=init_config.enable_track_id_cache,
                        cache_max_size=init_config.cache_max_size,
                        cache_ttl=3600,
                        background_refresh_interval=43200,
                        staff_embeddings_cache_ttl=43200,
                    )
            self.embedding_manager = EmbeddingManager(init_config.embedding_config, self.face_client)
                
            self.logger.info("Embedding manager initialized")
            if emb:
                                
                # Load staff embeddings immediately for fast startup (avoid race conditions)
                # This MUST succeed before we can proceed - fail fast if it doesn't
                
                embeddings_loaded = await self.embedding_manager._load_staff_embeddings()
                               
                if not embeddings_loaded:
                    error_msg = "CRITICAL: Failed to load staff embeddings at initialization - cannot proceed without embeddings"
                    print(f"=============== {error_msg} ===============")
                    self.logger.error(error_msg)
                    raise RuntimeError(error_msg)
                
                # Verify embeddings are actually loaded using is_ready() method
                if not self.embedding_manager.is_ready():
                    status = self.embedding_manager.get_status()
                    error_msg = f"CRITICAL: Embeddings not ready after load - status: {status}"
                    print(f"=============== {error_msg} ===============")
                    self.logger.error(error_msg)
                    raise RuntimeError(error_msg)
                
                self.logger.info(f"Successfully loaded {len(self.embedding_manager.staff_embeddings)} staff embeddings at initialization")
            
                # NOW start background refresh after successful initial load (prevents race conditions)
                if init_config.embedding_config.enable_background_refresh:
                    # print("=============== STEP 4: STARTING BACKGROUND REFRESH ===============")
                    self.embedding_manager.start_background_refresh()
                    self.logger.info("Background embedding refresh started after successful initial load")
            
            # Initialize TemporalIdentityManager with EmbeddingManager for fast local search
            # print("=============== STEP 5: INITIALIZING TEMPORAL IDENTITY MANAGER ===============")
            self.temporal_identity_manager = TemporalIdentityManager(
                face_client=self.face_client,
                embedding_manager=self.embedding_manager,
                 redis_matcher=self.redis_face_matcher,
                recognition_threshold=float(init_config.similarity_threshold),
                history_size=20,
                unknown_patience=7,
                switch_patience=5,
                fallback_margin=0.05,
            )
            self.logger.info("Temporal identity manager initialized with embedding manager for local similarity search")
            
            # Final verification before marking as initialized
            
            # if not self.embedding_manager.is_ready():
            #     status = self.embedding_manager.get_status()
            #     error_msg = f"CRITICAL: Final verification failed - embeddings not ready. Status: {status}"
            #     print(f"=============== {error_msg} ===============")
            #     self.logger.error(error_msg)
            #     raise RuntimeError(error_msg)
            
            # # Log detailed status for debugging
            # status = self.embedding_manager.get_status()

            
            self._initialized = True
            self.logger.info("Face recognition use case fully initialized and verified")
                      
        except Exception as e:
            self.logger.error(f"Error during use case initialization: {e}", exc_info=True)
            raise RuntimeError(f"Failed to initialize face recognition use case: {e}") from e

    def _extract_camera_info_from_stream(self, stream_info: Optional[Dict[str, Any]]) -> Dict[str, str]:
        """
        Extract camera_name, camera_id, and location_id from stream_info.
        
        Handles multiple sources and shapes for camera_id/camera_name/location_id to ensure
        correct extraction even when a single container is connected to multiple camera streams.
        
        Supported stream_info shapes (seen across pipeline/components):
        - stream_info["camera_info"]
        - stream_info["input_settings"]["camera_info"]
        - stream_info["input_settings"]["input_stream"]["camera_info"]
        - stream_info["input_streams"][i]["input_stream"]["camera_info"]
        - camera_id derived from stream_info["topic"] suffix markers ("_input_topic" or "_input-topic")
        
        Args:
            stream_info: Stream information dictionary
            
        Returns:
            Dict with camera_name, camera_id, location_id
        """
        camera_name = ""
        camera_id = ""
        location_id = ""
        
        if not stream_info or not isinstance(stream_info, dict):
            self.logger.debug("stream_info is None/invalid, returning empty camera info")
            return {"camera_name": camera_name, "camera_id": camera_id, "location_id": location_id}

        def _to_str(value: Any) -> str:
            """Convert common stream-info values to a safe string."""
            if value is None:
                return ""
            if isinstance(value, str):
                return value.strip()
            if isinstance(value, (int, float)):
                return str(value)
            if isinstance(value, dict):
                return ""
            if isinstance(value, (list, tuple, set)):
                for item in value:
                    s = _to_str(item)
                    if s:
                        return s
                return ""
            try:
                return str(value).strip()
            except Exception:
                return ""

        def _dict_get_str(d: Any, *keys: str) -> str:
            """Get first non-empty key from dict as string."""
            if not isinstance(d, dict):
                return ""
            for k in keys:
                val = _to_str(d.get(k))
                if val:
                    return val
            return ""

        def _extract_camera_id_from_topic(topic_val: Any) -> str:
            """Extract camera_id from topic formats like '{camera_id}_input_topic' or '{camera_id}_input-topic'."""
            topic = _to_str(topic_val)
            if not topic:
                return ""
            for suffix in ("_input_topic", "_input-topic"):
                if topic.endswith(suffix):
                    return topic[: -len(suffix)].strip()
            for marker in ("_input_topic", "_input-topic"):
                if marker in topic:
                    return topic.split(marker)[0].strip()
            return ""

        def _extract_camera_id_from_frame_id(frame_id_val: Any) -> str:
            """
            Best-effort fallback: extract a stable camera/stream identifier from frame_id.

            Observed upstream format (py_inference legacy mode):
              - 'legacy_{hexId}_{suffix}'
            Example:
              - 'legacy_694e7603a086e13d9c95dd3d_51b30e93'

            We ONLY accept the middle segment if it looks like a hex identifier (>= 8 chars)
            to avoid mis-parsing arbitrary frame_id formats.
            """
            fid = _to_str(frame_id_val)
            if not fid:
                return ""
            if fid.startswith("legacy_"):
                parts = fid.split("_")
                if len(parts) >= 3:
                    candidate = parts[1].strip()
                    if candidate and re.fullmatch(r"[0-9a-f]{8,}", candidate, re.IGNORECASE):
                        return candidate
            return ""

        input_settings = stream_info.get("input_settings") or {}
        if not isinstance(input_settings, dict):
            input_settings = {}

        camera_info_root = stream_info.get("camera_info") or {}
        if not isinstance(camera_info_root, dict):
            camera_info_root = {}

        camera_info_input_settings = input_settings.get("camera_info") or {}
        if not isinstance(camera_info_input_settings, dict):
            camera_info_input_settings = {}

        input_stream = input_settings.get("input_stream") or {}
        if not isinstance(input_stream, dict):
            input_stream = {}

        camera_info_input_stream = input_stream.get("camera_info") or {}
        if not isinstance(camera_info_input_stream, dict):
            camera_info_input_stream = {}

        input_streams = stream_info.get("input_streams") or []
        input_stream_candidates: List[Dict[str, Any]] = []
        camera_info_input_streams: List[Dict[str, Any]] = []
        if isinstance(input_streams, list):
            for item in input_streams:
                if not isinstance(item, dict):
                    continue
                inner = item.get("input_stream", item)
                if not isinstance(inner, dict):
                    continue
                input_stream_candidates.append(inner)
                ci = inner.get("camera_info") or {}
                if isinstance(ci, dict) and ci:
                    camera_info_input_streams.append(ci)

        topic_camera_id = (
            _extract_camera_id_from_topic(stream_info.get("topic"))
            or _extract_camera_id_from_topic(input_settings.get("topic"))
        )
        if not topic_camera_id:
            topics_val = stream_info.get("topics")
            if isinstance(topics_val, (list, tuple, set)):
                for t in topics_val:
                    topic_camera_id = _extract_camera_id_from_topic(t)
                    if topic_camera_id:
                        break

        camera_info_sources: List[Dict[str, Any]] = [
            camera_info_root,
            camera_info_input_settings,
            camera_info_input_stream,
        ] + camera_info_input_streams

        def _camera_id_from_camera_info(ci: Dict[str, Any]) -> str:
            return _dict_get_str(ci, "camera_id", "cameraId", "_id", "id")

        matched_ci: Dict[str, Any] = {}
        if topic_camera_id:
            camera_id = topic_camera_id
            for ci in camera_info_sources:
                if _camera_id_from_camera_info(ci) == camera_id:
                    matched_ci = ci
                    break

        if not camera_id:
            camera_id = (
                _dict_get_str(stream_info, "camera_id", "cameraId")
                or _dict_get_str(input_settings, "camera_id", "cameraId")
                or _camera_id_from_camera_info(camera_info_root)
                or _camera_id_from_camera_info(camera_info_input_settings)
                or _camera_id_from_camera_info(camera_info_input_stream)
            )
            if not camera_id:
                for candidate in input_stream_candidates:
                    camera_id = _dict_get_str(candidate, "camera_id", "cameraId", "_id", "id")
                    if camera_id:
                        break
            if not camera_id:
                camera_id = topic_camera_id

        # Final fallback: derive camera_id from frame_id if stream_info doesn't include camera_info/topic
        if not camera_id:
            camera_id = _extract_camera_id_from_frame_id(stream_info.get("frame_id"))

        # Use matched camera_info (if found) to set camera_name/location_id
        if matched_ci:
            camera_name = _dict_get_str(matched_ci, "camera_name", "cameraName", "name")
            location_id = _dict_get_str(matched_ci, "location", "location_id", "locationId")

        if not camera_name:
            camera_name = (
                _dict_get_str(camera_info_root, "camera_name", "cameraName", "name")
                or _dict_get_str(camera_info_input_settings, "camera_name", "cameraName", "name")
                or _dict_get_str(camera_info_input_stream, "camera_name", "cameraName", "name")
                or _dict_get_str(stream_info, "camera_name", "cameraName")
                or _dict_get_str(input_settings, "camera_name", "cameraName")
            )
            if not camera_name:
                for ci in camera_info_input_streams:
                    camera_name = _dict_get_str(ci, "camera_name", "cameraName", "name")
                    if camera_name:
                        break

        if not location_id:
            location_id = (
                _dict_get_str(camera_info_root, "location", "location_id", "locationId")
                or _dict_get_str(camera_info_input_settings, "location", "location_id", "locationId")
                or _dict_get_str(camera_info_input_stream, "location", "location_id", "locationId")
                or _dict_get_str(stream_info, "location_id", "location", "locationId")
                or _dict_get_str(input_settings, "location_id", "location", "locationId")
            )
            if not location_id:
                for ci in camera_info_input_streams:
                    location_id = _dict_get_str(ci, "location", "location_id", "locationId")
                    if location_id:
                        break

        self.logger.debug(
            "Extracted camera info - camera_name: '%s', camera_id: '%s', location_id: '%s'",
            camera_name,
            camera_id,
            location_id,
        )

        return {"camera_name": camera_name, "camera_id": camera_id, "location_id": location_id}

    async def _fetch_location_name(self, location_id: str) -> str:
        """
        Fetch location name from API using location_id.
        
        Args:
            location_id: The location ID to look up
            
        Returns:
            Location name string, or 'Entry Reception' as default if API fails
        """
        global _location_name_cache
        default_location = "Entry Reception"
        
        if not location_id:
            self.logger.debug(f"[LOCATION] No location_id provided, using default: '{default_location}'")
            return default_location
        
        # Check cache first
        if location_id in _location_name_cache:
            cached_name = _location_name_cache[location_id]
            self.logger.debug(f"[LOCATION] Using cached location name for '{location_id}': '{cached_name}'")
            return cached_name
        
        # Need a session to make API call
        if not self.face_client or not hasattr(self.face_client, 'session') or not self.face_client.session:
            self.logger.warning(f"[LOCATION] No session available, using default: '{default_location}'")
            return default_location
        
        try:
            endpoint = f"/v1/inference/get_location/{location_id}"
            self.logger.info(f"[LOCATION] Fetching location name from API: {endpoint}")
            
            response = self.face_client.session.rpc.get(endpoint)
            
            if response and isinstance(response, dict):
                success = response.get("success", False)
                if success:
                    data = response.get("data", {})
                    location_name = data.get("locationName", default_location)
                    self.logger.info(f"[LOCATION] ✓ Fetched location name: '{location_name}' for location_id: '{location_id}'")
                    
                    # Cache the result
                    _location_name_cache[location_id] = location_name
                    return location_name
                else:
                    self.logger.warning(
                        f"[LOCATION] API returned success=false for location_id '{location_id}': "
                        f"{response.get('message', 'Unknown error')}"
                    )
            else:
                self.logger.warning(f"[LOCATION] Invalid response format from API: {response}")
                
        except Exception as e:
            self.logger.error(f"[LOCATION] Error fetching location name for '{location_id}': {e}", exc_info=True)
        
        # Use default on any failure
        self.logger.info(f"[LOCATION] Using default location name: '{default_location}'")
        _location_name_cache[location_id] = default_location
        return default_location

    async def _get_facial_recognition_client(
        self, config: FaceRecognitionEmbeddingConfig
    ) -> FacialRecognitionClient:
        """Get facial recognition client and update deployment"""
        # Initialize face recognition client if not already done
        if self.face_client is None:
            self.logger.info(
                f"Initializing face recognition client with server ID: {config.facial_recognition_server_id}"
            )
            print(f"=============== CONFIG: {config} ===============")  
            print(f"=============== CONFIG.SESSION: {config.session} ===============")  
            account_number = os.getenv("MATRICE_ACCOUNT_NUMBER", "")
            access_key_id = os.getenv("MATRICE_ACCESS_KEY_ID", "")
            secret_key = os.getenv("MATRICE_SECRET_ACCESS_KEY", "")
            project_id = os.getenv("MATRICE_PROJECT_ID", "")
            
            self.logger.info(f"[PROJECT_ID] Initial project_id from env: '{project_id}'")
            
            self.session1 = Session(
                account_number=account_number,
                access_key=access_key_id,
                secret_key=secret_key,
                project_id=project_id,
            )
            self.face_client = FacialRecognitionClient(
                server_id=config.facial_recognition_server_id, session=self.session1
            )
            self.logger.info("Face recognition client initialized")
            
            # After FacialRecognitionClient initialization, it may have fetched project_id from action details
            # and updated MATRICE_PROJECT_ID env var. Update session1 with the correct project_id.
            updated_project_id = self.face_client.project_id or os.getenv("MATRICE_PROJECT_ID", "")
            if updated_project_id and updated_project_id != project_id:
                self.logger.info(f"[PROJECT_ID] Project ID updated by FacialRecognitionClient: '{updated_project_id}'")
                try:
                    self.session1.update(updated_project_id)
                    self.logger.info(f"[PROJECT_ID] Updated session1 with project_id: '{updated_project_id}'")
                except Exception as e:
                    self.logger.warning(f"[PROJECT_ID] Failed to update session1 with project_id: {e}")
            elif updated_project_id:
                self.logger.info(f"[PROJECT_ID] Using project_id: '{updated_project_id}'")

            # Call update_deployment if deployment_id is provided
            if config.deployment_id:
                try:
                    # Create temporary RedisFaceMatcher to get app_deployment_id using verified method
                    redis_session = getattr(self.face_client, "session", None) or config.session
                    temp_redis_matcher = RedisFaceMatcher(
                        session=redis_session,
                        logger=self.logger,
                        face_client=self.face_client,
                    )
                    app_deployment_id = await temp_redis_matcher._ensure_app_deployment_id()

                    if app_deployment_id:
                        self.logger.info(f"Updating deployment action with app_deployment_id: {app_deployment_id}")
                        response = await self.face_client.update_deployment_action(app_deployment_id)
                        if response:
                            self.logger.info(f"Successfully updated deployment action {app_deployment_id}")
                        else:
                            self.logger.warning(f"Failed to update deployment: {response.get('error', 'Unknown error')}")
                    else:
                        self.logger.warning("Could not resolve app_deployment_id, skipping deployment action update")

                    self.logger.info(f"Updating deployment with ID: {config.deployment_id}")
                    response = await self.face_client.update_deployment(config.deployment_id)
                    if response:
                        self.logger.info(f"Successfully updated deployment {config.deployment_id}")
                    else:
                        self.logger.warning(f"Failed to update deployment: {response.get('error', 'Unknown error')}")
                except Exception as e:
                    self.logger.error(f"Exception while updating deployment: {e}", exc_info=True)
            else:
                self.logger.debug("No deployment_id provided, skipping deployment update")

        return self.face_client

    async def process(
        self,
        data: Any,
        config: ConfigProtocol,
        input_bytes: Optional[bytes] = None,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        """
        Main entry point for face recognition with embeddings post-processing.
        Applies all standard processing plus face recognition and auto-enrollment.
        
        Thread-safe: Uses local variables for per-request state and locks for global totals.
        Order-preserving: Processes detections sequentially to maintain input order.
        """
        processing_start = time.time()
        # Ensure config is correct type
        self.logger.info(f"[CONFIG-PRINT]-------------------------- {config} --------------------------")
        self.logger.info(f"[STREAM-PRINT]-------------------------- {stream_info} --------------------------")
        
        if not isinstance(config, FaceRecognitionEmbeddingConfig):
            return self.create_error_result(
                "Invalid config type",
                usecase=self.name,
                category=self.category,
                context=context,
            )
        if context is None:
            context = ProcessingContext()
        
        # Defensive check: Ensure context is ProcessingContext object (production safety)
        # This handles edge cases where parameter mismatch might pass a dict as context
        if not isinstance(context, ProcessingContext):
            self.logger.warning(
                f"Context parameter is not ProcessingContext (got {type(context).__name__}, {context}). "
                "Creating new ProcessingContext. This may indicate a parameter mismatch in the caller."
            )
            context = ProcessingContext()

        # Lazy initialization on first process() call (similar to tracker initialization pattern)
        if not self._initialized:
            self.logger.info("Initializing face recognition use case on first process() call...")
            try:
                await self.initialize(config)
                self.logger.info("Face recognition use case initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize face recognition use case: {e}", exc_info=True)
                return self.create_error_result(
                    f"Initialization failed: {e}",
                    usecase=self.name,
                    category=self.category,
                    context=context,
                )

        # Ensure confidence threshold is set
        if not config.confidence_threshold:
            config.confidence_threshold = 0.35

        
        # Detect input format and store in context
        input_format = match_results_structure(data)
        context.input_format = input_format

        context.confidence_threshold = config.confidence_threshold

        # Parse face recognition model output format (with embeddings)
        processed_data = self._parse_face_model_output(data)
        # Normalize embeddings early for consistency (local parity)
        for _det in processed_data:
            try:
                emb = _det.get("embedding", []) or []
                if emb:
                    _det["embedding"] = _normalize_embedding(emb)
            except Exception:
                pass
        # Ignore any pre-existing track_id on detections (we rely on our own tracker)
        for _det in processed_data:
            if isinstance(_det, dict) and "track_id" in _det:
                try:
                    del _det["track_id"]
                except Exception:
                    _det["track_id"] = None

        # Apply standard confidence filtering
        if config.confidence_threshold is not None:
            processed_data = filter_by_confidence(
                processed_data, config.confidence_threshold
            )
            self.logger.debug(
                f"Applied confidence filtering with threshold {config.confidence_threshold}"
            )
        else:
            self.logger.debug(
                "Did not apply confidence filtering since threshold not provided"
            )

        # Apply category mapping if provided
        if config.index_to_category:
            processed_data = apply_category_mapping(
                processed_data, config.index_to_category
            )
            self.logger.debug("Applied category mapping")

        # Apply category filtering
        if config.target_categories:
            processed_data = filter_by_categories(
                processed_data, config.target_categories
            )
            self.logger.debug("Applied category filtering")

        
        # Advanced tracking (BYTETracker-like) - only if enabled
        if config.enable_face_tracking:
            from ..advanced_tracker import AdvancedTracker
            from ..advanced_tracker.config import TrackerConfig

            # Create tracker instance if it doesn't exist (preserves state across frames)
            if self.tracker is None:
                tracker_config = TrackerConfig(
                                track_high_thresh=0.5,
                                track_low_thresh=0.05,
                                new_track_thresh=0.5,
                                match_thresh=0.8,
                                track_buffer=int(600),  # Increased to match local code - allows longer occlusions
                                max_time_lost=int(300),  # Increased to match local code
                                fuse_score=True,
                                enable_gmc=False,
                                frame_rate=int(20)
                )

                self.tracker = AdvancedTracker(tracker_config)
                self.logger.info(
                    "Initialized AdvancedTracker for Face Recognition with thresholds: "
                    f"high={tracker_config.track_high_thresh}, "
                    f"low={tracker_config.track_low_thresh}, "
                    f"new={tracker_config.new_track_thresh}"
                )

            # The tracker expects the data in the same format as input
            # It will add track_id and frame_id to each detection (we rely ONLY on these)
            processed_data = self.tracker.update(processed_data)
        else:
            self.logger.debug("Advanced face tracking disabled; continuing without external track IDs")

        # Initialize local recognition summary variables
        current_recognized_count = 0
        current_unknown_count = 0
        recognized_persons = {}
        current_frame_staff_details = {}


        # Extract camera info and fetch location name
        camera_info_extracted = self._extract_camera_info_from_stream(stream_info)
        camera_name = camera_info_extracted.get("camera_name", "")
        camera_id = camera_info_extracted.get("camera_id", "")
        location_id = camera_info_extracted.get("location_id", "")
        
        # Fetch actual location name from API
        location_name = await self._fetch_location_name(location_id)
        self.logger.debug(f"Using location_name: '{location_name}', camera_name: '{camera_name}', camera_id: '{camera_id}'")

        # Process face recognition for each detection (if enabled)
        if config.enable_face_recognition:
            # Additional safety check: verify embeddings are still loaded and ready
            # if not self.embedding_manager or not self.embedding_manager.is_ready():
            #     status = self.embedding_manager.get_status() if self.embedding_manager else {}
            #     error_msg = f"CRITICAL: Cannot process face recognition - embeddings not ready. Status: {status}"
            #     self.logger.error(error_msg)
            #     print(f"ERROR: {error_msg}")
            #     return self.create_error_result(
            #         error_msg,
            #         usecase=self.name,
            #         category=self.category,
            #         context=context,
            #     )
            
            face_recognition_result = await self._process_face_recognition(
                processed_data, config, stream_info, input_bytes,
                camera_name=camera_name, camera_id=camera_id, location_name=location_name
            )
            processed_data, current_recognized_count, current_unknown_count, recognized_persons, current_frame_staff_details = face_recognition_result
        else:
            # Just add default face recognition fields without actual recognition
            for detection in processed_data:
                detection["person_id"] = None
                detection["person_name"] = "Unknown"
                detection["recognition_status"] = "disabled"
                detection["enrolled"] = False


        # Update tracking state for total count per label
        self._update_tracking_state(processed_data)

        # Update frame counter
        self._total_frame_counter += 1

        # Extract frame information from stream_info
        frame_number = None
        if stream_info:
            input_settings = stream_info.get("input_settings", {})
            start_frame = input_settings.get("start_frame")
            end_frame = input_settings.get("end_frame")
            # If start and end frame are the same, it's a single frame
            if (
                start_frame is not None
                and end_frame is not None
                and start_frame == end_frame
            ):
                frame_number = start_frame

        # Compute summaries and alerts
        general_counting_summary = calculate_counting_summary(data)
        counting_summary = self._count_categories(processed_data, config)
        # Add total unique counts after tracking using only local state
        total_counts = self.get_total_counts()
        counting_summary["total_counts"] = total_counts

        # NEW: Add face recognition summary
        counting_summary.update(self._get_face_recognition_summary(
            current_recognized_count, current_unknown_count, recognized_persons
        ))


        # Add detections to the counting summary (standard pattern for detection use cases)
        # Ensure display label is present for UI (does not affect logic/counters)
        for _d in processed_data:
            if "display_name" not in _d:
                name = _d.get("person_name")
                # Use person_name only if recognized; otherwise leave empty to honor probation logic
                _d["display_name"] = name if _d.get("recognition_status") == "known" else (_d.get("display_name", "") or "")
        counting_summary["detections"] = processed_data

        alerts = self._check_alerts(counting_summary, frame_number, config)

        # Step: Generate structured incidents, tracking stats and business analytics with frame-based keys
        incidents_list = self._generate_incidents(
            counting_summary, alerts, config, frame_number, stream_info
        )
        tracking_stats_list = self._generate_tracking_stats(
            counting_summary, alerts, config, frame_number, stream_info, current_frame_staff_details
        )
        business_analytics_list = self._generate_business_analytics(
            counting_summary, alerts, config, stream_info, is_empty=True
        )
        summary_list = self._generate_summary(incidents_list, tracking_stats_list, business_analytics_list)

        # Extract frame-based dictionaries from the lists
        incidents = incidents_list[0] if incidents_list else {}
        tracking_stats = tracking_stats_list[0] if tracking_stats_list else {}
        business_analytics = (
            business_analytics_list[0] if business_analytics_list else {}
        )
        summary = summary_list[0] if summary_list else {}


        agg_summary = {
            str(frame_number): {
                "incidents": incidents,
                "tracking_stats": tracking_stats,
                "business_analytics": business_analytics,
                "alerts": alerts,
                "human_text": summary,
                "person_tracking": self.get_person_tracking_summary(),
            }
        }

        context.mark_completed()

        # Build result object following the standard pattern - same structure as people counting
        result = self.create_result(
            data={"agg_summary": agg_summary},
            usecase=self.name,
            category=self.category,
            context=context,
        )
        proc_time = time.time() - processing_start
        processing_latency_ms = proc_time * 1000.0
        processing_fps = (1.0 / proc_time) if proc_time > 0 else None
        # Log the performance metrics using the module-level logger
        print("latency in ms:",processing_latency_ms,"| Throughput fps:",processing_fps,"| Frame_Number:",self._total_frame_counter)

        return result

    def _parse_face_model_output(self, data: Any) -> List[Dict]:
        """Parse face recognition model output to standard detection format, preserving embeddings"""
        processed_data = []

        if isinstance(data, dict):
            # Handle frame-based format: {"0": [...], "1": [...]}
            for frame_id, frame_detections in data.items():
                if isinstance(frame_detections, list):
                    for detection in frame_detections:
                        if isinstance(detection, dict):
                            # Convert to standard format but preserve face-specific fields
                            standard_detection = {
                                "category": detection.get("category", "face"),
                                "confidence": detection.get("confidence", 0.0),
                                "bounding_box": detection.get("bounding_box", {}),
                                "track_id": detection.get("track_id", ""),
                                "frame_id": detection.get("frame_id", frame_id),
                                # Preserve face-specific fields
                                "embedding": detection.get("embedding", []),
                                "landmarks": detection.get("landmarks", None),
                                "fps": detection.get("fps", 30),
                            }
                            processed_data.append(standard_detection)
        elif isinstance(data, list):
            # Handle list format
            for detection in data:
                if isinstance(detection, dict):
                    # Convert to standard format and ensure all required fields exist
                    standard_detection = {
                        "category": detection.get("category", "face"),
                        "confidence": detection.get("confidence", 0.0),
                        "bounding_box": detection.get("bounding_box", {}),
                        "track_id": detection.get("track_id", ""),
                        "frame_id": detection.get("frame_id", 0),
                        # Preserve face-specific fields
                        "embedding": detection.get("embedding", []),
                        "landmarks": detection.get("landmarks", None),
                        "fps": detection.get("fps", 30),
                        "metadata": detection.get("metadata", {}),
                    }
                    processed_data.append(standard_detection)

        return processed_data

    def _build_search_id(self, track_key: Any, frame_id: Optional[Any]) -> str:
        """Generate a deterministic Redis search identifier per detection."""
        base_frame = frame_id if frame_id is not None else self._total_frame_counter
        safe_track = str(track_key if track_key is not None else "na").replace(" ", "_")
        return f"face_{base_frame}_{safe_track}"

    def _extract_frame_from_data(self, input_bytes: bytes) -> Optional[np.ndarray]:
        """
        Extract frame from original model data

        Args:
            original_data: Original data from model (same format as model receives)

        Returns:
            np.ndarray: Frame data or None if not found
        """
        try:
            try:
                if isinstance(input_bytes, str):
                    frame_bytes = base64.b64decode(input_bytes)
                else:
                    frame_bytes = input_bytes
                nparr = np.frombuffer(frame_bytes, np.uint8)
                frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                return frame
            except Exception as e:
                self.logger.debug(f"Could not decode direct frame data: {e}")

            return None

        except Exception as e:
            self.logger.debug(f"Error extracting frame from data: {e}")
            return None

    # Removed unused _calculate_bbox_area_percentage (not referenced)

    async def _process_face_recognition(
        self,
        detections: List[Dict],
        config: FaceRecognitionEmbeddingConfig,
        stream_info: Optional[Dict[str, Any]] = None,
        input_bytes: Optional[bytes] = None,
        camera_name: str = "",
        camera_id: str = "",
        location_name: str = "",
    ) -> List[Dict]:
        """Process face recognition for each detection with embeddings"""

        # Face client is initialized in initialize(); if absent, this indicates a prior init failure
        if not self.face_client:
            self.logger.error("Face client not initialized; initialize() must succeed before processing")
            return []

        # Initialize unknown faces storage if not exists
        if not hasattr(self, "unknown_faces_storage"):
            self.unknown_faces_storage = {}

        # Initialize frame availability warning flag to avoid spam
        if not hasattr(self, "_frame_warning_logged"):
            self._frame_warning_logged = False

        # Initialize per-request tracking (thread-safe)
        current_recognized_count = 0
        current_unknown_count = 0
        recognized_persons = {}
        current_frame_staff_details = {}  # Store staff details for current frame

        # Extract frame from original data for cropping unknown faces
        current_frame = (
            self._extract_frame_from_data(input_bytes) if input_bytes else None
        )

        # Log frame availability once per session
        if current_frame is None and not self._frame_warning_logged:
            if config.enable_unknown_face_processing:
                self.logger.info(
                    "Frame data not available in model output - unknown face cropping/uploading will be skipped. "
                    "To disable this feature entirely, set enable_unknown_face_processing=False"
                )
            self._frame_warning_logged = True

        # Use the location_name passed from process() (fetched from API)
        location = location_name if location_name else "Entry Reception"

        # Extract rtp_number from stream_info (same pattern as license_plate_monitoring)
        input_settings = stream_info.get("input_settings", {}) if stream_info and isinstance(stream_info.get("input_settings", {}), dict) else {}
        rtp_number = (
            (stream_info or {}).get("rtp_number", "") or
            (stream_info or {}).get("rtpNumber", "") or
            input_settings.get("rtp_number", "") or
            input_settings.get("rtpNumber", "") or
            ""
        )

        # Generate current timestamp
        current_timestamp = datetime.now(timezone.utc).isoformat()

        final_detections = []
        # Process detections sequentially to preserve order
        for detection in detections:
            
            # Process each detection sequentially with await to preserve order
            st1=time.time()
            processed_detection = await self._process_face(
                detection, current_frame, location, current_timestamp, config,
                current_recognized_count, current_unknown_count, 
                recognized_persons, current_frame_staff_details,
                camera_name=camera_name, camera_id=camera_id, rtp_number=rtp_number
            )
            # print("------------------WHOLE FACE RECOG PROCESSING DETECTION----------------------------")
            # print("LATENCY:",(time.time() - st1)*1000,"| Throughput fps:",(1.0 / (time.time() - st1)) if (time.time() - st1) > 0 else None)
            # print("------------------WHOLE FACE RECOG PROCESSING DETECTION----------------------------")

            # Include both known and unknown faces in final detections (maintains original order)
            if processed_detection:
                final_detections.append(processed_detection)
                # Update local counters based on processed detection
                if processed_detection.get("recognition_status") == "known":
                    staff_id = processed_detection.get("person_id")
                    if staff_id:
                        current_frame_staff_details[staff_id] = processed_detection.get("person_name", "Unknown")
                        current_recognized_count += 1
                        recognized_persons[staff_id] = recognized_persons.get(staff_id, 0) + 1
                elif processed_detection.get("recognition_status") == "unknown":
                    current_unknown_count += 1

        return final_detections, current_recognized_count, current_unknown_count, recognized_persons, current_frame_staff_details

    async def _process_face(
        self,
        detection: Dict,
        current_frame: np.ndarray,
        location: str = "",
        current_timestamp: str = "",
        config: FaceRecognitionEmbeddingConfig = None,
        current_recognized_count: int = 0,
        current_unknown_count: int = 0,
        recognized_persons: Dict = None,
        current_frame_staff_details: Dict = None,
        camera_name: str = "",
        camera_id: str = "",
        rtp_number: str = "",
    ) -> Dict:

        # Extract and validate embedding using EmbeddingManager
        st2=time.time()
        detection, embedding = self.embedding_manager.extract_embedding_from_detection(detection)
        if not embedding:
            return None

        # Internal tracker-provided ID (from AdvancedTracker; ignore upstream IDs entirely)
        track_id = detection.get("track_id")
        # print("------------------FACE RECOG EMBEDDING EXTRACTION----------------------------")
        # print("LATENCY:",(time.time() - st2)*1000,"| Throughput fps:",(1.0 / (time.time() - st2)) if (time.time() - st2) > 0 else None)
        # print("------------------FACE RECOG EMBEDDING EXTRACTION----------------------------")

        # Determine if detection is eligible for recognition (similar to compare_similarity gating)
        bbox = detection.get("bounding_box", {}) or {}
        x1 = int(bbox.get("xmin", bbox.get("x1", 0)))
        y1 = int(bbox.get("ymin", bbox.get("y1", 0)))
        x2 = int(bbox.get("xmax", bbox.get("x2", 0)))
        y2 = int(bbox.get("ymax", bbox.get("y2", 0)))
        w_box = max(1, x2 - x1)
        h_box = max(1, y2 - y1)
        frame_id = detection.get("frame_id", None) #TODO: Maybe replace this with stream_info frame_id

        track_key = track_id if track_id is not None else f"no_track_{id(detection)}"
        search_id = self._build_search_id(track_key, frame_id)

        # Track probation age strictly by internal tracker id
        if track_id is not None:
            if track_id not in self._track_first_seen:
                try:
                    self._track_first_seen[track_id] = int(frame_id) if frame_id is not None else self._total_frame_counter
                except Exception:
                    self._track_first_seen[track_id] = self._total_frame_counter
            age_frames = (int(frame_id) if frame_id is not None else self._total_frame_counter) - int(self._track_first_seen.get(track_id, 0)) + 1
        else:
            age_frames = 1

        # Eligible for recognition if face is large enough (lowered threshold to match local code behavior)
        eligible_for_recognition = (w_box >= self._min_face_w and h_box >= self._min_face_h)

        # Primary: API-based identity smoothing via TemporalIdentityManager
        staff_id = None
        person_name = ""
        similarity_score = 0.0
        employee_id = None
        staff_details: Dict[str, Any] = {}
        detection_type = "unknown"
        try:
            if self.temporal_identity_manager:
                if not eligible_for_recognition:
                    # Mirror compare_similarity: when not eligible, keep stable label if present
                    s = self.temporal_identity_manager.tracks.get(track_key, {})
                    if isinstance(s, dict):
                        stable_staff_id = s.get("stable_staff_id")
                        stable_person_name = s.get("stable_person_name") or "Unknown"
                        stable_employee_id = s.get("stable_employee_id")
                        stable_score = float(s.get("stable_score", 0.0))
                        stable_staff_details = s.get("stable_staff_details") if isinstance(s.get("stable_staff_details"), dict) else {}
                        if stable_staff_id is not None:
                            staff_id = stable_staff_id
                            person_name = stable_person_name
                            employee_id = stable_employee_id
                            similarity_score = stable_score
                            staff_details = stable_staff_details
                            detection_type = "known"
                        else:
                            detection_type = "unknown"
                    # Also append embedding to history for temporal smoothing
                    if embedding:
                        try:
                            
                            self.temporal_identity_manager._ensure_track(track_key)
                            hist = self.temporal_identity_manager.tracks[track_key]["embedding_history"]  # type: ignore
                            hist.append(_normalize_embedding(embedding))  # type: ignore
                        except Exception:
                            pass
                else: #if eligible for recognition
                    st3=time.time()
                    staff_id, person_name, similarity_score, employee_id, staff_details, detection_type = await self.temporal_identity_manager.update(
                        track_id=track_key,
                        emb=embedding,
                        eligible_for_recognition=True,
                        location=location,
                        timestamp=current_timestamp,
                        search_id=search_id,
                    )
                    # print("------------------FACE RECOG TEMPORAL IDENTITY MANAGER UPDATE----------------------------")
                    # print("LATENCY:",(time.time() - st3)*1000,"| Throughput fps:",(1.0 / (time.time() - st3)) if (time.time() - st3) > 0 else None)
                    # print("------------------FACE RECOG TEMPORAL IDENTITY MANAGER UPDATE----------------------------")
        except Exception as e:
            self.logger.warning(f"TemporalIdentityManager update failed: {e}")

        # # Fallback: if still unknown and we have an EmbeddingManager, use local search
        # if (staff_id is None or detection_type == "unknown") and self.embedding_manager is not None:
        #     try:
        #         search_result = await self.embedding_manager.search_face_embedding(
        #             embedding=embedding,
        #             track_id=track_id,
        #             location=location,
        #             timestamp=current_timestamp,
        #         )
        #         if search_result:
        #             employee_id = search_result.employee_id
        #             staff_id = search_result.staff_id
        #             detection_type = search_result.detection_type
        #             staff_details = search_result.staff_details
        #             person_name = search_result.person_name
        #             similarity_score = search_result.similarity_score
        #     except Exception as e:
        #         self.logger.warning(f"Local embedding search fallback failed: {e}")

        # Update detection object directly (avoid relying on SearchResult type)
        detection = detection.copy()
        detection["person_id"] = staff_id
        detection["person_name"] = person_name or ""
        detection["recognition_status"] = "known" if staff_id else "unknown"
        detection["employee_id"] = employee_id
        detection["staff_details"] = staff_details if isinstance(staff_details, dict) else {}
        detection["similarity_score"] = float(similarity_score)
        detection["enrolled"] = bool(staff_id)
        # Display label policy: ALWAYS show identified faces immediately, only suppress "Unknown" during probation
        is_identified = (staff_id is not None and detection_type == "known")
        if is_identified:
            # Identified faces: show name immediately (no probation delay)
            detection["display_name"] = person_name
        else:
            # Unknown faces: only show "Unknown" label after probation period to avoid flicker
            show_unknown_label = (age_frames >= self._probation_frames)
            detection["display_name"] = "" if show_unknown_label else "" #TODO: Maybe replace this with "Unknown" bec probationif fail we show unknown.
        # Preserve original category (e.g., 'face') for tracking/counting

        # Update global tracking per unique internal track id to avoid double-counting within a frame
        # Determine unknown strictly by recognition_status (display label never affects counters)
        is_truly_unknown = (detection.get("recognition_status") == "unknown")

        try:
            internal_tid = detection.get("track_id")
        except Exception:
            internal_tid = None

        if not is_truly_unknown and detection_type == "known":
            # Mark recognized and ensure it is not counted as unknown anymore
            self._track_person(staff_id, camera_id=camera_id)
            with self._tracking_lock:
                if internal_tid is not None:
                    self._unknown_track_ids.discard(internal_tid)
                    self._recognized_track_ids.add(internal_tid)
        else:
            # Only count as unknown in session totals if probation has been exceeded and still unknown
            matured_unknown = (age_frames >= self._probation_frames)
            if matured_unknown:
                with self._tracking_lock:
                    if internal_tid is not None:
                        # If it later becomes recognized, we'll remove it from unknown set above
                        self._unknown_track_ids.add(internal_tid)

        # Enqueue detection for background logging with all required parameters
        try:
            # Log known faces for activity tracking (skip any employee_id starting with "unknown_")
            if (
                detection["recognition_status"] == "known"
                and self.people_activity_logging
                and config
                and getattr(config, 'enable_people_activity_logging', True)
                and employee_id
                and not str(employee_id).startswith("unknown_")
            ):
                st4=time.time()
                await self.people_activity_logging.enqueue_detection(
                    detection=detection,
                    current_frame=current_frame,
                    location=location,
                    camera_name=camera_name,
                    camera_id=camera_id,
                    rtp_number=rtp_number,
                )
                # print("------------------FACE RECOG ENQUEUEING DETECTION FOR ACTIVITY LOGGING----------------------------")
                # print("LATENCY:",(time.time() - st4)*1000,"| Throughput fps:",(1.0 / (time.time() - st4)) if (time.time() - st4) > 0 else None)
                # print("------------------FACE RECOG ENQUEUEING DETECTION FOR ACTIVITY LOGGING----------------------------")

                self.logger.debug(f"Enqueued known face detection for activity logging: {detection.get('person_name', 'Unknown')}")
        except Exception as e:
            self.logger.error(f"Error enqueueing detection for activity logging: {e}")
        # print("------------------PROCESS FACE LATENCY TOTAL----------------------------")
        #print("LATENCY:",(time.time() - st2)*1000,"| Throughput fps:",(1.0 / (time.time() - st2)) if (time.time() - st2) > 0 else None)
        # print("------------------PROCESS FACE LATENCY TOTAL----------------------------")

        return detection



    def _return_error_detection(
        self,
        detection: Dict,
        person_id: str,
        person_name: str,
        recognition_status: str,
        enrolled: bool,
        category: str,
        error: str,
    ) -> Dict:
        """Return error detection"""
        detection["person_id"] = person_id
        detection["person_name"] = person_name
        detection["recognition_status"] = recognition_status
        detection["enrolled"] = enrolled
        detection["category"] = category
        detection["error"] = error
        return detection

    def _track_person(self, person_id: str, camera_id: str = "") -> None:
        """Track person with camera ID and UTC timestamp"""
        if person_id not in self.person_tracking:
            self.person_tracking[person_id] = []

        # Add current detection with actual camera_id
        detection_record = {
            "camera_id": camera_id or "",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        self.person_tracking[person_id].append(detection_record)

    def get_person_tracking_summary(self) -> Dict:
        """Get summary of tracked persons with camera IDs and timestamps"""
        return dict(self.person_tracking)

    def get_unknown_faces_storage(self) -> Dict[str, bytes]:
        """Get stored unknown face images as bytes"""
        if self.people_activity_logging:
            return self.people_activity_logging.get_unknown_faces_storage()
        return {}

    def clear_unknown_faces_storage(self) -> None:
        """Clear stored unknown face images"""
        if self.people_activity_logging:
            self.people_activity_logging.clear_unknown_faces_storage()

    def _get_face_recognition_summary(self, current_recognized_count: int, current_unknown_count: int, recognized_persons: Dict) -> Dict:
        """Get face recognition summary for current frame"""
        recognition_rate = 0.0
        total_current = current_recognized_count + current_unknown_count
        if total_current > 0:
            recognition_rate = (current_recognized_count / total_current) * 100

        # Get thread-safe global totals
        with self._tracking_lock:
            total_recognized = len(self._recognized_track_ids)
            total_unknown = len(self._unknown_track_ids)

        return {
            "face_recognition_summary": {
                "current_frame": {
                    "recognized": current_recognized_count,
                    "unknown": current_unknown_count,
                    "total": total_current,
                    "recognized_persons": dict(recognized_persons),
                    "recognition_rate": round(recognition_rate, 1),
                },
                "session_totals": {
                    "total_recognized": total_recognized,
                    "total_unknown": total_unknown,
                    "total_processed": total_recognized + total_unknown,
                },
                "person_tracking": self.get_person_tracking_summary(),
            }
        }

    def _check_alerts(
        self, summary: dict, frame_number: Any, config: FaceRecognitionEmbeddingConfig
    ) -> List[Dict]:
        """
        Check if any alert thresholds are exceeded and return alert dicts.
        """

        def get_trend(data, lookback=900, threshold=0.6):
            window = data[-lookback:] if len(data) >= lookback else data
            if len(window) < 2:
                return True  # not enough data to determine trend
            increasing = 0
            total = 0
            for i in range(1, len(window)):
                if window[i] >= window[i - 1]:
                    increasing += 1
                total += 1
            ratio = increasing / total
            if ratio >= threshold:
                return True
            elif ratio <= (1 - threshold):
                return False

        frame_key = str(frame_number) if frame_number is not None else "current_frame"
        alerts = []
        total_detections = summary.get("total_count", 0)
        face_summary = summary.get("face_recognition_summary", {})
        current_unknown = face_summary.get("current_frame", {}).get("unknown", 0)

        if not config.alert_config:
            return alerts

        if (
            hasattr(config.alert_config, "count_thresholds")
            and config.alert_config.count_thresholds
        ):
            for category, threshold in config.alert_config.count_thresholds.items():
                if category == "unknown_faces" and current_unknown > threshold:
                    alerts.append(
                        {
                            "alert_type": (
                                getattr(config.alert_config, "alert_type", ["Default"])
                                if hasattr(config.alert_config, "alert_type")
                                else ["Default"]
                            ),
                            "alert_id": f"alert_unknown_faces_{frame_key}",
                            "incident_category": "unknown_face_detection",
                            "threshold_level": threshold,
                            "current_count": current_unknown,
                            "ascending": get_trend(
                                self._ascending_alert_list, lookback=900, threshold=0.8
                            ),
                            "settings": {
                                t: v
                                for t, v in zip(
                                    (
                                        getattr(
                                            config.alert_config,
                                            "alert_type",
                                            ["Default"],
                                        )
                                        if hasattr(config.alert_config, "alert_type")
                                        else ["Default"]
                                    ),
                                    (
                                        getattr(
                                            config.alert_config, "alert_value", ["JSON"]
                                        )
                                        if hasattr(config.alert_config, "alert_value")
                                        else ["JSON"]
                                    ),
                                )
                            },
                        }
                    )
                elif category == "all" and total_detections > threshold:
                    alerts.append(
                        {
                            "alert_type": (
                                getattr(config.alert_config, "alert_type", ["Default"])
                                if hasattr(config.alert_config, "alert_type")
                                else ["Default"]
                            ),
                            "alert_id": "alert_" + category + "_" + frame_key,
                            "incident_category": self.CASE_TYPE,
                            "threshold_level": threshold,
                            "ascending": get_trend(
                                self._ascending_alert_list, lookback=900, threshold=0.8
                            ),
                            "settings": {
                                t: v
                                for t, v in zip(
                                    (
                                        getattr(
                                            config.alert_config,
                                            "alert_type",
                                            ["Default"],
                                        )
                                        if hasattr(config.alert_config, "alert_type")
                                        else ["Default"]
                                    ),
                                    (
                                        getattr(
                                            config.alert_config, "alert_value", ["JSON"]
                                        )
                                        if hasattr(config.alert_config, "alert_value")
                                        else ["JSON"]
                                    ),
                                )
                            },
                        }
                    )

        return alerts

    def _generate_tracking_stats(
        self,
        counting_summary: Dict,
        alerts: List,
        config: FaceRecognitionEmbeddingConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
        current_frame_staff_details: Dict = None,
    ) -> List[Dict]:
        """Generate structured tracking stats matching eg.json format with face recognition data."""
        camera_info = self.get_camera_info_from_stream(stream_info)
        tracking_stats = []

        total_detections = counting_summary.get("total_count", 0)
        total_counts_dict = counting_summary.get("total_counts", {})
        cumulative_total = sum(total_counts_dict.values()) if total_counts_dict else 0
        per_category_count = counting_summary.get("per_category_count", {})
        face_summary = counting_summary.get("face_recognition_summary", {})

        current_timestamp = self._get_current_timestamp_str(
            stream_info, precision=False
        )
        start_timestamp = self._get_start_timestamp_str(stream_info, precision=False)

        # Create high precision timestamps for input_timestamp and reset_timestamp
        high_precision_start_timestamp = self._get_current_timestamp_str(
            stream_info, precision=True
        )
        high_precision_reset_timestamp = self._get_start_timestamp_str(
            stream_info, precision=True
        )

        # Build total_counts array - only "Recognized Faces" and "Unknown Faces"
        # Note: We exclude generic "face" category to avoid duplicate/confusing fields
        session_totals = face_summary.get("session_totals", {})
        total_counts = [
            {
                "category": "Recognized Faces",
                "count": session_totals.get("total_recognized", 0),
            },
            {
                "category": "Unknown Faces",
                "count": session_totals.get("total_unknown", 0),
            },
        ]

        # Build current_counts array - only "Recognized Faces" and "Unknown Faces"
        current_frame = face_summary.get("current_frame", {})
        current_counts = [
            {
                "category": "Recognized Faces",
                "count": current_frame.get("recognized", 0),
            },
            {
                "category": "Unknown Faces",
                "count": current_frame.get("unknown", 0),
            },
        ]

        # Get new track IDs count (requires tracker to be enabled)
        new_counts_dict = self.get_new_counts_this_frame()
        # current_new_counts: Only NEW objects that appeared for first time
        current_new_counts = [{"category": cat, "count": count} for cat, count in new_counts_dict.items()]

        # Prepare detections with face recognition info
        detections = []
        for detection in counting_summary.get("detections", []):
            bbox = detection.get("bounding_box", {})
            category = detection.get("display_name", "")

            detection_obj = self.create_detection_object(category, bbox)
            # Add face recognition specific fields
            detection_obj.update(
                {
                    "person_id": detection.get("person_id"),
                    # Use display_name for front-end label suppression policy
                    "person_name": detection.get("display_name", ""),
                    # Explicit label field for UI overlays
                    "label": detection.get("display_name", ""),
                    "recognition_status": detection.get(
                        "recognition_status", "unknown"
                    ),
                    "enrolled": detection.get("enrolled", False),
                }
            )
            detections.append(detection_obj)

        # Build alert_settings array in expected format
        alert_settings = []
        if config.alert_config and hasattr(config.alert_config, "alert_type"):
            alert_settings.append(
                {
                    "alert_type": (
                        getattr(config.alert_config, "alert_type", ["Default"])
                        if hasattr(config.alert_config, "alert_type")
                        else ["Default"]
                    ),
                    "incident_category": self.CASE_TYPE,
                    "threshold_level": (
                        config.alert_config.count_thresholds
                        if hasattr(config.alert_config, "count_thresholds")
                        else {}
                    ),
                    "ascending": True,
                    "settings": {
                        t: v
                        for t, v in zip(
                            (
                                getattr(config.alert_config, "alert_type", ["Default"])
                                if hasattr(config.alert_config, "alert_type")
                                else ["Default"]
                            ),
                            (
                                getattr(config.alert_config, "alert_value", ["JSON"])
                                if hasattr(config.alert_config, "alert_value")
                                else ["JSON"]
                            ),
                        )
                    },
                }
            )

    
        human_text_lines = [f"CURRENT FRAME @ {current_timestamp}:"]

        current_recognized = current_frame.get("recognized", 0)
        current_unknown = current_frame.get("unknown", 0)
        recognized_persons = current_frame.get("recognized_persons", {})
        total_current = current_recognized + current_unknown

        # Show staff names and IDs being recognized in current frame (with tabs)
        human_text_lines.append(f"\t- Current Total Faces: {total_current}")
        human_text_lines.append(f"\t- Current Recognized: {current_recognized}")
        
        if recognized_persons:
            for person_id in recognized_persons.keys():
                # Get actual staff name from current frame processing
                staff_name = (current_frame_staff_details or {}).get(
                    person_id, f"Staff {person_id}"
                )
                human_text_lines.append(f"\t\t- Name: {staff_name} (ID: {person_id})")
        human_text_lines.append(f"\t- Current Unknown: {current_unknown}")

        # Show current frame counts only (with tabs)
        human_text_lines.append("")
        # human_text_lines.append(f"TOTAL SINCE @ {start_timestamp}")
        # human_text_lines.append(f"\tTotal Faces: {cumulative_total}")
        # human_text_lines.append(f"\tRecognized: {face_summary.get('session_totals',{}).get('total_recognized', 0)}")  
        # human_text_lines.append(f"\tUnknown: {face_summary.get('session_totals',{}).get('total_unknown', 0)}")
        # Additional counts similar to compare_similarity HUD
        # try:
        #     human_text_lines.append(f"\tCurrent Faces (detections): {total_detections}")
        #     human_text_lines.append(f"\tTotal Unique Tracks: {cumulative_total}")
        # except Exception:
        #     pass

        human_text = "\n".join(human_text_lines)

        # if alerts:
        #     for alert in alerts:
        #         human_text_lines.append(
        #             f"Alerts: {alert.get('settings', {})} sent @ {current_timestamp}"
        #         )
        # else:
        #     human_text_lines.append("Alerts: None")

        # human_text = "\n".join(human_text_lines)
        reset_settings = [
            {"interval_type": "daily", "reset_time": {"value": 9, "time_unit": "hour"}}
        ]

        tracking_stat = self.create_tracking_stats(
            total_counts=total_counts,
            current_counts=current_counts,
            detections=detections,
            human_text=human_text,
            camera_info=camera_info,
            alerts=alerts,
            alert_settings=alert_settings,
            reset_settings=reset_settings,
            start_time=high_precision_start_timestamp,
            reset_time=high_precision_reset_timestamp,
        )
        tracking_stat['target_categories'] = ['Recognized Faces', 'Unknown Faces']
        # current_new_counts: NEW track IDs that appeared for first time in this frame/aggregation
        tracking_stat['current_new_counts'] = current_new_counts
        tracking_stats.append(tracking_stat)
        return tracking_stats

    # Copy all other methods from face_recognition.py but add face recognition info to human text
    def _generate_incidents(
        self,
        counting_summary: Dict,
        alerts: List,
        config: FaceRecognitionEmbeddingConfig,
        frame_number: Optional[int] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> List[Dict]:
        """Generate structured incidents for the output format with frame-based keys."""

        incidents = []
        total_detections = counting_summary.get("total_count", 0)
        face_summary = counting_summary.get("face_recognition_summary", {})
        current_frame = face_summary.get("current_frame", {})

        current_timestamp = self._get_current_timestamp_str(stream_info)
        camera_info = self.get_camera_info_from_stream(stream_info)

        self._ascending_alert_list = (
            self._ascending_alert_list[-900:]
            if len(self._ascending_alert_list) > 900
            else self._ascending_alert_list
        )

        if total_detections > 0:
            # Determine event level based on unknown faces ratio
            level = "low"
            intensity = 5.0
            start_timestamp = self._get_start_timestamp_str(stream_info)
            if start_timestamp and self.current_incident_end_timestamp == "N/A":
                self.current_incident_end_timestamp = "Incident still active"
            elif (
                start_timestamp
                and self.current_incident_end_timestamp == "Incident still active"
            ):
                if (
                    len(self._ascending_alert_list) >= 15
                    and sum(self._ascending_alert_list[-15:]) / 15 < 1.5
                ):
                    self.current_incident_end_timestamp = current_timestamp
            elif (
                self.current_incident_end_timestamp != "Incident still active"
                and self.current_incident_end_timestamp != "N/A"
            ):
                self.current_incident_end_timestamp = "N/A"

            # Base intensity on unknown faces
            current_unknown = current_frame.get("unknown", 0)
            unknown_ratio = (
                current_unknown / total_detections if total_detections > 0 else 0
            )
            intensity = min(10.0, unknown_ratio * 10 + (current_unknown / 3))

            if intensity >= 9:
                level = "critical"
                self._ascending_alert_list.append(3)
            elif intensity >= 7:
                level = "significant"
                self._ascending_alert_list.append(2)
            elif intensity >= 5:
                level = "medium"
                self._ascending_alert_list.append(1)
            else:
                level = "low"
                self._ascending_alert_list.append(0)

            # Generate human text in new format with face recognition info
            current_recognized = current_frame.get("recognized", 0)
            human_text_lines = [f"FACE RECOGNITION INCIDENTS @ {current_timestamp}:"]
            human_text_lines.append(f"\tSeverity Level: {(self.CASE_TYPE,level)}")
            human_text_lines.append(f"\tRecognized Faces: {current_recognized}")
            human_text_lines.append(f"\tUnknown Faces: {current_unknown}")
            human_text_lines.append(f"\tTotal Faces: {total_detections}")
            human_text = "\n".join(human_text_lines)

            alert_settings = []
            if config.alert_config and hasattr(config.alert_config, "alert_type"):
                alert_settings.append(
                    {
                        "alert_type": (
                            getattr(config.alert_config, "alert_type", ["Default"])
                            if hasattr(config.alert_config, "alert_type")
                            else ["Default"]
                        ),
                        "incident_category": self.CASE_TYPE,
                        "threshold_level": (
                            config.alert_config.count_thresholds
                            if hasattr(config.alert_config, "count_thresholds")
                            else {}
                        ),
                        "ascending": True,
                        "settings": {
                            t: v
                            for t, v in zip(
                                (
                                    getattr(
                                        config.alert_config, "alert_type", ["Default"]
                                    )
                                    if hasattr(config.alert_config, "alert_type")
                                    else ["Default"]
                                ),
                                (
                                    getattr(
                                        config.alert_config, "alert_value", ["JSON"]
                                    )
                                    if hasattr(config.alert_config, "alert_value")
                                    else ["JSON"]
                                ),
                            )
                        },
                    }
                )

            event = self.create_incident(
                incident_id=self.CASE_TYPE + "_" + str(frame_number),
                incident_type=self.CASE_TYPE,
                severity_level=level,
                human_text=human_text,
                camera_info=camera_info,
                alerts=alerts,
                alert_settings=alert_settings,
                start_time=start_timestamp,
                end_time=self.current_incident_end_timestamp,
                level_settings={"low": 1, "medium": 3, "significant": 4, "critical": 7},
            )
            incidents.append(event)

        else:
            self._ascending_alert_list.append(0)
            incidents.append({})

        return incidents

    def _generate_business_analytics(
        self,
        counting_summary: Dict,
        alerts: Any,
        config: FaceRecognitionEmbeddingConfig,
        stream_info: Optional[Dict[str, Any]] = None,
        is_empty=False,
    ) -> List[Dict]:
        """Generate standardized business analytics for the agg_summary structure."""
        if is_empty:
            return []
        return []

    def _generate_summary(self, incidents: List, tracking_stats: List, business_analytics: List) -> List[str]:
        """
        Generate a human_text string for the tracking_stat, incident, business analytics and alerts.
        """
        lines = []
        lines.append("Application Name: "+self.CASE_TYPE)
        lines.append("Application Version: "+self.CASE_VERSION)
        if len(incidents) > 0:
            lines.append("Incidents: "+f"\n\t{incidents[0].get('human_text', 'No incidents detected')}")
        if len(tracking_stats) > 0:
            lines.append("Tracking Statistics: "+f"\t{tracking_stats[0].get('human_text', 'No tracking statistics detected')}")
        if len(business_analytics) > 0:
            lines.append("Business Analytics: "+f"\t{business_analytics[0].get('human_text', 'No business analytics detected')}")

        if len(incidents) == 0 and len(tracking_stats) == 0 and len(business_analytics) == 0:
            lines.append("Summary: "+"No Summary Data")

        return ["\n".join(lines)]

    # Include all the standard helper methods from face_recognition.py...
    def _count_categories(
        self, detections: list, config: FaceRecognitionEmbeddingConfig
    ) -> dict:
        """
        Count the number of detections per category and return a summary dict.
        The detections list is expected to have 'track_id' (from tracker), 'category', 'bounding_box', etc.
        Output structure will include 'track_id' for each detection as per AdvancedTracker output.
        """
        counts = {}
        for det in detections:
            cat = det.get("category", "unknown")
            counts[cat] = counts.get(cat, 0) + 1
        # Each detection dict will now include 'track_id' and face recognition fields
        return {
            "total_count": sum(counts.values()),
            "per_category_count": counts,
            "detections": [
                {
                    "bounding_box": det.get("bounding_box"),
                    "category": det.get("category"),
                    "confidence": det.get("confidence"),
                    "track_id": det.get("track_id"),
                    "frame_id": det.get("frame_id"),
                    # Face recognition fields
                    "person_id": det.get("person_id"),
                    "person_name": det.get("person_name"),
                    "label": det.get("display_name", ""),
                    "recognition_status": det.get("recognition_status"),
                    "enrolled": det.get("enrolled"),
                    "embedding": det.get("embedding", []),
                    "landmarks": det.get("landmarks"),
                    "staff_details": det.get(
                        "staff_details"
                    ),  # Full staff information from API
                }
                for det in detections
            ],
        }

    # Removed unused _extract_predictions (counts and outputs are built elsewhere)

    # Copy all standard tracking, IoU, timestamp methods from face_recognition.py
    def _update_tracking_state(self, detections: list):
        """Track unique categories track_ids per category for total count after tracking.
        Computes which track IDs are NEW (appeared for first time this frame).
        """
        if not hasattr(self, "_per_category_total_track_ids"):
            self._per_category_total_track_ids = {
                cat: set() for cat in self.target_categories
            }
        if not hasattr(self, "_previous_frame_track_ids"):
            self._previous_frame_track_ids = {cat: set() for cat in self.target_categories}
        self._current_frame_track_ids = {cat: set() for cat in self.target_categories}

        for det in detections:
            cat = det.get("category")
            raw_track_id = det.get("track_id")
            if cat not in self.target_categories or raw_track_id is None:
                continue
            bbox = det.get("bounding_box", det.get("bbox"))
            canonical_id = self._merge_or_register_track(raw_track_id, bbox)
            det["track_id"] = canonical_id

            self._per_category_total_track_ids.setdefault(cat, set()).add(canonical_id)
            self._current_frame_track_ids[cat].add(canonical_id)

        # NEW track IDs = present in current frame but NOT in previous frame
        self._new_track_ids_this_frame = {
            cat: (self._current_frame_track_ids.get(cat, set()) - self._previous_frame_track_ids.get(cat, set()))
            for cat in self.target_categories
        }

        # Snapshot current -> previous for next call
        self._previous_frame_track_ids = {cat: set(ids) for cat, ids in self._current_frame_track_ids.items()}

    def get_total_counts(self):
        """Return total unique track_id count for each category."""
        return {
            cat: len(ids)
            for cat, ids in getattr(self, "_per_category_total_track_ids", {}).items()
        }

    def get_new_counts_this_frame(self) -> Dict[str, int]:
        """Get count of NEW track IDs that appeared in this frame vs the previous one."""
        return {cat: len(ids) for cat, ids in getattr(self, '_new_track_ids_this_frame', {}).items()}

    def get_current_frame_counts(self) -> Dict[str, int]:
        """Get count of ALL track IDs currently in this frame (existing + new)."""
        return {cat: len(ids) for cat, ids in getattr(self, '_current_frame_track_ids', {}).items()}

    def _format_timestamp_for_stream(self, timestamp: float) -> str:
        """Format timestamp for streams (YYYY:MM:DD HH:MM:SS format)."""
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        return dt.strftime("%Y:%m:%d %H:%M:%S")

    def _format_timestamp_for_video(self, timestamp: float) -> str:
        """Format timestamp for video chunks (HH:MM:SS.ms format)."""
        hours = int(timestamp // 3600)
        minutes = int((timestamp % 3600) // 60)
        seconds = round(float(timestamp % 60), 2)
        return f"{hours:02d}:{minutes:02d}:{seconds:.1f}"

    def _format_timestamp(self, timestamp: Any) -> str:
        """Format a timestamp to match the current timestamp format: YYYY:MM:DD HH:MM:SS.

        The input can be either:
        1. A numeric Unix timestamp (``float`` / ``int``) – it will be converted to datetime.
        2. A string in the format ``YYYY-MM-DD-HH:MM:SS.ffffff UTC``.

        The returned value will be in the format: YYYY:MM:DD HH:MM:SS (no milliseconds, no UTC suffix).

        Example
        -------
        >>> self._format_timestamp("2025-10-27-19:31:20.187574 UTC")
        '2025:10:27 19:31:20'
        """

        # Convert numeric timestamps to datetime first
        if isinstance(timestamp, (int, float)):
            dt = datetime.fromtimestamp(timestamp, timezone.utc)
            return dt.strftime('%Y:%m:%d %H:%M:%S')

        # Ensure we are working with a string from here on
        if not isinstance(timestamp, str):
            return str(timestamp)

        # Remove ' UTC' suffix if present
        timestamp_clean = timestamp.replace(' UTC', '').strip()

        # Remove milliseconds if present (everything after the last dot)
        if '.' in timestamp_clean:
            timestamp_clean = timestamp_clean.split('.')[0]

        # Parse the timestamp string and convert to desired format
        try:
            # Handle format: YYYY-MM-DD-HH:MM:SS
            if timestamp_clean.count('-') >= 2:
                # Replace first two dashes with colons for date part, third with space
                parts = timestamp_clean.split('-')
                if len(parts) >= 4:
                    # parts = ['2025', '10', '27', '19:31:20']
                    formatted = f"{parts[0]}:{parts[1]}:{parts[2]} {'-'.join(parts[3:])}"
                    return formatted
        except Exception:
            pass

        # If parsing fails, return the cleaned string as-is
        return timestamp_clean

    def _get_current_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False, frame_id: Optional[str]=None) -> str:
        """Get formatted current timestamp based on stream type."""
        
        if not stream_info:
            return "00:00:00.00"
        if precision:
            if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
                if frame_id:
                    start_time = int(frame_id)/stream_info.get("input_settings", {}).get("original_fps", 30)
                else:
                    start_time = stream_info.get("input_settings", {}).get("start_frame", 30)/stream_info.get("input_settings", {}).get("original_fps", 30)
                stream_time_str = self._format_timestamp_for_video(start_time)
                
                return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
            else:
                return datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")

        if stream_info.get("input_settings", {}).get("start_frame", "na") != "na":
            if frame_id:
                start_time = int(frame_id)/stream_info.get("input_settings", {}).get("original_fps", 30)
            else:
                start_time = stream_info.get("input_settings", {}).get("start_frame", 30)/stream_info.get("input_settings", {}).get("original_fps", 30)

            stream_time_str = self._format_timestamp_for_video(start_time)
           

            return self._format_timestamp(stream_info.get("input_settings", {}).get("stream_time", "NA"))
        else:
            stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
            if stream_time_str:
                try:
                    timestamp_str = stream_time_str.replace(" UTC", "")
                    dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                    timestamp = dt.replace(tzinfo=timezone.utc).timestamp()
                    return self._format_timestamp_for_stream(timestamp)
                except:
                    return self._format_timestamp_for_stream(time.time())
            else:
                return self._format_timestamp_for_stream(time.time())

    def _get_start_timestamp_str(self, stream_info: Optional[Dict[str, Any]], precision=False) -> str:
        """Get formatted start timestamp for 'TOTAL SINCE' based on stream type."""
        if not stream_info:
            return "00:00:00"
        
        if precision:
            if self.start_timer is None:
                candidate = stream_info.get("input_settings", {}).get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
                return self._format_timestamp(self.start_timer)
            elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
                candidate = stream_info.get("input_settings", {}).get("stream_time")
                if not candidate or candidate == "NA":
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                self.start_timer = candidate
                return self._format_timestamp(self.start_timer)
            else:
                return self._format_timestamp(self.start_timer)

        if self.start_timer is None:
            # Prefer direct input_settings.stream_time if available and not NA
            candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
                # Fallback to nested stream_info.stream_time used by current timestamp path
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(self._tracking_start_time, timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                    except:
                        candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                else:
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
            return self._format_timestamp(self.start_timer)
        elif stream_info.get("input_settings", {}).get("start_frame", "na") == 1:
            candidate = stream_info.get("input_settings", {}).get("stream_time")
            if not candidate or candidate == "NA":
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        ts = dt.replace(tzinfo=timezone.utc).timestamp()
                        candidate = datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                    except:
                        candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
                else:
                    candidate = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H:%M:%S.%f UTC")
            self.start_timer = candidate
            return self._format_timestamp(self.start_timer)
        
        else:
            if self.start_timer is not None and self.start_timer != "NA":
                return self._format_timestamp(self.start_timer)

            if self._tracking_start_time is None:
                stream_time_str = stream_info.get("input_settings", {}).get("stream_info", {}).get("stream_time", "")
                if stream_time_str:
                    try:
                        timestamp_str = stream_time_str.replace(" UTC", "")
                        dt = datetime.strptime(timestamp_str, "%Y-%m-%d-%H:%M:%S.%f")
                        self._tracking_start_time = dt.replace(tzinfo=timezone.utc).timestamp()
                    except:
                        self._tracking_start_time = time.time()
                else:
                    self._tracking_start_time = time.time()

            dt = datetime.fromtimestamp(self._tracking_start_time, tz=timezone.utc)
            dt = dt.replace(minute=0, second=0, microsecond=0)
            return dt.strftime('%Y:%m:%d %H:%M:%S')

    
    def _compute_iou(self, box1: Any, box2: Any) -> float:
        """Compute IoU between two bounding boxes which may be dicts or lists."""

        def _bbox_to_list(bbox):
            if bbox is None:
                return []
            if isinstance(bbox, list):
                return bbox[:4] if len(bbox) >= 4 else []
            if isinstance(bbox, dict):
                if "xmin" in bbox:
                    return [bbox["xmin"], bbox["ymin"], bbox["xmax"], bbox["ymax"]]
                if "x1" in bbox:
                    return [bbox["x1"], bbox["y1"], bbox["x2"], bbox["y2"]]
                values = [v for v in bbox.values() if isinstance(v, (int, float))]
                return values[:4] if len(values) >= 4 else []
            return []

        l1 = _bbox_to_list(box1)
        l2 = _bbox_to_list(box2)
        if len(l1) < 4 or len(l2) < 4:
            return 0.0
        x1_min, y1_min, x1_max, y1_max = l1
        x2_min, y2_min, x2_max, y2_max = l2

        x1_min, x1_max = min(x1_min, x1_max), max(x1_min, x1_max)
        y1_min, y1_max = min(y1_min, y1_max), max(y1_min, y1_max)
        x2_min, x2_max = min(x2_min, x2_max), max(x2_min, x2_max)
        y2_min, y2_max = min(y2_min, y2_max), max(y2_min, y2_max)

        inter_x_min = max(x1_min, x2_min)
        inter_y_min = max(y1_min, y2_min)
        inter_x_max = min(x1_max, x2_max)
        inter_y_max = min(y1_max, y2_max)

        inter_w = max(0.0, inter_x_max - inter_x_min)
        inter_h = max(0.0, inter_y_max - inter_y_min)
        inter_area = inter_w * inter_h

        area1 = (x1_max - x1_min) * (y1_max - y1_min)
        area2 = (x2_max - x2_min) * (y2_max - y2_min)
        union_area = area1 + area2 - inter_area

        return (inter_area / union_area) if union_area > 0 else 0.0

    def _merge_or_register_track(self, raw_id: Any, bbox: Any) -> Any:
        """Return a stable canonical ID for a raw tracker ID."""
        if raw_id is None or bbox is None:
            return raw_id

        now = time.time()

        if raw_id in self._track_aliases:
            canonical_id = self._track_aliases[raw_id]
            track_info = self._canonical_tracks.get(canonical_id)
            if track_info is not None:
                track_info["last_bbox"] = bbox
                track_info["last_update"] = now
                track_info["raw_ids"].add(raw_id)
            return canonical_id

        for canonical_id, info in self._canonical_tracks.items():
            if now - info["last_update"] > self._track_merge_time_window:
                continue
            iou = self._compute_iou(bbox, info["last_bbox"])
            if iou >= self._track_merge_iou_threshold:
                self._track_aliases[raw_id] = canonical_id
                info["last_bbox"] = bbox
                info["last_update"] = now
                info["raw_ids"].add(raw_id)
                return canonical_id

        canonical_id = raw_id
        self._track_aliases[raw_id] = canonical_id
        self._canonical_tracks[canonical_id] = {
            "last_bbox": bbox,
            "last_update": now,
            "raw_ids": {raw_id},
        }
        return canonical_id

    def __del__(self):
        """Cleanup when object is destroyed"""
        try:
            if hasattr(self, "people_activity_logging") and self.people_activity_logging:
                self.people_activity_logging.stop_background_processing()
        except:
            pass
        
        try:
            if hasattr(self, "embedding_manager") and self.embedding_manager:
                self.embedding_manager.stop_background_refresh()
        except:
            pass