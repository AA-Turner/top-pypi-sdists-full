"""The API the containers talk to: the suite's fake by default, a real server on request.

FAKE (default): ``tests.conftest.FakeApp`` served on a UNIX socket, relayed into the
container network as ``https://api`` (TLS with a throwaway CA) and ``http://r2.test``
(the fake's presigned and multipart upload host).

REAL: set all three of ``PROBE_BASE_URL``, ``PROBE_TOKEN`` and ``PROBE_E2E_PROJECT``.
The containers then talk to that server directly (or through the test's proxy), and
every read below goes through the public API. ``PROBE_E2E_PROJECT`` is required on
purpose: a developer's shell that merely has a login exported must not send these
tests to production.

The values are read at IMPORT, before the suite's autouse fixtures isolate HOME and
config for each test.
"""

from __future__ import annotations

import math
import subprocess
import threading
import time
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import os

REAL_BASE_URL = os.environ.get("PROBE_BASE_URL", "").strip()
REAL_TOKEN = os.environ.get("PROBE_TOKEN", "").strip()
REAL_PROJECT = os.environ.get("PROBE_E2E_PROJECT", "").strip()

#: Where the relay container finds the fake's socket and its TLS material.
RELAY_MOUNT = "/relay"
#: Where workload containers find the CA that signed the relay's certificate.
CA_MOUNT = "/etc/probe-envtest/ca.pem"
FAKE_URL = "https://api"
FAKE_TOKEN = "ros_pat_deadbeef"
FAKE_PROJECT = "envtest"


def real_mode() -> bool:
    return bool(REAL_PROJECT)


def real_mode_problem() -> str | None:
    if real_mode() and not (REAL_BASE_URL and REAL_TOKEN):
        return "PROBE_E2E_PROJECT is set but PROBE_BASE_URL or PROBE_TOKEN is not"
    return None


def make_ca(directory: Path) -> None:
    """A throwaway CA and a server certificate for ``api`` and ``r2.test``."""
    d = str(directory)
    cmds = [
        ["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "2",
         "-keyout", f"{d}/ca.key", "-out", f"{d}/ca.pem", "-subj", "/CN=probe-envtest-ca"],
        ["openssl", "req", "-newkey", "rsa:2048", "-nodes", "-keyout", f"{d}/server.key",
         "-out", f"{d}/server.csr", "-subj", "/CN=api"],
    ]
    for cmd in cmds:
        subprocess.run(cmd, check=True, capture_output=True, timeout=60)
    (directory / "san.ext").write_text(
        "subjectAltName=DNS:api,DNS:r2.test\nbasicConstraints=CA:FALSE\n"
        "keyUsage=digitalSignature,keyEncipherment\nextendedKeyUsage=serverAuth\n"
    )
    subprocess.run(
        ["openssl", "x509", "-req", "-in", f"{d}/server.csr", "-CA", f"{d}/ca.pem",
         "-CAkey", f"{d}/ca.key", "-CAcreateserial", "-days", "2", "-out", f"{d}/server.pem",
         "-extfile", f"{d}/san.ext"],
        check=True, capture_output=True, timeout=60,
    )
    for name in ("server.key", "ca.key"):
        os.chmod(directory / name, 0o600)


@dataclass
class Point:
    step: int
    key: str
    value: float


def _flatten_expected(rows: list[dict]) -> dict[tuple[int, str], float]:
    return {(int(r["step"]), str(r["key"])): float(r["value"]) for r in rows}


@dataclass
class Reconciliation:
    """Every logged (step, key, value) against what the server holds."""

    expected: int
    missing: list[tuple[int, str]] = field(default_factory=list)
    wrong_value: list[tuple[int, str, float, float]] = field(default_factory=list)
    duplicated: list[tuple[int, str, int]] = field(default_factory=list)
    unexpected: list[tuple[int, str]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not (self.missing or self.wrong_value or self.duplicated)

    def summary(self) -> str:
        return (
            f"expected={self.expected} missing={len(self.missing)} "
            f"wrong_value={len(self.wrong_value)} duplicated={len(self.duplicated)} "
            f"unexpected={len(self.unexpected)}"
            + (f" first_missing={self.missing[:5]}" if self.missing else "")
            + (f" first_wrong={self.wrong_value[:3]}" if self.wrong_value else "")
            + (f" first_dup={self.duplicated[:5]}" if self.duplicated else "")
        )


class Backend:
    """What a test needs from the server, identical in both modes except where a
    method says the fake can show more (raw deliveries) than a real server can."""

    kind: str
    url: str
    token: str
    project: str

    def container_env(self) -> dict[str, str]:
        env = {"PROBE_BASE_URL": self.url, "PROBE_TOKEN": self.token}
        return env

    def container_volumes(self) -> list[str]:
        return []

    # -- reads -------------------------------------------------------------
    def client(self):
        raise NotImplementedError

    def run(self, run_id: str) -> dict:
        return self.client().get_run(run_id)

    def writers(self, run_id: str) -> list[dict]:
        return self.client().list_writers(run_id)

    def artifacts(self, run_id: str) -> list[dict]:
        page = self.client().list_run_artifacts(run_id)
        items = getattr(page, "items", page)
        return list(items or [])

    def points(self, run_id: str) -> list[Point]:
        raise NotImplementedError

    def request_summary(self) -> str:
        return "(a real server: no request log)"

    def raw_deliveries(self, run_id: str) -> Counter | None:
        """(step, key) -> how many times it was POSTed. Fake only: a real server
        stores each point once however often it arrives, so it cannot show this."""
        return None

    def wait_status(self, run_id: str, want: set[str], timeout: float) -> str | None:
        deadline = time.monotonic() + timeout
        status = None
        while time.monotonic() < deadline:
            status = self.run(run_id).get("status")
            if status in want:
                return status
            time.sleep(2)
        return status

    def reconcile(self, run_id: str, logged: list[dict], *, wait: float = 120.0,
                  keys: set[str] | None = None) -> Reconciliation:
        """Wait up to ``wait`` for every logged point, then compare by (step, key, value)."""
        expected = _flatten_expected(logged)
        deadline = time.monotonic() + wait
        while True:
            got = self.points(run_id)
            have = {(p.step, p.key) for p in got}
            if set(expected) <= have or time.monotonic() > deadline:
                break
            time.sleep(3)
        result = Reconciliation(expected=len(expected))
        stored: dict[tuple[int, str], list[float]] = {}
        for p in got:
            if keys is not None and p.key not in keys:
                continue
            stored.setdefault((p.step, p.key), []).append(p.value)
        for ident, value in expected.items():
            values = stored.get(ident)
            if not values:
                result.missing.append(ident)
            elif not any(math.isclose(v, value, rel_tol=1e-6, abs_tol=1e-9) for v in values):
                result.wrong_value.append((*ident, value, values[0]))
        for ident, values in stored.items():
            if len(values) > 1:
                result.duplicated.append((*ident, len(values)))
            if ident not in expected:
                result.unexpected.append(ident)
        return result


def _wall_clock_stamp():
    """A stamp function for the fake: now, in UTC, distinct and increasing per call
    (the fixed-clock stamp's guarantee), in the same `...Z` form."""
    from datetime import datetime, timedelta

    from probe._compat import UTC

    last = [datetime.min.replace(tzinfo=UTC)]
    guard = threading.Lock()

    def stamp() -> str:
        with guard:
            now = max(datetime.now(UTC), last[0] + timedelta(microseconds=1))
            last[0] = now
        return now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    return stamp


class FakeBackend(Backend):
    kind = "fake"

    def __init__(self, workdir: Path):
        from tests.conftest import FakeApp

        self.url = FAKE_URL
        self.token = FAKE_TOKEN
        self.project = FAKE_PROJECT
        self.app = FakeApp()
        # Mirror what production declares (2.8 leases, M1 multipart); the class
        # defaults keep both off for the unit suite's older-server tests.
        self.app.supports_leases = True
        self.app.supports_artifact_multipart = True
        # And the server's clock: the unit suite's fake stamps a fixed July date,
        # which a real SDK reads against wall-clock time -- a requeued job then
        # sees its own run's `crashed` as "ended months ago" and refuses to
        # reopen it (client._older_than_reopen_window).
        self.app._stamp = _wall_clock_stamp()
        self.lock = threading.Lock()
        self.relay_dir = workdir / "relay"
        self.relay_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
        make_ca(self.relay_dir)
        self.socket = self.relay_dir / "fake.sock"
        self._client = None
        self._server = None
        self._lease_clock = None

    # The fake's own state is plain dicts; the socket server's threads and this
    # process's reads share one lock.
    def handler(self, request):
        with self.lock:
            return self.app.handler(request)

    def start(self) -> None:
        from .fakeserver import serve_unix

        self._server = serve_unix(self, self.socket)
        self._server.__enter__()
        self.client().ensure_project(self.project)

    def stop(self) -> None:
        if self._lease_clock is not None:
            self._lease_clock.stop()
        if self._server is not None:
            self._server.__exit__(None, None, None)
            self._server = None

    def relay_volumes(self) -> list[str]:
        return [f"{self.relay_dir}:{RELAY_MOUNT}"]

    def container_env(self) -> dict[str, str]:
        return {**super().container_env(), "SSL_CERT_FILE": CA_MOUNT}

    def container_volumes(self) -> list[str]:
        return [f"{self.relay_dir / 'ca.pem'}:{CA_MOUNT}:ro"]

    def client(self):
        if self._client is None:
            import httpx

            from probe.sdk import Client
            from probe.sdk.config import Settings
            from probe.sdk.journal import Journal
            from probe.sdk.transport import Transport
            import tempfile

            settings = Settings(base_url="http://test", token=FAKE_TOKEN)
            http = httpx.Client(base_url="http://test", transport=httpx.MockTransport(self.handler))
            self._client = Client(
                settings=settings,
                transport=Transport(settings, client=http),
                journal=Journal(tempfile.mkdtemp(prefix="envtest-host-journal-"),
                                context={"name": None, "base_url": "http://test"}),
            )
        return self._client

    def _run_key(self, run_id: str) -> list[str]:
        row = self.app.runs.get(run_id) or {}
        return [k for k in {run_id, row.get("slug")} if k]

    def points(self, run_id: str) -> list[Point]:
        with self.lock:
            rows = [r for k in self._run_key(run_id) for r in self.app.metric_points_posted.get(k, [])]
        out = []
        for r in rows:
            if r.get("step_index") is None or r.get("value") is None:
                continue
            out.append(Point(int(r["step_index"]), str(r["key"]), float(r["value"])))
        return out

    def raw_deliveries(self, run_id: str) -> Counter:
        return Counter((p.step, p.key) for p in self.points(run_id))

    def requests(self) -> list:
        with self.lock:
            return list(self.app.requests)

    def request_summary(self) -> str:
        """Method + path shape -> count, for a failure message."""
        import re as _re

        counts = Counter(
            f"{r.method} {_re.sub(r'[0-9a-f-]{32,36}|/[0-9]+(?=/|$)', '<id>', r.url.path)}"
            for r in self.requests()
        )
        return "\n".join(f"{n:5d} {k}" for k, n in sorted(counts.items()))

    def age_leases(self, expiry_seconds: float) -> "LeaseClock":
        """Give the fake the server's lease clock: a lease unheard for
        ``expiry_seconds`` is marked expired and closure is re-evaluated, as the
        server derives it (`lease_state_sql`). The fake otherwise treats every
        unreleased lease as live forever."""
        self._lease_clock = LeaseClock(self, expiry_seconds)
        self._lease_clock.start()
        return self._lease_clock


class LeaseClock:
    def __init__(self, backend: FakeBackend, expiry: float):
        self.backend = backend
        self.expiry = expiry
        self._stop = threading.Event()
        self._seen: dict[tuple[str, str], tuple[int, float]] = {}
        self.expired: list[tuple[str, str, float]] = []
        self._thread = threading.Thread(target=self._loop, daemon=True)

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()

    def _loop(self) -> None:
        while not self._stop.wait(1.0):
            now = time.monotonic()
            with self.backend.lock:
                app = self.backend.app
                for rid, leases in app.leases.items():
                    for session, lease in leases.items():
                        beats = int(lease.get("beats") or 0)
                        prev = self._seen.get((rid, session))
                        if prev is None or prev[0] != beats:
                            self._seen[(rid, session)] = (beats, now)
                            continue
                        live = not lease.get("released_at") and not lease.get("gone_at")
                        if live and not lease.get("expired") and now - prev[1] >= self.expiry:
                            lease["expired"] = True
                            self.expired.append((rid, session, now))
                            app._close_by_leases(rid, allow_crashed=False)


class RealBackend(Backend):
    kind = "real"

    def __init__(self):
        self.url = REAL_BASE_URL
        self.token = REAL_TOKEN
        self.project = REAL_PROJECT
        self._client = None

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def relay_volumes(self) -> list[str]:
        return []

    def client(self):
        if self._client is None:
            from probe.sdk import Client
            from probe.sdk.config import Settings
            from probe.sdk.transport import Transport

            settings = Settings(base_url=REAL_BASE_URL, token=REAL_TOKEN)
            self._client = Client(settings=settings, transport=Transport(settings))
        return self._client

    def points(self, run_id: str) -> list[Point]:
        out = []
        for p in self.client().export_metric_points(run_id, limit=5000):
            if p.get("step_index") is None or p.get("value") is None:
                continue
            out.append(Point(int(p["step_index"]), str(p["key"]), float(p["value"])))
        return out


def make_backend(workdir: Path) -> Backend:
    return RealBackend() if real_mode() else FakeBackend(workdir)
