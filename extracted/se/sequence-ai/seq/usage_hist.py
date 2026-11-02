"""What your machines used and cost — `seq usage [--policy NAME] [--since WHEN] [--until WHEN] [--by hour|day]
[--group deployment|gpu|kind] [--csv]` and `seq.gpu_usage(...)`.

In one sentence: the gateway's GET /v1/account/usage sums your machines' windows into GPU card-hours (seconds x cards /
3600) per hour or day, every bucket of the window (empty ones as zero) with what its machines cost - GPU, CPU and memory,
what the balance was charged for them - optionally split by deployment, card type (a machine with no card reads CPU) or
kind of machine (policy workers, evals, build checks, weight copies) → over this billing period (the UTC month so far)
unless --since / --until name another window, in UTC days and hours, the bill's own → printed as a table with a bar per
bucket, or as CSV, or returned. `--policy` keeps one policy's rows, and adds what its robots did over the window: their
acts, errors and round trips, and how many of their action chunks came on time. A robot's key, which may read its own
policy's use and nothing of its account's, reads it per UTC day from the policy's own usage instead.

WHY one command: `seq usage`, `seq billing export` and `seq policy usage` each read the account's use their own way, over
a window and a zone of their own - the last 24 hours in this machine's zone, two dates, the last 30 days - so the same
day read three ways. They are one now, its numbers the console's Usage page's (the same SQL), its window the bill's.



"""
from __future__ import annotations

import csv
import io
import math
from datetime import datetime, timedelta, timezone
from typing import Any, Callable

from sequence_ai._core.money import money
from urllib.parse import urlencode

BAR = 28

_KIND = {"serving": "policy workers", "eval": "evals", "check": "build checks", "weights": "weight copies"}

CSV_COLUMNS = ("start", "group", "card_hours", "cost_usd")


def month_start(at: datetime) -> datetime:
    """The start of `at`'s billing period: midnight UTC on the first of its UTC month."""
    at = at.astimezone(timezone.utc)
    return at.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def _instant(value: Any, flag: str) -> datetime:
    """--since / --until as an instant: a date (midnight UTC, the bill's day), a time, or a span back from now (7d,
    24h, 30m) - as every --since of the CLI reads one (seq.listing.since_iso)."""
    from seq.listing import since_iso
    from sequence_ai.errors import InvalidRequest

    try:
        text = since_iso(value)
    except InvalidRequest:
        raise InvalidRequest(f"{flag} takes a date (2026-10-01), a time, or a span back from now (7d, 24h); "
                             f"got {value!r}") from None
    t = datetime.fromisoformat(str(text).replace("Z", "+00:00"))
    return t if t.tzinfo else t.replace(tzinfo=timezone.utc)


def gpu_usage(*, since: Any = None, until: Any = None, by: str | None = None, group: str = "none",
              policy: str | None = None, base_url: str | None = None) -> dict:
    """Your machines' use from `since` to `until` (dates, times or spans back; default this billing period, the UTC
    month so far), per hour or day in UTC (`by`; hours up to a week by default), split by `group` - or, given `policy`,
    that policy's rows alone:

        {"from", "to", "by", "tz": "UTC", "group", "policy",
         "buckets": [{"start", "group", "card_hours", "cost_usd", "deployments"}, ...],
         "total_card_hours", "total_usd"}

    card_hours counts GPU cards; cost_usd is what those machines cost, GPU, CPU and memory, so a machine without a card
    (a weights copy, a CPU policy) has a cost and no card-hours. With group "kind" a group is serving, eval, check or
    weights. A robot's key reads its policy's per UTC day (by "day")."""
    return _read(since=since, until=until, by=by, group=group, policy=policy, base_url=base_url)[0]


def _read(*, since: Any, until: Any, by: str | None, group: str, policy: str | None,
          base_url: str | None) -> tuple[dict, dict | None]:
    """gpu_usage's page, and the policy's own usage when that is what was read (a robot's key) - so its robots are
    said from the same answer, not asked again."""
    from seq.deployments_cli import _call
    from sequence_ai._core.names import segment
    from sequence_ai.errors import InvalidRequest, PermissionDenied

    if policy:
        segment(policy)
        if group not in (None, "none", "deployment"):
            raise InvalidRequest("--policy keeps one policy's rows; leave --group out")
    to = _instant(until, "--until") if until not in (None, "") else datetime.now(timezone.utc)
    start = _instant(since, "--since") if since not in (None, "") else month_start(to)
    query = {"from": start.isoformat(timespec="seconds"), "to": to.isoformat(timespec="seconds"), "by": by,
             "tz": "UTC", "group": "deployment" if policy else group}
    try:
        out = _call("GET", f"/v1/account/usage?{urlencode({k: v for k, v in query.items() if v})}", base_url)
    except PermissionDenied:
        if not policy:
            raise

        own = _call("GET", _own_path(policy, start), base_url)
        return _by_day(own, policy, start, to), own
    if policy:

        rows = [r for r in out.get("buckets") or [] if r.get("group") == policy]
        out = {**out, "group": "none", "policy": policy, "buckets": rows,
               "total_card_hours": round(sum(float(r.get("card_hours") or 0) for r in rows), 6),
               "total_usd": round(sum(float(r.get("cost_usd") or 0) for r in rows), 6)}
    return out, None


def _own_path(policy: str, start: datetime) -> str:
    """A policy's own usage from the window's start to now (GET /v1/deployments/{name}/usage?from=): its days, its
    robots' figures and its spend, the database's total. Asked from `start` itself, so its first day begins where the
    window does - asked as whole days back, it began up to a day before."""
    from sequence_ai._core.names import segment

    return f"/v1/deployments/{segment(policy)}/usage?{urlencode({'from': start.isoformat(timespec='seconds')})}"


def _by_day(own: dict, policy: str, start: datetime, to: datetime) -> dict:
    """A policy's own usage (GET /v1/deployments/{name}/usage: one row per UTC day, its card-seconds and the dollars of
    its GPU, CPU and memory) as gpu_usage's page: the days the window touches, a bucket each."""
    rows = []
    for d in own.get("days") or []:
        try:
            day = datetime.fromisoformat(str(d.get("day"))).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        if day + timedelta(days=1) <= start or day >= to:
            continue
        rows.append({"start": day.isoformat(), "group": policy, "deployments": [policy],
                     "card_hours": round(float(d.get("gpu_card_s") or 0) / 3600, 6),
                     "cost_usd": round(sum(float(d.get(k) or 0) for k in ("gpu_usd", "cpu_usd", "memory_usd")), 6)})
    return {"from": start.isoformat(timespec="seconds"), "to": to.isoformat(timespec="seconds"), "by": "day",
            "tz": "UTC", "group": "none", "policy": policy, "buckets": rows,
            "total_card_hours": round(sum(r["card_hours"] for r in rows), 6),
            "total_usd": round(sum(r["cost_usd"] for r in rows), 6)}


def usage_cli(*, since: Any = None, until: Any = None, by: str | None = None, group: str = "none",
              policy: str | None = None, csv_out: bool = False, base_url: str | None = None,
              echo: Callable[[str], None] = print) -> dict:
    """`seq usage`: the window as a table - one line per bucket (per bucket and group with --group), its card-hours,
    dollars and a bar - then the totals (and, split, each group's); with --policy, that policy's robots over the
    window; with --csv, the same rows as CSV."""
    out, own = _read(since=since, until=until, by=by, group=group, policy=policy, base_url=base_url)
    rows = out.get("buckets") or []
    if csv_out:
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(CSV_COLUMNS)
        for r in rows:
            w.writerow([r.get("start"), r.get("group") or policy or "", f"{float(r.get('card_hours') or 0):.6f}",
                        f"{float(r.get('cost_usd') or 0):.6f}"])
        echo(buf.getvalue().rstrip("\n"))
        return out
    step = out.get("by") or "hour"
    shown_group = out.get("group") or "none"
    echo(f"{'Use of ' + policy if policy else 'Use'} {_when(out.get('from'), 'minute')} → {_when(out.get('to'), 'minute')} "
         f"UTC, by {step}: {float(out.get('total_card_hours') or 0):.3f} card-hours, "
         f"{money(out.get('total_usd'))} (GPU, CPU and memory)")
    if own is not None:
        echo("(a robot's key reads its policy's use per UTC day; a full key reads it per hour, as the account's)")

    shown = rows if shown_group == "none" else [r for r in rows if r.get("card_hours") or r.get("cost_usd")]
    top = max([float(r.get("card_hours") or 0) for r in shown] + [0.0])
    label = {"deployment": "deployment", "gpu": "card", "kind": "machines"}.get(shown_group)
    echo(f"{'when':<16} " + (f"{label:<20} " if label else "") + f"{'card-hours':>10} {'cost':>9}")
    for r in shown:
        ch = float(r.get("card_hours") or 0)
        bar = "█" * (round(BAR * ch / top) if top else 0)
        who = _KIND.get(r.get("group"), r.get("group") or "—") if shown_group == "kind" else (r.get("group") or "—")
        echo(f"{_when(r.get('start'), step):<16} " + (f"{who[:20]:<20} " if label else "")
             + f"{ch:>10.3f} {money(r.get('cost_usd')):>9}  {bar}")
    if label:
        per: dict[str, list[float]] = {}
        for r in rows:
            if r.get("card_hours") or r.get("cost_usd"):
                key = (_KIND.get(r.get("group"), r.get("group")) if shown_group == "kind" else r.get("group")) or "—"
                sums = per.setdefault(key, [0.0, 0.0])
                sums[0] += float(r.get("card_hours") or 0)
                sums[1] += float(r.get("cost_usd") or 0)
        if per:
            echo("by " + label + ": " + " · ".join(f"{k} {ch:.3f} ({money(usd)})" for k, (ch, usd)
                                                   in sorted(per.items(), key=lambda kv: (-kv[1][0], -kv[1][1]))))
    if policy and until in (None, ""):
        robots_said(policy, out, base_url, echo, own)
    return out


def robots_said(policy: str, out: dict, base_url: str | None, echo: Callable[[str], None],
                own: dict | None = None) -> None:
    """What a policy's robots did over a window that ends now: their acts and errors, the round trip they reported
    (p50 / p95, each split into inference and the rest when their SDK says it) and how many of their action chunks came
    on time - the policy page's headline - and its spend, the database's total over the window, its storage in it: the
    figure its page and its monthly budget read (the table above counts its machines alone). Read from the policy's own
    usage from the window's start (_own_path). Nothing said when it cannot be read.
    
"""
    from seq.deployments_cli import _call

    got = own
    if got is None:
        try:
            start = datetime.fromisoformat(str(out.get("from")).replace("Z", "+00:00"))
            got = _call("GET", _own_path(policy, start), base_url)
        except Exception:
            return
    spend = got.get("total") or {}
    if isinstance(spend.get("total_usd"), (int, float)):

        echo(f"its spend: {money(spend['total_usd'])} with its storage ({money(spend.get('storage_usd'))}) - what its "
             "page and its monthly budget count")
    lat = got.get("latency") or {}

    acts = int(lat["calls"]) if isinstance(lat.get("calls"), (int, float)) else \
        sum(int(r.get("calls") or 0) for r in got.get("days") or [])
    errors = int(lat["errors"]) if isinstance(lat.get("errors"), (int, float)) else \
        sum(int(r.get("errors") or 0) for r in got.get("days") or [])
    trips = [t for t in (_trip(lat, "p50"), _trip(lat, "p95")) if t]
    echo(f"its robots: {acts:,} acts · {errors:,} errors" + (" · round trip " + ", ".join(trips) if trips else ""))
    cont = got.get("continuity") or {}
    otr = cont.get("on_time_rate")
    if not cont.get("runs") or not isinstance(otr, (int, float)):

        echo("on-time: — (no runs reported over the window)")
    else:
        stalls = int(cont["stalls"]) if isinstance(cont.get("stalls"), (int, float)) else 0
        lost = (f" ({float(cont['stall_s']):.1f} s lost)" if stalls and isinstance(cont.get("stall_s"), (int, float))
                else "")
        since = f" since {str(cont['since'])[:10]}" if cont.get("since") else ""
        echo(f"on-time {math.floor(otr * 1000 + 0.5) / 10:.1f}% · stalls {stalls:,}{lost} · over {int(cont['runs']):,} "
             f"run(s){since}: of the action chunks they ran, the share that acted within its time budget; a stall is one "
             "that came too late")
    each_robot(got.get("robots"), echo)


def each_robot(robots: Any, echo: Callable[[str], None]) -> None:
    """Each robot of the policy, by the key it connects with, the busiest first as the platform lists them
: its acts and errors, its round trip p50 / p95 as its own SDK measured it, and its on-time share over
    its own runs - a dash where it reported none, never a false 100 %. Robots that share a key are one line.

"""
    rows = [r for r in robots or [] if isinstance(r, dict)]
    if not rows:
        return
    echo("each robot, by the key it connects with:")
    for r in rows:

        who = f"…{r['last_four']}" if r.get("last_four") else str(r.get("key") or "?")[:8]
        said = [f"{int(r.get('acts') or 0):,} acts"]
        if r.get("errors"):
            said.append(f"{int(r['errors']):,} error{'s' if int(r['errors']) != 1 else ''}")
        if isinstance(r.get("p50_ms"), (int, float)):
            said.append(f"round trip p50 {r['p50_ms']:.0f} ms"
                        + (f", p95 {r['p95_ms']:.0f} ms" if isinstance(r.get("p95_ms"), (int, float)) else ""))
        otr = r.get("on_time_rate")
        if isinstance(otr, (int, float)) and r.get("chunks"):
            stalls = int(r.get("stalls") or 0)
            said.append(f"on-time {math.floor(otr * 1000 + 0.5) / 10:.1f}% of {int(r['chunks']):,} chunks"
                        + (f" ({stalls:,} stall{'s' if stalls != 1 else ''})" if stalls else ""))
        else:
            said.append("on-time — (no run reported)")
        echo(f"  {who}" + (f" {r['name']}" if r.get("name") else "") + ": " + " · ".join(said))


def _trip(lat: dict, q: str) -> str:
    """One quantile of the round trip, in ms halved up as the console rounds them (232.5 is 233), with its inference
    and the rest in brackets when the robots' SDK reported inference."""
    def ms(x: Any) -> int | None:
        return math.floor(float(x) + 0.5) if isinstance(x, (int, float)) else None

    whole, inference = ms(lat.get(f"{q}_ms")), ms(lat.get(f"inference_{q}_ms"))
    if whole is None:
        return ""
    split = f" (inference {inference} + other {whole - inference})" if inference is not None else ""
    return f"{q} {whole} ms{split}"


def _when(iso: Any, step: str) -> str:
    """An instant in UTC, as the bucket names it: 10-06 14:00 for an hour, 2026-10-06 for a day, 2026-10 for a month."""
    try:
        t = datetime.fromisoformat(str(iso).replace("Z", "+00:00")).astimezone(timezone.utc)
    except (ValueError, TypeError):
        return str(iso or "—")
    return t.strftime({"hour": "%m-%d %H:%M", "day": "%Y-%m-%d", "month": "%Y-%m"}.get(step, "%Y-%m-%d %H:%M"))
