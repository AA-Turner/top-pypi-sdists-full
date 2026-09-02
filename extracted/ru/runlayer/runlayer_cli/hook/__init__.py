"""aiwatch-hook — Python port of runlayer-hook.sh."""

# Kept here (not in ``relay.py``) so ``main.py`` / ``aiwatch.py`` can read the
# argv[1] sentinel without importing the heavy ``relay`` module on the hot path.
TRANSCRIPT_STREAM_WORKER_SENTINEL = "__transcript_stream_worker__"
