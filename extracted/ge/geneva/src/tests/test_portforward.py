# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
import itertools
import socket
from collections.abc import Callable
from contextlib import suppress
from types import SimpleNamespace

import geneva.runners.ray._portforward as pf  # this actually uses ray module


def _core_api() -> SimpleNamespace:
    return SimpleNamespace(connect_get_namespaced_pod_portforward=object())


def changing_resolver_with_recording(prefix="pod") -> Callable[[], tuple[str, str]]:
    counter = itertools.count(1)
    seen = []

    def _resolver() -> tuple[str, str]:
        name = f"{prefix}-{next(counter)}"
        seen.append(name)
        return name, "namespace"

    _resolver.seen = seen
    return _resolver


class _DummyPF:
    def __init__(self, sock: socket.socket) -> None:
        self._sock = sock

    def socket(self, port: int) -> socket.socket:
        return self._sock


def test_connect_pod_socket_handles_pod_rename_then_succeeds(monkeypatch) -> None:
    """
    _connect_pod_socket:
      - resolver returns a different pod name on each call
      - first portforward call fails (old pod), second succeeds (new pod)
    """
    pod_sock, proxy_side = socket.socketpair()
    resolver = changing_resolver_with_recording()

    calls = {"n": 0}
    seen_pod_args: list[str] = []

    def flappy_portforward(connect_fn, pod_name, ns, **kwargs) -> _DummyPF:
        seen_pod_args.append(pod_name)
        calls["n"] += 1
        if calls["n"] == 1:
            raise BrokenPipeError("old head vanished")
        return _DummyPF(proxy_side)

    # Patch low-levels only
    monkeypatch.setattr(pf.kubernetes.stream, "portforward", flappy_portforward)
    monkeypatch.setattr(pf.time, "sleep", lambda s: None)  # keep retry tight

    fwd = pf.PortForward(port=10001, core_api=_core_api(), pod_resolver=resolver)

    s = fwd._connect_pod_socket(attempts=2, sleep_s=0.0)
    try:
        assert isinstance(s, socket.socket)
        # ensure resolver advanced and portforward saw the two different names
        assert resolver.seen == ["pod-1", "pod-2"]
        assert seen_pod_args == ["pod-1", "pod-2"]
    finally:
        with suppress(Exception):
            s.close()
        with suppress(Exception):
            pod_sock.close()
        with suppress(Exception):
            proxy_side.close()


def test_listener_end_to_end_after_pod_rename(monkeypatch) -> None:
    """
    Full listener path:
      - first resolver value 'pod-1' -> portforward raises (head restarted)
      - second resolver value 'pod-2' -> portforward succeeds
      - client connects once; _connect_pod_socket retries inside and then proxy works
    """
    pod_sock, proxy_side = socket.socketpair()
    resolver = changing_resolver_with_recording()

    seen_pod_args: list[str] = []
    attempts = itertools.count(1)

    def flappy_portforward(connect_fn, pod_name, ns, **kwargs) -> _DummyPF:
        seen_pod_args.append(pod_name)
        # fail on first call only, succeed thereafter
        if next(attempts) == 1:
            raise BrokenPipeError("transient during rename")
        return _DummyPF(proxy_side)

    monkeypatch.setattr(pf.kubernetes.stream, "portforward", flappy_portforward)
    monkeypatch.setattr(pf.time, "sleep", lambda s: None)

    fwd = pf.PortForward(port=10001, core_api=_core_api(), pod_resolver=resolver)
    with fwd:
        # Single client connect triggers _connect_pod_socket's internal retry
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.settimeout(1.0)
        c.connect(("127.0.0.1", fwd.local_port))

        # Send bytes; they should arrive at pod_sock once retry succeeds
        c.sendall(b"hi")
        got = pod_sock.recv(2)  # blocks if proxy never came up
        assert got == b"hi"

        c.close()

    # Assertions about resolver progression and what portforward saw
    # Expect exactly two resolver calls: pod-1 (fail), pod-2 (success)
    assert resolver.seen[:2] == ["pod-1", "pod-2"]
    assert seen_pod_args[:2] == ["pod-1", "pod-2"]

    with suppress(Exception):
        pod_sock.close()
    with suppress(Exception):
        proxy_side.close()
