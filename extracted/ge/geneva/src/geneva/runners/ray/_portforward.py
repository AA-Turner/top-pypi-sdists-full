# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# A simple port forwarder for talking to ray head
# this is for testing only, and should NEVER be used in production

import logging
import select
import socket
import threading
import time
from collections.abc import Callable
from contextlib import suppress

import attrs
import kubernetes
import kubernetes.stream.ws_client
from typing_extensions import Self

from geneva.runners.ray.raycluster import RayCluster

_LOG = logging.getLogger(__name__)


@attrs.define
class _Flag:
    val: bool
    lock: threading.Lock = attrs.field(factory=threading.Lock, init=False)

    @classmethod
    def true(cls) -> Self:
        return cls(True)

    def __bool__(self) -> bool:
        with self.lock:
            return self.val

    def set(self, val: bool) -> None:
        with self.lock:
            self.val = val


@attrs.define
class PortForward:
    """
    A simple port forwarder for talking to a k8s pod

    This forwarder binds and listens on a local port. Any traffic
    sent to this port is forwarded to the specified pod and port.

    Note: when local_port is 0, a random port will be allocated by the OS
    and the local port will be set to that value. User is responsible
    for checking the local port value after the forwarder is started.
    """

    port: int
    core_api: kubernetes.client.CoreV1Api
    pod_resolver: Callable[[], tuple[str | None, str | None]]

    local_port: int = 0
    alive: _Flag = attrs.field(factory=_Flag.true, init=False)
    threads: list[threading.Thread] = attrs.field(factory=list, init=False)
    proxy_start_barrier: threading.Barrier = attrs.field(init=False)
    proxy_listener: socket.socket = attrs.field(init=False)

    @classmethod
    def to_head_node(
        cls,
        cluster: RayCluster,
    ) -> Self:
        # the head pod can get head reset and renamed, so we need to get updated info
        def resolve() -> tuple[str, str]:
            pod = cluster.head_node_pod  # always re-reads current head
            return pod.metadata.name, cluster.namespace

        return cls(
            port=10001,
            core_api=cluster.clients.core_api,
            pod_resolver=resolve,
        )

    @classmethod
    def to_ui(
        cls,
        cluster: RayCluster,
    ) -> Self:
        def resolve() -> tuple[str | None, str | None]:
            pod = cluster.ui_pod
            if not pod:
                return None, None
            return pod.metadata.name, cluster.namespace

        return cls(
            port=3000,
            core_api=cluster.clients.core_api,
            pod_resolver=resolve,
        )

    def _start_proxy(
        self,
        pod_socket: socket.socket,
        client_socket: socket.socket,
    ) -> None:
        _LOG.debug("Starting proxy from pod to client")
        # Enable TCP keepalive to reduce idle-time drops on long-lived tunnels
        self._tune_socket(pod_socket)
        self._tune_socket(client_socket)
        proxy_thread = threading.Thread(
            target=_proxy,
            args=(pod_socket, client_socket, self.alive),
            daemon=True,
        )
        self.threads.append(proxy_thread)
        proxy_thread.start()

        _LOG.debug("Proxy started")

    def _connect_pod_socket(
        self, *, attempts: int = 12, sleep_s: float = 2.5
    ) -> socket.socket:
        last_err = None
        for _ in range(attempts):
            if not self.alive:
                raise RuntimeError("forwarder stopping")
            try:
                pod_name, ns = self.pod_resolver()
                if not pod_name or not ns:
                    continue

                pf: kubernetes.stream.ws_client.PortForward = (
                    kubernetes.stream.portforward(
                        self.core_api.connect_get_namespaced_pod_portforward,
                        pod_name,
                        ns,
                        ports=f"{self.port}",
                    )
                )
                s = pf.socket(self.port)
                s.setblocking(True)
                return s
            except Exception as e:  # NotFound / Gone / transient
                _LOG.debug(f"failed to resolve pod for port forwarding: {e}")
                last_err = e
                time.sleep(sleep_s)
        if last_err is not None:
            raise last_err
        else:
            raise RuntimeError("Connection failed with no exception recorded")

    def _start_listener_loop(self) -> None:
        _LOG.debug("Starting listener loop")
        proxy_listener = self._create_listener()
        self.proxy_start_barrier.wait()

        while self.alive:
            try:
                client_socket, _ = proxy_listener.accept()
            except TimeoutError:
                continue
            except OSError:
                if self.alive:
                    _LOG.warning("Listener socket error; restarting listener")
                    # Attempt to re-bind a fresh listener while still alive
                    with suppress(Exception):
                        proxy_listener.close()
                    proxy_listener = self._create_listener()
                    continue
                else:
                    _LOG.info("Listener socket closed")
                    break

            try:
                pod_socket = self._connect_pod_socket()
            except Exception as e:
                _LOG.exception(
                    "Failed to connect to head pod port; dropping client: %r", e
                )
                with suppress(Exception):
                    client_socket.close()
                continue

            self._start_proxy(pod_socket, client_socket)

    def __enter__(self) -> Self:
        _LOG.debug("Starting port forward")
        self.alive.set(True)
        self.proxy_start_barrier = threading.Barrier(2)
        listener_thread = threading.Thread(
            target=self._start_listener_loop, daemon=True
        )
        self.threads.append(listener_thread)
        listener_thread.start()
        self.proxy_start_barrier.wait()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        _LOG.debug("Stopping port forward")
        self.alive.set(False)

        # not a clean shutdown, but we don't care
        try:
            self.proxy_listener.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            # socket may have been closed by the head pod terminating
            _LOG.debug(f"error stopping portforward: {e}")

        for thread in self.threads:
            thread.join(timeout=2)

        self.threads.clear()
        _LOG.debug("Port forward stopped")

    def _create_listener(self) -> socket.socket:
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind(("127.0.0.1", self.local_port))
        if self.local_port == 0:
            self.local_port = listener.getsockname()[1]
        listener.listen()
        listener.settimeout(1.0)  # so we can check self.alive
        self.proxy_listener = listener
        return listener

    def _tune_socket(self, s: socket.socket) -> None:
        with suppress(Exception):
            s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        # Platform-specific TCP keepalive tuning (best effort)
        # Linux
        tcp_keepidle = getattr(socket, "TCP_KEEPIDLE", None)
        tcp_keepintvl = getattr(socket, "TCP_KEEPINTVL", None)
        tcp_keepcnt = getattr(socket, "TCP_KEEPCNT", None)
        if tcp_keepidle is not None:
            with suppress(Exception):
                s.setsockopt(socket.IPPROTO_TCP, tcp_keepidle, 30)
        if tcp_keepintvl is not None:
            with suppress(Exception):
                s.setsockopt(socket.IPPROTO_TCP, tcp_keepintvl, 10)
        if tcp_keepcnt is not None:
            with suppress(Exception):
                s.setsockopt(socket.IPPROTO_TCP, tcp_keepcnt, 3)


def _format_sock(sock: socket.socket) -> str:
    """Return a short from "host:port" to "host:port" description, or fallback to
    type name."""
    try:
        laddr = sock.getsockname()
        raddr = sock.getpeername()
        return f"{laddr[0]}:{laddr[1]} <-> {raddr[0]}:{raddr[1]}"
    except Exception:
        return f"<{type(sock).__name__}>"


def _proxy(
    s1: socket.socket,
    s2: socket.socket,
    alive: _Flag | None = None,  # fix B008: no function calls in defaults
    *,
    buffer_size: int = 4096,
) -> None:
    if alive is None:
        alive = _Flag.true()  # safe to call at runtime

    _LOG.debug(f"Proxying between {_format_sock(s1)} and {_format_sock(s2)}")
    sockets = (s1, s2)

    try:
        # PERF203: put try/except around the whole iteration, not inside the for-loop
        while alive:
            r, _, _ = select.select(sockets, [], [], 1.0)
            if not r:
                continue

            for s in r:
                data = s.recv(buffer_size)
                if not data:  # peer closed
                    return
                dest = s2 if s is s1 else s1
                dest.sendall(data)

    except (ConnectionResetError, BrokenPipeError, OSError):
        # peer vanished; just exit quietly
        return
    finally:
        for s in sockets:
            with suppress(Exception):
                s.shutdown(socket.SHUT_RDWR)
            with suppress(Exception):
                s.close()
