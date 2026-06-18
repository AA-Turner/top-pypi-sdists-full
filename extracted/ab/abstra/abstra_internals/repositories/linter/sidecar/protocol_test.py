"""Contract tests for the sidecar JSON-RPC stdio protocol (PR1, TDD).

Written before the implementation (RED) and kept unchanged afterwards as the
non-regression proof for the linter sidecar's IPC layer.
"""

import io
import os
import threading
import time
import unittest

from abstra_internals.repositories.linter.sidecar.protocol import (
    ConnectionClosed,
    ProtocolError,
    RpcChannel,
    RpcError,
    StopPump,
    encode_frame,
    read_frame,
)


class FramingTest(unittest.TestCase):
    def test_roundtrip_utf8_payload(self):
        msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "run_rules",
            "params": {"texto": "ação çñ 🚀", "n": 42},
        }
        buf = io.BytesIO(encode_frame(msg))
        self.assertEqual(read_frame(buf), msg)

    def test_roundtrip_large_payload(self):
        msg = {"id": 2, "result": {"blob": "x" * (5 * 1024 * 1024)}}
        buf = io.BytesIO(encode_frame(msg))
        self.assertEqual(read_frame(buf), msg)

    def test_sequential_frames(self):
        msgs = [{"id": i, "result": {"i": i}} for i in range(3)]
        buf = io.BytesIO(b"".join(encode_frame(m) for m in msgs))
        for m in msgs:
            self.assertEqual(read_frame(buf), m)
        self.assertIsNone(read_frame(buf))

    def test_eof_at_frame_boundary_returns_none(self):
        self.assertIsNone(read_frame(io.BytesIO(b"")))

    def test_truncated_header_raises_protocol_error(self):
        with self.assertRaises(ProtocolError):
            read_frame(io.BytesIO(b"Content-Length: 10"))

    def test_header_without_content_length_raises_protocol_error(self):
        with self.assertRaises(ProtocolError):
            read_frame(io.BytesIO(b"X-Nope: 1\r\n\r\n{}"))

    def test_non_numeric_content_length_raises_protocol_error(self):
        with self.assertRaises(ProtocolError):
            read_frame(io.BytesIO(b"Content-Length: abc\r\n\r\n{}"))

    def test_truncated_body_raises_protocol_error(self):
        with self.assertRaises(ProtocolError):
            read_frame(io.BytesIO(b"Content-Length: 100\r\n\r\nshort"))

    def test_invalid_json_body_raises_protocol_error(self):
        body = b"{not json}"
        data = b"Content-Length: %d\r\n\r\n" % len(body) + body
        with self.assertRaises(ProtocolError):
            read_frame(io.BytesIO(data))

    def test_concurrent_writes_do_not_interleave_frames(self):
        r_fd, w_fd = os.pipe()
        reader = os.fdopen(r_fd, "rb")
        writer = os.fdopen(w_fd, "wb")
        self.addCleanup(lambda: _close_quietly(writer, reader))

        chan = RpcChannel(io.BytesIO(), writer)
        payloads = {"p%d" % i: ("%d:" % i) + ("x" * 200_000) for i in range(8)}
        threads = [
            threading.Thread(
                target=chan.notify, args=("blob", {"key": k, "data": v}), daemon=True
            )
            for k, v in payloads.items()
        ]
        for t in threads:
            t.start()

        got = {}
        for _ in range(len(payloads)):
            msg = read_frame(reader)
            assert msg is not None
            got[msg["params"]["key"]] = msg["params"]["data"]
        for t in threads:
            t.join(timeout=5)
        self.assertEqual(got, payloads)


def _close_quietly(*streams):
    for stream in streams:
        try:
            stream.close()
        except Exception:
            pass


class RpcChannelTest(unittest.TestCase):
    def _pair(self):
        """Two RpcChannels wired to each other over OS pipes (full duplex)."""
        a2b_r, a2b_w = os.pipe()
        b2a_r, b2a_w = os.pipe()
        a_reader = os.fdopen(b2a_r, "rb")
        a_writer = os.fdopen(a2b_w, "wb")
        b_reader = os.fdopen(a2b_r, "rb")
        b_writer = os.fdopen(b2a_w, "wb")
        a = RpcChannel(a_reader, a_writer)
        b = RpcChannel(b_reader, b_writer)
        # Writers first: their EOF unblocks any pump thread stuck in read();
        # closing a reader under a blocked read deadlocks on the buffer lock.
        self.addCleanup(lambda: _close_quietly(a_writer, b_writer, a_reader, b_reader))
        return a, b

    def _pump(self, chan, dispatch=None):
        """Run chan.pump on a daemon thread; collect any raised exception."""
        errors = []

        def run():
            try:
                chan.pump(dispatch or (lambda msg: None))
            except Exception as e:  # noqa: BLE001 - test harness records anything
                errors.append(e)

        t = threading.Thread(target=run, daemon=True)
        t.start()
        return t, errors

    def test_request_response_roundtrip(self):
        a, b = self._pair()

        def b_dispatch(msg):
            b.respond(msg["id"], {"echo": msg["params"]})

        self._pump(b, b_dispatch)
        self._pump(a)
        self.assertEqual(a.request("echo", {"v": 1}, timeout=5), {"echo": {"v": 1}})

    def test_out_of_order_responses_matched_by_id(self):
        a, b = self._pair()
        pending = []
        lock = threading.Lock()

        def b_dispatch(msg):
            with lock:
                pending.append(msg)
                if len(pending) == 2:
                    # Respond in REVERSE arrival order
                    for req in reversed(pending):
                        b.respond(req["id"], {"tag": req["params"]["tag"]})

        self._pump(b, b_dispatch)
        self._pump(a)

        results = {}

        def call(tag):
            results[tag] = a.request("op", {"tag": tag}, timeout=5)

        t1 = threading.Thread(target=call, args=("one",), daemon=True)
        t2 = threading.Thread(target=call, args=("two",), daemon=True)
        t1.start()
        t2.start()
        t1.join(timeout=5)
        t2.join(timeout=5)
        self.assertEqual(results, {"one": {"tag": "one"}, "two": {"tag": "two"}})

    def test_reverse_request_while_main_request_in_flight(self):
        a, b = self._pair()

        def b_dispatch(msg):
            if msg.get("method") == "slow":

                def work():
                    r = b.request("ask", {"q": 1}, timeout=5)
                    b.respond(msg["id"], {"got": r})

                threading.Thread(target=work, daemon=True).start()

        def a_dispatch(msg):
            if msg.get("method") == "ask":
                a.respond(msg["id"], {"answer": 42})

        self._pump(b, b_dispatch)
        self._pump(a, a_dispatch)
        self.assertEqual(a.request("slow", {}, timeout=5), {"got": {"answer": 42}})

    def test_error_response_raises_rpc_error(self):
        a, b = self._pair()

        def b_dispatch(msg):
            b.respond_error(msg["id"], "boom happened")

        self._pump(b, b_dispatch)
        self._pump(a)
        with self.assertRaises(RpcError) as cm:
            a.request("explode", timeout=5)
        self.assertIn("boom happened", str(cm.exception))

    def test_request_timeout(self):
        a, b = self._pair()
        self._pump(b)  # b ignores everything
        self._pump(a)
        start = time.monotonic()
        with self.assertRaises(TimeoutError):
            a.request("never", timeout=0.2)
        self.assertLess(time.monotonic() - start, 5)

    def test_peer_close_fails_pending_and_pump_returns(self):
        a, b = self._pair()
        pump_t, errors = self._pump(a)
        result = {}

        def call():
            try:
                a.request("never", timeout=30)
            except Exception as e:  # noqa: BLE001
                result["exc"] = e

        t = threading.Thread(target=call, daemon=True)
        t.start()
        time.sleep(0.2)
        b.close()
        t.join(timeout=5)
        self.assertIsInstance(result.get("exc"), ConnectionClosed)
        pump_t.join(timeout=5)
        self.assertFalse(pump_t.is_alive())
        self.assertEqual(errors, [])  # clean EOF: pump returns, does not raise
        with self.assertRaises(ConnectionClosed):
            a.request("again", timeout=1)

    def test_corrupt_stream_fails_pending_and_pump_raises(self):
        # Hand-built wiring so the test owns the raw byte stream feeding A.
        a2b_r, a2b_w = os.pipe()
        b2a_r, b2a_w = os.pipe()
        a_reader = os.fdopen(b2a_r, "rb")
        a_writer = os.fdopen(a2b_w, "wb")
        b_reader = os.fdopen(a2b_r, "rb")
        raw_writer = os.fdopen(b2a_w, "wb")
        self.addCleanup(
            lambda: _close_quietly(a_writer, raw_writer, a_reader, b_reader)
        )
        a = RpcChannel(a_reader, a_writer)

        pump_t, errors = self._pump(a)
        result = {}

        def call():
            try:
                a.request("never", timeout=30)
            except Exception as e:  # noqa: BLE001
                result["exc"] = e

        t = threading.Thread(target=call, daemon=True)
        t.start()
        time.sleep(0.2)
        # Valid header, body that is not JSON -> corruption mid-stream
        raw_writer.write(b"Content-Length: 5\r\n\r\nABCDE")
        raw_writer.flush()
        t.join(timeout=5)
        self.assertIsInstance(result.get("exc"), ConnectionClosed)
        pump_t.join(timeout=5)
        self.assertFalse(pump_t.is_alive())
        self.assertEqual(len(errors), 1)
        self.assertIsInstance(errors[0], ProtocolError)

    def test_dispatch_stop_pump_ends_pump_cleanly(self):
        a, b = self._pair()

        def b_dispatch(msg):
            raise StopPump()

        pump_t, errors = self._pump(b, b_dispatch)
        a.notify("quit", {})
        pump_t.join(timeout=5)
        self.assertFalse(pump_t.is_alive())
        self.assertEqual(errors, [])

    def test_unknown_id_response_is_ignored(self):
        a, b = self._pair()

        def b_dispatch(msg):
            if msg.get("method") == "echo":
                b.respond(msg["id"], {"ok": True})

        self._pump(b, b_dispatch)
        self._pump(a)
        # A stale/unsolicited response must be dropped without breaking the pump
        b.respond(999_999, {"stale": True})
        self.assertEqual(a.request("echo", timeout=5), {"ok": True})


if __name__ == "__main__":
    unittest.main()
