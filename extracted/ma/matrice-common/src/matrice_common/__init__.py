"""Matrice common utilities: session, RPC, streaming, and optimization."""

import multiprocessing

# Only run dependency checks in the main process, NOT in spawned child processes.
# Child processes re-import modules which would trigger pip install commands,
# causing race conditions and BrokenProcessPool errors with file corruption.
_is_main_process = multiprocessing.parent_process() is None

if _is_main_process:
    from .utils import dependencies_check

    dependencies_check(
        [
            "httpx",  # imported at module load by matrice_common.rpc; must be installed pre-import
            "requests",
            "python-dateutil",
            "redis",
            "confluent-kafka",
            "aiokafka",
            "kafka-python",
            # Pruned: Pillow, aioredis, imagehash, msgpack, dotenv — none are
            # imported anywhere in src/ (aioredis is also deprecated on py>=3.11;
            # the async code uses redis.asyncio). Do not re-add without a real
            # import.
        ]
    )
