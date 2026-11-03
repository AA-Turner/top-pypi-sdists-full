"""
GPUs, what they cost, and how a deployment uses them: `seq gpus`, `seq account`, a deployment's max GPUs,
`seq policy status`'s fleet view, and the price `seq deploy` prints. (What the account's machines used and cost is
`seq usage`, seq/usage_hist.py: it read three ways before, `seq billing export` and `seq policy usage` among them.)

In one sentence: each command reads one gateway route with the caller's key → prints it in the
units the platform's limits are made of — cards, never workers; a count the platform could not read says "unknown",
never "full" — and returns what it read, which `seq --json` prints instead. The same from Python, with the client's
typed errors: `sequence_ai.gpus()`, `.account()`, `.billing()`, `.usage()`, `.fleet()`, `.scale()`.

WHY one module: these are the questions the limits raise — which cards exist and what they cost, how many the account
holds and how many are left, what a deployment used and spent, why a worker died. Before them a person learned that
the account was at its GPU limit only from a refusal.

"""
from __future__ import annotations

import math
from typing import Any, Callable, Optional

from sequence_ai._core.capacity import LOAD_MAX, count, held, wait_said

from seq.clock import stamp
from sequence_ai._core.money import money, per_hour, whole
from seq.deployments_cli import _call
from sequence_ai._core.names import segment

Echo = Callable[..., None]


MIN_CPU_CORES = 0.125
MIN_MEMORY_GIB = 0.125





DEATH = {

    "gpu_out_of_memory": "out of GPU memory: its model copy did not fit on the card — declare a card with more memory",
    "host_out_of_memory": "out of the worker's memory — declare more with @seq.policy(memory=...); a worker of several "
                          "cards may instead start their copies one at a time: "
                          "@seq.policy(replica_start=\"one_by_one\")",
    "crashed": "its policy process kept crashing — `seq policy logs <name>` shows why",
    "hung": "its policy kept hanging in infer (each copy ended in a call past twice its time limit), so the worker "
            "stopped — `seq policy logs <name>` shows the lines it printed before it hung",
    "group_member_lost": "one machine of its group stopped, so the whole group stopped; the next connect starts a new "
                         "group — `seq policy logs <name>` shows which machine and why",
    "load_failed": "loading the policy raised while its worker started — `seq policy logs <name>` shows the error and "
                   "the lines it raised in",
}



SERVED_NOT = {
    "image_failed": "its image could not be built or pulled — `seq policy logs <name>` shows the lines its build ended "
                    "with",
    "fetch_failed": "its files could not be downloaded — the next connect starts another machine",
    "gpu_failed": "its machine could not reach its GPU — the next connect starts another machine",
}




NEVER_UP = {
    "no_card": "no card of its kind was free where it was placed",
    "quota": "the platform's limit of its card where it was placed was reached",
    "boot_timeout": "its machine did not come up in time",
    "start_error": "its machine could not be created",
    "taken_back": "its machine was taken back",
}





EPISODE_LOST = {
    "gpu_out_of_memory": "out of GPU memory",
    "host_out_of_memory": "out of host memory",
    "crashed": "in a crash",
    "hung": "with an act far past its time limit",
    "group_member_lost": "when a machine of its group stopped",
    "idle": "idle past its idle time",
    "unknown": "for a cause not recorded",
}





WHY = {
    "cold-start": "started for a robot that connected",

    "first-worker": "the machine its version's check ran on, kept on as its first worker",
    "resume": "started again for a robot that reconnected",
    "min_containers": "kept running: the policy's min workers",
    "min_workers": "kept running: the policy's min workers",
    "warm_hours": "kept running: the policy's warm hours",
    "buffer": "a spare, ready for the next robot (buffer workers)",
    "replacement": "started to take over from a worker that has served its hours",


    "version-replacement": "started to serve a new version",
    "probe-alive": "its robot's lease ran out while it still answered: kept a little longer",
    "idle-cooldown": "stopped: no robot acted on it for the idle timeout",
    "unclaimed": "stopped: no robot took it within a minute of starting; billed until then",
    "surplus": "stopped: a second worker was started for the same place; not billed",

    "warm-hours-ended": "stopped: its warm hours ended",
    "min-workers-lowered": "stopped: the policy's min workers went down",
    "spare-unneeded": "stopped: no robot needed it as a spare any more",
    "lease-expired": "stopped: its robot stopped renewing its session",
    "version-retired": "stopped: another version serves",
    "max-lifetime": "stopped: it reached the longest a worker runs",
    "rotate": "replaced after serving its hours",
    "rotated": "replaced after serving its hours",
    "boot-timeout": "stopped: it did not start in time",
    "gone-while-starting": "ended while it was starting",
    "gone": "ended by the platform",
    "interrupted": "ended: its machine was taken away",
    "unhealthy": "replaced: it stopped answering",
    "leak-reconcile": "ended: no longer in use",
    "error": "ended after an error",


    "resume-no-card": "started new: its stopped worker could not start again, no card available where it was",
    "resume-failed": "started new: its stopped worker could not start again",

    "stopped-expired": "ended: kept stopped for a fast start, unused for the days one is kept",
    "stopped-surplus": "ended: its version keeps one stopped worker for a fast start, the one used last",
}


LIMITS = {"max_policies_per_user": "policies", "max_benchmarks_per_user": "benchmarks",
          "max_production_policies_per_user": "production policies", "max_keys_per_user": "dev and production keys",
          "max_robot_keys_per_user": "robot keys", "max_planner_keys_per_user": "planner keys",
          "max_calls_per_min": "calls a minute",
          "max_gpus_per_user": "GPUs at once", "daily_spend_cap_per_user_usd": "daily spend (USD)"}


def why(reason: Any, name: str) -> str | None:
    """A worker's reason in words: its cause when it ended of one ("unhealthy (gpu_out_of_memory)"), else the event's,
    else None."""
    if not isinstance(reason, str):
        return None
    base, _, cause = reason.partition(" (")
    cause = cause.rstrip(")")
    if base == "gone-while-starting" and cause in NEVER_UP:
        return f"{WHY[base]}: {NEVER_UP[cause]}"
    said = {**DEATH, **SERVED_NOT}
    text = said.get(cause) or said.get(base) or WHY.get(base)
    return text.replace("<name>", name) if text else None


def _silent(*_args: Any, **_kwargs: Any) -> None:
    """The `echo` of a Python call: it returns what it read and prints nothing."""


def _yes(v: Any) -> str:
    return "yes" if v is True else "no" if v is False else "—"


def _usd(v: Any, fmt: Callable[[Any], str] = money) -> str:
    """An amount, a price an hour (per_hour) or a plan's whole dollars (whole) as sequence_ai/_core/money.py writes
    them; '—' where the platform did not say it."""
    return fmt(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else "—"


def _clock(at: Any) -> str:
    """An ISO time or epoch seconds on this machine's clock, '17:10 EDT' (with the date when it is not today here); '—'
    when absent (seq/clock.py)."""
    return stamp(at)



def gpus(*, base_url: str | None = None, echo: Echo = _silent) -> dict:
    """The cards `gpu=` can name — memory, price per hour (usage is billed by the second, a price said by the hour:
    sequence_ai/_core/money.py), whether a policy and a benchmark may use it, RT cores, video encoding — and the CPU
    and memory prices. Public: no key needed. No render column: the figure was a
    fixed per-card estimate, never measured
 ."""
    import sequence_ai

    prices = sequence_ai.gpus(base_url=base_url)
    show_gpus(prices, echo)
    return prices


def show_gpus(prices: dict, echo: Echo) -> None:
    from sequence_base.constants.cards import DEFAULT_BENCHMARK_GPU

    rows = prices.get("gpus") or []
    w = max([len("card")] + [len(str(g.get("gpu"))) for g in rows]) + 2
    echo(f"{'card':{w}}{'VRAM':>7}  {'price':>10}  {'policy':8}{'benchmark':15}{'RT core':9}NVENC")
    for g in rows:
        vram = f"{g['vram_gb']} GB" if g.get("vram_gb") is not None else "—"
        bench = _yes(g.get("benchmark")) + (" (default)" if g.get("benchmark") and g.get("gpu") == DEFAULT_BENCHMARK_GPU
                                            else "")
        echo(f"{str(g.get('gpu')):{w}}{vram:>7}  {_usd(g.get('usd_per_hour'), per_hour):>10}  "
             f"{_yes(g.get('policy')):8}{bench:15}{_yes(g.get('rt_core')):9}{_yes(g.get('nvenc'))}")
        if g.get("regions"):
            echo(f"{'':{w}}runs in {', '.join(g['regions'])}")
    if not rows:
        echo("(no cards are offered right now)")
    cpu_rates, mem_rates = prices.get("cpu") or {}, prices.get("memory") or {}
    cpu, memory = cpu_rates.get("usd_per_core_hour"), mem_rates.get("usd_per_gib_hour")


    if cpu_rates.get("serving_usd_per_core_hour") is not None:
        echo(f"CPU     {_usd(cpu_rates['serving_usd_per_core_hour'])} per core-hour serving a policy; "
             f"{_usd(cpu)} on checks, evals and benchmarks")
    else:
        echo(f"CPU     {_usd(cpu)} per core-hour")
    if mem_rates.get("serving_usd_per_gib_hour") is not None:
        echo(f"memory  {_usd(mem_rates['serving_usd_per_gib_hour'])} per GiB-hour serving a policy; "
             f"{_usd(memory)} on checks, evals and benchmarks")
    else:
        echo(f"memory  {_usd(memory)} per GiB-hour")
    storage = (prices.get("storage") or {}).get("usd_per_gb_month")
    if storage is not None:



        shared = (prices.get("storage") or {}).get("shared_weights_templates") or []
        echo(f"storage {_usd(storage)} per GB-month: a deployment's copy of its weights and the image its versions save, and "
             "your volumes - billed every day they are kept, whether or not a worker runs; deleting stops it"
             + (f" (an official template's weights - {', '.join(shared)} - are read from the platform's copy, not "
                "copied or billed, while its code is unchanged)" if shared else ""))


    echo("CPU and memory are billed per second on the greater of what a worker requests and what it uses; a worker "
         "that declares no GPU pays those alone, no card.")



    floor = prices.get("min_billable_s")
    if floor:
        echo(f"Each time a machine starts, its card is billed for at least {float(floor):.0f} s, and an eval's machines "
             "for at least that much CPU and memory too.")

    echo('gpu="TYPE:N" takes N cards of one type. A deployment runs on its one card and waits '
         'for it to come free - up to 10 min.')



def _account_id(base_url: str | None) -> str | None:
    """The account's id - the one the console's Account page asks for to delete it - read as you (GET /v1/account/person) when you are
    signed in on this machine; None with a key alone - the id is the person's to read - or when it could not be read."""
    from sequence_ai._core import login as signin

    from seq.login_cli import _base

    if signin.saved(_base(base_url)) is None:
        return None
    try:
        return (_call("GET", "/v1/account/person", base_url, person=True) or {}).get("account_id") or None
    except Exception:
        return None


def account(*, base_url: str | None = None, echo: Echo = _silent) -> dict:
    """The account's balance, its GPUs (limit, held by serving, by evals and by build checks, available, the evals
    waiting for GPUs), usage and limits - or, with a robot key, the one deployment it is for (show_deployment); signed
    in, headed by the account's id, the one the console's Account page asks for to delete it.
"""
    out = _call("GET", "/v1/account", base_url)
    acct = _account_id(base_url)
    if acct:
        echo(f"account   {acct}")
    show_account(out, echo)
    return {**out, "account_id": acct} if acct and isinstance(out, dict) else out


def own(key: str, value: Any, overrides: Any, plan: Any) -> str:
    """' (raised for this account; Starter: 5)' beside a limit the account has of its own, not its plan's (GET
    /v1/account limit_overrides, each with its plan's value), else '' - the shared test account's 20 policies read as
    Starter's, whose are 5."""
    o = overrides.get(key) if isinstance(overrides, dict) else None
    if not isinstance(o, dict):
        return ""
    base = o.get("plan")
    raised = isinstance(value, (int, float)) and isinstance(base, (int, float)) and value > base
    name = str((plan or {}).get("name") or "plan").capitalize() if isinstance(plan, dict) else "plan"
    return f" ({'raised' if raised else 'set'} for this account; {name}: {'none' if base is None else f'{base:g}'})"


def show_deployment(out: dict, echo: Echo) -> None:
    """What `seq account` says with a robot key: the platform answers a robot's key with the one deployment it is
    for (GET /v1/account scope "deployment") - what its machines used and cost over the window, its acts and errors - so
    the first line says whose figures they are, and they never read as the account's. {the user 10-14, relayed by third
    plan: "this shold limit to the account only on that deploymente..g the ocst of that machine not the entire account
    all models"}"""
    name = out.get("deployment") or "its deployment"
    u = out.get("usage") or {}

    def hours(seconds: Any) -> str:
        return f"{float(seconds or 0) / 3600:,.2f}"



    echo(f"{name} only: this key is a robot key of {name}, so these are that one policy's figures, not the "
         f"account's - `seq policy status {name}` shows how it runs; the account's balance, limits, other policies and "
         "bills need a full key")


    since = str(u.get("from") or "")[:10]
    window = f"this billing period (from {since} UTC)" if since else "this billing period"



    saves = (f" · image saves {float(u.get('network_gb') or 0):,.2f} GB sent {_usd(u.get('network_usd'))}"
             if float(u.get("network_usd") or 0) > 0 else "")
    echo(f"{window}  GPU {hours(u.get('gpu_card_s'))} card-hours {_usd(u.get('gpu_usd'))} · CPU "
         f"{hours(u.get('cpu_core_s'))} core-hours {_usd(u.get('cpu_usd'))} · memory {hours(u.get('memory_gib_s'))} "
         f"GiB-hours {_usd(u.get('memory_usd'))} · storage {float(u.get('storage_gb_months') or 0):,.2f} GB-months "
         f"{_usd(u.get('storage_usd'))}{saves} · {_usd(u.get('total_usd'))} in all")
    if isinstance(u.get("calls"), int):
        echo(f"acts  {u['calls']:,} · {int(u.get('errors') or 0):,} errors")


def show_account(out: dict, echo: Echo) -> None:
    if out.get("scope") == "deployment":
        show_deployment(out, echo)
        return
    bal = out.get("balance") or {}
    overrides, plan = out.get("limit_overrides"), out.get("plan")
    show_plan(plan, bal.get("free_credit"), echo, overrides)
    show_spend(bal, echo)
    g = out["gpus"]
    in_use = g.get("in_use") or {}
    echo(f"GPUs      limit {count(g.get('limit'))} · in use {count(in_use.get('total'))} ({held(in_use)}) · "
         f"{count(g.get('available'))} available")
    waiting = g.get("waiting_evals") or []
    for w in waiting:
        waited = w.get("waited_s")

        echo(f"  queued: eval {w.get('eval_id')} needs {count(w.get('cards'))} GPUs"
             + (f", waited {float(waited):.0f} s" if isinstance(waited, (int, float)) else "")
             + f", gives up at {_clock(w.get('gives_up_at'))}")
    if not waiting:
        echo("  no eval is queued for GPUs")
    show_compute(out.get("compute"), echo, overrides)
    usage = out.get("usage") or {}
    if usage:
        echo(f"usage     {usage.get('policies', 0)} deployment(s), {usage.get('benchmarks', 0)} benchmark(s)")
    show_storage(out.get("storage"), echo)
    limits = out.get("limits") or {}
    if limits:
        echo("limits    " + ", ".join(f"{LIMITS.get(k, k.removeprefix('max_').replace('_', ' '))} "
                                     f"{'none' if v is None else v}{own(k, v, overrides, plan)}"
                                     for k, v in limits.items()))


def show_spend(bal: Any, echo: Echo) -> None:
    """The month as billing reads it, postpaid (GET /v1/account's balance): what this month has spent, how much of the
    plan's monthly limit is left, what running workers and evals hold until they stop - and the payment method its bill
    goes to, or, with none on the account, that usage stops at the monthly credit. Nothing when the platform did not
    say what was spent. The limit and the credit are a plan's, in whole dollars, as its fee is (money.whole).
    

"""
    if not isinstance(bal, dict) or not _amount(bal.get("period_spent_usd")):
        return
    line = f"spent     {_usd(bal['period_spent_usd'])} this month"
    if _amount(bal.get("month_left_usd")) and _amount(bal.get("month_limit_usd")):
        line += f" · {_usd(bal['month_left_usd'])} of your {_usd(bal['month_limit_usd'], whole)} monthly limit left"
    held = bal.get("held_usd")
    if _amount(held) and held > 0:

        line += f" · {_usd(held)} held for running workers and evals until they stop"
    echo(line)
    card = bal.get("payment_method")
    if isinstance(card, dict):
        month, year = card.get("exp_month"), card.get("exp_year")
        echo(f"payment   {card.get('brand') or 'card'} ending {card.get('last4') or '····'}"
             + (f", expires {int(month):02d}/{int(year)}" if _amount(month) and _amount(year) else ""))
    elif "payment_method" in bal:
        credit = f"your {_usd(bal['credit_usd'], whole)} " if _amount(bal.get("credit_usd")) else "the "
        echo(f"payment   none: usage stops at {credit}monthly credit - add a payment method on the console's Billing "
             "page")


def _amount(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def show_storage(st: Any, echo: Echo) -> None:
    """Everything the account stores against its one storage limit (GET /v1/account's storage) - whose number it is, its
    own or its plan's - and once it nears it, how to raise it (storage_note). Nothing when the platform could not read
    it."""
    from seq import deps_cost, storage_note

    if not isinstance(st, dict) or st.get("limit_bytes") is None:
        return
    share = st.get("used_share")
    echo(f"storage   {deps_cost.size(st.get('used_bytes'))} of {deps_cost.size(st['limit_bytes'])}"
         + (f" ({round(float(share) * 100)}%)" if isinstance(share, (int, float)) else "")
         + f" · {storage_note.whose(st)}")
    said = storage_note.note(st)
    if said:
        echo(f"  {said}")


def show_plan(plan: dict | None, free: dict | None, echo: Echo, overrides: Any = None) -> None:
    """The account's plan - its monthly fee and free credit - and how much of this month's free credit is left: the same
    two lines the console's Billing page heads its Plan card with (GET /v1/account's plan and balance.free_credit).
    (the limits are the line below)"""
    if isinstance(plan, dict) and plan:
        name = str(plan.get("name") or "starter").capitalize()
        monthly = float(plan.get("monthly_free_credit_usd") or 0)
        echo(f"plan      {name} — {whole(plan.get('monthly_fee_usd'))} a month"
             + (f", {whole(monthly)} free credit each month" if monthly else "")
             + own("monthly_free_credit_usd", monthly, overrides, plan))
    if isinstance(free, dict) and free:
        echo(f"free      {_usd(free.get('used_usd'))} of {_usd(free.get('monthly_usd'), whole)} used this month · "
             f"{_usd(free.get('left_usd'))} left · renews {stamp(free.get('resets_at'))}")


def show_compute(c: dict | None, echo: Echo, overrides: Any = None) -> None:
    """CPU cores, memory and machines the account's live containers requested, against its plan's caps — the account
    quota a worker or an eval's machines must fit, as its GPUs."""
    if not isinstance(c, dict):
        return
    parts = []
    for key, what, unit in (("cpu_cores", "CPU", " cores"), ("memory_gib", "memory", " GiB"),
                            ("containers", "machines", "")):
        v = c.get(key) or {}
        used, cap = v.get("used"), v.get("limit")
        parts.append(f"{what} {float(used or 0):g}" + (f" of {float(cap):g}" if cap is not None else "") + unit
                     + own(key, cap, overrides, {"name": c.get("plan")}))
    plan = f" ({c['plan']} plan)" if c.get("plan") else ""
    echo(f"compute   {' · '.join(parts)} in use{plan}")




def every_words(seconds: float) -> str:
    """How often a worker is replaced, in words: `5 h`, `5 h 30 min`, `10 min` — not `0.166667 h`.
    """
    hours, minutes = divmod(round(seconds / 60), 60)
    return " ".join(p for p in (f"{hours} h" if hours else "", f"{minutes} min" if minutes else "") if p) or "1 min"



def fleet(name: str, *, base_url: str | None = None, echo: Echo = _silent, version: int | None = None,
          deploying: bool = False) -> dict:
    """A deployment's workers (state, card, copies, seats, sessions, why one died), the robots waiting for a slot, and
    the limits they run under. `version`: the version whose price, capacity and
    measurements it gives (the platform says which in `priced_version`); the serving one's without it. `deploying`:
    the read is `seq deploy`'s, after its build, so the platform's word on where its workers run names the region it
    was deployed to (its query's `dependencies=true`, the platform's name for that read)."""
    query = "&".join(q for q in (f"version={int(version)}" if version else "",
                                 "dependencies=true" if deploying else "") if q)
    out = _call("GET", f"/v1/deployments/{segment(name)}/fleet" + (f"?{query}" if query else ""), base_url)
    show_fleet(name, out, echo)
    return out


def where_line(w: dict) -> str | None:
    """Where a worker runs and why it was started there, as the platform says them (the fleet's `region`, our
    region's name, and `placed`, its why in words): "in US East: the region nearest the robot it was started for".
    None from a platform that says neither.
"""
    region = w.get("region") if isinstance(w.get("region"), str) and w["region"] else None
    placed = w.get("placed") if isinstance(w.get("placed"), str) and w["placed"] else None
    if region is None and placed is None:
        return None
    return (f"in {region}" if region else "") + (": " if region and placed else "") + (placed or "")


def _turn(w: dict) -> str | None:
    """How long a worker has served and when it is to be replaced — or, once it is leaving, why and that its robots move
    at an episode boundary to a worker already up. Said as what is to come: "replaced
    from <time>" read as done."""
    if w.get("leaving") == "version":
        return "leaving: another version serves — its robots move at their next episode boundary"
    if w.get("leaving") == "rotate":
        return "leaving: it has served its hours — its robots move to the replacement at their next episode boundary"
    if w.get("state") in ("provisioning", "resuming"):
        took = w.get("starting_s")
        return ("starting: not serving yet" + (f", {int(float(took)) // 60}m {int(float(took)) % 60:02d}s so far"
                                               if isinstance(took, (int, float)) else ""))
    if w.get("age_s") is None or not w.get("rotates_at"):
        return None
    hours, rest = divmod(int(float(w["age_s"])), 3600)
    by = f" by {_clock(w['moved_by'])} at the latest" if w.get("moved_by") else ""
    return (f"serving {hours}h {rest // 60:02d}m; to be replaced from {_clock(w['rotates_at'])}, its robots to move "
            f"between episodes{by}")


def holds_gpus(f: dict) -> bool:
    """Whether a deployment holds GPUs, from its fleet reply: it does when the reply names a card - a `gpus` block (its
    declared cards, which the gateway returns from the deploy on and leaves None for CPU, routes/fleet._gpu_list) or a
    `price` for a card (a running GPU worker). A CPU deployment has neither (its price.card is None, or "CPU" where its
    build check ran on a machine with no card), so max GPUs is nothing it needs and nothing to warn about. Read from
    `gpus`, not price alone: a fresh deploy is not priced yet, so a CPU deploy with no price was read as a GPU's and
    warned to name a cap it does not need.
    
"""
    if f.get("gpus") is not None:
        return True
    price = f.get("price")
    card = price.get("card") if isinstance(price, dict) else None
    return card is not None and str(card).strip().lower() not in ("cpu", "none")


def show_fleet(name: str, f: dict, echo: Echo) -> None:
    workers, queue = f.get("workers") or [], f.get("queue") or []



    live = [w for w in workers if w.get("state") not in ("stopped", "failed")]
    cards = sum(int(w.get("cards") or 0) for w in live)
    cap = (f"max GPUs {f['max_gpus']}" if f.get("max_gpus") else
           "no max GPUs of its own" if holds_gpus(f) else "on CPU, no GPUs")
    full = f"when full a new robot waits up to {f.get('queue_timeout_s', 120)} s for a seat"


    members = f.get("planner")
    seats = f.get("max") if f.get("max") is not None else "—"
    echo(f"fleet: {len(live)} worker(s) holding {cards} GPU(s) · {cap} · plans for {', '.join(members)}" if members else
         f"fleet: {len(live)} worker(s) holding {cards} GPU(s) · {cap} · {full} · robots per worker: {seats}"
         f"{wait_said(f)}")


    for w in f.get("waits") or ():
        echo(f"  {w.get('robot') or 'a robot'} waited p50 {w.get('p50_ms', 0):.0f} ms, p95 {w.get('p95_ms', 0):.0f} ms "
             f"for an answer ({w.get('acts')} acts)")
    now = now_line(f)
    if now:
        echo(now)

    sw = max([len("state")] + [len(str(w.get("state"))) for w in workers]) + 2




    if workers:
        echo(f"  {'worker':14}{'state':{sw}}{'card':12}up since" if members else
             f"  {'worker':14}{'state':{sw}}{'card':12}{'copies':>7}{'seats':>8}{'sessions':>10}  up since")
    for w in workers:
        card = f"{w.get('gpu') or '—'} × {count(w.get('cards'))}"
        echo(f"  {str(w.get('handle'))[:12]:14}{str(w.get('state')):{sw}}{card:12}"
             + ("" if members else f"{count(w.get('slots')):>7}{count(w.get('seats')):>8}{count(w.get('sessions')):>10}  ")
             + f"{_clock(w.get('started_at')) if w.get('started_at') else '—'}")
        if why(w.get("reason"), name):
            echo(f"    ↳ {why(w['reason'], name)}")
        where = where_line(w)
        if where:
            echo(f"    ↳ {where}")
        turn = _turn(w)
        if turn:
            echo(f"    ↳ {turn}")
        if isinstance(w.get("group"), dict):
            _show_group(w["group"], echo)
    last = f.get("last_failure")
    if last and last.get("cause"):


        d = last.get("details") or {}
        took = (f" (one copy took {d['per_replica_vram_mb'] / 1024:.1f} GiB of GPU memory; {d.get('declared')} declared, "
                f"copy {d.get('reached')} did not start)") if d.get("per_replica_vram_mb") and d.get("reached") else ""
        echo(f"last failure: a worker of v{last.get('version', '?')} stopped {_clock(last.get('at'))} — "
             f"{why(last['cause'], name) or 'it stopped serving'}{took}")
    ended = episodes_lost_line(f.get("episodes_lost"), name)
    if ended:
        echo(ended)
    show_billed_price(f.get("price"), echo)

    show_gpu(f.get("gpus"), f["scaling"]["start_wait_s"], echo)
    show_capacity(f.get("capacity"), echo, f.get("measured"))
    show_batching(f.get("measured"), echo)
    show_cuda_graphs(f.get("measured"), echo)

    show_hints(f.get("hints"), "workers", echo)

    show_sample(f.get("measured"), echo)
    show_hints(f.get("hints"), "build", echo)

    show_ceiling(name, f.get("ceiling"), echo, capped=bool(f.get("max_gpus")) or not holds_gpus(f))
    if queue:
        echo(f"queue: {len(queue)} robot(s) waiting for a slot")
        for q in queue:
            waited = q.get("queued_s")
            eta = q.get("eta_s")

            to_go = f" · about {float(eta):.0f} s to go" if isinstance(eta, (int, float)) else ""
            echo(f"  {count(q.get('position'))}. session {str(q.get('session'))[:8]}"
                 + (f"  waited {float(waited):.0f} s" if isinstance(waited, (int, float)) else "") + to_go)
    else:
        echo("queue: empty")


    show_hints(f.get("hints"), "robots", echo)
    moving = continuity_line(f.get("continuity"))
    if moving:
        echo(moving)
    show_hints(f.get("hints"), "stalls", echo)
    connected = connects_line(f.get("connects"))
    if connected:
        echo(connected)
    show_hints(f.get("hints"), None, echo)
    show_session_params(f, echo)




HINT_PLACES = ("workers", "robots", "stalls", "build", "load")


def show_hints(hints: Any, at: str | None, echo: Echo) -> None:
    """What the deployment's own measurements say is worth adding next, said beside the figure it comes from (`at`;
    None: those of a place this SDK does not know) - the platform's words as it gives them (the fleet's `hints`), a
    `hint:` line each.
"""
    for h in hints if isinstance(hints, list) else []:
        if not isinstance(h, dict) or not isinstance(h.get("says"), str) or not h["says"].strip():
            continue
        if (h.get("at") == at) if at is not None else (h.get("at") not in HINT_PLACES):
            echo(f"hint: {h['says'].strip()}")


def continuity_line(c: Any) -> str | None:
    """How well the chunks kept the robots' arms moving over the platform's window (the fleet's `continuity`): the share
    of chunks on time, to a tenth rounded down as the console says it, and the stalls with their time - the line the
    stalls' hints follow. None before any run reported them."""
    if not isinstance(c, dict) or not c.get("runs") or not isinstance(c.get("on_time_rate"), (int, float)):
        return None
    rate = float(c["on_time_rate"])
    share = "100" if rate >= 1 else f"{math.floor(max(0.0, rate) * 1000) / 10:g}"
    stalls = int(c.get("stalls") or 0)
    took = f" ({float(c.get('stall_s') or 0):.1f} s)" if stalls else ""
    days = c.get("days") or 7
    return (f"on time: {share}% of {count(c.get('chunks'))} chunks · {stalls} stall{'s' if stalls != 1 else ''}{took} "
            f"over {days} days ({count(c.get('runs'))} run{'s' if c.get('runs') != 1 else ''})")



_STAGE_SAID = {"gateway": "connect", "auth": "auth", "place": "placement", "queue": "in line",
               "cold_start": "cold start", "tcp": "TCP", "tls": "TLS", "stream": "stream", "first_act": "first act"}


def _ms_said(ms: float) -> str:
    """A connect's time as the connects line says it: 812 ms, 1.9 s, 3m 16s."""
    if ms < 1000:
        return f"{ms:.0f} ms"
    if ms < 60_000:
        return f"{ms / 1000:.1f} s"
    return f"{int(ms // 60_000)}m {int(ms % 60_000 // 1000):02d}s"


def connects_line(c: Any) -> str | None:
    """Its robots' connects over the platform's window (the fleet's `connects`, their SDKs' reports): how many, the p50
    and p95 of the ones that served - to their first act answered - and the others by the stage they stopped in, most
    first. None before any connect was reported.
"""
    if not isinstance(c, dict) or not isinstance(c.get("connects"), int) or c["connects"] <= 0:
        return None
    line = f"connects: {count(c['connects'])} in the last {c.get('window_h') or 24} h"
    if isinstance(c.get("p50_ms"), (int, float)) and isinstance(c.get("p95_ms"), (int, float)):
        line += f" · p50 {_ms_said(float(c['p50_ms']))} · p95 {_ms_said(float(c['p95_ms']))}"
    by = c.get("failed_by_stage") if isinstance(c.get("failed_by_stage"), dict) else {}
    failed = int(c.get("failed") or 0)
    if not failed:
        return line + " · none failed"
    where = ", ".join(f"{_STAGE_SAID.get(stage, stage)} {n}" for stage, n in by.items() if isinstance(n, int))
    return line + f" · {failed} failed" + (f": {where}" if where else "")


def episodes_lost_line(lost: Any, name: str) -> str | None:
    """The episodes the platform ended in its window (the last 24 h): how many, and why, most first - None when it ended
    none, or when the platform could not read its workers' lines (null).
"""
    if not isinstance(lost, dict) or not isinstance(lost.get("total"), int) or lost["total"] <= 0:
        return None
    by = lost.get("by_cause") if isinstance(lost.get("by_cause"), dict) else {}
    parts = sorted(((n, c) for c, n in by.items() if isinstance(n, int) and n > 0), key=lambda nc: (-nc[0], nc[1]))
    hours = int(lost["window_s"]) // 3600 if isinstance(lost.get("window_s"), (int, float)) else 24
    why_ = ", ".join(f"{n} {EPISODE_LOST.get(c, c)}" for n, c in parts)
    return (f"episodes the platform ended in the last {hours} h: {lost['total']}" + (f" - {why_}" if why_ else "")
            + f" (`seq policy logs {name}` names each)")


def now_line(f: dict) -> str | None:
    """The card the deployment's live workers run on now and what one worker costs an hour on it, from the fleet's own
    workers and GPU list (gpus.cards, priced as billed). None without a live worker. A deployment runs on its one card
    , so this names one."""
    cards = (f.get("gpus") or {}).get("cards") or []
    if not cards:
        return None
    kind = lambda c: str(c).split(":")[0]
    live: dict[str, int] = {}
    for w in f.get("workers") or []:
        if w.get("state") not in ("stopped", "failed") and w.get("gpu"):
            live[kind(w["gpu"])] = live.get(kind(w["gpu"]), 0) + 1
    if not live:
        return None
    row = {kind(c.get("card")): c for c in cards}
    parts = []
    for gpu, n in live.items():
        c = row.get(gpu) or {"card": gpu}
        price = f" at {_usd(c['usd_per_hour'], per_hour)} a worker" if c.get("usd_per_hour") is not None else ""
        parts.append(f"{n} worker{'s' if n != 1 else ''} on {c['card']}{price}")
    return "now: " + ", ".join(parts)


def show_session_params(f: dict, echo: Echo) -> None:
    """The inference parameters each connected robot runs with — its own over the deployment's defaults — and the
    defaults themselves (`seq policy set <name> params.<name>=`), and who drives each robot now: its model, a person
    by the name their console gave, or nobody, stopped (driver_words). Nothing for a policy that declares none. Under
    each robot, why it sits on its worker, as the platform says it (`seated`).
    
"""
    defaults, sessions = f.get("params"), f.get("sessions")
    if defaults:
        echo("inference parameters (deployment defaults): " + _kv(defaults))
    for s in sessions or []:
        given = s.get("params")
        driver = driver_words(s.get("driver"))
        region = f" ({s['region']})" if isinstance(s.get("region"), str) and s["region"] else ""
        echo(f"  robot {s.get('session')} on {str(s.get('worker') or '')[:12]}{region}: "
             + (_kv(given) if given else "the policy's defaults" if given == {} else "parameters not recorded")
             + (f" · {driver}" if driver else ""))
        if isinstance(s.get("seated"), str) and s["seated"]:
            echo(f"    ↳ {s['seated']}")


def driver_words(driver: dict | None) -> str | None:
    """Who drives a robot, as `seq policy status` says it: "driven by its model", "driven by <operator>" (a person,
    by the name their console gave; "a person" for none), "stopped"; None when it says none."""
    if not isinstance(driver, dict) or driver.get("by") not in ("model", "human", "stopped"):
        return None
    if driver["by"] == "human":
        return f"driven by {driver.get('operator') or 'a person'}"
    return "stopped" if driver["by"] == "stopped" else "driven by its model"


def _kv(d: dict) -> str:
    return ", ".join(f"{k}={v}" for k, v in sorted(d.items()))


def _show_group(group: dict, echo: Echo) -> None:
    """A model across several machines: each machine's rank, its state and its last heartbeat as rank 0 saw them, or
    why the group ended."""
    if group.get("failure"):
        echo(f"    ↳ the group of {count(group.get('size'))} machines ended: {group['failure']}")
        return
    parts = []
    for m in group.get("members") or []:
        beat = m.get("beat_age_s")
        parts.append(f"rank {count(m.get('rank'))} {m.get('state') or '?'}"
                     + (f" (beat {float(beat):.0f} s ago)" if isinstance(beat, (int, float)) else ""))
    if parts:
        echo(f"    machines: {' · '.join(parts)}")



def worker_price(resources: Any, prices: dict) -> Optional[dict]:
    """One worker's price per hour in three parts — its card(s), its CPU and its memory — at the requests it declared
    (the minimum when undeclared), from the platform's price list. None when its card is not on the list.
    """
    first = (resources.gpu or ["cpu"])[0]
    card, _, n = str(first).partition(":")
    cards = int(n) if n.strip().isdigit() else 1
    rows = {str(g.get("gpu")).lower(): g for g in prices.get("gpus") or []}
    gpu_h = 0.0
    if card.lower() != "cpu":
        row = rows.get(card.lower())
        if row is None:
            return None
        gpu_h = float(row.get("usd_per_hour") or 0) * cards
    cores = max(float(resources.cpu or 0), MIN_CPU_CORES)
    gib = max(float(resources.memory_gb or 0), MIN_MEMORY_GIB)
    cpu_h = cores * float((prices.get("cpu") or {}).get("usd_per_core_hour") or 0)
    memory_h = gib * float((prices.get("memory") or {}).get("usd_per_gib_hour") or 0)
    return {"card": card, "cards": cards, "gpu_usd_per_hour": gpu_h, "cpu_cores": cores, "cpu_limit": resources.cpu_limit, "cpu_usd_per_hour": cpu_h,
            "memory_gib": gib, "memory_limit_gib": resources.memory_limit_gb, "memory_usd_per_hour": memory_h,
            "cpu_declared": resources.cpu is not None, "memory_declared": resources.memory_gb is not None}


def show_price(p: dict, echo: Echo) -> None:
    """The three-part hourly price `seq deploy` prints once the deployment is ready."""

    def size(v: float, declared: bool, limit: Any, unit: str) -> str:
        what = f"{v:g} {unit}" + (f" (up to {float(limit):g})" if limit else "")
        return what if declared else f"{what} — the minimum; the worker may use more"

    echo("price: one worker, per hour")
    if p["card"].lower() != "cpu":
        echo(f"  GPU     {p['card']} × {p['cards']}  {_usd(p['gpu_usd_per_hour'], per_hour)}")
    echo(f"  CPU     {size(p['cpu_cores'], p['cpu_declared'], p['cpu_limit'], 'cores')}  "
         f"{_usd(p['cpu_usd_per_hour'], per_hour)}")
    echo(f"  memory  {size(p['memory_gib'], p['memory_declared'], p['memory_limit_gib'], 'GiB')}  "
         f"{_usd(p['memory_usd_per_hour'], per_hour)}")
    full = p["gpu_usd_per_hour"] + p["cpu_usd_per_hour"] + p["memory_usd_per_hour"]
    echo(f"  total   {_usd(full, per_hour)}")
    echo("  CPU and memory are billed on the greater of the request and actual use.")


def show_measured(measured: dict | None, echo: Echo) -> None:
    """What the build check's replicas measured as they started — for reference only: the platform sizes nothing from
    it, and a real load may differ. Nothing when the build reported none."""
    if not measured:
        return


    vram = measured.get("per_replica_vram_need_mb") or measured.get("per_replica_vram_mb")
    parts = [f"{v / 1024:.1f} GiB {what}" for v, what in ((vram, "of GPU memory"),
                                                          (measured.get("per_replica_ram_mb"), "of memory")) if v]
    if not parts:
        return
    n = int(measured.get("replicas") or 1)
    slowest = f", the slowest started in {float(measured['load_s']):g} s" if measured.get("load_s") else ""

    acts = "; its acts were not measured - the build check acts only on a sample episode (@seq.sample)" \
        if acts_unmeasured(measured) else ""
    echo(f"measured at the build check (for reference): one copy took {' and '.join(parts)}"
         + (f"; {n} copies started" if n > 1 else "") + slowest + acts)


def show_gpu(g: dict | None, start_wait_s: Any, echo: Echo) -> None:
    """The one card the deployment runs on: whose choice it is (its template's own, or its owner's beside the
    template's), one worker's price per hour on it as billed and how many of its workers are on it now; how long a start
    waits for it to come free (`start_wait_s`); and the most GPUs it holds at once, the smaller of its cap and the
    account's. Nothing for one on CPU. A deployment runs on one card and never switches
.
    """
    if not g or not g.get("cards"):
        return
    c = g["cards"][0]
    card = str(c["card"])
    if g.get("source") == "template":
        whose = f"{g['template']}'s own"
    elif g.get("template"):
        whose = f"your own; {g['template']} uses {', '.join(g.get('template_cards') or [])}"
    else:
        whose = "your policy's own"
    price = f"{_usd(c['usd_per_hour'], per_hour)} a worker" if c.get("usd_per_hour") is not None else "not priced"
    n = int(c.get("workers") or 0)
    now = f"   ← {n} worker{'s' if n != 1 else ''} on it now" if n else ""
    echo(f"GPU: {card} ({whose})   {price}{now}")
    if g.get("region"):


        echo(f"  region {g['region']}: every worker runs there, and a start waits there for an available {card.split(':')[0]}")
    if isinstance(start_wait_s, (int, float)) and start_wait_s > 0:

        echo(f"  a start waits up to {every_words(float(start_wait_s))} for an available {card.split(':')[0]}")
    caps = [x for x in (g.get("max_gpus"), g.get("account_gpus")) if x]
    if caps:

        mine = f"this policy's max GPUs {g['max_gpus']}" if g.get("max_gpus") else "no max GPUs of its own"
        acct = f", your account's GPU limit {g['account_gpus']}" if g.get("account_gpus") else ""
        echo(f"  at most {min(caps)} GPU{'s' if min(caps) != 1 else ''} at once ({mine}{acct})")


def show_billed_price(p: dict | None, echo: Echo) -> None:
    """One worker's price per hour as the platform computed it from the build check's measurements: the card, CPU and
    memory each with what was requested and what serving one robot used - or what its serving workers use now, where
    that is more - the total at the requests and as billed (the greater of request and use), and the cpu= / memory=
    that would make the two agree.
    """
    if not p:
        return
    req, used = p.get("requested") or {}, p.get("used") or {}


    echo("price: one worker, per hour" + (" (CPU and memory at the serving rates)"
                                          if p.get("tier") == "serving" else ""))
    if p.get("gpu_usd_per_hour"):
        echo(f"  GPU     {p.get('card')}  {_usd(p['gpu_usd_per_hour'], per_hour)}")




    whose = p["used_from"]
    now = "used by its workers now"
    cpu = f"{float(req.get('cpu') or 0):g} cores requested" + (
        f", {float(used['cpu']):g} {now if whose.get('cpu') == 'workers' else 'used serving one robot'}"
        if used.get("cpu") is not None else "")
    mem = f"{float(req.get('memory_gib') or 0):g} GiB requested" + (
        f", {float(used['memory_gib']):g} GiB {now if whose.get('memory') == 'workers' else 'used'}"
        if used.get("memory_gib") is not None else "")
    echo(f"  CPU     {cpu}  {_usd(p.get('cpu_usd_per_hour') or 0, per_hour)}")
    echo(f"  memory  {mem}  {_usd(p.get('memory_usd_per_hour') or 0, per_hour)}")
    at_request, billed = float(p.get("request_usd_per_hour") or 0), float(p.get("usd_per_hour") or 0)
    if abs(billed - at_request) < 0.0001:
        echo(f"  total   {_usd(billed, per_hour)}")
    else:
        echo(f"  total   {_usd(at_request, per_hour)} at the requests; {_usd(billed, per_hour)} as billed — CPU and "
             "memory are billed "
             "on the greater of the request and actual use")
    suggest = p.get("suggest") or {}
    if suggest:
        what = ", ".join(f"{k}={v:g}" for k, v in sorted(suggest.items()))
        echo(f"  declare @seq.policy({what}) and the price at the requests is what is billed")


def acts_unmeasured(measured: dict | None) -> bool:
    """Whether the build check never called infer, so what it measured of a copy is its load alone: the check acts on a
    sample episode only (@seq.sample, measured.sample) and a planner's answers no act (measured.planner), so a version
    measured with neither. The worker's measured said io_mode and its probe until worker 5's 64ad99b0 took them out,
    and this read io_mode "raw", never there since."""
    m = measured if isinstance(measured, dict) else {}
    return bool(m) and not (m.get("sample") or m.get("planner"))


def show_capacity(cap: dict | None, echo: Echo, measured: dict | None = None) -> None:
    """One copy's need of a card and whether it fits on the card it was measured on: a worker runs one copy on each
    card.
    When the build check never called infer (acts_unmeasured, of the version's `measured` beside it), what it measured
    is the load's alone, and the line says so and how its acts would be measured: "one copy needs 16.7 GiB" read as all
    a card must hold.
    A worker runs one copy a card.
 """
    if not cap or not cap.get("per_copy_vram_mb"):
        return
    whose = ("its framework's own peak" if cap["measured_by"] != "driver"
             else "the driver's figure, which for a framework that preallocates is its whole pool")
    gib = f"{cap['per_copy_vram_mb'] / 1024:.1f} GiB of GPU memory ({whose})"
    loaded = acts_unmeasured(measured)
    line = (f"loading one copy took {gib}; its acts were not measured and may need more - the build check acts only on "
            "a sample episode (@seq.sample)" if loaded else f"one copy needs {gib}")
    on, n = cap.get("measured_on"), cap.get("fits")
    if on and n is not None:
        size = f" ({cap['card_vram_mb'] / 1024:.1f} GiB)" if cap.get("card_vram_mb") else ""
        fit = "fits" if n >= 1 else "does not fit"
        line += f". Loaded, it {fit} on one {on}{size}" if loaded else f". It {fit} on one {on}{size}"

    echo(line[0].upper() + line[1:] + ("" if line.endswith(".") else "."))


def show_cuda_graphs(measured: dict | None, echo: Echo) -> None:
    """What its version's check found of CUDA graphs
: on, and how much faster its acts are; or off, and why.
    Nothing for a version that asked for none.
"""
    graphs = (measured or {}).get("cuda_graphs")
    if not isinstance(graphs, dict):
        return
    if not graphs.get("on"):
        echo(f"CUDA graphs: off - {graphs.get('why') or 'its check left them off'}")
        return
    faster = graphs.get("speedup")
    echo("CUDA graphs: on" + (f" (acts {float(faster):.2f}× faster)" if isinstance(faster, (int, float)) else ""))


def show_batching(measured: dict | None, echo: Echo) -> None:
    """How a deployment that declares `@seq.concurrent` batches: a copy seats as many robots as the largest batch size
    it lists whose batch answers within the time its robots can wait for an answer (@seq.policy(hz=,
    action_chunk_valid_len=, action_chunk_replan_at=): the steps between the two, at hz; asking at the last valid step,
    or declaring no valid length, one robot a copy), as long as their batches fill at most LOAD_MAX of the time between
    a robot's asks - and an eval's copy runs its acts in batches of those sizes. Nothing for a policy that declares no
    @seq.concurrent. The worker reports the declaration as `measured.concurrent` ({sizes}).
"""
    batch = (measured or {}).get("concurrent") or {}
    listed = [int(n) for n in batch["sizes"]] if isinstance(batch.get("sizes"), list) and batch["sizes"] else None
    if not listed:
        return
    sizes = ", ".join(map(str, listed[:-1])) + f" and {listed[-1]}" if len(listed) > 1 else str(listed[0])
    echo(f"batching: a copy seats as many robots as the largest of its batches of {sizes} that answers within the time "
         "its robots can wait for an answer (the steps from action_chunk_replan_at to action_chunk_valid_len, at hz), "
         f"as long as their batches fill at most {LOAD_MAX:.0%} of the time between a robot's asks "
         "(action_chunk_replan_at steps at hz) - one robot a copy when it asks at its last valid step or declares no "
         "action_chunk_valid_len; where it sets max_wait_for_batch, within that wait in place of those steps; an "
         "eval's copy runs its acts in batches of those sizes")


def show_sample(measured: dict | None, echo: Echo) -> None:
    """
    What the build check played on the policy, as its worker reported it: the sample episode it marks (@seq.sample,
    `measured.sample`: its calls, its acts' times and its GPU memory - sample_said). A policy that names none is never
    acted on - which the platform's hint says, with how to name one (show_hints, at "build").

    """
    played = (measured or {}).get("sample")
    if isinstance(played, dict) and played.get("acts"):
        echo(f"build check: {sample_said(played)}")


def sample_said(played: dict) -> str:
    """The sample episode the build check played whole
, as the build's act step says it (harness/control_progress.py sample_said): its calls - observes and
    acts - each act's time, the first and the median of the rest, and the GPU memory it held at most: the framework's
    own peak, else what the card showed in use.
"""
    calls, acts = int(played.get("calls") or played["acts"]), int(played["acts"])
    which = (f"the {calls} calls of its sample episode (@seq.sample) - {_counted(calls - acts, 'observe')} and "
             f"{_counted(acts, 'act')} - were" if calls > acts
             else f"the {_counted(acts, 'act')} of its sample episode (@seq.sample) {'were' if acts > 1 else 'was'}")

    first = f"{float(played.get('first_ms') or 0):.0f} ms"
    times = (f"the first act in {first}, then {float(played.get('p50_ms') or 0):.0f} ms an act" if acts > 1
             else f"the act in {first}")
    line = f"{which} answered, {times}"
    peak, held_mb = (played.get("framework") or {}).get("peak_mb"), played.get("vram_peak_mb")
    if isinstance(peak, (int, float)) and peak > 0:
        line += f"; peak GPU memory {peak / 1024:.1f} GiB"
    elif isinstance(held_mb, (int, float)) and held_mb > 0:
        line += f"; {held_mb / 1024:.1f} GiB of GPU memory in use at most"
    return line


def _counted(n: int, word: str) -> str:
    """"1 act", "3 acts"."""
    return f"{n} {word}{'' if n == 1 else 's'}"





_NEAR_A_DAY_S = 20 * 3600.0


def _daily(seconds: float) -> str:
    """" (about once a day)" for an interval near a day, else nothing."""
    return " (about once a day)" if seconds >= _NEAR_A_DAY_S else ""


def _one_worker_usd(c: dict) -> float | None:
    """One worker's price per hour: the ceiling's, every worker busy, over its workers - what the one started beside a
    worker being replaced is billed. None when the ceiling says no price or no worker."""
    usd, workers = c.get("usd_per_hour"), c.get("workers")
    if not isinstance(usd, (int, float)) or not isinstance(workers, int) or isinstance(workers, bool) or workers < 1:
        return None
    return float(usd) / workers


def _next_replacement(turn: dict) -> str:
    """When the deployment's next worker is replaced and the latest its robots move by, as the platform says them (its
    oldest worker's), on this machine's clock: " - next from 10-18 01:27 EDT, its robots to move by 02:12 EDT at the
    latest"; "" while no worker serves. It said "(within 335 min)" - a count of minutes from a time it did
    not give."""
    if not turn.get("next_at"):
        return ""
    by = f", its robots to move by {_clock(turn['next_by'])} at the latest" if turn.get("next_by") else ""
    return f" - next from {_clock(turn['next_at'])}{by}"


def show_ceiling(name: str, c: dict | None, echo: Echo, *, capped: bool = True) -> None:
    """The deployment's own max GPUs at work: the most workers it allows and what they cost per hour all busy, the
    account's GPU limit beside it, how to change it, and the last time the deployment reached half of it or found it
    full — or, for one deployed before max GPUs was required, that it has none."""
    if not capped:
        echo(f"warning: {name} has no max GPUs of its own — its next deploy must set it (max_gpus=N); "
             f"set it now with `seq policy set {name} max_gpus=N`")
        return
    if not c:
        return
    account = f" (your account's GPU limit: {c['account_gpus']})" if c.get("account_gpus") else ""
    on = f" on {c['card']}" if c.get("card") else ""
    cost = (f"; with all of them busy ({c['workers']} worker{'s' if c.get('workers') != 1 else ''}{on}) about "
            f"{_usd(c['usd_per_hour'], per_hour)}") if c.get("usd_per_hour") is not None else ""
    echo(f"max GPUs: {c['max_gpus']}{account}{cost} — change it any time: "
         f"seq policy set {name} max_gpus=N")
    turn = c.get("rotation") or {}
    used, cap = c.get("account_in_use"), c.get("account_gpus")
    full = used is not None and cap and int(used) >= int(cap)



    if turn.get("replace_every_s"):





        price = _one_worker_usd(c)
        cost = f", about {_usd(price, per_hour)} while it runs" if price is not None else ""
        every = float(turn["replace_every_s"])
        echo(f"  a worker is replaced every {every_words(every)}{_daily(every)}: one more "
             f"starts beside it - past max_gpus, billed as any worker{cost}, for up to "
             f"{round(float(turn.get('wait_s') or 0) / 60)} min - and its robots move to it at an episode "
             f"boundary{_next_replacement(turn)}")
        if turn.get("past_cap_now"):

            n = int(turn["past_cap_now"])
            echo(f"  now: {n} worker{'s' if n != 1 else ''} past max_gpus while a worker is replaced - billed as any "
                 "worker, until its robots have moved")
        if full:
            echo(f"  your account's GPUs are all in use ({int(used)} of {int(cap)}): a worker being replaced cannot start "
                 "its replacement beside it, so its robots move at its forced end")
    last = c.get("last_event") or {}
    if last.get("event") in ("gpu_ceiling_near", "gpu_ceiling_reached"):
        what = ("reached half of it" if last["event"] == "gpu_ceiling_near"
                else "was full and a robot waited or was refused")
        echo(f"  last {_clock(last.get('at'))}: {what} ({last.get('reason')})")


def print_worker_price(resources: Any, base_url: str | None, name: str | None = None,
                       version: int | None = None) -> None:
    """After a deploy: the hourly price split, and what the build check measured — the platform's own figures (the
    same `seq policy status` and the console show) when it has them, else the price list's at the requests. A line of
    output is never worth failing a deploy over, so whatever cannot be read prints nothing.
    `version`: the version the deploy made. The platform's figures are printed only when they are that version's
    (`priced_version`): one still on its way in beside the serving version has its own
    requests and its own build's measurements, never the serving one's.
    Before: the serving version's figures were printed for the version just made.


    """
    f: dict = {}
    if name:
        try:
            f = fleet(name, base_url=base_url, version=version, deploying=True)
        except Exception:
            f = {}

    mine = version is None or f.get("priced_version") == version
    if f.get("price") and mine:
        show_billed_price(f["price"], print)
        show_capacity(f.get("capacity"), print, f.get("measured"))

        show_batching(f.get("measured"), print)


        show_sample(f.get("measured"), print)
        show_hints(f.get("hints"), "build", print)
        show_ceiling(name, f.get("ceiling"), print, capped=bool(f.get("max_gpus")) or not holds_gpus(f))
        return
    try:
        price = worker_price(resources, _call("GET", "/v1/pricing", base_url))
    except Exception:
        price = None
    if price is not None:
        show_price(price, print)
    if name and mine:
        show_measured(f.get("measured"), print)
        show_sample(f.get("measured"), print)
        show_hints(f.get("hints"), "build", print)
