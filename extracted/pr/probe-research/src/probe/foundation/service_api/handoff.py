"""The SDK's one door to the Probe service (plan D9, D10): start one where none runs, then send it a
request, open files too. No local path and no quiet periods: no service means `ServiceUnavailable`,
and the caller's work waits on disk (the journal) or fails open into it. DESIGN.md (service_api)."""

from __future__ import annotations

import contextlib
import os
import socket
import sys
import threading
import time
import uuid

#: What a start waits for the new service to answer (a cold start is 0.3 to 1 s).
START_WAIT_S = 5.0
#: One request's answer, at most, unless the caller names its own (`api.call` names its own).
REQUEST_TIMEOUT_S = 30.0
#: `telemetry.send`'s answer, at most: the analytics sender's own exit flush is 3.5 s.
TELEMETRY_TIMEOUT_S = 2.0
#: The keep-alive connection, gone (the service stopped), connects again after this.
HOLD_RETRY_S = 5.0
#: The state root under the outbox root, on a home nobody can write (`prepare_state_root`).
FALLBACK_ROOT_NAME = ".probe-service"
#: An SDK's own state root beside an older machine service (C1, the D13 pattern): under the
#: state dir, else (a read-only home) under the outbox root, never the read-only fallback's name.
OWN_ROOT_NAME = "sdk-service"
OWN_FALLBACK_ROOT_NAME = ".probe-sdk-service"
#: What the SDK relies on (plan D8, D10, D20): a service whose hello lacks one is older than it.
SDK_CAPS = ("outbox.journal.v1", "sdk.relay.v1")
#: The methods an older service cannot serve as this SDK sends them: retried on its own service.
NEEDS_SDK_CAPS = frozenset({"api.call", "files.hash", "credentials.hold", "outbox.drain"})
#: A service that does not answer a request's hello within this is wedged (a live one answers in
#: milliseconds, whatever its HTTP waits on): the request costs this one budget, and this process
#: asks no service for SILENT_BACKOFF_S after (its writes wait on disk meanwhile).
HELLO_WAIT_S = 2.0
SILENT_BACKOFF_S = 30.0


class ServiceUnavailable(ConnectionError):
    """No service answered, even after a start; `outcome` is `ensure`'s (`start.Ensured`)."""

    def __init__(self, outcome: str, detail: str = "") -> None:
        super().__init__(f"the Probe service is not running here ({outcome}){': ' + detail if detail else ''}")
        self.outcome = outcome


_lock = threading.Lock()
#: The last `service.hello` answer: its `caps` and `outbox_journals`.
_hello: dict = {}
#: The keep-alive thread (`hold_open`), and whether it should run.
_holder: threading.Thread | None = None


def _reset_after_fork() -> None:
    # A lock held at a fork (a DataLoader worker) stays held in the child; the holder thread is the
    # parent's and is not running here (nor is its connection this process's to close).
    global _lock, _holder
    _lock = threading.Lock()
    _holder = None
    _held_connection.clear()


if hasattr(os, "register_at_fork"):  # POSIX only
    os.register_at_fork(after_in_child=_reset_after_fork)


def version() -> str:
    try:
        from probe.foundation.version.version import VERSION

        return str(VERSION)
    except Exception:  # noqa: BLE001
        return "unknown"


def cwd() -> str | None:
    try:
        return os.getcwd()
    except OSError:  # deleted under us: the service's default folder
        return None


def runtime_env() -> dict:
    """This process's settings as a service child needs them (`env.runtime_env_name`): where config
    and the outbox are, PROBE_* settings, proxies and CAs. Values a request cannot carry are left out.
    An empty PROBE_BASE_URL is unset, as `config.resolve` reads it."""
    from probe.foundation.service_api.env import MAX_HOOK_ENV, MAX_HOOK_ENV_VALUE, runtime_env_name

    env = {}
    for name, value in os.environ.items():
        if not runtime_env_name(name) or (name == "PROBE_BASE_URL" and not value):
            continue
        if len(value) <= MAX_HOOK_ENV_VALUE and "\0" not in value:
            env[name] = value
    return dict(sorted(env.items())[:MAX_HOOK_ENV])


def credential_env(environ=None) -> dict:
    """The Probe credentials this process holds in its environment (`env.CREDENTIAL_ENV`): they
    travel with a request over the 0600 socket and live in that child's memory only (plan D11)."""
    from probe.foundation.service_api.env import CREDENTIAL_ENV

    source = os.environ if environ is None else environ
    return {name: source[name] for name in sorted(CREDENTIAL_ENV) if source.get(name)}


def is_under_service() -> bool:
    """This process is the Probe service or one it runs (`paths.SERVICE_ROLE_ENV`): it sends its own
    HTTP and telemetry; every other process sends them through the service (plan D10)."""
    from .paths import SERVICE_ROLE_ENV

    return bool(os.environ.get(SERVICE_ROLE_ENV))


def env_credential() -> bool:
    """Whether this process's environment holds a Probe credential."""
    return bool(credential_env())


# -- starting the service ----------------------------------------------------------------


def prepare_state_root(outbox_root: str | os.PathLike | None = None) -> None:
    """Where no client can write the service's default folder (a read-only home in a container),
    the state root moves under the outbox root, which the SDK writes anyway (plan D9 task 21):
    this process's root (`paths.set_root`, never `os.environ` from a thread), which the service it
    starts gets as PROBE_SERVICE_ROOT."""
    from . import paths

    if os.environ.get(paths.SERVICE_ROOT_ENV) or paths.get_root_override():
        return
    try:
        paths.ensure_dirs()
        return
    except OSError:
        pass
    if outbox_root is None:
        from probe.sdk.delivery.journal.paths import default_root, private_fallback_root

        outbox_root = default_root()
        if not _is_writable(outbox_root):
            outbox_root = private_fallback_root()
    paths.set_root(os.path.join(str(outbox_root), FALLBACK_ROOT_NAME))


def _is_writable(folder) -> bool:
    """`folder` takes a new file (made, then removed: `os.access` and `mkdir(exist_ok)` both say
    yes on a read-only mount, M2)."""
    import tempfile

    try:
        os.makedirs(folder, mode=0o700, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=folder, prefix=".probe-write-check-"):
            return True
    except OSError:
        return False


def is_older(hello: dict) -> bool:
    """The service that answered this hello lacks what this SDK relies on (`SDK_CAPS`)."""
    caps = hello.get("caps") or []
    return not all(cap in caps for cap in SDK_CAPS)


def use_own_service() -> bool:
    """An older machine service answers here (C1): this process uses a delivery service of its own
    under its own state root (`paths.set_root`, the D13 pattern; PROBE_SERVICE_ROOT for the service
    it starts), which its next request starts. True when it switched now; False when it already
    uses one."""
    from . import paths

    with _lock:
        if _own_root:
            return False
        root = paths.state_dir() / OWN_ROOT_NAME
        if not _is_writable(root):
            from probe.sdk.delivery.journal.paths import private_fallback_root

            root = private_fallback_root() / OWN_FALLBACK_ROOT_NAME
        _own_root.append(str(root))
        paths.set_root(str(root))
    _drop_held()  # the keep-alive moves to the new service with the next request
    return True


#: The own state root this process switched to (`use_own_service`), once.
_own_root: list = []


def ensure_service(*, wait: float = START_WAIT_S, outbox_root=None) -> str:
    """Make sure a service answers here, starting one when none does: this machine's CLI install's
    machine service where there is one (H-3), else a delivery service on this interpreter (plan D9,
    D28). `start.Ensured`'s RUNNING when one answers within `wait`, else why not. Never raises."""
    from . import start

    try:
        prepare_state_root(outbox_root)
        python = sys.executable if sys.executable and os.path.isabs(sys.executable) else ""
        # Its `probe` may sit where `-I` cannot see it (`pip install --user`, PYTHONPATH), so its
        # folder goes along (H1); the API this SDK writes to is the delivery service's own (M-5).
        # Its proxies, CA files and config path too (H-2): a container behind an egress proxy, or with a
        # company CA, reaches the API through them; a fenced caller's calls use these, never its own.
        from .env import is_fence_endpoint_name

        starter = {name: value for name, value in os.environ.items() if is_fence_endpoint_name(name)}
        if _starter_api:
            starter.update({STARTER_API_ENV: _starter_api[0], "PROBE_BASE_URL": _starter_api[0]})
        return start.ensure(wait=wait, sdk_python=python, package_dir=start.get_package_dir(),
                            starter_env=starter)
    except Exception as exc:  # noqa: BLE001 -- the caller's work waits on disk
        return f"{start.Ensured.UNAVAILABLE}: {type(exc).__name__}"


_is_start_asked = False
#: The API the SDK client that started this process's service writes to (`start_soon`), once.
_starter_api: list = []
#: `relay/targets.STARTER_API_ENV`, spelled here: the delivery service may reach it for a fenced caller.
STARTER_API_ENV = "PROBE_SERVICE_STARTER_API"


def start_soon(api_base: str | None = None) -> None:
    """Start the service on a thread of its own and hold it (an SDK client's start, plan D9): its
    first drain, relay or hash then finds it up, a SIGTERM's close included. Once per process.
    `api_base`: the API this client writes to (a delivery service started for it may reach it)."""
    global _is_start_asked
    with _lock:
        if api_base and not _starter_api:
            _starter_api.append(api_base.rstrip("/"))
        if _is_start_asked:
            return
        _is_start_asked = True

    def run() -> None:
        ensure_service()
        hold_open()

    try:
        threading.Thread(target=run, name="probe-service-start", daemon=True).start()
    except RuntimeError:  # interpreter shutting down
        pass


# -- one request -----------------------------------------------------------------------


#: Until when (monotonic) no service is asked: one was silent (`HELLO_WAIT_S`).
_silent_until = 0.0
#: Closes under way in this process (`closing`): a close always asks, whatever the back-off (M-1).
_closing_count = [0]


@contextlib.contextmanager
def mark_closing():
    """A run's close: its requests ask the service even while a silent one is backed off from."""
    with _lock:
        _closing_count[0] += 1
    try:
        yield
    finally:
        with _lock:
            _closing_count[0] -= 1


def _connect(timeout: float, should_start: bool):
    """A raw connection (no hello yet), starting the service when none answers and `start`."""
    from . import service_api

    if time.monotonic() < _silent_until and not _closing_count[0]:
        raise ServiceUnavailable("silent", "it did not answer lately")

    connection = service_api.connect(min(timeout, 2.0))
    if connection is None and should_start:
        outcome = ensure_service()
        connection = service_api.connect(min(timeout, 2.0))
        if connection is None:
            raise ServiceUnavailable(outcome)
    if connection is None:
        raise ServiceUnavailable("not_started")
    connection.sock.settimeout(timeout)
    return connection


def _build_hello(is_keepalive: bool = False) -> dict:
    from .vocabularies import Client
    from .wire import API_VERSION

    parameters = {"client": Client.SDK, "client_version": version(), "api": API_VERSION}
    if is_keepalive:
        parameters["keepalive"] = True
    return parameters


def open_connection(*, timeout: float, should_start: bool = True, is_keepalive: bool = False):
    """A connection to the service with its hello done (`service_api.Connection`), starting the
    service when none answers and `start`. ServiceUnavailable when there is still none.
    `keepalive`: the service stays up while this connection is open."""
    from .wire import Method

    connection = _connect(timeout, should_start)
    try:
        _remember_hello(connection.call(Method.HELLO, _build_hello(is_keepalive)))
        _lift_silence()
    except BaseException:
        connection.close()
        raise
    return connection


def request(method: str, parameters: dict, *, timeout: float = REQUEST_TIMEOUT_S, fds=(), should_start: bool = True):
    """Send one request (with `fds`, open files the service reads) and return its result.
    ServiceUnavailable, `service_api.ServiceError` for an error answer (the hello's too), OSError
    when the connection breaks. Its hello goes in the same write. Open files cross over
    SCM_RIGHTS: the request names how many (`wire.FDS_FIELD`), the service answers `fds.ready`
    when it can take them, then they follow."""
    # SEAM(L1 transports): `transports.connect(timeout).call(method, parameters, fds=fds)` once it lands.
    from .service_api import ServiceError

    for attempt in (0, 1):
        failed = None
        with _connect(timeout, should_start) as connection:
            try:
                result = call_on(connection, method, parameters, fds=fds, should_hello=True)
            except ServiceError as exc:
                failed, result = exc, None
            hello = getattr(connection, "hello_answer", None) or {}
        # An older machine service (C1): an SDK process (M-2) whose call failed there or needs what
        # it lacks moves to a delivery service of its own, and the call goes there.
        if (attempt == 0 and _is_start_asked and is_older(hello) and (failed or method in NEEDS_SDK_CAPS)
                and use_own_service()):
            should_start = True
            continue
        if failed is not None:
            raise failed
        return result
    raise ServiceUnavailable("older")


def call_on(connection, method: str, parameters: dict, *, fds=(), should_hello: bool = False) -> object:
    """`request` on an open connection; `hello`: this connection's hello goes first, pipelined."""
    from .service_api import ServiceError
    from .wire import FDS_FIELD, FDS_READY_TOPIC, JSONRPC, Method, encode
    from .wire import request as make_request

    fds = list(fds)
    if fds:
        parameters = {**parameters, FDS_FIELD: len(fds)}
    lines = b""
    hello_id = None
    if should_hello:
        connection._next_id += 1
        hello_id = connection._next_id
        lines += encode(make_request(hello_id, Method.HELLO, _build_hello()))
    connection._next_id += 1
    id_ = connection._next_id
    connection.sock.sendall(lines + encode(make_request(id_, method, parameters)))
    pending = bool(fds)
    wait = connection.sock.gettimeout()
    if hello_id is not None:
        connection.sock.settimeout(HELLO_WAIT_S if wait is None else min(wait, HELLO_WAIT_S))
    while True:
        try:
            message = connection._read_message()
        except TimeoutError:
            if hello_id is not None:
                _mark_silent()
                raise ServiceUnavailable("silent", f"no answer to its hello in {HELLO_WAIT_S:g}s") from None
            raise
        if message.get("method") == "event" and "id" not in message:
            event = message.get("params") or {}
            if pending and event.get("topic") == FDS_READY_TOPIC and event.get("id") == id_:
                socket.send_fds(connection.sock, [b"\0"], fds)
                pending = False
            continue
        if message.get("jsonrpc") != JSONRPC or message.get("id") not in (id_, hello_id):
            continue
        if "error" in message:
            error_body = message["error"] or {}
            raise ServiceError(int(error_body.get("code", 0)), str(error_body.get("message", "")), error_body.get("data"))
        if message.get("id") == hello_id:
            connection.hello_answer = message.get("result")
            _remember_hello(connection.hello_answer)
            _lift_silence()
            hello_id = None
            connection.sock.settimeout(wait)
            continue
        return message.get("result")


def _mark_silent() -> None:
    global _silent_until
    _silent_until = time.monotonic() + SILENT_BACKOFF_S


def _lift_silence() -> None:
    """A hello was answered: the back-off ends at once (M-1)."""
    global _silent_until
    _silent_until = 0.0


def _remember_hello(answer: object) -> None:
    with _lock:
        _hello.clear()
        if isinstance(answer, dict):
            _hello.update(answer)


def hello_answer() -> dict:
    """The last `service.hello` answer this process had (empty before its first request)."""
    with _lock:
        return dict(_hello)


def is_fate_shared() -> bool:
    """The service this process last spoke to goes when this job goes (H2), on real evidence only
    (M-4): this process runs in a job that ends all its processes (a container, a pod, a Slurm job),
    and the service is its own (a delivery service this SDK started inside it) or shares its cgroup
    (or, in a container, its pid namespace). A desktop terminal's processes share a cgroup too: no
    evidence there. Linux reads /proc. Never raises."""
    try:
        if not _is_in_ending_job():
            return False
        hello = hello_answer()
        if hello.get("role") == "delivery":
            return True
        pid = hello.get("pid")
        if not isinstance(pid, int) or not os.path.isdir(f"/proc/{pid}"):
            return False
        with open("/proc/self/cgroup", encoding="utf-8") as mine, open(f"/proc/{pid}/cgroup", encoding="utf-8") as its:
            if mine.read() == its.read():
                return True
        return _is_in_container() and os.stat("/proc/self/ns/pid").st_ino == os.stat(f"/proc/{pid}/ns/pid").st_ino
    except (OSError, ValueError):
        return False


#: A cgroup path of a job that ends every process in it: a container runtime's, a pod's, a Slurm job's.
JOB_CGROUP_WORDS = ("docker", "containerd", "libpod", "kubepods", "crio", "slurm")


def _is_in_ending_job() -> bool:
    """Does this process run where the end of the job ends every process: a container, a pod, or a
    Slurm job (its environment, or a job's cgroup)?"""
    if _is_in_container() or os.environ.get("SLURM_JOB_ID"):
        return True
    try:
        with open("/proc/self/cgroup", encoding="utf-8") as handle:
            text = handle.read()
    except OSError:
        return False
    return any(word in text for word in JOB_CGROUP_WORDS)


def _is_in_container() -> bool:
    return (os.path.exists("/.dockerenv") or os.path.exists("/run/.containerenv")
            or bool(os.environ.get("KUBERNETES_SERVICE_HOST")) or bool(os.environ.get("container")))


def get_start_id() -> str | None:
    """Which start of the service the last hello came from (`pid` and `started_at`): a key it
    held in memory is gone once this changes (M5)."""
    hello = hello_answer()
    if not hello.get("pid"):
        return None
    return f"{hello.get('pid')}@{hello.get('started_at')}"


# -- holding the service open ----------------------------------------------------------


def hold_open() -> None:
    """Keep the service up while this process lives (a keep-alive connection, plan D9): a delivery
    service idles out 5 s after its last client, and the next request would pay its start again.
    Idempotent; a thread of its own, which connects again when the service restarts (the next
    request starts one that stopped) and lets go when the service's folder changes or on `release`."""
    global _holder, _held_folder
    from . import paths

    with _lock:
        if _holder is not None and _holder.is_alive() and _held_folder == str(paths.service_dir()):
            return
        _held_folder = str(paths.service_dir())
        _release.clear()
        _holder = threading.Thread(target=_hold, args=(_held_folder,), name="probe-service-hold", daemon=True)
        try:
            _holder.start()
        except RuntimeError:  # interpreter shutting down: nothing to hold
            _holder = None


def release() -> None:
    """Let the held service go (tests; a process that is done with Probe)."""
    _release.set()
    _drop_held()


def _drop_held() -> None:
    """Close the keep-alive connection; its thread, blocked reading it, wakes (a `shutdown`: a bare
    `close` from another thread does not wake a `recv`) and lets go when the folder changed."""
    with _lock:
        connection = _held_connection.pop("connection", None)
    if connection is not None:
        with contextlib.suppress(OSError):
            connection.sock.shutdown(socket.SHUT_RDWR)
        connection.close()


_release = threading.Event()
_held_folder = ""
_held_connection: dict = {}


def _hold(folder: str) -> None:
    from . import paths, service_api

    while not _release.is_set() and str(paths.service_dir()) == folder:
        try:
            with open_connection(timeout=START_WAIT_S, should_start=False, is_keepalive=True) as connection:
                with _lock:
                    _held_connection["connection"] = connection
                connection.sock.settimeout(None)
                while not _release.is_set() and connection.sock.recv(65536):
                    pass  # events: none subscribed; EOF when the service stops
        except (OSError, ValueError, service_api.ServiceError):
            pass
        finally:
            with _lock:
                _held_connection.pop("connection", None)
        _release.wait(HOLD_RETRY_S)


# -- telemetry -----------------------------------------------------------------------


def stamp(entries: list) -> list:
    """Give each telemetry entry a `uuid` of its own (kept if present): PostHog collapses events
    sharing one, so a batch resent after a lost answer counts once."""
    for entry in entries:
        if isinstance(entry, dict):
            entry.setdefault("uuid", str(uuid.uuid4()))
    return entries


def telemetry(entries: list) -> bool:
    """Hand one batch of telemetry entries this process built to the service (`telemetry.send`, plan
    D10: the only way a client sends it). True when it took them; False drops the batch. One resend
    under the same id when the first answer was lost. Only a process whose SDK started the service
    (`start_soon`) starts it for telemetry; the CLI's never does (M6). Never raises."""
    try:
        from probe.foundation.service_api.env import MAX_TELEMETRY_ENTRIES
        from probe.foundation.service_api.wire import Method

        if not entries or len(entries) > MAX_TELEMETRY_ENTRIES:
            return False
        parameters = {"entries": stamp(entries), "id": uuid.uuid4().hex}
        for attempt in range(2):
            try:
                answer = request(Method.TELEMETRY_SEND, parameters, timeout=TELEMETRY_TIMEOUT_S,
                                 should_start=_is_start_asked)
                return isinstance(answer, dict) and answer.get("accepted") is True
            except ServiceUnavailable:
                return False
            except OSError:
                if attempt:
                    return False
        return False
    except Exception:  # noqa: BLE001 -- observability must never become observable
        return False

