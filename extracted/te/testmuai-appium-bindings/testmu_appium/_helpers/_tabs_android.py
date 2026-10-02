"""Android Chrome tab provider over the browser DevTools endpoint."""
from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, field

from testmu_appium import _config
from testmu_appium._errors import WebSurfaceUnavailable
from testmu_appium._helpers import _web
from testmu_appium._helpers.foreground import foreground_app
from testmu_appium._vars import var

_CHROME_PACKAGES = frozenset(
    {
        "com.android.chrome",
        "com.chrome.beta",
        "com.chrome.dev",
        "com.chrome.canary",
    }
)


def is_chrome_package(package: str) -> bool:
    """Whether this package is a Chrome build that publishes a browser socket.

    Tab operations, the visibility probe, and the consumer that classifies a
    collapsed accessibility projection all gate on the same rule. A second copy
    of the set would diverge silently: one side would offer a candidate the
    other refuses as an unsupported package.
    """
    return package in _CHROME_PACKAGES


_MUTATION_DEADLINE_S = 5.0
_POLL_INTERVAL_S = 0.05


@dataclass(frozen=True)
class _Target:
    target_id: str
    url: str
    title: str
    ws_url: str = ""


@dataclass
class _Order:
    target_ids: list[str] = field(default_factory=list)
    seeded: bool = False

    def merge(self, targets: list[_Target]) -> list[_Target]:
        by_id = {target.target_id: target for target in targets}
        if not self.seeded:
            self.target_ids = [target.target_id for target in targets]
            self.seeded = True
        else:
            self.target_ids = [
                target_id for target_id in self.target_ids if target_id in by_id
            ]
            known = set(self.target_ids)
            self.target_ids.extend(
                target.target_id
                for target in targets
                if target.target_id not in known
            )
        return [by_id[target_id] for target_id in self.target_ids]


@dataclass(frozen=True)
class _Connection:
    key: tuple[str, str, str]
    package: str
    port: int
    browser_ws: str
    transport: str  # "target" | "http"


def _session_id(driver) -> str:
    try:
        session_id = str(driver.session_id or "")
    except Exception:  # noqa: BLE001 - the empty value remains session-keyed by UDID
        session_id = ""
    return session_id or f"driver:{id(driver)}"


def _read_json(port: int, path: str, *, timeout: float = 8.0):
    request = urllib.request.Request(f"http://127.0.0.1:{port}{path}")
    with urllib.request.urlopen(request, timeout=max(0.01, timeout)) as response:
        return json.loads(response.read())


def _mutate_http(
    port: int, path: str, *, method: str = "GET", timeout: float = 8.0
):
    request = urllib.request.Request(
        f"http://127.0.0.1:{port}{path}", method=method
    )
    with urllib.request.urlopen(request, timeout=max(0.01, timeout)) as response:
        body = response.read()
    if not body:
        return None
    try:
        return json.loads(body)
    except (TypeError, ValueError):
        return body.decode("utf-8", errors="replace")


def _method_unavailable(error: BaseException) -> bool:
    message = str(error).lower()
    return (
        "-32601" in message
        or "method not found" in message
        or "wasn't found" in message
        or "was not found" in message
    )


def _remaining(deadline: float | None) -> float:
    if deadline is None:
        return 8.0
    return max(0.01, deadline - time.monotonic())


def _receive_cdp(connection, request_id: int, method: str) -> dict:
    """Receive one flattened browser-session response without exposing ids."""
    while True:
        message = json.loads(connection.recv())
        if message.get("id") != request_id:
            continue
        if "error" in message:
            raise RuntimeError(f"{method} failed")
        result = message.get("result", {})
        if not isinstance(result, dict):
            raise RuntimeError(f"{method} returned an invalid response")
        return result


def _discover_target_infos(browser_ws: str, *, timeout: float) -> list[dict]:
    """Collect the existing targetCreated events emitted before discovery acks.

    Chrome 150 on Android omits background tabs from ``Target.getTargets`` even
    with an all-target filter. ``Target.setDiscoverTargets`` emits the complete
    current set before its response on one persistent browser WebSocket.
    """
    import websocket  # noqa: PLC0415

    connection = websocket.create_connection(
        browser_ws,
        timeout=max(0.01, timeout),
        suppress_origin=_web._SUPPRESS_ORIGIN,
    )
    found = []
    try:
        connection.send(
            json.dumps(
                {
                    "id": 1,
                    "method": "Target.setDiscoverTargets",
                    "params": {"discover": True, "filter": [{}]},
                }
            )
        )
        while True:
            message = json.loads(connection.recv())
            if message.get("method") == "Target.targetCreated":
                info = (message.get("params") or {}).get("targetInfo")
                if isinstance(info, dict):
                    found.append(info)
                continue
            if message.get("id") != 1:
                continue
            if "error" in message:
                raise RuntimeError("Target.setDiscoverTargets failed")
            return found
    finally:
        connection.close()


def _evaluate_in_target(
    browser_ws: str,
    target_id: str,
    expression: str,
    *,
    timeout: float,
):
    """Evaluate in a Target-domain target through a flattened child session.

    Android Chrome's ``Target.getTargets`` and ``/json`` ids can describe
    different proxy layers. Attaching to an id emitted by browser discovery
    keeps the Target domain authoritative and avoids guessing a page WebSocket.
    """
    import websocket  # noqa: PLC0415

    connection = websocket.create_connection(
        browser_ws,
        timeout=max(0.01, timeout),
        suppress_origin=_web._SUPPRESS_ORIGIN,
    )
    try:
        connection.send(
            json.dumps(
                {
                    "id": 1,
                    "method": "Target.attachToTarget",
                    "params": {"targetId": target_id, "flatten": True},
                }
            )
        )
        attached = _receive_cdp(connection, 1, "Target.attachToTarget")
        session_id = str(attached.get("sessionId") or "")
        if not session_id:
            raise RuntimeError("Target.attachToTarget returned no session")

        connection.send(
            json.dumps(
                {
                    "id": 2,
                    "sessionId": session_id,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": expression,
                        "returnByValue": True,
                    },
                }
            )
        )
        evaluated = _receive_cdp(connection, 2, "Runtime.evaluate")
        if evaluated.get("exceptionDetails"):
            raise RuntimeError("Runtime.evaluate raised in the tab target")
        result = evaluated.get("result", {})
        if not isinstance(result, dict):
            raise RuntimeError("Runtime.evaluate returned an invalid result")
        return result.get("value")
    finally:
        connection.close()


def _normalized_url(value: str) -> str:
    """URL origin/path identity with query, fragment and default ports removed."""
    try:
        parsed = urllib.parse.urlsplit(value)
    except (TypeError, ValueError):
        return ""
    scheme = parsed.scheme.lower()
    if scheme not in {"http", "https"} or not parsed.hostname:
        return ""
    host = parsed.hostname.lower()
    try:
        port = parsed.port
    except ValueError:
        return ""
    if ":" in host and not host.startswith("["):
        host = f"[{host}]"
    if port is not None and not (
        (scheme == "http" and port == 80) or (scheme == "https" and port == 443)
    ):
        host = f"{host}:{port}"
    path = parsed.path or "/"
    return urllib.parse.urlunsplit((scheme, host, path, "", ""))


def _resolved_url(value) -> str:
    if value is None:
        return "about:blank"
    resolved = var(value)
    if not isinstance(resolved, str):
        raise ValueError(
            f"new_tab URL must resolve to a string, got {type(resolved).__name__}"
        )
    resolved = resolved.strip()
    if resolved == "about:blank":
        return resolved
    try:
        parsed = urllib.parse.urlsplit(resolved)
    except ValueError as error:
        raise ValueError("new_tab URL is invalid") from error
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.netloc:
        raise ValueError(
            "new_tab URL must use http or https, or be exactly 'about:blank'"
        )
    return resolved


def _validate_index(index, count: int, *, optional: bool = False) -> int | None:
    if optional and index is None:
        return None
    if isinstance(index, bool) or not isinstance(index, int):
        raise TypeError("tab index must be an integer")
    if index < 0 or index >= count:
        raise IndexError(f"tab index {index} is outside the {count} open tabs")
    return index


def _identifier(target: _Target, targets: list[_Target]) -> str | None:
    normalized = _normalized_url(target.url)
    if normalized and sum(
        _normalized_url(candidate.url) == normalized for candidate in targets
    ) == 1:
        return normalized
    if target.title and sum(
        candidate.title == target.title for candidate in targets
    ) == 1:
        return target.title
    return None


class AndroidChromeTabProvider:
    """Stable-order provider for the foreground Android Chrome session."""

    def __init__(self):
        self._orders: dict[tuple[str, str, str], _Order] = {}

    def reset(self) -> None:
        self._orders.clear()

    def _connect(self, driver) -> _Connection:
        package = foreground_app(driver)
        if not is_chrome_package(package):
            raise WebSurfaceUnavailable("browser tab operations", package)
        if not _web.reachable():
            raise WebSurfaceUnavailable("browser tab operations", package)
        try:
            socket = next(
                candidate
                for candidate in _web.sockets()
                if candidate.kind == "browser"
                and candidate.name == _web._BROWSER_SOCKET
            )
            port = _web.forward(socket)
            version = _read_json(port, "/json/version")
        except (StopIteration, OSError, RuntimeError, ValueError) as error:
            raise WebSurfaceUnavailable("browser tab operations", package) from error

        if not isinstance(version, dict):
            raise WebSurfaceUnavailable("browser tab operations", package)
        endpoint_package = str(version.get("Android-Package") or "")
        browser_ws = str(version.get("webSocketDebuggerUrl") or "")
        if endpoint_package != package or endpoint_package not in _CHROME_PACKAGES:
            raise WebSurfaceUnavailable("browser tab operations", package)
        if not browser_ws:
            raise WebSurfaceUnavailable("browser tab operations", package)

        transport = "target"
        try:
            _web.Channel(browser_ws).call("Target.getTargets")
        except Exception as error:  # noqa: BLE001 - only method absence selects fallback
            if not _method_unavailable(error):
                raise RuntimeError("could not enumerate Chrome browser targets") from error
            transport = "http"

        return _Connection(
            key=(
                _session_id(driver),
                str(_config.get("udid") or ""),
                socket.name,
            ),
            package=package,
            port=port,
            browser_ws=browser_ws,
            transport=transport,
        )

    def _raw_targets(
        self, connection: _Connection, *, deadline: float | None = None
    ) -> list[_Target]:
        if connection.transport == "target":
            timeout = _remaining(deadline)
            infos = _discover_target_infos(
                connection.browser_ws,
                timeout=min(_web._CDP_TIMEOUT_S, timeout),
            )
            pages = [
                info
                for info in infos
                if info.get("type") == "page"
                and not info.get("subtype")
                and info.get("targetId")
            ]

            # /json is not an identity source. When present, its page rows are a
            # useful discriminator for tab/page/browser proxy targets because
            # discovery on Android emits all of them. Exact id correlation is
            # preferred; if namespaces differ, retain all discovered pages and
            # let attached-session visibility/semantic identity fail closed.
            page_ws_by_id = {}
            try:
                descriptors = _read_json(
                    connection.port, "/json", timeout=_remaining(deadline)
                )
                if isinstance(descriptors, list):
                    page_ids = {
                        str(item.get("id") or "")
                        for item in descriptors
                        if item.get("type") == "page" and item.get("id")
                    }
                    correlated = [
                        info
                        for info in pages
                        if str(info.get("targetId") or "") in page_ids
                    ]
                    if correlated and len(correlated) == len(page_ids):
                        pages = correlated
                        page_ws_by_id = {
                            str(item["id"]): str(item["webSocketDebuggerUrl"])
                            for item in descriptors
                            if item.get("type") == "page"
                            and item.get("id")
                            and item.get("webSocketDebuggerUrl")
                        }
            except Exception:  # noqa: BLE001 - Target discovery is authoritative
                pass
            return [
                _Target(
                    target_id=str(info["targetId"]),
                    url=str(info.get("url") or ""),
                    title=str(info.get("title") or ""),
                    ws_url=page_ws_by_id.get(str(info["targetId"]), ""),
                )
                for info in pages
            ]

        descriptors = _read_json(
            connection.port, "/json", timeout=_remaining(deadline)
        )
        if not isinstance(descriptors, list):
            raise RuntimeError("Chrome /json returned an invalid inventory")
        pages_by_id = {
            str(item.get("id") or ""): item
            for item in descriptors
            if item.get("type") == "page"
            and item.get("id")
            and item.get("webSocketDebuggerUrl")
        }

        return [
            _Target(
                target_id=target_id,
                url=str(item.get("url") or ""),
                title=str(item.get("title") or ""),
                ws_url=str(item["webSocketDebuggerUrl"]),
            )
            for target_id, item in pages_by_id.items()
        ]

    def _targets(
        self, connection: _Connection, *, deadline: float | None = None
    ) -> list[_Target]:
        raw = self._raw_targets(connection, deadline=deadline)
        order = self._orders.setdefault(connection.key, _Order())
        targets = order.merge(raw)
        if not targets:
            raise RuntimeError("Chrome reported no open page tabs")
        return targets

    @staticmethod
    def _active(
        connection: _Connection,
        targets: list[_Target],
        *,
        deadline: float | None = None,
    ) -> _Target:
        visible = []
        for target in targets:
            timeout = min(_web._CDP_TIMEOUT_S, _remaining(deadline))
            try:
                if target.ws_url:
                    is_visible = _web.Channel(
                        target.ws_url, timeout=timeout
                    ).is_visible()
                elif connection.transport == "target":
                    state = _evaluate_in_target(
                        connection.browser_ws,
                        target.target_id,
                        "document.visibilityState",
                        timeout=timeout,
                    )
                    is_visible = state == "visible"
                else:
                    is_visible = False
                if is_visible:
                    visible.append(target)
            except Exception:  # noqa: BLE001 - a stale page is not the active page
                continue
        if len(visible) != 1:
            raise RuntimeError(
                "Chrome did not report exactly one visible page tab"
            )
        return visible[0]

    def _snapshot(
        self, connection: _Connection, *, deadline: float | None = None
    ) -> tuple[list[_Target], _Target]:
        targets = self._targets(connection, deadline=deadline)
        active = self._active(connection, targets, deadline=deadline)
        return targets, active

    @staticmethod
    def _remember_active(
        connection: _Connection,
        active: _Target,
        *,
        deadline: float | None = None,
    ) -> None:
        if active.ws_url:
            _web.remember_target(active.ws_url)
            _web.remember_target(active.ws_url, connection.package)
            return

        # The existing cookie/storage/history helpers consume a page WebSocket.
        # Map it only as an optional cache by exact discovered id, then semantic
        # page metadata. Target ids remain authoritative for inventory/mutation.
        remembered = ""
        try:
            descriptors = _read_json(
                connection.port, "/json", timeout=_remaining(deadline)
            )
            if isinstance(descriptors, list):
                matches = [
                    item
                    for item in descriptors
                    if str(item.get("id") or "") == active.target_id
                    and item.get("type") == "page"
                    and item.get("webSocketDebuggerUrl")
                ]
                if not matches:
                    matches = [
                        item
                        for item in descriptors
                        if item.get("type") == "page"
                        and item.get("url") == active.url
                        and item.get("webSocketDebuggerUrl")
                    ]
                if len(matches) > 1 and active.title:
                    titled = [
                        item
                        for item in matches
                        if item.get("title") == active.title
                    ]
                    matches = titled or matches
                if len(matches) == 1:
                    remembered = str(matches[0]["webSocketDebuggerUrl"])
        except Exception:  # noqa: BLE001 - this cache is not tab identity
            pass
        _web.remember_target(remembered)
        _web.remember_target(remembered, connection.package)

    @staticmethod
    def _public(targets: list[_Target], active: _Target) -> list[dict]:
        return [
            {
                "index": index,
                "url": target.url,
                "title": target.title,
                "active": target.target_id == active.target_id,
                "identifier": _identifier(target, targets),
            }
            for index, target in enumerate(targets)
        ]

    def get_tabs(self, driver) -> list[dict]:
        connection = self._connect(driver)
        targets, active = self._snapshot(connection)
        self._remember_active(connection, active)
        return self._public(targets, active)

    @staticmethod
    def _resolve(
        targets: list[_Target], index: int | None, title: str | None, *,
        require_index: bool,
    ) -> tuple[int, _Target]:
        if title is not None:
            resolved_title = var(title)
            if not isinstance(resolved_title, str) or not resolved_title:
                raise ValueError("tab identifier must be a non-empty string")
            matches = [
                (position, target)
                for position, target in enumerate(targets)
                if _normalized_url(target.url) == resolved_title
                or target.title == resolved_title
            ]
            if len(matches) != 1:
                qualifier = "no" if not matches else "multiple"
                raise RuntimeError(
                    f"tab identifier matched {qualifier} open tabs"
                )
            position, target = matches[0]
            if index is not None:
                guard = _validate_index(index, len(targets))
                if guard != position:
                    raise RuntimeError(
                        "tab identity drifted from its recorded index"
                    )
            elif require_index:
                raise ValueError("switch_tab requires index")
            return position, target

        if index is None and require_index:
            raise ValueError("switch_tab requires index")
        if index is None:
            raise ValueError("tab target was not specified")
        position = _validate_index(index, len(targets))
        return position, targets[position]

    @staticmethod
    def _target_call(
        connection: _Connection,
        method: str,
        params: dict,
        *,
        deadline: float | None = None,
    ) -> dict:
        try:
            timeout = min(_web._CDP_TIMEOUT_S, _remaining(deadline))
            return _web.Channel(
                connection.browser_ws, timeout=timeout
            ).call(method, params)
        except Exception as error:  # noqa: BLE001 - mutation outcome must stay singular
            raise RuntimeError(f"{method} failed; mutation outcome is unknown") from error

    def _activate(
        self,
        connection: _Connection,
        target: _Target,
        *,
        deadline: float | None = None,
    ) -> None:
        if connection.transport == "target":
            self._target_call(
                connection,
                "Target.activateTarget",
                {"targetId": target.target_id},
                deadline=deadline,
            )
            return
        try:
            _mutate_http(
                connection.port,
                f"/json/activate/{urllib.parse.quote(target.target_id, safe='')}",
                timeout=_remaining(deadline),
            )
        except Exception as error:  # noqa: BLE001 - do not retry a mutation
            raise RuntimeError(
                "HTTP tab activation failed; mutation outcome is unknown"
            ) from error

    def _wait_for(
        self,
        connection: _Connection,
        *,
        visible_id: str,
        absent_id: str | None = None,
        deadline: float | None = None,
    ) -> tuple[list[_Target], _Target]:
        if deadline is None:
            deadline = time.monotonic() + _MUTATION_DEADLINE_S
        last_error: BaseException | None = None
        while time.monotonic() < deadline:
            try:
                targets, active = self._snapshot(
                    connection, deadline=deadline
                )
                ids = {target.target_id for target in targets}
                if (
                    active.target_id == visible_id
                    and (absent_id is None or absent_id not in ids)
                ):
                    self._remember_active(
                        connection, active, deadline=deadline
                    )
                    return targets, active
            except Exception as error:  # noqa: BLE001 - bounded re-enumeration
                last_error = error
            remaining = deadline - time.monotonic()
            if remaining > 0:
                time.sleep(min(_POLL_INTERVAL_S, remaining))
        raise TimeoutError(
            "Chrome tab mutation did not reach the expected visible state "
            "within 5 seconds"
        ) from last_error

    def _wait_for_new(
        self,
        connection: _Connection,
        *,
        previous_ids: set[str],
    ) -> tuple[list[_Target], _Target]:
        """Confirm the newly visible discovered page, independent of proxy ids."""
        deadline = time.monotonic() + _MUTATION_DEADLINE_S
        last_error: BaseException | None = None
        while time.monotonic() < deadline:
            try:
                targets, active = self._snapshot(
                    connection, deadline=deadline
                )
                if active.target_id not in previous_ids:
                    self._remember_active(
                        connection, active, deadline=deadline
                    )
                    return targets, active
            except Exception as error:  # noqa: BLE001 - bounded re-enumeration
                last_error = error
            remaining = deadline - time.monotonic()
            if remaining > 0:
                time.sleep(min(_POLL_INTERVAL_S, remaining))
        raise TimeoutError(
            "Chrome new-tab mutation did not produce a newly visible page "
            "within 5 seconds"
        ) from last_error

    def new_tab(self, driver, url) -> dict:
        resolved_url = _resolved_url(url)
        connection = self._connect(driver)
        previous, _ = self._snapshot(
            connection
        )  # seed and prove visibility before mutation
        previous_ids = {target.target_id for target in previous}
        if connection.transport == "target":
            result = self._target_call(
                connection,
                "Target.createTarget",
                {"url": resolved_url, "forTab": True},
            )
            target_id = str(result.get("targetId") or "")
        else:
            encoded = urllib.parse.quote(resolved_url, safe="")
            result = _mutate_http(
                connection.port, f"/json/new?{encoded}", method="PUT"
            )
            target_id = str((result or {}).get("id") or "")
        if not target_id:
            raise RuntimeError(
                "Chrome created a tab without returning its identity; "
                "mutation outcome is unknown"
            )
        targets, active = self._wait_for_new(
            connection, previous_ids=previous_ids
        )
        return self._public(targets, active)[
            next(
                index
                for index, target in enumerate(targets)
                if target.target_id == active.target_id
            )
        ]

    def switch_tab(
        self, driver, index: int, title: str | None
    ) -> dict:
        connection = self._connect(driver)
        targets, _ = self._snapshot(connection)
        _, target = self._resolve(
            targets, index, title, require_index=True
        )
        self._activate(connection, target)
        targets, active = self._wait_for(
            connection, visible_id=target.target_id
        )
        return self._public(targets, active)[
            next(
                position
                for position, candidate in enumerate(targets)
                if candidate.target_id == target.target_id
            )
        ]

    def _close(self, connection: _Connection, target: _Target) -> None:
        if connection.transport == "target":
            try:
                _web.Channel(connection.browser_ws).call(
                    "Target.closeTarget", {"targetId": target.target_id}
                )
                return
            except Exception as error:  # noqa: BLE001 - method absence did not mutate
                if not _method_unavailable(error):
                    raise RuntimeError(
                        "Target.closeTarget failed; mutation outcome is unknown"
                    ) from error
        try:
            _mutate_http(
                connection.port,
                f"/json/close/{urllib.parse.quote(target.target_id, safe='')}",
            )
        except Exception as error:  # noqa: BLE001 - do not retry a mutation
            raise RuntimeError(
                "HTTP tab close failed; mutation outcome is unknown"
            ) from error

    def close_tab(
        self, driver, index: int | None, title: str | None
    ) -> dict:
        connection = self._connect(driver)
        targets, active = self._snapshot(connection)
        if len(targets) <= 1:
            raise RuntimeError("cannot close the final open tab")

        if index is None and title is None:
            position = next(
                i
                for i, target in enumerate(targets)
                if target.target_id == active.target_id
            )
            target = active
        else:
            position, target = self._resolve(
                targets, index, title, require_index=False
            )

        closing_active = target.target_id == active.target_id
        survivor = active
        if closing_active:
            survivor = targets[position - 1] if position > 0 else targets[1]

        self._close(connection, target)
        deadline = time.monotonic() + _MUTATION_DEADLINE_S
        if closing_active:
            self._activate(connection, survivor, deadline=deadline)
        targets, active = self._wait_for(
            connection,
            visible_id=survivor.target_id,
            absent_id=target.target_id,
            deadline=deadline,
        )
        return self._public(targets, active)[
            next(
                i
                for i, candidate in enumerate(targets)
                if candidate.target_id == survivor.target_id
            )
        ]
