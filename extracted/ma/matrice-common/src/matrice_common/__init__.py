"""Module providing __init__ functionality."""

import multiprocessing

# Only run dependency checks in the main process, NOT in spawned child processes.
# Child processes re-import modules which would trigger pip install commands,
# causing race conditions and BrokenProcessPool errors with file corruption.
_is_main_process = multiprocessing.parent_process() is None

if _is_main_process:
    from .utils import dependencies_check

    dependencies_check(
        [
            "requests",
            "Pillow",
            "python-dateutil",
            "redis",
            "aioredis",
            "confluent-kafka",
            "aiokafka",
            "imagehash",
            "kafka-python",
            "sentry-sdk",
            "msgpack"
        ]
    )
