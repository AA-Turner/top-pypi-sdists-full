"""A small rosbridge client: the JSON protocol a ROS 2 graph speaks over one WebSocket.

Anvil's Devbox serves its control stack's topics and services this way, so a program beside
the stack needs no ROS install. One reader thread hands each message to its topic's handler;
handlers must return quickly.
"""

from __future__ import annotations

import itertools
import json
import threading

from dreamscale.hardware.rig import RigFault


class RosBridgeError(RigFault):
    """The bridge can't be reached, closed, or didn't answer."""


def _connect(url, *, timeout_s):
    from websockets.sync.client import connect

    # Camera frames arrive as large messages; on one machine compressing them costs more
    # than it saves.
    return connect(url, open_timeout=timeout_s, max_size=None, compression=None)


class RosBridge:
    """subscribe, advertise and publish topics and call services on one rosbridge server."""

    def __init__(self, url, *, connect=_connect, timeout_s=5.0):
        self.url, self._connect, self.timeout_s = url, connect, timeout_s
        self._ws = None
        self._send_lock = threading.Lock()
        self._handlers = {}
        self._calls = {}
        self._ids = itertools.count(1)
        self._closed = threading.Event()
        self._thread = None
        self.failure = None
        # The last exception a topic's handler raised; its message was dropped.
        self.handler_failure = None

    def open(self) -> RosBridge:
        if self._ws is not None:
            raise RosBridgeError("Already connected.")
        try:
            self._ws = self._connect(self.url, timeout_s=self.timeout_s)
        except Exception as exc:
            raise RosBridgeError(f"No rosbridge at {self.url}: {exc}") from exc
        self._closed.clear()
        self._thread = threading.Thread(
            target=self._read, args=(self._ws,), name="rosbridge", daemon=True,
        )
        self._thread.start()
        return self

    @property
    def alive(self) -> bool:
        return self._ws is not None and not self._closed.is_set()

    def _read(self, ws):
        try:
            for raw in ws:
                message = json.loads(raw)
                op = message.get("op")
                if op == "publish":
                    handler = self._handlers.get(message.get("topic"))
                    if handler is not None:
                        try:
                            handler(message.get("msg") or {})
                        except Exception as exc:  # noqa: BLE001 - one bad message, not the link
                            self.handler_failure = exc
                elif op == "service_response":
                    call = self._calls.get(message.get("id"))
                    if call is not None:
                        call["response"] = message
                        call["done"].set()
        except Exception as exc:
            self.failure = exc
        finally:
            self._closed.set()
            for call in list(self._calls.values()):
                call["done"].set()

    def _send(self, message):
        if not self.alive:
            raise RosBridgeError(f"The connection to {self.url} closed.")
        try:
            with self._send_lock:
                self._ws.send(json.dumps(message))
        except Exception as exc:
            raise RosBridgeError(f"The connection to {self.url} failed: {exc}") from exc

    def subscribe(self, topic, type, handler, *, throttle_ms=0, queue_length=1):
        """handler(msg) for each message, at most one per throttle_ms, newest kept."""
        self._handlers[topic] = handler
        self._send({
            "op": "subscribe", "topic": topic, "type": type, "throttle_rate": int(throttle_ms),
            "queue_length": int(queue_length),
        })

    def unsubscribe(self, topic):
        if self._handlers.pop(topic, None) is not None and self.alive:
            self._send({"op": "unsubscribe", "topic": topic})

    def advertise(self, topic, type):
        self._send({"op": "advertise", "topic": topic, "type": type})

    def publish(self, topic, msg):
        self._send({"op": "publish", "topic": topic, "msg": msg})

    def call(self, service, args=None, *, type=None, timeout_s=None):
        """A service's response values; raises if it fails or doesn't answer in time."""
        call_id = f"call:{next(self._ids)}"
        call = self._calls[call_id] = {"done": threading.Event(), "response": None}
        try:
            self._send({
                "op": "call_service", "id": call_id, "service": service, "args": args or {},
                **({"type": type} if type is not None else {}),
            })
            if not call["done"].wait(self.timeout_s if timeout_s is None else timeout_s):
                raise RosBridgeError(f"{service} didn't answer.")
        finally:
            self._calls.pop(call_id, None)
        response = call["response"]
        if response is None:
            raise RosBridgeError(f"The connection closed before {service} answered.")
        if response.get("result") is False:
            raise RosBridgeError(f"{service} failed: {response.get('values')}")
        values = response.get("values")
        return values if isinstance(values, dict) else {}

    def close(self):
        ws, self._ws = self._ws, None
        if ws is None:
            return
        try:
            ws.close()
        finally:
            self._closed.set()
            if self._thread is not None and self._thread is not threading.current_thread():
                self._thread.join(timeout=2.0)
            self._handlers.clear()
