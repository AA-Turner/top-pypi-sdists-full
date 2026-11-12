"""
`seq deploy`'s request in words (its --dry-run too) and its wait, `seq policy status` and `seq policy logs
--build`: the body assembled offline and checked against the contract, the echo of what will be sent (image, code,
contract), the build's phases and newest log line while a policy builds or a benchmark registers, and the state and
fleet of a deployment. seq/cli.py's `_cmd_deploy` loads the folder's class (through `cli._load_folder`,
which tests replace) and calls in here; `_cmd_policy` sends `status` and `logs --build` here.
Moved out of seq/cli.py when it reached 1500 lines; the output is unchanged.


"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from typing import Any, Callable

from seq.cli_json import _print_json
from seq.clock import stamp
from seq.errors import (CANCELED, TIME_LIMIT, SeqAuthoringError, build_failed, canceled, following, out_of_time,
                        state_said, still_building)
from sequence_ai._core.names import segment
from sequence_ai.errors import AuthError, Conflict, InvalidRequest, SequencesError



def _request_of(kind: str, cls: type, *, name: str | None = None, require_cap: bool = False,
                snapshots: list | None = None) -> Any:
    """The body `seq deploy` sends for this class — assembled here, offline, and checked against its contract.
    `require_cap` refuses a GPU policy that names no max_gpus, as the platform does at deploy.

    What is uploaded is appended to `snapshots` when given (seq.code_bundle.Snapshot)."""
    from pydantic import ValidationError

    try:
        if kind == "benchmark":
            from seq.benchmark_registry import benchmark_request

            request = benchmark_request(cls, name=name, snapshots=snapshots)
        else:
            from seq.deploy import deployment_request

            request = deployment_request(cls, name=name, snapshots=snapshots)
            if require_cap:
                _require_gpu_cap(request)
        _contract_check(request)
    except ValidationError as exc:
        raise SeqAuthoringError("; ".join(f"{'.'.join(map(str, e['loc'])) or 'request'}: {e['msg']}"
                                          for e in exc.errors())) from None
    return request


def max_gpus_required_message() -> str:
    """Why a GPU deployment sets its own max GPUs, what it means, and how to write it: the platform's refusal word for word,
    but for the account's figure."""
    return ("max_gpus is required for a GPU deployment: the most GPUs it may hold at once, counted in cards. How many "
            "robots each worker seats is the policy's own (`seq policy status <name>` shows its seats); with every "
            "seat taken the next robot waits in line. Declare @seq.policy(max_gpus=N); change it any time "
            "with `seq policy set <name> max_gpus=N`, without a redeploy")


def _require_gpu_cap(request: Any) -> None:
    """A policy on a GPU sets its own max GPUs: refused here, before anything is sent - by `seq deploy` and its --dry-run
    alike - as the platform refuses it at deploy
. A dry run that only warned passed what the deploy then refused.

    """
    gpus = [str(g) for g in (request.resources.gpu or [])]
    if any(g.lower() != "cpu" for g in gpus) and request.autoscaler.max_gpus is None:
        raise InvalidRequest(max_gpus_required_message())


def account_gpu_limit(base_url: str | None) -> int | None:
    """The GPUs this account may hold at once: GET /v1/account's gpus.limit, the platform's own figure (its contracted
    limit, else its plan's - Starter 8, Team 32), or None when it cannot be read (offline, no key): the platform holds
    a cap to it anyway, at deploy and on a change."""
    from seq.deployments_cli import _call

    try:
        acct = _call("GET", "/v1/account", base_url) or {}
    except SequencesError:
        return None
    limit = (acct.get("gpus") or {}).get("limit") if isinstance(acct, dict) else None
    return int(limit) if isinstance(limit, (int, float)) and not isinstance(limit, bool) and limit >= 1 else None


def over_limit_message(max_gpus: int, limit: int) -> str:
    """Max GPUs past the account's limit, said as the platform says it, word for word
."""
    return (f"max_gpus={max_gpus} is more GPUs than this account may hold at once: its limit is {limit}, counted in "
            f"cards. Set max_gpus to {limit} or less (`seq policy set <name> max_gpus={limit}`); the plans with a "
            "higher limit are on the console's Billing page")


def hold_cap_to_account(request: Any, base_url: str | None) -> None:
    """A GPU policy's own max GPUs past the account's limit, refused here - before code is uploaded or a build started - with
    the platform's words. The CLI took any cap from 1 to 256 and a Starter account (limit 8) deployed with 100
    ; the platform refuses it since, and this says so first
    
. A CPU policy's max GPUs counts no GPU, as the platform reads it."""
    gpus = [str(g) for g in (request.resources.gpu or [])]
    cap = request.autoscaler.max_gpus if request.autoscaler else None
    if cap is None or not any(g.lower() != "cpu" for g in gpus):
        return
    limit = account_gpu_limit(base_url)
    if limit is not None and cap > limit:
        raise InvalidRequest(over_limit_message(cap, limit))


def _contract_check(request: Any) -> None:
    """Re-validate the assembled request against its own contract type — this SDK's copy of the schema the platform
    enforces, where every sub-shape forbids unknown fields and pins its types — here with no network and no build. A
    round trip that holds is valid for THIS SDK's contract, not the platform's verdict: the platform checks it again,
    against its own and its newer rules, when it is sent.
"""
    type(request).model_validate(json.loads(request.model_dump_json()))


def _print_request(kind: str, request: Any, snap: Any = None, cls: Any = None) -> None:
    """The request in words, before anything is built: a benchmark's, or a policy's - its class `cls`, where given, says
    which argument its weights' directory is handed as (its registration's init=)."""
    if kind == "benchmark":
        _print_benchmark_echo(request, snap)
    else:
        _print_echo(request, snap, constructor=_constructor_of(cls))


def _constructor_of(cls: Any) -> Any:
    """The class's init= as its registration keeps it (PolicyRegistration.constructor), or None - none declared, no
    class, or one that cannot be read here (the dry run goes on without it)."""
    if cls is None:
        return None
    try:
        import seq

        return getattr(seq.registration(cls), "constructor", None)
    except Exception:
        return None


def _slug(name: str) -> str:
    """The last part of the directory a policy's weights are copied to: its name with each character but a letter, a
    digit or _ made _, as its workers name it - for the dry run's example alone, the class reads the real path from its
    argument.
 """
    import re

    s = re.sub(r"[^A-Za-z0-9_]", "_", str(name)).strip("_") or "policy"
    return f"p_{s}" if s[0].isdigit() else s


def weights_dir_line(request: Any, constructor: Any = None) -> str:
    """What `seq deploy --dry-run` says under the weights of a policy: they are copied before its workers start, and its
    class is handed the directory - as the argument its init= (`constructor`, its registration's) names "{weights}" for,
    where one does - such as
    /srv/ckpt/<its name>, read from there and never written in, as where it is depends on the machine its worker runs
    on: a worker whose replica runs isolated stages them to /srv/ckpt/<name>, another reads them under /data. Before, it
    said they were "mounted at /data" - the request's mount, not the class's path.

"""
    kwargs = getattr(constructor, "kwargs", None) or {}
    kwargs = kwargs if isinstance(kwargs, dict) else {}
    slug = _slug(request.name)



    parts = [str(n) for n in (getattr(request, "extra_weights", None) or {})]
    if parts:
        names = [str(getattr(request, "weights_name", None) or "weights"), *parts]
        handed = ", ".join(f"{n} {_handed(kwargs, '{weights.' + n + '}')}" for n in names)
        return (f"            → copied before its workers start; your class is handed each part's directory, {handed}, "
                f"such as /srv/ckpt/{slug} for {names[0]} and /srv/ckpt/{slug}.extra.{names[1]} for {names[1]}: read "
                "them from there, never write the paths in - where they are depends on the machine its worker runs on")
    return (f"            → copied before its workers start; your class is handed the directory "
            f"{_handed(kwargs, '{weights}')}, such as /srv/ckpt/{slug}: read it from there, never write the path in - "
            "where it is depends on the machine its worker runs on")


def _handed(kwargs: dict, form: str) -> str:
    """How init= hands a weights directory: as the argument that names `form` outright, else by the form itself."""
    arg = next((k for k, v in kwargs.items() if v == form), None)
    return f"as {arg}" if arg else f'by "{form}" in init='


def weights_parts_line(verdict: dict | None) -> str | None:
    """What the platform's check read of weights in named parts: each part by its name with its size (its
    weights_parts) - None for weights in one part, or a platform that says none.
"""
    parts = (verdict or {}).get("weights_parts") or {}
    if not parts:
        return None
    from seq.deployments_cli import part_size

    return "weights     " + ", ".join(f"{name} {part_size(part)}" for name, part in parts.items()) + \
        ", each part as the platform read it"


def _print_echo(request: Any, snap: Any = None, constructor: Any = None) -> None:
    """The policy's request in words: what the platform installs, where its class finds the weights, which files are
    uploaded, and what the policy declares about its inputs and outputs — seen before a single layer is built."""
    from sequence_base.constants.version import CONTRACT_VERSION

    print(f"{'policy':<12}{request.name}")
    print(f"contract    valid for this SDK's deployment contract {CONTRACT_VERSION} (the platform checks it again "
          "when you deploy)")
    _print_image(request.image)
    _print_deps(snap)
    w = request.weights
    if w is None:
        print("weights     none (no checkpoint: nothing is copied or mounted)")
    else:

        parts = getattr(request, "extra_weights", None) or {}
        rows = [(str(getattr(request, "weights_name", None) or "weights"), w.uri),
                *((str(n), p.uri) for n, p in parts.items())] if parts else [("", w.uri)]
        width = max(len(n) for n, _ in rows)
        for i, (n, uri) in enumerate(rows):
            print(f"{'weights' if i == 0 else '':<12}" + (f"{n:<{width}}  " if parts else "") + uri)
        print(weights_dir_line(request, constructor))
    _print_code(request.code, snap)
    _print_contract(request.policy)
    if request.policy.params:
        from sequence_base.contract.deployments import describe


        shown = ", ".join(f"{k}: {p.type} = {p.default!r}"
                          + (f" ({describe(p)})" if (p.min, p.max, p.choices) != (None, None, None) else "")
                          for k, p in request.policy.params.items())




        print(f"params      {shown}  (defaults: `seq policy set {request.name} params.NAME=VALUE`; one eval's: "
              "`seq eval run --param policy.NAME=VALUE`)")

    if getattr(request.policy, "models", None):
        shown = ", ".join(m.rsplit("/", 1)[-1] for m in request.policy.models)
        print(f"models      {shown}  (the robot key driving this deployment may call these on /v1/chat, /v1/decide)")


def _print_benchmark_echo(req: Any, snap: Any = None) -> None:
    """The benchmark's registration in words: its image, where its sims run, what it evaluates, the uploaded files."""
    from sequence_base.constants.version import CONTRACT_VERSION

    print(f"benchmark   {req.name}")
    print(f"contract    valid for this SDK's contract {CONTRACT_VERSION} (the platform checks it again when you "
          "deploy)")
    _print_image(req.image)
    _print_deps(snap)
    if req.gpu == "cpu":
        mem = getattr(req, "memory_gb", None)
        print(f"sims        on CPU machines, {req.cpu} cores each" + (f"; {mem:g} GB memory" if mem else ""))
    else:
        print(f"sims        on {req.gpu}, one card per benchmark machine")

    if req.worlds:
        print(f"worlds      up to {req.worlds} a step call (@seq.concurrent(sizes=[{req.worlds}])): an eval builds as "
              "many as it needs, at most that")
    else:
        print("worlds      one a step call: an eval runs as many copies of the benchmark as it needs")
    limits = sorted(set(req.max_seconds.values())) if isinstance(req.max_seconds, dict) else [req.max_seconds]
    said = f"{limits[0]:g} s" if len(limits) == 1 else f"{limits[0]:g}-{limits[-1]:g} s by task"
    described = sum(1 for text in req.tasks.values() if text)
    print(f"episodes    {len(req.tasks)} task(s) × {len(req.seeds)} seed(s), each at most {said} on the robot's clock"
          + (f"; {described} task description(s)" if described else ""))
    _print_code(req.code, snap)


def _print_image(img: Any) -> None:
    """The image the platform builds: its origin, then every step in the order the build runs them."""
    print(f"image       {f'dockerfile ({len(img.dockerfile)} bytes)' if img.dockerfile else img.base}")
    any_step = False
    for step in img.steps:
        d = step.model_dump()
        any_step = True
        if "apt_install" in d:
            print(f"  apt-get install   {', '.join(d['apt_install']) or '(none)'}")
        elif "uv_pip_install" in d:
            print(f"  uv pip install    {', '.join(d['uv_pip_install']) or '(none)'}")
        elif "run_commands" in d:
            for cmd in d["run_commands"]:
                print(f"  run               {cmd}")
        elif "env" in d:
            for k, v in d["env"].items():
                print(f"  env               {k}={v}")
        elif "add_local" in d:
            print(f"  add               {d['add_local']['src']} → {d['add_local']['dst']}")
        elif "project" in d:
            p = d["project"]
            files = [f"{p['root']}/{f}" if p["root"] else f for f in ([p["lock"]] if p["lock"] else []) + p["declared"]]
            print(f"  project           {', '.join(files) or 'its packages'}"
                  + (f"; {len(p['packages'])} package(s) of the code's own" if p["packages"] else ""))
    if not any_step:
        print("  (no build steps — base image only)")


def _print_deps(snap: Any = None) -> None:
    """What the deploy makes of the project's own dependency files: what it installs from them and why, or that it
    reads none of them and how to make it (seq.project_deps). Said by `seq deploy` and its --dry-run alike."""
    for line in getattr(snap, "deps_lines", None) or []:
        print(line)


def _print_code(code: Any, snap: Any = None) -> None:
    """What the deploy uploads: the folder it deploys, whole, and the class in it it deploys - how many files, how
    large, and their hash, the one the platform keeps beside the version; then what was left out, and why.
    """
    if code is None:
        print("code        none uploaded — the image itself installs the handler's module")
        return
    if snap is None:
        from seq.code_bundle import bundle_listing

        names = bundle_listing(code)
        print(f"code        {len(names)} file(s), {len(code.raw()) / 1024:.1f} KiB uploaded:")
        for n in names:
            print(f"              {n}")
        return
    from seq.code_bundle import _shown

    size = f"{snap.raw_bytes / 1e6:.1f} MB" if snap.raw_bytes >= 100_000 else f"{snap.raw_bytes / 1024:.1f} KiB"
    packed = f"{len(code.raw()) / 1e6:.2f} MB" if len(code.raw()) >= 100_000 else f"{len(code.raw()) / 1024:.1f} KiB"
    if snap.folder is None:
        print(f"code        the declared files: {snap.files} file(s), {size} ({packed} compressed)")
    else:
        print(f"code        the folder {_shown(snap.folder)}, whole: {snap.files} file(s), {size} ({packed} "
              "compressed)")

        print(f"            the class it deploys is in {snap.entry}")
    from seq.code_bundle import bundle_listing

    print(f"            {_top_level(bundle_listing(code))}")
    print(f"            tree sha256 {snap.tree_sha256}")
    for line in _left_out_lines(snap.left_out):
        print(f"            {line}")
    for st in snap.sources:
        if st.state == "not downloaded":
            print(f"            {st.path}: not in the folder (seq init --no-source) - the image installs it from its "
                  f"official package, sha256 {st.source.package_sha256[:12]}")


def _top_level(names: list[str]) -> str:
    """What a bundle holds, by its top level: each file there by name, each directory with how many files it holds."""
    counts: dict[str, int] = {}
    for n in names:
        head, sep, _ = n.partition("/")
        key = head + "/" if sep else head
        counts[key] = counts.get(key, 0) + 1
    return ", ".join(f"{k} ({v})" if k.endswith("/") else k for k, v in sorted(counts.items()))


def _left_out_lines(left_out: list) -> list[str]:
    """What a snapshot left out, one reason a line: caches and bytecode counted by name, anything else by path."""
    groups: dict[str, list[str]] = {}
    for path, why in left_out:
        groups.setdefault(why, []).append(path)
    lines = []
    for why, paths in groups.items():
        if why in ("a cache", "compiled bytecode", "the Finder's folder notes"):
            names: dict[str, int] = {}
            for p in paths:
                base = p.rstrip("/").rsplit("/", 1)[-1] + ("/" if p.endswith("/") else "")
                key = "*" + base[base.rfind("."):] if why == "compiled bytecode" else base
                names[key] = names.get(key, 0) + 1
            shown = ", ".join(f"{k} ×{n}" if n > 1 else k for k, n in names.items())
        else:
            shown = ", ".join(paths[:4]) + (f" and {len(paths) - 4} more" if len(paths) > 4 else "")
        lines.append(f"{'left out: ' if not lines else '          '}{shown} ({why})")
    return lines


def _print_contract(policy: Any) -> None:
    """What the deployment says of its inputs and outputs: its own - the platform hands its functions what its robot
    sends and its robot what it returns, unchecked (north star 5)."""
    print("I/O         the policy's own — the platform hands its functions what its robot sends and returns what they "
          "return, unchecked")


def name_claim(name: str, handler_ref: str, base_url: str | None) -> dict | None:
    """What deploying `handler_ref` under `name` would be, as the platform sees it now: {"state": "new" | "version" |
    "replace" | "taken", ...}. None when it cannot be asked (no key, offline)."""
    from urllib.parse import quote

    from seq.deployments_cli import _call

    try:
        return _call("GET", f"/v1/deployments/{segment(name)}/claim?handler_ref={quote(handler_ref)}", base_url)
    except Exception:
        return None


def claim_line(name: str, claim: dict | None) -> str:
    """The line `seq deploy --dry-run` prints about the name."""
    state = (claim or {}).get("state")
    if state == "new":
        return f"name        {name!r} — a new deployment"
    if state == "version":
        return f"name        {name!r} — a new version of it; the one serving goes on until this one builds"
    if state == "replace":
        return (f"name        {name!r} runs {claim.get('held_by')} with {int(claim.get('robots') or 0)} robot(s) "
                "connected — deploying this takes it over: add --override, or name it otherwise with --name")
    if state == "taken":


        why = (claim or {}).get("detail") or "another account had it first, and it is too long to be made yours too"
        return f"name        {name!r} cannot be yours: {why}"
    if state == "invalid":
        return f"name        {name!r} cannot be used: {(claim or {}).get('detail') or 'the platform refuses it'}"
    return f"name        {name!r} (not checked: the platform could not be asked)"


def refuse_claim(claim: dict | None) -> None:
    """A dry run ends as the deploy would when the platform refuses the name: a name it cannot take (a ".") as the
    request's (rc 2), one another account holds and that cannot be made yours as the state's (rc 5). The line above
    already said why.
"""
    state = (claim or {}).get("state")
    if state == "invalid":
        raise InvalidRequest((claim or {}).get("detail") or "the platform refuses this name")
    if state == "taken":
        raise Conflict((claim or {}).get("detail") or "another account holds this name")


def platform_check(request: Any, *, override: bool, base_url: str | None) -> dict | None:
    """The platform's own check of the request, with nothing built (POST /v1/deployments/validate): its refusal raised
    as the deploy's would be - the same error and exit code - its answer {"ok", "name", "state", "contract"} on
    acceptance, None when it cannot be asked (no key, offline). Before it a dry run
    said "platform accepted" from this SDK's own contract, and a platform with newer rules refused the same file at
    deploy."""
    from seq._deploy_gateway import DeploymentsClient

    try:
        client = DeploymentsClient(api_key=None, base_url=base_url or os.environ.get("SEQUENCES_BASE_URL"))
    except AuthError:
        return None
    try:
        return client.validate(request, override=override)
    except AuthError:
        return None


def request_check(request: Any, *, base_url: str | None) -> None:
    """The platform's word on the request alone, for `seq --json deploy --dry-run`, which prints the request: asked as
    platform_check asks it (POST /v1/deployments/validate, the deploy's own checks), its refusal of the request itself -
    a 400, such as a card it does not offer - raised as the deploy's, the same error and exit code. What the name or the
    account holds (a name taken, credit, a volume not uploaded), and a platform that cannot be asked, leave it the
    request read here, as before: the JSON is the request, those are the deploy's to say.
"""
    try:
        platform_check(request, override=False, base_url=base_url)
    except InvalidRequest:
        raise
    except SequencesError:
        return


def platform_line(verdict: dict | None) -> str:
    """The line `seq deploy --dry-run` prints about the platform's check."""
    if verdict is None:
        return ("platform    not checked: the platform could not be asked (no key, or offline); it checks this when "
                "you deploy")
    contract = verdict.get("contract")
    return ("platform    accepted  (checked by the platform"
            + (f" against its contract {contract}" if contract else "") + "; nothing was built)")


def margin_line(verdict: dict | None) -> str | None:
    """What the platform said of the request's replan step in its dry run: whether
    its robots' answers would come before they played the valid steps of the ones before, on what the platform knows of
    its policy's time and the account's robots' network, and what would let them. None where they would, or the platform
    was not asked."""
    said = ((verdict or {}).get("margin") or {}).get("says")
    return f"margin      {said}" if isinstance(said, str) and said else None


def memory_line(verdict: dict | None) -> str | None:
    """The platform's dry-run reminder when the host memory the request asks for is less than its weights' size
    (`memory_note`): one line under the verdict, a reminder only - not a refusal, here or at deploy. None where the
    platform said none, or it was not asked."""
    note = (verdict or {}).get("memory_note")
    return f"memory      {note}" if isinstance(note, str) and note else None


def registration_check(ask: Callable[[], dict | None]) -> dict | None:
    """The platform's own check of a benchmark's or an adapter's registration, with nothing registered or built - `ask`
    posts it (EvalGatewayClient.validate): its refusal raised as the registration's would be, the same error and exit
    code; its answer on acceptance; None when it cannot be asked - no key, a key it does not take, no answer - and the
    dry run is then the checks here alone. A policy's is platform_check.
    """
    try:
        return ask()
    except AuthError:
        return None


def registration_line(kind: str, verdict: dict | None) -> str:
    """The line `seq deploy --dry-run` prints about the platform's check of a benchmark or an adapter (`kind`): what
    registering it would make, or why it was not checked."""
    if verdict is None:
        return ("platform    not checked: the platform could not be asked (no key, or offline); it checks this when you "
                "register it")
    name, version, contract = verdict.get("name"), verdict.get("version"), verdict.get("contract")
    made = {"new": f"a new {kind}, v{version}", "version": f"{name} v{version}, its next version",
            "same": f"this code is {name}@v{version} already, which registering it keeps",
            "replace": f"{name} v{version}, taken over from {verdict.get('held_by')} (--override)"}.get(verdict.get("state"))
    return ("platform    accepted  (checked by the platform" + (f" against its contract {contract}" if contract else "")
            + (f": {made}" if made else "") + "; nothing was built)")


def first_start_lines(name: str, verdict: dict | None) -> list[str]:
    """What the platform said of the name's first start in its dry run: its
    newest version that passed its check - how long it took to ready, each step's time - and what this version's check
    would cost on the card it asks for; for a name with nothing measured, that there is no data, never a guess. Nothing
    when the platform was not asked."""
    from sequence_ai._core.money import money

    if not verdict:
        return []
    fs = verdict.get("first_start")
    if not fs:

        return [f"first start no data: no version of {name} was measured yet; the next build measures it"]
    head = f"first start v{fs.get('version')} took {elapsed(fs.get('seconds') or 0)} from its build's start to ready"
    steps = fs.get("steps") or {}
    if steps:
        head += ": " + " · ".join(f"{_STAGE_SHORT.get(k, k)} {elapsed(v)}" for k, v in steps.items())
    out = [head]
    check = fs.get("check") or {}
    if check.get("seconds"):
        cards = int(check.get("cards") or 0)
        on = f"{cards} x {check.get('card')}" if cards > 1 else (check.get("card") or "a machine with no card")


        ran = f"its check machine ran {elapsed(check['seconds'])} from its start"
        if check.get("usd") is None:
            said = f"{ran}; {on} is not offered now, so this version's check is not priced"
        else:
            said = (f"{ran}: about {money(check['usd'])} for this version's check on {on}"
                    + ("" if check.get("billed", True) else ", though checks are not billed now"))
        out.append(f"{'':12}{said}")



    build = fs.get("build") or {}
    if build.get("seconds"):
        ran = f"the machine preparing its build ran {elapsed(build['seconds'])}"
        out.append(f"{'':12}" + (f"{ran}: about {money(build['usd'])} for this version's build"
                                 if build.get("usd") is not None else f"{ran}; not priced"))
    return out


def _seats_line(summary: dict | None) -> str | None:
    """How many robots one worker serves at once, from a ready build's summary (seats = the deployment's max_sessions),
    for `seq deploy`'s last words; None when the summary does not say it (a CPU-only or non-serving build). Of a policy
    that batches, how long each robot waits for an answer beside it (max_wait_for_batch), or that it is not set.
    """
    seats = (summary or {}).get("seats")
    if not seats:
        return None
    from sequence_ai._core.capacity import wait_said

    return f"a worker seats {seats} robot{'s' if seats != 1 else ''} at once" + wait_said(summary)


def _deploy_policy(args: argparse.Namespace, request: Any, snap: Any = None, *, sample: bool = False) -> int:
    """POST /v1/deployments, then (by default) poll building → ready | failed. A submit-time refusal (bad payload,
    unknown or foreign secret), an auth failure, a network error, a conflict and a failed build all raise with the
    reason, and none is reported as success. `--no-wait` stops after the 202. `sample`: the class names a sample
    episode (@seq.sample), which the request does not carry."""
    from seq._deploy_gateway import DeploymentsClient
    from sequence_base.contract import DeploymentState

    client = DeploymentsClient(api_key=None, base_url=args.base_url or os.environ.get("SEQUENCES_BASE_URL"))
    override = bool(getattr(args, "override", False))
    if override:

        claim = name_claim(request.name, request.policy.handler_ref, args.base_url)
        if claim and claim.get("state") == "replace":
            print(f"replacing: {request.name!r} ran {claim['held_by']} with {int(claim.get('robots') or 0)} robot(s) "
                  "connected — they switch to this policy once it builds")


        print(f"override: the version of {request.name} serving now is deleted for good once this one has passed its "
              "check and its workers have ended; if this one fails, nothing is deleted")

    accepted = client.submit(request, override=override, time_limit_s=getattr(args, "timeout", None))

    name = accepted.deployment_id
    if getattr(accepted, "unread", False):



        print(f"accepted: the platform took the deployment of {name} and its build has started, but its answer is not "
              f"one this sequence-ai reads (pip install -U sequence-ai); `seq{_tier_suffix(args.base_url)} policy "
              f"status {name} --wait` follows the build")
    else:
        print(f"accepted: deployment {name} is {accepted.status} (built on the platform, not here)")
    notice = getattr(accepted, "notice", None)
    if notice:

        print(f"{name}: {notice}")
    if getattr(accepted, "adapters", None):
        print(adapters_line(accepted.adapters, "a benchmark template you registered pairs with this policy"))
    if snap is not None and snap.tree_sha256:
        print(_kept_tree_line(name, snap.tree_sha256, args.base_url))
    for line in _kept_lines(name, request, args.base_url):
        print(line)

    before = _deployment_row(request.name, args.base_url)
    stopped = _stopped_how(request.name, before, args.base_url)
    if stopped:
        print(f"stopped: {request.name} is stopped, and a deploy keeps it so - {stopped}")
    if not args.wait:
        print(f"follow it with: seq{_tier_suffix(args.base_url)} policy status {name} --wait")
        return 0




    gpus = [str(g) for g in (getattr(getattr(request, "resources", None), "gpu", None) or [])]
    progress = _BuildProgress(name, args.base_url, acts=build_acts(request.policy), sample=sample,
                              card=gpus[0] if gpus else None,
                              plans=getattr(request.policy, "plan_every_s", None) is not None)


    stop = (f"`seq{_tier_suffix(args.base_url)} policy rm {name}` stops it now and deletes the policy"
            if (before or {}).get("status") == "building" else None)

    with following(name, getattr(args, "timeout", None), stop):
        final = client.wait(name, on_poll=progress, poll_interval_s=DEPLOY_POLL_S, timeout_s=math.inf)
    row = _deployment_row(request.name, args.base_url)
    if final.status == DeploymentState.READY:
        ver = f" v{row['version']}" if row and row.get("version") else ""
        fleet = _fleet_now(request.name, args.base_url)
        stopped = _stopped_how(request.name, row, args.base_url)
        if stopped:
            print(f"stopped: {request.name}{ver} is deployed, but {request.name} is stopped - {stopped}")
        else:
            print(f"ready: {request.name}{ver} is deployed — connect with sequence_ai.connect({request.name!r})")
        kept = None if stopped else _check_machine_kept(request.name, args.base_url, fleet)
        if kept:






            from sequence_ai._core.capacity import duration


            card = gpus[0].split(':')[0] if gpus else "cpu"
            machine = "CPU machine" if card.lower() == "cpu" else f"{card} machine"
            print(f"  its check's {machine} stays on as its first worker: it saves this version's image for its next "
                  f"machines, usually a minute or two, then with no robot connected ends after "
                  f"{duration(fleet['scaling']['idle_timeout'])} (its idle timeout), billed as a worker until then")
        elif kept is False:
            print("  its check's machine ended after its check: this version's first worker starts when it is needed "
                  "(a cold start)")


        start = progress.steps_line()
        if start:
            print(f"  {start}")

        seats = _seats_line(progress.summary)
        if seats:
            print(f"  {seats}")


        from seq.capacity_cli import print_worker_price


        made = ((row or {}).get("latest") or {}).get("version") or (row or {}).get("version")
        print_worker_price(request.resources, args.base_url or os.environ.get("SEQUENCES_BASE_URL"), name=request.name,
                           version=int(made) if made else None)

        from seq import storage_note

        storage_note.after_write(args.base_url)
        return 0

    serving = (f"{request.name} v{row.get('version')} is still serving; " if row and row.get("status") == "ready"
               else "")
    limit = out_of_time(final.error, "seq deploy")
    if limit:
        raise build_failed(name, final.error, hint=f"{serving}{limit}")

    said = progress.failure(request.name, final.error)
    sure = said[1] if said else None
    error = said[0] if said else (final.error or "no reason reported")



    ours = any(PLATFORMS_TO_FIX in (text or "") for text in (error, final.error))
    raise build_failed(name, error, hint=(f"{sure}; " if sure else "")
                       + (f"{serving}nothing in this version needs changing: run seq deploy again later" if ours
                          else f"{serving}fix what the build names and run seq deploy again"))


def _kept_lines(name: str, request: Any, base_url: str | None) -> list[str]:
    """What a new version of a deployment that runs keeps of its scaling where the file says otherwise - the platform
    keeps the deployment's - read from its fleet view.
    Nothing for a new deployment (no fleet yet), or where the view cannot be read."""
    from seq.deployments_cli import _call
    from seq.upgrade_cli import kept_lines, kept_scaling

    try:
        scaling = _call("GET", f"/v1/deployments/{segment(name)}/fleet", base_url)["scaling"]
    except Exception:
        return []
    kept = kept_scaling(getattr(request, "autoscaler", None), scaling)
    return kept_lines(name, kept, source="the file")


def _deploy_benchmark(args: argparse.Namespace, request: Any) -> int:
    """POST /v1/benchmarks (the declaration and its source), then (by default) wait for the platform to build its sim
    image. `seq deploy` registers a benchmark the way it deploys a policy: one command for both."""
    from seq._eval_gateway import EvalGatewayClient

    client = EvalGatewayClient(base_url=args.base_url)
    override = bool(getattr(args, "override", False))



    for line in _price_before(client, request, override):
        print(line)
    if override:


        print(f"override: the version of {request.name} evals run now is deleted for good once this one has passed its "
              "check and no eval runs it; if this one fails, nothing is deleted")
    registered = client.register(request, override=override, time_limit_s=getattr(args, "timeout", None))
    print(f"accepted: benchmark {request.name} is building (its sim image builds on the platform, not here)")
    if registered.adapters:
        print(adapters_line(registered.adapters, "its template pairs with its template policies"))
    if not args.wait:
        print(f"follow it with: seq{_tier_suffix(args.base_url)} benchmark status {request.name} --wait")
        return 0
    seen: list[str] = []

    def _show(resp: Any) -> None:
        state = state_said(resp.status.value, resp.error)
        if not seen or seen[-1] != state:
            seen.append(state)
            print(f"  {resp.name}: {state}", flush=True)

    from seq.eval_cli import lost_line


    with following(f"benchmark {request.name}", getattr(args, "timeout", None),
                   f"`seq{_tier_suffix(args.base_url)} benchmark cancel {request.name}` stops it now"):
        final = client.wait_benchmark(request.name, timeout_s=math.inf, on_poll=_show, on_retry=lost_line)
    if final.status.value == "ready":
        print(f"ready: evaluate a deployed policy on it with `seq eval run <policy> --benchmark {request.name}`")
        return 0
    raise build_failed(f"benchmark {request.name}", final.error, hint=out_of_time(final.error, "seq deploy"))


def _price_before(client: Any, request: Any, override: bool) -> list[str]:
    """A benchmark registration's price and its name's last first start, as its dry run says them, before it registers;
    nothing when the platform cannot be asked or refuses - the registration then says why."""
    try:
        verdict = client.validate("/v1/benchmarks/validate", content=request.model_dump_json(exclude_none=True),
                                  headers={"Content-Type": "application/json"},
                                  params={"override": "true"} if override else None)
    except Exception:
        return []
    return registration_price_lines(verdict) + first_start_lines(request.name, verdict)


def registration_price_lines(verdict: dict | None) -> list[str]:
    """What registering a benchmark costs before anything is paid, as the platform priced it (its dry run's `price`,
    gateway deployments/first_start.registration): each machine a registration runs, by the hour, billed by the second
    from when it starts - the one preparing its image where that is a machine of its own, and its check's, on its card.
    How long they run is the registration's own (first start says the last version's). Nothing from a platform that
    priced none.
"""
    from sequence_ai._core.money import per_hour

    price = (verdict or {}).get("price") or {}
    check, build = price.get("check") or {}, price.get("build") or {}
    if not check:
        return []

    def rate(m: dict) -> str:
        return "not priced now" if m.get("usd_per_hour") is None else per_hour(m["usd_per_hour"])

    def size(m: dict) -> str:
        cores, gib = float(m.get("cpu") or 0), float(m.get("memory_gib") or 0)
        return f"{cores:g} core{'' if cores == 1 else 's'}, {gib:g} GiB"

    cards = int(check.get("cards") or 0)
    on = (f"on {cards} x {check['card']}" if cards > 1 else f"on {check['card']}") if check.get("card") else \
        "with no card"
    if build:
        said = (f"price       registering it runs two machines, each billed by the second from when it starts: the one "
                f"preparing its image {rate(build)} ({size(build)}), and its check's {on} {rate(check)} ({size(check)})")
    else:
        said = (f"price       registering it runs its check's machine, billed by the second from when it starts: {on} "
                f"{rate(check)} ({size(check)}), its image built on it")
    return [said] + ([f"{'':12}checks are not billed now"] if price.get("billed") is False else [])


def adapters_line(adapters: list[str], whose: str) -> str:
    """The adapters the platform registered in the account with a registration, said where it is: which, whose they are,
    and that an eval names them with nothing deployed for them.

"""
    many = len(adapters) > 1
    return (f"  also registered in your account: {', '.join(adapters)} - the adapter{'s' if many else ''} {whose}; an "
            f"eval names {'them' if many else 'it'} with nothing more to deploy")


def more_line(name: str) -> Callable[[float], None]:
    """The line `seq benchmark status --wait` prints as it waits on a build that still moves."""
    from seq._eval_gateway import BENCHMARK_WAIT_MAX_S, BUILD_MORE_S

    return lambda waited: print(f"  {name}: still building after {waited / 60:.0f} min, its build log still moving: "
                                f"waiting {BUILD_MORE_S / 60:.0f} min more (up to {BENCHMARK_WAIT_MAX_S / 3600:.0f} h "
                                "in all)", flush=True)


def _kept_tree_line(name: str, uploaded: str, base_url: str | None) -> str:
    """What the platform keeps beside the new version, set against what was uploaded: the same tree sha256, said, or
    a difference, said - never silence."""
    try:
        from seq.deployments_cli import _call

        rows = _call("GET", f"/v1/deployments/{name}/versions",
                     base_url or os.environ.get("SEQUENCES_BASE_URL")).get("data") or []
        kept = ((rows[0] if rows else {}).get("code") or {}).get("sha256")
    except Exception:
        kept = None
    if kept is None:
        return "code        not checked: the platform's record of this version's files could not be read"
    if kept == uploaded:
        return f"code        the platform holds the same files: tree sha256 {kept[:12]}"
    return (f"code        the platform holds other files than were uploaded: tree sha256 {kept[:12]}, uploaded "
            f"{uploaded[:12]} - deploy again")


def _stopped_how(name: str, row: dict | None, base_url: str | None) -> str | None:
    """How a stopped deployment is started again, as the CLI says it where it would have said ready: a deploy keeps a
    deployment stopped - its owner stopped it, often to hold its spend - so a new version serves once it is started,
    never by the deploy. One its monthly budget stopped is told to raise or clear the budget first, or the platform's
    budget check stops it again (its row's stopped_reason "budget"). None for one that is not stopped.
    

"""
    if not (row or {}).get("stopped"):
        return None
    seq = f"seq{_tier_suffix(base_url)}"
    start = f"`{seq} policy start {name}`"
    if row.get("stopped_reason") == "budget":
        return (f"it was stopped at its monthly budget: raise it (`{seq} policy set {name} budget.monthly_usd=<usd>`) "
                f"or clear it (`{seq} policy set {name} budget.monthly_usd=`), then {start}")
    return f"robots are refused until {start}"


def _deployment_row(name: str, base_url: str | None) -> dict | None:
    """The platform's summary of one deployment (serving version, latest build), or None when unreadable. A policy's
    robot key may not list the account's policies, so its own policy's row is read from the policy's fleet view,
    which says the same of it (_row_from_fleet).
"""
    from sequence_ai.errors import PermissionDenied

    try:
        from seq.deployments_cli import _call

        rows = _call("GET", "/v1/deployments", base_url or os.environ.get("SEQUENCES_BASE_URL"))["data"]
    except PermissionDenied:
        return _row_from_fleet(name, base_url)
    except Exception:
        return None
    return next((r for r in rows if r.get("name") == name), None)


def _row_from_fleet(name: str, base_url: str | None) -> dict | None:
    """`name`'s list row as its fleet view says it - its state, the version that serves, the one on its way in, whether
    it is stopped and why, its act frames and what a redeploy brings - for a robot key, which reads its own policy's
    fleet but not the list. None where the view cannot be read."""
    try:
        from seq import capacity_cli

        fleet = capacity_cli.fleet(name, base_url=base_url or os.environ.get("SEQUENCES_BASE_URL"))
    except Exception:
        return None
    if not isinstance(fleet, dict):
        return None
    return {"name": name, "status": fleet["status"], "version": fleet.get("version"), "latest": fleet.get("next"),
            "stopped": bool(fleet.get("stopped")), "stopped_reason": fleet.get("stopped_reason")}


def status(name: str, *, wait: bool = False, timeout: float | None = None, base_url: str | None = None,
           echo: Callable[[str], Any] | None = None, warn: Callable[[str], Any] | None = None,
           on_data: Callable[[dict], Any] | None = None) -> dict:
    """`seq policy status <name>` / seq.policy_status: one GET, or `wait` to poll to a terminal state - then the fleet:
    each worker's copies, seats and sessions and why one died, and the robots waiting for a slot. Returns the
    deployment's state with its fleet, as `seq --json policy status` prints it.
    What it says goes through `echo` (nothing is said without one); what it warns of - a fleet it could not read, a
    version that failed beside the one serving - through `warn` (stderr, for the command). `on_data` hears the data
    once it is read, before the call ends in a refusal: a deployment whose build failed, or whose wait ran out, ends
    in one, after `seq --json` has printed what it read. The refusal is raised."""
    from seq._deploy_gateway import DeploymentsClient
    from sequence_base.contract import DeploymentState

    show = None if echo is None else (lambda resp: echo(status_text(resp)))
    base = base_url or os.environ.get("SEQUENCES_BASE_URL")
    client = DeploymentsClient(api_key=None, base_url=base)
    if wait:

        on_poll = (lambda r: show(r) if r.status != DeploymentState.READY else None) if show else None
        kwargs: dict = {"on_poll": on_poll} if on_poll else {}
        if timeout is not None:
            kwargs["timeout_s"] = timeout
        resp = client.wait(name, **kwargs)
    else:
        resp = client.status(name)
        if show and resp.status not in (DeploymentState.FAILED, DeploymentState.READY):
            show(resp)
    fleet = None
    if resp.status == DeploymentState.READY:
        fleet = _fleet_now(name, base)
        if show:
            stopped = _stopped_how(name, _deployment_row(name, base), base)
            echo(f"  {name}: stopped - {stopped}" if stopped else f"  {name}: ready")


    row = (_deployment_row(name, base) or {}) if resp.status == DeploymentState.FAILED else {}
    latest = row.get("latest") or {}
    serving = row.get("status") == "ready" and latest.get("status") == "failed"
    if show and resp.status == DeploymentState.FAILED and not wait:
        if serving:
            echo(f"  {name}: ready — v{row.get('version')} serving")
        else:
            show(resp)
    if fleet is None:
        fleet = _fleet_view(name, base, echo=echo, warn=warn)
    elif echo is not None:
        from seq import capacity_cli


        capacity_cli.show_fleet(name, fleet, echo)
    if echo is not None and resp.status != DeploymentState.FAILED:
        from seq.upgrade_cli import template_lines


        for line in template_lines((fleet or {}).get("template"), (fleet or {}).get("template_update"), name,
                                   edited=(fleet or {}).get("edited_from")):
            echo(line)
    data = {**resp.model_dump(mode="json"), "fleet": fleet}
    if on_data is not None:
        on_data(data)
    if resp.status == DeploymentState.FAILED:


        if serving:
            if warn is not None:
                said = build_failed(f"{name} v{latest.get('version')}", resp.error).message
                warn(f"warning: {said}; v{row.get('version')} goes on serving")
            return data
        raise build_failed(name, resp.error)
    if wait and resp.status != DeploymentState.READY:
        raise still_building(name, f"seq policy status {name} --wait")
    return data


def _stderr(line: str) -> None:
    print(line, file=sys.stderr)


def _cmd_status(args: argparse.Namespace) -> int:
    """`seq policy status <name> [--wait [--timeout S]]`: status, printed - with --json, as data, before the refusal a
    failed build ends in."""
    status(args.name, wait=args.wait, timeout=args.timeout, base_url=args.base_url,
           echo=None if args.json else _live, warn=None if args.json else _stderr,
           on_data=_print_json if args.json else None)
    if not args.json:


        from seq import manage_cli
        from sequence_ai.errors import SequencesError

        try:
            manage_cli.policy_metrics(args.name, base_url=args.base_url, echo=print)
        except SequencesError:
            pass
    return 0






_NO_ACT = ("checking it starts and answers its health check; it names no sample episode (@seq.sample), so the check "
           "calls nothing")



_PLAYS_SAMPLE = "playing its sample episode on it (@seq.sample), call by call"


_PLAYS_SAMPLE_AND_PLANS = ("playing its sample episode on it (@seq.sample), call by call, planning once after the first "
                           "act")


def build_acts(policy: Any) -> bool:
    """Whether the build check acts on `policy` beside its sample episode: never - a policy's inputs are its own, and
    the check plays the sample episode it marks (@seq.sample), which `sample` says. (harness/smoke_act.py)"""
    return False




_STAGES = {"upload": "unpacking the code", "image": "building the image", "weights": "copying the weights",
           "assets": "mounting its assets", "card": "waiting for a card", "machine": "waiting for a machine",
           "load": "starting a worker and loading the policy", "compile": "compiling and timing its batch sizes",
           "snapshot": "taking its snapshot", "act_check": "checking one /act on it", "check": "checking it on its card",
           "image_save": "saving the image"}
_STAGE_SHORT = {"act_check": "check", "image_save": "save"}
_ENDED = ("done", "reused", "failed", "skipped")


DEPLOY_POLL_S = 2.0


def elapsed(seconds: float) -> str:
    """A step's time as `seq deploy` says it: "7 s", "1 min 49 s"."""
    s = max(0, int(round(float(seconds))))
    return f"{s // 60} min {s % 60} s" if s >= 60 else f"{s} s"




PLATFORMS_TO_FIX = "the platform's to fix"


def _cut(text: str, most: int = 160) -> str:
    """A build's line as its step says it: whole up to `most` characters, else cut with "…" where it was cut, so a
    cut line reads as one (`seq policy logs NAME@vN --build` keeps it whole).
"""
    return text if len(text) <= most else text[:most - 1] + "…"


class _BuildProgress:
    """`seq deploy`'s live view of its build, step by step (GET .../build `stages`): each step's line as it begins,
    every line the build writes under the step it belongs to - read after the last one shown (after_seq) - each step's
    end with its time and what it did, and only then the state, so a step never shows up after the state it led to (a
    check said after "ready" when it began and ended between two reads); on a terminal the running step's time so far,
    kept live. Keeps the steps, the failed one and the build's summary for the deploy's last words.
    

"""

    def __init__(self, target: str, base_url: str | None, *, acts: bool = True, sample: bool = False,
                 card: str | None = None, out: Any = None, plans: bool = False) -> None:
        self._target, self._base_url = target, base_url


        self._acts, self._sample, self._plans = acts, sample, plans
        self._card = card
        self._state = None
        self.stages: list | None = None
        self.failed: dict | None = None
        self.summary: dict | None = None
        self._seq = 0
        self._running: dict | None = None
        self._now = 0.0
        self._said: dict[str, str] = {}
        self._shown: set[str] = set()
        self._printed: dict[str, set[str]] = {}
        self._open: str | None = None
        self._furthest = -1
        self._out = out or sys.stdout
        self._live = bool(getattr(self._out, "isatty", lambda: False)())
        self._status_on = False

    def _print(self, text: str) -> None:
        if self._status_on:
            self._out.write("\r\x1b[K")
            self._status_on = False
        print(text, file=self._out, flush=True)

    def _line(self, step: str, text: str) -> None:
        """A line the build wrote, said under its step - its step's line said again first where another step's came
        after it - and kept as said, for the step's failure to point to."""
        if self._open != step:
            self._again(step)
        self._print(f"      {_cut(text)}")
        self._printed.setdefault(step, set()).add(text)

    def _again(self, step: str) -> None:
        """Its step's line said again - "· load, continued" - so what follows it reads as that step's."""
        self._print(f"  · {_STAGE_SHORT.get(step, step)}, continued")
        self._open = step

    def _label(self, s: dict) -> str:
        name = s.get("stage")
        if name == "act_check" and not self._acts:
            return (_PLAYS_SAMPLE_AND_PLANS if self._plans else _PLAYS_SAMPLE) if self._sample else _NO_ACT
        if name == "card":
            limit = s.get("limit_s")
            card = f"an available {self._card}" if self._card and self._card.lower() != "cpu" else "a machine"
            return f"waiting for {card}" + (f" - up to {round(limit / 60)} min" if limit else "")
        return _STAGES.get(name, str(name))

    def _usual(self, s: dict) -> str:
        """How long such a step usually takes, from this deployment's earlier builds (typical_s) - said when the step
        begins so the wait has a yardstick, the same figure `seq policy logs --build` shows at the end."""
        t = s.get("typical_s")
        return f" (usually {elapsed(t)})" if isinstance(t, (int, float)) else ""

    def _end(self, s: dict) -> str | None:
        state, took, said = s.get("state"), s.get("duration_s"), s.get("summary")
        tail = f" · {said}" if said else ""
        if state == "done":
            return f"    done in {elapsed(took)}{tail}" if took is not None else (f"    done{tail}" if said else None)
        if state == "reused":
            return f"    reused from v{s.get('from_version')}" + (f" · {elapsed(took)}" if took is not None else "")
        if state == "failed":
            return f"    {_how_it_ended(s)}" + (f" after {elapsed(took)}" if took is not None else "")
        return None

    def _steps(self, got: dict) -> None:
        """One read of the build's steps: what began, what it printed and what ended since the last read, in order."""
        self.stages = [s for s in got["stages"] if isinstance(s, dict)]
        lines = sorted((ln for ln in got.get("lines") or [] if isinstance(ln, dict) and isinstance(ln.get("seq"), int)
                        and ln["seq"] > self._seq), key=lambda ln: ln["seq"])
        if lines:
            self._seq = lines[-1]["seq"]
        running = None
        for i, s in enumerate(self.stages):
            name, state = s.get("stage"), s.get("state")
            was = self._said.get(name)
            if state in (None, "pending") or (state == "skipped" and was is None and not s.get("summary")):
                continue
            if was is None and state in _ENDED and i < self._furthest:



                self._said[name] = state
                continue
            if state == "skipped":
                if was is None:
                    self._print(f"  · {_STAGE_SHORT.get(name, name)}: {s['summary']}")
                    self._furthest = max(self._furthest, i)
                    self._open = name
                self._said[name] = state
                continue
            if was is None:
                self._print(f"  · {self._label(s)}{self._usual(s)}")
                self._shown.add(name)
                self._furthest = max(self._furthest, i)
                self._open = name
            if was in _ENDED and name in self._shown and name != "upload":




                said = str(s.get("summary") or "")
                late = [str(ln.get("line") or "") for ln in lines if ln.get("stage") == name]
                late = [text for text in late if text and text not in said]
                if late:
                    self._again(name)
                    for text in late:
                        self._line(name, text)
            if was not in _ENDED:





                said = str(s.get("summary") or "")
                for ln in lines:
                    text = str(ln.get("line") or "")
                    if ln.get("stage") == name and name != "upload" and not (text and text in said):
                        self._line(name, text)
                if state in _ENDED:
                    end = self._end(s)
                    if end:



                        self._print(end if self._open == name else f"    {_STAGE_SHORT.get(name, name)} {end.strip()}")
            if state == "running":
                running = s
            if state == "failed":
                self.failed = s
            self._said[name] = state

        self._running = running
        self._now = got.get("now") if isinstance(got.get("now"), (int, float)) else time.time()
        if isinstance(got.get("summary"), dict):
            self.summary = got["summary"]

    def _draw_live(self) -> None:
        """On a terminal, the running step's time so far, on a line of its own the next line said takes the place of."""
        s = self._running
        if s is None or not self._live or not isinstance(s.get("started_at"), (int, float)):
            return
        self._out.write(f"\r\x1b[K  … {self._label(s)} · {elapsed(self._now - s['started_at'])}")
        self._out.flush()
        self._status_on = True

    def __call__(self, resp: Any) -> None:
        state = resp.status.value
        try:
            from seq.deployments_cli import _call



            query = f"?after_seq={self._seq}" if self.stages is not None else ""
            got = _call("GET", f"/v1/deployments/{segment(self._target)}/build{query}",
                        self._base_url or os.environ.get("SEQUENCES_BASE_URL"))
        except Exception:
            got = None
        if isinstance(got, dict):
            self._steps(got)
        if state != self._state:
            self._state = state
            if state == "failed" and self.failed is not None:

                step = self.failed.get("stage")
                self._print(f"  {resp.model}: {_how_it_ended(self.failed)} in its {_STAGE_SHORT.get(step, step)} step")
            else:
                self._print(status_text(resp))
        if state == "building":
            self._draw_live()

    def steps_line(self) -> str | None:
        """Each step's time at the end of a ready build, in order: "steps: upload 1 s · image 11 s · weights: no
        weights · card 2 s ..." - None before its steps were read."""
        if not self.stages:
            return None
        said = []
        for s in self.stages:
            name, state = s.get("stage"), s.get("state")
            short = _STAGE_SHORT.get(name, name)
            if state in ("done", "reused") and s.get("duration_s") is not None:
                said.append(f"{short} {elapsed(s['duration_s'])}" + (" (reused)" if state == "reused" else ""))
            elif state == "skipped" and s.get("summary"):
                said.append(f"{short}: {s['summary']}")
        return "steps: " + " · ".join(said) if said else None

    def failure(self, name: str, fallback: str | None) -> tuple[str, str | None] | None:
        """(what failed, its hint) for the step the build failed in, said once: its message, its last lines and the
        platform's hint where it is sure of one - None where no step failed with its words. A last line this view said
        under its step is not said again: where each one was, the failure says they are above.
"""
        if self.failed is None or not isinstance(self.failed.get("error"), dict):
            return None
        err, step = self.failed["error"], self.failed.get("stage")
        short = _STAGE_SHORT.get(step, step)
        text = f"its {short} step failed: {err.get('message') or fallback or 'no reason reported'}"
        lines = [str(ln.get("line")) for ln in err.get("last_lines") or [] if isinstance(ln, dict)]
        unsaid = [line for line in lines if line not in self._printed.get(step, set())]
        whole = f"all of it: seq policy logs {name} --build"
        if unsaid:
            some = " not shown above" if len(unsaid) < len(lines) else ""
            text += f"\n  its last lines{some} ({whole}):\n" + "\n".join(f"    {line}" for line in unsaid)
        elif lines:
            text += f"\n  its last lines are above ({whole})"
        return text, err.get("hint")


def _cmd_build_log(target: str, base_url: str | None, *, as_json: bool = False, version: int | None = None) -> int:
    """`seq policy logs <name>[@vN] --build`: the newest version's build, or version N's — its steps: each with its
    state, its time and what it did, every line under its step, the failed one's words and hint.
"""
    from seq._observe_gateway import read



    query = f"?version={int(version)}" if version is not None else ""
    got = read(f"/v1/deployments/{segment(target)}/build{query}", base_url)
    if as_json:
        _print_json(got)
        return 0
    _print_steps(got)
    return 0


_MARKS = {"done": "✓", "reused": "↺", "failed": "✗", "running": "…", "skipped": "-"}


def _print_steps(got: dict) -> None:
    """A build step by step, as `seq policy logs --build` prints it: each step with its state, its time (and what such a step usually takes, from this deployment's own builds), what it did, its
    lines under it with when each was printed, and the failed one's words and hint."""
    failed = got.get("failed_stage")
    print(f"{got['deployment']} v{got['version']}: {got['state']}"
          + (f" — failed in its {_STAGE_SHORT.get(failed, failed)} step" if failed else ""))
    by_step: dict = {}
    for ln in got.get("lines") or []:
        if isinstance(ln, dict):
            by_step.setdefault(ln.get("stage"), []).append(ln)
    named = set()
    for s in got["stages"]:
        name, state = s.get("stage"), s.get("state")
        named.add(name)
        if state == "pending" or (state == "skipped" and not s.get("summary")):
            continue
        took = elapsed(s["duration_s"]) if isinstance(s.get("duration_s"), (int, float)) else ""
        usual = f" (usually {elapsed(s['typical_s'])})" if isinstance(s.get("typical_s"), (int, float)) else ""
        print(f"  {_MARKS.get(state, '?')} {_STAGE_SHORT.get(name, name):<12}{took:>10}{usual}  "
              f"{s.get('summary') or ''}".rstrip())
        for ln in by_step.get(name, []):
            print(f"      {stamp(ln.get('ts'), unit='second')}  {ln.get('line')}")
        if state == "failed" and isinstance(s.get("error"), dict):
            if s["error"].get("message"):
                print(f"    failed: {s['error']['message']}")
            if s["error"].get("hint"):
                print(f"    hint: {s['error']['hint']}")
    for ln in [ln for step, lns in by_step.items() if step not in named for ln in lns]:
        print(f"      {stamp(ln.get('ts'), unit='second')}  {ln.get('line')}")


def _how_it_ended(step: dict) -> str:
    """How a step that did not finish ended, as its own error says it: stopped, at the time its deploy gave it, or failed.
    WHY its own: the build's state is read apart from its steps, so a step can be read ended while the state still says
    building. {dev 11-06, w9t_pol3_user: "failed after 1 min 35 s", then "stopped in its image step"}"""
    error = step.get("error") if isinstance(step.get("error"), dict) else {}
    return "stopped" if str(error.get("message") or "").startswith(TIME_LIMIT.removeprefix(CANCELED)) else "failed"


def status_text(resp: Any) -> str:
    """The line for an observed build state — the transition the user watches (building → ready | failed)."""
    if resp.status.value == "failed" and canceled(resp.error):
        return f"  {resp.model}: canceled — {resp.error.removeprefix(CANCELED)}"
    if resp.status.value == "failed":
        return f"  {resp.model}: failed — {resp.error or 'no reason reported'}"
    return f"  {resp.model}: {resp.status.value}"


def _live(line: str) -> None:
    """A status line, flushed: on a pipe too it appears as the wait goes on."""
    print(line, flush=True)




_KEPT_READ_EVERY_S = 1.0
_KEPT_READS = 2


def _check_machine_kept(name: str, base_url: str | None, fleet: dict | None) -> bool | None:
    """Whether the machine the version's check ran on stays on as its first worker, as the fleet lists it: running, its
    newest event the take-over's boot and not
    leaving for a newer version. A version checked on a sandbox that is ended after it (a CPU policy, a worker of
    several cards, before seq-control keeps one) has none - nor one whose take-over failed. None where the fleet cannot
    be read: nothing is said then.

"""
    for read in range(_KEPT_READS + 1):
        if read:
            time.sleep(_KEPT_READ_EVERY_S)
            fleet = _fleet_now(name, base_url)
        if fleet is None:
            return None
        if any(isinstance(w, dict) and w.get("state") == "running" and w.get("reason") == "first-worker"
               and w.get("leaving") != "version" for w in fleet.get("workers") or []):
            return True
    return False


def _fleet_now(name: str, base_url: str | None) -> dict | None:
    """The deployment's fleet view, read without printing it - None in the mock tier or where it cannot be read: a
    deploy or a status never fails over it."""
    from seq import capacity_cli
    from sequence_ai._core.mock_gate import is_mock

    base = base_url or os.environ.get("SEQUENCES_BASE_URL")
    if base and is_mock(base):
        return None
    try:
        return capacity_cli.fleet(name, base_url=base)
    except SequencesError:
        return None


def _fleet_view(name: str, base_url: str | None, *, echo: Callable[[str], Any] | None = None,
                warn: Callable[[str], Any] | None = None) -> dict | None:
    """The deployment's fleet, said through `echo` when there is one; None in the mock tier or where it cannot be read
    (said through `warn`) - a status never fails over it."""
    from seq import capacity_cli
    from sequence_ai._core.mock_gate import is_mock

    if base_url and is_mock(base_url):
        return None
    try:
        return capacity_cli.fleet(name, base_url=base_url, echo=echo if echo is not None else capacity_cli._silent)
    except SequencesError as exc:
        if warn is not None:
            warn(f"fleet: unavailable — {exc}")
        return None


def _tier_suffix(base_url: str | None) -> str:
    """The global `--base-url` for a follow-up hint, so a staging submit tells the user to poll the same place."""
    b = base_url or os.environ.get("SEQUENCES_BASE_URL")
    return f" --base-url {b}" if b else ""
