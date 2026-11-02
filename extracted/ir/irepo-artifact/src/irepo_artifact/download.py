"""Credential-free streaming downloads using AP-issued URLs."""
from __future__ import annotations

import http.client
from pathlib import Path
import ssl
import time
from typing import Callable, Literal
import urllib.error
import urllib.parse
import urllib.request

from .api import internal_download_url
from .errors import ArtifactError, ArtifactNotFound, DownloadError, HTTPStatusError, NetworkError
from .models import DownloadTarget


class _RemoteDownloadError(DownloadError):
    """A remote transfer failed; a different validated provider may work."""


class _DownloadRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        newurl = internal_download_url(newurl)
        if req.full_url.startswith('https:') and not newurl.startswith('https:'):
            raise DownloadError('refusing insecure download redirect')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _network_error(exc):
    reason = exc.reason if isinstance(exc, urllib.error.URLError) else exc
    if isinstance(reason, ssl.SSLError):
        return _RemoteDownloadError('TLS validation or handshake failed')
    return NetworkError('artifact connection failed or transfer interrupted')


def stream_download(url: str, destination: Path, timeout: float = 30) -> None:
    url = internal_download_url(url)
    # Fresh opener and headers: API identity must never be copied to signed URLs.
    try:
        response = urllib.request.build_opener(_DownloadRedirect()).open(url, timeout=timeout)
    except urllib.error.HTTPError as exc:
        code = exc.code
        missing = False
        try:
            # Bound untrusted bodies; never retain their contents in exceptions.
            if code != 404:
                missing = b'NoSuchKey' in exc.read(65536)
        except (OSError, http.client.HTTPException):
            pass  # Preserve status-based handling if the body cannot be read.
        finally:
            exc.close()
        if missing:
            raise ArtifactNotFound('artifact content not found') from None
        raise HTTPStatusError(code) from None
    except (urllib.error.URLError, OSError, http.client.HTTPException) as exc:
        raise _network_error(exc) from None
    with response:
        if response.status != 200:
            raise HTTPStatusError(response.status)
        expected = response.headers.get('Content-Length')
        try:
            expected = int(expected) if expected is not None else None
            if expected is not None and expected < 0:
                raise ValueError
        except ValueError:
            raise _RemoteDownloadError('invalid download content length') from None
        try:
            output = Path(destination).open('wb')
        except OSError:
            raise DownloadError('cannot open artifact output file') from None
        try:
            with output:
                count = 0
                while True:
                    try:
                        chunk = response.read(1024 * 1024)
                    except (OSError, http.client.HTTPException) as exc:
                        raise _network_error(exc) from None
                    if not chunk:
                        break
                    output.write(chunk)
                    count += len(chunk)
                if expected is not None and count != expected:
                    raise NetworkError('artifact transfer interrupted')
        except OSError:
            raise DownloadError('cannot write artifact output file') from None


def download_with_refresh(target: DownloadTarget, destination: Path,
                          refresh: Callable[[], DownloadTarget], timeout: float = 30) -> None:
    refreshed = False
    failures = 0
    while True:
        try:
            stream_download(target.url, destination, timeout)
            return
        except HTTPStatusError as exc:
            if exc.status in (401, 403) and not refreshed:
                target = refresh()
                refreshed = True
                continue
            if (exc.status == 429 or 500 <= exc.status < 600) and failures < 2:
                time.sleep(0.25 * (2 ** failures))
                failures += 1
                continue
            raise


def download_archive(targets: dict[str, DownloadTarget], destination: Path,
                     refresh_targets: Callable[[str], dict[str, DownloadTarget]],
                     timeout: float = 30, *, on_refreshed=None, probe=None,
                     get_proxy_targets=None) -> Literal['oss', 'proxy'] | None:
    channel = next((kind for kind in ('oss', 'proxy', 'legacy') if kind in targets), None)
    if channel not in targets:
        raise DownloadError('no artifact download channel available')

    refresh_error = None

    def refresh():
        nonlocal refresh_error, channel
        try:
            renewed = dict(refresh_targets(channel))
            if channel not in renewed:
                if channel == 'legacy' and renewed:
                    channel = next((kind for kind in ('oss', 'proxy', 'legacy') if kind in renewed), None)
                elif 'legacy' in renewed:
                    channel = 'legacy'
                elif channel == 'oss' and 'proxy' in renewed:
                    targets.clear()
                    targets.update(renewed)
                    if on_refreshed is not None:
                        on_refreshed()
                    raise _RemoteDownloadError('refreshed links require proxy')
                else:
                    raise DownloadError('original download channel unavailable after refresh')
        except ArtifactError as exc:
            refresh_error = exc
            raise
        targets.clear()
        targets.update(renewed)
        if on_refreshed is not None:
            on_refreshed()
        return targets[channel]

    try:
        if channel == 'oss' and ('proxy' in targets or get_proxy_targets is not None) and probe is not None:
            if not probe(targets[channel].url):
                # Use the existing network-failure fallback, including the
                # distinction between missing artifacts and unavailable OSS.
                raise NetworkError('OSS TCP probe failed')
        download_with_refresh(targets[channel], destination, refresh, timeout)
        return None if channel == 'legacy' else channel
    except ArtifactError as exc:
        remote_failure = isinstance(exc, (NetworkError, HTTPStatusError, ArtifactNotFound, _RemoteDownloadError)) or exc is refresh_error
        if channel != 'oss' or ('proxy' not in targets and get_proxy_targets is None) or not remote_failure:
            raise
        oss_missing = isinstance(exc, ArtifactNotFound) or isinstance(exc, HTTPStatusError) and exc.status == 404
    if 'proxy' not in targets:
        try:
            targets.update(get_proxy_targets())
        except ArtifactNotFound:
            if not oss_missing:
                raise DownloadError('proxy artifact missing after OSS transfer failed') from None
            raise
        if 'proxy' not in targets:
            raise DownloadError('proxy link unavailable after OSS transfer failed')
    channel = 'proxy'
    try:
        download_with_refresh(targets[channel], destination, refresh, timeout)
    except (ArtifactNotFound, HTTPStatusError) as exc:
        proxy_missing = isinstance(exc, ArtifactNotFound) or exc.status == 404
        if proxy_missing and not oss_missing:
            raise DownloadError('proxy artifact missing after OSS transfer failed') from None
        raise
    return None if channel == 'legacy' else channel
