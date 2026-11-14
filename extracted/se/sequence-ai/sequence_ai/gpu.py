"""
GPU machines you run yourself: `sequence_ai.gpu.add` opens them near a place in the United States,
`.list` shows those live and `.history` those over, `.logs` reads one's log, `.allow` changes who reaches their ports, `.remove`
shuts one down, `.save` keeps one's disk as a snapshot to start others from, and `.places` lists the
US cities a place can be chosen from, each with its latitude and longitude. Each is said by the place
you asked for, never a region of ours. A machine is a container you are root in, on one card, reached over SSH
(`seq gpu ssh`) — install and run what you like; the ports you publish are reached straight at its
address, nothing of ours in between; `remove` ends the machine and its disk, and stops its billing.

These are owner-scoped: a full key or a signed-in session, never a robot key. They count against
your account's GPU limit — the ceiling serving and evals share — and draw on its credit like any
machine. A refusal is one of three of its own where it is one of these: GpuBadRequest, for what was
asked; GpuOverLimit, at a limit of your account's or its credit; GpuNoCard, for a card not to be had -
`seq gpu` exiting by each one's code, as every `seq` command does. `sequence_ai.gpus()` (no namespace) is
a different thing entirely: the catalogue of cards and their prices.

"""
from __future__ import annotations

import time
from contextlib import contextmanager
from typing import Any, Callable, Iterator, Optional
from urllib.parse import urlencode

import httpx

from ._core.money import money
from ._core.names import segment
from ._core.transport import Transport
from .errors import (Conflict, GpuBadRequest, GpuNoCard, GpuOverLimit, InvalidRequest, OutOfCredit, SequencesError,
                     Unavailable)



WAIT_S = 25 * 60.0
LOOK_S = 4.0
EVERYWHERE = "0.0.0.0/0"

NO_IPV4 = ("with no allow, a GPU's ports open to this machine's IPv4 address, asked over IPv4, and this machine could not "
           "reach the platform over IPv4: give allow (seq gpu add --allow), the IPv4 ranges your robots connect from")

LIMITS = frozenset({"gpu_limit_reached", "cpu_limit_reached", "memory_limit_reached", "container_limit_reached",
                    "storage_full"})




SNAPSHOT_ASKED = frozenset({"snapshot_exists", "gpu_saving", "snapshot_not_found", "snapshot_not_ready"})
SAVE_ASKED = SNAPSHOT_ASKED | {"gpu_not_running", "name_taken"}


def _mapped(exc: SequencesError, asked: frozenset = SNAPSHOT_ASKED) -> SequencesError:
    """A GPU call's refusal as one of the three its caller tells apart, what the platform said kept on it: what was asked
    (InvalidRequest, or a reason in `asked`) GpuBadRequest; a limit or the credit (a 409 of LIMITS, OutOfCredit)
    GpuOverLimit; no card now (gpu_no_card, gpu_busy) GpuNoCard. Any other as it came."""
    reason = (exc.details or {}).get("reason")
    if isinstance(exc, (GpuBadRequest, GpuOverLimit, GpuNoCard)):
        return exc
    cls = (GpuBadRequest if isinstance(exc, InvalidRequest) or reason in asked else
           GpuOverLimit if isinstance(exc, OutOfCredit) or (isinstance(exc, Conflict) and reason in LIMITS) else
           GpuNoCard if isinstance(exc, Unavailable) and reason in ("gpu_no_card", "gpu_busy") else None)
    if cls is None:
        return exc
    return cls(exc.message, status=exc.status, code=exc.code, retryable=exc.retryable, retry_after_s=exc.retry_after_s,
               request_id=exc.request_id, hint=exc.hint, details=exc.details, body=exc.body)


@contextmanager
def _owned(api_key: str | None, base_url: str | None, asked: frozenset = SNAPSHOT_ASKED, *,
           ipv4: bool = False) -> Iterator[Transport]:
    """A transport for the GPU management calls — owner-scoped (login=True: a full key or a signed-in
    session, never a robot key), with the mock tier mapped as the rest of the SDK maps it, over IPv4
    alone where `ipv4` — closed as the call ends, what it raised as a GPU call's own (_mapped, the reasons in `asked`
    what was asked). `sequence_ai` is imported here, not at module load, because this module is imported while
    `sequence_ai.__init__` is still running."""
    import sequence_ai

    t = Transport(api_key=api_key, base_url=sequence_ai._resolve_base_url(base_url), login=True,
                  **({"ipv4": True} if ipv4 else {}))
    try:
        yield t
    except SequencesError as exc:
        mapped = _mapped(exc, asked)
        if mapped is exc:
            raise
        raise mapped from None
    finally:
        t.close()


def add(place: str, gpu: str, count: int = 1, *, snapshot: str | None = None, ports: list[int] | None = None,
        allow: list[str] | None = None, run: str | None = None, name: str | None = None, wait: bool = True,
        api_key: str | None = None, base_url: str | None = None) -> list[dict[str, Any]]:
    """
    Open `count` GPU machines near `place`, each with a `gpu` card — a machine you are root on,
    reached over SSH (`seq gpu ssh`), yours until you `remove` it. Waits until each runs and returns
    them, one dict each, as `list` says them — `"address"`, `"ports"`, `"image"` among them — with
    `"expected_rtt"`: `{"ms", "probes", "within_km", "days"}`, the median round trip measured from
    within `within_km` of `place` over the last `days` days (`"ms"` None where nothing that near was
    measured), or None where it could not be read. `wait=False` returns once each is asked for -
    seconds, where running takes a minute or two -, each "starting".

    `place` is the exact spot you want them near, in the United States — a US city ("San Francisco,
    CA") or a lat,lon in the US ("37.77,-122.42"); `places` lists the US cities. The platform opens
    each at the place quickest to reach from there that has the card.

    `ports`: the TCP ports your server listens on (1024-65535, not 22 or 8080, eight at most), reached
    straight at the machine's address from the IPv4 ranges in `allow` alone — the address this call
    comes from, where you name none, the call then made over IPv4 (a machine that reaches the platform
    over IPv6 alone names them); `["0.0.0.0/0"]` opens them to every address, so authenticate in
    your server. `allow` changes them later. `run`: a command run in the container as it starts (with
    bash, from /root, its output in /var/log/seq-run.log), started again each time it exits, and no
    more once it exits within 10 s five times running. `snapshot`: the name of a snapshot of yours
    (`save`) to start from, its `run` command with it unless you give one.

    `name`: a fixed name (1-40 lowercase letters, digits and hyphens) — the GPU is also reached at its
    `"host"`, `<name>.<your id>.gpu.generalsequences.com`, which moves to each GPU you add later under
    that name once it runs, so a robot is set up with the name once. DNS alone: robots still connect
    straight to the GPU. One GPU's: `count` must be 1.

    `count` over 1 is all-or-nothing at the add; each then runs or fails on its own. Raises
    GpuBadRequest for what cannot be had (a place outside the US, ports, a snapshot of no such name or
    one still saving or failed, a name that cannot be one or is asked of several),
    GpuOverLimit at a limit of your account's or its credit, GpuNoCard where no card is to be had, now
    or within the 20 minutes the platform gives each - never billed (`details["gpus"]` holds each as it
    ended or runs). A KeyboardInterrupt while it waits removes those not running yet and is raised on:
    its `cancelled` the ids removed, its `billed` what each of those was billed, by id, as the platform
    says it once removed - 0 for none, the seconds one of the places asked for it held a card where one
    did, None where it could not be read -, and its `running` those left running. Owner-scoped: a
    full key or a signed-in session, never a robot key.
    """
    body: dict[str, Any] = {"place": place, "gpu": gpu, "count": int(count)}
    if snapshot is not None:
        body["from"] = snapshot
    if ports:
        body["ports"] = [int(p) for p in ports]
    if allow:
        body["allow"] = [str(a) for a in allow]
    if run is not None:
        body["run"] = run
    if name is not None:
        body["name"] = name



    ipv4 = bool(ports) and not allow
    try:
        with _owned(api_key, base_url, ipv4=ipv4) as t:
            added = t.post("/v1/gpus", body)["gpus"]
    except Unavailable as exc:
        if not (ipv4 and isinstance(exc.__cause__, (httpx.ConnectError, httpx.ConnectTimeout))):
            raise
        raise Unavailable(exc.message, retryable=exc.retryable, hint=NO_IPV4) from exc.__cause__
    return _running(added, api_key=api_key, base_url=base_url) if wait else added


def _nap(seconds: float) -> None:
    time.sleep(seconds)


def _now() -> float:
    return time.monotonic()


def _running(added: list[dict[str, Any]], *, timeout_s: float = WAIT_S, said: Optional[Callable[[float, list], None]] = None,
             api_key: str | None = None, base_url: str | None = None) -> list[dict[str, Any]]:
    """`added` (as `add` answered them) once each runs or is over: each as the list says it, or its history once over, with
    the "expected_rtt" `add` answered. `said(seconds, starting)` is told at each read while some still start (`seq gpu
    add` says how long it has waited). Raises GpuNoCard when one got no card or still starts past `timeout_s`, Unavailable
    when one had its card and did not start. A KeyboardInterrupt meanwhile removes those not running (_cancel) and is
    raised on."""
    ids = [str(g["id"]) for g in added]
    began = _now()
    by: dict[str, dict[str, Any]] = {}
    with _owned(api_key, base_url) as t:
        try:
            while True:
                by = _read(t, ids)
                starting = [i for i in ids if (by.get(i) or {}).get("status", "starting") == "starting"]
                if not starting or _now() - began >= timeout_s:
                    break
                if said is not None:
                    said(_now() - began, starting)
                _nap(LOOK_S)
        except KeyboardInterrupt as stop:
            _cancel(t, ids, by, stop)
            expected = {str(g["id"]): g.get("expected_rtt") for g in added}
            stop.running = [{**g, "expected_rtt": expected.get(str(g["id"]))}
                            for g in stop.running]
            raise
    out = [{**(by.get(i) or {"id": i, "status": "starting"}), "expected_rtt": g.get("expected_rtt")}
           for i, g in zip(ids, added)]
    failed = [g for g in out if g.get("status") not in ("running", "starting")]
    late = [g for g in out if g.get("status") == "starting"]
    if failed or late:
        words = [f"{g['id']} {_why(g)}" for g in failed] + [f"{g['id']} still starting after {timeout_s / 60:.0f} minutes"
                                                            for g in late]
        no_card = bool(late) or any(g.get("reason") == "gpu_no_card" for g in failed)
        raise (GpuNoCard if no_card else Unavailable)(
            "; ".join(words), retryable=True, details={"reason": "gpu_no_card" if no_card else "gpu_not_started",
                                                       "gpus": out},
            hint="add again later, or near another place; seq gpu list shows those that run")
    return out


def _read(t: Transport, ids: list[str]) -> dict[str, dict[str, Any]]:
    """Each of `ids` as the list says it, or its history once it is over."""
    by = {str(g["id"]): g for g in t.get("/v1/gpus").get("gpus") or [] if str(g.get("id")) in ids}
    gone = [i for i in ids if i not in by]
    if gone:
        over = t.get(f"/v1/gpus/history?{urlencode({'limit': 200})}").get("gpus") or []
        by.update({str(g["id"]): g for g in over if str(g.get("id")) in gone})
    return by


def _cancel(t: Transport, ids: list[str], by: dict[str, dict[str, Any]], stop: BaseException) -> None:
    """Ctrl-C while waiting: each of `ids` not running, as the list says it now, removed, those that run left running;
    `stop` told which (its `cancelled`, `running`, and `not_cancelled`, those whose removal was not answered) and what each
    removed was billed (`billed`, read once removed: _spent) - none of its own time, as it never ran, but the seconds one of
    the places asked for it held a card, as each that held one is billed. A second Ctrl-C meanwhile stops none of it.
    

"""
    try:
        by = _read(t, ids)
    except (SequencesError, KeyboardInterrupt):
        pass
    running = [by[i] for i in ids if (by.get(i) or {}).get("status") == "running"]
    cancelled, kept = [], []
    for i in ids:
        if (by.get(i) or {}).get("status", "starting") != "starting":
            continue
        try:
            t.delete(f"/v1/gpus/{segment(i, 'gpu id')}")
            cancelled.append(i)
        except (SequencesError, KeyboardInterrupt):
            kept.append(i)
    stop.cancelled, stop.running, stop.not_cancelled = cancelled, running, kept
    stop.billed = _spent(t, cancelled)


def _usd(v: Any) -> float | None:
    """An amount the platform said, None where it said none."""
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def _spent(t: Transport, ids: list[str]) -> dict[str, float | None]:
    """What each of `ids` was billed, by id, as the platform says it now - its `usd_so_far`, which counts the seconds each
    place asked for it held a card -, None where it could not be read. The DELETE's answer carries no amount, and its
    platform bills those places as it removes a GPU, before it answers, so a read after it says the whole of it. {sequence-
    gateway routes/gpus.remove: `return {"id": gpu_id, "status": gpu.SHUT_DOWN}`; machines/gpu._finish: "those of its pool
    first, each billed for a card it held, then its own"}"""
    if not ids:
        return {}
    try:
        by = _read(t, ids)
    except (SequencesError, KeyboardInterrupt):
        by = {}
    return {i: _usd((by.get(i) or {}).get("usd_so_far")) for i in ids}


def _billed(usd: float | None) -> str:
    """What a GPU that never ran was billed, in words: "not billed" for nothing, else the amount and what it is for - the
    seconds one of the places asked for it held a card, which its owner pays -, or that it could not be read. Said as
    the platform said it, never worked out here.
"""
    if usd is None:
        return "what was billed could not be read - seq gpu history says it"
    if not usd:
        return "not billed"
    return f"billed {money(usd)} for the seconds one of the places asked for it held a card"


def _why(g: dict[str, Any]) -> str:
    """Why a GPU that failed to start did, in words, and what it was billed (_billed): no card near its place in 20
    minutes, its card had and no start in them, or what its reason says."""
    reason = g.get("reason")
    if reason == "gpu_no_card":
        return f"got no card near its place within 20 minutes: {_billed(_usd(g.get('usd_so_far')))}"
    if reason == "could_not_start":
        return f"had its card and did not start within 20 minutes: {_billed(_usd(g.get('usd_so_far')))}"
    return f"ended as it started ({reason or g.get('status')})"


def allow(id: str, allow: list[str], *, api_key: str | None = None, base_url: str | None = None) -> dict[str, Any]:
    """
    Who reaches a GPU's published ports from now on: the IPv4 ranges in `allow` ("203.0.113.0/24", or
    an address alone), in place of those it had — for when your robot's or office's address changes.
    The GPU is not restarted. Returns `{"id", "allow", "applied"}`: `applied` True once the machine
    said its ports are open to those alone, which a running one does within seconds; False where it
    had not by then (it is still told, a little longer — call again to be sure) or for one still
    starting, which is handed them as it starts. `["0.0.0.0/0"]` opens them to every address.
    Owner-scoped.
    """
    with _owned(api_key, base_url) as t:
        return t.put(f"/v1/gpus/{segment(id, 'gpu id')}/allow", {"allow": [str(a) for a in allow]})


def places(q: str = "", limit: int = 8, *, api_key: str | None = None,
           base_url: str | None = None) -> list[dict[str, Any]]:
    """
    The US cities a place for `add` can be chosen from: `[{"name", "region", "country", "lat", "lon",
    "also"}]`, those whose name or another name they go by starts with `q` (case and accents aside),
    those of their own name first, each the largest first, `limit` of them (1 to 20); with no `q`, the
    largest US cities. A state after a comma narrows them ("Springfield, IL"). `region` is its state;
    `also` is the other name a city was found by ("big apple" finds New York City as "Big Apple"), None
    where `q` starts its own. Pass one's `f"{lat},{lon}"` as `add(place=...)`. The list the console's
    City picker shows; `seq gpu places` prints it. Owner-scoped.
    {the user 11-11: "a city drop down list and auto fill the long and lat"; the user 11-12: "we
    shouldnt allow locaiton out of us"}
    """
    with _owned(api_key, base_url) as t:
        return t.get(f"/v1/gpus/places?{urlencode({'q': q, 'limit': int(limit)})}")["data"]


def list(*, api_key: str | None = None, base_url: str | None = None) -> dict[str, Any]:
    """
    Your GPU machines that are live, and how many of your GPU limit they hold:
    `{"gpus": [{"id", "place", "gpu", "status", "started_at", "address", "ssh_port", "ports", "allow",
    "image", "robots", "run", "usd_so_far", "usd_per_hour"}], "quota": {"used", "limit"}}`, oldest
    first. `place` is the place you gave `add`, as you gave it (None for one added before it was kept);
    `status` is "starting" or "running" (SSH connects now). Once it runs: `address`, where it is reached,
    and `ssh_port`; `ports` you published and `allow`, the ranges they are open to; `image`, what it
    started from ("base 2026.11", "snapshot <name>"); `robots`, as the machine measures them —
    `{"count", "rtt_p50_ms"}`, the robots connected to its ports and their median round trip — absent
    while it has said nothing lately; `run`, how the `run` command goes: "running", "restarting", or
    "failing" (exited within 10 s five times running, and not started again). Those over are
    `history`'s. What `seq gpu list` prints. Owner-scoped.


    """
    with _owned(api_key, base_url) as t:
        return t.get("/v1/gpus")


def history(limit: int | None = None, cursor: str | None = None, *, api_key: str | None = None,
            base_url: str | None = None) -> dict[str, Any]:
    """
    Your GPU machines that are over, kept 30 days, the one ended last first, one page:
    `{"gpus": [{"id", "place", "gpu", "status", "reason"?, "started_at", "ended_at", "usd_so_far",
    "usd_per_hour"}], "total", "offset", "next_cursor"}`. `status` is "shut_down" (removed, or ended
    when the account ran out of credit: `reason` "out_of_credit") or "failed" (with `reason`);
    `usd_so_far` is what it cost in all. `limit` rows a page (1-200, 50 unless given); pass a page's
    `next_cursor` as `cursor` for the next. What `seq gpu history` prints. Owner-scoped.
    """
    asked = {k: v for k, v in (("limit", None if limit is None else int(limit)), ("cursor", cursor)) if v is not None}
    with _owned(api_key, base_url) as t:
        return t.get("/v1/gpus/history" + (f"?{urlencode(asked)}" if asked else ""))


def save(id: str, name: str, replace: bool = False, *, api_key: str | None = None,
         base_url: str | None = None) -> dict[str, Any]:
    """
    Keep a running GPU's disk — what you installed over its base environment — as a snapshot called
    `name`, to start others from (`add(snapshot=name)`), its `run` command with it. Returns at once,
    `{"name", "status": "saving", ...}`; the GPU keeps running and serving meanwhile — a file being
    written as it saves may be kept half-written. `replace` takes the place of a snapshot of that name.
    Its storage is billed to you each month from when it is ready and counts toward your storage limit.
    Raises GpuBadRequest for a name you have a snapshot of (without `replace`) or something else of
    yours holds, a GPU saving one already or not running, and GpuOverLimit where it would pass your
    storage limit. Owner-scoped.

    """
    with _owned(api_key, base_url, SAVE_ASKED) as t:
        return t.post(f"/v1/gpus/{segment(id, 'gpu id')}/save", {"name": name, "replace": bool(replace)})


def saved(*, api_key: str | None = None, base_url: str | None = None) -> dict[str, Any]:
    """
    Your snapshots: `{"snapshots": [{"name", "status", "size_gb", "gpu", "image", "saved_at",
    "usd_per_month", "reason"?}]}`. `status` is "saving", "ready" (an add can start from it) or
    "failed", `reason` saying why; `gpu` and `image` are the card and base environment it was saved
    from ("L4", "base 2026.11"); `size_gb`, `saved_at` and `usd_per_month` once it is ready. What
    `seq gpu saved` prints. Owner-scoped.
    """
    with _owned(api_key, base_url) as t:
        return t.get("/v1/gpus/saved")


def remove_saved(name: str, *, api_key: str | None = None, base_url: str | None = None) -> dict[str, Any]:
    """Delete a snapshot: its storage stops being billed. Returns `{"name", "status": "deleted"}`; GpuBadRequest for a
    name you have no snapshot of. Owner-scoped."""
    with _owned(api_key, base_url) as t:
        return t.delete(f"/v1/gpus/saved/{segment(name, 'snapshot name')}")


def remove(id: str, *, force: bool = False, api_key: str | None = None, base_url: str | None = None) -> dict[str, Any]:
    """
    Shut a GPU machine down now — this ends the machine and its disk, and stops its billing.
    Returns `{"id", "status": "shut_down"}`; removing one already gone answers the same. One being
    saved is refused (GpuBadRequest) unless `force`, which gives that snapshot up, never billed.
    Owner-scoped.
    """
    with _owned(api_key, base_url) as t:
        return t.delete(f"/v1/gpus/{segment(id, 'gpu id')}" + ("?force=true" if force else ""))


def logs(id: str, since: str | float | None = None, after: int | None = None, limit: int | None = None, *,
         api_key: str | None = None, base_url: str | None = None) -> dict[str, Any]:
    """
    A GPU machine's log, oldest first, one page: `{"id", "status", "ended", "entries": [{"id", "at",
    "kind", "what", "text", "detail"}], "next"}`. `kind` is "event" — what happened to it, in the
    platform's words: asked for, started, its image loaded, ready, its command started, exited or given
    up on, the addresses its ports are open to, its name, its end and why, what it was billed — or
    "output", a line its command printed; `what` names an event. `since`: from this time on — "30m",
    "1h", "2d" back from now, an ISO time with its zone, or seconds since the epoch. `after`: the entries
    after this one (a page's `next`) — ask again with it to follow the machine as it goes, until `ended`
    and nothing new. `limit`: entries a page (1-1000, 500 unless given). Kept 90 days after the machine
    ends. What `seq gpu logs` prints. Owner-scoped.
    """
    from datetime import datetime, timezone

    if isinstance(since, (int, float)) and not isinstance(since, bool):
        since = datetime.fromtimestamp(float(since), timezone.utc).isoformat()
    asked = {k: v for k, v in (("since", since), ("after", None if after is None else int(after)),
                               ("limit", None if limit is None else int(limit))) if v is not None}
    with _owned(api_key, base_url) as t:
        return t.get(f"/v1/gpus/{segment(id, 'gpu id')}/logs" + (f"?{urlencode(asked)}" if asked else ""))
