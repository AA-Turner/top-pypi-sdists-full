"""Unit tests for the Option A async-SQL queuing proxy: the registry completion signal
(``_MaterializationRegistry.settle`` / ``wait_until_ready`` / ``get_result``) and the
``PendingDataFrame`` blocking proxy."""

import threading
import time
import unittest

import pandas as pd

from sagemaker_studio.utils.pending_dataframe import PendingDataFrame
from sagemaker_studio.utils.sqlutils_async import (
    _AsyncMaterializationFailed,
    _AsyncMaterializationSuperseded,
    _MaterializationRegistry,
)


class RegistryCompletionSignalTest(unittest.TestCase):
    def setUp(self):
        self.reg = _MaterializationRegistry()

    def test_settle_success_then_get_result(self):
        gen, _cancel = self.reg.start("df")
        df = pd.DataFrame({"a": [1, 2]})
        self.reg.settle("df", gen, result=df)
        self.assertTrue(self.reg.wait_until_ready("df", gen, timeout=1))
        self.assertIs(self.reg.get_result("df", gen), df)

    def test_settle_error_is_raised_by_get_result(self):
        gen, _cancel = self.reg.start("df")
        err = _AsyncMaterializationFailed("df")
        self.reg.settle("df", gen, error=err)
        self.assertTrue(self.reg.wait_until_ready("df", gen, timeout=1))
        with self.assertRaises(_AsyncMaterializationFailed):
            self.reg.get_result("df", gen)

    def test_wait_times_out_when_not_settled(self):
        gen, _cancel = self.reg.start("df")
        start = time.monotonic()
        self.assertFalse(self.reg.wait_until_ready("df", gen, timeout=0.05))
        self.assertLess(time.monotonic() - start, 1.0)

    def test_progress_resets_stall_patience(self):
        # Stall-based wait (finding C): a run that keeps making progress is NOT timed out,
        # even past the stall window, because note_progress resets patience. Here the stall
        # window is 0.15s but a background bumper calls note_progress every 0.03s for ~0.4s
        # (well past the window) then settles -- the wait must return True (settled), not
        # False (stalled).
        import threading as _th

        gen, _cancel = self.reg.start("df")

        def bumper():
            for _ in range(12):
                time.sleep(0.03)
                self.reg.note_progress("df", gen)
            self.reg.settle("df", gen, result=pd.DataFrame({"a": [1]}))

        t = _th.Thread(target=bumper, daemon=True)
        t.start()
        # Stall window 0.15s < the 0.4s total run, but progress keeps resetting it.
        self.assertTrue(self.reg.wait_until_ready("df", gen, timeout=0.15))
        t.join(2)

    def test_wait_times_out_when_progress_stalls(self):
        # The complement: a run that makes NO progress for the stall window times out, even
        # though it was started (armed) -- this is the hung-run case the bound exists for.
        gen, _cancel = self.reg.start("df")
        # note_progress once, then go silent well past the stall window.
        self.reg.note_progress("df", gen)
        start = time.monotonic()
        self.assertFalse(self.reg.wait_until_ready("df", gen, timeout=0.1))
        self.assertLess(time.monotonic() - start, 2.0)

    def test_wait_bounded_when_progress_record_missing(self):
        # Backstop: if the _progress record is absent (e.g. the run was reaped mid-wait) and
        # the Event is never set, the wait must still time out at the absolute deadline
        # rather than poll forever. Arm the generation, drop its _progress record, and leave
        # the Event unset -> wait_until_ready must return False within a bounded time.
        gen, _cancel = self.reg.start("df")
        with self.reg._lock:
            self.reg._progress.pop(("df", gen), None)  # simulate a missing progress record
        start = time.monotonic()
        self.assertFalse(self.reg.wait_until_ready("df", gen, timeout=0.1))
        self.assertLess(time.monotonic() - start, 2.0)

    def test_settle_is_idempotent_first_outcome_wins(self):
        gen, _cancel = self.reg.start("df")
        first = pd.DataFrame({"a": [1]})
        self.reg.settle("df", gen, result=first)
        # A second (later) terminal path must not overwrite the first outcome.
        self.reg.settle("df", gen, error=_AsyncMaterializationFailed("df"))
        self.assertIs(self.reg.get_result("df", gen), first)

    def test_new_generation_has_independent_signal(self):
        gen1, _ = self.reg.start("df")
        self.reg.settle("df", gen1, result=pd.DataFrame({"a": [1]}))
        gen2, _ = self.reg.start("df")  # supersede: new generation, fresh unset signal
        self.assertNotEqual(gen1, gen2)
        # gen2 is not settled yet.
        self.assertFalse(self.reg.wait_until_ready("df", gen2, timeout=0.05))
        # gen1's already-settled result is still readable (kept until reaped/reused).
        self.assertTrue(self.reg.wait_until_ready("df", gen1, timeout=0.05))

    def test_wait_returns_true_for_unarmed_generation(self):
        # A generation that was never armed returns True immediately; get_result then
        # decides. This is the defensive "already reaped / never existed" path.
        self.assertTrue(self.reg.wait_until_ready("never", 99, timeout=0.05))
        with self.assertRaises(KeyError):
            self.reg.get_result("never", 99)

    def test_cross_thread_wait_then_settle(self):
        gen, _cancel = self.reg.start("df")
        df = pd.DataFrame({"a": [1, 2, 3]})

        def _settle_later():
            time.sleep(0.05)
            self.reg.settle("df", gen, result=df)

        t = threading.Thread(target=_settle_later)
        t.start()
        self.assertTrue(self.reg.wait_until_ready("df", gen, timeout=2))
        self.assertIs(self.reg.get_result("df", gen), df)
        t.join()


class PendingDataFrameTest(unittest.TestCase):
    def setUp(self):
        self.reg = _MaterializationRegistry()

    def _proxy(self, name="df", timeout=2):
        gen, _cancel = self.reg.start(name)
        return PendingDataFrame(name, gen, self.reg, timeout=timeout), gen

    def test_resolve_returns_real_frame(self):
        proxy, gen = self._proxy()
        df = pd.DataFrame({"a": [1, 2]})
        self.reg.settle("df", gen, result=df)
        self.assertIs(proxy._resolve(), df)

    def test_attribute_access_forwards(self):
        proxy, gen = self._proxy()
        df = pd.DataFrame({"a": [1, 2, 3]})
        self.reg.settle("df", gen, result=df)
        self.assertEqual(list(proxy.columns), ["a"])
        self.assertEqual(proxy.shape, (3, 1))

    def test_len_and_getitem_and_iter_forward(self):
        proxy, gen = self._proxy()
        df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
        self.reg.settle("df", gen, result=df)
        self.assertEqual(len(proxy), 3)
        self.assertEqual(list(proxy["a"]), [1, 2, 3])
        self.assertEqual(sorted(iter(proxy)), ["a", "b"])

    def test_resolve_caches(self):
        proxy, gen = self._proxy()
        df = pd.DataFrame({"a": [1]})
        self.reg.settle("df", gen, result=df)
        self.assertFalse(proxy.is_resolved)
        proxy._resolve()
        self.assertTrue(proxy.is_resolved)
        # Second resolve returns the cached frame without touching the registry again.
        self.assertIs(proxy._resolve(), df)

    def test_blocking_access_waits_for_background_settle(self):
        proxy, gen = self._proxy()
        df = pd.DataFrame({"a": [7, 8]})

        def _settle_later():
            time.sleep(0.05)
            self.reg.settle("df", gen, result=df)

        t = threading.Thread(target=_settle_later)
        t.start()
        # .shape access blocks until settle, then forwards.
        self.assertEqual(proxy.shape, (2, 1))
        t.join()

    def test_timeout_raises(self):
        proxy, _gen = self._proxy(timeout=0.05)  # never settled
        with self.assertRaises(TimeoutError):
            proxy._resolve()

    def test_failed_materialization_raises_on_access(self):
        proxy, gen = self._proxy()
        self.reg.settle("df", gen, error=_AsyncMaterializationFailed("df"))
        with self.assertRaises(_AsyncMaterializationFailed):
            _ = proxy.shape

    def test_superseded_materialization_raises_on_access(self):
        proxy, gen = self._proxy()
        self.reg.settle("df", gen, error=_AsyncMaterializationSuperseded("df"))
        with self.assertRaises(_AsyncMaterializationSuperseded):
            len(proxy)

    def test_isinstance_is_proxy_while_pending(self):
        # The known leak point: before resolution the object is a PendingDataFrame, not a
        # DataFrame. (After the background thread rebinds the namespace name, the name
        # points at a real DataFrame -- but the captured proxy stays a proxy.)
        proxy, _gen = self._proxy()
        self.assertIsInstance(proxy, PendingDataFrame)
        self.assertNotIsInstance(proxy, pd.DataFrame)

    def test_repr_forwards(self):
        proxy, gen = self._proxy()
        df = pd.DataFrame({"a": [1]})
        self.reg.settle("df", gen, result=df)
        self.assertEqual(repr(proxy), repr(df))


class PendingDataFrameOperatorForwardingTest(unittest.TestCase):
    """Implicit operator/protocol dunders must block-then-delegate, since Python
    looks them up on the type and bypasses __getattr__."""

    def setUp(self):
        self.reg = _MaterializationRegistry()

    def _settled_proxy(self, df, name="df"):
        gen, _cancel = self.reg.start(name)
        proxy = PendingDataFrame(name, gen, self.reg, timeout=2)
        self.reg.settle(name, gen, result=df)
        return proxy

    def test_bool_forwards_and_raises_pandas_ambiguous(self):
        # The silent-wrong case: a multi-element frame must raise pandas' ambiguous-truth
        # ValueError, NOT fall back to object truthiness (always True).
        proxy = self._settled_proxy(pd.DataFrame({"a": [1, 2]}))
        with self.assertRaises(ValueError):
            bool(proxy)

    def test_ordering_comparisons_forward(self):
        proxy = self._settled_proxy(pd.DataFrame({"a": [1, 2, 3]}))
        self.assertEqual(list((proxy < 2)["a"]), [True, False, False])
        self.assertEqual(list((proxy >= 2)["a"]), [False, True, True])

    def test_arithmetic_forwards_including_reflected(self):
        proxy = self._settled_proxy(pd.DataFrame({"a": [1, 2]}))
        self.assertEqual(list((proxy + 1)["a"]), [2, 3])
        self.assertEqual(list((1 + proxy)["a"]), [2, 3])  # __radd__
        self.assertEqual(list((proxy * 2)["a"]), [2, 4])
        self.assertEqual(list((10 - proxy)["a"]), [9, 8])  # __rsub__

    def test_unary_and_bitwise_forward(self):
        proxy = self._settled_proxy(pd.DataFrame({"a": [1, -2]}))
        self.assertEqual(list((-proxy)["a"]), [-1, 2])
        self.assertEqual(list(abs(proxy)["a"]), [1, 2])
        mask = self._settled_proxy(pd.DataFrame({"a": [True, False]}), name="m")
        self.assertEqual(list((~mask)["a"]), [False, True])

    def test_array_protocol_forwards(self):
        import numpy as np

        proxy = self._settled_proxy(pd.DataFrame({"a": [1, 2, 3]}))
        arr = np.asarray(proxy)  # __array__
        self.assertEqual(arr.shape, (3, 1))
        ufunc_result = np.add(proxy, 1)  # __array_ufunc__
        self.assertEqual(list(ufunc_result["a"]), [2, 3, 4])

    def test_operator_blocks_until_settled(self):
        # A dunder access on a still-pending proxy must wait for the background settle.
        gen, _cancel = self.reg.start("df")
        proxy = PendingDataFrame("df", gen, self.reg, timeout=2)
        df = pd.DataFrame({"a": [1, 2]})

        def _settle_later():
            time.sleep(0.05)
            self.reg.settle("df", gen, result=df)

        t = threading.Thread(target=_settle_later)
        t.start()
        self.assertEqual(list((proxy + 1)["a"]), [2, 3])  # blocks then delegates
        t.join()

    def test_all_forwarded_dunders_exist_on_type(self):
        # Completeness guard: every name in the generated list is a real slot on the class.
        from sagemaker_studio.utils.pending_dataframe import _FORWARDED_DUNDERS

        for name in _FORWARDED_DUNDERS:
            self.assertTrue(
                hasattr(PendingDataFrame, name), f"{name} missing from PendingDataFrame"
            )


class RegistryMemoryReleaseTest(unittest.TestCase):
    """The registry must not retain a materialized frame for the life of the kernel.
    Once every proxy bound to a run has resolved, the retained _result slot is dropped."""

    def setUp(self):
        self.reg = _MaterializationRegistry()

    def test_result_released_after_single_proxy_resolves(self):
        gen, _cancel = self.reg.start("df")
        proxy = PendingDataFrame("df", gen, self.reg, timeout=2)  # retain -> count 1
        df = pd.DataFrame({"a": [1, 2]})
        self.reg.settle("df", gen, result=df)
        self.assertIn(("df", gen), self.reg._result)  # retained while proxy unresolved
        proxy._resolve()  # last consumer resolves -> slot dropped
        self.assertNotIn(("df", gen), self.reg._result)
        self.assertNotIn(("df", gen), self.reg._consumers)
        # The frame still lives in the proxy's cache, so access still works.
        self.assertEqual(len(proxy), 2)

    def test_result_retained_until_last_of_multiple_proxies_resolves(self):
        gen, _cancel = self.reg.start("df")
        p1 = PendingDataFrame("df", gen, self.reg, timeout=2)  # count 1
        p2 = PendingDataFrame("df", gen, self.reg, timeout=2)  # count 2 (e.g. x = df)
        df = pd.DataFrame({"a": [1]})
        self.reg.settle("df", gen, result=df)
        p1._resolve()
        # Second proxy hasn't resolved yet: slot must remain so it can still read it.
        self.assertIn(("df", gen), self.reg._result)
        p2._resolve()
        self.assertNotIn(("df", gen), self.reg._result)

    def test_reap_drops_result_when_no_consumer_bound(self):
        # No proxy was ever constructed (count 0): reap reclaims the frame immediately.
        gen, _cancel = self.reg.start("df")
        self.reg.settle("df", gen, result=pd.DataFrame({"a": [1]}))
        self.assertIn(("df", gen), self.reg._result)
        self.reg.reap("df", gen)
        self.assertNotIn(("df", gen), self.reg._result)
        self.assertNotIn(("df", gen), self.reg._done)

    def test_reap_keeps_result_while_proxy_still_waiting(self):
        # reap runs in the daemon finally; if a proxy is still bound but not yet resolved,
        # reap must NOT drop the frame (the proxy still needs to read it).
        gen, _cancel = self.reg.start("df")
        proxy = PendingDataFrame("df", gen, self.reg, timeout=2)  # count 1
        df = pd.DataFrame({"a": [1, 2, 3]})
        self.reg.settle("df", gen, result=df)
        self.reg.reap("df", gen)  # daemon reap while proxy unresolved
        self.assertIn(("df", gen), self.reg._result)  # kept for the waiting proxy
        self.assertIs(proxy._resolve(), df)  # proxy can still resolve
        self.assertNotIn(("df", gen), self.reg._result)  # then released

    def test_release_consumer_is_idempotent_and_safe_after_reap(self):
        gen, _cancel = self.reg.start("df")
        proxy = PendingDataFrame("df", gen, self.reg, timeout=2)
        self.reg.settle("df", gen, result=pd.DataFrame({"a": [1]}))
        proxy._resolve()
        # A second resolve does not double-release (cached _real short-circuits), and a
        # direct extra release_consumer call is a harmless no-op.
        proxy._resolve()
        self.reg.release_consumer("df", gen)
        self.assertNotIn(("df", gen), self.reg._result)


class RegistryLeakOnNeverResolvedTest(unittest.TestCase):
    """#1: the normal success path never calls _resolve() (the background thread commits the
    real frame into the namespace and the proxy is dropped untouched). Without the
    weakref.finalize backstop, reap would see _consumers==1 and keep the frame for the
    kernel's life. The finalize must release the consumer when the proxy is GC'd."""

    def setUp(self):
        self.reg = _MaterializationRegistry()

    def test_never_resolved_proxy_releases_on_gc(self):
        import gc

        gen, _cancel = self.reg.start("df")
        proxy = PendingDataFrame("df", gen, self.reg, timeout=2)  # retain -> count 1
        self.reg.settle("df", gen, result=pd.DataFrame({"a": [1, 2]}))
        # Simulate the daemon reap while the (never-accessed) proxy is still alive: it must
        # keep the frame because a consumer is still bound.
        self.reg.reap("df", gen)
        self.assertIn(("df", gen), self.reg._result)
        # Now the proxy goes out of scope WITHOUT ever being resolved (the success path).
        del proxy
        gc.collect()
        # weakref.finalize fired release_consumer -> the frame is no longer pinned.
        self.assertNotIn(("df", gen), self.reg._result)
        self.assertNotIn(("df", gen), self.reg._consumers)

    def test_failed_run_never_resolved_releases_on_gc(self):
        import gc

        gen, _cancel = self.reg.start("df")
        proxy = PendingDataFrame("df", gen, self.reg, timeout=2)
        self.reg.settle("df", gen, error=_AsyncMaterializationFailed("df"))
        del proxy
        gc.collect()
        # The _error slot is not leaked either.
        self.assertNotIn(("df", gen), self.reg._error)
        self.assertNotIn(("df", gen), self.reg._consumers)

    def test_proxy_is_weakrefable(self):
        import weakref

        gen, _cancel = self.reg.start("df")
        proxy = PendingDataFrame("df", gen, self.reg, timeout=2)
        # __weakref__ in __slots__ makes this possible; without it weakref.ref raises.
        self.assertIsNotNone(weakref.ref(proxy))

    def test_resolved_proxy_does_not_double_release_on_gc(self):
        # A proxy that resolves releases its consumer once (in _resolve); the GC finalizer
        # must be detached so it does NOT release a second time and drive the shared count
        # negative. Without the detach, count would go 1 -> 0 (resolve) -> -1 (GC).
        import gc

        gen, _cancel = self.reg.start("df")
        proxy = PendingDataFrame("df", gen, self.reg, timeout=2)  # count 1
        self.reg.settle("df", gen, result=pd.DataFrame({"a": [1]}))
        _ = proxy._resolve()  # releases -> count 0, _result dropped
        self.assertNotIn(("df", gen), self.reg._consumers)
        del proxy
        gc.collect()  # finalizer detached -> no second release
        # Count never went negative (a negative count is the double-release signature).
        self.assertGreaterEqual(self.reg._consumers.get(("df", gen), 0), 0)

    def test_two_proxies_sharing_key_no_keyerror(self):
        # The per-index df_i proxy AND the consolidated-list element proxy
        # share one (var_name, gen). If a resolved proxy also released on GC, the shared
        # count would drop _result early and a sibling's resolve would KeyError. Detaching
        # the finalizer on resolve prevents that.
        import gc

        gen, _cancel = self.reg.start("df")
        p1 = PendingDataFrame("df", gen, self.reg, timeout=2)  # count 1
        p2 = PendingDataFrame("df", gen, self.reg, timeout=2)  # count 2
        self.reg.settle("df", gen, result=pd.DataFrame({"a": [1]}))
        r1 = p1._resolve()  # count 2 -> 1
        del p1
        gc.collect()  # p1's finalizer was detached on resolve -> count stays 1, _result kept
        # p2 can still resolve: _result was NOT popped early.
        r2 = p2._resolve()  # count 1 -> 0
        self.assertEqual(list(r1["a"]), [1])
        self.assertEqual(list(r2["a"]), [1])
        self.assertNotIn(("df", gen), self.reg._consumers)


class ProxyProbeFastFailTest(unittest.TestCase):
    """#3: introspection / rich-display probes must NOT resolve (which would block an idle
    kernel for the full timeout). A pending proxy answers them like a ready frame: raise
    AttributeError immediately so hasattr() returns False, without waiting."""

    def setUp(self):
        self.reg = _MaterializationRegistry()

    def _pending_proxy(self):
        gen, _cancel = self.reg.start("df")
        # NEVER settle -> any resolve would block until timeout. A short timeout makes an
        # accidental resolve fail fast-and-loud in the test rather than hanging it.
        return PendingDataFrame("df", gen, self.reg, timeout=0.2)

    def test_ipython_canary_does_not_block(self):
        proxy = self._pending_proxy()
        # hasattr must return False quickly, NOT raise TimeoutError from a resolve.
        self.assertFalse(hasattr(proxy, "_ipython_canary_method_should_not_exist_"))

    def test_repr_and_ipython_prefixed_probes_fast_fail(self):
        proxy = self._pending_proxy()
        # Every display-negotiation / introspection probe must fast-fail (hasattr False)
        # WITHOUT resolving -- a resolve would block the 0.2s-timeout proxy and raise
        # TimeoutError. Includes _repr_pretty_ explicitly: pandas does NOT define it, and it
        # is not covered by any resolving class method, so it MUST be in the fast-fail set
        # (regression guard for dropping the old blanket _repr_ prefix).
        for name in (
            "_repr_json_",
            "_repr_latex_",
            "_repr_markdown_",
            "_repr_javascript_",
            "_repr_pdf_",
            "_repr_jpeg_",
            "_repr_png_",
            "_repr_svg_",
            "_repr_pretty_",
            "_repr_data_resource_",
            "_repr_fits_horizontal_",
            "_repr_fits_vertical_",
            "_ipython_display_",
            "_ipython_canary_method_should_not_exist_",
            "getdoc",
            "__wrapped__",
        ):
            self.assertFalse(hasattr(proxy, name), name)

    def test_real_attribute_still_resolves(self):
        # A genuine data attribute is NOT a probe -> it must still route through _resolve().
        gen, _cancel = self.reg.start("df")
        proxy = PendingDataFrame("df", gen, self.reg, timeout=2)
        self.reg.settle("df", gen, result=pd.DataFrame({"a": [1, 2, 3]}))
        self.assertEqual(proxy.shape, (3, 1))


class ResolveAtomicityAndNoneGuardTest(unittest.TestCase):
    """#9 (atomic consume) and #11 (never cache None)."""

    def setUp(self):
        self.reg = _MaterializationRegistry()

    def test_concurrent_resolve_no_keyerror(self):
        # Two proxies (aliases) on the same run resolve concurrently. The atomic
        # consume_result must not let one drop _result between the other's read and release.
        gen, _cancel = self.reg.start("df")
        p1 = PendingDataFrame("df", gen, self.reg, timeout=2)
        p2 = PendingDataFrame("df", gen, self.reg, timeout=2)
        df = pd.DataFrame({"a": [1, 2]})
        self.reg.settle("df", gen, result=df)
        errors = []
        results = []

        def _resolve(p):
            try:
                results.append(p._resolve())
            except Exception as e:  # pragma: no cover - failure path asserted below
                errors.append(e)

        t1 = threading.Thread(target=_resolve, args=(p1,))
        t2 = threading.Thread(target=_resolve, args=(p2,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        self.assertEqual(errors, [])
        self.assertEqual(len(results), 2)
        self.assertNotIn(("df", gen), self.reg._result)  # released after last consumer

    def test_settled_none_is_treated_as_failure_not_cached(self):
        # #11: a mis-settled None (should not happen, but guard it) must raise rather than
        # cache None and drive later accesses / the consumer count wrong.
        gen, _cancel = self.reg.start("df")
        proxy = PendingDataFrame("df", gen, self.reg, timeout=2)
        self.reg.settle("df", gen, result=None)
        with self.assertRaises(_AsyncMaterializationFailed):
            proxy._resolve()
        self.assertFalse(proxy.is_resolved)  # None was NOT cached


class TerminalErrorIdempotencyTest(unittest.TestCase):
    """A proxy whose run settled non-success must re-raise the SAME terminal error on every
    later access -- symmetric with the _real success cache -- instead of re-entering
    consume_result on an already-released consumer (which would KeyError on a dropped slot
    and double-decrement the shared count)."""

    def setUp(self):
        self.reg = _MaterializationRegistry()

    def test_failed_run_reraises_terminal_error_on_repeat_access_not_keyerror(self):
        gen, _cancel = self.reg.start("df")
        proxy = PendingDataFrame("df", gen, self.reg, timeout=2)  # count 1 (last consumer)
        err = _AsyncMaterializationFailed("df")
        self.reg.settle("df", gen, error=err)
        # First access raises the terminal error AND (being the last consumer) drops the
        # _error slot inside consume_result.
        with self.assertRaises(_AsyncMaterializationFailed):
            _ = proxy.shape
        self.assertNotIn(("df", gen), self.reg._error)  # slot dropped by the first access
        # Second access must re-raise the SAME cached error, NOT a KeyError from re-entering
        # consume_result on the now-empty slot.
        with self.assertRaises(_AsyncMaterializationFailed) as ctx:
            _ = proxy.shape
        self.assertIs(ctx.exception, err)
        # Third access, via a different code path (a dunder), still re-raises the same error.
        with self.assertRaises(_AsyncMaterializationFailed):
            len(proxy)

    def test_superseded_run_reraises_terminal_error_on_repeat_access(self):
        gen, _cancel = self.reg.start("df")
        proxy = PendingDataFrame("df", gen, self.reg, timeout=2)
        err = _AsyncMaterializationSuperseded("df")
        self.reg.settle("df", gen, error=err)
        with self.assertRaises(_AsyncMaterializationSuperseded):
            _ = proxy.columns
        with self.assertRaises(_AsyncMaterializationSuperseded) as ctx:
            _ = proxy.columns
        self.assertIs(ctx.exception, err)

    def test_repeat_access_after_failure_does_not_drive_count_negative(self):
        # Two proxies share the key; one fails-then-repeats. The repeat must not re-release
        # (it short-circuits on the cached error), so the shared consumer count never goes
        # negative and the sibling is unaffected.
        gen, _cancel = self.reg.start("df")
        p1 = PendingDataFrame("df", gen, self.reg, timeout=2)  # count 1
        p2 = PendingDataFrame("df", gen, self.reg, timeout=2)  # count 2
        err = _AsyncMaterializationFailed("df")
        self.reg.settle("df", gen, error=err)
        with self.assertRaises(_AsyncMaterializationFailed):
            _ = p1.shape  # count 2 -> 1
        with self.assertRaises(_AsyncMaterializationFailed):
            _ = p1.shape  # cached: NO further release, count stays 1
        self.assertGreaterEqual(self.reg._consumers.get(("df", gen), 0), 0)
        # p2 can still resolve its error without KeyError (slot kept while it was bound).
        with self.assertRaises(_AsyncMaterializationFailed):
            _ = p2.shape  # count 1 -> 0
        self.assertNotIn(("df", gen), self.reg._consumers)

    def test_none_guard_error_is_cached_and_reraised(self):
        # The mis-settled-None path also caches its synthesized _AsyncMaterializationFailed
        # so a second access re-raises it rather than re-waiting/re-consuming.
        gen, _cancel = self.reg.start("df")
        proxy = PendingDataFrame("df", gen, self.reg, timeout=2)
        self.reg.settle("df", gen, result=None)
        with self.assertRaises(_AsyncMaterializationFailed) as first:
            proxy._resolve()
        with self.assertRaises(_AsyncMaterializationFailed) as second:
            proxy._resolve()
        self.assertIs(first.exception, second.exception)  # same cached error object


class ProxyForwardingMethodsTest(unittest.TestCase):
    """Remaining transparent-forwarding methods that block-then-delegate: the explicit
    dunders and helper methods on the class (not the generated _FORWARDED_DUNDERS loop)."""

    def setUp(self):
        self.reg = _MaterializationRegistry()

    def _settled_proxy(self, df, name="df"):
        gen, _cancel = self.reg.start(name)
        proxy = PendingDataFrame(name, gen, self.reg, timeout=2)
        self.reg.settle(name, gen, result=df)
        return proxy

    def test_public_resolve_alias_returns_real_frame(self):
        df = pd.DataFrame({"a": [1, 2]})
        proxy = self._settled_proxy(df)
        # resolve() is the public alias for _resolve() (used by the DuckDB pre-resolve pass).
        self.assertIs(proxy.resolve(), df)

    def test_str_forwards(self):
        df = pd.DataFrame({"a": [1, 2]})
        proxy = self._settled_proxy(df)
        self.assertEqual(str(proxy), str(df))

    def test_setattr_forwards_to_frame(self):
        df = pd.DataFrame({"a": [1, 2]})
        proxy = self._settled_proxy(df)
        # A non-slot attribute set mutates the underlying frame (adds a column).
        proxy.columns = ["b"]
        self.assertEqual(list(proxy.columns), ["b"])

    def test_setitem_forwards_to_frame(self):
        df = pd.DataFrame({"a": [1, 2]})
        proxy = self._settled_proxy(df)
        proxy["b"] = [3, 4]
        self.assertEqual(list(proxy["b"]), [3, 4])

    def test_contains_forwards(self):
        df = pd.DataFrame({"a": [1], "b": [2]})
        proxy = self._settled_proxy(df)
        self.assertIn("a", proxy)
        self.assertNotIn("z", proxy)

    def test_eq_and_ne_forward(self):
        df = pd.DataFrame({"a": [1, 2]})
        proxy = self._settled_proxy(df)
        # == / != delegate to pandas (elementwise), returning a DataFrame mask.
        eq_mask = proxy == 1
        self.assertEqual(list(eq_mask["a"]), [True, False])
        ne_mask = proxy != 1
        self.assertEqual(list(ne_mask["a"]), [False, True])

    def test_hash_forwards_and_raises_like_pandas(self):
        # DataFrames are unhashable: the proxy delegates, so hash() raises TypeError.
        df = pd.DataFrame({"a": [1, 2]})
        proxy = self._settled_proxy(df)
        with self.assertRaises(TypeError):
            hash(proxy)

    def test_repr_html_forwards_to_real(self):
        df = pd.DataFrame({"a": [1, 2]})
        proxy = self._settled_proxy(df)
        # _repr_html_ resolves then delegates to the real frame's _repr_html_.
        self.assertEqual(proxy._repr_html_(), df._repr_html_())

    def test_repr_html_falls_back_to_repr_when_absent(self):
        # If the real object lacks _repr_html_, fall back to repr(real).
        class Plain:
            def __repr__(self):
                return "PLAIN"

        gen, _cancel = self.reg.start("df")
        proxy = PendingDataFrame("df", gen, self.reg, timeout=2)
        self.reg.settle("df", gen, result=Plain())
        self.assertEqual(proxy._repr_html_(), "PLAIN")

    def test_repr_mimebundle_forwards_when_present(self):
        # A real object that defines _repr_mimebundle_ has it called with include/exclude.
        class WithBundle:
            def _repr_mimebundle_(self, include=None, exclude=None):
                return {"text/plain": "bundle", "include": include, "exclude": exclude}

        gen, _cancel = self.reg.start("df")
        proxy = PendingDataFrame("df", gen, self.reg, timeout=2)
        self.reg.settle("df", gen, result=WithBundle())
        out = proxy._repr_mimebundle_(include=["text/plain"], exclude=None)
        self.assertEqual(out["text/plain"], "bundle")
        self.assertEqual(out["include"], ["text/plain"])

    def test_repr_mimebundle_falls_back_to_text_plain(self):
        # pandas DataFrames do NOT define _repr_mimebundle_, so the proxy returns a
        # {"text/plain": repr(real)} bundle.
        df = pd.DataFrame({"a": [1]})
        proxy = self._settled_proxy(df)
        out = proxy._repr_mimebundle_()
        self.assertEqual(out, {"text/plain": repr(df)})

    def test_reduce_pickles_as_resolved_frame(self):
        import pickle

        df = pd.DataFrame({"a": [1, 2, 3]})
        proxy = self._settled_proxy(df)
        # __reduce__ pickles the resolved frame, so a round-trip is a plain DataFrame.
        restored = pickle.loads(pickle.dumps(proxy))
        self.assertIsInstance(restored, pd.DataFrame)
        self.assertNotIsInstance(restored, PendingDataFrame)
        self.assertEqual(list(restored["a"]), [1, 2, 3])

    def test_identity_unpickle_helper_returns_object(self):
        from sagemaker_studio.utils.pending_dataframe import _identity

        sentinel = object()
        self.assertIs(_identity(sentinel), sentinel)


class ProxyBackCompatRegistryTest(unittest.TestCase):
    """A registry double WITHOUT consume_result exercises the two-call back-compat path in
    _resolve (get_result + release_consumer), and a registry without retain/release_consumer
    exercises the best-effort getattr guards in __init__."""

    def test_resolve_uses_get_result_and_release_when_no_consume_result(self):
        calls = {"get": 0, "release": 0}
        df = pd.DataFrame({"a": [1, 2]})

        class NoConsumeRegistry:
            # No consume_result attribute -> _resolve falls back to get_result + release.
            def retain(self, var_name, gen):
                pass

            def wait_until_ready(self, var_name, gen, timeout):
                return True

            def get_result(self, var_name, gen):
                calls["get"] += 1
                return df

            def release_consumer(self, var_name, gen):
                calls["release"] += 1

        proxy = PendingDataFrame("df", 1, NoConsumeRegistry(), timeout=2)
        self.assertIs(proxy._resolve(), df)
        self.assertEqual(calls["get"], 1)
        self.assertEqual(calls["release"], 1)

    def test_init_tolerates_registry_without_retain_or_release(self):
        # An older registry / bare double lacking retain (and release_consumer) must not
        # break proxy construction: the getattr(..., None) guards no-op.
        df = pd.DataFrame({"a": [1]})

        class BareRegistry:
            def wait_until_ready(self, var_name, gen, timeout):
                return True

            def consume_result(self, var_name, gen):
                return df

        proxy = PendingDataFrame("df", 1, BareRegistry(), timeout=2)  # no retain -> no finalizer
        self.assertIsNone(object.__getattribute__(proxy, "_finalizer"))
        self.assertIs(proxy._resolve(), df)

    def test_init_with_retain_but_no_release_sets_no_finalizer(self):
        # A registry that has retain but NOT release_consumer: retain runs, but the
        # finalizer is not armed (the inner `release is not None` guard is False).
        df = pd.DataFrame({"a": [1]})
        retained = []

        class RetainOnlyRegistry:
            def retain(self, var_name, gen):
                retained.append((var_name, gen))

            def wait_until_ready(self, var_name, gen, timeout):
                return True

            def consume_result(self, var_name, gen):
                return df

        proxy = PendingDataFrame("df", 7, RetainOnlyRegistry(), timeout=2)
        self.assertEqual(retained, [("df", 7)])  # retain was called
        self.assertIsNone(object.__getattribute__(proxy, "_finalizer"))  # but no finalizer

    def test_resolve_get_result_without_release_consumer(self):
        # Back-compat: a registry with get_result but NO release_consumer takes the
        # `release is None` branch (get_result only, no release call).
        df = pd.DataFrame({"a": [1, 2]})
        calls = {"get": 0}

        class GetOnlyRegistry:
            def retain(self, var_name, gen):
                pass

            def wait_until_ready(self, var_name, gen, timeout):
                return True

            def get_result(self, var_name, gen):
                calls["get"] += 1
                return df

            # no consume_result, no release_consumer

        proxy = PendingDataFrame("df", 1, GetOnlyRegistry(), timeout=2)
        self.assertIs(proxy._resolve(), df)
        self.assertEqual(calls["get"], 1)

    def test_setattr_to_slot_name_sets_slot_not_frame(self):
        # __setattr__ with a slot name goes through object.__setattr__ (sets the slot),
        # NOT through the frame-mutation else-branch. Setting _real to a frame makes the
        # proxy resolved without any registry round-trip.
        reg = _MaterializationRegistry()
        gen, _cancel = reg.start("df")
        proxy = PendingDataFrame("df", gen, reg, timeout=2)
        df = pd.DataFrame({"a": [1, 2]})
        proxy._real = df  # slot name -> object.__setattr__ path
        self.assertTrue(proxy.is_resolved)
        self.assertIs(proxy._resolve(), df)


class DefaultStallTimeoutParseTest(unittest.TestCase):
    """`_parse_stall_timeout_seconds` reads SAGEMAKER_STUDIO_ASYNC_STALL_TIMEOUT_SECONDS and
    falls back to the default on a missing or non-numeric value. Calls the real function
    (not a module reload, which would rebind PendingDataFrame and break other tests)."""

    def test_invalid_env_value_falls_back_to_default(self):
        import os
        from unittest import mock

        import sagemaker_studio.utils.pending_dataframe as pdmod

        with mock.patch.dict(
            os.environ, {"SAGEMAKER_STUDIO_ASYNC_STALL_TIMEOUT_SECONDS": "not-a-number"}
        ):
            self.assertEqual(pdmod._parse_stall_timeout_seconds(), 300.0)

    def test_valid_env_value_is_used(self):
        import os
        from unittest import mock

        import sagemaker_studio.utils.pending_dataframe as pdmod

        with mock.patch.dict(os.environ, {"SAGEMAKER_STUDIO_ASYNC_STALL_TIMEOUT_SECONDS": "42.5"}):
            self.assertEqual(pdmod._parse_stall_timeout_seconds(), 42.5)

    def test_missing_env_value_uses_default(self):
        import os
        from unittest import mock

        import sagemaker_studio.utils.pending_dataframe as pdmod

        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("SAGEMAKER_STUDIO_ASYNC_STALL_TIMEOUT_SECONDS", None)
            self.assertEqual(pdmod._parse_stall_timeout_seconds(), 300.0)


if __name__ == "__main__":
    unittest.main()
