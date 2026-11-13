"""Read-only access to hugpy-discovery: the export database and the request socket.

Discovery publishes two consumer surfaces (docs/discovery-wrapper-responsibilities.md:
core reads both sides read-only; discovery never listens on the LAN):

- The export directory ``/var/lib/hugpy/discovery/export``: every published
  ``api_*_v1`` view materialised into ``discovery.sqlite3`` (journal DELETE,
  group ``hugpy``), with ``discovery.json`` as the manifest. Consumers open it
  with ``file:<path>?mode=ro`` and never touch discovery's live WAL store.
- The request socket ``/run/hugpy/discovery/requests.sock``: one JSON object per
  line each way, protocol ``v`` 1. Core keeps to the read-only ops
  (``generation``, ``read``, ``unit_bytes``, ``placements``).

This module deliberately imports neither ``hugpy_discovery`` nor
``hugpy_wrapper``: ownership flows discovery -> wrapper -> core, and core only
needs the published interfaces, not the packages.
"""
from __future__ import annotations

import json
import os
import socket
import sqlite3

PROTOCOL_VERSION = 1
SHARED_SOCKET = "/run/hugpy/discovery/requests.sock"
EXPORT_DIR = "/var/lib/hugpy/discovery/export"
SETTINGS_FILE = "/etc/hugpy/discovery/settings/settings.json"


class DiscoveryError(RuntimeError):
    """Discovery could not answer: socket missing, export absent, or a refusal."""


def socket_path() -> str:
    return os.environ.get("HUGPY_DISCOVERY_SOCKET") or SHARED_SOCKET


def request(op: str, timeout: float = 30.0, **message):
    """One request over discovery's socket; the reply payload, or DiscoveryError."""
    payload = {"op": op, "v": PROTOCOL_VERSION, **message}
    path = socket_path()
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect(path)
            sock.sendall(json.dumps(payload).encode() + b"\n")
            chunks = []
            while not chunks or b"\n" not in chunks[-1]:
                chunk = sock.recv(1 << 16)
                if not chunk:
                    break
                chunks.append(chunk)
    except OSError as exc:
        raise DiscoveryError(f"discovery socket {path}: {exc}") from exc
    raw = b"".join(chunks).split(b"\n", 1)[0]
    if not raw:
        raise DiscoveryError("discovery closed the connection without answering")
    reply = json.loads(raw)
    if not isinstance(reply, dict):
        raise DiscoveryError("discovery sent a non-object reply")
    if reply.get("error"):
        raise DiscoveryError(str(reply["error"]))
    return reply


def generation() -> dict:
    """The api_meta_v1 row over the socket: interface_version, generation, changed_at."""
    return request("generation")


def read_view(view: str, where: dict | None = None, limit: int | None = None) -> list[dict]:
    """Rows of a published ``api_<name>_v<N>`` view over the socket."""
    message = {"view": view}
    if where:
        message["where"] = where
    if limit:
        message["limit"] = limit
    reply = request("read", **message)
    return reply.get("rows") or []


# ── the export database ───────────────────────────────────────────────────────
def export_dir() -> str:
    explicit = os.environ.get("HUGPY_DISCOVERY_EXPORT")
    if explicit:
        return explicit
    try:
        with open(SETTINGS_FILE) as source:
            profile = (json.load(source).get("profiles") or {}).get("local") or {}
        output = profile.get("discovery_output")
        if output:
            return os.path.join(output, "export")
    except (OSError, ValueError):
        pass
    return EXPORT_DIR


def export_db() -> str:
    return os.path.join(export_dir(), "discovery.sqlite3")


def manifest() -> dict | None:
    """The export manifest (generation, refreshed_at, files, views), or None."""
    try:
        with open(os.path.join(export_dir(), "discovery.json")) as source:
            return json.load(source)
    except (OSError, ValueError):
        return None


def connect(path: str | None = None) -> sqlite3.Connection:
    """Open the export read-only. Raises DiscoveryError when it is not readable."""
    path = path or export_db()
    if not os.access(path, os.R_OK):
        raise DiscoveryError(f"discovery export not readable: {path}")
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def export_generation(conn: sqlite3.Connection | None = None) -> str | None:
    """The export's api_meta_v1 generation; compare for equality only."""
    own = conn is None
    try:
        conn = conn or connect()
    except DiscoveryError:
        return None
    try:
        row = conn.execute("SELECT generation FROM api_meta_v1").fetchone()
        return row[0] if row else None
    except sqlite3.Error:
        return None
    finally:
        if own:
            conn.close()


def central_drives() -> list[dict]:
    """Discovery's central drives as it measured them: root, capacity, free and model budget."""
    with connect() as conn:
        return [dict(row) for row in conn.execute("SELECT * FROM api_drives_v1 WHERE role = 'central' ORDER BY root")]


def central_units() -> list[dict]:
    """What discovery lists on central, one row per model: its directory there, the central
    root, its task, the bytes of its units and whether it is a GGUF model."""
    with connect() as conn:
        return [dict(row) for row in conn.execute(
            "SELECT key, MIN(central_dir) AS dir, MIN(central_root) AS root, MIN(task) AS task, "
            "SUM(own_weight_bytes) AS bytes, MAX(gguf_model) AS gguf, COUNT(*) AS units "
            "FROM api_units_v1 WHERE central_dir IS NOT NULL AND central_dir != '' "
            "GROUP BY key ORDER BY key")]


def drive_roots() -> dict[str, list[str]]:
    """Discovery's declared drives by role, e.g. {'central': [...], 'worker': [...]}.

    Read from the export; a fleet may declare several roots per role, so every
    root is returned, in the export's order.
    """
    roots: dict[str, list[str]] = {}
    with connect() as conn:
        for row in conn.execute("SELECT role, root FROM api_drives_v1"):
            roots.setdefault(row["role"], []).append(row["root"])
    return roots
