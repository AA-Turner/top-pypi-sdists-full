import os
from pathlib import Path
from uuid import uuid4

import anyio
import structlog
import typer
from rich.console import Console

from runlayer_cli.api import RunlayerClient, SkillScanResponse
from runlayer_cli.console import print_error
from runlayer_cli.config import (
    AI_WATCH_MDM_ORG_KEY_LABEL,
    resolve_credentials,
    resolve_skill_sync_secret,
    set_credentials_in_context,
)
from runlayer_cli.logging import setup_logging
from runlayer_cli.mdm_config import read_managed_config, resolve_sync_skills
from runlayer_cli.symbols import OK
from runlayer_cli.commands.interactive_find import (
    confirm_install,
    format_choice,
    prompt_clients,
    prompt_items,
    prompt_scope,
)
from runlayer_cli.skills.discovery import discover_skills
from runlayer_cli.skills.models import DiscoveredSkill
from runlayer_cli.skills.scan_summary import (
    FailOn,
    ScannedSkill,
    emit_scan_summary,
    exit_code,
    render_scan_results,
    should_fail,
)
from runlayer_cli.skills.installer import (
    SKILLS_DIR_MAP,
    InstallResult,
    UpdateResult,
    read_lockfile,
    install_skills,
    resolve_dirs,
    uninstall_skill,
    update_skills,
)
from runlayer_cli.skills.sync_engine import SyncResult, sync_skills

logger = structlog.get_logger(__name__)
console = Console()

app = typer.Typer(help="Manage skills")


@app.callback(invoke_without_command=True)
def skills_callback(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


def _resolve_client(client_name: str | None) -> str:
    if client_name:
        if client_name not in SKILLS_DIR_MAP:
            typer.secho(
                f"Unsupported client: {client_name}. "
                f"Supported: {', '.join(SKILLS_DIR_MAP)}",
                fg=typer.colors.RED,
                err=True,
            )
            raise typer.Exit(1)
        return client_name
    return "claude_code"


def _load_skills(path: str) -> list[DiscoveredSkill]:
    target = Path(path).resolve()
    if not target.exists():
        raise ValueError(f"Path does not exist: {target}")

    if target.is_file():
        if target.name.lower() != "skill.md":
            raise ValueError("Pass a skill dir or SKILL.md path")
        root = target.parent
    else:
        root = target

    skills = discover_skills(root)
    if not skills:
        raise ValueError(f"No skill found under {root}")
    return skills


def _scan_skill(
    client: RunlayerClient, skill: DiscoveredSkill, scan_id: str
) -> SkillScanResponse:
    response = client.score_skill(
        skill_name=skill.name,
        scan_id=scan_id,
        files=[
            {
                "name": file.title,
                "content": file.content,
            }
            for file in skill.files
        ],
    )
    if not response.scan_id:
        response = response.model_copy(update={"scan_id": scan_id})
    return response


def _override_skill_name(skill: DiscoveredSkill, name: str) -> DiscoveredSkill:
    return DiscoveredSkill(
        path=skill.path,
        name=name,
        description=skill.description,
        files=skill.files,
    )


@app.command()
def push(
    ctx: typer.Context,
    path: str = typer.Argument(".", help="Root directory"),
    namespace: str = typer.Option(
        ..., "--namespace", "-N", help="Namespace for matching skills on the server"
    ),
    public: bool = typer.Option(False, "--public"),
    secret: str | None = typer.Option(
        None, "--secret", "-s", envvar="RUNLAYER_API_KEY"
    ),
    host: str | None = typer.Option(None, "--host", "-H", envvar="RUNLAYER_HOST"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
    prune: bool = typer.Option(
        False, "--prune", help="Remove skills from API whose directories were removed"
    ),
) -> None:
    """Push skills to Runlayer API."""
    root = Path(path).resolve()

    log_file_path = setup_logging(command="skills-push", quiet_console=False)

    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, require_auth=True)

    try:
        client = RunlayerClient(
            hostname=credentials["host"], secret=credentials["secret"]
        )

        def on_progress(skill_path: str, status: str) -> None:
            typer.echo(f"  {skill_path}: {status}")

        async def _run() -> SyncResult:
            return await sync_skills(
                root,
                client,
                namespace=namespace,
                is_public=True if public else None,
                dry_run=dry_run,
                prune=prune,
                on_progress=on_progress,
            )

        result = anyio.run(_run)

        if dry_run:
            typer.secho("[dry run] ", fg=typer.colors.YELLOW, nl=False)

        typer.echo(
            f"Sync complete: {result.created} created, "
            f"{result.updated} updated, {result.unchanged} unchanged, "
            f"{result.deleted} deleted"
        )
        if result.errors:
            for err in result.errors:
                typer.secho(f"  Error: {err}", fg=typer.colors.RED, err=True)
            raise typer.Exit(1)

    except typer.Exit:
        raise
    except Exception as e:
        logger.error("push_failed", error=str(e), exc_info=True)
        print_error(str(e), str(log_file_path))
        raise typer.Exit(1)


@app.command()
def scan(
    ctx: typer.Context,
    path: str = typer.Argument(..., help="Skill dir or SKILL.md path"),
    name: str | None = typer.Option(
        None,
        "--name",
        help="Override skill name sent to security scan API",
    ),
    fail_on: FailOn | None = typer.Option(
        None,
        "--fail-on",
        help="Exit non-zero on warn or block result",
    ),
    secret: str | None = typer.Option(
        None, "--secret", "-s", envvar="RUNLAYER_API_KEY"
    ),
    host: str | None = typer.Option(None, "--host", "-H", envvar="RUNLAYER_HOST"),
) -> None:
    """Scan one skill with security scan API."""
    log_file_path = setup_logging(command="skills-scan", quiet_console=False)

    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, require_auth=True, allow_org_key=True)

    try:
        skills = _load_skills(path)
        if name is not None and len(skills) != 1:
            raise ValueError("--name requires a single skill path")
        if name is not None:
            skills[0] = _override_skill_name(skills[0], name)
        client = RunlayerClient(
            hostname=credentials["host"], secret=credentials["secret"]
        )
        scan_id = str(uuid4())
        scanned_skills: list[ScannedSkill] = []
        try:
            for skill in skills:
                scanned_skills.append((skill, _scan_skill(client, skill, scan_id)))
        except Exception:
            # Completed scans are already recorded in Audit Logs under this
            # scan ID, so surface it even when a later skill's scan fails.
            typer.echo(
                f"Scan failed after {len(scanned_skills)} of {len(skills)} skill(s). "
                f"Scan ID: {scan_id}",
                err=True,
            )
            raise
        typer.echo(render_scan_results(scanned_skills))
        scan_failed = any(
            should_fail(result.skill_risk_level, fail_on)
            for _, result in scanned_skills
        )
        emit_scan_summary(scanned_skills, scan_id, fail_on)
        if scan_failed and fail_on is not None:
            raise typer.Exit(exit_code(fail_on))
    except typer.Exit:
        raise
    except Exception as e:
        logger.error("scan_failed", error=str(e), exc_info=True)
        print_error(str(e), str(log_file_path))
        raise typer.Exit(1)


@app.command()
def find(
    ctx: typer.Context,
    secret: str | None = typer.Option(
        None, "--secret", "-s", envvar="RUNLAYER_API_KEY"
    ),
    host: str | None = typer.Option(None, "--host", "-H", envvar="RUNLAYER_HOST"),
) -> None:
    """Find and install one skill from Runlayer API."""
    log_file_path = setup_logging(command="skills-find", quiet_console=False)

    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, require_auth=True)

    try:
        api = RunlayerClient(hostname=credentials["host"], secret=credentials["secret"])
        with console.status("Loading skills..."):
            skills = sorted(
                api.list_skills(filter="all"),
                key=lambda skill: (skill.name.lower(), (skill.namespace or "").lower()),
            )
        selected_skills = prompt_items(
            skills,
            noun="skills",
            format_item=lambda skill: format_choice(skill),
        )
        resolved_clients = prompt_clients(list(SKILLS_DIR_MAP))
        install_scope = prompt_scope()
        global_install = install_scope == "global"
        confirm_install(
            item_count=len(selected_skills),
            client_count=len(resolved_clients),
            item_label="skill(s)",
        )

        async def _run() -> InstallResult:
            combined = InstallResult()
            for resolved_client in resolved_clients:
                canonical, editor, lockfile = resolve_dirs(
                    resolved_client, global_install, Path.cwd()
                )

                def on_progress(name: str, status: str) -> None:
                    typer.echo(f"  {resolved_client} / {name}: {status}")

                for selected_skill in selected_skills:
                    result = await install_skills(
                        client=api,
                        source=selected_skill.id,
                        install_all=False,
                        skill_name=None,
                        canonical_dir=canonical,
                        editor_dir=editor,
                        lockfile_path=lockfile,
                        client_name=resolved_client,
                        install_scope=install_scope,
                        dry_run=False,
                        on_progress=on_progress,
                    )
                    combined.installed.extend(result.installed)
                    combined.skipped.extend(result.skipped)
                    combined.errors.extend(result.errors)
            return combined

        result = anyio.run(_run)
        parts = []
        if result.installed:
            parts.append(f"{len(result.installed)} installed")
        if result.skipped:
            parts.append(f"{len(result.skipped)} skipped")
        typer.echo(f"Done: {', '.join(parts) if parts else 'nothing to do'}")

        if result.errors:
            for err in result.errors:
                typer.secho(f"  Error: {err}", fg=typer.colors.RED, err=True)
            raise typer.Exit(1)
    except typer.Exit:
        raise
    except Exception as e:
        logger.error("find_failed", error=str(e), exc_info=True)
        print_error(str(e), str(log_file_path))
        raise typer.Exit(1)


@app.command(name="list")
def list_skills(
    client_name: str | None = typer.Option(
        None, "--client", "-c", help="Target editor client"
    ),
    global_install: bool = typer.Option(
        False, "--global", "-g", help="List global skills"
    ),
) -> None:
    """List installed skills."""
    log_file_path = setup_logging(command="skills-list", quiet_console=False)
    resolved_client = _resolve_client(client_name)
    _, _, lockfile = resolve_dirs(resolved_client, global_install, Path.cwd())
    try:
        entries = [e for e in read_lockfile(lockfile) if e.client == resolved_client]

        if not entries:
            typer.echo("No skills installed.")
            raise typer.Exit(0)

        for e in entries:
            line = f"  {e.name}"
            if e.namespace:
                line += f"  ({e.namespace})"
            typer.echo(line)

        typer.echo(f"\n{len(entries)} skill(s) installed")
    except typer.Exit:
        raise
    except Exception as e:
        logger.error("list_failed", error=str(e), exc_info=True)
        print_error(str(e), str(log_file_path))
        raise typer.Exit(1)


@app.command()
def add(
    ctx: typer.Context,
    source: str | None = typer.Argument(
        None, help="Skill UUID or namespace (e.g. Org/Repo)"
    ),
    install_all: bool = typer.Option(
        False, "--all", help="Install all accessible skills across namespaces"
    ),
    skill: str | None = typer.Option(
        None, "--skill", help="Filter by skill name within namespace"
    ),
    client_name: str | None = typer.Option(
        None, "--client", "-c", help="Target editor client"
    ),
    global_install: bool = typer.Option(
        False, "--global", "-g", help="Install globally"
    ),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
    secret: str | None = typer.Option(
        None, "--secret", "-s", envvar="RUNLAYER_API_KEY"
    ),
    host: str | None = typer.Option(None, "--host", "-H", envvar="RUNLAYER_HOST"),
) -> None:
    """Add skills from Runlayer API."""
    if install_all and source is not None:
        typer.secho(
            "Pass either SOURCE or --all, not both.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)
    if not install_all and source is None:
        typer.secho(
            "Missing argument 'SOURCE'. Use SOURCE or --all.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)

    log_file_path = setup_logging(command="skills-add", quiet_console=False)

    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, require_auth=not dry_run)

    resolved_client = _resolve_client(client_name)
    canonical, editor, lockfile = resolve_dirs(
        resolved_client, global_install, Path.cwd()
    )

    try:
        api = RunlayerClient(hostname=credentials["host"], secret=credentials["secret"])

        def on_progress(name: str, status: str) -> None:
            typer.echo(f"  {name}: {status}")

        async def _run() -> InstallResult:
            return await install_skills(
                client=api,
                source=source,
                install_all=install_all,
                skill_name=skill,
                canonical_dir=canonical,
                editor_dir=editor,
                lockfile_path=lockfile,
                client_name=resolved_client,
                install_scope="global" if global_install else "project",
                dry_run=dry_run,
                on_progress=on_progress,
            )

        result = anyio.run(_run)

        if dry_run:
            typer.secho("[dry run] ", fg=typer.colors.YELLOW, nl=False)

        parts = []
        if result.installed:
            parts.append(f"{len(result.installed)} installed")
        if result.skipped:
            parts.append(f"{len(result.skipped)} skipped")
        typer.echo(f"Done: {', '.join(parts) if parts else 'nothing to do'}")

        if result.errors:
            for err in result.errors:
                typer.secho(f"  Error: {err}", fg=typer.colors.RED, err=True)
            raise typer.Exit(1)

    except typer.Exit:
        raise
    except Exception as e:
        logger.error("add_failed", error=str(e), exc_info=True)
        print_error(str(e), str(log_file_path))
        raise typer.Exit(1)


@app.command()
def remove(
    name: str | None = typer.Argument(None, help="Skill name to remove"),
    remove_all: bool = typer.Option(False, "--all", help="Remove all installed skills"),
    yes: bool = typer.Option(False, "--yes", help="Skip confirmation prompt"),
    client_name: str | None = typer.Option(
        None, "--client", "-c", help="Target editor client"
    ),
    global_install: bool = typer.Option(
        False, "--global", "-g", help="Uninstall from global skills"
    ),
) -> None:
    """Remove an installed skill."""
    log_file_path = setup_logging(command="skills-remove", quiet_console=False)
    if remove_all and name is not None:
        typer.secho(
            "Pass either SKILL_NAME or --all, not both.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)
    if not remove_all and name is None:
        typer.secho(
            "Missing argument 'SKILL_NAME'. Use SKILL_NAME or --all.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)

    try:
        resolved_client = _resolve_client(client_name)
        canonical, editor, lockfile = resolve_dirs(
            resolved_client, global_install, Path.cwd()
        )

        if remove_all:
            entries = [
                e for e in read_lockfile(lockfile) if e.client == resolved_client
            ]
            if not entries:
                typer.echo("No skills installed.")
                raise typer.Exit(0)

            names = list(dict.fromkeys(e.name for e in entries))
            if not yes:
                scope = "global" if global_install else "project"
                confirmed = typer.confirm(
                    f"Remove {len(names)} skill(s) from {scope} install?", default=False
                )
                if not confirmed:
                    typer.echo("Aborted.")
                    raise typer.Exit(0)

            async def _run_all() -> list[str]:
                errors: list[str] = []
                for target_name in names:
                    try:
                        await uninstall_skill(
                            target_name,
                            canonical,
                            editor,
                            lockfile,
                            resolved_client,
                        )
                    except Exception as e:
                        errors.append(f"{target_name}: {e}")
                return errors

            errors = anyio.run(_run_all)
            removed_count = len(names) - len(errors)
            typer.echo(f"Done: {removed_count} removed")
            if errors:
                for err in errors:
                    typer.secho(f"  Error: {err}", fg=typer.colors.RED, err=True)
                raise typer.Exit(1)
            return

        assert name is not None

        async def _run() -> None:
            await uninstall_skill(name, canonical, editor, lockfile, resolved_client)

        anyio.run(_run)
        typer.echo(f"Removed: {name}")

    except typer.Exit:
        raise
    except ValueError as e:
        if remove_all:
            logger.error("remove_failed", error=str(e), exc_info=True)
            print_error(str(e), str(log_file_path))
            raise typer.Exit(1)
        typer.secho(str(e), fg=typer.colors.RED, err=True)
        raise typer.Exit(1)
    except Exception as e:
        logger.error("remove_failed", error=str(e), exc_info=True)
        print_error(str(e), str(log_file_path))
        raise typer.Exit(1)


def _privileged_sync_context() -> bool:
    """Root (POSIX) or SYSTEM (Windows) — skill sync writes user homes only.

    Anything written from these contexts would be root/SYSTEM-owned inside a
    user's home, so the reconciler refuses instead of degrading.
    """
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        return True
    from runlayer_cli.scan.windows_users import is_windows_system_context  # noqa: PLC0415

    return is_windows_system_context()


@app.command()
def sync(
    ctx: typer.Context,
    secret: str | None = typer.Option(
        None,
        "--secret",
        "-s",
        envvar="RUNLAYER_API_KEY",
        help="API secret for authentication",
    ),
    host: str | None = typer.Option(
        None,
        "--host",
        "-H",
        envvar="RUNLAYER_HOST",
        help="Runlayer host URL (required if not in config)",
    ),
    username: str | None = typer.Option(
        None,
        "--username",
        envvar="RUNLAYER_USERNAME",
        help="Override detected username (e.g., for MDM deployments)",
    ),
    quiet: bool = typer.Option(
        False,
        "--quiet",
        "-q",
        help="Suppress all output except errors",
    ),
) -> None:
    """Reconcile locally installed managed skills against the backend manifest."""
    log_file_path = setup_logging(command="skills-sync", quiet_console=quiet)

    if _privileged_sync_context():
        if not quiet:
            typer.echo(
                "Skill sync manages per-user skill directories; "
                "run it as the target user, not root/SYSTEM."
            )
        raise typer.Exit(0)

    managed = read_managed_config()
    if not resolve_sync_skills(managed):
        if not quiet:
            typer.echo("Skill sync is disabled by managed configuration.")
        raise typer.Exit(0)

    set_credentials_in_context(ctx, secret, host)
    # require_auth=False: a fleet may push ONLY SkillSyncOrgApiKey (no
    # OrgApiKey, no user login), so the general credential resolution is
    # allowed to come back empty — host resolution (CLI arg > config > MDM
    # managed host) still happens here, and the dedicated key is consulted
    # before we hard-fail. Matches the scheduled twin's semantics.
    credentials = resolve_credentials(
        ctx,
        require_auth=False,
        allow_org_key=True,
        implicit_org_key_label=AI_WATCH_MDM_ORG_KEY_LABEL,
        interactive_login_on_missing=False,
    )

    # `from ... import` here would break the scan-path lazy-import contract;
    # keep parity with commands/scan.py's deferred device imports.
    from runlayer_cli.scan.device import get_or_create_device_id  # noqa: PLC0415

    # Explicit --secret/env wins — RUNLAYER_API_KEY deliberately outranks the
    # MDM SkillSyncOrgApiKey, matching the repo-wide env-beats-managed-config
    # scan contract. Then the dedicated skill-sync key (MDM
    # SkillSyncOrgApiKey / RUNLAYER_SKILL_SYNC_API_KEY), then whatever
    # resolve_credentials found (managed OrgApiKey / stored user secret).
    sync_secret = (
        secret
        or resolve_skill_sync_secret(credentials["host"])
        or credentials["secret"]
    )
    if not sync_secret:
        typer.secho(
            "Error: No credentials found. Provide --secret, push an MDM "
            "SkillSyncOrgApiKey/OrgApiKey, or run 'runlayer login'.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)
    client = RunlayerClient(hostname=credentials["host"], secret=sync_secret)
    effective_username = username or managed.get("username")

    try:
        from runlayer_cli.skills.device_sync import sync_assigned_skills  # noqa: PLC0415

        report = sync_assigned_skills(
            client,
            username=effective_username,
            device_id=get_or_create_device_id(),
        )
    except Exception as e:
        logger.error("skills_sync_failed", error=str(e), exc_info=True)
        print_error(str(e), str(log_file_path))
        raise typer.Exit(1)

    if report is None:
        # Keep-state: unresolved identity or backend unreachable. Silent exit 0
        # so launchd/scheduled runs never flap on transient failures.
        logger.info("skills_sync_kept_state")
        if not quiet:
            typer.echo(
                "Skill sync skipped (identity unresolved or backend unavailable)."
            )
        raise typer.Exit(0)

    # Best-effort check-in mirroring the scan-tick path (device context built
    # from local metadata; the manual command has no scan result, so tools=[]).
    from runlayer_cli.aiwatch_checkin import (  # noqa: PLC0415
        _make_device_context,
        _run_isolated,
        submit_skill_sync_checkin,
    )

    _run_isolated(
        "skill_sync",
        lambda: submit_skill_sync_checkin(
            client, ctx=_make_device_context(), tools=[], report=report
        ),
    )

    logger.info(
        "skills_sync_completed",
        installed=len(report.installed),
        updated=len(report.updated),
        removed=len(report.removed),
        restored=len(report.restored),
        up_to_date=len(report.up_to_date),
        skipped=len(report.skipped),
        errors=len(report.errors),
    )
    if not quiet:
        parts = [
            f"{len(report.installed)} installed",
            f"{len(report.updated)} updated",
            f"{len(report.removed)} removed",
            f"{len(report.up_to_date)} up to date",
        ]
        if report.restored:
            parts.append(f"{len(report.restored)} restored")
        if report.skipped:
            parts.append(f"{len(report.skipped)} skipped")
        if report.errors:
            parts.append(f"{len(report.errors)} errors")
            typer.secho(
                f"Skill sync completed with errors: {', '.join(parts)}",
                fg=typer.colors.RED,
            )
        else:
            typer.secho(
                f"{OK} Skill sync complete: {', '.join(parts)}",
                fg=typer.colors.GREEN,
            )
        for line in report.skipped:
            typer.secho(f"  skipped: {line}", fg=typer.colors.YELLOW)
    # --quiet suppresses everything *except* errors.
    for line in report.errors:
        typer.secho(f"  error: {line}", fg=typer.colors.RED, err=True)
    if report.errors:
        raise typer.Exit(1)


@app.command()
def update(
    ctx: typer.Context,
    skill: str | None = typer.Option(
        None, "--skill", help="Update specific skill only"
    ),
    client_name: str | None = typer.Option(
        None, "--client", "-c", help="Target editor client"
    ),
    global_install: bool = typer.Option(
        False, "--global", "-g", help="Update global skills"
    ),
    dry_run: bool = typer.Option(False, "--dry-run", "-n"),
    secret: str | None = typer.Option(
        None, "--secret", "-s", envvar="RUNLAYER_API_KEY"
    ),
    host: str | None = typer.Option(None, "--host", "-H", envvar="RUNLAYER_HOST"),
) -> None:
    """Update installed skills from Runlayer API."""
    log_file_path = setup_logging(command="skills-update", quiet_console=False)

    set_credentials_in_context(ctx, secret, host)
    credentials = resolve_credentials(ctx, require_auth=not dry_run)

    resolved_client = _resolve_client(client_name)
    canonical, editor, lockfile = resolve_dirs(
        resolved_client, global_install, Path.cwd()
    )

    try:
        api = RunlayerClient(hostname=credentials["host"], secret=credentials["secret"])

        def on_progress(name: str, status: str) -> None:
            typer.echo(f"  {name}: {status}")

        async def _run() -> UpdateResult:
            return await update_skills(
                client=api,
                skill_name=skill,
                canonical_dir=canonical,
                editor_dir=editor,
                lockfile_path=lockfile,
                client_name=resolved_client,
                dry_run=dry_run,
                on_progress=on_progress,
            )

        result = anyio.run(_run)

        if dry_run:
            typer.secho("[dry run] ", fg=typer.colors.YELLOW, nl=False)

        parts = []
        if result.updated:
            parts.append(f"{len(result.updated)} updated")
        if result.up_to_date:
            parts.append(f"{len(result.up_to_date)} up to date")
        if result.removed:
            parts.append(f"{len(result.removed)} removed")
        typer.echo(f"Done: {', '.join(parts) if parts else 'nothing to do'}")

        if result.errors:
            for err in result.errors:
                typer.secho(f"  Error: {err}", fg=typer.colors.RED, err=True)
            raise typer.Exit(1)

    except typer.Exit:
        raise
    except Exception as e:
        logger.error("update_failed", error=str(e), exc_info=True)
        print_error(str(e), str(log_file_path))
        raise typer.Exit(1)
