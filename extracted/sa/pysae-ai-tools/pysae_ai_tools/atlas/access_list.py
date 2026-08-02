"""Add or remove the current IP address from a MongoDB Atlas project IP access list.

Usage:
    pysae-ai-tools atlas access-list add \
        --project-id 5f919336b8532e2c6c30ea94 \
        [--comment "CI runner"] \
        [--duration 2h] \
        [--wait mongodb+srv://cluster.mongodb.net --wait-timeout 90]

    pysae-ai-tools atlas access-list remove \
        --project-id 5f919336b8532e2c6c30ea94 \
        [--ip 1.2.3.4]

Requires MONGODB_ATLAS_PUBLIC_KEY and MONGODB_ATLAS_PRIVATE_KEY environment variables.
Uses the Atlas Administration API v2 with HTTP Digest authentication.

Output (JSON, one line):
    {"action": "added", "ip": "1.2.3.4", "project_id": "...", "delete_after": "..."}
    {"action": "already_exists", "ip": "1.2.3.4", "matched_entry": "10.0.0.0/8"}
    {"action": "removed", "ip": "1.2.3.4"}
    {"error": "..."}
"""

import ipaddress
import json
import os
import sys
import time
import urllib.parse
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

import httpx
import typer
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure, ServerSelectionTimeoutError

from ..common.duration import parse_duration

ATLAS_API_BASE = "https://cloud.mongodb.com/api/atlas/v2"
IPIFY_URL = "https://api4.ipify.org/"
ATLAS_ACCEPT_HEADER = "application/vnd.atlas.2023-02-01+json"


# ---------------------------------------------------------------------------
# Atlas API client
# ---------------------------------------------------------------------------


class AtlasApiError(Exception):
    def __init__(self, status_code: int, detail: str, error_code: str = ""):
        super().__init__(f"Atlas API error {status_code}: {detail} ({error_code})")
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code


def _make_client(public_key: str, private_key: str) -> httpx.Client:
    return httpx.Client(
        auth=httpx.DigestAuth(public_key, private_key),
        headers={"Accept": ATLAS_ACCEPT_HEADER},
        timeout=15.0,
    )


def _raise_for_status(response: httpx.Response) -> None:
    if response.is_success:
        return
    try:
        error_data = response.json()
        detail = error_data.get("detail", response.text)
        error_code = error_data.get("errorCode", "")
    except (json.JSONDecodeError, ValueError):  # fmt: skip
        detail = response.text
        error_code = ""
    raise AtlasApiError(response.status_code, detail, error_code)


# ---------------------------------------------------------------------------
# Public IP detection
# ---------------------------------------------------------------------------


def get_current_ip() -> str:
    """Get the current public IPv4 address via ipify."""
    response = httpx.get(IPIFY_URL, timeout=10.0)
    response.raise_for_status()
    return response.text.strip()


# ---------------------------------------------------------------------------
# Access list operations
# ---------------------------------------------------------------------------


@dataclass
class AccessListResult:
    action: str
    ip: str
    project_id: str = ""
    matched_entry: str = ""
    delete_after: str = ""
    error: str = ""

    def to_json(self) -> str:
        d: dict[str, str] = {"action": self.action, "ip": self.ip}
        if self.project_id:
            d["project_id"] = self.project_id
        if self.matched_entry:
            d["matched_entry"] = self.matched_entry
        if self.delete_after:
            d["delete_after"] = self.delete_after
        if self.error:
            d["error"] = self.error
        return json.dumps(d)


def _parse_duration(duration_str: str) -> timedelta:
    """Parse a duration string like '2h', '30m', '1d' into a timedelta."""
    try:
        return parse_duration(duration_str, allow_bare=False, allowed_units="hmd")
    except ValueError:
        raise ValueError(f"Invalid duration format: {duration_str} (expected: 2h, 30m, 1d)") from None


def _ip_matches_entry(ip_str: str, entry: dict[str, object]) -> bool:
    """Check if an IP address matches an access list entry (exact or CIDR)."""
    ip_obj = ipaddress.ip_address(ip_str)
    entry_ip = entry.get("ipAddress")
    if isinstance(entry_ip, str) and entry_ip == ip_str:
        return True
    cidr = entry.get("cidrBlock")
    if isinstance(cidr, str):
        try:
            if ip_obj in ipaddress.ip_network(cidr, strict=False):
                return True
        except ValueError:
            pass
    return False


def _entry_covers_duration(entry: dict[str, object], duration: timedelta | None) -> bool:
    """Check if an existing entry will remain active for the requested duration."""
    if duration is None:
        # No duration requested — permanent entry or any expiry is fine
        delete_after = entry.get("deleteAfterDate")
        return delete_after is None  # Only permanent entries match when no duration is requested
    delete_after_str = entry.get("deleteAfterDate")
    if delete_after_str is None:
        # Permanent entry covers any duration
        return True
    if not isinstance(delete_after_str, str):
        return False
    try:
        delete_after_dt = datetime.fromisoformat(delete_after_str.replace("Z", "+00:00"))
        return datetime.now(tz=timezone.utc) + duration <= delete_after_dt
    except ValueError:
        return False


def add_ip(
    client: httpx.Client,
    project_id: str,
    ip_address: str | None = None,
    comment: str = "claude-code",
    duration: timedelta | None = None,
) -> AccessListResult:
    """Add the current IP to the Atlas project access list.

    If the IP already exists (exact or in a CIDR range) and covers the
    requested duration, skip the creation.
    """
    if ip_address is None:
        ip_address = get_current_ip()

    # Check existing entries
    response = client.get(f"{ATLAS_API_BASE}/groups/{project_id}/accessList")
    _raise_for_status(response)
    data = response.json()
    results = data.get("results", [])
    if isinstance(results, list):
        for entry in results:
            if not isinstance(entry, dict):
                continue
            if _ip_matches_entry(ip_address, entry) and _entry_covers_duration(entry, duration):
                matched = str(entry.get("cidrBlock") or entry.get("ipAddress") or "")
                return AccessListResult(
                    action="already_exists",
                    ip=ip_address,
                    project_id=project_id,
                    matched_entry=matched,
                )

    # Build entry
    entry_payload: dict[str, object] = {"ipAddress": ip_address, "comment": comment}
    delete_after_iso = ""
    if duration:
        delete_after_dt = datetime.now(tz=timezone.utc) + duration
        delete_after_iso = delete_after_dt.isoformat().replace("+00:00", "Z")
        entry_payload["deleteAfterDate"] = delete_after_iso

    response = client.post(f"{ATLAS_API_BASE}/groups/{project_id}/accessList", json=[entry_payload])
    _raise_for_status(response)

    return AccessListResult(
        action="added",
        ip=ip_address,
        project_id=project_id,
        delete_after=delete_after_iso,
    )


def remove_ip(
    client: httpx.Client,
    project_id: str,
    ip_address: str | None = None,
) -> AccessListResult:
    """Remove an IP from the Atlas project access list."""
    if ip_address is None:
        ip_address = get_current_ip()

    encoded_ip = urllib.parse.quote(ip_address, safe="")
    response = client.delete(f"{ATLAS_API_BASE}/groups/{project_id}/accessList/{encoded_ip}")
    _raise_for_status(response)

    return AccessListResult(action="removed", ip=ip_address, project_id=project_id)


# ---------------------------------------------------------------------------
# Wait for MongoDB connectivity
# ---------------------------------------------------------------------------


class WaitForConnectionError(Exception):
    """Raised when wait_for_connection times out."""

    def __init__(self, uri: str, timeout: float, last_error: Exception):
        self.uri = uri
        self.timeout = timeout
        self.last_error = last_error
        super().__init__(f"Connection to {uri} timed out after {timeout}s: {last_error}")


def wait_for_connection(uri: str, timeout: float = 120.0, interval: float = 5.0) -> None:
    """Wait until a MongoDB ping command succeeds on the given URI.

    Uses pymongo to handle SRV resolution, TLS, and authentication natively.
    This validates that the Atlas IP access list change has propagated
    and the firewall now allows connections from the current IP.
    Raises WaitForConnectionError on timeout with the original error.
    """
    start = time.monotonic()
    last_error: Exception | None = None

    while time.monotonic() - start < timeout:
        try:
            client: MongoClient[dict[str, object]] = MongoClient(
                uri, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000
            )
            client.admin.command("ping")
            client.close()
            return
        except (ConnectionFailure, ServerSelectionTimeoutError, OperationFailure) as e:
            last_error = e
            elapsed = int(time.monotonic() - start)
            print(
                json.dumps({"waiting": True, "elapsed_seconds": elapsed, "last_error": str(e)}),
                file=sys.stderr,
            )
            time.sleep(interval)

    assert last_error is not None
    raise WaitForConnectionError(uri, timeout, last_error)

    return False


# ---------------------------------------------------------------------------
# CLI entry point (typer)
# ---------------------------------------------------------------------------

app = typer.Typer(help="Manage MongoDB Atlas IP access list")


def _get_atlas_client() -> httpx.Client:
    public_key = os.environ.get("MONGODB_ATLAS_PUBLIC_KEY", "")
    private_key = os.environ.get("MONGODB_ATLAS_PRIVATE_KEY", "")
    if not public_key or not private_key:
        typer.echo(json.dumps({"error": "MONGODB_ATLAS_PUBLIC_KEY and MONGODB_ATLAS_PRIVATE_KEY must be set"}))
        raise typer.Exit(1)
    return _make_client(public_key, private_key)


@app.command()
def add(
    project_id: str = typer.Option(..., help="Atlas project ID"),
    ip: str | None = typer.Option(None, help="IP address (default: auto-detect via ipify)"),
    comment: str = typer.Option("claude-code", help="Comment for the access list entry"),
    duration: str | None = typer.Option(None, help="Auto-delete after duration (e.g. 2h, 30m, 1d)"),
    wait: str | None = typer.Option(None, help="MongoDB URI — wait until connection succeeds after adding IP"),
    wait_timeout: int = typer.Option(120, help="Timeout in seconds for --wait"),
) -> None:
    """Add the current IP to the Atlas project access list."""
    client = _get_atlas_client()
    try:
        dur = _parse_duration(duration) if duration else None
        result = add_ip(client, project_id, ip, comment, dur)
        typer.echo(result.to_json())

        if wait:
            typer.echo(f"Waiting for connection to {wait} (timeout: {wait_timeout}s)...", err=True)
            wait_for_connection(wait, timeout=wait_timeout)
            typer.echo("Connected.", err=True)
    except (AtlasApiError, WaitForConnectionError, httpx.HTTPError, ValueError) as e:
        typer.echo(json.dumps({"error": str(e)}))
        raise typer.Exit(1) from e
    finally:
        client.close()


@app.command()
def remove(
    project_id: str = typer.Option(..., help="Atlas project ID"),
    ip: str | None = typer.Option(None, help="IP address (default: auto-detect via ipify)"),
) -> None:
    """Remove an IP from the Atlas project access list."""
    client = _get_atlas_client()
    try:
        result = remove_ip(client, project_id, ip)
        typer.echo(result.to_json())
    except (AtlasApiError, httpx.HTTPError, ValueError) as e:
        typer.echo(json.dumps({"error": str(e)}))
        raise typer.Exit(1) from e
    finally:
        client.close()


@app.command(name="wait-mongo")
def wait_mongo(
    uri: str = typer.Option(..., help="MongoDB URI (e.g. mongodb+srv://cluster.mongodb.net)"),
    timeout: int = typer.Option(120, help="Timeout in seconds"),
) -> None:
    """Wait until a MongoDB connection succeeds."""
    typer.echo(f"Waiting for connection to {uri} (timeout: {timeout}s)...", err=True)
    try:
        wait_for_connection(uri, timeout=timeout)
    except WaitForConnectionError as e:
        typer.echo(json.dumps({"error": str(e)}))
        raise typer.Exit(1) from e
    typer.echo("Connected.", err=True)


if __name__ == "__main__":
    app()
