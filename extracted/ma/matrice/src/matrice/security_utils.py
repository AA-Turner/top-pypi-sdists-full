"""Shared security helpers for the matrice SDK.

Small, dependency-free utilities for:

* redacting sensitive URLs before they reach logs (``redact_url``) -- presigned
  S3 URLs carry their authorization signature in the query string and RTSP feed
  URLs embed ``user:pass@`` credentials, so both must be stripped before
  printing;
* validating outbound download URLs (``validate_download_url``) with an
  https-only scheme allowlist plus SSRF protection against
  private/loopback/link-local/reserved and cloud-metadata addresses;
* extracting untrusted zip archives with a zip-slip guard
  (``safe_extractall_zip``).
"""

from __future__ import annotations

import ipaddress
import os
import socket
from urllib.parse import urlsplit, urlunsplit

_ALLOWED_DOWNLOAD_SCHEMES = ("https",)
_METADATA_ADDRESS = "169.254.169.254"


def redact_url(url):
    """Return a URL that is safe to log.

    Strips the query string (which for presigned S3 URLs carries the signature
    that *is* the credential) and any ``user:pass@`` userinfo (RTSP camera feed
    credentials), keeping only scheme, host[:port] and path so logs remain
    useful without leaking secrets.
    """
    if not isinstance(url, str) or not url:
        return url
    try:
        parts = urlsplit(url)
    except (ValueError, TypeError):
        return "<redacted-url>"
    if not parts.scheme and not parts.netloc:
        # Not a URL (e.g. a bare filename); nothing sensitive to strip.
        return url
    netloc = parts.hostname or ""
    if parts.port is not None:
        netloc = f"{netloc}:{parts.port}"
    return urlunsplit((parts.scheme, netloc, parts.path, "", ""))


def _is_disallowed_address(ip_str):
    """True if the resolved address must not be contacted (SSRF guard)."""
    try:
        ip = ipaddress.ip_address(ip_str)
    except ValueError:
        return True
    return bool(
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_reserved
        or ip.is_multicast
        or ip.is_unspecified
        or ip_str == _METADATA_ADDRESS
    )


def validate_download_url(url, allow_http=False):
    """Validate an outbound download URL; fail closed on anything suspicious.

    * Enforces an https-only scheme allowlist (pass ``allow_http=True`` only for
      explicitly trusted internal callers).
    * Resolves the hostname and rejects the request if **any** resolved A/AAAA
      record is private/loopback/link-local/reserved/multicast or the cloud
      metadata endpoint (169.254.169.254), mitigating SSRF and DNS-rebinding
      that targets only a subset of records.

    Returns the URL unchanged when valid; raises ``ValueError`` otherwise.
    """
    if not isinstance(url, str) or not url:
        raise ValueError("download URL must be a non-empty string")
    parts = urlsplit(url)
    schemes = ("https", "http") if allow_http else _ALLOWED_DOWNLOAD_SCHEMES
    if parts.scheme.lower() not in schemes:
        raise ValueError(f"disallowed URL scheme {parts.scheme!r}; allowed: {schemes}")
    host = parts.hostname
    if not host:
        raise ValueError("download URL has no host")
    try:
        infos = socket.getaddrinfo(host, parts.port or None, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise ValueError(f"could not resolve host {host!r}: {exc}") from exc
    for info in infos:
        ip_str = info[4][0]
        if _is_disallowed_address(ip_str):
            raise ValueError(f"refusing to download from host {host!r} resolving to disallowed address {ip_str}")
    return url


def safe_extractall_zip(zip_ref, dest_dir):
    """Extract a ``zipfile.ZipFile`` with a zip-slip guard.

    Rejects members with absolute paths or ``..`` traversal that would resolve
    outside ``dest_dir`` before extracting anything.
    """
    dest_root = os.path.realpath(dest_dir)
    for member in zip_ref.namelist():
        target = os.path.realpath(os.path.join(dest_dir, member))
        if target != dest_root and not target.startswith(dest_root + os.sep):
            raise ValueError(f"unsafe path in zip archive (zip-slip): {member!r}")
    zip_ref.extractall(dest_dir)  # nosec B202 - members validated above
