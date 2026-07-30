"""Matrice common utilities: session, RPC, streaming, and optimization."""

import multiprocessing
import os

# Only run dependency checks in the main process, NOT in spawned child processes.
# Child processes re-import modules which would trigger pip install commands,
# causing race conditions and BrokenProcessPool errors with file corruption.
_is_main_process = multiprocessing.parent_process() is None

if _is_main_process:
    # Allow the runtime dependency self-heal by DEFAULT in the main process
    # (opt-OUT via MATRICE_ALLOW_RUNTIME_PIP=0). The child-process guard above
    # keeps this off the fork/spawn hot path, so it can't race on pip. We do NOT
    # declare these as hard `dependencies` in pyproject — the Docker image / env
    # ships them, and forcing a version there breaks on system (Debian) packages
    # pip cannot uninstall. Instead each is `suggested`: install-only-if-missing
    # at an org-APPROVED_DEPS version (legal + a fallback for standalone/fresh
    # venvs), never overriding whatever the image already provides.
    os.environ.setdefault("MATRICE_ALLOW_RUNTIME_PIP", "1")

    from .utils import dependencies_check

    try:
        dependencies_check(
            [
                # imported at matrice_common module load (rpc -> httpx,
                # token_auth -> dateutil); the rest are lazy stream clients.
                {"name": "httpx", "suggested": "0.28.1"},
                {"name": "requests", "suggested": "2.33.1"},
                {"name": "python-dateutil", "suggested": "2.9.0.post0"},
                {"name": "kafka-python", "suggested": "2.3.1"},
                # Stream clients: image/env ships current versions; suggest none
                # (install latest only if entirely absent — standalone fallback).
                "redis",
                "confluent-kafka",
                "aiokafka",
                # Pruned: Pillow, aioredis, imagehash, msgpack, dotenv — none are
                # imported anywhere in src/ (aioredis is also deprecated on
                # py>=3.11; the async code uses redis.asyncio).
            ]
        )
    except Exception:  # noqa: BLE001 - never let dep self-heal crash the import
        pass
