"""The iOS web surface: reaching a WKWebView's DOM over ios_webkit_debug_proxy.

The iOS sibling of `_web.py`, and deliberately a thin one. Everything above the
wire is shared: the DOM walk is JavaScript, `is_visible` asks the page, and the
placement/calibration maths never learns which platform it ran on. What differs
is only how a page is reached and how a message is addressed.

Three differences from the Android channel, each measured on a device rather than
read from a spec:

**Messages are Target-multiplexed.** A plain ``Runtime.evaluate`` on an iwdp page
socket is refused outright — ``"'Runtime' domain was not found"``. The connection
carries no domains of its own; it announces its targets with ``Target.targetCreated``
(``page-6``, ``frame-4294967297``) and every command must be wrapped in
``Target.sendMessageToTarget`` and read back out of ``Target.dispatchMessageFromTarget``.

**A throw is reported as ``wasThrown``**, not CDP's ``exceptionDetails``. It is
translated here so the shared ``evaluate`` keeps its one way of noticing.

**A target carries no ``type``.** Android filters ``/json`` down to ``type ==
"page"`` because a socket also advertises service workers; iwdp lists pages only,
and the field is simply absent — filtering on it would drop everything.

**A simulator is reached differently from a device, and only at the attach.** A
device answers over usbmux, which is what ``-c <udid>:<port>`` addresses. A
simulator has no usbmux: it publishes the same service on a unix socket
(``com.apple.webinspectord_sim.socket``, under a launchd directory whose name is
new on every boot), reached with ``-s unix:<socket>``. Two consequences, both
measured: the simulator attaches under the literal pseudo-id ``SIMULATOR``, which
``-c``'s grammar cannot name — it only matches hex-and-dash udids — so its port
cannot be pinned and is read back from the device listing instead; and its
command line carries no udid, so a stale proxy is identified by its socket.

Everything above the attach is shared with the device path, because the protocol
is the same one: the page list, the Target envelope, and ``appId: "PID:…"``
ownership are identical on both.

What is the same is what matters: an in-app WKWebView is listed alongside Safari
and tagged with its owning process (``appId: "PID:1729"``), which is the iOS
counterpart of Android's ``webview_devtools_remote_<pid>``, and it answers
``document.visibilityState`` — the primitive page selection is built on.
"""

import json
import logging
import shutil
import subprocess
import time
import urllib.request

from testmu_appium._helpers import _web

_log = logging.getLogger("testmu_appium")

#: How long to wait for a freshly spawned proxy to answer /json.
_PROXY_READY_TIMEOUT_S = 15.0
_PROXY_POLL_S = 0.5

#: How long a connection is given to announce its targets. They arrive as soon as
#: the socket opens; this is the ceiling for a page that has gone away, not the
#: expected wait.
_TARGET_ANNOUNCE_S = 3.0

#: Spawn attempts before giving up. A spawn can lose its kernel-assigned port
#: in the instant between the free-port probe releasing it and iwdp binding it;
#: each retry asks the kernel for a fresh one, so consecutive losses take a
#: machine allocating ports faster than we can spawn a process.
_SPAWN_ATTEMPTS = 3

#: What a simulator calls itself in iwdp's device listing. Not a udid — the
#: literal string — which is exactly why `-c` cannot name it.
_SIM_DEVICE_ID = "SIMULATOR"

#: How wide a page-port range to offer the simulator spawn. iwdp assigns from
#: the range and skips what is already bound, so this is headroom against a
#: neighbour rather than a count of anything we use: one port is ever served.
_SIM_PORT_SPAN = 9

#: How long to let a freshly spawned proxy finish enumerating pages before
#: handing its port back. A proxy answers /json before its page list is
#: populated, and a caller that reads targets in that window sees an empty
#: surface and concludes the channel is dead rather than not-listed-yet.
#:
#: The window is real on BOTH targets, which is why this is not scoped to one:
#: polled at 100ms over three spawns each, a simulator published its first page
#: at 0.57s / 0.00s / 0.00s and an iPhone 11 on iOS 26.5.2 at 0.10s / 0.11s /
#: 0.10s. The ceiling is ~5x the worst of those, because the two mistakes are
#: not symmetric: too low marks a live surface permanently unreachable, while
#: too high is only ever paid by a target that genuinely has nothing open —
#: which returns its empty list one grace period later, honestly.
_PAGE_GRACE_S = 3.0


class _State:
    """Per-session proxy state. Reset between runs by ``reset()``."""

    port: int | None = None
    process: subprocess.Popen | None = None
    unreachable: bool = False
    remembered: str = ""
    #: The simulator's webinspectord socket, once resolved — "" on a real
    #: device, and the flag that says which attach this session is using.
    #: Cached because resolving it reads the process table, and the answer
    #: cannot change while the session's simulator stays booted.
    sim_socket: str = ""
    #: The pid of the app on screen, stashed by the foreground-identity read
    #: (``mobile: activeAppInfo`` reports it beside the bundle id). It is what
    #: keeps target selection from probing — or adopting — Safari's pages while
    #: gestures target the app under test. 0 means "never learned", which keeps
    #: the pre-ownership behaviour for a caller that never resolved foreground.
    foreground_pid: int = 0


_state = _State()


def note_foreground(pid: int) -> None:
    """Record which process owns the screen, for target ownership below.

    A CHANGED pid also forgets the remembered target: the page that proved
    visible belonged to the app that has just left the foreground, and
    revalidating it against the new owner is this one line.
    """
    pid = int(pid or 0)
    if pid and pid != _state.foreground_pid and _state.foreground_pid:
        _state.remembered = ""
    if pid:
        _state.foreground_pid = pid


def reset() -> None:
    """Give back what reading the device claimed.

    The proxy is a child process holding the device's inspector connection —
    usbmux on a device, the webinspectord socket on a simulator; leaving it
    running outlives the session that started it and blocks the next one from
    binding the port.
    """
    if _state.process is not None and _state.process.poll() is None:
        _state.process.terminate()
        try:
            _state.process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            _state.process.kill()
    _state.process = None
    _state.port = None
    _state.unreachable = False
    _state.remembered = ""
    _state.foreground_pid = 0
    _state.sim_socket = ""


def _json(port: int, path: str = "/json", timeout: float = 8.0, host: str = "127.0.0.1"):
    with urllib.request.urlopen(f"http://{host}:{port}{path}", timeout=timeout) as r:
        return json.loads(r.read())


def _free_port() -> int:
    """A port the kernel just guaranteed free — the same answer adb's `tcp:0`
    gets, asked one step earlier because iwdp must be told its port up front."""
    import socket  # noqa: PLC0415

    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return probe.getsockname()[1]


def _sim_socket_for(udid: str, kind: str = "") -> str:
    """This simulator's webinspectord socket, or ``""`` for a real device.

    ``kind`` is the session's ``target_kind`` and is AUTHORITATIVE where it is
    set: the caller resolved it from real discovery, so a ``physical`` target
    returns immediately without reading the process table. Only an unset kind
    makes this function decide for itself, which is what keeps a standalone
    generated test — where nobody passes one — correct.

    Deciding for itself never reads the SHAPE of the udid. A simulator is a
    device that publishes this socket, so the lookup that finds the socket we
    need is also the answer to which attach to use, and a real device (which
    publishes none) falls through to the usbmux path untouched.

    The mapping is indirect because the socket's own path says nothing about
    whose it is: the launchd directory holding it is named randomly at boot. Its
    OWNER does say — every booted simulator has a ``launchd_sim`` whose
    environment points at ``CoreSimulator/Devices/<udid>``. So: sockets from
    ``lsof``, owner from the pid, udid from the owner's environment.

    An unnamed session never decides for itself, even when exactly one simulator
    is booted. A socket cannot be tied to a session without a udid to match it
    against, and attaching to a simulator while gestures drive a plugged-in
    phone is the same failure ``reachable()`` already refuses for a cloud run:
    reading a different device than the session drives. Xcode leaves simulators
    booted long after anyone stopped using them, so "one is booted" is no
    evidence at all about what this session holds.
    """
    if _state.sim_socket:
        return _state.sim_socket
    if kind and kind != "simulator":
        # Told what this is, and it is not a simulator. Re-deriving it here could
        # only produce a contradiction with no principled winner.
        return ""
    try:
        listing = subprocess.run(  # noqa: S603 — fixed executable, no shell
            ["lsof", "-aUc", "launchd_sim"],
            capture_output=True, text=True, timeout=10).stdout
    except Exception:  # noqa: BLE001 — no lsof, or no simulators: not a simulator
        return ""

    owners: dict[str, str] = {}
    for line in listing.splitlines():
        if "webinspectord_sim.socket" not in line:
            continue
        fields = line.split()
        if len(fields) >= 2 and fields[1].isdigit():
            owners.setdefault(fields[-1], fields[1])
    if not owners:
        return ""
    if not udid:
        _log.info("[web] %d booted simulator(s) publish a web inspector socket, but "
                  "this session names no device; reading the simulator could attach "
                  "to something the session does not drive, so the device path is "
                  "used — configure(udid=...) to inspect a simulator", len(owners))
        return ""

    for socket_path, pid in owners.items():
        try:
            env = subprocess.run(  # noqa: S603 — fixed executable, no shell
                ["ps", "eww", "-p", pid],
                capture_output=True, text=True, timeout=10).stdout
        except Exception:  # noqa: BLE001 — the simulator went away mid-read
            continue
        if f"CoreSimulator/Devices/{udid}/" in env:
            _state.sim_socket = socket_path
            return socket_path
    return ""


def _sim_page_port(listing) -> int | None:
    """The port iwdp assigned the simulator, read out of its device listing.

    The one thing the device path gets for free and this one cannot: ``-c``
    matches a udid, and a simulator's id is the word ``SIMULATOR``, so the port
    is chosen by iwdp and reported rather than requested. Any physical device
    plugged into the same Mac is listed here too, which is why the entry is
    selected by id instead of position.
    """
    for entry in listing or []:
        if str(entry.get("deviceId") or "") != _SIM_DEVICE_ID:
            continue
        _, _, tail = str(entry.get("url") or "").rpartition(":")
        if tail.isdigit():
            return int(tail)
    return None


def _await_pages(port: int) -> None:
    """Give a freshly spawned proxy time to publish its page list.

    Returning the moment the port answers is too early: it is bound but empty
    for a beat afterwards, and a caller that reads targets right then treats the
    surface as dead rather than as not-listed-yet. Waiting for the first page
    closes that window without inventing a readiness contract — an empty list
    after the grace period is returned as it is, because a target with nothing
    open genuinely has no pages.

    This is not a simulator quirk. It was found on a simulator, where the extra
    device-listing hop makes the window wider, and then measured on a device
    too: 0 pages on attach and 1 at 2.5s, three spawns out of three.
    """
    deadline = time.time() + _PAGE_GRACE_S
    while time.time() < deadline:
        try:
            if _json(port):
                return
        except Exception:  # noqa: BLE001 — the port is bound but not serving yet
            pass
        time.sleep(_PROXY_POLL_S)


def _kill_stale_proxies(udid: str, sim_socket: str = "") -> None:
    """Kill leftover iwdp processes serving THIS device.

    The iOS step Android does not need: a leaked adb forward is inert, but the
    device's webinspectord tolerates ONE proxy connection per device — an
    orphan from a killed session can hold it and starve the fresh spawn. A
    device is single-tenant, so any existing proxy for our udid belongs to a
    dead session by definition. Other devices' proxies are untouched; with no
    udid to name (single-device dev flow) any iwdp on this host is ours to
    clear for the same reason.

    A simulator is matched on its socket rather than its udid, because the udid
    never appears on a simulator spawn's command line — the socket path does,
    and it identifies that simulator exactly. Matching on the udid there would
    silently clear nothing and let the orphan keep the slot.
    """
    if sim_socket:
        pattern = f"ios_webkit_debug_proxy.*{sim_socket}"
    elif udid:
        pattern = f"ios_webkit_debug_proxy.*{udid}"
    else:
        pattern = "ios_webkit_debug_proxy"
    result = subprocess.run(  # noqa: S603 — fixed executable, no shell
        ["pkill", "-f", pattern], capture_output=True, text=True)
    if result.returncode == 0:
        _log.info("[web] cleared a stale ios_webkit_debug_proxy for %s",
                  sim_socket or udid or "this host")


def ensure_proxy(udid: str = "", port: int | None = None) -> int:
    """The port this session's own ios_webkit_debug_proxy answers on.

    Always OUR proxy on a kernel-assigned free port — never an adoption:
    something already listening is either an unknown process (not ours to
    trust) or a dead session's orphan (killed below, because webinspectord
    serves one proxy per device). One host running many devices in parallel
    needs no coordination — every session asks the kernel, exactly as
    Android's `adb forward tcp:0` does.

    An explicit ``port`` is honoured for a caller that owns its allocation.
    """
    if _state.port is not None:
        # A cached port is only an answer while OUR proxy is alive behind it —
        # an iwdp that died mid-run would otherwise be "served" for the rest
        # of the session as a port nothing listens on.
        if _state.process is None or _state.process.poll() is None:
            return _state.port
        _log.info("[web] the session's ios_webkit_debug_proxy died; respawning")
        _state.port = None
        _state.process = None

    from testmu_appium import _config  # noqa: PLC0415
    binary = str(_config.get("iwdp_binary") or "") or shutil.which(
        "ios_webkit_debug_proxy")
    if not binary:
        raise RuntimeError(
            "ios_webkit_debug_proxy is not installed; the iOS web surface cannot "
            "be reached without it (brew install ios-webkit-debug-proxy, or "
            "configure(iwdp_binary=...) with its path)")

    kind = str(_config.get("target_kind") or "").lower()
    sim_socket = _sim_socket_for(udid, kind)
    if kind == "simulator" and not sim_socket:
        # The caller named a simulator, so falling through to the usbmux path
        # would spend 15s and then blame the wrong thing entirely ("is the
        # device connected and trusted?"). Say what is actually wrong.
        raise RuntimeError(
            f"no booted simulator publishes a web inspector socket for "
            f"{udid or 'this session'}; is it still booted "
            f"(xcrun simctl list devices booted)?")
    _kill_stale_proxies(udid, sim_socket)

    last_error = "no spawn attempted"
    for _ in range(_SPAWN_ATTEMPTS):
        if sim_socket:
            # The simulator cannot be told which port to serve pages on, so it
            # is given a listing port — which it CAN be told — and a range to
            # choose from, and the choice is read back below.
            asked = int(port) if port else _free_port()
            low = _free_port()
            args = [binary, "-s", f"unix:{sim_socket}",
                    "-c", f"null:{asked},:{low}-{low + _SIM_PORT_SPAN}"]
        else:
            asked = int(port) if port else _free_port()
            args = [binary, "-c", f"{udid}:{asked}" if udid else f"null:{asked}"]
        _state.process = subprocess.Popen(
            args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        deadline = time.time() + _PROXY_READY_TIMEOUT_S
        while time.time() < deadline:
            try:
                answer = _json(asked)
                # A device serves its pages on the port it was given; a
                # simulator serves a device listing there and names the page
                # port inside it. An answering listing that does not yet name
                # the simulator is a proxy that has bound its port but not
                # finished attaching — indistinguishable from "not answering
                # yet", and treated as such.
                serving = _sim_page_port(answer) if sim_socket else asked
                if serving is None:
                    raise RuntimeError("the simulator has not attached yet")
                _await_pages(serving)
                _state.port = serving
                _log.info("[web] ios_webkit_debug_proxy serving %s on %d",
                          udid or ("the simulator" if sim_socket else "the device"),
                          serving)
                return serving
            except Exception:  # noqa: BLE001 — not answering yet
                if _state.process.poll() is not None:
                    # Lost the port race, or the device is not reachable. A
                    # fresh kernel port distinguishes the two: a race never
                    # loses twice to the same neighbour, a dead device fails
                    # every attempt the same way.
                    last_error = (
                        "ios_webkit_debug_proxy exited immediately; is the "
                        "simulator still booted?"
                        if sim_socket else
                        "ios_webkit_debug_proxy exited immediately; is the "
                        "device connected, unlocked and trusted, with Safari > "
                        "Advanced > Web Inspector enabled?")
                    break
                time.sleep(_PROXY_POLL_S)
        else:
            # Spawned but never answered. The child is still RUNNING and
            # holding the device's single webinspectord slot — leaving it
            # alive both leaks it and starves every retry, so it is torn down
            # before the next attempt rather than after the session.
            last_error = (
                f"ios_webkit_debug_proxy did not list the simulator on {asked} "
                f"within {_PROXY_READY_TIMEOUT_S:.0f}s; is Web Inspector enabled "
                f"on it (Settings > Safari > Advanced)?"
                if sim_socket else
                f"ios_webkit_debug_proxy did not answer on {asked} within "
                f"{_PROXY_READY_TIMEOUT_S:.0f}s")
            _state.process.terminate()
            try:
                _state.process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                _state.process.kill()
            _state.process = None
        if port:
            break  # an owned port that failed is the caller's to re-allocate
    raise RuntimeError(last_error)


def list_targets(port: int, host: str = "127.0.0.1"):
    """Inspectable pages on the device, owned by the foreground app when known.

    ``host`` is where the proxy answers: this machine for a proxy spawned here,
    the device host when the Mobile Binary spawned it (see _web_remote).

    No ``type`` filter, unlike the Android reader: iwdp lists pages only and its
    entries carry no ``type`` field at all, so filtering on it drops everything.

    Ownership IS filtered, because one proxy serves every inspectable page on
    the device: without it Safari or another app's page can win the visibility
    probe — or exhaust the probe budget — while gestures target the app under
    test. The filter only bites when both sides can speak: a foreground pid was
    learned AND the entries carry parseable pids. When the owner has no pages,
    an empty list is the honest answer, not somebody else's pages.
    """
    targets = [t for t in _json(port, host=host) if t.get("webSocketDebuggerUrl")]
    owner = _state.foreground_pid
    if not owner:
        return targets
    attributed = [t for t in targets if pid_of_target(t) is not None]
    if not attributed:
        return targets
    return [t for t in attributed if pid_of_target(t) == owner]


def _js_cookie(cookie: dict) -> str:
    """One cookie as a ``document.cookie`` assignment string.

    The same construction Appium's driver uses on this platform (its
    ``createJSCookie``): value URI-encoded, ``path`` defaulted to ``/`` because
    Safari does not reliably update a cookie without one, epoch ``expires``
    rendered as an HTTP date. ``url`` scoping from the CDP contract collapses
    to the page the write runs in — which is the visible page, the only one
    the caller could mean.
    """
    from email.utils import formatdate  # noqa: PLC0415
    from urllib.parse import quote  # noqa: PLC0415

    parts = [f"{cookie['name']}={quote(str(cookie.get('value', '')), safe='')}"]
    parts.append(f"path={cookie.get('path') or '/'}")
    if cookie.get("domain"):
        parts.append(f"domain={cookie['domain']}")
    expires = cookie.get("expires")
    if isinstance(expires, (int, float)) and expires > 0:
        parts.append(f"expires={formatdate(expires, usegmt=True)}")
    if cookie.get("sameSite"):
        parts.append(f"SameSite={cookie['sameSite']}")
    if cookie.get("secure"):
        parts.append("secure")
    return "; ".join(parts)


def pid_of_target(target) -> int | None:
    """The process a page belongs to, from ``appId: "PID:1729"``.

    The iOS counterpart of reading a pid out of ``webview_devtools_remote_<pid>``:
    it is what says an in-app WebView belongs to the app under test rather than
    to Safari or another app.
    """
    raw = str(target.get("appId") or "")
    _, _, digits = raw.partition("PID:")
    return int(digits) if digits.isdigit() else None


class IosChannel(_web.Channel):
    """One connection to one iwdp page, speaking the Target envelope.

    Subclasses the shared channel and overrides the wire — plus the one place
    where the two debuggers are not the same protocol at all. `evaluate`,
    `is_visible` and `read_page` are JavaScript run in the page and are identical
    on both platforms; cross-origin frame RECOVERY is not, because it is made of
    protocol methods rather than script (see `unreachable_frames`).
    """

    def unreachable_frames(self, page, seen=()):
        """None are recoverable here, and saying so is cheaper than finding out.

        The shared implementation asks for `Page.getFrameTree` and then reads the
        frame through `Page.createIsolatedWorld`. Both are **Chrome DevTools
        Protocol**; a WebKit target answers `-32601 method was not found`, which
        travels back as an exception on every capture of any page carrying a
        cross-origin iframe — an ad slot, a Cloudflare challenge, an embedded
        map. Measured on iplocation.net that cost 12–19 s per perception, twice
        per capture, and took the whole surface down with it.

        So the honest answer for this protocol is "no frames were recovered".
        The walk's own `blockedFrames` count still reports that something was
        unread, which is the part a caller can act on. Recovering them needs
        WebKit's own vocabulary (`Page.getResourceTree`, and an execution context
        obtained some other way, since WebKit has no isolated worlds) — a real
        feature, not a translation of these two calls.
        """
        return []

    #: This channel does not speak raw Chrome DevTools RPC. Verbs whose method
    #: vocabulary is Chrome-only (cookies, history navigation) check this
    #: rather than discovering it as a -32601 mid-action.
    cdp_rpc = False

    def call(self, method, params=None):
        self._id += 1
        message_id = self._id
        connection = self._ws.create_connection(
            self._ws_url, timeout=self._timeout, suppress_origin=_web._SUPPRESS_ORIGIN)
        try:
            target_id = self._await_target(connection)
            self._send_to_target(connection, target_id, message_id, method, params)
            return self._await_reply(connection, message_id, method)
        finally:
            connection.close()

    def call_function(self, function_declaration, arguments=()):
        """Invoke a page function with structured arguments, Target-wrapped.

        The shared implementation opens a connection and sends RAW
        ``Runtime.evaluate`` / ``Runtime.callFunctionOn`` — which this socket
        refuses outright (see the module docstring). Same two RPCs, same single
        connection (the ``objectId`` is scoped to it), each wrapped in the
        Target envelope the page actually answers. Without this override,
        every value-carrying storage verb failed on iOS while plain
        ``evaluate`` worked.
        """
        connection = self._ws.create_connection(
            self._ws_url, timeout=self._timeout, suppress_origin=_web._SUPPRESS_ORIGIN)
        try:
            target_id = self._await_target(connection)

            self._id += 1
            evaluate_id = self._id
            self._send_to_target(
                connection, target_id, evaluate_id, "Runtime.evaluate",
                {"expression": "globalThis", "returnByValue": False})
            evaluated = self._await_reply(connection, evaluate_id, "Runtime.evaluate")
            object_id = evaluated.get("result", {}).get("objectId")
            if not object_id:
                raise RuntimeError(
                    "Runtime.evaluate: visible page returned no global object")

            self._id += 1
            call_id = self._id
            self._send_to_target(
                connection, target_id, call_id, "Runtime.callFunctionOn", {
                    "functionDeclaration": function_declaration,
                    "objectId": object_id,
                    "arguments": [{"value": value} for value in arguments],
                    "returnByValue": True,
                    "awaitPromise": True,
                })
            called = self._await_reply(connection, call_id, "Runtime.callFunctionOn")
            if called.get("exceptionDetails"):
                raise RuntimeError(
                    "Runtime.callFunctionOn: page function raised an exception")
            return called.get("result", {}).get("value")
        finally:
            connection.close()

    def _send_to_target(self, connection, target_id, message_id, method, params):
        connection.send(json.dumps({
            "id": message_id,
            "method": "Target.sendMessageToTarget",
            "params": {
                "targetId": target_id,
                "message": json.dumps(
                    {"id": message_id, "method": method, "params": params or {}}),
            },
        }))

    # ── page state: cookies and history, in WebKit's vocabulary ─────────
    #
    # The same verbs the Chrome channel serves with Network/Storage methods.
    # Every route here is the one Appium's own remote debugger uses on this
    # wire — Page.getCookies / Page.deleteCookie on the protocol, and a
    # document.cookie write for setting, which is why an httpOnly write is
    # refused rather than silently not sticking: no JavaScript can create one.

    def get_cookies(self) -> list:
        return self.call("Page.getCookies").get("cookies", [])

    def set_cookies(self, params: list) -> None:
        for cookie in params:
            if cookie.get("httpOnly"):
                raise ValueError(
                    f"cookie {cookie.get('name')!r} asks for httpOnly, which a "
                    "WebKit page cannot grant: cookies are written through "
                    "document.cookie here, and script-created cookies are never "
                    "httpOnly. Set it server-side or through execute_api.")
            self.evaluate(f"document.cookie = {json.dumps(_js_cookie(cookie))}")
        # A document.cookie write can be silently refused — a domain the page
        # does not own, a __Host- name off its rules, SameSite=None without
        # Secure. Chrome's wire call reports; this one must read back and say
        # which names did not stick, or "set N cookie(s)" is a claim, not a
        # fact.
        jar = str(self.evaluate("document.cookie") or "")
        missing = [str(c.get("name")) for c in params
                   if f"{c.get('name')}=" not in jar]
        if missing:
            _log.warning("[web] the page refused cookie(s) %s — the write ran "
                         "but the browser's own rules dropped them", missing)

    def delete_cookie(self, cookie: dict) -> None:
        """``Page.deleteCookie`` addresses a cookie by name AND the url it lives
        on, so the url is rebuilt from the enumerated cookie's own scope."""
        domain = str(cookie.get("domain") or "").lstrip(".")
        scheme = "https" if cookie.get("secure") else "http"
        self.call("Page.deleteCookie", {
            "cookieName": cookie["name"],
            "url": f"{scheme}://{domain}{cookie.get('path') or '/'}",
        })

    def clear_cookies(self) -> None:
        """No ``clearBrowserCookies`` counterpart exists: enumerate and delete."""
        for cookie in self.get_cookies():
            self.delete_cookie(cookie)

    def navigate_history(self, delta: int) -> bool:
        """Ask the PAGE to move — WebKit has no getNavigationHistory to consult.

        Always reports the move as attempted: without an index to read, "did it
        move" is unanswerable here, and at a history boundary the page's own
        ``history.back()`` is a no-op — the same outcome Chrome's False
        describes, reached without the report.
        """
        self.evaluate("history.back()" if delta < 0 else "history.forward()")
        return True

    def _await_target(self, connection):
        """The page target this connection announced.

        A connection carries no domains of its own — it exists to route to the
        targets it names. The page target is preferred over the frame ones: a
        frame target answers too, but the page is the whole document and its id
        survives an in-page navigation.
        """
        announced = []
        deadline = time.time() + _TARGET_ANNOUNCE_S
        while time.time() < deadline:
            try:
                message = json.loads(connection.recv())
            except Exception:  # noqa: BLE001 — silence means it announced all it has
                break
            if message.get("method") == "Target.targetCreated":
                info = message["params"]["targetInfo"]
                announced.append((info.get("targetId"), info.get("type")))
                if info.get("type") == "page":
                    return info["targetId"]
        if not announced:
            raise RuntimeError(
                "the page socket announced no target; it is a stale entry in "
                "/json rather than a live page")
        return announced[0][0]

    def _await_reply(self, connection, message_id, method):
        while True:
            message = json.loads(connection.recv())
            if message.get("method") != "Target.dispatchMessageFromTarget":
                continue
            inner = json.loads(message["params"]["message"])
            if inner.get("id") != message_id:
                continue
            if "error" in inner:
                raise RuntimeError(f"{method}: {inner['error']}")
            result = inner.get("result", {})
            # WebKit reports a throw as a sibling boolean where CDP reports a
            # structured exceptionDetails. Translated so the shared `evaluate`
            # keeps one way of noticing, and does not read a throw as an empty
            # page.
            if result.get("wasThrown"):
                result = dict(result)
                result["exceptionDetails"] = {
                    "text": "the page script threw",
                    "exception": result.get("result", {}),
                }
            return result


class IwdpWebDebugTransport:
    """Provider boundary implementation for a device reached over iwdp.

    Deliberately shaped like the local-adb provider so `_action_web` cannot tell
    them apart. Where the two genuinely differ, the iOS side degenerates rather
    than pretends: there is ONE endpoint for the whole device, so a "socket" is
    that endpoint and there is no per-app forwarding to do.
    """

    def __init__(self, udid: str = "", port: int | None = None):
        self._udid = udid
        self._port = port

    # ── provider identity ───────────────────────────────────────────────
    def capabilities(self):
        return {
            "contract_version": 1,
            "provider": "ios-iwdp",
            "cdp_rpc": False,   # Target-wrapped WebKit, not raw CDP
            "session_bound": False,
        }

    # ── reachability ────────────────────────────────────────────────────
    def reachable(self):
        if _state.unreachable:
            return False
        # A cloud session's device is not on this host's usbmux: an iwdp spawned
        # here would serve whatever LOCAL device happens to be plugged in, and
        # web inspection would attach to it while Appium gestures target the
        # cloud device. A cloud run wants a session-bound provider registered in
        # its place; until one is, "no web surface" is the true answer.
        from testmu_appium import _config  # noqa: PLC0415
        if _config.run_target != "local":
            self.mark_unreachable(
                "run_target is not local; a locally spawned ios_webkit_debug_proxy "
                "would read a different device than the session drives")
            return False
        try:
            ensure_proxy(self._udid, self._port)
            return True
        except Exception as e:  # noqa: BLE001
            self.mark_unreachable(e)
            return False

    def mark_unreachable(self, cause):
        if not _state.unreachable:
            _log.info("[web] the device's debug channel is unreachable: %s", cause)
        _state.unreachable = True

    # ── target memory ───────────────────────────────────────────────────
    def remember_target(self, target_id):
        _state.remembered = target_id or ""

    def remembered_target(self):
        return _state.remembered

    # ── discovery ───────────────────────────────────────────────────────
    def sockets(self):
        """One endpoint for the whole device.

        Android publishes a debug socket per app process, so it enumerates and
        filters them. iwdp multiplexes every inspectable page onto one port, so
        there is exactly one to return — the per-app question is answered on the
        TARGET instead, via its pid.
        """
        return [_web.Socket(name=f"iwdp:{self._port}", pid=None, kind="webview")]

    def pids_of(self, package):
        """No socket-level pid filter on iOS.

        Returning None rather than an empty set is load-bearing: `_scan_targets`
        reads a non-None value as "the foreground app owns these sockets and no
        others", and would report a missing socket for a device that has one.
        Ownership is decided per target here, and visibility does the rest.
        """
        return None

    def forward(self, socket):
        return ensure_proxy(self._udid, self._port)

    def list_targets(self, port):
        return list_targets(port)

    def channel(self, ws_url):
        return IosChannel(ws_url)

    # ── liveness bookkeeping ────────────────────────────────────────────
    def is_dead(self, socket):
        # One endpoint, and its health IS the transport's health, which
        # `reachable()` already answers. A per-socket death would mean the whole
        # provider is down.
        return False

    def mark_dead(self, socket, cause):
        self.mark_unreachable(cause)

    def mark_no_socket(self, package):
        # Unreachable here: pids_of returns None, so `_scan_targets` never
        # concludes the foreground app owns no socket.
        _log.debug("[web] no debug socket for %s", package)
