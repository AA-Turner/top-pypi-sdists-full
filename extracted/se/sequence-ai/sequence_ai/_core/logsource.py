"""
The reading layer of `seq policy logs`: one abstract `LogSource`, one backend per tier, the query, merge, join and
attribution written once.

In one sentence: the CLI calls `LogSource.logs(deployment)` / `.logs_for_rid(deployment, rid)`, which merge the lines
of two sinks - the gateway's `connect.*` lines and the worker's `act.*` lines - strictly within the deployment, parse
them into `LogRecord`s that keep their structure, and for `--rid` join the worker's phases (from its log lines) with
the client's timing (from the stored `request_latency` rows) by rid, order them by when each was emitted, time each hop
and attribute a failure to the worker or to connect. Only the three fetches (connect lines, worker lines, latency rows)
differ by backend: the real one reads the gateway's read-only endpoints (seq/_observe_gateway.GatewayLogSource), the
tests' stands in for it - so a test that passes on the stand-in says something about the real one.

What holds (and can be checked):
  * scope: with several deployments' lines about, every line of the one asked for comes and none of another's;
  * merge: one result holds both sources, connect.* and act.*;
  * rid join: the worker's phase comes from its log lines, the client's timing from request_latency rows; a side
    missing is said to be missing;
  * order: by the timestamp each entry was emitted with, never a database's created_at; adjacent phases give each
    hop's dt;
  * failure: on the worker's side → its act.fail line; before the worker wrote a line (402 / 401 / 503 / connect /
    network) → attributed from the connect side; a rid with no record at all (never carried into connect) → said
    (rid_gap), never an empty answer;
  * redaction: a platform secret the CLI itself handles (direct_secret / lease / JWT / SEQUENCES_API_KEY) prints as ***.
"""
from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable, Optional



_SECRET_KEYS = ("direct_secret", "secret", "lease", "lease_token", "jwt", "token",
                "authorization", "api_key", "sequences_api_key")
_REDACTED = "***"


_KV = re.compile(r'(\w[\w.]*)=("(?:[^"\\]|\\.)*"|\S+)')


def redact(fields: dict[str, str]) -> dict[str, str]:
    """`fields` with each platform secret's value as *** (keys matched case-insensitively): what the CLI itself handles;
    a stored row is not this side's to un-redact."""
    out: dict[str, str] = {}
    for k, v in fields.items():
        out[k] = _REDACTED if k.lower() in _SECRET_KEYS else v
    return out


@dataclass
class LogRecord:
    """One parsed line that keeps its structure - not a lump of raw text; `fields` are read by key.

    ts_ms is when the entry was emitted, from its metadata (not parsed from the line, and not a database's created_at,
    which ordered badly in production). source is "connect" or "worker": which of the two sinks it came from.
    """

    ts_ms: float
    ev: str
    source: str
    rid: Optional[str] = None
    fields: dict[str, str] = field(default_factory=dict)

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        return self.fields.get(key, default)

    def redacted(self) -> "LogRecord":
        """The same line with each platform secret's value as *** (called before a verbose print)."""
        return LogRecord(ts_ms=self.ts_ms, ev=self.ev, source=self.source, rid=self.rid,
                         fields=redact(self.fields))


def parse_line(text: str) -> Optional[dict[str, str]]:
    """`seq ev=<ev> rid=<rid> k=v ...` as {k: v}: the structure kept, each value read by its key.

    A line of another shape (no `ev=`) is None: an implementation that handed raw text back whole would fail here.
    """
    kvs = {m.group(1): _unquote(m.group(2)) for m in _KV.finditer(text)}
    if "ev" not in kvs:
        return None
    return kvs


def _unquote(v: str) -> str:
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        return v[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return v


@dataclass
class RidTimeline:
    """What `--rid` returns: the chain ordered by when each line was emitted, with each hop's timing, the client's timing
    and where a failure happened."""

    rid: str
    records: list[LogRecord]
    hops: list[dict]
    client_timing: Optional[dict]
    worker_phase: Optional[str]
    failure_stage: Optional[str]
    failure_detail: Optional[str] = None
    rid_gap: bool = False


    cause_rid: Optional[str] = None

    def redacted(self) -> "RidTimeline":
        return RidTimeline(
            rid=self.rid,
            records=[r.redacted() for r in self.records],
            hops=self.hops,
            client_timing=(redact({k: str(v) for k, v in self.client_timing.items()})
                           if self.client_timing else None),
            worker_phase=self.worker_phase,
            failure_stage=self.failure_stage,
            failure_detail=self.failure_detail,
            rid_gap=self.rid_gap,
            cause_rid=self.cause_rid,
        )


class LogSource(ABC):
    """Query, merge, join, order and attribution, all here; only the three fetches below differ by backend."""


    @abstractmethod
    def _connect_entries(self, deployment: str) -> Iterable[tuple[float, str]]:
        """The deployment's `connect.*` lines from the gateway's sink, as (emit_ts_ms, raw_line)."""

    @abstractmethod
    def _worker_entries(self, deployment: str) -> Iterable[tuple[float, str]]:
        """The deployment's `act.*` lines from the worker's stdout sink, as (emit_ts_ms, raw_line)."""

    def _refused_entries(self, deployment: str) -> Iterable[tuple[float, str]]:
        """The deployment's robots' refused requests - one `connect.refused` / `ready.refused` line each, as the gateway
        lists them beside its connect lines (a gateway since 10-17) - as (emit_ts_ms, raw_line); none from a backend
        that keeps none."""
        return ()

    @abstractmethod
    def _latency_rows(self, deployment: str) -> Iterable[dict]:
        """The deployment's request_latency rows (stored as clients report them, keyed by rid): where the client's wall-clock
        timing comes from."""


    def _records(self, deployment: str) -> list[LogRecord]:
        """Both sinks' lines merged, parsed and ordered by ts; the backend's two fetches keep it to the deployment."""
        recs: list[LogRecord] = []

        for source, entries in (("connect", self._connect_entries(deployment)),
                                 ("connect", self._refused_entries(deployment)),
                                 ("worker", self._worker_entries(deployment))):
            for ts_ms, line in entries:
                kvs = parse_line(line)
                if kvs is None:
                    continue
                ev = kvs.pop("ev")
                rid = kvs.pop("rid", None)
                recs.append(LogRecord(ts_ms=float(ts_ms), ev=ev, source=source, rid=rid, fields=kvs))
        recs.sort(key=lambda r: r.ts_ms)
        return recs

    def logs(self, deployment: str) -> list[LogRecord]:
        """`seq policy logs <deployment>`: every structured line of the deployment, both sinks merged, in time order."""
        return self._records(deployment)

    def logs_for_rid(self, deployment: str, rid: str) -> RidTimeline:
        """`seq policy logs <deployment> --rid`: that rid's lines only, both sources joined on it, ordered by when each was
        emitted, each hop timed and a failure attributed. An act the platform refused is followed to its refusal: the
        line of the request the refusal was answered under (its latency row's error_request_id) is in its records, and
        the failure is the refusal's."""
        row = self._latency_row_for(deployment, rid)
        cause = (row or {}).get("error_request_id")
        cause = cause if isinstance(cause, str) and cause and cause != rid else None
        recs = [r for r in self._records(deployment) if r.rid == rid or (cause is not None and r.rid == cause)]
        client = self._client_timing_of(row)


        hops: list[dict] = []
        prev: Optional[float] = None
        for r in recs:
            hops.append({"ev": r.ev, "source": r.source, "ts_ms": r.ts_ms,
                         "dt_ms": None if prev is None else round(r.ts_ms - prev, 3)})
            prev = r.ts_ms


        worker_phase: Optional[str] = None
        for r in recs:
            if r.source == "worker" and r.ev in ("act.done", "act.fail"):
                worker_phase = r.ev

        stage, detail = self._attribute_failure(recs, worker_phase, client)

        rid_gap = not recs and client is None
        return RidTimeline(rid=rid, records=recs, hops=hops, client_timing=client,
                           worker_phase=worker_phase, failure_stage=stage, failure_detail=detail,
                           rid_gap=rid_gap, cause_rid=cause)

    def _latency_row_for(self, deployment: str, rid: str) -> Optional[dict]:
        """The rid's request_latency row as the client reported it; None without one."""
        return next((row for row in self._latency_rows(deployment) if row.get("rid") == rid), None)

    def _client_timing_for(self, deployment: str, rid: str) -> Optional[dict]:
        return self._client_timing_of(self._latency_row_for(deployment, rid))

    @staticmethod
    def _client_timing_of(row: Optional[dict]) -> Optional[dict]:
        """A request_latency row's client wall clock (total / rtt / network), with the worker's time and, for the first
        act after a connect, the connect, the TCP connect and the TLS handshake it paid; None without a row (never made
        up)."""
        if row is None:
            return None
        return {k: row.get(k) for k in ("total_ms", "rtt_ms", "network_ms", "handler_ms", "inference_ms",
                                        "first_after_connect", "connect_ms", "tcp_ms", "tls_ms", "outcome")}

    @staticmethod
    def _attribute_failure(recs: list[LogRecord], worker_phase: Optional[str],
                           client: Optional[dict]) -> tuple[Optional[str], Optional[str]]:
        """Both kinds of failure: (a) on the worker's side - an act.fail line - is stage "worker"; (b) one before the
        worker wrote a line (402 / 401 / 503 / connect / network) has no act.fail and is attributed from the connect
        side's records.
        """
        if worker_phase == "act.fail":
            fail = next((r for r in recs if r.source == "worker" and r.ev == "act.fail"), None)
            detail = (fail.get("err") or fail.get("status") or "worker act failed") if fail else None
            return "worker", detail

        for r in recs:
            if r.source != "connect":
                continue
            status = r.get("status")
            ev = r.ev
            if ev.endswith(".refused"):

                return "connect", f"refused ({r.get('reason') or r.get('code')}, status {status})"
            if ev in ("connect.error", "connect.warming") or status in ("402", "401", "503"):
                st = status or ""
                if st in ("503",) or ev == "connect.warming":
                    return "connect", f"warming/503 before worker ({ev} status={status})"
                if st in ("402", "401"):
                    return "connect", f"auth/balance rejected ({ev} status={status})"
                return "network", f"connect/network failure ({ev} status={status})"

        if worker_phase == "act.done" or (client and client.get("outcome") == "served"):
            return None, None

        if recs or client:
            return None, None
        return None, None
