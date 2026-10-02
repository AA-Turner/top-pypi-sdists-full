"""The web debug channel for a device on a LambdaTest host, via the Mobile Binary.

On a cloud run the device is on somebody else's host: there is no adb here to
forward a devtools socket with, and no usbmuxd for ios_webkit_debug_proxy to
speak to. That host runs the Mobile Binary, the per-device agent whose
``POST /v1.0/startdevtools`` already does both for AppLive's DevTools: on
Android it forwards the app's ``webview_devtools_remote_<pid>`` socket onto a
host port (``devtoolsPort``); on iOS it spawns ios_webkit_debug_proxy for the
device and reports the port mapped to it (``iwdpPort``). The host is reachable
from the runner over ``HOST_IP``, which the hub writes into ``rd-details.env``
beside ``MOBILE_BINARY_PORT``.

Two providers, one per platform, shaped like the local ones so ``_action_web``
cannot tell them apart. What the local providers do with a subprocess these do
with one HTTP call to the Mobile Binary, and every loopback address in the
answers is rewritten to the host, because the ports live there.
"""
import json
import logging
import os
import urllib.parse
import urllib.request

from testmu_appium import _config
from testmu_appium._helpers import _web
from testmu_appium._helpers._rd import rd_details

_log = logging.getLogger("testmu_appium")

#: One startdevtools call does an adb forward plus a page listing on Android,
#: and on iOS spawns ios_webkit_debug_proxy and waits for it to answer /json.
_START_TIMEOUT_S = 60.0

#: Listing pages on a forwarded port, same budget as the local reader.
_LIST_TIMEOUT_S = 8.0

_LOOPBACK = {"", "localhost", "127.0.0.1", "::1", "0.0.0.0"}


class _State:
    unreachable: bool = False
    #: (platform key) → the endpoint startdevtools handed back, so a session
    #: pays the forward once — the Mobile Binary keeps one devtools forward at a
    #: time and re-forwards on every call.
    endpoints: dict = {}
    dead: set = set()
    #: (HOST_IP, MOBILE_BINARY_PORT) once resolved; the file does not change
    #: within a session and reachable() is asked on every perception.
    host_port: tuple = ()


_state = _State()


def reset() -> None:
    _state.unreachable = False
    _state.endpoints = {}
    _state.dead = set()
    _state.host_port = ()


def host_port() -> tuple[str, str]:
    """(HOST_IP, MOBILE_BINARY_PORT), env first, then rd-details.env."""
    if _state.host_port:
        return _state.host_port
    details = rd_details()
    host = os.getenv("HOST_IP", "").strip() or details.get("HOST_IP", "")
    port = os.getenv("MOBILE_BINARY_PORT", "").strip() or details.get("MOBILE_BINARY_PORT", "")
    if host and port:
        _state.host_port = (host, port)
    return host, port


def available() -> bool:
    """Whether this session's device has a Mobile Binary to reach for.

    Only a cloud session does — a local run drives a device on this machine
    and forwards its own sockets — and only when the hub wrote the host's
    address for it. Without both, the local providers keep the answer.
    """
    if _config.run_target != "cloud":
        return False
    host, port = host_port()
    return bool(host and port)


def rewrite_host(url: str, host: str, port: int | None = None) -> str:
    """``url`` with a loopback (or absent) host replaced by ``host``.

    A devtools listing names its pages as the host saw them —
    ``ws://127.0.0.1:<port>/devtools/page/<id>``, or ``ws:///devtools/page/<id>``
    with no authority at all — and that loopback is the Mobile Binary's, not
    ours. The URL's own port is kept; ``port`` fills in when it names none.
    """
    parts = urllib.parse.urlsplit(url)
    if parts.hostname not in _LOOPBACK and parts.hostname is not None:
        return url
    chosen = parts.port or port
    netloc = f"{host}:{chosen}" if chosen else host
    return urllib.parse.urlunsplit((parts.scheme, netloc, parts.path, parts.query, parts.fragment))


def _post_json(url: str, payload: dict, timeout: float) -> dict:
    body = json.dumps(payload).encode()
    request = urllib.request.Request(
        url, data=body, method="POST", headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310 — device-host API
        return json.loads(response.read() or b"{}")


def _get_json(url: str, timeout: float):
    with urllib.request.urlopen(url, timeout=timeout) as response:  # noqa: S310 — device-host API
        return json.loads(response.read())


def start_devtools(*, os_name: str, bundle_id: str = "", device_id: str = "") -> dict:
    """Ask the Mobile Binary to publish the device's debug channel; its answer."""
    host, port = host_port()
    payload: dict = {"os": os_name}
    if bundle_id:
        payload["bundleId"] = bundle_id
    if device_id:
        payload["deviceId"] = device_id
    response = _post_json(f"http://{host}:{port}/v1.0/startdevtools", payload, _START_TIMEOUT_S)
    if response.get("status") != "Success":
        raise RuntimeError(
            f"startdevtools refused: {response.get('error') or response.get('status') or response}")
    return response


def _device_udid() -> str:
    """The device's udid: configured, else what the live session negotiated."""
    configured = str(_config.get("udid") or "")
    if configured:
        return configured
    from testmu_appium._helpers.driver import get_driver  # noqa: PLC0415 — avoid a module cycle

    driver = get_driver()
    caps = getattr(driver, "capabilities", None) or {}
    for key in ("udid", "appium:udid", "deviceUDID", "appium:deviceUDID"):
        if caps.get(key):
            return str(caps[key])
    return ""


def _port_of(url: str) -> int | None:
    try:
        return urllib.parse.urlsplit(url).port
    except ValueError:
        return None


class _RemoteTransport:
    """What the two platforms share: reachability, liveness, host rewriting."""

    provider = "mobile-binary"

    def capabilities(self):
        return {
            "contract_version": 1,
            "provider": self.provider,
            "cdp_rpc": self.cdp_rpc,
            "session_bound": True,
        }

    def reachable(self):
        return not _state.unreachable and available()

    def mark_unreachable(self, cause):
        if not _state.unreachable:
            _log.info("[web] the device host's debug channel is unreachable (%s); the "
                      "accessibility projection serves web content for the rest of this "
                      "session", cause)
        _state.unreachable = True

    def is_dead(self, socket):
        return socket.name in _state.dead

    def mark_dead(self, socket, cause):
        _state.dead.add(socket.name)
        _log.info("[web] %s did not answer (%s); skipping it for the rest of this session",
                  socket.name, cause)

    def mark_no_socket(self, package):
        _web.mark_no_socket(package)

    def list_targets(self, endpoint):
        host, port = endpoint
        targets = self._list(host, port)
        for target in targets:
            target["webSocketDebuggerUrl"] = rewrite_host(
                target["webSocketDebuggerUrl"], host, port)
        return targets


class RemoteAndroidWebDebugTransport(_RemoteTransport):
    """An Android device's WebView, forwarded by the Mobile Binary on its host.

    The Mobile Binary resolves the socket itself (``pidof <package>`` →
    ``webview_devtools_remote_<pid>``), so there is no socket enumeration
    here: one synthetic socket stands for "the foreground app's WebView", and
    the package it names is learned from ``pids_of``, which ``_action_web``
    calls with the foreground app before it forwards anything.
    """

    provider = "mobile-binary-adb"
    cdp_rpc = True

    def __init__(self):
        self._package = ""

    def remembered_target(self):
        return _web.remembered_target()

    def remembered_target_for(self, package):
        return _web.remembered_target(package)

    def remember_target(self, ws_url):
        _web.remember_target(ws_url)

    def remember_target_for(self, package, ws_url):
        _web.remember_target(ws_url, package)

    def channel(self, ws_url):
        return _web.Channel(ws_url)

    def sockets(self):
        return [_web.Socket(name=f"mobile-binary:webview:{self._package}", pid=None, kind="webview")]

    def pids_of(self, package):
        # No pid filter: the Mobile Binary attributes the socket to the package
        # itself. None, not an empty set — `_scan_targets` reads a non-None value
        # as "the foreground app owns these sockets and no others".
        self._package = package or ""
        return None

    def forward(self, socket):
        key = ("android", self._package)
        endpoint = _state.endpoints.get(key)
        if endpoint:
            return endpoint
        host, _ = host_port()
        answer = start_devtools(os_name="android", bundle_id=self._package)
        # The host port the socket was forwarded to: reported as devtoolsPort,
        # and also named by every page (ws://localhost:<port>/devtools/page/<id>)
        # — the pages serve a Mobile Binary that predates the field.
        port = answer.get("devtoolsPort")
        if not port:
            for page in answer.get("pages") or []:
                port = _port_of(str(page.get("webSocketDebuggerUrl") or ""))
                if port:
                    break
        if not port:
            raise RuntimeError("startdevtools reported no devtools port for the forward")
        endpoint = (host, int(port))
        _state.endpoints[key] = endpoint
        _log.info("[web] %s webview forwarded on the device host at %s:%d",
                  self._package or "foreground app", host, int(port))
        return endpoint

    def _list(self, host, port):
        raw = _get_json(f"http://{host}:{port}/json", _LIST_TIMEOUT_S)
        return [t for t in raw
                if t.get("type") == "page" and t.get("webSocketDebuggerUrl")]


class RemoteIosWebDebugTransport(_RemoteTransport):
    """An iOS device's pages, over the ios_webkit_debug_proxy the Mobile Binary
    spawned on its host. One endpoint for the whole device, exactly as the
    local iwdp provider; the per-app question is answered per target."""

    provider = "mobile-binary-iwdp"
    cdp_rpc = False  # Target-wrapped WebKit, not raw CDP

    def remembered_target(self):
        from testmu_appium._helpers import _web_ios  # noqa: PLC0415
        return _web_ios._state.remembered

    def remembered_target_for(self, package):
        return self.remembered_target()

    def remember_target(self, ws_url):
        from testmu_appium._helpers import _web_ios  # noqa: PLC0415
        _web_ios._state.remembered = ws_url or ""

    def remember_target_for(self, package, ws_url):
        self.remember_target(ws_url)

    def channel(self, ws_url):
        from testmu_appium._helpers._web_ios import IosChannel  # noqa: PLC0415
        return IosChannel(ws_url)

    def sockets(self):
        return [_web.Socket(name="mobile-binary:iwdp", pid=None, kind="webview")]

    def pids_of(self, package):
        return None

    def forward(self, socket):
        key = ("ios", "")
        endpoint = _state.endpoints.get(key)
        if endpoint:
            return endpoint
        host, _ = host_port()
        answer = start_devtools(os_name="ios", device_id=_device_udid())
        # iwdp serves THIS device's pages on the port it mapped to the udid;
        # the pages in the answer point at the CDP adapter layered on top,
        # which the WebKit-protocol reader here does not speak.
        port = answer.get("iwdpPort")
        if not port:
            raise RuntimeError(
                "startdevtools did not report the ios_webkit_debug_proxy page port; "
                "the device host's Mobile Binary predates the iwdpPort field")
        endpoint = (host, int(port))
        _state.endpoints[key] = endpoint
        _log.info("[web] ios_webkit_debug_proxy serving the device on %s:%d", host, int(port))
        return endpoint

    def _list(self, host, port):
        from testmu_appium._helpers import _web_ios  # noqa: PLC0415
        return _web_ios.list_targets(port, host=host)

    def is_dead(self, socket):
        # One endpoint; its health is the transport's, which reachable() answers.
        return False

    def mark_dead(self, socket, cause):
        self.mark_unreachable(cause)

    def mark_no_socket(self, package):
        _log.debug("[web] no debug socket for %s", package)


def transport_for(platform: str):
    if platform == "android":
        return RemoteAndroidWebDebugTransport()
    if platform == "ios":
        return RemoteIosWebDebugTransport()
    return None
