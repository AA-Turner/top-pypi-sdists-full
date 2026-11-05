"""AllowedTargets: where a fenced caller's `api.call` may go (plan D25, H4c): the API origins this
service's own config names (and the API of the SDK that started a delivery service), and the storage
hosts those APIs hand out by name in a 2xx answer (presigned https URLs). Never a loopback, link-local,
private or metadata address unless the service's own config names it as its API."""

from __future__ import annotations

import ipaddress
import json
import os
import socket
import threading
import time
from urllib.parse import urlsplit

#: A storage host an API answer named stays reachable this long (a presigned URL's life is shorter).
HANDED_OUT_S = 3600.0
#: Storage origins kept, at most (the oldest goes first).
MAX_HANDED_OUT = 256
#: The service's own API origins are read again after this.
CONFIG_TTL_S = 30.0
#: An answer is read for URLs only up to this size.
MAX_SCANNED_BYTES = 512 * 1024
#: Where the API hands out storage URLs, by name (H-1), and nowhere else: top-level keys of an answer
#: (`upload_url` of a presigned upload, `download_url`), and the keys of each item under a list or a
#: map of items (`parts[].url` of a multipart grant, the catalog door's `uploads[].url`, a batch
#: presign's `items{id: {download_url}}`).
URL_KEYS = ("upload_url", "download_url")
ITEM_LIST_KEYS = ("parts", "uploads", "items")
ITEM_URL_KEYS = ("url", "upload_url", "download_url")
#: Names of the clouds' metadata services (their addresses are link-local or shared, refused anyway).
METADATA_NAMES = frozenset({"metadata.google.internal", "metadata", "instance-data", "instance-data.ec2.internal"})
#: The shared address space (RFC 6598): Alibaba's metadata service lives in it; `is_private` misses it.
SHARED_SPACE = ipaddress.ip_network("100.64.0.0/10")
#: The SDK that started a delivery service names its API here (plan M-5): reachable like the config's.
STARTER_API_ENV = "PROBE_SERVICE_STARTER_API"


def get_origin(url: str) -> str | None:
    """`scheme://host[:port]`, lower case, the default port dropped; None for anything not http(s)."""
    try:
        parts = urlsplit(url)
        host = (parts.hostname or "").lower().rstrip(".")
        port = parts.port
    except ValueError:
        return None
    if parts.scheme not in ("http", "https") or not host:
        return None
    default = 443 if parts.scheme == "https" else 80
    shown = f"[{host}]" if ":" in host else host
    return f"{parts.scheme}://{shown}" + (f":{port}" if port and port != default else "")


def is_forbidden_host(host: str, *, should_resolve: bool = True) -> bool:
    """A loopback, link-local (the clouds' metadata service included), private, shared, unspecified,
    multicast or reserved address: by literal, else by every address the name resolves to. A name
    that does not resolve counts as forbidden. Blocking (DNS): a relay thread."""
    host = host.strip("[]").lower().rstrip(".")
    try:
        return is_forbidden_ip(ipaddress.ip_address(host.split("%")[0]))
    except ValueError:
        pass
    if host in METADATA_NAMES or host == "localhost" or host.endswith((".localhost", ".internal")):
        return True
    if not should_resolve:
        return False
    try:
        found = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except OSError:
        return True
    return not found or any(is_forbidden_ip(ipaddress.ip_address(str(item[4][0]).split("%")[0])) for item in found)


#: Ranges refused whatever the interpreter's `ipaddress` tables say (#4287 L2): IPv6 site-local, and
#: the IPv6 forms that carry an IPv4 address inside (NAT64, 6to4, Teredo), checked by what they carry.
SITE_LOCAL_V6 = ipaddress.ip_network("fec0::/10")
NAT64 = ipaddress.ip_network("64:ff9b::/96")
SIX_TO_FOUR = ipaddress.ip_network("2002::/16")


def is_forbidden_ip(address: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    mapped = getattr(address, "ipv4_mapped", None)
    if mapped is not None:
        address = mapped
    if address.version == 6:
        if address in SITE_LOCAL_V6:
            return True
        inner = None
        if address in NAT64:
            inner = ipaddress.IPv4Address(int(address) & 0xFFFFFFFF)
        elif address in SIX_TO_FOUR:
            inner = ipaddress.IPv4Address((int(address) >> 80) & 0xFFFFFFFF)
        elif address.teredo is not None:
            inner = address.teredo[1]
        if inner is not None and is_forbidden_ip(inner):
            return True
    return (address.is_loopback or address.is_link_local or address.is_private or address.is_unspecified
            or address.is_multicast or address.is_reserved or address in SHARED_SPACE)


def is_metadata_host(host: str) -> bool:
    """A cloud metadata service's name or link-local address: refused even when a config names it."""
    host = host.strip("[]").lower().rstrip(".")
    if host in METADATA_NAMES:
        return True
    try:
        address = ipaddress.ip_address(host.split("%")[0])
    except ValueError:
        return False
    mapped = getattr(address, "ipv4_mapped", None) or address
    return mapped.is_link_local or mapped in SHARED_SPACE


class AllowedTargets:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._handed_out: dict[str, float] = {}
        self._api: set[str] = set()
        self._api_read_at = float("-inf")

    def is_allowed(self, url: str, *, is_fenced: bool) -> bool:
        """An unfenced caller may go anywhere it could go itself; a fenced one only to the API and
        the storage it hands out. Blocking (it may resolve a name): a relay thread."""
        if not is_fenced:
            return True
        origin = get_origin(url)
        if origin is None:
            return False
        host = urlsplit(url).hostname or ""
        if origin in self._get_api_origins():
            return not is_metadata_host(host)
        with self._lock:
            until = self._handed_out.get(origin)
        if until is None or until <= time.monotonic():
            return False
        return not is_forbidden_host(host)  # again at each call: a name may point elsewhere since

    def record_answer(self, url: str, status: int, content_type: str, body: bytes) -> None:
        """A 2xx JSON answer of one of the service's API origins: the https storage URLs it hands out
        by name (`URL_KEYS`, `ITEM_LIST_KEYS`) are reachable for a while; none on a private address."""
        if not 200 <= status < 300 or "json" not in content_type or not body or len(body) > MAX_SCANNED_BYTES:
            return
        if get_origin(url) not in self._get_api_origins():
            return
        try:
            found = list(_find_handed_out(json.loads(body)))
        except ValueError:
            return
        learned = [origin for origin, host in found if not is_forbidden_host(host)]
        if not learned:
            return
        until = time.monotonic() + HANDED_OUT_S
        with self._lock:
            for origin in learned:
                self._handed_out.pop(origin, None)
                self._handed_out[origin] = until
            while len(self._handed_out) > MAX_HANDED_OUT:
                self._handed_out.pop(next(iter(self._handed_out)))

    def _get_api_origins(self) -> set[str]:
        with self._lock:
            if time.monotonic() - self._api_read_at < CONFIG_TTL_S:
                return set(self._api)
        origins = {o for o in map(get_origin, get_configured_apis()) if o}
        with self._lock:
            self._api, self._api_read_at = origins, time.monotonic()
            return set(origins)


def get_configured_apis() -> list[str]:
    """The API addresses this service's own CLI config names (every context's `base_url`), the hosted
    API, and the API of the SDK that started a delivery service (`STARTER_API_ENV`). Never a fenced
    caller's: its `PROBE_BASE_URL` or config could name any address."""
    from probe.sdk.settings.settings import CONTEXTS_KEY, DEFAULT_BASE_URL, load_file

    found = [DEFAULT_BASE_URL]
    starter = os.environ.get(STARTER_API_ENV)
    if starter:
        found.append(starter)
    try:
        contexts = load_file().get(CONTEXTS_KEY)
    except Exception:  # noqa: BLE001 -- an unreadable config: the hosted API only
        return found
    if isinstance(contexts, dict):
        found += [row["base_url"] for row in contexts.values()
                  if isinstance(row, dict) and isinstance(row.get("base_url"), str)]
    return found


def _find_handed_out(answer: object):
    """`(origin, host)` of each https URL the answer hands out by name."""
    if not isinstance(answer, dict):
        return
    values = [answer.get(key) for key in URL_KEYS]
    for key in ITEM_LIST_KEYS:
        items = answer.get(key)
        if isinstance(items, dict):
            items = list(items.values())
        if isinstance(items, list):
            for item in items[:10000]:
                if isinstance(item, dict):
                    values += [item.get(name) for name in ITEM_URL_KEYS]
    for value in values:
        if isinstance(value, str) and value.startswith("https://"):
            origin = get_origin(value)
            host = urlsplit(value).hostname
            if origin and host:
                yield origin, host
