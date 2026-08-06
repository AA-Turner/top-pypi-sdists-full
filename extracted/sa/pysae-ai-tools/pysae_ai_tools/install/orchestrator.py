"""Install orchestration for the meta-installer.

The engine behind ``tools install`` / ``configure`` / ``require``: the
two-phase install-then-configure pipeline, env-var resolution and preloading,
tool/system dependency resolution, MCP server teardown, and the headless
classification helpers. Presentation lives in :mod:`render`; the declarative
registry in :mod:`registry`.
"""

import os
import shutil
from dataclasses import dataclass, field
from typing import Any

import typer

from .common.base import Status
from .registry import TOOLS, Category, Tool, _find_tool, _instance


@dataclass
class Result:
    name: str
    status: str  # "installed" | "updated" | "up-to-date" | "skipped" | "failed" | "manually-installed"
    detail: dict[str, Any] = field(default_factory=dict)
    error: str = ""

    def to_dict(self) -> dict[str, object]:
        out: dict[str, object] = {"name": self.name, "status": self.status}
        if self.detail:
            out["detail"] = self.detail
        if self.error:
            out["error"] = self.error
        return out


def _can_ask() -> bool:
    """True when this run may put a question to the user.

    A real terminal is the only condition — the same signal the tool checklist
    uses. There is no flag to opt into being asked: a value the run needs is
    asked for, or the run reports what it could not do. ``CI``, a non-TTY (pipes,
    ``--json`` consumers, pytest) and ``--non-interactive`` all report False, so
    unattended runs never block.
    """
    from .common.checklist import is_interactive

    return is_interactive()


def _ensure_system_deps(module_path: str) -> list[str]:
    """Ensure the tool's declared OS-level dependencies. Returns the names that
    could not be satisfied (each :class:`~common.syspkg.SystemDep` is verified by
    its own probe before and after any package-manager attempt).

    Decoupled from the tool's own installer: the tool only declares
    ``system_deps``; provisioning lives in :mod:`common.syspkg`.
    """
    from .common import syspkg

    deps = _instance(module_path).system_deps
    if not deps:
        return []
    return [name for name, status in syspkg.ensure_all(deps).items() if status in ("missing", "unsupported")]


def uninstall_mcp_servers(*, dry_run: bool = False) -> list[str]:
    """Remove every MCP server that ``tools install`` registers, from each active target
    (Claude's ``~/.claude.json`` and Codex's ``~/.codex/config.toml``).

    Returns the server names present on at least one target (and removed from every target
    where present, unless ``dry_run``). Best-effort: a module that fails to import is skipped.
    """
    from .common.assistants import active_assistants

    assistants = active_assistants()
    removed: list[str] = []
    seen: set[str] = set()
    for tool in TOOLS:
        if tool.category is not Category.MCP:
            continue
        try:
            instance = _instance(tool.module)
        except Exception:  # noqa: BLE001
            continue
        for name in instance.mcp_server_names():
            if name in seen:
                continue
            seen.add(name)
            present = [assistant for assistant in assistants if assistant.mcp.get(name) is not None]
            if not present:
                continue
            if not dry_run:
                for assistant in present:
                    assistant.mcp.remove(name)
            removed.append(name)
    return removed


def _configure_one(tool: Tool, *, dry_run: bool) -> Result:
    """Re-apply a tool's configuration only — no binary install or update.

    Resolves the tool's env vars (auth tokens, MCP keys — the values its
    configuration reads) then runs ``do_configure``. Plain binaries with
    nothing to configure fall through to a grey ``skipped``.
    """
    env = tool.env
    if env.pre:
        from .common.interactive import ensure_env_vars

        if not ensure_env_vars(env.pre, tool.name, env.help, interactive=_can_ask()):
            return Result(name=tool.name, status="skipped", detail={"reason": "missing env vars"})

    _resolve_optional_env(tool)

    instance = _instance(tool.module)

    if dry_run:
        _resolve_post_configure(tool)
        return Result(name=tool.name, status="configured", detail={"dry_run": True})

    try:
        report = instance.do_configure()
    except Exception as exc:  # noqa: BLE001
        return Result(name=tool.name, status="failed", error=str(exc))

    _resolve_post_configure(tool)

    payload = report.to_dict()
    if payload.get("error"):
        return Result(name=tool.name, status="failed", error=str(payload["error"]), detail=payload)
    if report.method == "nothing to configure":
        return Result(name=tool.name, status="skipped", detail={"reason": "nothing to configure"})
    return Result(name=tool.name, status="configured", detail=payload)


def _ensure_tool_deps(
    tool: Tool,
    *,
    dry_run: bool,
    install_only: bool,
) -> Result | None:
    """Install ``tool``'s declared tool dependencies that aren't already on the
    system. Returns a failed :class:`Result` for ``tool`` if a dependency is
    unknown or its install fails, else ``None``.

    Dependencies are always installed binary-first (their configuration, if
    any, is a separate concern); ``install_only`` propagates so a build-time
    run stays binary-only through the whole dependency chain.
    """
    for dep_name in tool.depends:
        dep_tool = _find_tool(dep_name)
        if dep_tool is None:
            return Result(name=tool.name, status="failed", error=f"unknown dependency '{dep_name}'")
        if dep_tool.installed:
            continue
        dep_result = _install_one(dep_tool, dry_run=dry_run, install_only=install_only)
        if dep_result.status == "failed":
            return Result(
                name=tool.name,
                status="failed",
                error=f"dependency '{dep_name}' failed: {dep_result.error}",
            )
    return None


def _install_one(
    tool: Tool,
    *,
    dry_run: bool,
    configure_only: bool = False,
    install_only: bool = False,
) -> Result:
    """Install then configure, with two-phase env handling.

    1. **Pre-configure** — resolve ``tool.env.pre`` *before* installing. Gates
       the install in non-interactive mode (missing → skipped) because the
       values are baked in at install time (e.g. MCP servers writing tokens
       into ``~/.claude.json``).
    2. **Install** — run ``do_install`` (the binary only). Skipped when
       ``get_state`` reports the tool already up-to-date.
    2b. **Configure** — run ``do_configure`` (auth, MCP registration,
       contexts). A concern disjoint from the binary; tools without a binary
       make ``do_install`` a no-op and carry their work here.
    3. **Post-configure** — resolve ``tool.env.post`` *after* the binary is in
       place. Best-effort — missing vars don't fail the install. Used for steps
       that need the binary itself (e.g. ``aws configure`` requires ``aws`` on
       PATH).

    ``configure_only`` runs step 2b alone; ``install_only`` is its mirror —
    step 2 alone, with every configuration phase (1, 2b, 3) skipped. The two
    are mutually exclusive; the CLI rejects passing both.
    """
    if configure_only:
        return _configure_one(tool, dry_run=dry_run)

    try:
        instance = _instance(tool.module)
    except Exception as exc:  # noqa: BLE001
        return Result(name=tool.name, status="failed", error=f"import: {exc}")

    env = tool.env

    # Phase 1 — pre-configure env vars (gates install). Skipped in install-only
    # mode: the values only matter for the configuration we're not running.
    if env.pre and not install_only:
        from .common.interactive import ensure_env_vars

        if not ensure_env_vars(env.pre, tool.name, env.help, interactive=_can_ask()):
            return Result(name=tool.name, status="skipped", detail={"reason": "missing env vars"})

    state_payload: dict[str, Any] = {}
    was_installed = False
    needs_work = True
    needs_binary_work = True
    try:
        state_obj = instance.get_state()
        state_payload = state_obj.to_dict()
        was_installed = state_obj.installed
        needs_work = state_obj.needs_work
        needs_binary_work = state_obj.needs_binary_work
    except Exception:  # noqa: BLE001
        state_payload = {}
    if not needs_work:
        # Binary is up-to-date; still surface post-configure prompts so
        # the user can complete (or update) configuration without
        # reinstalling — unless install-only, where config is off-limits.
        if not install_only:
            _resolve_post_configure(tool)
        return Result(name=tool.name, status="up-to-date", detail=state_payload)
    if not was_installed:
        was_installed = shutil.which(tool.name) is not None

    # Only a reconfigure is pending: the binary is present and current, so this
    # run is a configuration pass and must report itself as one.
    if not needs_binary_work:
        return _configure_one(tool, dry_run=dry_run)

    success_status = "updated" if was_installed else "installed"

    if dry_run:
        return Result(name=tool.name, status=success_status, detail={"dry_run": True, **state_payload})

    # Phase 1b — ensure declared OS-level dependencies before the binary. A tool
    # that declares a dependency it cannot satisfy must not proceed.
    unmet = _ensure_system_deps(tool.module)
    if unmet:
        return Result(
            name=tool.name,
            status="failed",
            error=f"unmet system dependencies: {', '.join(unmet)} — install them and retry",
        )

    # Phase 1c — install declared tool dependencies (other TOOLS this tool's
    # installer needs on PATH). Only the missing ones, so an already-present
    # dependency costs nothing. install_only propagates so a build stays
    # binary-only end to end.
    dep_failure = _ensure_tool_deps(tool, dry_run=dry_run, install_only=install_only)
    if dep_failure is not None:
        return dep_failure

    # Phase 2 — install the binary.
    try:
        report = instance.do_install()
    except Exception as exc:  # noqa: BLE001
        return Result(name=tool.name, status="failed", error=str(exc))

    payload = report.to_dict()
    if payload.get("error"):
        return Result(name=tool.name, status="failed", error=str(payload["error"]), detail=payload)

    # Phase 2b — configure (a concern separate from the binary). Tools without
    # a binary make do_install a no-op and carry their work here, so running
    # both is never double work. Skipped in install-only mode.
    if not install_only:
        # Same offer the configure-only path makes: a value the configuration
        # needs but that must not gate the tool is asked for here too, otherwise
        # `tools install <name>` on a fresh machine installs the binary and then
        # configures nothing for want of a credential it never requested.
        _resolve_optional_env(tool)
        try:
            cfg = instance.do_configure()
        except Exception as exc:  # noqa: BLE001
            return Result(name=tool.name, status="failed", error=str(exc), detail=payload)
        cfg_payload = cfg.to_dict()
        if cfg_payload.get("error"):
            return Result(
                name=tool.name,
                status="failed",
                error=str(cfg_payload["error"]),
                detail=payload,
            )
        report.extra.update(cfg.extra)
        payload = report.to_dict()

    # Phase 3 — post-configure env vars (best-effort, never blocks). Skipped in
    # install-only mode.
    if not install_only:
        _resolve_post_configure(tool)

    return Result(name=tool.name, status=success_status, detail=payload if isinstance(payload, dict) else {})


def _resolve_optional_env(tool: Tool) -> None:
    """Offer the tool's ``env_optional`` vars before its configuration runs.

    ``_configure_one`` only enforces ``env.pre``, which gates the tool when
    missing. A value that must not gate — a credential a tool poses when it has
    one, and reports as skipped when it doesn't — therefore lives in
    ``env.optional``, and nothing on the ``--configure-only`` path used to ask
    for it: the configuration could only ever reuse a value already in the
    environment or the cache, never obtain one.

    Asks whenever the run may ask (:func:`_can_ask`). Answers are persisted, so
    the next run finds them on its own.
    """
    env = tool.env
    if not env.optional:
        return

    from ..env.resolve import try_auto_resolve
    from .common.interactive import prompt_env_var

    for var in env.optional:
        if os.environ.get(var) or try_auto_resolve(var) is not None:
            continue
        if _can_ask():
            prompt_env_var(var, tool.name, env.help.get(var, ""), persist=True)


def _resolve_post_configure(tool: Tool) -> None:
    """Best-effort post-install env var resolution.

    Auto-resolves what it can; asks the user when the terminal can answer.
    Never gates the install — this runs *after* the binary is in place.
    Missing vars at the end are simply left unresolved; the tool's own
    runtime can complain or ask for them later.
    """
    env = tool.env
    if not env.post or all(os.environ.get(v) for v in env.post):
        return
    from .common.interactive import ensure_env_vars

    ensure_env_vars(env.post, tool.name, env.help, interactive=_can_ask())


def install_all(
    *,
    dry_run: bool = False,
    only: tuple[str, ...] = (),
    skip: tuple[str, ...] = (),
    configure_only: bool = False,
    install_only: bool = False,
) -> list[Result]:
    results: list[Result] = []
    for tool in TOOLS:
        if only and tool.name not in only:
            continue
        if tool.name in skip:
            results.append(Result(name=tool.name, status="skipped", detail={"reason": "user-skipped"}))
            continue
        result = _install_one(
            tool,
            dry_run=dry_run,
            configure_only=configure_only,
            install_only=install_only,
        )
        results.append(result)
    return results


def _preload_secrets(names: tuple[str, ...], tools: tuple[Tool, ...]) -> None:
    """Warm the AWS Secrets Manager cache in parallel before resolving vars.

    Collects every secret id the upcoming resolution will touch — from the env
    vars' resolver chains plus each tool's ``secret_ids()`` hook — and fetches
    the distinct ids concurrently. Best-effort: it only warms a cache, so a
    failure here never blocks the install (the individual resolver surfaces the
    error later).
    """
    from ..env import secret_store
    from ..env.resolve import collect_secret_ids

    ids = collect_secret_ids(names)
    for tool in tools:
        try:
            instance = _instance(tool.module)
        except Exception:  # noqa: BLE001
            continue
        try:
            ids |= set(instance.secret_ids())
        except Exception:  # noqa: BLE001
            pass
    if len(ids) < 2:
        return
    typer.secho(f"  ⇣ préchargement de {len(ids)} secrets AWS en parallèle…", fg=typer.colors.BRIGHT_BLACK)
    secret_store.preload(ids)


def _resolve_env_section(tools: tuple[Tool, ...]) -> None:
    """Resolve every env var declared by ``tools`` upfront, in a dedicated section.

    Each distinct var is tried at most once (vars shared across tools are
    deduplicated). Vars already in the environment are left as-is. Auto-resolve
    runs unconditionally; a var left unresolved is asked for whenever the run may
    ask (:func:`_can_ask`) — a terminal is enough, ``-i`` is not required.

    No gating / no skipping happens here — the per-tool install phase
    (``_install_one``) handles ``env.pre`` enforcement using whatever ended up
    in ``os.environ``.
    """
    from ..env.resolve import try_auto_resolve
    from .common.interactive import prompt_env_var
    from .render import SECTION_ENV, _section_header

    seen: dict[str, str] = {}  # var → first tool that declared it (for help-text lookup)
    help_by_var: dict[str, str] = {}
    for tool in tools:
        env = tool.env
        for var in env.all:
            seen.setdefault(var, tool.name)
        for var, hint in env.help.items():
            help_by_var.setdefault(var, hint)

    if not seen:
        return

    # Resolvers that need a human (browser OAuth via ``slack get-token``,
    # ``glab auth login``) decide for themselves through ``env.trace``: they
    # self-skip without a TTY, and ``--non-interactive`` sets that flag globally
    # (see ``checklist.force_non_interactive``). Nothing to scope here.
    _section_header(SECTION_ENV)
    _preload_secrets(tuple(seen), tools)
    for var, tool_name in seen.items():
        if os.environ.get(var):
            # Symmetric with the resolver-trace path: blank line + cyan
            # ``$VAR`` heading + indented green status. The blank line is
            # added by ``try_auto_resolve``'s ``_trace_header`` for the
            # other branch — we mirror it manually here.
            typer.echo("")
            typer.secho(f"  ${var}", fg=typer.colors.CYAN)
            typer.secho("    ✓ déjà défini dans l'environnement", fg=typer.colors.GREEN)
            continue
        if try_auto_resolve(var) is not None:
            continue
        if _can_ask():
            help_text = help_by_var.get(var, "")
            # ``persist=True`` writes the entered value to the on-disk env
            # cache so subsequent runs (when the upstream source — AWS
            # Secrets Manager, glab CLI, etc. — is still down) can reuse
            # it via try_auto_resolve's last-resort cache fallback.
            prompt_env_var(var, tool_name, help_text, persist=True)


def _result_for_unselected(tool: Tool) -> Result:
    """Build a Result for a tool excluded from the selection.

    If the tool happens to be installed already, surface it as
    ``manually-installed`` so the user sees normal output. Otherwise mark it
    grey-skipped.
    """
    try:
        state_obj = _instance(tool.module).get_state()
        if state_obj.installed:
            return Result(name=tool.name, status="manually-installed", detail=state_obj.to_dict())
    except Exception:  # noqa: BLE001
        pass
    return Result(name=tool.name, status="skipped", detail={"reason": "not selected"})


def _install_pretty(
    *,
    skip: tuple[str, ...],
    selection: set[str] | None = None,
    configure_only: bool = False,
    install_only: bool = False,
) -> list[Result]:
    """Run the install pipeline with grouped 'Environment variables' + 'Tools' sections.

    ``selection`` lists tool names the user opted into. Tools outside the set
    are not installed but still rendered (as ``manually-installed`` if
    detected on the system, otherwise as ``skipped``). REQUIRED tools are
    forced into the selection.
    """
    from .registry import CATEGORY_ORDER, Mode, _tools_by_category
    from .render import _category_header, _render_install_result

    if selection is not None:
        selection = set(selection) | {t.name for t in TOOLS if t.mode is Mode.REQUIRED}

    def _is_selected(tool_name: str) -> bool:
        return selection is None or tool_name in selection

    tools_to_run = tuple(t for t in TOOLS if t.name not in skip)
    grouped = _tools_by_category(tools_to_run)

    # Resolve every env var declared by the *selected* tools upfront, in a
    # single dedicated section. Per-tool fallback in ``_install_one``
    # short-circuits because ``os.environ`` is already populated. Skipped in
    # install-only mode: env vars only feed the configuration we won't run.
    selected_tools = tuple(t for t in tools_to_run if _is_selected(t.name))
    if not install_only:
        _resolve_env_section(selected_tools)

    results: list[Result] = []
    for cat in CATEGORY_ORDER:
        bucket = grouped.get(cat) or []
        if not bucket:
            continue
        _category_header(cat)
        for tool in bucket:
            if not _is_selected(tool.name):
                result = _result_for_unselected(tool)
            else:
                result = _install_one(
                    tool,
                    dry_run=False,
                    configure_only=configure_only,
                    install_only=install_only,
                )
            results.append(result)
            _render_install_result(result)
    return results


def _state_dict(tool: Tool) -> dict[str, Any]:
    """Serialize the state of a single tool for JSON output."""
    try:
        d = _instance(tool.module).get_state().to_dict()
        d["name"] = tool.name
        return d
    except Exception as exc:  # noqa: BLE001
        return {"name": tool.name, "error": str(exc)}


def _classify(tool: Tool) -> Status:
    """Return the tool's :data:`Status` — the headless, no-I/O counterpart of
    :func:`render._render_tool_status`. Delegates to :meth:`ToolState.classify`;
    falls back to a bare PATH probe only when ``get_state`` itself raises."""
    try:
        return _instance(tool.module).get_state().classify()
    except Exception:  # noqa: BLE001
        return "installed" if shutil.which(tool.name) is not None else "missing"


def _configure_env_vars(selected_tools: list[Tool]) -> None:
    """Walk env vars for the selected tools and prompt for missing ones.

    Pre-configure vars are walked unconditionally — they're needed before
    install, regardless of whether the binary is on the system yet.

    Post-configure vars are walked only for tools whose binary is already
    installed: configuring them earlier doesn't help (the binary is what
    powers the configuration step, e.g. ``aws configure``), and it would
    fail or lead to half-applied state.
    """
    from ..env.resolve import try_auto_resolve
    from .common.interactive import prompt_env_var

    seen: dict[str, str] = {}  # var → first tool name that needs it
    help_by_var: dict[str, str] = {}
    for tool in selected_tools:
        env = tool.env
        for var in env.pre:
            seen.setdefault(var, tool.name)
        # env_optional — tunables surfaced at configure-time so the user
        # can answer once and forget; never gates the install (handled
        # outside this function).
        for var in env.optional:
            seen.setdefault(var, tool.name)
        if tool.installed:
            for var in env.post:
                seen.setdefault(var, tool.name)
        for var, hint in env.help.items():
            help_by_var.setdefault(var, hint)

    if not seen:
        return

    # Warm every AWS secret the still-unresolved vars touch in one parallel
    # batch before the serial resolution below — same preload the install
    # pipeline uses. Vars already in the environment need no fetch.
    _preload_secrets(tuple(v for v in seen if not os.environ.get(v)), tuple(selected_tools))

    typer.echo("")
    typer.secho("  🔑 Variables d'environnement", fg=typer.colors.CYAN)

    for var, tool_name in seen.items():
        if os.environ.get(var):
            typer.secho(f"  ✓ ${var} (déjà défini)", fg=typer.colors.GREEN)
            continue
        if try_auto_resolve(var) is not None:
            continue
        env_help = help_by_var.get(var, "")
        if prompt_env_var(var, tool_name, env_help, persist=True) is None:
            typer.secho(f"  ⊘ ${var} non renseigné — sera demandé à l'install", fg=typer.colors.BRIGHT_BLACK)
