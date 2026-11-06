"""
The commands `seq policy logs` / `seq policy doctor`: LogSource's and Diagnostics' results printed, secrets redacted.

In one sentence: the CLI's subcommands land here - `cmd_logs` reads the log as events (a request's timeline through
LogSource.logs_for_rid with --rid), `cmd_doctor` calls Diagnostics.run, and a timeline prints through `redacted()` (a
platform secret becomes ***); the data comes from the gateway's read-only endpoints, which authorize on the server (the
CLI never reads logs with the caller's own cloud credentials).
doctor's sections run on the gateway, and this prints its report; the tests replace `_real_logsource` /
`_real_diagnostics`.

The old `--fixture` (an offline sample) is gone: the platform is the one place things run, and the mock is the SDK's own
tests'.

"""
from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from datetime import datetime

from seq import clock
from sequence_ai._core.money import per_hour
from sequence_ai._core import diagnostics as dx
from sequence_ai._core.logsource import RidTimeline



def _at(ts_ms) -> str:
    """Epoch milliseconds as the time of day here, 14:05:09.149 (the day and zone are on the line above)."""
    return clock.stamp(ts_ms, unit="milli", day="never", zone=False, ms=True)


def _day_head(days: clock.Days, ts_ms) -> str | None:
    t = clock.instant(ts_ms, ms=True)
    return days.head(t) if t else None


def _ms_of(value) -> Optional[float]:
    """A timing as a page row or a redacted timeline holds it - a number, or its text ("412.5", "None") - else None."""
    if value is None or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _split(row: dict) -> Optional[dict]:
    """One act's time in its parts, as its robot's SDK and its worker measured them: the connect before the first act
    after one, the TCP connect and TLS handshake of a connection the act opened, the transfer (the round trip less the
    worker, TCP and TLS) and the worker's own handling, the policy's inference in it. None without both the round trip
    and the worker's time.
"""
    rtt, worker = _ms_of(row.get("rtt_ms")), _ms_of(row.get("handler_ms"))
    if rtt is None or worker is None:
        return None
    connect, tcp, tls = (_ms_of(row.get(k)) for k in ("connect_ms", "tcp_ms", "tls_ms"))
    network = max(0.0, rtt - worker)
    return {"connect": connect, "TCP": tcp, "TLS": tls, "transfer": max(0.0, network - (tcp or 0.0) - (tls or 0.0)),
            "worker": worker,
            "inference": _ms_of(row.get("inference_ms"))}


def _said_split(parts: dict) -> str:
    """The parts in that order, the ones measured: "connect 412 ms · TCP 88 ms · TLS 176 ms · transfer 120 ms · worker
    140 ms (inference 139)"."""
    def whole(ms: float) -> int:
        return int(ms + 0.5)

    said = [f"{name} {whole(parts[name])} ms" for name in ("connect", "TCP", "TLS", "transfer")
            if parts.get(name) is not None]
    inference = parts.get("inference")
    said.append(f"worker {whole(parts['worker'])} ms" + (f" (inference {whole(inference)})" if inference is not None
                                                          else ""))
    return " · ".join(said)


def _timed(parts: dict) -> bool:
    """Whether a split says any of the connect, TCP or TLS - the parts the legend explains."""
    return any(parts.get(name) is not None for name in ("connect", "TCP", "TLS"))


_SPLIT_LEGEND = ("connect: the platform handing the robot its worker, before the first act on it; TCP and TLS: opening "
                 "the connection to the worker; transfer: the request and its reply on the way")




_WORKER_NAME = re.compile(r"[a-z]+\d{4}")


def _worker_name(label) -> str | None:
    """`label` when it is a worker's name, a0001 - as `seq policy status` lists the worker - else None."""
    return label if isinstance(label, str) and _WORKER_NAME.fullmatch(label) else None


def _record_json(r) -> dict:
    return {"ts_ms": r.ts_ms, "ev": r.ev, "source": r.source, "rid": r.rid, "fields": dict(r.fields)}


def _timeline_json(tl: RidTimeline) -> dict:
    return {"rid": tl.rid, "records": [_record_json(r) for r in tl.records], "hops": tl.hops,
            "client_timing": tl.client_timing, "worker_phase": tl.worker_phase, "failure_stage": tl.failure_stage,
            "failure_detail": tl.failure_detail, "rid_gap": tl.rid_gap}



_WORDS = ("detail", "hint")
_ESCAPED = re.compile(r"\\(.)|_")


def _words(field: str) -> str:
    """A words field as the text it was - quoted, as it holds spaces: `\\n` a line break, `\\\\` a backslash, `\\_`
    an underscore, `_` a space (sequence-base unescape_text, which this package need not have)."""
    def one(m: re.Match) -> str:
        if m.group(1) is None:
            return " "
        return {"n": "\n", "\\": "\\", "_": "_"}.get(m.group(1), m.group(0))

    return '"' + _ESCAPED.sub(one, field) + '"'


def format_rid_timeline(tl: RidTimeline) -> str:
    out = [f"rid {tl.rid}"]
    if tl.rid_gap:
        out.append("  ! rid gap: no connect-side or worker-side record and no client timing")
        out.append("    (upstream did not thread this rid into the connect record — cannot correlate)")
        return "\n".join(out)
    days = clock.Days()
    for h, r in zip(tl.hops, tl.records):
        head = _day_head(days, h["ts_ms"])
        if head:
            out.append(f"  {head}")
        dt = "" if h["dt_ms"] is None else f"  (+{h['dt_ms']:.1f}ms)"
        kv = " ".join(f"{k}={_words(v) if k in _WORDS else v}" for k, v in r.fields.items())

        under = f" (request {r.rid})" if r.rid and r.rid != tl.rid else ""
        out.append(f"  {_at(h['ts_ms'])}  [{r.source:7}] {r.ev}{under}{dt}  {kv}".rstrip())
    if tl.client_timing:
        out.append(f"  client timing: {tl.client_timing}")
        parts = _split(tl.client_timing)
        if parts:
            out.append(f"  where it went: {_said_split(parts)}")
            if _timed(parts):
                out.append(f"    ({_SPLIT_LEGEND})")
    else:
        out.append("  client timing: (none persisted for this rid)")
    out.append(f"  worker phase: {tl.worker_phase or '(no worker-side record)'}")
    if tl.failure_stage:
        out.append(f"  FAILURE stage={tl.failure_stage}: {tl.failure_detail}")
    return "\n".join(out)


def format_doctor(rep: dx.DoctorReport) -> str:
    out = [f"doctor {rep.deployment}: {rep.overall.upper()}"]
    for s in rep.segments:
        mark = {"ok": "OK ", "fail": "FAIL", "warming": "WARM", "skipped": "-- ", "warn": "WARN"}.get(s.status, "?")
        extra = f"  {s.extra}" if s.extra else ""
        out.append(f"  [{mark}] {s.name}: {s.detail}{extra}")
    if rep.overall == dx.WARMING:
        out.append(f"  warming: retry_after_s={rep.retry_after_s}  eta_s={rep.eta_s}")
    return "\n".join(out)



def since_epoch(text, *, now: Optional[float] = None) -> float:
    """--since as epoch seconds: a span back from now ("90s", "30m", "2h", "1d") or an ISO-8601 time - and, from a
    script (seq.policy_logs(since=...)), a datetime (one with no zone in UTC) or epoch seconds as a number.
    {worker 3 on dev 10-29: since=time.time() - 3600 raised TypeError from inside the time pattern}"""
    import time as _time
    from datetime import datetime, timezone

    from sequence_ai.errors import InvalidRequest

    if isinstance(text, datetime):
        return (text if text.tzinfo else text.replace(tzinfo=timezone.utc)).timestamp()
    if isinstance(text, (int, float)) and not isinstance(text, bool):
        return float(text)
    m = re.fullmatch(r"\s*(\d+(?:\.\d+)?)\s*([smhd])\s*", text or "")
    if m:
        return (_time.time() if now is None else now) - float(m.group(1)) * {"s": 1, "m": 60, "h": 3600, "d": 86400}[
            m.group(2)]
    try:
        t = datetime.fromisoformat(str(text).strip().replace("Z", "+00:00"))
    except ValueError:
        raise InvalidRequest(f"--since {text!r} is not a time: 30m, 2h, 1d, or 2026-10-18T12:00:00Z") from None
    return (t if t.tzinfo else t.replace(tzinfo=timezone.utc)).timestamp()


def before_point(text, *, now: Optional[float] = None) -> tuple[Optional[int], Optional[float]]:
    """--before as the point a page of a log ends at: (its number, None) for a line's number in the log - its `seq`,
    as a page's last line says it and `seq --json` gives it - or (None, epoch seconds) for a time, in --since's forms;
    from a script an int is a line's number, and a float (epoch seconds) or a datetime a time.
    """
    from datetime import datetime

    from sequence_ai.errors import InvalidRequest

    if isinstance(text, (datetime, float)):
        return None, since_epoch(text, now=now)
    said = str(text).strip()
    if said.isdigit():
        return int(said), None
    try:
        return None, since_epoch(said, now=now)
    except InvalidRequest:
        raise InvalidRequest(f"--before {text!r} is neither a line's number nor a time: a number the log gave, 30m, "
                             "2h, 1d, or 2026-10-18T12:00:00Z") from None


def _kept_said(by_kind: dict) -> Optional[str]:
    """How long the platform keeps the log's lines, kind by kind, in a line: the shortest-kept named, the rest said
    as one."""
    if not by_kind:
        return None
    days = sorted({int(d) for d in by_kind.values() if isinstance(d, (int, float))})
    if len(days) < 2:
        return f"kept {days[0]} days" if days else None
    named = {"act": "acts", "print": "prints", "refused": "refused requests"}
    parts = [f"{' and '.join(named.get(k, k) for k, d in by_kind.items() if d == day)} {day} days" for day in days[:-1]]
    return f"kept: {', '.join(parts)}, everything else {days[-1]} days"


def _since_back(source, deployment: str, page: dict, *, every: bool, worker: Optional[str], since: float) -> dict:
    """--since: every event since then - the page the platform answered and each one before it while it `has_older`,
    read by `before_seq` (its oldest event's), to the first. Before, it read at most 10 pages, the newest 5,000 lines,
    and said the console's Logs tab paged back to the rest.
"""
    events, older = list(page.get("events") or []), page.get("has_older")
    while older:
        seqs = [e["seq"] for e in events if isinstance(e.get("seq"), int)]
        if not seqs:
            break
        back = source.events(deployment, every=every, worker=worker, since=since, before_seq=min(seqs))
        if not back.get("events"):
            break
        events = list(back["events"]) + events
        older = back.get("has_older")
    return {**page, "events": events, "has_older": bool(older)}




PURPOSE = {"deploy_check": "deploy check", "replica_check": "replica check", "serving": "serving", "eval": "eval"}


def _machine_name(m: dict) -> str:
    """A machine as its lines are led by it: its worker's label and what it was for, "a0001 · deploy check"."""
    label = m.get("label") or f"machine {m.get('machine')}"
    return f"{label} · {PURPOSE.get(m.get('purpose'), 'purpose not recorded')}"


def _machine_price(m: dict) -> Optional[str]:
    """What an hour of a machine costs its owner, as the platform says it: one worker's price on its card, said as a
    worker's as `seq policy status` says it ("$0.9612/h a worker": the card with its CPU and memory, more than the card
    alone), for a machine that serves or checks a deploy; "billed with its eval" for an eval's machine, which its eval
    bills for what its run used. None where the platform gave no price: a machine whose purpose is not recorded (it could
    have been either), a card it does not price. No machine is said to be free: every one the platform starts for its
    user is billed from when it starts, and no replica check runs any more.

 
"""
    if m.get("purpose") == "eval":
        return "billed with its eval"
    v = m.get("usd_per_hour")
    return f"{per_hour(v)} a worker" if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def _machines_said(machines: list[dict]) -> list[str]:
    """The machines themselves, before their lines: when each started, was ready and stopped, how long it took to load
    its policy, its card and what an hour of it costs (_machine_price) - "stop not recorded" for one that stopped before
    the platform kept stops (10-12), "running" for one with no stop yet.
"""
    shown = sorted(machines, key=lambda m: int(m.get("machine") or 0))
    if not shown:
        return []
    width = max(len(_machine_name(m)) for m in shown)
    out = ["machines:"]
    for m in shown:
        said = [f"started {clock.stamp(m.get('started_ms'), unit='second', ms=True)}"]
        if m.get("ready_ms") is not None:
            said.append(f"ready {clock.stamp(m['ready_ms'], unit='second', ms=True)}")
        if m.get("load_s") is not None:
            said.append(f"loaded in {float(m['load_s']):.1f} s")
        if m.get("stopped_ms") is not None:
            said.append(f"stopped {clock.stamp(m['stopped_ms'], unit='second', ms=True)}")
        else:
            said.append("stop not recorded" if m.get("stop_recorded") is False else "running")
        if m.get("card"):
            said.append(f"on {m['card']}")

        if price := _machine_price(m):
            said.append(price)
        out.append(f"  {_machine_name(m):<{width}}  " + " · ".join(said))
    return out


def format_events(page: dict, deployment: str, *, flags: str = "") -> str:
    """The log as events, a line each: when, the machine that wrote it and what that machine was for ("a0001 · deploy
    check", _machine_name), what happened - a robot's acts in one run and a print the policy repeated folded into one
    with when they ended (seq policy logs --all: every one), what the policy printed marked when it was while it loaded
    or on its stderr - and how long it is kept. First the machines themselves (_machines_said). The policy's planning, which a
    gateway sends beside the first page (`plan`: plans, failed, p50_ms, p95_ms, cost_usd), is not printed here."""
    machines = {m["machine"]: m for m in page.get("machines") or [] if isinstance(m, dict) and m.get("machine")}
    lines = _machines_said(list(machines.values()))
    named = {n: _machine_name(m) for n, m in machines.items()}
    width = max([11, *map(len, named.values())])
    for e in page.get("events") or []:
        who = named.get(e.get("machine")) or _worker_name(e.get("worker")) or (
            f"machine {e['machine']}" if e.get("machine") else str(e.get("worker") or "-"))
        text = str(e.get("text") or "")
        if e.get("kind") == "user":


            tags = ((["setup"] if e.get("setup") else []) + (["shutdown"] if e.get("shutdown") else [])
                    + (["stderr"] if e.get("stream") == "stderr" else []))
            text = f"({', '.join(tags)}) {text}" if tags else text
        until = e.get("billed_until")
        if e.get("kind") == "end" and isinstance(until, (int, float)) and not isinstance(until, bool):



            text = text.replace("billed up to this time", f"billed up to {clock.stamp(until, unit='second')}")
        if e.get("kind") == "start" and e.get("reason") == "check" and e.get("build_version"):


            text += f"  (that build: seq policy logs {deployment}@v{e['build_version']} --build)"
        if (e.get("count") or 1) > 1 and e.get("to_ts") is not None:
            text += f"  (to {clock.stamp(e['to_ts'], unit='second')})"
        lines.append(f"{clock.stamp(e.get('ts'), unit='second')}  {who:<{width}} {text}")
    if not page.get("events"):
        lines.append("(no lines yet)")
    kept = _kept_said(page.get("retention_days_by_kind") or {})
    if page.get("folded"):
        lines.append(f"each robot's acts and repeated prints are folded: seq policy logs {deployment} --all shows "
                     "every one")
    if page.get("has_older"):


        first = min((e["seq"] for e in page.get("events") or [] if isinstance(e.get("seq"), int)), default=None)
        lines.append(f"older lines are kept: seq policy logs {deployment}{flags} --before {first} reads the page before "
                     "these; --since 1d (or another time) reads every line back to then" if first is not None else
                     f"older lines are kept: seq policy logs {deployment}{flags} --since 1d (or another time) reads "
                     "back to them")
    if kept:
        lines.append(kept)
    return "\n".join(lines)


def policy_logs(name: str, *, since: str | float | datetime | None = None,
                before: int | str | float | datetime | None = None, worker: Optional[str] = None,
                every: bool = False, base_url: Optional[str] = None, echo=None) -> dict:
    """`seq policy logs <name> [--since WHEN] [--before WHEN|SEQ] [--worker W] [--all]`, its own function: the log as
    events - the newest page, the page before `before` (a line's number, or a time: the page before the first event at
    it), or every event since `since`, read back a page at a time - as the platform answered them, oldest first. A time
    is --since's words, epoch seconds or a datetime (since_epoch); an int `before` is a line's number (before_point).
    Printed only through `echo`, as format_events says them.
"""

    after = since_epoch(since) if since not in (None, "") else None
    end, when = before_point(before) if before is not None else (None, None)
    source = _real_logsource(base_url)
    if when is not None:


        first = source.events(name, every=every, worker=worker, since=when, after_seq=0)
        end = min((e["seq"] for e in first.get("events") or [] if isinstance(e.get("seq"), int)), default=None)
    page = source.events(name, every=every, worker=worker, since=after,
                         **({"before_seq": end} if end is not None else {}))
    if after is not None:
        page = _since_back(source, name, page, every=every, worker=worker, since=after)
    if echo is not None:
        echo(format_events(page, name, flags=(" --all" if every else "") + (f" --worker {worker}" if worker else "")))
    return page


def cmd_logs(deployment: str, *, rid: Optional[str] = None, base_url: Optional[str] = None,
             as_json: bool = False, every: bool = False, worker: Optional[str] = None,
             since: Optional[str] = None, before: Optional[str] = None) -> int:
    """`seq policy logs <deployment> [--rid r-…] [--all] [--worker W] [--since 2h] [--before WHEN|SEQ]`, from the
    gateway's read-only endpoint (authorized on the server): the log as events, folded unless --all (policy_logs), or
    with --rid the request's timeline through `LogSource`'s queries. With `as_json` (`seq --json policy logs`): what the
    platform sent - the events - or the request's timeline, its platform secrets masked as the printed form masks
    them."""
    if rid:
        tl = _real_logsource(base_url).logs_for_rid(deployment, rid).redacted()
        print(json.dumps(_timeline_json(tl), indent=2) if as_json else format_rid_timeline(tl))
        return 0
    got = policy_logs(deployment, since=since, before=before, worker=worker, every=every, base_url=base_url,
                      echo=None if as_json else print)
    if as_json:
        print(json.dumps(got, indent=2))
    return 0


def cmd_doctor(deployment: str, *, base_url: Optional[str] = None) -> int:
    """`seq policy doctor <deployment>`, from the gateway's `/diagnostics` endpoint: the sectioned diagnosis runs on the
    server (authorized there)."""
    diag = _real_diagnostics(base_url)
    rep = diag.run(deployment)
    print(format_doctor(rep))
    return 0 if rep.overall != dx.FAIL else 1


def _real_logsource(base_url: Optional[str]):
    """LogSource over the gateway's owner-scoped read-only endpoints (authorized server-side)."""
    from seq._observe_gateway import GatewayLogSource
    return GatewayLogSource(base_url=base_url)


def _real_diagnostics(base_url: Optional[str]):
    from seq._observe_gateway import GatewayDiagnostics
    return GatewayDiagnostics(base_url=base_url)
