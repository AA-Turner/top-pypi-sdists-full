"""per-run tokens for a job on another machine: probe run token, and the hand-off token probe exec mints."""

from __future__ import annotations
import re
import sys
from typing import Any

import typer

from .... import errors
from probe.cli.commands.refs import run_ref
from probe.cli.commands.runs.runs import run_app


def _job_token_env(minted: dict | None, why_not: str | None) -> dict[str, str] | None:
    """PROBE_TOKEN for the launched process: the run's own token when one was
    minted; EMPTY when one was asked for and the mint failed on a server that
    has them (fail closed: never the researcher's key in a job); unchanged when
    none was asked for, or the server predates them (the old hand-off)."""
    if minted is not None:
        return {"PROBE_TOKEN": minted["token"]}
    if why_not is not None and why_not != _NO_RUN_TOKENS:
        return {"PROBE_TOKEN": ""}
    return None


def _predates_run_tokens(exc: Exception) -> bool:
    """A 404 from a server with no per-run token routes (FastAPI's unmatched
    route answers exactly `Not Found`), not a run that does not exist."""
    detail = getattr(exc, "detail", None)
    return detail == "Not Found" or (detail is None and "Not Found" in str(exc))


def _mint_handoff_token(c: Any, run_id: str, ttl_seconds: int | None) -> tuple[dict | None, str | None]:
    """A per-run token for a hand-off's job, or (None, why) when there is none:
    a server older than per-run tokens, or a refusal. Never raises -- the run is
    already open, and the old forwarding still works."""
    try:
        return c.mint_run_token(run_id, ttl_seconds=ttl_seconds), None
    except errors.NotFoundError as exc:
        return None, _NO_RUN_TOKENS if _predates_run_tokens(exc) else f"no per-run token: {exc}"
    except errors.RosError as exc:
        return None, f"no per-run token: {exc}"


_DURATION_RE = re.compile(r"^\s*(\d+)\s*([smhdw]?)\s*$", re.IGNORECASE)
_DURATION_UNIT_S = {"": 1, "s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}


def _parse_duration(text: str) -> int:
    """`36h`, `7d`, `2w`, `90m`, `3600s` or bare seconds -> seconds (BadParameter otherwise)."""
    m = _DURATION_RE.match(str(text))
    if not m or int(m.group(1)) <= 0:
        raise typer.BadParameter(f"{text!r} is not a duration: use e.g. 36h, 7d, 2w")
    return int(m.group(1)) * _DURATION_UNIT_S[m.group(2).lower()]


def _when(iso: str | None) -> str:
    """An ISO time as `YYYY-MM-DD HH:MM UTC`, or the raw text."""
    from datetime import datetime, timezone

    try:
        at = datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return str(iso)
    return at.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


_NO_RUN_TOKENS = (
    "this Probe server predates per-run tokens: give the job a token from "
    "`probe token create --name <job> --scope read --scope write` instead"
)


@run_app.command("token")
def run_token(
    run: str = run_ref(),
    ttl: str = typer.Option(
        None,
        "--ttl",
        help="mint: how long the token lives, e.g. 36h, 7d, 2w (the run's expected length plus margin; default 30d)",
    ),
    extend: str = typer.Option(
        None,
        "--extend",
        help="move the expiry of every token of this run to now + this, e.g. 7d; the running job keeps its token",
    ),
    revoke_all: bool = typer.Option(False, "--revoke-all", help="stop every token minted for this run"),
    show: bool = typer.Option(False, "--show", help="print when this run's tokens expire (never a token)"),
) -> None:
    """Mint a token that records THIS run only, for a job on another machine.

    The token goes to stdout alone, so `export PROBE_TOKEN=$(probe run token my-run --ttl 7d)`
    works. Put it in the job's environment as PROBE_TOKEN: the job's `probe.init()` joins this
    run with it, and the token can read or write nothing else (no other run, no project, no
    new run). It is safe in a plain job spec or env file. `probe exec --detached-launcher`
    mints one for you. Its life is set here and lives on the server: when Probe alerts that a
    live run's token is close to expiring, `--extend 7d` moves it and the job keeps running.
    """
    chosen = [flag for flag, on in (("--ttl", ttl is not None), ("--extend", extend is not None),
                                    ("--revoke-all", revoke_all), ("--show", show)) if on]
    if len(chosen) > 1:
        raise typer.BadParameter(f"choose one of --ttl, --extend, --revoke-all, --show (got {', '.join(chosen)})")
    with _client() as c:
        try:
            if extend is not None:
                state = c.extend_run_tokens(run, ttl_seconds=_parse_duration(extend))
                print(f"run {run}: its tokens now expire {_when(state.get('expires_at'))}", file=sys.stderr)
                return
            if revoke_all:
                c.revoke_run_tokens(run)
                print(f"run {run}: every token minted so far is revoked", file=sys.stderr)
                return
            if show:
                state = c.run_token_state(run)
                print(f"run {run}: tokens expire {_when(state.get('expires_at'))} (generation {state.get('gen')})")
                return
            minted = c.mint_run_token(run, ttl_seconds=_parse_duration(ttl) if ttl else None)
        except errors.NotFoundError as exc:
            if "no tokens" in str(exc):
                raise typer.BadParameter(f"run {run} has no tokens yet: mint one with `probe run token {run}`") from exc
            print(f"probe: {_NO_RUN_TOKENS if _predates_run_tokens(exc) else exc}", file=sys.stderr)
            raise typer.Exit(1) from exc
    print(minted["token"])
    print(
        f"probe: token for run {run}: records this run only, expires {_when(minted.get('expires_at'))}"
        + ("" if ttl else " (default 30 days; set --ttl to the run's expected length plus margin)"),
        file=sys.stderr,
    )
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
