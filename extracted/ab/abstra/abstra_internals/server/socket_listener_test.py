import types
import unittest
from typing import Any, Callable, List, Optional
from unittest import mock

from simple_websocket import ConnectionClosed

from abstra_internals.server.socket_listener import (
    DEFAULT_INACTIVITY_TIMEOUT_SECONDS,
    drain_inbound_frames,
    serve_listener_websocket,
)


class FakeWS:
    """Fake websocket with a scripted receive().

    Each item in `script` is either a message (returned), None (returned,
    signalling inactivity timeout) or an exception instance (raised).
    Every call's `timeout` keyword is recorded in `timeouts`. The `timeout`
    parameter is keyword-only on purpose: passing it positionally raises a
    TypeError before the call is recorded, so the tests can assert the
    production code passes it as a keyword argument.
    """

    def __init__(
        self,
        script: List[Any],
        call_log: Optional[List[str]] = None,
    ) -> None:
        self.script = list(script)
        self.timeouts: List[Any] = []
        self.thread = types.SimpleNamespace(name="")
        self.call_log = call_log

    def receive(self, *, timeout: Any = None) -> Any:
        self.timeouts.append(timeout)
        if self.call_log is not None:
            self.call_log.append("receive")
        item = self.script.pop(0)
        if isinstance(item, BaseException):
            raise item
        return item


class FakeRegistry:
    """Fake registry recording register/unregister calls."""

    def __init__(
        self,
        call_log: Optional[List[str]] = None,
        register_side_effect: Optional[BaseException] = None,
    ) -> None:
        self.registered: List[Any] = []
        self.unregistered: List[Any] = []
        self.call_log = call_log
        self.register_side_effect = register_side_effect

    def register(self, ws: Any) -> None:
        if self.call_log is not None:
            self.call_log.append("register")
        if self.register_side_effect is not None:
            raise self.register_side_effect
        self.registered.append(ws)

    def unregister(self, ws: Any) -> None:
        if self.call_log is not None:
            self.call_log.append("unregister")
        self.unregistered.append(ws)


class TestDrainInboundFrames(unittest.TestCase):
    def test_returns_when_receive_returns_none(self):
        """drain returns cleanly when receive returns None (inactivity)."""
        ws = FakeWS(script=[None])

        result = drain_inbound_frames(ws)

        self.assertIsNone(result)
        self.assertEqual(len(ws.timeouts), 1)

    def test_returns_when_receive_raises_connection_closed(self):
        """ConnectionClosed from receive must not propagate."""
        ws = FakeWS(script=[ConnectionClosed()])

        drain_inbound_frames(ws)  # must not raise

        self.assertEqual(len(ws.timeouts), 1)

    def test_returns_when_receive_raises_generic_exception(self):
        """Any exception from receive must not propagate."""
        ws = FakeWS(script=[OSError("socket error")])

        drain_inbound_frames(ws)  # must not raise

        self.assertEqual(len(ws.timeouts), 1)

    def test_discards_messages_then_exits_on_none(self):
        """N keepalive frames then None must call receive exactly N+1 times."""
        ws = FakeWS(script=["keepalive", "keepalive", "keepalive", None])

        drain_inbound_frames(ws)

        self.assertEqual(len(ws.timeouts), 4)
        self.assertEqual(ws.script, [])

    def test_discards_messages_then_exits_on_disconnect(self):
        """Messages are discarded until the client disconnects."""
        ws = FakeWS(script=["keepalive", ConnectionClosed()])

        drain_inbound_frames(ws)

        self.assertEqual(len(ws.timeouts), 2)

    def test_passes_custom_timeout_as_keyword(self):
        """The given inactivity_timeout reaches every receive call."""
        ws = FakeWS(script=["keepalive", None])

        drain_inbound_frames(ws, inactivity_timeout=7.5)

        self.assertEqual(ws.timeouts, [7.5, 7.5])

    def test_uses_default_timeout_when_not_given(self):
        """Without inactivity_timeout, the module default is used."""
        ws = FakeWS(script=[None])

        drain_inbound_frames(ws)

        self.assertEqual(ws.timeouts, [DEFAULT_INACTIVITY_TIMEOUT_SECONDS])

    def test_default_inactivity_timeout_value(self):
        """The module-level default is 130 seconds (tolerates Chrome's
        hidden-page keepalive throttling; see the constant's comment)."""
        self.assertEqual(DEFAULT_INACTIVITY_TIMEOUT_SECONDS, 130)


class TestServeListenerWebsocket(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch("abstra_internals.server.socket_listener.AbstraLogger")
        self.logger = patcher.start()
        self.addCleanup(patcher.stop)

    def serve(
        self,
        ws: FakeWS,
        registry: FakeRegistry,
        *,
        thread_name: str = "test-listener",
        on_registered: Optional[Callable[[Any], None]] = None,
        **kwargs: Any,
    ) -> Any:
        return serve_listener_websocket(
            ws,
            thread_name=thread_name,
            registry=registry,
            on_registered=on_registered,
            **kwargs,
        )

    def test_sets_thread_name(self):
        """ws.thread.name must be set to the given thread_name."""
        ws = FakeWS(script=[None])
        registry = FakeRegistry()

        self.serve(ws, registry, thread_name="editor-logs-listener")

        self.assertEqual(ws.thread.name, "editor-logs-listener")

    def test_registers_before_drain_and_unregisters_after(self):
        """register happens before the first receive; unregister after."""
        call_log: List[str] = []
        ws = FakeWS(script=["keepalive", None], call_log=call_log)
        registry = FakeRegistry(call_log=call_log)

        self.serve(ws, registry)

        self.assertEqual(call_log, ["register", "receive", "receive", "unregister"])
        self.assertEqual(registry.registered, [ws])
        self.assertEqual(registry.unregistered, [ws])

    def test_on_registered_called_once_with_ws_after_register_before_receive(self):
        """on_registered runs once, after register and before draining."""
        call_log: List[str] = []
        ws = FakeWS(script=[None], call_log=call_log)
        registry = FakeRegistry(call_log=call_log)
        on_registered_calls: List[Any] = []

        def on_registered(received_ws: Any) -> None:
            call_log.append("on_registered")
            on_registered_calls.append(received_ws)

        self.serve(ws, registry, on_registered=on_registered)

        self.assertEqual(on_registered_calls, [ws])
        self.assertEqual(
            call_log, ["register", "on_registered", "receive", "unregister"]
        )

    def test_on_registered_none_is_supported(self):
        """on_registered=None (the default) must work without errors."""
        ws = FakeWS(script=[None])
        registry = FakeRegistry()

        result = serve_listener_websocket(
            ws, thread_name="no-callback", registry=registry
        )

        self.assertIsNone(result)
        self.assertEqual(registry.registered, [ws])
        self.assertEqual(registry.unregistered, [ws])

    def test_on_registered_raising_is_captured_and_unregisters(self):
        """An exception in on_registered is captured and unregister still runs."""
        ws = FakeWS(script=[None])
        registry = FakeRegistry()
        error = ValueError("on_registered boom")

        def on_registered(_ws: Any) -> None:
            raise error

        result = self.serve(ws, registry, on_registered=on_registered)

        self.assertIsNone(result)
        self.logger.capture_exception.assert_called_once_with(error)
        self.assertEqual(registry.unregistered, [ws])

    def test_register_raising_is_captured_and_unregisters(self):
        """An exception in registry.register is captured; unregister still runs."""
        error = RuntimeError("register boom")
        ws = FakeWS(script=[None])
        registry = FakeRegistry(register_side_effect=error)

        result = self.serve(ws, registry)

        self.assertIsNone(result)
        self.logger.capture_exception.assert_called_once_with(error)
        self.assertEqual(registry.unregistered, [ws])
        self.assertEqual(len(registry.unregistered), 1)

    def test_connection_closed_is_a_normal_disconnect(self):
        """ConnectionClosed: clean return, unregister called, nothing captured."""
        ws = FakeWS(script=[ConnectionClosed()])
        registry = FakeRegistry()

        result = self.serve(ws, registry)

        self.assertIsNone(result)
        self.assertEqual(registry.unregistered, [ws])
        self.assertEqual(len(registry.unregistered), 1)
        self.logger.capture_exception.assert_not_called()

    def test_inactivity_returns_cleanly_and_unregisters(self):
        """receive returning None (inactivity): clean return + unregister."""
        ws = FakeWS(script=[None])
        registry = FakeRegistry()

        result = self.serve(ws, registry)

        self.assertIsNone(result)
        self.assertEqual(registry.unregistered, [ws])
        self.assertEqual(len(registry.unregistered), 1)
        self.logger.capture_exception.assert_not_called()

    def test_custom_inactivity_timeout_reaches_receive(self):
        """A custom inactivity_timeout is forwarded to every receive call."""
        ws = FakeWS(script=["keepalive", "keepalive", None])
        registry = FakeRegistry()

        self.serve(ws, registry, inactivity_timeout=12.5)

        self.assertEqual(ws.timeouts, [12.5, 12.5, 12.5])

    def test_default_inactivity_timeout_reaches_receive(self):
        """Without inactivity_timeout, receive gets the module default."""
        ws = FakeWS(script=[None])
        registry = FakeRegistry()

        self.serve(ws, registry)

        self.assertEqual(ws.timeouts, [DEFAULT_INACTIVITY_TIMEOUT_SECONDS])

    def test_keepalive_frames_are_discarded_until_inactivity(self):
        """Inbound keepalive frames are drained; receive runs N+1 times."""
        ws = FakeWS(script=["keepalive", "keepalive", "keepalive", None])
        registry = FakeRegistry()

        self.serve(ws, registry)

        self.assertEqual(len(ws.timeouts), 4)
        self.assertEqual(registry.unregistered, [ws])


if __name__ == "__main__":
    unittest.main()
