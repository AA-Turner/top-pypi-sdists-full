"""
The gateway client for remote benchmarks and evals: register a benchmark and wait for its sim image to
build, then evaluate a deployed model on it and wait for the report.

    POST /v1/benchmarks  → 202 building           GET /v1/benchmarks/{name} → building | ready | failed (+ error)
    POST /v1/eval        → {eval_id, estimate}    GET /v1/eval/{id}         → EvalReport: [queued →] running →
                           (+ queue when short)                                completed | failed
    GET /v1/eval/{id}/details → manifest, means, episodes; while queued, `queue` {cards, available,
                                waited_s, gives_up_at}

Nothing runs locally: the gateway builds the benchmark's image from its declaration and source, and the eval runs
the benchmark's code against the deployed policy on the platform. The API key is a Bearer credential only — never
in a body, a log line, or an error message.
"""
from __future__ import annotations

import os
import re
import time
from typing import Any, Callable

from sequence_base.contract import BenchmarkRegisterRequest, BenchmarkStatusResponse, DeploymentState, EvalReport

from seq._account import auth_headers, credential
from seq.errors import raise_for, unreachable
from sequence_ai._core.names import segment
from sequence_ai.errors import InvalidRequest, SequencesError, Unavailable

DEFAULT_BASE_URL = "https://api.generalsequences.com"
_TIMEOUT_S = 60.0



BENCHMARK_WAIT_S = 3600.0





BUILD_MOVED_S = 600.0
BUILD_MORE_S = 1800.0
BENCHMARK_WAIT_MAX_S = 3 * 3600.0
EVAL_WAIT_S = 2 * 3600.0
POLL_S = 10.0




RETRY_FOR_S = 300.0
RETRY_FIRST_S = 5.0
RETRY_MAX_S = 60.0




EVAL_TERMINAL = _EVAL_TERMINAL = ("completed", "failed", "canceled")


def _page(limit: int, cursor: str | None) -> dict:
    """A list call's paging, as the gateway takes it: `limit` rows from the opaque `cursor` it handed out last page."""
    return {"limit": limit, **({"cursor": cursor} if cursor else {})}


def _episode_filters(task: str | list[str] | None, outcome: str | None, arm: int | None) -> dict:
    """Which of an eval's episodes, as its page and its CSV file take them: `task` repeated (task=a&task=b)."""
    out: dict[str, Any] = {"task": [task] if isinstance(task, str) else list(task)} if task else {}
    return {**out, **{k: v for k, v in (("outcome", outcome), ("arm", arm)) if v is not None}}


class Registered(BenchmarkStatusResponse):
    """A registration's 202 as this sequence-ai read it: the contract's fields, and beside them the adapters registered
    with it in the account (the X-Adapters-Registered header) - none for a benchmark that is no template's."""

    adapters: list[str] = []


class EvalGatewayClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None, *, transport: Any = None) -> None:
        self._base = (base_url or os.environ.get("SEQUENCES_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        self._key = credential(api_key, self._base)
        self._transport = transport

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        return self._get(method, path, timeout=_TIMEOUT_S, **kwargs).json()

    def _get(self, method: str, path: str, *, timeout: float, **kwargs: Any) -> Any:
        """One call to this client's own gateway: the answer, or the exception the one mapping makes of it."""
        import httpx

        from seq._http import RetryReads

        try:

            with httpx.Client(base_url=self._base, timeout=timeout, transport=RetryReads(self._transport),
                              headers=auth_headers(self._key)) as c:
                r = c.request(method, path, **kwargs)
        except httpx.TransportError as exc:
            raise unreachable(self._base, exc) from None
        raise_for(r)
        return r


    def register(self, request: BenchmarkRegisterRequest, *, override: bool = False,
                 time_limit_s: float | None = None) -> Registered:
        """POST /v1/benchmarks: every earlier version is kept - or, `override` (seq deploy --override), the one evals run
        now is deleted once this one has passed its check. `time_limit_s` (--timeout): how long this registration may
        run, the platform stopping it then."""

        from seq._deploy_gateway import _params, adapters_of

        r = self._get("POST", "/v1/benchmarks", timeout=_TIMEOUT_S, content=request.model_dump_json(exclude_none=True),
                      headers={"Content-Type": "application/json"}, params=_params(override, time_limit_s))
        return Registered(**BenchmarkStatusResponse.model_validate(r.json()).model_dump(), adapters=adapters_of(r))

    def validate(self, path: str, **kwargs: Any) -> dict | None:
        """POST to the platform's own check of a registration, with nothing registered or built - /v1/benchmarks/validate
        or /v1/adapters/validate, which `seq deploy --dry-run` asks: its refusal raised as the registration's is (the one
        mapping, so the same error and exit code), its answer on acceptance {"ok", "name", "state", "version",
        "contract"}; None when it cannot be asked: no answer (offline).
        
"""
        import httpx

        from seq._http import RetryReads

        try:
            with httpx.Client(base_url=self._base, timeout=_TIMEOUT_S, transport=RetryReads(self._transport),
                              headers=auth_headers(self._key)) as c:
                r = c.post(path, **kwargs)
        except httpx.TransportError:
            return None
        raise_for(r)
        try:
            return dict(r.json())
        except Exception:
            return None

    def benchmark(self, name: str) -> BenchmarkStatusResponse:
        return BenchmarkStatusResponse.model_validate(self._request("GET", f"/v1/benchmarks/{segment(name)}"))

    def benchmarks(self, *, limit: int = 50, cursor: str | None = None) -> dict:
        """Your benchmarks, newest first, one page: {"benchmarks": [...], "total": N, "next_cursor": ...}."""
        return self._request("GET", "/v1/benchmarks", params=_page(limit, cursor))

    def delete_benchmark(self, name: str, *, dry_run: bool = False, force: bool = False) -> dict:
        """DELETE /v1/benchmarks/{name}: deleted for good, at once (its name and quota place free); with `dry_run`, only
        what it would touch; `force` cancels the evals running on it (refused 409 otherwise)."""
        params = {k: "true" for k, on in (("dry_run", dry_run), ("force", force)) if on}
        return self._request("DELETE", f"/v1/benchmarks/{segment(name)}", params=params or None)

    def delete_benchmark_version(self, name: str, version: int, *, dry_run: bool = False) -> dict:
        """DELETE /v1/benchmarks/{name}/versions/{version}: that version deleted for good, the benchmark and its other
        versions staying - {benchmark, version, dry_run, state: "deleting" (a kept one, once no eval runs it) |
        "deleted" (a failed one)}; its latest, and the one evals run while the latest is out, are refused (409)."""
        return self._request("DELETE", f"/v1/benchmarks/{segment(name)}/versions/{int(version)}",
                             params={"dry_run": "true"} if dry_run else None)

    def cancel_benchmark(self, name: str) -> dict:
        """POST /v1/benchmarks/{name}/cancel: its registration in flight stopped - {name, version, status "canceled",
        runs: the version an eval runs, None when none passed its check}; 409 when none is running."""
        return self._request("POST", f"/v1/benchmarks/{segment(name)}/cancel")

    def benchmark_logs(self, name: str, *, version: int | None = None) -> dict:
        """GET /v1/benchmarks/{name}/logs: a version's build as it reported itself — phases, log, the check's verdict."""
        return self._request("GET", f"/v1/benchmarks/{segment(name)}/logs",
                             params={"version": version} if version is not None else None)

    def eval_logs(self, eval_id: str, *, side: str | None = None, arm: int | None = None,
                  machine: str | None = None, after: int | None = None, before: int | None = None,
                  limit: int = 500) -> dict:
        """GET /v1/eval/{id}/logs: the eval's lines (the newest `limit`, the `limit` before the `before` cursor - a page's
        `older` - or every one after the `after` cursor), each naming the machine it came from (`machine_name`);
        `machine` keeps one machine's."""
        params = {"limit": limit, **({"side": side} if side else {}), **({"arm": arm} if arm is not None else {}),
                  **({"machine": machine} if machine else {}), **({"after": after} if after is not None else {}),
                  **({"before": before} if before is not None else {})}
        return self._request("GET", f"/v1/eval/{segment(eval_id)}/logs", params=params)

    def benchmark_evals(self, name: str, *, policy: str | None = None, since: str | None = None, limit: int = 50,
                        cursor: str | None = None) -> dict:
        """Every eval run on benchmark `name` across your policies (or one, `policy`), newest first, one page:
        {"benchmark": name, "evals": [...], "total": N, "next_cursor": ...}. `since` is an ISO date or time."""
        params = {**_page(limit, cursor), **({"policy": policy} if policy else {}), **({"since": since} if since else {})}
        return self._request("GET", f"/v1/benchmarks/{segment(name)}/evals", params=params)

    def wait_benchmark(self, name: str, *, timeout_s: float = BENCHMARK_WAIT_S, poll_s: float = POLL_S,
                       on_poll: Callable[[BenchmarkStatusResponse], None] | None = None,
                       on_retry: Callable[[SequencesError, float], None] | None = None,
                       while_moving: bool = False, on_more: Callable[[float], None] | None = None,
                       on_stall: Callable[[float], None] | None = None,
                       sleep: Callable[[float], None] = time.sleep,
                       now: Callable[[], float] = time.monotonic) -> BenchmarkStatusResponse:
        """Poll until the build is ready or failed, or `timeout_s` passes (then the last, still-building status; `math.inf`
        for no window: a build ends, at the latest at the platform's own limit). A platform it cannot reach is asked again
        for RETRY_FOR_S (see `patiently`). `while_moving`: a build whose log
        moved in the last BUILD_MOVED_S before the deadline is waited on BUILD_MORE_S more, up to BENCHMARK_WAIT_MAX_S
        in all, `on_more(waited_s)` hearing each time; one whose log stood still those last minutes ends the
        wait, `on_stall(waited_s)` hearing it, so the caller says why it ended rather than as a wait run out."""
        ask = lambda: self.patiently(lambda: self.benchmark(name), on_retry=on_retry, sleep=sleep, now=now,
                                     going_on=f"the build of {name} goes on on the platform",
                                     hint=f"seq benchmark status {name} --wait")
        start = now()
        deadline = start + timeout_s
        mark = None
        last = ask()
        while True:
            if on_poll is not None:
                on_poll(last)
            if last.status != DeploymentState.BUILDING:
                return last
            t = now()
            if while_moving and mark is None and t >= deadline - BUILD_MOVED_S:
                mark = self._log_mark(name)
            if t >= deadline:
                fresh = self._log_mark(name) if while_moving else None
                if fresh is not None and mark is not None and fresh == mark and on_stall is not None:
                    on_stall(t - start)
                if fresh is None or mark is None or fresh == mark or t - start >= BENCHMARK_WAIT_MAX_S:
                    return last

                deadline, mark = min(start + BENCHMARK_WAIT_MAX_S, t + BUILD_MORE_S), None
                if on_more is not None:
                    on_more(t - start)
            sleep(poll_s)
            last = ask()

    def _log_mark(self, name: str) -> tuple | None:
        """How far the latest build's log has got, to tell a build that moves from one that stalled: when its newest
        line was printed (`lines`' ts), how many phases it has been through, and its length; None when it cannot be
        read.

        WHY the newest line's time: the platform keeps a log's newest 400 lines, so once it has that many each line in
        pushes one out, and lines of one width - a progress bar's - leave its length where it was: a build still moving
        read as stalled and ended its wait at the hour.
 """
        try:
            logs = self.benchmark_logs(name)
        except SequencesError:
            return None
        newest = max((float(line.get("ts") or 0) for line in logs.get("lines") or [] if isinstance(line, dict)),
                     default=None)
        return newest, len(logs.get("phases") or []), len(logs.get("log") or "")


    def start_eval(self, body: dict) -> dict:
        """POST /v1/eval → {eval_id, gpus_granted, estimate} — plus `queue` when the account was short of GPUs and the
        eval waits in line — or, with dry_run, the estimate with its layout and `cards`."""
        return self._request("POST", "/v1/eval", json={k: v for k, v in body.items() if v is not None})

    def cancel(self, eval_id: str) -> dict:
        """POST /v1/eval/{id}/cancel: {eval_id, status} — "canceling" while the machines stop, "canceled" once done."""
        return self._request("POST", f"/v1/eval/{segment(eval_id)}/cancel")

    def report(self, eval_id: str) -> EvalReport:
        return report_of(self._request("GET", f"/v1/eval/{segment(eval_id)}"))

    def details(self, eval_id: str) -> dict:
        """GET /v1/eval/{id}/details → {manifest, means, episodes, episodes_total, ...}."""
        return self._request("GET", f"/v1/eval/{segment(eval_id)}/details")

    def eval_episodes(self, eval_id: str, *, task: str | list[str] | None = None, outcome: str | None = None,
                      arm: int | None = None, limit: int = 50, cursor: str | None = None) -> dict:
        """GET /v1/eval/{id}/episodes: one page of an eval's episodes - a running eval's, as far as they have reported
        - only those of `task` (one or several), of `outcome` (success / failure / error / truncated / timed_out; a
        success as the benchmark's @seq.step said of the episode's last step) and of `arm`:
        {eval_id, episodes: [as /details has them], total, offset, next_cursor}.
        """
        params = {**_page(limit, cursor), **_episode_filters(task, outcome, arm)}
        return self._request("GET", f"/v1/eval/{segment(eval_id)}/episodes", params=params)

    def episodes_csv(self, eval_id: str, *, task: str | list[str] | None = None, outcome: str | None = None,
                     arm: int | None = None) -> str:
        """GET /v1/eval/{id}/episodes.csv: an eval's episodes - every one, or those of `task`, `outcome` and `arm` as a
        page takes them - as the one CSV file the console downloads too, a row per episode, its cells guarded against
        spreadsheet formulas."""
        return self._get("GET", f"/v1/eval/{segment(eval_id)}/episodes.csv", timeout=120.0,
                         params=_episode_filters(task, outcome, arm)).text

    def all_episodes(self, eval_id: str, details: dict) -> list[dict]:
        """Every episode of an eval: /details' own when they are all there, else every page of /episodes (200 a page)
        when its `episodes_total` says there are more - /details gives the first 5000.
"""
        given = list(details["episodes"])
        if details["episodes_total"] <= len(given):
            return given
        out: list[dict] = []
        cursor = None
        while True:
            page = self.eval_episodes(eval_id, limit=200, cursor=cursor)
            out.extend(page.get("episodes") or [])
            cursor = page.get("next_cursor")
            if not cursor:
                return out

    def open_machines(self) -> list[dict]:
        """The account's machines open beside its workers and evals' (GET /v1/machines: its benchmarks' shells, and machines
        checking a version on a VM), each what it is for, its version and card, when its card's first second was and what
        it still waits on."""
        return list((self._request("GET", "/v1/machines") or {}).get("data") or [])

    def benchmark_tasks(self, name: str, *, version: int | None = None) -> dict:
        """GET /v1/benchmarks/{name}/tasks: a benchmark version's tasks (the current one unless `version`) - each
        task's description, time limit (max_seconds), seeds ("0-49") and episodes - with the template it comes from,
        its channel and whether it records its 3D replay."""
        return self._request("GET", f"/v1/benchmarks/{segment(name)}/tasks",
                             params={"version": int(version)} if version is not None else None)

    def benchmark_io(self, name: str) -> dict:
        """GET /v1/benchmarks/{name}/io: what the latest version's simulation hands an adapter and takes back - the
        observation its registration check read (its keys, each one's shape and dtype), the observation contract it
        declared, and the templates it is made from."""
        return self._request("GET", f"/v1/benchmarks/{segment(name)}/io")

    def record(self, eval_id: str, index: int) -> bytes:
        """One episode's record - what its policy was sent, its cameras as video, and each answer: a zstd frame of
        msgpack entries - from this client's own gateway, the path built
        here, never taken from a response.
"""
        if not re.fullmatch(r"[0-9A-Za-z_-]+", eval_id) or int(index) < 0:
            raise InvalidRequest(f"not an eval episode: {eval_id!r} #{index}")
        return self._get("GET", f"/v1/eval/{segment(eval_id)}/episodes/{int(index)}/record", timeout=300.0).content

    def replay(self, eval_id: str, index: int) -> bytes:
        """One episode's 3D replay (a .seqreplay file, gzip), from this client's own gateway - the path is built here,
        never taken from a response."""
        if not re.fullmatch(r"[0-9A-Za-z_-]+", eval_id) or int(index) < 0:
            raise InvalidRequest(f"not an eval episode: {eval_id!r} #{index}")
        return self._get("GET", f"/v1/eval/{segment(eval_id)}/replays/{int(index)}", timeout=120.0).content

    def scene(self, eval_id: str, sha256: str) -> bytes:
        """A scene an eval's replays are drawn in (a glTF binary), by the sha256 its episodes name."""
        if not re.fullmatch(r"[0-9A-Za-z_-]+", eval_id) or not re.fullmatch(r"[0-9a-f]{64}", sha256 or ""):
            raise InvalidRequest(f"not an eval's scene: {eval_id!r} {sha256!r}")
        return self._get("GET", f"/v1/eval/{segment(eval_id)}/scenes/{sha256}", timeout=300.0).content

    def wait_report(self, eval_id: str, *, timeout_s: float = EVAL_WAIT_S, poll_s: float = POLL_S,
                    on_poll: Callable[[EvalReport], None] | None = None,
                    on_retry: Callable[[SequencesError, float], None] | None = None,
                    hint: str | None = None, going_on: str | None = None,
                    sleep: Callable[[float], None] = time.sleep,
                    now: Callable[[], float] = time.monotonic) -> EvalReport:
        """Poll until the eval completes or fails, or `timeout_s` passes (then the last, still-running report). A
        platform it cannot reach is asked again for RETRY_FOR_S (see `patiently`); giving up, the error says what goes
        on (`going_on`, default: this eval) and `hint` (default: seq eval report <id> --wait) how to wait again."""
        ask = lambda: self.patiently(lambda: self.report(eval_id), on_retry=on_retry, sleep=sleep, now=now,
                                     going_on=going_on or f"eval {eval_id} goes on running on the platform",
                                     hint=hint or f"seq eval report {eval_id} --wait")
        deadline = now() + timeout_s
        last = ask()
        while True:
            if on_poll is not None:
                on_poll(last)
            if last.status.value in _EVAL_TERMINAL or now() >= deadline:
                return last
            sleep(poll_s)
            last = ask()

    def patiently(self, call: Callable[[], Any], *, going_on: str, hint: str,
                  on_retry: Callable[[SequencesError, float], None] | None = None,
                  sleep: Callable[[float], None] = time.sleep, now: Callable[[], float] = time.monotonic) -> Any:
        """`call()`, asked again while the platform cannot be reached or answers it may be asked again (Unavailable,
        or an error it marks retryable): after RETRY_FIRST_S, doubling to RETRY_MAX_S, for RETRY_FOR_S. Then the last
        error, saying what `going_on` (the run goes on without this wait) and, as its hint, how to wait again.
        `on_retry(error, seconds)` hears each retry. Anything else - not found, not yours - is raised at once."""
        lost, pause = None, RETRY_FIRST_S
        while True:
            try:
                return call()
            except SequencesError as exc:
                if not (isinstance(exc, Unavailable) or exc.retryable):
                    raise
                lost = now() if lost is None else lost
                if now() - lost >= RETRY_FOR_S:
                    raise Unavailable(f"{exc.message}; still so after {(now() - lost) / 60:.0f} min of asking again, "
                                      f"so this wait stops, but {going_on}", code=exc.code, status=exc.status,
                                      request_id=exc.request_id, hint=hint) from exc
                if on_retry is not None:
                    on_retry(exc, pause)
                sleep(pause)
                pause = min(RETRY_MAX_S, pause * 2)


def _known(model: Any, value: Any) -> Any:
    """`value` as `model` reads it: the keys it does not define left out, at every level where a field is a model of its
    own - an arm, a metric's aggregate, a task's - through the lists, maps and optionals that hold them."""
    if not isinstance(value, dict):
        return value
    out = {}
    for name, field in model.model_fields.items():
        key = field.alias or name
        if key in value:
            out[key] = _known_as(field.annotation, value[key])
    return out


def _known_as(annotation: Any, value: Any) -> Any:
    """A field's value pruned as its annotation reads it (_known); a value of any other type as it came."""
    import types
    import typing

    from pydantic import BaseModel

    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return _known(annotation, value)
    origin, args = typing.get_origin(annotation), typing.get_args(annotation)
    if origin in (typing.Union, types.UnionType):
        inner = [a for a in args if a is not type(None)]
        return _known_as(inner[0], value) if len(inner) == 1 and value is not None else value
    if origin is list and args and isinstance(value, list):
        return [_known_as(args[0], v) for v in value]
    if origin is dict and len(args) == 2 and isinstance(value, dict):
        return {k: _known_as(args[1], v) for k, v in value.items()}
    return value


def report_of(body: dict) -> EvalReport:
    """The report, read at the boundary: a failed run's single `error` joins `errors`, and keys the report contract does
    not define (a stored report's `reason`; a key the platform still sends a release behind, or one a newer platform
    adds) are left out, at every level (_known), instead of failing the whole read - so a client released before its
    platform still reads a report
. A
    queued eval that gave up comes back as {"status": "failed", "error": ..., "reason": "queue_timeout", ...} — the
    error is kept, the read never raises.
    `arm_params` that this client's contract cannot read — a parameter source a newer platform added, as "deployment"
    was in sequence-base 0.3.25 — is dropped rather than failing the report: the metrics stay readable, and the report
    prints the eval's own params instead."""
    from pydantic import ValidationError

    b = dict(body or {})
    error = b.pop("error", None)
    if isinstance(error, str) and error:
        b["errors"] = [*(b.get("errors") or []), error]
    known = _known(EvalReport, b)
    try:
        return EvalReport.model_validate(known)
    except ValidationError as exc:
        if known.get("arm_params") is None or any(not e["loc"] or e["loc"][0] != "arm_params" for e in exc.errors()):
            raise
        return EvalReport.model_validate({**known, "arm_params": None})
