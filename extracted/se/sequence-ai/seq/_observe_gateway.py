"""
Real-tier backends for `seq policy logs` / `seq policy doctor`: they read the gateway's owner-scoped, read-only
endpoints.

In one sentence: authorization is the server's - the CLI never reads logs with the caller's own cloud credentials; it
sends its `SEQUENCES_API_KEY` (`Authorization: Bearer …`) to the gateway's `GET /v1/deployments/{id}/logs` and
`/diagnostics`, and the gateway resolves the key to its owner (sha256 → `api_key_identity`) and answers 404 to anyone
else, so no account reads another's data. `GatewayLogSource` reuses `LogSource`'s merge, rid join, ordering and failure
attribution - the same code path as the tests' backend - and only its three fetches become HTTP GETs.

`GatewayLogSource`: one GET brings the three sources `{connect, worker, latency}`, already scoped to the deployment by
the gateway, and caches them; the three fetch methods slice that cache, and the client filters nothing by deployment
itself (scope is the server's job). `GatewayDiagnostics.run`: GET `/diagnostics`, the server's sectioned report read into
a `DoctorReport`.
"""
from __future__ import annotations

import os
from typing import Any, Optional

import httpx

from seq._account import auth_headers, credential
from seq._http import RetryReads
from seq.errors import raise_for, unreachable
from sequence_ai._core import diagnostics as dx
from sequence_ai._core.logsource import LogSource
from sequence_ai._core.names import segment

DEFAULT_BASE_URL = "https://api.generalsequences.com"
_TIMEOUT_S = 30.0


def _api_key(api_key: Optional[str], base_url: Optional[str] = None) -> Any:
    """The caller's API key: the argument, else SEQUENCES_API_KEY, else their `seq login` sign-in (seq/_account.py).
    Without one it fails before any request: nothing is ever sent anonymously."""
    return credential(api_key, base_url)


def _base_url(base_url: Optional[str]) -> str:
    return (base_url or os.environ.get("SEQUENCES_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")


def _get(base: str, key: str, path: str) -> dict:
    """One read-only GET, asked again while its connection fails (seq._http): its JSON, or the shared error mapping
    (not yours and not there are both a 404 `NotFound`: the server never says which). No secret reaches an error's
    text: these two endpoints' answers hold none."""
    try:
        with httpx.Client(base_url=base, timeout=_TIMEOUT_S, headers=auth_headers(key), transport=RetryReads()) as c:
            r = c.get(path)
    except httpx.TransportError as exc:
        raise unreachable(base, exc) from None
    raise_for(r)
    return r.json()


def read(path: str, base_url: Optional[str] = None) -> dict:
    """GET `path` with the caller's key, as `_get` reads: `seq policy logs --build`'s build."""
    return _get(_base_url(base_url), _api_key(None, base_url), path)


class GatewayLogSource(LogSource):
    """The real backend: the three sources through the gateway's read-only endpoint (authorized and scoped by the
    server); query, merge and join come from LogSource."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None) -> None:
        self._key = _api_key(api_key, base_url)
        self._base = _base_url(base_url)
        self._cache: dict[str, dict] = {}

    def _fetch(self, deployment: str) -> dict:
        if deployment not in self._cache:
            self._cache[deployment] = _get(self._base, self._key, f"/v1/deployments/{segment(deployment)}/logs")
        return self._cache[deployment]

    def events(self, deployment: str, *, every: bool = False, worker: Optional[str] = None,
               since: Optional[float] = None, before_seq: Optional[int] = None,
               after_seq: Optional[int] = None) -> dict:
        """The log as events (GET .../logs?events=1, or all=1 for every act and print on its own; one machine's alone
        with `worker`; none before `since`, epoch seconds; the page before the event `before_seq`, when the one read
        `has_older`; the page after `after_seq`, oldest first - 0, the log's first).
"""
        from urllib.parse import urlencode

        query = {("all" if every else "events"): "1", **({"worker": worker} if worker else {}),


                 **({"since": f"{since:.6f}"} if since is not None else {}),
                 **({"before_seq": str(int(before_seq))} if before_seq is not None else {}),
                 **({"after_seq": str(int(after_seq))} if after_seq is not None else {})}
        return _get(self._base, self._key, f"/v1/deployments/{segment(deployment)}/logs?{urlencode(query)}")

    def _connect_entries(self, deployment: str):
        return [(float(ts), line) for ts, line in self._fetch(deployment)["connect"]]

    def _refused_entries(self, deployment: str):

        return [(float(ts), line) for ts, line in self._fetch(deployment)["refused"]]

    def _worker_entries(self, deployment: str):
        return [(float(ts), line) for ts, line in self._fetch(deployment)["worker"]]

    def _latency_rows(self, deployment: str):
        return list(self._fetch(deployment)["latency"])


class GatewayDiagnostics:
    """The real backend: doctor's sections run on the server; this reads their report and makes it a `DoctorReport`."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None) -> None:
        self._key = _api_key(api_key, base_url)
        self._base = _base_url(base_url)

    def run(self, deployment: str) -> dx.DoctorReport:
        return _report_from_dict(deployment, _get(self._base, self._key,
                                                  f"/v1/deployments/{segment(deployment)}/diagnostics"))


def _report_from_dict(deployment: str, d: dict) -> dx.DoctorReport:
    """The gateway's `/diagnostics` JSON as a DoctorReport: a missing field is tolerated, and None stays None (never
    zero)."""
    segs = [
        dx.Segment(name=s.get("name", "?"), status=s.get("status", dx.FAIL),
                   detail=s.get("detail"), extra=s.get("extra", {}) or {})
        for s in d.get("segments", [])
    ]
    return dx.DoctorReport(
        deployment=d.get("deployment", deployment),
        segments=segs,
        overall=d.get("overall", dx.FAIL),
        retry_after_s=d.get("retry_after_s"),
        eta_s=d.get("eta_s"),
    )
