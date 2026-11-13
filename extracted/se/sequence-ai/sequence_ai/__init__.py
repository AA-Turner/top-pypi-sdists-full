"""
sequence_ai — the Python client for the Sequences robot inference API.

── In one sentence ───────────────────────────────────────────────────
`connect()` opens one HTTP connection and hands back a `Policy`: your robot hands it what it
observes (`observe`), asks it what to do when your own code says so (`act`), and plays the answer
its own way, at its own rate.

    import sequence_ai

    with sequence_ai.connect("my_policy_user") as policy_user:
        policy_user.observe(frame_user)                   # as the robot makes it; never blocks
        actions_user = policy_user.act()                  # when your code wants them: what the act function returned
        for step_user in actions_user:                    # played by your code, at your rate
            robot_user.apply(step_user)
        policy_user.end_episode()

    policy_user.interrupt()      # from any thread, at any moment

── Two brains, one string between them ───────────────────────────────
A VLM looks at a snapshot, decides *what* to do next, and says it in a sentence. This package is
the *how*. The two halves run at completely different speeds — the brain thinks between
subtasks, the arm needs a chunk of motion every second — and that sentence is their entire
interface: the robot hands it to its policy with what it observes, as any input,
policy.observe({"instruction": ..., ...}), so the brain's clock never holds the arm's, and
`interrupt()` lets the brain change its mind mid-wait.

    slow brain   POST /v1/chat               messages in, one message out
    fast brain   this package                policy.observe(x); policy.act()

Wiring the two together — retries, failure detection, choosing the next sub-goal — is yours. This
package provides inference, not orchestration.

── What it does for you ──────────────────────────────────────────────
Three things, each of them work a loop written straight against the HTTP endpoints has to get
right before it behaves properly on a robot:

    keeps the connection open      184.9 ms of handshake otherwise paid on every call,
                                   60% of a bare request  (see _transport.py)
    classifies errors              `warming` with a retry_after_s is "wait 118 s"; a plain
                                   Unavailable is "stop" — opposite instructions (see errors)
    one driver per Policy          two threads acting through one handle interleave its
                                   episodes (see Policy._driving)

And `interrupt()` cuts through an act waiting on a starting worker or a slow answer, so stop
latency is never a property of the service (see Policy.interrupt).

None of these is guesswork. Each is a defect that existed in this client, was measured, and
was fixed; the cited modules carry the measurements.

── Safety ────────────────────────────────────────────────────────────
An action returned by any model is model output, not a safe robot command. This library does
not check joint limits, reachability, collisions, velocity, or anything else. Bounds
checking and an e-stop belong between this library and your motors. connect(on_stale=) is told
the moment the arm runs out of answer, to hold it - no emergency stop, which stays physical.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from typing import Any

from ._core.names import segment





from ._core.catalogue import Model
from ._core.encode import DEFAULT_JPEG_QUALITY, encode, image_size, resize_image
from ._core.stale import Stale
from ._core.transport import DEFAULT_BASE_URL, Transport
from .act import Interrupted, Policy, Ready
from .act.teleop_handle import TeleopHandle
from .chat import ChatResult, ChatStream, Conversation, cached, chat, image
from .decide import DecideResult, decide

from .markers import Depth, Tactile, Video
from ._core.direct import DirectConnection
from ._core import teleop as _teleop
from ._core import teleop_link as _teleop_link
from ._core import teleop_robot as _teleop_robot
from ._core.teleop import Teleop
from ._core.recorder import Recorder
from ._core import mock_gate


from . import gpu
from ._core.reporting import INGEST_PATH, Reporter, connect_record, latency_record, run_record
from .errors import (
    AuthError,
    CertPinError,
    Conflict,
    NewVersion,
    Gone,
    GpuBadRequest,
    GpuNoCard,
    GpuOverLimit,
    InternalError,
    InvalidRequest,
    MissingPackage,
    NotFound,
    OutOfCredit,
    PLANNERS_GONE,
    PermissionDenied,
    PolicyError,
    SequencesError,
    StreamRefused,
    TELEOP_BY_KEY,
    TELEOP_NAMED,
    Unavailable,
    from_response,
)

__all__ = [
    "connect",


    "teleop",
    "Teleop",

    "record",
    "Recorder",

    "Video",
    "Depth",
    "Tactile",
    "models",
    "account",

    "gpu",


    "gpus",
    "billing",
    "usage",
    "fleet",

    "chat",

    "Conversation",
    "image",
    "cached",
    "decide",
    "encode",

    "resize_image",
    "image_size",
    "DEFAULT_JPEG_QUALITY",
    "Policy",
    "Interrupted",
    "Ready",

    "Stale",
    "Model",
    "ChatResult",
    "ChatStream",
    "DecideResult",

    "SequencesError",
    "InvalidRequest",
    "AuthError",
    "PermissionDenied",
    "OutOfCredit",
    "NotFound",
    "Conflict",
    "NewVersion",
    "Gone",
    "Unavailable",
    "PolicyError",
    "InternalError",
    "CertPinError",
    "StreamRefused",
    "MissingPackage",

    "GpuBadRequest",
    "GpuOverLimit",
    "GpuNoCard",
    "from_response",
    "DEFAULT_BASE_URL",
]











try:
    from importlib.metadata import version as _pkg_version

    __version__ = _pkg_version("sequence-ai")
except Exception:


    __version__ = "dev"


def _resolve_base_url(base_url: str | None) -> str | None:
    """
    Map the `mock` tier to a live local URL, leaving every other base URL untouched.

    The mock tier is the SDK's own test fixture, never a user's: with
    SEQ_INTERNAL_MOCK=1, as the SDK's tests run, `connect()`/`models()` at `mock` (the argument,
    or `SEQUENCES_BASE_URL=mock`) get the real direct-connect transport running against an
    in-process gateway + self-signed HTTPS worker - the connect → act loop offline over the same
    code path production uses, cert-pin and two auth planes included. Without it, `mock` is
    refused as not for users (mock_gate.is_mock). Any real `http(s)://` base URL falls straight
    through.
    """
    effective = base_url if base_url is not None else os.environ.get("SEQUENCES_BASE_URL")
    if mock_gate.is_mock(effective):
        from ._core.mock_direct import resolve_mock_base_url

        return resolve_mock_base_url()
    return base_url


def connect(
    model: str,
    *more: str,
    policy: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout_s: float | None = None,
    startup_timeout_s: float | None = None,
    on_warming: Callable[[float, float], None] | None = None,
    on_queue: Callable[[Any, Any, float, Any], None] | None = None,
    on_stale: Callable[[Stale], None] | None = None,
    on_resume: Callable[[Stale], None] | None = None,
    teleop: Any = None,
    hold: Any = None,
) -> Policy | TeleopHandle | tuple[Policy | TeleopHandle, ...]:
    """
    Open a connection to one policy, or to several at once - or to teleop, alone or among them.

    What `act()` returns is what the deployment's own act function returned: the
    platform converts nothing. What they mean — joint velocities, deltas, absolute targets — is the
    policy's own, stated in its template's README, and the robot-side `client.py` turns them into
    commands.

    model       the name of the policy to connect to — what `seq deploy` registered it as (its id works too) - or "teleop",
                for a robot a person drives, which needs no policy and no machine. Each name must be on this robot's list
                (`seq robot set <robot> policies=…`); one off the list is refused. A robot is picked out by its key, so
                you never write the robot's name here.
    *more       more names to connect to in the same call, each also on the robot's list: `connect("pick_user",
                "place_user", "teleop")`. One name returns one handle, as before; several return a tuple of handles in
                that order, each policy its own connection on its own worker (each billed, so connect only the ones you
                use). Every handle has observe() and act(), and those of one connect share who drives the robot. {121 §139}
    policy      gone: connecting through a planner is no more. Planning is a `@seq.plan` method of the policy itself, so
                a robot connects to its policy by its name alone; passing it raises InvalidRequest (PLANNERS_GONE).
    api_key     defaults to $SEQUENCES_API_KEY
    base_url    defaults to $SEQUENCES_BASE_URL, then the platform's gateway
    timeout_s   how long one request waits for its answer, in seconds. Unset, an act waits as long as the deployment
                allows one - the platform's, 300 s unless its check measured slower acts - and 10 s more, so
                the worker's own 504 at that deadline is what you get; 30 s where the deployment says none. Every other
                request waits 30 s. Set, it bounds every request, acts included. An act that gets no answer in time
                while its worker still runs it is never sent again: it raises Unavailable (504, details.reason
                "act_still_running"), as running it twice would. A worker busy with other robots' acts (429) is waited
                out within the same time from its first refusal, in steps no longer than its Retry-After.
    startup_timeout_s  how long an act() or wait_until_ready() waits for a worker that is starting (a
                wait_until_ready(timeout_s=) of its own wins). Unset, as long as
                the platform gives that start - a card's wait, then what the deployment's start takes - by the deadline
                it says with each answer, and 1800 s where it says none; in line for a slot, until the platform's
                queue timeout (2 minutes, the same for every deployment) ends the line. Set, that many seconds from
                the first ask, in line or not. 0 has an act raise at once instead of waiting; wait_until_ready() then
                waits as it does unset.
    on_warming  called as (waited_s, retry_s) each time an act() waits for the model to start, within
                `startup_timeout_s`: how long it has waited, and how long until it asks again; the
                default writes one line to stderr, never to stdout.
    on_queue    called as (position, eta_s, waited_s, reason) each time the robot, in line for a slot of a full
                deployment, asks again; `eta_s` is the platform's estimate of the wait, None when it sent none. The
                default writes one line to stderr ("queued for a seat: position 2 — …"), never to stdout.
                Like a cold start, a full deployment is waited out by an act() (within `startup_timeout_s`, polled
                no faster than the key's rate limit allows). `reason` is
                why there is no slot: "gpu_busy" (the platform), "gpu_limit_reached" (your account's GPUs),
                "deployment_full" (the deployment's max_gpus). Closing the policy gives the slot back at once.
    on_stale    called as (stale) the moment the answer the robot plays runs out with no answer after it in hand -
                the arm has nothing valid left to play - from a thread of the SDK's, once a stretch: hold or stop the
                arm there. Watched while the robot asks ahead (an act sent while the answer it plays has valid steps
                left, the acts `seq policy status` holds its on-time share by): `stale.reason` is "late" while that
                act is on its way, "failed" when it raised, "not asked" when the robot's loop asked for none in time.
                Unset, each is logged on "sequence_ai" and the first said once a process. It is no emergency stop:
                keep a physical one between this library and the motors.
    on_resume   called as (stale) as the next answer comes, before act() returns it - `stale.stale_s` how long the
                arm went without one: move it on there. `policy.stale` says the stretch under way and those before.
    teleop      gone: name "teleop" among the names, with the robot's own key; passing it raises InvalidRequest
                (TELEOP_NAMED).
    hold        what act() hands back while a robot with "teleop" among its names is stopped, or its person's chunk was
                played: by default the model's last answer with nothing in it, its keys kept - each array cut to no
                steps, each list empty, each dict's values emptied alike, any other value (a string, a number) None -
                {} before one.

    With "teleop" among the names (it needs sequence-ai[teleop], Python 3.10 or later: pip install
    'sequence-ai[teleop]'), a person can watch and drive this robot from a console holding its key
    (sequence_ai.teleop), connected straight to it. Its observe() sends every step to its consoles; while a person
    drives it, act() - of any handle of this connect - hands back the newest chunk they sent at once, with no network
    wait, and nothing goes to the policy's worker. Each chunk once: with none newer, `hold`, the robot staying where it
    is; while it is stopped (by a console, by its plan, or the console that drove it silent for 3 s), `hold`. An act on
    its way as it is stopped or taken comes back the same - a person's chunk or `hold`, never the policy's answer;
    on_resume waits for what the arm can play: a person's chunk, or its model's answer once it drives again. act()'s use
    and its answer's form are unchanged; `policy.driver` says who drives: "model", "human" or "stopped". The handle
    "teleop" has no model: with no one driving it, act() is `hold`.

    Use it as a context manager. The connection is what makes this worth calling at all, and
    a `Policy` that is never closed leaks a socket:

        with sequence_ai.connect("my_pi05_user") as policy_user:
            ...

    Nothing is sent at connect time — no session is opened on the server and nothing is
    billed. The first request happens on the first `act()` or `observe()`, which is where the one
    control-plane `POST /v1/act/connect` fires: it returns the worker's direct coordinates, the
    certificate fingerprint to pin, a per-worker secret, and a lease, and every steady-state
    `act` after it goes straight to that worker over one reused, cert-pinned TLS connection —
    the gateway is off the hot path. Recovery (a rotated secret, a worker that went away, an
    expiring lease, a cold fleet warming up) folds back through the gateway transparently, so the
    caller's loop never reconnects by hand. Constructing the handle is still purely local: an
    unreachable gateway or a cold model surfaces on the first request, not here.

    A robot names nothing of the policy's: its control rate, how many steps of an answer are valid and when the next is
    asked for are the policy's to declare (@seq.policy(hz=, action_chunk_valid_len=, action_chunk_replan_at=)), and
    what differs between
    robots goes in their observations: a policy's inputs and answers are its own, with no contract to check them against.
    """
    if teleop is not None:
        raise InvalidRequest(TELEOP_NAMED)
    if policy is not None:
        raise InvalidRequest(PLANNERS_GONE)
    names = (model, *more)
    drives = _teleop_link.NAME in names
    if hold is not None and not drives:
        raise TypeError('connect(hold=) is what act() hands back while a person stops the robot: it goes with "teleop" '
                        "among the names")

    driven = link = None
    if drives:
        _teleop._direct.require()
        driven = _teleop_robot.Driven() if hold is None else _teleop_robot.Driven(hold)
        link = _teleop_link.RobotLink(api_key, _resolve_base_url(base_url), driven)
    handles: list = []
    try:
        for name in names:
            handles.append(TeleopHandle(driven, link) if name == _teleop_link.NAME else
                           _connect(name, api_key=api_key, base_url=base_url, timeout_s=timeout_s,
                                    startup_timeout_s=startup_timeout_s, on_warming=on_warming, on_queue=on_queue,
                                    teleop=driven, on_stale=on_stale, on_resume=on_resume))
    except BaseException:
        for handle in handles:
            handle.close()
        raise
    if link is not None:
        link.start()
    return handles[0] if not more else tuple(handles)


def teleop(policy: Any = None, *, key: str | None = None, operator: str | None = None, base_url: str | None = None,
           timeout_s: float | None = None) -> Teleop:
    """
    A person's console for one robot: watch it, take it, drive it with action chunks, hand it back, stop it - connected
    straight to the robot, its pictures and commands reaching no server of ours.

        with sequence_ai.teleop(key=ROBOT_KEY_user, operator="alice_user") as op_user:
            for step_user in op_user.stream():     # the robot's newest view: {"episode", "seq", "observation", "t_us"}
                ...
            op_user.take()                         # one person at a time: Conflict while another drives it
            op_user.send({"actions": chunk_user})  # the robot's next act() hands it back, at once
            op_user.release()                      # back to its model; op_user.stop() stops it where it is

    policy      gone: the key says which robot; passing it raises InvalidRequest (TELEOP_BY_KEY)
    key         the robot's own key - the one its loop connects with; defaults to $SEQUENCES_API_KEY
    operator    the name this console goes by: who drives, in the robot's audit trail
    base_url    defaults to $SEQUENCES_BASE_URL, then the platform's gateway
    timeout_s   how long the platform's answers may take, 10 s unset; meeting the robot takes 15 s at least

    It needs sequence-ai[teleop] (Python 3.10 or later): pip install 'sequence-ai[teleop]'. The robot must be connected,
    with "teleop" among its names: Conflict while it is not (details.reason "robot_not_connected"), and for a robot whose
    list does not name teleop ("teleop_not_listed"). Unavailable, saying why, where the two cannot reach each other
    (details.reason "direct_failed": both behind symmetric NAT, a network that lets no UDP out...): nothing goes any
    other way in its place. A console that drives the robot and goes - closed, or silent for 3 s - stops it; one that
    only watches changes nothing by going. stream() hands on the robot's newest view each time something new comes: at most 8
    cameras are sent, in the order the robot first observes them, and a camera's frame may be a few steps from the arrays
    beside it, behind them or ahead. op.driver is who drives as the robot last said it, a dict - {"driver": "model",
    "human" or "stopped", "by": who, "since": its epoch second} - where the robot's own handle's driver is that one word.
    metrics() says how late its commands and the robot's steps were: p50, p95 and p99 of each, in microseconds.
    """
    if policy is not None:
        raise InvalidRequest(TELEOP_BY_KEY)
    _teleop._direct.require()

    gateway = Transport(api_key=key, base_url=_resolve_base_url(base_url),
                        timeout_s=max(timeout_s or 10.0, _teleop.PAIRING_WAIT_S + 10.0))
    try:
        return Teleop(gateway, operator=operator, timeout_s=timeout_s or 10.0)
    finally:
        gateway.close()


def record(policy: str, *, key: str | None = None, base_url: str | None = None,
           timeout_s: float | None = None) -> Recorder:
    """
    Your own recorder of a policy's steps: every step each of its robots runs, straight from the workers that served it,
    for you to write wherever you keep your data - the platform keeps none of it.

        with sequence_ai.record("pick_user", key=RECORD_KEY_user) as rec_user:
            for item_user in rec_user.steps():      # one act ("step"), a label, an episode's end, or a gap
                my_bucket_user.write(item_user)

    policy      the deployment, as connect() names it; record must be on: `seq policy set <name> record=on`
    key         a record key of the policy (`seq record add --policy <name>`): it reads this policy's steps and opens
                nothing else; defaults to $SEQUENCES_API_KEY
    base_url    defaults to $SEQUENCES_BASE_URL, then the platform's gateway
    timeout_s   how long the platform's answer and each worker's opening may take: 10 s unset

    Each worker keeps its newest minute (60 s, 32 MiB at most) in its memory for you, nothing on disk: a recorder away
    longer is told how many records it lost (a "gap" item). One that must have no gap keeps capture on as well. Conflict
    while record is off (details.reason "record_off"); Forbidden for a key that is no record key of the policy.
    """
    resolved = _resolve_base_url(base_url)
    gateway = Transport(api_key=key, base_url=resolved, timeout_s=timeout_s or 10.0)
    try:
        return Recorder(gateway, policy, timeout_s=timeout_s or 10.0)
    except BaseException:
        gateway.close()
        raise


def _connect(model: str, *, api_key: str | None, base_url: str | None, timeout_s: float | None,
             startup_timeout_s: float | None, on_warming: Callable[[float, float], None] | None,
             on_queue: Callable[[Any, Any, float, Any], None] | None, teleop: Any = None,
             on_stale: Callable[[Stale], None] | None = None,
             on_resume: Callable[[Stale], None] | None = None) -> Policy:
    """connect()'s body: `model` the policy it is seated on, sent to the gateway as `robot_of`."""




    resolved = _resolve_base_url(base_url)
    if resolved is not base_url:



        api_key = api_key or os.environ.get("SEQUENCES_API_KEY") or "mock"
    gateway = Transport(api_key=api_key, base_url=resolved, timeout_s=timeout_s, robot_of=model)





    reporter_gateway = Transport(api_key=api_key, base_url=resolved,
                                 timeout_s=min(timeout_s or 10.0, 10.0))

    def _send_reports(batch: list) -> None:




        records = [latency_record(r, model) for r in batch if "run" not in r and "connect" not in r]
        runs = [run_record(r["run"], model) for r in batch if "run" in r]

        connects = [connect_record(r["connect"], model) for r in batch if "connect" in r]
        payload: dict = {}
        if records:
            payload["records"] = records
        if runs:
            payload["runs"] = runs
        if connects:
            payload["connects"] = connects
        if payload:
            reporter_gateway.post(INGEST_PATH, payload)

    reporter = Reporter(_send_reports, on_close=reporter_gateway.close)
    return Policy(


        DirectConnection(gateway, model=model, timeout_s=timeout_s, teleop=teleop),
        model=model,
        reporter=reporter,




        startup_timeout_s=startup_timeout_s,
        on_warming=on_warming,
        on_queue=on_queue,
        on_stale=on_stale,
        on_resume=on_resume,
    )


def __getattr__(name: str) -> Any:
    """`sequence_ai.planner(...)` and `sequence_ai.Planner` are gone with planners: they say so (PLANNERS_GONE)."""
    if name in ("planner", "Planner"):
        raise AttributeError(PLANNERS_GONE)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def models(
    *,
    kind: str | None = None,
    endpoint: str | None = None,
    api_key: str | None = None,
    base_url: str | None = None,
) -> list[Model]:
    """
    Everything on the platform you can start from, as one list: the models it serves itself
    (`kind="model"` — call them with a key: `endpoint="chat"` vision-language, `"decide"` decision)
    and the templates `seq init` writes (`kind="template"` — `template_kind` "policy", "benchmark" or
    "adapter", `stable` / `beta` the version each channel points at, `usage` the command).

    No arguments: all of it. `kind="model"` / `kind="template"` keep one kind; `endpoint=` keeps the
    models answering on it (a template has no endpoint). `seq models` prints the same list. A robot
    policy you deployed is not in it — connect(<your deployment's name>).

    Fetched from the server every call rather than shipped as a constant in this package: a
    hard-coded list goes stale the moment a model is added, and a client that disagrees with
    the server about what exists is worse than one that has to make a request to find out.

    """
    if kind not in (None, "model", "template"):
        raise InvalidRequest(f"kind={kind!r}: models() lists kind='model' and kind='template'")
    if endpoint not in (None, "chat", "decide"):
        raise InvalidRequest(f"endpoint={endpoint!r}: the catalogue lists chat and decide models; a robot policy "
                             "is your own deployment — connect(<its name>)",
                             hint="seq init <template> my_policy_user && seq deploy my_policy_user "
                                  "(seq init --list names the templates)")
    if endpoint and kind == "template":
        raise InvalidRequest("a template has no endpoint; drop endpoint= or ask for kind='model'")


    t = Transport(api_key=api_key, base_url=_resolve_base_url(base_url), require_key=False)
    try:
        out: list[Model] = []
        if kind != "template":
            body = t.get("/v1/models" + (f"?endpoint={segment(endpoint, 'endpoint')}" if endpoint else ""))

            out += [_to_model(d) for d in body["data"]]
        if kind != "model" and not endpoint:


            out += [_to_template(d) for d in t.get("/v1/templates").get("data", [])]
        return out
    finally:
        t.close()

def account(*, api_key: str | None = None, base_url: str | None = None) -> dict[str, Any]:
    """
    With a full key, your whole account: what this month has spent, current usage and limits, and its GPUs —
    what `seq account` prints. With a robot key, only the one deployment it is for (below).

    Billing is postpaid: usage is billed at the month's end, the plan's monthly credit spent first, up to the
    plan's monthly limit - and past the credit only with a payment method on the account. So a CI job or control
    loop can check this before a big run instead of meeting the limit as an `OutOfCredit` mid-way:
    `balance["spendable"]` is what the account may spend now - its credits and any payment method's line, at most
    what this month's limit, where its plan has one, leaves past what was spent and what running workers and evals
    hold (`held_usd`) - the figure `seq account` says is left to spend and the console's Left to spend; work that
    would spend past it is refused. `balance` also holds `period_spent_usd` (this month so far), `credit_usd` and `credit_left_usd`,
    `month_limit_usd` and `month_left_usd` (the limit less this month's spend, before what is held), and
    `payment_method` ({"brand", "last4", "exp_month", "exp_year"}, or None). Returns
    `{"balance": {"spendable", "period_spent_usd", "month_left_usd", ...}, "usage": {"policies", "benchmarks"},
    "limits": {...}, "gpus": {"limit", "in_use": {"serving", "eval", "total"}, "available", "waiting_evals": [...]}}` —
    `limits` only carries the per-account knobs that are configured; in `gpus`, a count the platform
    could not read is None (unknown — never read it as "full"), and `waiting_evals` lists the evals in
    line for GPUs ({eval_id, cards, waited_s, gives_up_at}). Read-only: creating keys and adding a payment
    method stay in the console.


    With a robot key the answer is that deployment's alone - `{"scope": "deployment", "deployment": name,
    "usage": {window_days, gpu_card_s, gpu_usd, cpu_core_s, cpu_usd, memory_gib_s, memory_usd, total_usd, calls,
    errors}}`, what its machines cost over the last 30 days: the account's balance, limits, other deployments and
    bills need a full key.
    """

    t = Transport(api_key=api_key, base_url=_resolve_base_url(base_url), login=True)
    try:
        return t.get("/v1/account")
    finally:
        t.close()


def gpus(*, base_url: str | None = None) -> dict[str, Any]:
    """
    The cards you can choose and what they cost and can do, and what a CPU core and a GiB of memory
    cost — what `seq gpus` prints, from the platform's one price list (the pricing page reads the same).

    Returns `{"gpus": [{"gpu", "usd_per_hour", "usd_per_second", "vram_gb", "policy", "benchmark",
    "rt_core", "nvenc"}], "cpu": {"usd_per_core_hour", "serving_usd_per_core_hour"},
    "memory": {"usd_per_gib_hour", "serving_usd_per_gib_hour"}, "storage": {"usd_per_gb_month"},
    "policy_machines": {card: {"cpu", "memory_gib"}}, "min_billable_s"}`. `gpu` is the name `gpu=` takes;
    `usd_per_hour` one card's hour alone; `benchmark` says whether a benchmark's sims may run on it; `cpu` and
    `memory` what a core and a GiB cost an hour - `serving_*` for a policy's workers, deployed or in an eval, the
    others for builds, checks, shells and an eval's benchmark machines. CPU and memory are billed apart from the card: an hour of a policy's worker is its
    cards x `usd_per_hour` + its card's standard machine (`policy_machines`), or what it declares where more, at the
    `serving_*` rates, wherever it runs; a benchmark's machine on a shared machine pays the greater of what it
    requests (0.125 at least) and what it uses, its request on a machine of its own; and a worker that declares no GPU
    pays no card.
    `min_billable_s` the seconds a machine's card is billed at least each time it starts - an eval's machines, their CPU
    and memory too; `storage` what a GB of a deployment's
    weights copy, its image or a volume costs a month, billed daily for as long as it is kept
    (absent when the price cannot be read).
    No key needed: the prices are public.
    """
    t = Transport(base_url=_resolve_base_url(base_url), require_key=False)
    try:
        return t.get("/v1/pricing")
    finally:
        t.close()


def billing(start: str, end: str, *, csv: bool = False, api_key: str | None = None,
            base_url: str | None = None) -> Any:
    """
    Your account's bill, day by day, per deployment and resource, from `start` to `end`
    (YYYY-MM-DD, both included) — the bill as the platform keeps it, per day, deployment and resource.

    Returns the rows `[{"day", "deployment", "resource", "qty", "unit", "usd"}]`, where `resource` is a
    card type, "cpu" or "memory"; `csv=True` returns the same rows as CSV text instead.

    """
    from urllib.parse import urlencode

    query = urlencode({"from": start, "to": end, "format": "csv" if csv else "json"})
    t = Transport(api_key=api_key, base_url=_resolve_base_url(base_url), login=True)
    try:
        if csv:
            r = t._client.get(f"/v1/account/billing?{query}")
            if r.status_code >= 300:
                Transport._unwrap(r)
            return r.text
        body = t.get(f"/v1/account/billing?{query}")
    finally:
        t.close()
    return list(body["rows"])


def _owned_get(path: str, api_key: str | None, base_url: str | None) -> dict[str, Any]:
    t = Transport(api_key=api_key, base_url=_resolve_base_url(base_url), login=True)
    try:
        return t.get(path)
    finally:
        t.close()


def usage(model: str, *, days: int = 30, api_key: str | None = None, base_url: str | None = None) -> dict[str, Any]:
    """
    A deployment's use per day over the last `days` — what the console's usage page shows, and where `seq usage --policy
    <name>` reads its robots' acts from: `{"days": [{"day", "gpu_card_s", "cpu_core_s", "memory_gib_s", "gpu_usd", "cpu_usd", "memory_usd",
    "calls", "p50_ms", "p95_ms", "errors"}]}`. GPU time is in card-seconds: a 2-card worker for one second is 2.

    """

    return _owned_get(f"/v1/deployments/{segment(model)}/usage?days={int(days)}", api_key, base_url)


def fleet(model: str, *, api_key: str | None = None, base_url: str | None = None) -> dict[str, Any]:
    """
    A deployment's workers and the robots waiting for one — what `seq policy status` shows below the state:
    `{"max_gpus", "target", "max", "workers": [{"handle", "state", "gpu", "cards",
    "slots", "sessions", "started_at", "reason"}], "queue": [{"position", "session", "queued_s"}]}`. A worker's
    `reason` says why it died: "gpu_out_of_memory", "host_out_of_memory", "crashed", "hung" (its copies ended in a
    call past twice its time limit), "group_member_lost" or "load_failed".

    """

    return _owned_get(f"/v1/deployments/{segment(model)}/fleet", api_key, base_url)


def _to_model(d: dict[str, Any]) -> Model:
    """
    Map a catalogue row, keeping the untouched dict in `.raw`.

    Only the fields a caller needs to *construct a request* are lifted into attributes — which
    model, and which endpoint it answers on; the rest (pricing, licence, latency, tags) stay in
    `.raw`. Lifting everything would mean this function has to change every time the catalogue
    grows a field, and forgetting to update it would silently drop data the server sent.
    """
    return Model(
        id=d["id"],
        endpoint=d.get("endpoint", ""),
        architecture=d.get("architecture", ""),
        raw=d,
    )


def _to_template(d: dict[str, Any]) -> Model:
    """A GET /v1/templates row ({name, kind, stable, beta}) as a `kind="template"` entry, the row kept in `.raw`."""
    return Model(
        id=d["name"], endpoint="", architecture="", raw=d, kind="template",
        template_kind=d.get("kind"), stable=d.get("stable"), beta=d.get("beta"),
        usage=f"seq init {d['name']}",
    )
