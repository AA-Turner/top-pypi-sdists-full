"""
`seq eval ls` and a policy's price before it is built - reading a deployment's evals over time, and knowing what it will
cost before it runs.

In one sentence: `seq deploy --dry-run` prices a policy's card from the platform's public price list before anything is
built (it was `seq policy estimate`, folded into the dry run); `seq eval ls <name>` prints its evals over time - a trend
of their success rate. A deployment's budget, alerts, warm hours and scaling are its settings now
(seq/settings_cli.py: `seq policy set`).
"""
from __future__ import annotations

from typing import Any

from seq import columns
from sequence_base.constants.serving import QUEUE_TIMEOUT_S

from seq.deployments_cli import _call, page_query
from seq.registry import MACHINE_CARDS
from sequence_ai._core.capacity import duration
from sequence_ai._core.money import money, per_hour as hourly
from sequence_ai._core.names import segment



def serving_view(name: str | None, *, base_url: str | None = None) -> dict | None:
    """The deployment `name`'s fleet as the platform answers it (GET /v1/deployments/{name}/fleet): what its serving
    version's check measured, its capacity and its price - None when it has not been deployed. One read serves a dry run's price: the capacity (measured) and the robots a worker of a version that batches
    seats (estimate)."""
    from sequence_ai.errors import NotFound

    if not name:
        return None
    try:
        return _call("GET", f"/v1/deployments/{segment(name)}/fleet", base_url)
    except NotFound:
        return None


_READ = object()


def measured(name: str | None, card: str | None = None, *, base_url: str | None = None, echo=print,
             view: Any = _READ) -> dict | None:
    """What the deployment `name` measured at its build check, as the platform sizes it: one copy's need of a card, and
    for each card (`card` alone when given) whether the copy fits and one worker's price per hour at the CPU and memory
    it used — the measured card's from its own driver, the others estimated from their size. None when it has not been
    deployed (or measured) yet. `view`: its fleet, already read (serving_view).
 A worker runs one copy a card: a card is
    said to fit or not, never a count of copies."""
    from seq.capacity_cli import show_capacity

    if not name:
        return None
    if view is _READ:
        view = serving_view(name, base_url=base_url)
    cap = (view or {}).get("capacity")
    if not cap:
        echo(f"(nothing measured yet: deploy {name} once and its build check measures what one copy needs and uses)")
        return None
    show_capacity(cap, echo, (view or {}).get("measured"))
    rows = cap.get("by_card") or {}
    if card:
        key = next((c for c in rows if c.lower() == str(card).split(":")[0].lower()), None)
        if key is None:
            raise ValueError(f"{card} is not an offered card ({', '.join(sorted(rows))})")
        rows = {key: rows[key]}

    cells = [[c, "fits" if int(row.get("copies") or 0) >= 1 else "does not fit",
              (f"{hourly(row['usd_per_hour'])} a worker" if row.get("usd_per_hour") is not None else "")
              + ("  (estimate from the card's size)" if row.get("estimate") else "")]
             for c, row in sorted(rows.items(), key=lambda kv: kv[1].get("usd_per_hour") or 0)]
    widths = columns.widths(cells)
    for row in cells:
        echo("  " + columns.line(row, widths).rstrip())
    return cap


def _kept_gb(name: str, base_url: str | None) -> dict[str, float]:
    """{"weights": GB} of what the platform keeps for the deployment `name` - its `deploy:<name>` volume, as the console's
    Storage page lists it - or {} when it keeps none (not deployed yet).
    Weights of no size are 0.0: a deployment of an official template's weights, its code changed or not, keeps no copy
    of its own (it reads the platform's read-only copy), and nothing of them is billed."""
    sizes: dict[str, float] = {}
    cursor = None
    for _ in range(20):
        page = _call("GET", "/v1/volumes?limit=200" + (f"&cursor={cursor}" if cursor else ""), base_url)
        for v in page.get("data") or []:
            if v.get("name") == f"deploy:{name}":
                sizes["weights"] = int(v.get("size_bytes") or 0) / 1e9
        cursor = page.get("next_cursor")
        if not cursor:
            break
    return sizes


def _size(gb: float) -> str:
    """A size as it is read: "12.4 GB", or "5.0 MB" under a tenth of a GB - one decimal there, as `seq volume ls` reads
    a size."""
    return f"{gb * 1000:,.1f} MB" if gb < 0.1 else f"{gb:,.1f} GB"







def weights_kept(uri: str | None, *, others: tuple | list = (), gpu: str | None = None,
                 shared: list | None = None) -> tuple[str, str | None]:
    """How the platform keeps a policy's weights, which decides what they cost in storage - by the build's own rules:
    ("none", None) it declares no checkpoint; ("volume", name) an uploaded volume (vol://<name>), read as it is and
    billed as that volume; ("shared", None) official templates' weights the platform shares (`shared`, GET /v1/pricing
    storage.shared_weights_templates) - its first part's and each of its `others` (the other parts' origins, weights in
    named parts) - on one machine, read from the platform's read-only copies, nothing copied, nothing billed, while the
    policy's code is that template's, unchanged, which the platform alone can tell (changed, they are copied and billed);
    ("unknown", None) an official template's where the platform could not say which it shares; ("copied", None) any other
    - an hf:// repo, a template it does not share, a part of its own beside a template's, a policy on several machines -
    copied for the deployment and billed by the GB-month.
    WHY: the estimate billed every policy's weights as a copy, an official template's too, which its build never copies.
    



"""
    if not uri:
        return "none", None
    if uri.startswith("vol://"):

        return "volume", uri[len("vol://"):].split("@", 1)[0]
    parts = [uri, *others]
    if not all(str(part).startswith("template://") for part in parts):
        return "copied", None
    if shared is None:
        return "unknown", None
    from sequence_base.contract.templates import parse_template

    card = gpu or ""
    cards = int(card.split(":", 1)[1]) if ":" in card and card.split(":", 1)[1].isdigit() else 1
    one_machine = cards <= MACHINE_CARDS
    every = all(parse_template(str(part))[0] in shared for part in parts)
    return ("shared" if every and one_machine else "copied"), None


def storage(name: str | None, prices: dict, *, base_url: str | None = None, echo=print,
            has_weights: bool = True, weights: str | None = None, weights_others: tuple | list = (),
            gpu: str | None = None) -> dict | None:
    """What keeping the deployment costs a month in storage, beside its worker time: its weights copy at the platform's
    price per GB-month (GET /v1/pricing storage), billed daily whether or not a worker runs - their
    sizes once it has been deployed, else the price and what 10 GB comes to, for weights it copies



.
    `weights` is the
    policy's weights origin (its URI; None with has_weights: an origin not said, read as copied). None when the
    platform cannot read its storage price.
"""
    storage_list = (prices or {}).get("storage") or {}
    rate = storage_list.get("usd_per_gb_month")
    if rate is None:
        echo("  plus storage while the deployment is kept, billed by the GB-month")
        return None
    rate = float(rate)
    if weights is not None:
        origin, volume = weights_kept(weights, others=weights_others, gpu=gpu,
                                      shared=storage_list.get("shared_weights_templates"))
    else:
        origin, volume = ("copied" if has_weights else "none"), None
    try:
        sizes = _kept_gb(name, base_url) if name else {}
    except Exception:
        sizes = {}
    if not sizes:

        if origin == "none":

            echo("  no storage for its weights: it declares none")
        elif origin == "shared":
            echo("  no storage for its weights while its code is the official template's, unchanged: read from the "
                 f"platform's read-only copy (nothing copied); with its code changed, a copy at {money(rate)}/GB-month")
        elif origin == "volume":
            echo(f"  no storage of its own for its weights: it reads your volume {volume} as it is (nothing copied), "
                 f"billed as that volume at {money(rate)}/GB-month for as long as you keep it")
        elif origin == "unknown":
            echo(f"  plus storage while it is kept: an official template's weights are read from the platform's copy, "
                 f"not billed, when it shares them and its code is unchanged; else copied at {money(rate)}/GB-month "
                 f"(10 GB: ~{money(10 * rate)}/month)")
        else:
            echo(f"  plus storage while it is kept: its weights copy at {money(rate)}/GB-month, whether or not a "
                 f"worker runs (10 GB: ~{money(10 * rate)}/month); its size is known once it is deployed - deleting it "
                 "stops it")
        return {"usd_per_gb_month": rate, **({"usd_per_month": 0.0} if origin in ("none", "shared", "volume") else {})}
    gb = sizes["weights"]
    month = gb * rate
    if gb > 0:
        echo(f"  plus storage while it is kept: its weights {_size(gb)} at {money(rate)}/GB-month: ~{money(month)}/month, "
             "whether or not a worker runs - deleting it stops it")
    else:

        echo("  plus storage while it is kept: its weights are not billed (an official template's: it reads the "
             "platform's copy, its code changed or not)")
    return {"usd_per_gb_month": rate, "weights_gb": round(gb, 3), "usd_per_month": round(month, 2)}


def compute_per_hour(prices: dict, gpu: str, cpu_cores: float | None = None,
                     memory_gib: float | None = None) -> tuple[float, str]:
    """What a worker's CPU and memory add to its hour, and the words that say how: its card's standard machine's cores
    and GiB, or the `cpu_cores` and `memory_gib` it declares where more (capacity_cli.billed_machine: the platform's
    list's policy_machines of `gpu`, "L4", "L4:4", "cpu"), wherever it runs, at the rates a deployment's workers pay -
    the serving ones when the list has them, else the base ones. Nothing added where the list prices no CPU or memory.
    Raises ValueError where it does and names no standard machine of `gpu`: never a size of the estimate's own
    guessing.
    WHY: a worker pays its card(s) and, apart, its cores and GiB, and one that declares no GPU pays no card at all - so
    an estimate at the card's price alone left the CPU and memory out, and a CPU policy's read the old per-hour figure
    the list sent for it, the default card's (L4's $0.96). {prod 10-16 GET /V1/PRICING: "COMPUTE_BILLED TRUE |
    CPU_USD_PER_HOUR 0.96", ('L4', 0.96), CPU {"USD_PER_CORE_HOUR": 0.1703, "SERVING_USD_PER_CORE_HOUR": 0.0568}}
    One price
    a card wherever it runs."""
    from seq.capacity_cli import billed_machine, serving_rates

    core_h, gib_h = serving_rates(prices)
    if not core_h and not gib_h:
        return 0.0, ""
    got = billed_machine(prices, gpu, cpu_cores, memory_gib)
    if got is None:
        raise ValueError(f"the platform's price list names no standard machine of {gpu}; try again shortly")
    cores, gib = got
    return (cores * core_h + gib * gib_h,
            f"{cores:g} cores x {money(core_h)}/core-h + {gib:g} GiB x {money(gib_h)}/GiB-h, its card's standard "
            "machine or what it declares where more")




QUEUE_WAIT_S = QUEUE_TIMEOUT_S






FIRST_SAVE_S = 120.0


def estimate(gpu: str | None, *, min_workers: int = 0, hours_per_day: float | None = None, cards: int = 1,
             base_url: str | None = None, echo=print, prices: dict | None = None,
             measured_per_hour: float | None = None, deployment: str | None = None,
             has_weights: bool = True, cpu_cores: float | None = None, memory_gib: float | None = None,
             idle_s: float | None = None, starts_per_day: int = 1, weights: str | None = None,
             weights_others: tuple | list = (), buffer_workers: int = 0, max_gpus: int | None = None,
             seats: int | None = None, seats_by: str | None = None, batches: bool = False,
             copies: int = 1, start_s: float | None = None, robots: int = 1, hz: float | None = None,
             chunk_steps: int | None = None, wait_s: float | None = None) -> dict:
    """What a deployment on `gpu` costs per day and per month: its warm floor around the clock, plus the hours robots
    use it (beyond the floor) - priced by the hour where `hours_per_day` is None, the use of it not known: `seq deploy
    --dry-run` takes no guess at it.
 From the platform's public prices; nothing is built. A worker's hour is its card(s) and
    its card's standard machine's CPU and memory, or the `cpu_cores` and `memory_gib` it declares where more
    (compute_per_hour), wherever it runs - a CPU worker's (`gpu` None or "cpu") is those alone. `measured_per_hour`,
    when given, is one worker's price as the platform has it for its deployment (its card and its CPU and memory) in
    place of the list's.
    `deployment`, when given, adds what keeping it costs in storage (storage(): `weights`, the policy's weights origin,
    and `weights_others`, its other parts' origins, say whether they are copied for it and so billed).
    `idle_s` (its idle timeout: its deployment's idle_timeout, else the platform's capacity.IDLE_S): a scale-to-zero
    worker's robots done, it runs that long before it ends, billed - once each of the `starts_per_day` times robots
    start using it, added to the day - and once a deploy, said apart, its check's machine staying on as its first
    worker, FIRST_SAVE_S with it. Before: the day was the hours in use alone, and every idle tail after them went
    unsaid.
    Priced for `robots` at once, as the platform runs them: a worker seats `seats` - what the check of version
    `seats_by` measured a worker of a policy that batches seating - else its `copies`, one robot a copy (`batches`: one
    that batches, before a check has measured it: its batches answer within the `chunk_steps` its robots play between
    asking for an answer and needing it, at `hz`, as the policy declares them) - so they take ceil(robots / seats) workers, and while robots use it its
    `buffer_workers` spares run beside them, billed, and none outside those hours (the platform keeps spares only while
    robots are connected, control/warm.py); never fewer than the warm floor, and `max_gpus` holds them to max_gpus //
    its cards - the robots past what that seats wait in line, up to QUEUE_WAIT_S, priced at the cap; after each use
    every worker that ran beside the warm floor runs its idle timeout. For one robot, what more robots take is said
    apart: every seats robots more add a worker at its price, up to what max_gpus allows.

    `start_s`, how long its new machines have taken to start, whole (its fleet's new_machine_s: boot, files, image and
    load): every worker that starts beside the warm floor is billed from its GPU (a CPU worker from when it starts), its
    start included - once each of the `starts_per_day` times, added to the day; None before one has started, said in
    words with no figure.
"""
    prices = prices or _call("GET", "/v1/pricing", base_url)
    card = gpu or "cpu"
    name, count = (card.split(":", 1) + ["1"])[:2] if ":" in card else (card, str(cards))
    rows = {g["gpu"].lower(): g for g in prices.get("gpus") or []}
    if name.lower() == "cpu":
        card_h, count = 0.0, 1
    elif name.lower() in rows:
        card_h = float(rows[name.lower()]["usd_per_hour"])
    else:
        raise ValueError(f"{name} is not an offered card ({', '.join(sorted(rows))})")
    compute_h, how = compute_per_hour(prices, name if name.lower() == "cpu" or int(count) == 1 else f"{name}:{count}",
                                      cpu_cores, memory_gib)
    per_hour = card_h * int(count) + compute_h
    if measured_per_hour is not None:
        per_hour = float(measured_per_hour)

    most = max(1, int(max_gpus) // int(count)) if max_gpus and name.lower() != "cpu" else None
    floor = max(0, int(min_workers)) if most is None else min(max(0, int(min_workers)), most)
    spare = max(0, int(buffer_workers or 0))
    k = int(seats) if seats else max(1, int(copies))
    n = max(1, int(robots))
    need = -(-n // k)
    wanted = max(floor, need + spare)
    in_use = wanted if most is None else min(wanted, most)
    beside = in_use - floor

    waiting = max(0, n - in_use * k) if most is not None and need > most else 0
    warm = floor * 24 * per_hour
    use = max(0.0, hours_per_day or 0.0) * beside * per_hour


    uses = max(0, int(starts_per_day)) if beside and hours_per_day is not None and hours_per_day > 0 else 0
    starts = uses if idle_s else 0
    idle = starts * beside * float(idle_s or 0) / 3600.0 * per_hour


    boot = uses * beside * float(start_s or 0) / 3600.0 * per_hour
    day = warm + use + idle + boot
    out = {"card": f"{name}" + (f" x{count}" if int(count) > 1 else ""), "usd_per_hour": round(per_hour, 4),
           "warm_usd_per_day": round(warm, 2), "use_usd_per_day": round(use, 2),
           **({"idle_usd_per_day": round(idle, 2)} if starts else {}),
           **({"start_usd_per_day": round(boot, 2)} if uses and start_s else {}), "usd_per_day": round(day, 2),
           "usd_per_month": round(day * 30, 2), "workers_in_use": in_use, "seats_per_worker": k, "robots": n,
           "robots_waiting": waiting}
    if measured_per_hour is not None:
        said = ", its card and its CPU and memory as the platform prices them now"
    elif how:
        said = f": {'its card, and ' if name.lower() != 'cpu' else ''}{how}"
    else:
        said = ": its card" if name.lower() != "cpu" else ""
    echo(f"estimate: {out['card']} at {hourly(per_hour)} a worker{said}")



    play = (f" within the {wait_s:g} s each robot waits for an answer (max_wait_for_batch)" if batches and wait_s else
            f" within the {chunk_steps / hz:.2g} s its robots can wait for an answer ({chunk_steps} steps at {hz:g} Hz)"
            if batches and hz and chunk_steps else "")
    whose = ((f", as {seats_by}'s check measured" if seats_by else ", as its check measured") if seats
             else f" until a deploy's check measures how many its batches seat{play}" if batches else "")
    more = ("every robot more adds a worker" if k == 1 else f"every {k} robots more add a worker") + \
        f" at {hourly(per_hour)}"
    if n == 1:

        held = (f", up to {most} worker{'s' if most != 1 else ''} (max_gpus={max_gpus}) - {most * k} "
                f"robot{'s' if most * k != 1 else ''} at once; any more wait in line, up to {QUEUE_WAIT_S // 60} min"
                if most is not None else "")
        echo(f"  a worker seats {k} robot{'s' if k != 1 else ''}{whose}: {more}{held}")
    else:
        echo(f"  {n} robots at once: {need} worker{'s' if need != 1 else ''} at {k} robot{'s' if k != 1 else ''} a "
             f"worker{whose}; {more}")
    if batches and seats:



        echo(f"  each robot waits up to {wait_s:g} s for an answer so that its act shares a batch (max_wait_for_batch)"
             if wait_s else "  max_wait_for_batch not set: each robot waits only while the answer it plays lasts")
    if waiting:
        echo(f"  max_gpus={max_gpus} holds it to {in_use} worker{'s' if in_use != 1 else ''} - {in_use * k} "
             f"robot{'s' if in_use * k != 1 else ''} at once: the other {waiting} wait in line, up to "
             f"{QUEUE_WAIT_S // 60} min, and the price is the cap's")
    elif in_use < wanted:
        busy = max(need, floor)
        echo(f"  max_gpus={max_gpus} holds it to {in_use} worker{'s' if in_use != 1 else ''} while robots use it: "
             f"{in_use - busy} spare{'s' if in_use - busy != 1 else ''} beside the busy "
             f"{'one' if busy == 1 else 'ones'}, not {spare}")
    if floor:
        echo(f"  min_workers={floor}: {money(warm)}/day kept warm around the clock (robot or not)")
        if beside:
            what = (f"{beside} spare{'s' if beside != 1 else ''}" if need <= floor
                    else f"{beside} worker{'s' if beside != 1 else ''} more for its robots and their spares")
            if hours_per_day is None:
                echo(f"  plus {what} beside the warm {'one' if floor == 1 else 'ones'} while robots are connected, at "
                     f"{hourly(per_hour)} a worker")
            else:
                echo(f"  plus ~{hours_per_day:g} h/day in use: {what} beside the warm "
                     f"{'one' if floor == 1 else 'ones'} while robots are connected -> {money(use)}/day")
    else:
        robots_on = min(need, in_use)
        spares_on = in_use - robots_on
        whom = ("its robot's" if n == 1 else
                f"{robots_on} for its {n - waiting} robot{'s' if n - waiting != 1 else ''} at once")
        if hours_per_day is None:
            workers = (f"{in_use} workers ({whom} and {spares_on} spare{'s' if spares_on != 1 else ''})" if spares_on
                       else f"{in_use} workers ({whom})" if in_use > 1 else "")
            echo(f"  scale to zero: billed only while robots use it, {hourly(per_hour)} a worker"
                 + (f" - {workers}" if workers else "") + "; nothing while none is connected")
        else:
            echo(f"  scale to zero: ~{hours_per_day:g} h/day in use"
                 + (f", {in_use} workers ({whom} and {spares_on} spare{'s' if spares_on != 1 else ''})" if spares_on else
                    f", {in_use} workers ({whom})" if in_use > 1 else "")
                 + f" -> {money(use)}/day")
    if starts:
        tail = (f"its worker runs {duration(idle_s)} after its robots are done, before it ends (its idle "
                "timeout), billed" if beside == 1 else
                f"its {beside} workers run {duration(idle_s)} after its robots are done, before they end "
                "(the idle timeout), billed")
        echo(f"  plus {money(idle)}/day idle: after each of {starts} start(s) a day {tail}")

    on_card = name.lower() != "cpu"
    billed = "billed from its GPU, its start included" if on_card else "billed from when it starts"

    took = (f"about {duration(start_s)}, as this policy's have taken" if start_s else
            "several minutes" if on_card else "a minute or more")
    if uses and start_s:
        who = "its worker is" if beside == 1 else f"each of its {beside} workers is"
        echo(f"  plus {money(boot)}/day starting: on each of {uses} start(s) a day {who} {billed} - {took}")
    elif uses:
        echo(f"  plus each start, not priced until one of its machines has started: {billed} - {took}")
    if hours_per_day is None:

        if beside and idle_s:
            echo(f"  and each time its robots disconnect, its worker runs {duration(idle_s)} more before it ends "
                 "(its idle timeout), billed: a robot connected holds its worker, billed, whether or not it acts")
        if beside:
            echo(f"  and each start is {billed} - {took}")
        if floor:
            echo(f"  ~{money(day)}/day, ~{money(day * 30)}/month kept warm, before the hours robots use it")
    else:
        echo(f"  ~{money(day)}/day, ~{money(day * 30)}/month in worker time")





    if idle_s:
        stays, minute = (float(idle_s) + FIRST_SAVE_S) / 3600.0 * per_hour, per_hour / 60.0
        out["first_worker_usd"], out["first_worker_usd_per_minute"] = round(stays, 2), round(minute, 4)
        echo(f"  each deploy, apart from these: its check's machine stays on as its first worker, billed - it saves "
             f"the version's image for its next machines, usually a minute or two, then with no robot connected ends "
             f"after {duration(idle_s)}: ~{money(stays)} with a usual save, ~{money(minute)} a minute")






    saves = prices.get("image_save") or {}
    if saves.get("usd_per_gb_min") is not None and saves.get("usd_per_gb_max") is not None:
        low, high = float(saves["usd_per_gb_min"]), float(saves["usd_per_gb_max"])
        out["image_save_usd_per_gb"] = [low, high]
        echo(f"  each deploy, its version's image is saved for its next machines: only what is not stored yet is sent, "
             f"often far less than the image, ${low:.2f}-${high:.2f} per GB sent (the cloud's own price where its check "
             "ran), billed")






    up = in_use if hours_per_day is not None and hours_per_day >= 23 else floor
    if up:
        extra = up * 0.75 * per_hour
        out["replace_usd_per_day"] = round(extra, 2)
        whom = (("each warm worker is" if floor > 1 else "its worker is") if up in (floor, 1)
                else f"each of its {up} workers is")
        echo(f"  plus up to {money(extra)}/day while {whom} "
             "replaced, "
             "about once a day: one more beside it for up to 45 min, billed")
    if deployment is not None:
        kept = storage(deployment, prices, base_url=base_url, echo=echo, has_weights=has_weights, weights=weights,
                       weights_others=weights_others, gpu=gpu)
        if kept:
            out["storage"] = kept
    return out


def evals(name: str, *, limit: int | None = None, cursor: str | None = None, base_url: str | None = None,
          echo=print) -> dict:
    """`seq eval ls <name> [--limit N] [--cursor C]`: one page of a deployed policy's evals over time, newest first,
    then where the page sits. Its eval schedules went with the feature (the user 10-17,
    "delete schedule as well")."""
    from seq.listing import _footer, _metric, _metric_head

    out = _call("GET", f"/v1/deployments/{segment(name)}/evals{page_query(limit, cursor)}", base_url)


    history = out["history"]
    if not history:
        if not out.get("total"):
            echo(f"no evals of {out['deployment']} yet: run one with `seq eval run {out['deployment']} --benchmark <name>`")
        return out


    benches = [(p.get("benchmark") or "") + (" (deleted)" if p.get("benchmark_deleted") else "") for p in history]
    width = max([len("BENCHMARK")] + [len(b) for b in benches])
    echo(f"{'EVAL':<8}  {'VER':<4}  {'BENCHMARK':<{width}}  {_metric_head(history)}")
    for p, bench in zip(history, benches):
        echo(f"{p['eval_id'][:8]}  {'v' + str(p.get('model_version') or '?'):<4}  {bench:<{width}}  "
             f"{_metric(p)}" + ("  (incomplete)" if p.get("incomplete") else ""))
    _footer(out, len(history), echo)
    return out

