"""
Why a request found no GPU, in one sentence each, and the short phrase a queued robot's notice uses.

In one sentence: a refused or queued connect (or eval) carries `details.reason` and its numbers -> `explain()` turns
them into the sentence a person reads (which limit binds, how many GPUs serving and evals hold, how many more this
needs, what to do) -> `errors.from_response` puts that sentence on the exception, and `seq` prints the same words.

WHY one sentence per reason rather than the status code: the three ways to be short of a GPU look alike from outside
(a 409 or a 503) and have opposite remedies. The account's own cap is fixed by stopping something of yours; the whole
platform being busy is not yours to fix, only to wait out; one card type out of stock is waited for - a deployment runs on
its one card and never switches - for as long as the platform's start wait lets it.
A caller handed "503" cannot tell which. No provider is named anywhere: the user picks cards, not where they come from.


Httpx-free and Python 3.9-clean like the rest of the client: it only formats numbers the server sent.
"""

from __future__ import annotations

import random
import sys
from typing import Any, Mapping, Optional




SHORTFALL = ("gpu_limit_reached", "gpu_busy", "gpu_low_stock", "deployment_full", "in_line", "queue_timeout")


def count(value: Any) -> str:
    """A GPU count as text, or "unknown" when the platform could not read it. Never a number that reads as "full": an
    account whose usage is unknown is not an account at its limit."""
    if value is None or isinstance(value, bool):
        return "unknown"
    try:
        return str(int(value))
    except (TypeError, ValueError):
        return "unknown"


def held(in_use: Optional[Mapping[str, Any]]) -> str:
    """What the account's GPUs are doing: 'serving 6, evals 2, build checks 1' (a count it could not read says
    'unknown'). A deploy's build check holds its card while it runs and the total counts it, so the parts name it too;
    an in_use without one (an eval's) leaves it out.
 
"""
    u = in_use if isinstance(in_use, Mapping) else {}
    words = f"serving {count(u.get('serving'))}, evals {count(u.get('eval'))}"
    return words + (f", build checks {count(u.get('build'))}" if "build" in u else "")


def _when(retry_after_s: Optional[float]) -> str:
    return f"in about {retry_after_s:.0f} s" if retry_after_s and retry_after_s > 0 else "in a minute"




IDLE_S = 600



LOAD_MAX = 0.9


def wait_steps(valid_len: Any, replan_at: Any) -> Optional[int]:
    """The steps a robot plays between asking for an answer and needing it, as its policy declares them:
    action_chunk_valid_len less action_chunk_replan_at, its last valid step when unset. Over hz, the time the next
    answer must arrive in, and so the time a batch of its copy's robots' acts answers within. None when it declares no
    action_chunk_valid_len; 0 when it asks at its last valid step, its robot waiting for every answer.
"""
    def whole(n: Any) -> bool:
        return isinstance(n, int) and not isinstance(n, bool) and n > 0

    if not whole(valid_len):
        return None
    return max(0, valid_len - (replan_at if whole(replan_at) else valid_len))


def wait_said(said: Any) -> str:
    """What follows a batching policy's seats of its max_wait_for_batch, as the gateway says it beside them (a deploy's
    summary, the fleet): each robot's wait where it is set, that it is not where it is not; "" for one that does not
    batch, which says nothing of it."""
    if not isinstance(said, dict) or "max_wait_for_batch" not in said:
        return ""
    wait = said["max_wait_for_batch"]
    return (f", each waiting up to {wait:g} s for an answer (max_wait_for_batch)" if wait
            else "; max_wait_for_batch not set")


def duration(seconds: float) -> str:
    """How long a robot waited, as the platform says it: 600 -> "10 min", 90 -> "90 s"."""
    s = int(round(float(seconds)))
    return f"{round(s / 60)} min" if s >= 120 else f"{s} s"


def explain(details: Optional[Mapping[str, Any]], *, retry_after_s: Optional[float] = None) -> Optional[str]:
    """The sentence for a shortfall `details` block, or None when its reason is not one of SHORTFALL.

    `retry_after_s` is the response's Retry-After, used where the sentence says when to try again."""
    d = details if isinstance(details, Mapping) else {}
    reason = d.get("reason")
    queued = d.get("queue_position") is not None
    in_line = f"you are queued at position {count(d.get('queue_position'))}"
    if reason == "gpu_limit_reached":
        limit, requested, short = d.get("limit"), d.get("requested"), d.get("short")
        try:
            never_fits = int(requested) > int(limit)
        except (TypeError, ValueError):
            never_fits = False
        if never_fits:
            return (f"This needs {count(requested)} GPUs at once and your account's limit is {count(limit)}; "
                    "lay it out on fewer cards.")
        need = f"this needs {count(requested)}" + (f", {count(short)} more than are free" if short else "")

        used = d.get("in_use") if isinstance(d.get("in_use"), Mapping) else {}
        wait_for = "an eval or a build check" if (used.get("build") or 0) > 0 else "an eval"
        then = (f"; {in_line} until enough free up." if queued
                else f"; stop a deployment or wait for {wait_for} to finish, then try again.")
        return f"Your account's {count(limit)} GPUs are in use ({held(d.get('in_use'))}) and {need}{then}"
    if reason == "gpu_busy":
        return ("Every GPU on the platform is busy right now (your account's limit is not the problem); "
                + (f"{in_line}." if queued else f"try again {_when(retry_after_s)}."))
    if reason == "in_line":


        return ("Every seat on this deployment's workers is taken; "
                + (f"{in_line}." if queued else f"try again {_when(retry_after_s)}."))
    if reason == "gpu_low_stock":




        gpu, waited = d.get("gpu") or "this card", d.get("waited_s")
        where = f" in {d['region']}" if isinstance(d.get("region"), str) and d["region"] else ""
        if queued:

            most = d.get("queue_timeout_s")
            up_to = f", for up to {duration(most)}" if isinstance(most, (int, float)) else ""
            return (f"No {gpu} is available{where} right now; {in_line} for one{up_to}, and nothing is billed while "
                    "you wait.")
        if not isinstance(waited, (int, float)):
            return f"{gpu} is out of stock{where} right now; try again {_when(retry_after_s)}."
        return f"No {gpu} became available{where} in the {duration(waited)} this robot waited; try again in a minute."
    if reason == "deployment_full":
        cap = f"max_gpus={count(d.get('max_gpus'))}"
        return (f"This deployment already holds its {cap} GPUs and every slot is taken; "
                + (f"{in_line}." if queued else
                   "raise its max_gpus with `seq policy set <name> max_gpus=N`, or try again when a robot finishes."))
    if reason == "queue_timeout":
        waited = d.get("waited_s")
        took = f"Waited {float(waited):.0f} s" if isinstance(waited, (int, float)) else "Waited"
        return f"{took} in the queue and no slot freed up, so nothing is held; try again later."
    return None


def queue_phrase(reason: Optional[str]) -> str:
    """Why a robot is queued, as the few words its notice carries."""
    return {"gpu_busy": "every GPU on the platform is busy",
            "gpu_limit_reached": "your account's GPUs are all in use",
            "deployment_full": "the deployment holds its max_gpus and every slot is taken",
            "in_line": "every seat on the deployment's workers is taken"}.get(
                reason or "", "waiting for a free slot")








QUEUE_POLL_MIN_S = 2.0
QUEUE_POLL_MAX_S = 30.0



HEAD_POLL_MIN_S = 1.0


def queue_wait(exc: Any) -> float:
    """Seconds before a queued robot (an `Unavailable` with `.queued`) polls again: the server's Retry-After, floored for
    the rate limit (less for the head of the line), capped, jittered."""
    asked = exc.retry_after_s if exc.retry_after_s and exc.retry_after_s > 0 else 5.0
    floor = HEAD_POLL_MIN_S if getattr(exc, "queue_position", None) == 1 else QUEUE_POLL_MIN_S
    return min(QUEUE_POLL_MAX_S, max(floor, asked)) * random.uniform(1.0, 1.2)


def queue_eta(exc: Any) -> Optional[float]:
    """The server's estimate of the wait, when it sent one (`eta_s`); else None. Never its Retry-After: that is when to
    ask again, and read as an estimate it told a robot "about 5s" for a wait of minutes.
    """
    eta = exc.details.get("eta_s")
    return float(eta) if isinstance(eta, (int, float)) and not isinstance(eta, bool) else None


def default_queue_notice(position: Optional[int], eta_s: Optional[float], waited_s: float,
                         reason: Optional[str]) -> None:
    """Say that the robot is in line for a slot, and why — the queue's counterpart of the warming notice, called on every
    poll so a long wait reads as progress.
    On stderr: a robot's program writes its own data to stdout, and fifteen of these lines at the head of its JSON broke
    the parse."""
    where = f"position {position}" if position is not None else "in line"
    eta = f", about {eta_s:.0f}s" if eta_s is not None and eta_s > 0 else ""



    print(f"[sequences] queued for a seat: {where}{eta} — {queue_phrase(reason)} "
          f"(waited {waited_s:.0f}s so far)", file=sys.stderr, flush=True)
