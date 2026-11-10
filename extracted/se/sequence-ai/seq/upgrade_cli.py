"""
`seq policy upgrade` / `seq benchmark upgrade`, and the lines `seq policy status / versions / ls` and `seq deploy` print
about a template's version and a deployment's scaling.

In one sentence: the platform reads which official template version a deployment or benchmark runs off its code →
`seq policy status` and `seq policy versions` name it, and the newer stable version with what it changed → `seq policy
upgrade <name>` asks the platform to deploy that version as the next one (POST .../upgrade), what the owner changed of
the old one and the deployment's scaling kept → it prints what changes, what stays and, when it changes, one worker's
price an hour before and after (a benchmark's: one machine's) - then follows the build as `seq deploy` does.
`--dry-run` prints the same and deploys nothing.

WHY "upgrade" and not "update": `seq policy set` updates a deployment's settings; this moves its
code to a newer version of the template it came from.
"""
from __future__ import annotations

import math
import os
from typing import Any, Callable

from seq.errors import build_failed, following, out_of_time, state_said
from sequence_ai._core.names import segment

from sequence_ai._core.money import per_hour



SETTING_KEY = {"max_gpus": "max_gpus", "min_containers": "min_workers", "buffer_containers": "buffer_workers"}


def fmt_bounds(bounds: Any) -> str:
    """[[-1, 1]] * 7 + [[0, 1]] → "[-1, 1] ×7, [0, 1]": each run of the same bounds once, with its count."""
    pairs = [tuple(float(x) for x in b) for b in (bounds or [])]
    out: list[str] = []
    i = 0
    while i < len(pairs):
        j = i
        while j < len(pairs) and pairs[j] == pairs[i]:
            j += 1
        lo, hi = pairs[i]
        out.append(f"[{lo:g}, {hi:g}]" + (f" ×{j - i}" if j - i > 1 else ""))
        i = j
    return ", ".join(out)


def action_limits(bounds: Any, max_delta: Any) -> str:
    """What the platform holds each step of an action to, as the dry run's action line and an upgrade's changes say it -
    the bounds it clips into and the most a step may change; "" when it declares neither (the line reads as it did)."""
    parts = []
    if bounds:
        parts.append(f"bounds {fmt_bounds(bounds)} (each step clipped into them)")
    if max_delta is not None:
        md = fmt_bounds([[-m, m] for m in max_delta]) if isinstance(max_delta, list) else f"{float(max_delta):g}"
        parts.append(f"max change per step {md}")
    return " · ".join(parts)


def camera_fit(camera: Any) -> str:
    """How a camera's frames are fitted to its size, as the policy declares it ("pad · bilinear"), or that it does not -
    then the robot fits them itself with sequence_ai.resize_image (the worker checks the size only)."""
    resize, filt = getattr(camera, "resize", None), getattr(camera, "filter", None)
    if resize or filt:
        return " · ".join(x for x in (resize, filt) if x)
    return "fit not declared: the robot calls resize_image itself"


def _fmt(field: str, value: Any) -> str:
    if field.endswith(".bounds"):
        return fmt_bounds(value) if value else "none"
    if isinstance(value, dict) and "uri" in value:
        return str(value["uri"])
    if isinstance(value, list):
        return ", ".join(str(v) for v in value) or "none"
    return "none" if value is None else str(value)


def template_lines(template: dict | None, update: dict | None, name: str, kind: str = "policy",
                   edited: dict | None = None) -> list[str]:
    """`template    pi05-droid v13` and, when the template's stable version is past it, what that one brings and the
    command that moves to it; for code edited after `seq init`, the template its image installs - `template
    toy-policy v3 (edited)` (the platform's edited_from) - with no upgrade from it. Nothing for code of no template."""
    if not template:
        from seq.listing import edited_label

        return [f"template    {edited_label(edited)}"] if edited else []
    cpu = " (its CPU version)" if template.get("variant") == "cpu" else ""
    lines = [f"template    {template['name']} {template['version']}{cpu}"]
    if update:
        from seq.listing import notes_said

        notes = notes_said(update.get("notes"))
        lines.append(f"            {update['name']} {update['version']} is available"
                     + (f": {notes}" if notes else "") + f" — seq {kind} upgrade {name}")

        if update.get("note"):
            lines.append(f"            {update['note']}")
    return lines


def kept_scaling(request_autoscaler: Any, scaling_now: dict | None) -> dict:
    """{field: (the deployment's, the file's)} for each scaling field a new version keeps where the file says otherwise:
    the deployment's, as `seq policy set` changes it."""
    asked = request_autoscaler.model_dump() if hasattr(request_autoscaler, "model_dump") else dict(request_autoscaler or {})
    now = scaling_now or {}
    return {k: (now[k], asked[k]) for k in SETTING_KEY if k in asked and k in now
            and asked[k] is not None and now[k] != asked[k]}


def kept_lines(name: str, kept: dict, *, source: str = "the file") -> list[str]:
    """One line per scaling field kept, by its setting's key: "kept mypi05's max_gpus 8 (the file says 1) — change it
    with seq policy set mypi05 max_gpus=N"."""
    out = []
    for field, pair in kept.items():
        mine, asked = (pair["deployment"], pair["request"]) if isinstance(pair, dict) else pair
        key = SETTING_KEY.get(field, field)
        out.append(f"kept        {name}'s {key} {mine} ({source} says {asked}) — change it with seq policy set {name} "
                   f"{key}=N")
    return out


def _price_line(price: dict | None, kind: str) -> str | None:
    """The upgrade's price, before → after - None when it does not change. A policy's is one worker's an hour, its CPU
    and memory at the rates it is billed at; a benchmark's one machine's card and the CPU and memory it asks for, which
    an eval bills at least - more when its machines use more (the platform's plan prices the request alone).
    WHY: libero-10's dry run said "$0.9849/h → $0.9849/h, one worker" - the same price, a word of policies, and none of
    its eval machines' $1.13-1.16/h, their CPU and memory as used.
 
"""
    price = price or {}
    before, after = price.get("before"), price.get("after")
    if before == after:
        return None

    def worker(p: dict | None) -> str:
        if not p or p.get("usd_per_hour") is None:
            return "unpriced"
        rates = "serving" if p.get("rates") == "serving" else "base"
        return f"{per_hour(p['usd_per_hour'])} ({p.get('card') or 'no GPU'}, CPU and memory at the {rates} rates)"

    def machine(p: dict | None) -> str:
        if not p or p.get("usd_per_hour") is None:
            return "unpriced"
        card = p.get("card")
        return f"{per_hour(p['usd_per_hour'])} ({'CPU' if not card or card == 'cpu' else card})"

    if kind == "benchmark":
        return (f"price       {machine(before)} → {machine(after)} a benchmark machine, for its card and the CPU and "
                "memory it asks for; an eval bills what its machines use beyond them")
    return f"price       {worker(before)} → {worker(after)}, one worker"


def _changed(c: dict) -> str:
    """A change as `changes` lists it: a structure in the platform's own clause ("image: base and 3 build steps
    changed"), else its value before → after. A structure it said none of is said changed, never printed whole: an
    image is a page of build steps."""
    if c.get("said"):
        return c["said"]
    if _whole(c.get("from")) or _whole(c.get("to")):
        return "changed"
    return f"{_fmt(c['field'], c.get('from'))} → {_fmt(c['field'], c.get('to'))}"


def _kept(k: dict) -> str:
    """A value that stays the owner's, as `stays yours` lists it: in the platform's clause for a structure, else yours
    beside the template's."""
    if k.get("said"):
        return k["said"]
    if _whole(k.get("yours")) or _whole(k.get("template")):
        return "differs from the template's"
    return f"{_fmt(k['field'], k.get('yours'))} (the template's: {_fmt(k['field'], k.get('template'))})"


def _whole(value: Any) -> bool:
    """Whether a value is a structure no line says whole: a mapping (a checkpoint, said by its uri, aside) or a list of
    them."""
    if isinstance(value, dict):
        return "uri" not in value
    return isinstance(value, list) and any(isinstance(v, dict) for v in value)


def _check_line(fs: dict | None) -> str:
    """A benchmark upgrade's check, as its last checked version measured it: about what it costs on its card - or that
    none of its versions kept its check's time, never a guess."""
    from sequence_ai._core.money import money

    check = (fs or {}).get("check") or {}
    if not check.get("seconds"):
        return "check       not priced: no version of it kept its check's time"
    on = check.get("card") or "a machine with no card"
    if check.get("usd") is None:
        return f"check       not priced: {on} is not offered now"
    return (f"check       about {money(check['usd'])} on {on}, as v{fs.get('version')}'s check took"
            + ("" if check.get("billed", True) else ", though checks are not billed now"))


def plan_lines(plan: dict, kind: str) -> list[str]:
    """What an upgrade does, as `seq policy upgrade` and its --dry-run print it."""
    frm, to = plan.get("from") or {}, plan.get("to") or {}
    out = [f"upgrade     {plan.get('name')}: {frm.get('name')} {frm.get('version')} → {to.get('version')}"]


    if plan.get("note"):
        out.append(f"why         {plan['note']}")
    for note in plan.get("notes") or []:
        out.append(f"new         {note}")
    for i, c in enumerate(plan.get("changes") or []):
        out.append(f"{'changes' if i == 0 else '':12}{c['field']}: {_changed(c)}")
    for i, k in enumerate(plan.get("kept") or []):
        out.append(f"{'stays yours' if i == 0 else '':12}{k['field']}: {_kept(k)}")
    price = _price_line(plan.get("price"), kind)
    if price:
        out.append(price)



    if kind == "benchmark" and "first_start" in plan:
        out.append(_check_line(plan.get("first_start")))


    if plan.get("notice"):
        out.append(f"notice      {plan['notice']}")


    if plan.get("adapters"):
        out.append(f"adapters    also registered in your account: {', '.join(plan['adapters'])}; an eval names "
                   f"{'them' if len(plan['adapters']) > 1 else 'it'} with nothing more to deploy")
    if kind == "policy":
        out.append(f"keeps       its name, robot keys, scaling (max GPUs, warm and spare workers), monthly budget, "
                   f"alerts and params; the version serving now is kept — seq policy rollback {plan.get('name')}")
    return out


def upgrade(name: str, *, kind: str = "policy", to: str | None = None, dry_run: bool = False, wait: bool = True,
            timeout: float | None = None, base_url: str | None = None, echo: Callable[[str], None] = print) -> dict:
    """`seq policy upgrade <name> [--to TEMPLATE@vN]` / `seq benchmark upgrade <name> [--to TEMPLATE@vN]`: POST
    .../upgrade, print what it does, and (unless --dry-run or --no-wait) follow the new version's build to its end, which
    raises when it does not end ready.
    `to` names a version of the template `name` was made from - any other template is refused before anything is
    deployed, by the platform's own dry run of it (its `from`) - and none is the template's stable version.
    `timeout` (--timeout): how long the build may run, the platform stopping it then, as `seq deploy --timeout`.
    """
    from seq.deployments_cli import _call

    path = f"/v1/{'deployments' if kind == 'policy' else 'benchmarks'}/{segment(name)}/upgrade"
    limit = {"time_limit_s": timeout} if timeout is not None and not dry_run else {}
    if to is None:
        plan = _call("POST", path, base_url, {"to": None, "dry_run": dry_run, **limit})
    else:
        from seq.cli_parser import at_version, version_alone
        from sequence_ai.errors import InvalidRequest

        alone = version_alone(to)
        if alone is not None:




            own = (_call("POST", path, base_url, {"to": f"v{alone}", "dry_run": True}).get("from") or {}).get("name")
            raise InvalidRequest(f"--to v{alone} names a version but not its template: {name} is made from {own}, so "
                                 f"write --to {own}@v{alone}")
        template, version = at_version(to, "template version")
        if version is None:
            raise InvalidRequest(f"{to!r} names no template version: --to TEMPLATE@vN (e.g. toy-policy@v3)")
        plan = _call("POST", path, base_url, {"to": f"v{version}", "dry_run": True})
        own = (plan.get("from") or {}).get("name")
        if own != template:
            raise InvalidRequest(f"{name} is made from {own}, not {template}: --to names a version of its own template, "
                                 f"e.g. --to {own}@v{version}")
        if not dry_run:
            plan = _call("POST", path, base_url, {"to": f"v{version}", "dry_run": False, **limit})
    if plan.get("already_runs"):


        echo(plan["message"])
        return plan
    for line in plan_lines(plan, kind):
        echo(line)
    if dry_run:
        echo("\n--dry-run: nothing was deployed; without it, " + (
            "the benchmark is registered again as its next version." if kind == "benchmark" else
            "the new version builds beside the one serving."))
        return plan
    version = plan.get("version")


    made = f"from template {plan['to']['name']} {plan['to']['version']}"
    if kind == "benchmark":



        runs = plan.get("runs")
        until = f"until it passes its check, evals run v{runs}" if runs else "an eval runs it once it passes its check"
        echo(f"{name} v{version} is building ({made}); {until}")
        if wait:
            from seq._eval_gateway import EvalGatewayClient

            with following(f"benchmark {name} v{version}", timeout, f"`seq benchmark cancel {name}` stops it now"):
                final = EvalGatewayClient(base_url=base_url).wait_benchmark(name, timeout_s=math.inf)
            _ended(final, name, kind, echo)
        return plan
    echo(f"{name} v{version} is building beside the one serving ({made})")
    if not wait:
        echo(f"follow it with: seq policy status {name} --wait")
        return plan
    from seq._deploy_gateway import DeploymentsClient

    client = DeploymentsClient(api_key=None, base_url=base_url or os.environ.get("SEQUENCES_BASE_URL"))
    with following(f"{name} v{version}", timeout):
        final = client.wait(name, timeout_s=math.inf)
    _ended(final, name, kind, echo)
    return plan


def _ended(final: Any, name: str, kind: str, echo: Callable[[str], None]) -> None:
    """An upgrade's build as it ended, said: ready, or raised as `seq deploy`'s is, so a script hears it. Before, a build that
    failed read `name: failed` and exited 0."""
    echo(f"{name}: {state_said(final.status.value, final.error)}")
    if final.status.value == "failed":
        raise build_failed(f"benchmark {name}" if kind == "benchmark" else name, final.error,
                           hint=out_of_time(final.error, f"seq {kind} upgrade {name}"))
