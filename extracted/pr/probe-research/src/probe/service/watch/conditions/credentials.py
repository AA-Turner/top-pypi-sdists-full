"""family credential_refused: each configured key asked once per interval whether the API still takes it."""

from __future__ import annotations

import asyncio
import json
import re
import time
from collections.abc import Callable
from probe.service.watch.incident import Family
from probe.service.watch.loop import _on_daemon_thread
from probe.service.watch.settings import (
    CREDENTIAL_CHECK_S,
    CREDENTIAL_DEADLINE_S,
    CREDENTIAL_RETRY_S,
    CREDENTIAL_TIMEOUT_S,
)
#: The CLI config's keys, by the kind a report names (never a key itself), and
#: the door that asks: `me` (`GET /v1/me`, which counts as the key's use) or
#: `capture` (`POST /v1/device-state`'s capture part, which records nothing:
#: a daemon key asked daily must not read as used on an idle machine).
CREDENTIAL_KEYS = (("login", "token", "me"), ("daemon_key", "companion_token", "capture"),
                   ("mcp_key", "mcp_token", "me"))
#: What the `report` read takes for `sid` (its parser refuses anything else,
#: and the whole report with it): any other session id rides in the facts.
_UUID = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


def _ask_me(base_url: str, token: str, timeout: float) -> str:
    """`GET /v1/me` with one key: `ok`, `refused` (401/403) or `unknown`
    (offline, a timeout, a redirect, anything else). One try, no retry."""
    import urllib.error
    import urllib.request

    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        """A redirect is answered (a 3xx: `unknown`), never followed: urllib
        would carry the key's `Authorization` header wherever it points
        (another host, plain HTTP)."""

        def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001, ARG002
            return None

    try:
        from probe.foundation.tls.tls import ssl_context

        context = ssl_context()
    except Exception:  # noqa: BLE001 -- urllib's default trust
        context = None
    opener = urllib.request.build_opener(_NoRedirect, urllib.request.HTTPSHandler(context=context))
    request = urllib.request.Request(
        base_url.rstrip("/") + "/v1/me",
        headers={"Authorization": f"Bearer {token}", "User-Agent": "probe-service-watch"},
    )
    try:
        with opener.open(request, timeout=timeout) as response:
            return "ok" if 200 <= response.status < 300 else "unknown"
    except urllib.error.HTTPError as exc:
        # Only a 401: a 403 is a proxy's or a scope's, not a dead key.
        return "refused" if exc.code == 401 else "unknown"
    except Exception:  # noqa: BLE001 -- offline is no refusal
        return "unknown"


def _ask_capture(base_url: str, token: str, timeout: float) -> str:
    """`POST /v1/device-state` with a capture key in its body and no bearer:
    the server's own verdict (`ok`, `rejected`: refused), which records no use
    of the key. Anything else (an older server, offline) is `unknown`."""
    import urllib.error
    import urllib.request

    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001, ARG002
            return None

    try:
        from probe.foundation.tls.tls import ssl_context

        context = ssl_context()
    except Exception:  # noqa: BLE001 -- urllib's default trust
        context = None
    try:
        from probe.foundation.harness_registry.harness_registry import get_registry

        # Any agent's source id: the door judges a capture key the same for each.
        source = get_registry().captured()[0].id
    except Exception:  # noqa: BLE001 -- no registry: no verdict
        return "unknown"
    opener = urllib.request.build_opener(_NoRedirect, urllib.request.HTTPSHandler(context=context))
    request = urllib.request.Request(
        base_url.rstrip("/") + "/v1/device-state", method="POST",
        data=json.dumps({"capture_tokens": {source: token}}).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "probe-service-watch"},
    )
    try:
        with opener.open(request, timeout=timeout) as response:
            body = json.loads(response.read(64 * 1024) or b"{}")
    except Exception:  # noqa: BLE001 -- offline, an older server: no verdict
        return "unknown"
    verdict = (body.get("capture") or {}).get(source) if isinstance(body, dict) else None
    return {"ok": "ok", "rejected": "refused"}.get(verdict, "unknown") if isinstance(verdict, str) else "unknown"


def _ask(base_url: str, token: str, timeout: float, door: str) -> str:
    return (_ask_capture if door == "capture" else _ask_me)(base_url, token, timeout)


def _may_carry_keys(base_url: str) -> bool:
    """HTTPS, or plain HTTP to this machine only: a key never crosses a
    network in the clear for a check."""
    from urllib.parse import urlsplit

    try:
        parts = urlsplit(base_url)
    except ValueError:
        return False
    if parts.scheme == "https":
        return True
    return parts.scheme == "http" and parts.hostname in ("127.0.0.1", "localhost", "::1")


def _credential_id(base_url: str, kind: str, token: str) -> str:
    """A key's name in `watch.json`: its backend, kind and value hashed, so a
    replaced key or another context is asked afresh. Never the key."""
    import hashlib

    return hashlib.sha256(f"{base_url}\0{kind}\0{token}".encode()).hexdigest()[:16]


def configured_key_ids() -> dict[str, str]:
    """`{kind: id}` (`_credential_id`) of each key the CLI config's active
    context holds (CREDENTIAL_KEYS), the backend's as `credential_verdicts`
    names them; {} without a config. Blocking: a thread."""
    try:
        from probe.analytics.core import DEFAULT_BASE, read_cli_config

        config = read_cli_config()
        base_url = str(config.get("base_url") or DEFAULT_BASE).rstrip("/")
    except Exception:  # noqa: BLE001 -- no config: no keys
        return {}
    return {
        kind: _credential_id(base_url, kind, config[key])
        for kind, key, _ in CREDENTIAL_KEYS if isinstance(config.get(key), str) and config.get(key)
    }


def credential_verdicts(
    *, due: Callable[[str], bool] = lambda ident: True,
    ask: Callable[[str, str, float, str], str] = _ask, monotonic: Callable[[], float] = time.monotonic,
) -> dict[str, tuple[str, str]]:
    """`{kind: (id, ok|refused|unknown)}` for each key the CLI config's
    active context holds (CREDENTIAL_KEYS) whose id (`_credential_id`) is
    `due`, asked one at a time within CREDENTIAL_DEADLINE_S in all: a key not
    asked before it is `unknown`, and no ask starts past it
    (`hints.HintFetcher`'s rule, not `alertpoll._get`'s retry past its
    deadline). Each key goes to its own context's backend only (never
    `PROBE_BASE_URL`: `alertpoll.endpoint`'s rule), and only over HTTPS
    (`_may_carry_keys`). Blocking: a thread."""
    try:
        from probe.analytics.core import DEFAULT_BASE, read_cli_config

        config = read_cli_config()
        base_url = str(config.get("base_url") or DEFAULT_BASE).rstrip("/")
    except Exception:  # noqa: BLE001 -- no config: nothing to ask about
        return {}
    if not base_url or not _may_carry_keys(base_url):
        return {}
    deadline = monotonic() + CREDENTIAL_DEADLINE_S
    found: dict[str, tuple[str, str]] = {}
    for kind, key, door in CREDENTIAL_KEYS:
        token = config.get(key)
        if not isinstance(token, str) or not token:
            continue
        ident = _credential_id(base_url, kind, token)
        if not due(ident):
            continue
        left = deadline - monotonic()
        if left <= 0:
            found[kind] = (ident, "unknown")
            continue
        found[kind] = (ident, ask(base_url, token, min(CREDENTIAL_TIMEOUT_S, left), door))
    return found


class CredentialCheckMixin:
    """Part of Watch: its methods run with `self` the Watch; compose() folds them into Watch."""

    async def _credential_check(self, now: float) -> None:
        """Each key not answered within CREDENTIAL_CHECK_S, asked once (and
        one with no answer, offline or a timeout, again CREDENTIAL_RETRY_S
        later); a refused one is `credential_refused`, reported once for that
        key (a key replaced is a new one)."""
        try:
            if self._credentials_busy or now < self._credentials_after:
                return
            if not self.enabled or not await self._may_ask_keys():
                return
            with self._lock:
                self._load_state()
                answered = dict(self._credentials_at)
            tried = dict(self._credentials_tried)

            def due(ident: str) -> bool:
                at, missed = answered.get(ident), tried.get(ident)
                if missed is not None and 0 <= now - missed < CREDENTIAL_RETRY_S:
                    return False
                return at is None or not 0 <= now - at < CREDENTIAL_CHECK_S

            def ask() -> dict:
                try:
                    return self.credentials(due=due)
                finally:
                    self._credentials_busy = False

            self._credentials_busy = True
            try:
                verdicts = await _on_daemon_thread(ask, CREDENTIAL_DEADLINE_S + CREDENTIAL_TIMEOUT_S)
            except RuntimeError:  # no thread could start: nothing holds the guard
                self._credentials_busy = False
                raise
            except asyncio.TimeoutError:
                self._credentials_after = now + CREDENTIAL_RETRY_S
                self.log("watch: the credential check did not finish in time")
                return
            with self._lock:
                self._load_state()
                self._key_answers.update({ident: verdict for ident, verdict in verdicts.values()})
            for ident, verdict in verdicts.values():
                if verdict == "unknown":
                    self._credentials_tried[ident] = now
                else:
                    self._credentials_tried.pop(ident, None)
            settled = {ident: now for ident, verdict in verdicts.values() if verdict != "unknown"}
            if settled:
                with self._lock:
                    kept = {k: v for k, v in self._credentials_at.items() if 0 <= now - v < 2 * CREDENTIAL_CHECK_S}
                    self._credentials_at = {**kept, **settled}
            if verdicts:
                await asyncio.to_thread(self._write_state)
            refused = sorted(kind for kind, (_, verdict) in verdicts.items() if verdict == "refused")
            if refused:
                unknown = sorted(kind for kind, (_, verdict) in verdicts.items() if verdict == "unknown")
                idents = ",".join(sorted(verdicts[kind][0] for kind in refused))
                self.note(Family.CREDENTIAL_REFUSED, "refused", None, {"refused": refused, "unknown": unknown},
                          once=f"credential_refused:{idents}")
                await self._send_next()  # it finished after the scan's own send
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 -- one bad check never stops the watch
            self.log(f"watch: the credential check failed: {exc!r}")
