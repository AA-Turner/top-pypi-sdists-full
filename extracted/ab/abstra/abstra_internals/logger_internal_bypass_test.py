"""Internal framework logs must bypass the patched sys.stderr so they are never
captured into an execution's logs by StdioPatcher."""

from abstra_internals.logger import (
    AbstraLogger,
    _DirectStderrStream,
    internal_logger,
)


def test_internal_logger_does_not_propagate_and_uses_direct_stderr():
    AbstraLogger.init("local")
    il = internal_logger()
    # Not propagating means abstra_internal records never reach the root handler
    # (whose sys.stderr.write is patched during executions).
    assert il.propagate is False
    streams = [getattr(h, "stream", None) for h in il.handlers]
    assert any(isinstance(s, _DirectStderrStream) for s in streams)


def test_init_is_idempotent_no_duplicate_handlers():
    AbstraLogger.init("local")
    AbstraLogger.init("local")
    il = internal_logger()
    direct = [
        h
        for h in il.handlers
        if isinstance(getattr(h, "stream", None), _DirectStderrStream)
    ]
    assert len(direct) == 1


def test_direct_stderr_write_never_raises():
    stream = _DirectStderrStream()
    # writes to fd 2 and returns an int; must not raise even on odd input
    assert isinstance(stream.write("ok\n"), int)
    stream.flush()
