"""
GPU machines you run yourself: `sequence_ai.gpu.add` opens them near a place in the United States,
`.list` shows those live and `.history` those over, `.logs` reads one's log, `.allow` changes who reaches their ports,
`.follow_token` makes one of your robots a token with which `.follow`, on the robot, lets its own address in as its
network changes it, `.remove`
shuts one down, `.save` keeps one's disk as a snapshot to start others from, and `.places` lists the
US cities a place can be chosen from, each with its latitude and longitude. Each is said by the place
you asked for, never a region of ours. A machine is a container you are root in, with its cards — 1, 2, 4 or 8 of
one kind —, reached over SSH
(`seq gpu ssh`) — install and run what you like; the ports you publish are reached straight at its
address, nothing of ours in between; `remove` ends the machine and its disk, and stops its billing.

These are owner-scoped: a full key or a signed-in session, never a robot key - all but `.follow`, which a robot calls
with its follow token alone. They count against
your account's GPU limit — the ceiling serving and evals share — a card each, and draw on its credit like any
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
from .errors import (Conflict, GpuBadRequest, GpuNoCard, GpuOverLimit, InternalError, InvalidRequest, OutOfCredit,
                     SequencesError, Unavailable)



WAIT_S = 25 * 60.0
START_MOST_S = 20 * 60.0
LOOK_S = 4.0
ENDED_READS = 3
LOG_PAGE = 1000




NOT_STARTED = {
    "not_up": "had its card and did not come up",
    "container_ended": "had its card, and its container stopped before it ran",
    "host_failed": "had its card, and the host its machine ran on failed before it ran",
    "reclaimed": "had its card, and the cloud it ran on took its machine back before it ran",
}
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
    Open a GPU machine of `count` cards of `gpu` near `place` — 1, 2, 4 or 8 —, one you are root on,
    reached over SSH (`seq gpu ssh`), yours until you `remove` it; for any other number of cards, or
    cards in different places, add several, each a GPU of its own with its own id, address and bill.
    Waits until it runs and returns it, a list of one, as `list` says it — `"address"`, `"ports"`,
    `"image"` among them — with `"cards"`, how many it has; `"request"` and `"request_cards"`, its own
    id and cards again; and `"expected_rtt"`: `{"ms"}`, the round trip expected from `place` (`"ms"`
    None where none is known yet), or None where it could not be read. `wait=False` returns once it
    is asked for - seconds, where running takes a minute or two -, "starting". Each card costs the same
    alone or among eight: its `"usd_per_hour"` is its cards times one card's.




    `place` is the exact spot you want it near, in the United States — a US city ("San Francisco,
    CA") or a lat,lon in the US ("37.77,-122.42"); `places` lists the US cities. The platform opens
    it at the closest GPU available.

    `ports`: the TCP ports your server listens on (1024-65535, not 22 or 8080, eight at most), reached
    straight at the machine's address from the ranges in `allow` alone — the address this call
    comes from, where you name none, the call then made over IPv4 (a machine that reaches the platform
    over IPv6 alone names them); `["0.0.0.0/0"]` opens them to every address, so authenticate in
    your server. IPv6 ranges ("2001:db8:42::/56") are taken where the GPU is given an IPv6 address,
    its `"address6"`: a robot on a shared IPv4 address (CGNAT: Starlink, cellular lines) is let in
    by its own IPv6 prefix there, which its network can still change. `allow` changes them later. `run`: a command run in the container as it starts (with
    bash, from /root, its output in /var/log/seq-run.log), started again each time it exits, and no
    more once it exits within 10 s five times running. `snapshot`: the name of a snapshot of yours
    (`save`) to start from, its `run` command with it unless you give one.

    `name`: a fixed name (1-40 lowercase letters, digits and hyphens) — the GPU is also reached at its
    `"host"`, `<name>.<your id>.gpu.generalsequences.com`, which moves to each GPU you add later under
    that name once it runs, so a robot is set up with the name once. DNS alone: robots still connect
    straight to the GPU.

    Raises GpuBadRequest for what cannot be had (a `count` not 1, 2, 4 or 8, or more cards than a
    machine of that card holds here - `details["counts"]` the counts it can be had in -, a place outside
    the US, ports, a snapshot of no such name or one still saving or failed, a name that cannot be one),
    GpuOverLimit at a limit of your account's or its credit, GpuNoCard where no card is to be had, now
    or within the 20 minutes the platform gives it - never billed -, and InternalError where it had
    its cards and did not start, its words saying how it ended (`details["gpus"]` holds it as it ended;
    `seq gpu logs <id>` says the rest). A KeyboardInterrupt while it waits removes it if it does not run
    yet and is raised on: its `cancelled` the ids removed, its `billed` what each of those was billed, by
    id, as the platform says it once removed - 0 for none, the capacity it held while it started where
    it held some, None where it could not be read -, and its `running` those left running,
    it where it ran by then. One while the add is asked - the seconds before the platform answers it -
    stops this call alone: what the platform adds then is yours all the same, and `list()` shows it.
    Owner-scoped: a full key or a signed-in session, never a robot key.


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


def _card_prices(*, api_key: str | None = None, base_url: str | None = None) -> dict[str, float]:
    """Each card's own price an hour, by its name, as the price list says it (GET /v1/pricing - what `seq gpus` and the
    pricing page read): what a GPU's card costs, its CPU and memory billed on top. {} where it could not be read."""
    try:
        with _owned(api_key, base_url) as t:
            rows = t.get("/v1/pricing").get("gpus") or []
    except SequencesError:
        return {}
    return {str(g.get("gpu")): float(g["usd_per_hour"]) for g in rows
            if isinstance(g.get("usd_per_hour"), (int, float)) and not isinstance(g.get("usd_per_hour"), bool)}


def _nap(seconds: float) -> None:
    time.sleep(seconds)


def _now() -> float:
    return time.monotonic()


def _running(added: list[dict[str, Any]], *, timeout_s: float = WAIT_S, said: Optional[Callable[[float, list], None]] = None,
             api_key: str | None = None, base_url: str | None = None) -> list[dict[str, Any]]:
    """`added` (as `add` answered them) once each runs or is over: each as the list says it, or its history once over, with
    the "expected_rtt" `add` answered. `said(seconds, starting)` is told at each read while some still start (`seq gpu
    add` says how long it has waited). Raises GpuNoCard when one got no card or still starts past `timeout_s`;
    InternalError when one had its card and did not start, how it ended read from its log (_ended_as) - the platform could
    not start it, which trying again is unlikely to change (`seq gpu` exits 1); Unavailable for any other end. A
    KeyboardInterrupt meanwhile removes those not running (_cancel) and is raised on.

"""
    ids = [str(g["id"]) for g in added]
    began = _now()
    by: dict[str, dict[str, Any]] = {}
    try:
        with _owned(api_key, base_url) as t:
            while True:
                by = _read(t, ids)
                starting = [i for i in ids if (by.get(i) or {}).get("status", "starting") == "starting"]
                if not starting or _now() - began >= timeout_s:
                    break
                if said is not None:
                    said(_now() - began, starting)
                _nap(LOOK_S)
            waited = _now() - began
            out = [{**(by.get(i) or {"id": i, "status": "starting"}), "expected_rtt": g.get("expected_rtt")}
                   for i, g in zip(ids, added)]
            failed = [g for g in out if g.get("status") not in ("running", "starting")]
            ends = {str(g["id"]): _ended_as(t, str(g["id"])) for g in failed if g.get("reason") == "could_not_start"}
    except KeyboardInterrupt as stop:


        raise _stopped(added, stop, by, api_key=api_key, base_url=base_url) from None
    late = [g for g in out if g.get("status") == "starting"]
    if not (failed or late):
        return out
    words = ([f"{g['id']} {_why(g, ends.get(str(g['id'])) or {}, waited)}" for g in failed]
             + [f"{g['id']} still starting after {timeout_s / 60:.0f} minutes" for g in late])
    if late or any(g.get("reason") == "gpu_no_card" for g in failed):
        raise GpuNoCard("; ".join(words), retryable=True, details={"reason": "gpu_no_card", "gpus": out},
                        hint="add again later, or near another place")
    if ends:
        raise InternalError("; ".join(words), details={"reason": "gpu_not_started", "gpus": out},
                            hint=f"seq gpu logs {next(iter(ends))} says why")
    raise Unavailable("; ".join(words), retryable=True, details={"reason": "gpu_not_started", "gpus": out},
                      hint="add again later, or near another place")


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
    removed was billed (`billed`, read once removed: _spent) - none of its own time, as it never ran, but the capacity it held
    while it started, where it held some. A second Ctrl-C meanwhile stops none of it.
    

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


def _stopped(added: list[dict[str, Any]], stop: BaseException, by: dict[str, dict[str, Any]] | None = None, *,
             api_key: str | None = None, base_url: str | None = None) -> BaseException:
    """`stop`, a Ctrl-C while `added` were asked for or waited on, told what became of them (_cancel, on a connection of
    its own - the one it stopped may be half open): those not running removed, those that run left running, each with
    the round trip `add` answered; all of them not cancelled where no connection could be had. Returned, to raise on."""
    ids = [str(g["id"]) for g in added]
    try:
        with _owned(api_key, base_url) as t:
            _cancel(t, ids, by or {}, stop)
    except (SequencesError, KeyboardInterrupt):
        if not hasattr(stop, "cancelled"):
            stop.cancelled, stop.running, stop.not_cancelled, stop.billed = [], [], ids, {}
    expected = {str(g["id"]): g.get("expected_rtt") for g in added}
    stop.running = [{**g, "expected_rtt": expected.get(str(g["id"]))}
                    for g in stop.running]
    return stop


def _usd(v: Any) -> float | None:
    """An amount the platform said, None where it said none."""
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def _spent(t: Transport, ids: list[str]) -> dict[str, float | None]:
    """What each of `ids` was billed, by id, as the platform says it now - its `usd_so_far` -, None where it could not be
    read. The DELETE's answer carries no amount, and the platform bills a GPU as it removes it, before it answers, so a
    read after it says the whole of it."""
    if not ids:
        return {}
    try:
        by = _read(t, ids)
    except (SequencesError, KeyboardInterrupt):
        by = {}
    return {i: _usd((by.get(i) or {}).get("usd_so_far")) for i in ids}


def _billed(usd: float | None) -> str:
    """What a GPU that never ran was billed, in words: "not billed" for nothing, else the amount and what it is for - the
    capacity it held while it started, which its owner pays -, or that it could not be read. Said as
    the platform said it, never worked out here.
"""
    if usd is None:
        return "what was billed could not be read - seq gpu history says it"
    if not usd:
        return "not billed"
    return f"billed {money(usd)} for the capacity it held while it started"


def _ended_as(t: Transport, gpu_id: str) -> dict[str, Any]:
    """How its log says a GPU ended - its "ended" event's detail: {"reason": "container_ended", "why": "its container
    stopped", "status": "failed"} -, {} where it says nothing of it. Its end is written as its row ends, after its bill,
    so a log read a moment after its history said it failed may not have it yet: read again a LOOK_S on, ENDED_READS
    times at most.
"""
    path = f"/v1/gpus/{segment(gpu_id, 'gpu id')}/logs"
    try:
        for n in range(ENDED_READS):
            after = None
            while True:
                page = t.get(f"{path}?{urlencode({'limit': LOG_PAGE, **({} if after is None else {'after': after})})}")
                entries = page.get("entries") or []
                for e in entries:
                    if e.get("kind") == "event" and e.get("what") == "ended":
                        return dict(e.get("detail") or {})
                if len(entries) < LOG_PAGE:
                    break
                after = page.get("next")
            if n < ENDED_READS - 1:
                _nap(LOOK_S)
    except (SequencesError, KeyboardInterrupt):
        pass
    return {}


def _why(g: dict[str, Any], end: dict[str, Any] | None = None, waited: float = 0.0) -> str:
    """Why a GPU that failed to start did, in words, and what it was billed (_billed): no card near its place, its card
    had and how it ended then as its log says it (`end`, _ended_as; NOT_STARTED), or what its reason says - "within 20
    minutes" only where `waited` was that long: the platform's end of one that did not come up is also said of a machine
    that ended early.
"""
    reason, end = g.get("reason"), end or {}
    within = " within 20 minutes" if waited >= START_MOST_S - 60.0 else ""
    if reason == "gpu_no_card":
        return f"got no card near its place{within}: {_billed(_usd(g.get('usd_so_far')))}"
    if reason == "could_not_start":
        word = str(end.get("reason") or "")
        said = (NOT_STARTED[word] + (within if word == "not_up" else "") if word in NOT_STARTED else
                f"had its card and did not start ({end['why']})" if end.get("why") else "had its card and did not start")
        return f"{said}: {_billed(_usd(g.get('usd_so_far')))}"
    return f"ended as it started ({reason or g.get('status')})"


def allow(id: str, allow: list[str], *, api_key: str | None = None, base_url: str | None = None) -> dict[str, Any]:
    """
    Who reaches a GPU's published ports from now on: the ranges in `allow` ("203.0.113.0/24", or
    an address alone; IPv6 ones too for a GPU with an `"address6"`), in place of those it had — for
    when your robot's or office's address changes.
    The GPU is not restarted. Returns `{"id", "allow", "applied"}`: `applied` True once the machine
    said its ports are open to those alone, which a running one does within seconds; False where it
    had not by then (it is still told, a little longer — call again to be sure) or for one still
    starting, which is handed them as it starts. `["0.0.0.0/0"]` opens them to every address.
    Owner-scoped.
    """
    with _owned(api_key, base_url) as t:
        return t.put(f"/v1/gpus/{segment(id, 'gpu id')}/allow", {"allow": [str(a) for a in allow]})






FOLLOW_ENV = "SEQUENCES_FOLLOW_TOKEN"
FOLLOW_CGNAT = ("followed over IPv4: on a network that shares one public IPv4 address among its users (CGNAT - "
                "Starlink's default, most cellular lines), everyone behind that address reaches the GPU's ports too. "
                "Give the GPU IPv6 and follow over IPv6, and authenticate in your server")


def follow_token(id: str, robot: str, *, api_key: str | None = None, base_url: str | None = None) -> dict[str, Any]:
    """
    A follow token for one of your robots: put it on the robot, and the robot lets its own address
    into this GPU's allow list as its network changes it (`follow`), and nothing else — never a range
    it names, another GPU, or anything else of your account. Returns `{"id", "robot", "token"}`.
    Made again for the same robot, the earlier token works no more and where it let the robot in from
    is taken away at once (`"applied"`, as `allow` says it). At most 8 robots follow one GPU; the
    GPU's other ranges stay yours (`allow`). Owner-scoped.
    """
    with _owned(api_key, base_url) as t:
        return t.post(f"/v1/gpus/{segment(id, 'gpu id')}/follow-token", {"robot": str(robot)})


def follow_revoke(id: str, robot: str, *, api_key: str | None = None, base_url: str | None = None) -> dict[str, Any]:
    """
    One robot follows a GPU's allow list no more: its follow token works no more, and where it was let
    in from is taken away at once. Returns `{"id", "robot", "applied"}`. Owner-scoped.
    """
    with _owned(api_key, base_url) as t:
        return t.delete(f"/v1/gpus/{segment(id, 'gpu id')}/follow/{segment(robot, 'robot name')}")


def follow(token: str | None = None, *, to: str | None = None, line: str | None = None, base_url: str | None = None,
           timeout_s: float | None = None) -> dict[str, Any]:
    """
    This machine's own address let into the allow list of the GPU its follow token is for, in place of
    where it was let in from before — what a robot calls as it starts and when it cannot reach its GPU,
    as its network changes its address. The platform lets in the address it is reached from, never one
    named: its /32, or over IPv6 its network's /64 (for a GPU with an `"address6"`).

    `token`: the robot's follow token (`follow_token`; `seq gpu follow-token ID --robot NAME`), default
    $SEQUENCES_FOLLOW_TOKEN — no API key is sent. `to`: the address, name or URL the robot reaches the
    GPU at. The follow then goes out from the address of this machine's that its packets to `to` go
    out from, so the address let in is the one the GPU sees — a machine with two networks, or two IPv6
    prefixes for a while, lets in the right one. With no `to`: over IPv6 first, then over IPv4.

    `line`: one of this machine's network interfaces — one of a robot's uplinks, as `connect(url,
    lines=[...])` names them. The follow goes out by it, from its address, and the GPU keeps where each
    line is let in from apart: a robot with two uplinks is let in by both, each line's address in
    place of that line's before. `connect(url, follow=..., lines=[...])` follows by each of its lines.

    Returns `{"id", "robot", "range", "applied", "ports"}` (and `"line"`, given one), and while the GPU
    runs, where it is reached: `"address"`, `"address6"` (reached over IPv6) and `"host"` (its fixed
    name). `applied` is True once the GPU said its ports are open to it, within seconds; False for one
    still starting, which takes it as it starts.

    Over IPv4, a network that shares one public address among its users (CGNAT: Starlink's default, most
    cellular lines) lets everyone behind that address in too: said once, as a warning. Give the GPU IPv6
    and the robot follows over IPv6.

    `timeout_s`: how long each try waits for the platform's answer (it waits up to 20 s for the GPU);
    the client's default unset.
    """
    import os

    import sequence_ai

    from ._core.warn import warn

    token = (token or os.environ.get(FOLLOW_ENV) or "").strip()
    if not token:
        raise InvalidRequest(f"no follow token: pass token=... or set {FOLLOW_ENV}; the GPU's owner makes one with "
                             "seq gpu follow-token ID --robot NAME", details={"reason": "follow_token"})
    if line:
        from .network import bind

        try:
            bind.check(line)
        except OSError as exc:
            raise InvalidRequest(str(exc), details={"reason": "follow_line"}) from None
    base = sequence_ai._resolve_base_url(base_url)
    froms = [_source_toward(to, line)] if to else ["::", "0.0.0.0"]
    last: SequencesError | None = None
    for src in froms:
        t = Transport(api_key=token, base_url=base, local_address=src, **({"interface": line} if line else {}))
        try:
            out = t.post("/v1/gpus/follow", {"line": line} if line else {}, timeout_s=timeout_s)
        except (InvalidRequest, Unavailable) as exc:

            closed = isinstance(exc, InvalidRequest) and exc.details.get("reason") == "gpu_ip6_closed"
            if src == "::" and (closed or isinstance(exc, Unavailable)):
                last = exc
                continue
            raise
        finally:
            t.close()
        if ":" not in str(out.get("range") or ""):
            warn(FOLLOW_CGNAT)
        return out
    assert last is not None
    raise last


def _source_toward(to: str, interface: str | None = None) -> str:
    """The address of this machine's that its packets to `to` (an address, a name, or a URL) go out from, as the system
    picks it - by `interface` alone, given one (network.bind): a UDP socket connected to it, no packet sent.
    InvalidRequest for what names no host that resolves here; Unavailable for one this machine has no way out to."""
    import ipaddress
    import socket
    from urllib.parse import urlsplit

    if interface:
        from .network import bind

    raw = str(to or "").strip()
    try:
        host: str | None = str(ipaddress.ip_address(raw.strip("[]")))
    except ValueError:
        try:
            host = urlsplit(raw if "://" in raw else f"//{raw}").hostname
        except ValueError:
            host = None
    try:
        infos = socket.getaddrinfo(host, 9, type=socket.SOCK_DGRAM) if host else []
    except (socket.gaierror, UnicodeError):
        infos = []
    if not infos:
        raise InvalidRequest(f"{raw[:120]!r} is no address or name that resolves here", details={"reason": "follow_to"})
    for family, _, _, _, sockaddr in infos:
        try:
            with socket.socket(family, socket.SOCK_DGRAM) as s:
                for option in bind.options(interface, family) if interface else ():
                    s.setsockopt(*option)
                s.connect(sockaddr)
                return str(s.getsockname()[0])
        except OSError:
            continue
    raise Unavailable(f"this machine has no way out to {host}" + (f" by {interface}" if interface else ""))


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


    """
    with _owned(api_key, base_url) as t:
        return t.get(f"/v1/gpus/places?{urlencode({'q': q, 'limit': int(limit)})}")["data"]


def list(*, api_key: str | None = None, base_url: str | None = None) -> dict[str, Any]:
    """
    Your GPU machines that are live, and how many cards of your GPU limit they hold:
    `{"gpus": [{"id", "place", "gpu", "cards", "request", "request_cards", "status", "started_at",
    "address", "ssh_port", "ports", "allow", "image", "robots", "run", "usd_so_far", "usd_per_hour"}],
    "quota": {"used", "limit"}}`, oldest first, `quota` in cards (a machine of four holds four). `gpu` is
    its card and `cards` how many it has; `request` and `request_cards` its own id and cards again, as
    one `add` opens one machine. `place` is the place you gave `add`, as you gave it (None for one added
    before it was kept); `status` is "starting" or "running" (SSH connects now). Once it runs: `address`,
    where it is reached,
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
    `{"gpus": [{"id", "place", "gpu", "cards", "request", "request_cards", "status", "reason"?, "started_at",
    "ended_at", "usd_so_far", "usd_per_hour"}], "total", "offset", "next_cursor"}`, `cards`, `request` and
    `request_cards` as `list` says them. `status` is "shut_down" (removed, or ended
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
