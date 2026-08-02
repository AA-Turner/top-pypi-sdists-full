"""Resolve env vars via AWS Secrets Manager and other strategies.

Exposed as ``pysae-ai-tools env resolve``. Values are produced by trying, in
order: the current process environment, then the auto-strategies declared in
:mod:`pysae_ai_tools.env.config` (AWS Secrets Manager, shell command, …).

This module is the orchestration + CLI layer: it walks each variable's resolver
chain, warms the AWS secret preload cache, applies the per-environment name
mapping and the project whitelist, and builds the eval-safe click command. The
per-kind resolution logic lives on the resolver dataclasses
(:mod:`pysae_ai_tools.env.config`); shell-syntax formatting in
:mod:`pysae_ai_tools.env.shell_format`; the progress trace in
:mod:`pysae_ai_tools.env.trace`.
"""

import contextlib
import json
import os
import shlex
from collections.abc import Iterable
from enum import StrEnum
from typing import Annotated, NoReturn

import click
import typer

from . import cache, shell_format, trace
from .config import ENV_CONFIG, get_manual_instructions


def try_auto_resolve(var: str, *, use_cache: bool = True) -> str | None:
    """Try each configured resolver in order — first non-empty value wins.

    When ``spec.cache`` is True and ``use_cache`` is True, the on-disk cache
    (``~/.config/pysae-ai-tools/env-cache.json``) is checked first, and a
    successful resolution is persisted back for the next call. For other
    vars, the cache is consulted only as a last-resort fallback after every
    resolver fails — this lets ``tools configure`` persist values the user
    typed manually without hiding upstream rotations from auto-resolution.
    """
    spec = ENV_CONFIG.get(var)
    if spec is None:
        return None

    trace.header(var)

    if spec.cache and use_cache:
        if (cached := cache.read(var)) is not None:
            os.environ[var] = cached
            trace.success("from cache")
            for unused in spec.resolvers:
                trace.skipped_fallback(trace.expand_label(unused.display_label))
            return cached

    for idx, resolver in enumerate(spec.resolvers):
        if (value := resolver.run(var)) is not None:
            if spec.cache:
                cache.write(var, value)
            for unused in spec.resolvers[idx + 1 :]:
                trace.skipped_fallback(trace.expand_label(unused.display_label))
            return value

    if use_cache and not spec.cache:
        if (cached := cache.read(var)) is not None:
            os.environ[var] = cached
            trace.success("from cache")
            return cached
    return None


def peek(var: str) -> str | None:
    """Resolve ``var`` for comparison only — no ``os.environ`` mutation, no
    cache write, no trace output.

    Runs the same resolver chain as :func:`try_auto_resolve` but leaves global
    state untouched, so a read-only caller (e.g. a status check detecting an
    upstream secret rotation) can compare the live value against a stored one
    without side effects. Interactive resolvers (browser auth, credential
    prompts) self-skip because the silenced trace reads as non-interactive.
    Returns the resolved value, or ``None`` when nothing resolves.
    """
    spec = ENV_CONFIG.get(var)
    if spec is None:
        return None
    saved = os.environ.get(var)
    try:
        with trace.silence_trace():
            for resolver in spec.resolvers:
                if (value := resolver.run(var)) is not None:
                    return value
        return None
    finally:
        if saved is None:
            os.environ.pop(var, None)
        else:
            os.environ[var] = saved


def collect_secret_ids(names: Iterable[str]) -> set[str]:
    """AWS secret ids that resolving ``names`` would fetch.

    Walks each var's resolver chain and asks every resolver for the secret id it
    would fetch (:meth:`Resolver.secret_id`), so the caller can warm them all in
    one parallel :func:`secret_store.preload`. Best-effort: an id that can't be
    computed yet (e.g. no AWS username) is skipped.
    """
    from . import secret_store

    ids: set[str] = set()
    for name in names:
        spec = ENV_CONFIG.get(name)
        if spec is None:
            continue
        for resolver in spec.resolvers:
            try:
                secret_id = resolver.secret_id()
            except secret_store.SecretError:
                continue
            if secret_id:
                ids.add(secret_id)
    return ids


def preload_secrets(names: Iterable[str]) -> None:
    """Warm the AWS Secrets Manager cache for ``names`` in parallel, tracing progress.

    Collapses the per-variable secret fetches the sequential resolution would do
    into one concurrent batch (same mechanism as ``tools install``). No-op below
    two **distinct** secret ids: a single secret is fetched inline just as fast,
    so parallelism buys nothing. Best-effort — it only warms a cache — and it
    respects the trace-silence flag so it stays quiet in ``--set`` / ``--json`` mode.
    """
    from . import secret_store

    ids = collect_secret_ids(names)
    if len(ids) < 2:
        return
    trace.emit(f"  ⇣ préchargement de {len(ids)} secrets AWS en parallèle…", color=typer.colors.BRIGHT_BLACK)
    secret_store.preload(ids)


def usual_name_map(environment: str) -> dict[str, str]:
    """Map each resolved name to its canonical variable for ``environment``.

    Reads each spec's ``resolved_name`` (defaulting to the variable's own name)
    and ``environment``. Environment-agnostic (``None``) names apply to every
    environment; an environment-specific entry wins over an agnostic one on a
    name collision (e.g. ``ATLAS_PUBLIC_KEY`` → the dev key rather than the org
    one for ``dev``).
    """
    agnostic: dict[str, str] = {}
    specific: dict[str, str] = {}
    for var, spec in ENV_CONFIG.items():
        name = spec.resolved_name or var
        if spec.environment is None:
            agnostic.setdefault(name, var)
        elif spec.environment == environment:
            specific.setdefault(name, var)
    return {**agnostic, **specific}


class Environment(StrEnum):
    """The environments a resolution can target (validated & shown by Typer)."""

    DEV = "dev"
    PROD = "prod"
    TESTING = "testing"
    ALL = "all"


# Shared across every `env` subcommand so the environment is always selected the
# same way: an option (never a positional), accepting -e / --env / --environment.
EnvOption = Annotated[
    Environment,
    typer.Option("--env", "--environment", "-e", help="Environment to target: dev, prod, testing, or all."),
]


def resolution_map(environment: str) -> dict[str, str]:
    """Map ``output_name -> canonical_var`` for a target environment.

    ``dev`` / ``prod`` expose each in-scope variable under its resolved (usual)
    name via :func:`usual_name_map`. ``all`` exposes **every** variable under its
    own original name (no usual-name rewrite, both environments included).
    """
    if environment == "all":
        return {var: var for var in ENV_CONFIG}
    return usual_name_map(environment)


def project_variable_filter(mapping: dict[str, str], *, ignore: bool = False) -> dict[str, str]:
    """Restrict ``mapping`` to the repo's ``env.variables`` whitelist.

    The whitelist (from ``.pysae-ai-tools.yaml`` found upwards from the cwd, bounded
    by the git repo) matches on **resolved_name**, so ``["MONGO_URI"]`` keeps both
    ``MONGO_URI_DEV`` and ``MONGO_URI_PROD`` under ``--env all``. No-op when ``ignore``
    is set or the whitelist is ``null`` (load everything); an empty whitelist yields an
    empty mapping (load nothing).
    """
    if ignore:
        return mapping
    from pathlib import Path

    from ..common.project_config import configured_env_variables

    allowed = configured_env_variables(Path.cwd())
    if allowed is None:
        return mapping
    allowset = set(allowed)
    kept: dict[str, str] = {}
    for name, var in mapping.items():
        spec = ENV_CONFIG.get(var)
        resolved = (spec.resolved_name or var) if spec else var
        if resolved in allowset:
            kept[name] = var
    return kept


ACTIVATE_BACKUP_VAR = "PYSAE_ENV_ACTIVATE_BACKUP"
"""Env var where ``env activate`` records the pre-activation snapshot (JSON:
``{name: old_value | null}``) so ``env deactivate`` can restore or unset each var."""


def _eval_safe_failure(message: str) -> None:
    """Emit a shell snippet on stdout that re-raises a failure in the caller's shell.

    The whole point of ``--set`` is to be consumed by ``eval "$(… )"``. When the
    command fails, plain stderr is not enough: callers routinely write
    ``eval "$(pysae-ai-tools env resolve --set … 2>/dev/null)"``, so the error
    on stderr is swallowed and the empty stdout makes ``eval ""`` a silent no-op
    — the variables just stay unset. Writing ``echo <msg> >&2; false`` to stdout
    means the eval, running in the live shell, re-prints the message to the
    shell's (unredirected) stderr and returns non-zero, turning the silent
    failure into a loud one.

    Only emitted when stdout is **not** a TTY (i.e. captured by ``$(…)`` or a
    pipe). On an interactive terminal the human already sees the stderr message,
    and printing shell code would just be noise.
    """
    if trace.is_tty():
        return
    typer.echo(f"echo {shlex.quote('pysae-ai-tools env resolve: ' + message)} >&2; false")


def _die(message: str, *, code: int, eval_safe: bool) -> NoReturn:
    """Report an error on stderr (and eval-safe on stdout when set-mode) then exit."""
    typer.echo(message, err=True)
    if eval_safe:
        _eval_safe_failure(message)
    raise typer.Exit(code=code)


def resolve(
    vars: Annotated[
        list[str] | None,
        typer.Argument(
            help=(
                "Env var name(s) to resolve. Supports aliasing via "
                "`OUT=SRC` — e.g. `DATADOG_API_KEY=DD_API_KEY` resolves "
                "DD_API_KEY and emits it under DATADOG_API_KEY."
            ),
        ),
    ] = None,
    environment: EnvOption = Environment.DEV,
    json_output: Annotated[bool, typer.Option("--json", help="JSON output: {VAR: value, …}")] = False,
    set_mode: Annotated[
        bool,
        typer.Option(
            "--set",
            "--export",
            help=(
                "Emit shell-compatible assignment lines (auto-detected). Safe for "
                '`eval "$(…)"` (posix), `| Invoke-Expression` (powershell), or '
                "`for /f` loops (cmd). Combine with `--shell` to override the format. "
                "`--export` is an accepted alias."
            ),
        ),
    ] = False,
    shell: Annotated[
        str | None,
        typer.Option(
            "--shell",
            help="Force the output shell format: `posix`, `powershell`, or `cmd`. Implies `--set`.",
        ),
    ] = None,
    no_cache: Annotated[
        bool,
        typer.Option(
            "--no-cache",
            help="Bypass the on-disk cache — force the resolver chain to run and overwrite any cached value.",
        ),
    ] = False,
    clear_cache: Annotated[
        bool,
        typer.Option(
            "--clear-cache",
            help="Clear cached entries (for the listed VARs, or the whole cache when none are given) and exit.",
        ),
    ] = False,
) -> None:
    """Resolve env vars via AWS Secrets Manager and other strategies.

    Tries the configured auto-resolve strategies (AWS Secrets Manager / shell / …) for each
    variable. Values already present in the environment are kept as-is.

    Every named variable must resolve or the command exits 1. To load a
    project's whole environment into the shell, use `env activate` / `env
    dotenv` (which honour the project whitelist) instead.
    """
    emit_set_lines = set_mode or shell is not None

    if json_output and emit_set_lines:
        _die("--json and --set/--shell are mutually exclusive", code=2, eval_safe=emit_set_lines)

    if shell is not None and shell not in shell_format.VALID_SHELLS:
        _die(f"--shell: invalid value {shell!r} (expected posix|powershell|cmd)", code=2, eval_safe=emit_set_lines)

    resolved_shell = shell or (shell_format.detect_shell() if emit_set_lines else None)

    if clear_cache:
        if not vars:
            cache.clear(None)
            typer.echo("cache cleared", err=True)
            return
        for spec in vars:
            target, _, _ = spec.partition("=")
            cache.clear(target)
        typer.echo(f"cache cleared for: {', '.join(v.partition('=')[0] for v in vars)}", err=True)
        return

    # output_name → canonical var for this environment (e.g. MONGO_URI → MONGO_URI_DEV;
    # `all` keeps each variable's original name). Agnostic names apply to every env.
    name_map = resolution_map(environment)

    if not vars:
        _die("usage: resolve <VAR>...", code=2, eval_safe=emit_set_lines)
    # Parse each spec into (output_name, source_name). Plain "VAR" → both equal.
    # A usual name maps to the environment's canonical var; unknown names pass through.
    pairs: list[tuple[str, str]] = []
    for spec in vars:
        out, sep, src = spec.partition("=")
        src = src if sep else out
        pairs.append((out, name_map.get(src, src)))

    # ``--set`` / ``--shell`` and ``--json`` both require pristine stdout
    # (shell-syntax assignments or a JSON payload), so the resolver's trace
    # lines are suppressed entirely. Failures are reported on stderr (always)
    # and, in ``--set`` mode with a captured stdout, mirrored as an eval-safe
    # snippet on stdout (see ``_eval_safe_failure``) so a swallowed stderr does
    # not turn into a silent ``eval ""``.
    quiet_stdout = emit_set_lines or json_output
    silence: contextlib.AbstractContextManager[object] = (
        trace.silence_trace() if quiet_stdout else contextlib.nullcontext()
    )

    resolved: dict[str, str] = {}
    missing: list[str] = []
    with silence:
        preload_secrets(src for _, src in pairs)
        for out, src in pairs:
            value = os.environ.get(src) or try_auto_resolve(src, use_cache=not no_cache)
            if value:
                resolved[out] = value
            else:
                missing.append(src)

    if missing:
        typer.echo(f"Could not resolve: {', '.join(missing)}", err=True)
        for var_name in missing:
            if hint := get_manual_instructions(var_name):
                typer.echo(f"  {var_name}: {hint}", err=True)
        if emit_set_lines:
            _eval_safe_failure(f"could not resolve: {', '.join(missing)}")
        raise typer.Exit(code=1)

    # Every var resolved (missing → exit above); emit in request order.
    emit = [(out, resolved[out]) for out, _ in pairs]

    if json_output:
        typer.echo(json.dumps(dict(emit)))
    elif resolved_shell is not None:
        typer.echo(shell_format.set_mode_hint(resolved_shell))
        for out, value in emit:
            typer.echo(shell_format.format_set_line(resolved_shell, out, value))
    else:
        for _, value in emit:
            typer.echo(value)


def _intercept_usage_errors(command: click.Command) -> click.Command:
    """Wrap a command's ``parse_args`` so option/usage errors are eval-safe.

    Click rejects an unknown option (e.g. ``--export`` mistyped for ``--set``)
    during ``parse_args`` — before our code runs — printing to stderr and
    leaving stdout empty. Under ``eval "$(… 2>/dev/null)"`` that is a silent
    no-op. We catch the :class:`click.UsageError`, mirror it as an eval-safe
    snippet on stdout (unless ``--json`` was requested, which is not eval-fed),
    then re-raise so Click still reports it on stderr and exits non-zero.
    """
    original_parse = command.parse_args

    def parse_args(ctx: click.Context, args: list[str]) -> list[str]:
        # Click mutates ``args`` in place as it consumes tokens, so snapshot the
        # original to reliably detect a JSON request even after a parse error.
        original_args = list(args)
        try:
            return original_parse(ctx, args)
        except click.UsageError as exc:
            if "--json" not in original_args:
                _eval_safe_failure(exc.format_message())
            raise

    command.parse_args = parse_args  # type: ignore[method-assign]
    return command


def _build_command() -> click.Command:
    """Build the click command for ``resolve`` with eval-safe error handling."""
    typer_app = typer.Typer(add_completion=False)
    typer_app.command()(resolve)
    command = typer.main.get_command(typer_app)
    if isinstance(command, click.Group) and len(command.commands) == 1:
        command = next(iter(command.commands.values()))
    return _intercept_usage_errors(command)


# Exposed as the CLI leaf (registered in __main__.py as `env resolve`).
app = _build_command()


if __name__ == "__main__":
    app()
