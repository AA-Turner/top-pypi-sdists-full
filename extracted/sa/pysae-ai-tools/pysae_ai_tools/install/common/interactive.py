"""Interactive env var prompting for install commands.

Env vars can be auto-resolved via shell commands (e.g. reading from AWS
Secrets Manager) or prompted interactively. Auto-resolution logic and
configuration live in :mod:`pysae_ai_tools.env`.
"""

import os
from pathlib import Path

import typer

from ... import config as _config_module
from ...config import ConfigParam, ParamValue, get_param, os_default_clone_dir, set_param
from ...env import cache
from ...env.config import ENV_CONFIG, get_manual_instructions
from ...env.resolve import preload_secrets, try_auto_resolve


def prompt_env_var(var: str, tool_name: str = "", help_text: str = "", *, persist: bool = False) -> str | None:
    """Prompt the user for a missing env var. Returns the value or None if skipped.

    When ``persist`` is True, the value is written to the on-disk env cache
    so subsequent commands (including ``tools install``) can pick it up via
    :func:`pysae_ai_tools.env.resolve.try_auto_resolve`.
    """
    # AWS credentials are owned by ``AwsConfigResolver``: it prompts and
    # persists to ``~/.aws/credentials`` directly, bypassing the env-cache.
    # If we reach here, the resolver already ran (and either succeeded — in
    # which case ``os.environ[var]`` is set and the caller should not have
    # called us — or the user declined). Don't add a second prompt.
    if var in {"AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"}:
        return None

    spec = ENV_CONFIG.get(var)
    resolved_help = help_text or (spec.description if spec else "")
    manual = get_manual_instructions(var)

    typer.echo("")
    typer.secho(f"  ${var} is required{f' for {tool_name}' if tool_name else ''}", fg=typer.colors.YELLOW)
    if resolved_help:
        typer.secho(f"  → {resolved_help}", fg=typer.colors.BRIGHT_BLACK)
    if manual:
        typer.secho(f"    {manual}", fg=typer.colors.BRIGHT_BLACK)

    value: str = typer.prompt(f"  ${var}", default="", show_default=False)
    if not value.strip():
        return None

    cleaned = value.strip()
    os.environ[var] = cleaned
    if persist:
        cache.write(var, cleaned)
    return cleaned


def prompt_config_param(spec: ConfigParam) -> ParamValue:
    """Prompt the user for one config parameter, pre-filling the current value.

    Persists the answer to ``config.toml`` and returns the new value. Hits
    the typer prompt subsystem so an EOF / Ctrl-C is propagated as
    ``typer.Abort``.
    """
    current = get_param(spec.name)
    typer.echo("")
    for line in spec.prompt.splitlines():
        typer.secho(f"  {line}", fg=typer.colors.CYAN)

    if spec.kind == "bool":
        default_bool = bool(current)
        answer = typer.confirm(f"  {spec.name}", default=default_bool)
        set_param(spec.name, bool(answer))
        return bool(answer)

    # path / string — show the resolved current value as default. For
    # ``git_clone_dir``, an empty stored value means "use OS default": we
    # surface the OS default in the prompt but keep the empty string in the
    # file so the existing fallback logic (env var > config > OS default)
    # keeps behaving the same way.
    display_default = str(current)
    if spec.kind == "path" and not display_default and spec.name == "git_clone_dir":
        display_default = str(os_default_clone_dir())

    answer_text: str = typer.prompt(f"  {spec.name}", default=display_default, show_default=True)
    cleaned = answer_text.strip()
    if spec.kind == "path" and cleaned:
        cleaned = str(Path(cleaned).expanduser())
    set_param(spec.name, cleaned)
    return cleaned


def configure_parameters(selected_tool_names: set[str]) -> None:
    """Walk relevant ConfigParams for ``selected_tool_names`` and prompt each.

    Phase 2 of ``tools configure``: runs after the tool checklist and before
    env-var resolution. Skipped silently when there's nothing to ask.
    """
    from ...config import iter_params

    params = list(iter_params(tools_selected=selected_tool_names))
    if not params:
        return

    typer.echo("")
    typer.secho("  ⚙️  Paramètres pysae-ai-tools", fg=typer.colors.CYAN)
    typer.secho(f"  ({_config_module.CONFIG_FILE})", fg=typer.colors.BRIGHT_BLACK)
    for spec in params:
        prompt_config_param(spec)


def ensure_env_vars(
    vars_required: tuple[str, ...],
    tool_name: str = "",
    env_help: dict[str, str] | None = None,
    interactive: bool = True,
) -> bool:
    """Resolve missing env vars: auto-resolve first, then prompt if interactive.

    Returns True if all vars are resolved.
    """
    # Warm every AWS secret the still-unresolved vars touch in one parallel
    # batch, so the per-var resolution below is a cache hit rather than a serial
    # round-trip. Vars already in the environment need no fetch.
    preload_secrets(tuple(v for v in vars_required if not os.environ.get(v)))

    for var in vars_required:
        if os.environ.get(var):
            continue

        # Try auto-resolve (works in both interactive and non-interactive mode)
        if try_auto_resolve(var) is not None:
            continue

        # Prompt only in interactive mode
        if interactive:
            help_text = (env_help or {}).get(var, "")
            if prompt_env_var(var, tool_name, help_text) is not None:
                continue

        typer.secho(f"  ✗ ${var} not set — {tool_name or 'tool'} will not be installed.", fg=typer.colors.RED)
        return False
    return True
