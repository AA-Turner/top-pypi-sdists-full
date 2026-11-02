"""Eligibility and lifecycle checks for temporary signal handlers."""

import signal
from contextlib import ExitStack
from types import SimpleNamespace
from unittest.mock import Mock, call, patch

import pytest

from agentic_devtools.cli.checks import pre_push_budget


def test_returns_restorable_signals_in_order_using_default_scope_predicates():
    term_handler = Mock()
    registration = Mock()
    signal_api = SimpleNamespace(SIGTERM=15, SIGHUP=1, signal=registration)
    get_handler = Mock(side_effect={15: term_handler, 1: signal.SIG_IGN}.get)
    main_thread = object()
    with (
        patch.object(pre_push_budget.os, "name", "posix"),
        patch.object(pre_push_budget.threading, "current_thread", return_value=main_thread),
        patch.object(pre_push_budget.threading, "main_thread", return_value=main_thread),
        patch.object(pre_push_budget, "signal", signal_api),
    ):
        with pre_push_budget._temporary_signal_handlers(get_handler=get_handler) as lifecycle:
            assert lifecycle.phase == "installing"
    get_handler.assert_has_calls([call(15), call(1)])
    assert [args[0] for args, _ in registration.call_args_list] == [15, 1, 1, 15]
    assert registration.call_args_list[-2:] == [call(1, signal.SIG_IGN), call(15, term_handler)]


def test_non_posix_scope_skips_handler_lookup():
    registration = Mock()
    signal_api = SimpleNamespace(SIGTERM=15, SIGHUP=1, signal=registration)
    get_handler = Mock()
    with (
        patch.object(pre_push_budget.os, "name", "nt"),
        patch.object(pre_push_budget, "signal", signal_api),
    ):
        with pre_push_budget._temporary_signal_handlers(get_handler=get_handler) as lifecycle:
            assert lifecycle.first_signum is None
    get_handler.assert_not_called()
    registration.assert_not_called()


def test_non_main_thread_scope_skips_handler_lookup():
    registration = Mock()
    signal_api = SimpleNamespace(SIGTERM=15, SIGHUP=1, signal=registration)
    get_handler = Mock()
    with patch.object(pre_push_budget, "signal", signal_api):
        with pre_push_budget._temporary_signal_handlers(
            is_posix=lambda: True, is_main_thread=lambda: False, get_handler=get_handler
        ) as lifecycle:
            assert lifecycle.first_signum is None
    get_handler.assert_not_called()
    registration.assert_not_called()


@pytest.mark.parametrize(("missing", "available"), [("SIGTERM", 1), ("SIGHUP", 15)])
def test_missing_signal_attribute_skips_only_that_candidate(missing, available):
    registration = Mock()
    attributes = {"SIGTERM": 15, "SIGHUP": 1}
    del attributes[missing]
    signal_api = SimpleNamespace(**attributes, signal=registration)
    get_handler = Mock(return_value=signal.SIG_DFL)
    with patch.object(pre_push_budget, "signal", signal_api):
        with pre_push_budget._temporary_signal_handlers(
            is_posix=lambda: True, is_main_thread=lambda: True, get_handler=get_handler
        ):
            assert registration.call_args[0][0] == available
    get_handler.assert_called_once_with(available)
    assert registration.call_args_list[-1] == call(available, signal.SIG_DFL)
    assert registration.call_count == 2


def test_none_previous_handler_is_omitted_without_substitution():
    registration = Mock()
    signal_api = SimpleNamespace(SIGTERM=15, SIGHUP=1, signal=registration)
    get_handler = Mock(side_effect={15: None, 1: signal.SIG_DFL}.get)
    with patch.object(pre_push_budget, "signal", signal_api):
        with pre_push_budget._temporary_signal_handlers(
            is_posix=lambda: True, is_main_thread=lambda: True, get_handler=get_handler
        ):
            assert registration.call_args[0][0] == 1
    get_handler.assert_has_calls([call(15), call(1)])
    assert registration.call_args_list[-1] == call(1, signal.SIG_DFL)
    assert registration.call_count == 2


@pytest.fixture
def lifecycle_scope():
    previous = {15: Mock(), 1: signal.SIG_IGN}
    registration = Mock()
    api = SimpleNamespace(SIGTERM=15, SIGHUP=1, signal=registration)
    with patch.object(pre_push_budget, "signal", api):
        scope = pre_push_budget._temporary_signal_handlers(
            is_posix=lambda: True, is_main_thread=lambda: True, get_handler=previous.get
        )
        yield scope, registration, previous


@pytest.mark.parametrize("delivery", ["none", "installing", "body", "boundary", "cleanup", "exit", "restoring"])
def test_lifecycle_deliveries(lifecycle_scope, delivery):
    scope, registration, previous = lifecycle_scope
    handlers = {}
    restores = []
    cleanup = Mock()

    def register(signum, handler):
        if handler is previous[signum]:
            assert lifecycle.phase == "restoring"
            restores.append(signum)
            if delivery == "restoring":
                handlers[15](15, None)
                handlers[1](1, None)
        else:
            handlers[signum] = handler
            if delivery == "installing":
                handler(1, None)

    registration.side_effect = register
    with scope as lifecycle:
        assert not lifecycle.restoration_started
        try:
            lifecycle.begin_body()
            assert lifecycle.phase == "body"
            if delivery in ("body", "boundary"):
                handlers[15](15, None)
            lifecycle.begin_cleanup()
        except lifecycle.Interrupted:
            assert lifecycle.first_signum == (1 if delivery == "installing" else 15)
        finally:
            lifecycle.begin_cleanup()
            assert lifecycle.phase == "cleanup"
            cleanup()
            if delivery == "cleanup":
                handlers[1](1, None)
                handlers[15](15, None)
        if delivery == "exit":
            handlers[15](15, None)
    cleanup.assert_called_once()
    assert restores == [1, 15]
    assert lifecycle.restoration_started
    expected = {"none": None, "installing": 1, "cleanup": 1}
    assert lifecycle.first_signum == expected.get(delivery, 15)


@pytest.mark.parametrize("failure", ["body", "cleanup"])
def test_exception_exits_preserve_identity_and_restore_once(lifecycle_scope, failure):
    scope, registration, _ = lifecycle_scope
    error = RuntimeError(failure)
    cleanup = Mock()
    with pytest.raises(RuntimeError) as caught:
        with scope as lifecycle:
            lifecycle.begin_body()
            try:
                if failure == "body":
                    raise error
            finally:
                lifecycle.begin_cleanup()
                cleanup()
                if failure == "cleanup":
                    raise error
    assert caught.value is error
    cleanup.assert_called_once()
    assert registration.call_count == 4


def test_body_sentinel_is_raised_once_and_not_consumed_on_exit(lifecycle_scope):
    scope, registration, _ = lifecycle_scope
    with ExitStack() as expected:
        with scope as lifecycle:
            expected.enter_context(pytest.raises(lifecycle.Interrupted))
            lifecycle.begin_body()
            with pytest.raises(lifecycle.Interrupted):
                registration.call_args[0][1](1, None)
            registration.call_args[0][1](15, None)
            lifecycle.begin_body()
            assert lifecycle.first_signum == 1
            raise lifecycle.Interrupted()
    assert lifecycle.restoration_started


@pytest.mark.parametrize("scenario", ["clean", "body", "caller-exception", "unwinding"])
def test_restoration_failures_attempt_all_signals_and_preserve_primary(lifecycle_scope, scenario):
    scope, registration, previous = lifecycle_scope
    restoration_error = OSError("SIGHUP restoration failed")
    body_error = RuntimeError("body failed")
    restored = []

    def register(signum, handler):
        if handler is previous[signum]:
            restored.append(signum)
            if signum == 1:
                raise restoration_error

    def deliver(frame, event, arg):
        if frame.f_locals.get("exc") is body_error:
            lifecycle.handle(15, None)
        return deliver

    registration.side_effect = register
    if scenario in ("body", "unwinding"):
        with ExitStack() as stack, pytest.raises(RuntimeError) as caught:
            if scenario == "unwinding":
                stack.callback(pre_push_budget.sys.settrace, pre_push_budget.sys.gettrace())
                pre_push_budget.sys.settrace(deliver)
            with scope as lifecycle:
                lifecycle.begin_body()
                raise body_error
        assert caught.value is body_error
        assert lifecycle.first_signum == (15 if scenario == "unwinding" else None)
        assert any("Signal restoration failed for 1" in note for note in body_error.__notes__)
    elif scenario == "caller-exception":
        outer_error = KeyError("caller")
        try:
            raise outer_error
        except KeyError as caught_outer:
            with pytest.raises(OSError) as caught:
                with scope as lifecycle:
                    lifecycle.begin_body()
            assert caught.value is restoration_error
            assert not getattr(caught_outer, "__notes__", [])
    else:
        with pytest.raises(OSError) as caught:
            with scope as lifecycle:
                lifecycle.begin_body()
        assert caught.value is restoration_error
    assert restored == [1, 15]


def test_nested_handler_delivery_keeps_first_signum_and_raises_once(lifecycle_scope):
    scope, _, _ = lifecycle_scope

    class ReentrantLock:
        acquired = False
        callback = None

        def acquire(self, blocking=False):
            if self.acquired:
                return False
            self.acquired = True
            callback, self.callback = self.callback, None
            if callback is not None:
                callback()
            return True

        def release(self):
            self.acquired = False

    with scope as lifecycle:
        lifecycle._handling_lock = ReentrantLock()
        lifecycle._handling_lock.callback = lambda: lifecycle.handle(1, None)
        lifecycle.begin_body()
        with pytest.raises(lifecycle.Interrupted):
            lifecycle.handle(15, None)
        lifecycle.handle(1, None)
        assert lifecycle.first_signum == 15
        assert lifecycle.interrupted


@pytest.mark.parametrize("fail_at", [15, 1])
def test_installation_failure_rolls_back_only_successes_without_interrupting(lifecycle_scope, fail_at):
    scope, registration, previous = lifecycle_scope
    error = ValueError("installation failed")
    handlers = {}
    restores = []

    def register(signum, handler):
        if handler is previous[signum]:
            assert handler_state.restoration_started
            assert handler_state.phase == "restoring"
            handlers[15](1, None)
            handlers[15](15, None)
            restores.append(signum)
        else:
            if signum == fail_at:
                raise error
            handlers[signum] = handler

    def capture(signum, handler):
        nonlocal handler_state
        if handler is not previous[signum]:
            handler_state = handler.__self__
        return register(signum, handler)

    handler_state = None
    registration.side_effect = capture
    with pytest.raises(ValueError) as caught:
        with scope:
            pytest.fail("installation should fail before entering the body")
    assert caught.value is error
    assert restores == ([] if fail_at == 15 else [15])
    assert handler_state.first_signum == (None if fail_at == 15 else 1)
