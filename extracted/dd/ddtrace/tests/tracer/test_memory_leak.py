"""
Variety of test cases ensuring that ddtrace does not leak memory.
"""

from weakref import WeakValueDictionary

import pytest

from ddtrace.trace import Span
from ddtrace.trace import Tracer
from tests.utils import DummyTracer


@pytest.fixture
def tracer() -> DummyTracer:
    return DummyTracer()


def trace(weakdict: WeakValueDictionary, tracer: Tracer, *args, **kwargs) -> Span:
    """Return a span created from ``tracer`` and add it to the given weak
    dictionary.

    Note: ensure to delete the returned reference from this function to ensure
    no additional references are kept to the span.
    """
    s = tracer.trace(*args, **kwargs)
    weakdict[s.span_id] = s
    return s


@pytest.mark.subprocess
def test_leak():
    import gc
    from weakref import WeakValueDictionary

    from ddtrace.trace import tracer
    from tests.tracer.test_memory_leak import trace

    wd = WeakValueDictionary()
    with trace(wd, tracer, "span1") as span:
        with trace(wd, tracer, "span2") as span2:
            pass
    assert len(wd) == 2

    # The spans are still open and referenced so they should not be gc'd
    gc.collect()
    assert len(wd) == 2
    tracer.flush()
    del span, span2
    gc.collect()
    assert len(wd) == 0


@pytest.mark.subprocess
def test_single_thread_single_trace():
    """
    Ensure a simple trace doesn't leak span objects.
    """
    import gc
    from weakref import WeakValueDictionary

    from ddtrace.trace import tracer
    from tests.tracer.test_memory_leak import trace

    wd = WeakValueDictionary()
    with trace(wd, tracer, "span1"):
        with trace(wd, tracer, "span2"):
            pass

    # Spans are serialized and unreferenced when traces are finished
    # so gc-ing right away should delete all span objects.
    gc.collect()
    assert len(wd) == 0


@pytest.mark.subprocess
def test_single_thread_multi_trace():
    """
    Ensure a trace in a thread is properly garbage collected.
    """
    import gc
    from weakref import WeakValueDictionary

    from ddtrace.trace import tracer
    from tests.tracer.test_memory_leak import trace

    wd = WeakValueDictionary()
    for _ in range(1000):
        with trace(wd, tracer, "span1"):
            with trace(wd, tracer, "span2"):
                pass
            with trace(wd, tracer, "span3"):
                pass
    tracer.flush()
    # Once these references are deleted then the spans should no longer be
    # referenced by anything and should be gc'd.
    gc.collect()
    assert len(wd) == 0


@pytest.mark.subprocess
def test_multithread_trace():
    """
    Ensure a trace that crosses thread boundaries is properly garbage collected.
    """
    import gc
    from threading import Thread
    from weakref import WeakValueDictionary

    from ddtrace.trace import tracer
    from tests.tracer.test_memory_leak import trace

    wd = WeakValueDictionary()
    state = []

    def _target(ctx):
        tracer.context_provider.activate(ctx)
        with trace(wd, tracer, "thread"):
            assert len(wd) == 2
        state.append(1)

    with trace(wd, tracer, "") as span:
        t = Thread(target=_target, args=(span.context,))
        t.start()
        t.join()
        # Ensure thread finished successfully
        assert state == [1]

    tracer.flush()
    del span
    gc.collect()
    assert len(wd) == 0


@pytest.mark.subprocess(err=None)
def test_fork_open_span():
    """
    When a fork occurs with an open span then the child process should not have
    a strong reference to the span because it might never be closed.
    """
    import ddtrace.auto  # noqa

    import gc
    import os
    from weakref import WeakValueDictionary

    from ddtrace.trace import tracer
    from tests.tracer.test_memory_leak import trace

    wd = WeakValueDictionary()
    span = trace(wd, tracer, "span")
    pid = os.fork()

    if pid == 0:
        assert len(wd) == 1
        gc.collect()
        # span is still open and in the context
        assert len(wd) == 1
        span2 = trace(wd, tracer, "span2")
        assert span2._parent is None
        assert len(wd) == 2
        span2.finish()

        del span2
        # Expect there to be one span left (the original from before the fork)
        # which is inherited into the child process but will never be closed.
        # The important thing in this test case is all new spans created in the
        # child will be gc'd.
        gc.collect()
        assert len(wd) == 1

        # Normally, if the child process leaves this function frame the span
        # reference would be lost and it would be free to be gc'd. We delete
        # the reference explicitly here to mimic this scenario.
        del span
        gc.collect()
        assert len(wd) == 0
        os._exit(12)

    assert len(wd) == 1
    span.finish()
    del span
    gc.collect()
    assert len(wd) == 0

    _, status = os.waitpid(pid, 0)
    exit_code = os.WEXITSTATUS(status)
    assert exit_code == 12
