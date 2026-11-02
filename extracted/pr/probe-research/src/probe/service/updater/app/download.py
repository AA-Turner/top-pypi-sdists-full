"""fetch the manifest and the archive over HTTPS within one deadline and a byte cap."""

from __future__ import annotations
import contextlib
import json
import time
from probe.service.updater.app.errors import InstallError
from probe.service.updater.app.manifest import parse_manifest

#: prbe-ai/desktop `src-tauri/tauri.conf.json`, `plugins.updater.endpoints`:
#: the manifest the app's own updater reads. Keep the two the same.
ENDPOINTS = ("https://github.com/prbe-ai/desktop-releases/releases/latest/download/latest.json",)
#: Each read from the network, at most.
READ_TIMEOUT_S = 30.0
MANIFEST_MAX_BYTES = 1024 * 1024


# -- the network -------------------------------------------------------------------

USER_AGENT = "probe-service (desktop app update)"


class _Deadline:
    def __init__(self, seconds: float) -> None:
        self.seconds = seconds
        self.end = time.monotonic() + seconds

    def left(self) -> float:
        left = self.end - time.monotonic()
        if left <= 0:
            raise InstallError(f"no result within {self.seconds:g} s; gave up on the update")
        return left


def _opener():
    """urllib with the one TLS decision of this package (`probe.foundation.tls.tls`: the OS
    store plus certifi, and the CA variables), the system's proxies (as the
    app's updater finds them), and redirects to https only."""
    import ssl
    import urllib.request

    try:
        from probe.foundation.tls.tls import ssl_context

        context = ssl_context()
    except Exception:  # noqa: BLE001 -- the stdlib's default trust, never none
        context = ssl.create_default_context()

    class HttpsOnly(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
            if not str(newurl).startswith("https://"):
                raise InstallError(f"a redirect to {newurl.split('?')[0]} is not https")
            return super().redirect_request(req, fp, code, msg, headers, newurl)

    return urllib.request.build_opener(urllib.request.HTTPSHandler(context=context), HttpsOnly())


def fetch(url: str, *, accept: str, limit: int, deadline: _Deadline, sink=None) -> bytes | int | None:
    """GET `url` (https only): its body (at most `limit` bytes), or with `sink`
    (a binary file) the number of bytes written to it. None: 204 No Content."""
    import urllib.error
    import urllib.request

    if not url.startswith("https://"):
        raise InstallError(f"{url.split('?')[0]} is not https")
    request = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": USER_AGENT})
    try:
        response = _opener().open(request, timeout=min(READ_TIMEOUT_S, deadline.left()))
    except urllib.error.HTTPError as exc:
        raise InstallError(f"{url.split('?')[0]} answered {exc.code}") from exc
    except (urllib.error.URLError, OSError) as exc:
        reason = getattr(exc, "reason", exc)
        raise InstallError(f"{url.split('?')[0]}: {reason}") from exc
    with response:
        if response.status == 204:
            return None
        length = response.headers.get("Content-Length")
        if length and length.isdigit() and int(length) > limit:
            raise InstallError(f"{url.split('?')[0]} is {length} bytes, over the {limit}-byte limit")
        body = bytearray()
        written = 0
        sock = getattr(getattr(getattr(response, "fp", None), "raw", None), "_sock", None)
        read = getattr(response, "read1", response.read)
        while True:
            # Each read waits at most what is left of the deadline: a server that
            # trickles a byte at a time cannot hold the step past it.
            left = deadline.left()
            if sock is not None:
                with contextlib.suppress(OSError):
                    sock.settimeout(min(READ_TIMEOUT_S, left))
            try:
                chunk = read(256 * 1024)
            except TimeoutError as exc:
                deadline.left()
                raise InstallError(f"{url.split('?')[0]}: no data for {min(READ_TIMEOUT_S, left):g} s") from exc
            except OSError as exc:
                raise InstallError(f"{url.split('?')[0]}: {exc}") from exc
            if not chunk:
                break
            written += len(chunk)
            if written > limit:
                raise InstallError(f"{url.split('?')[0]} is over the {limit}-byte limit")
            if sink is None:
                body += chunk
            else:
                sink.write(chunk)
    return bytes(body) if sink is None else written


def check(endpoints=ENDPOINTS, *, deadline: _Deadline, fetcher=fetch, machine_arch: str | None = None) -> tuple:
    """The updater's `check`: each endpoint in order, the first one that answers
    a manifest wins. `(version, entry)`; `(None, None)` for 204 No Content."""
    last: Exception | None = None
    for url in endpoints:
        try:
            body = fetcher(url, accept="application/json", limit=MANIFEST_MAX_BYTES, deadline=deadline)
        except InstallError as exc:
            last = exc
            continue
        if body is None:
            return None, None
        try:
            return parse_manifest(json.loads(body), machine_arch)
        except (InstallError, ValueError) as exc:
            last = exc
    raise InstallError(f"no update manifest: {last}" if last else "no update manifest")
