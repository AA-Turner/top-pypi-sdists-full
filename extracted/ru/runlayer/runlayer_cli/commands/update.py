"""User and scheduler entrypoints for backend-authoritative binary updates."""

from __future__ import annotations

import ctypes
from dataclasses import replace
import os
import sys

from click.core import Context as ClickContext
from click.core import ParameterSource
import typer

from runlayer_cli import __version__
from runlayer_cli.config import (
    AI_WATCH_MDM_ORG_KEY_LABEL,
    resolve_credentials,
    set_credentials_in_context,
)
from runlayer_cli.commands.update_privilege import (
    PRIVILEGED_CA_BUNDLE_ENV,
    PRIVILEGED_CA_DIR_ENV,
    PRIVILEGED_HOST_ENV,
    PRIVILEGED_ORG_KEY_ENV,
    configure_privileged_temp_root,
    elevating_runner,
    run_privileged_update,
)
from runlayer_cli.platform_installers import (
    NativePlatformInstaller,
    native_install_target,
)
from runlayer_cli.product import (
    InstalledPackage,
    installed_package,
    package_display_name,
)
from runlayer_cli.tls import (
    REQUESTS_CA_BUNDLE_ENV,
    RUNLAYER_CA_BUNDLE_ENV,
    SSL_CERT_DIR_ENV,
    SSL_CERT_FILE_ENV,
    get_ca_bundle_dir,
    get_ca_bundle_path,
    set_ca_bundle_path,
)
from runlayer_cli.updater import (
    InstallTarget,
    UpdateResult,
    UpdateStatus,
    check_and_update,
)
from runlayer_cli.variant import installed_variant


def _has_explicit_option(ctx: typer.Context, name: str) -> bool:
    current: ClickContext | None = ctx
    supplied = False
    while current is not None and not supplied:
        supplied = current.get_parameter_source(
            name
        ) is ParameterSource.COMMANDLINE and bool(current.params.get(name))
        current = current.parent
    return supplied


def _is_windows_elevated() -> bool:
    if sys.platform != "win32":
        return False
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except (AttributeError, OSError):
        return False


def _installed_package_or_exit() -> InstalledPackage:
    try:
        return installed_package()
    except RuntimeError as exc:
        typer.secho(f"Update failed: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1) from None


def _install_target_for(package: str) -> InstallTarget:
    """Compose the native slot with the installed build variant.

    ALL update entrypoints must build their InstallTarget through this helper:
    a variant-blind InstallTarget on a variant device would silently select
    the standard build. A corrupt marker raises here (fail closed); the sudo
    re-exec continuation re-reads the same root-owned file instead of trusting
    argv/env. The marker must be world-readable (packaging ships it 0644)
    because this read happens pre-sudo as the invoking user; an unreadable
    marker is a fail-closed error.
    """
    return replace(native_install_target(), variant=installed_variant(package))


def _perform_update(
    *,
    package: str,
    host: str,
    org_api_key: str,
    allow_privileged_reexec: bool = True,
    minimum_target_version: str | None = None,
) -> UpdateResult | None:
    target = _install_target_for(package)
    if target.platform == "windows" and not _is_windows_elevated():
        raise RuntimeError(
            "Windows self-update requires an elevated administrator console"
        )
    getuid = getattr(os, "geteuid", None)
    if callable(getuid) and getuid() == 0:
        configure_privileged_temp_root()
    if (
        allow_privileged_reexec
        and getattr(sys, "frozen", False)
        and callable(getuid)
        and getuid() != 0
    ):
        run_privileged_update(
            package=package,
            platform=target.platform,
            host=host,
            org_api_key=org_api_key,
            ca_bundle=get_ca_bundle_path(),
            ca_bundle_dir=get_ca_bundle_dir(),
        )
        return None
    installer = NativePlatformInstaller(
        package,
        target=target,
        runner=elevating_runner,
    )
    return check_and_update(
        package=package,
        installed_version=__version__,
        host=host,
        org_api_key=org_api_key,
        installer=installer,
        install_target=target,
        minimum_target_version=minimum_target_version,
        outcome_marker_path=installer.outcome_marker_path,
    )


def _print_result(result: UpdateResult, *, product: str) -> None:
    if result.status is UpdateStatus.UPDATED:
        typer.echo(
            f"Updated {product} from {result.from_version} to {result.to_version}."
        )
    elif result.status is UpdateStatus.SCHEDULED:
        typer.echo(
            f"Scheduled {product} update from {result.from_version} "
            f"to {result.to_version}."
        )
    elif result.status is UpdateStatus.UP_TO_DATE:
        typer.echo(f"{product} is already at the backend-selected version.")
    elif result.status is UpdateStatus.NO_TARGET:
        typer.echo(f"No {product} update target is available yet.")
    elif result.status is UpdateStatus.TARGET_BELOW_MINIMUM:
        typer.echo(
            f"The backend-selected {product} version is below the managed "
            "auto-update minimum."
        )
    elif result.status is UpdateStatus.NOT_FROZEN:
        typer.secho(
            f"{product} self-update is available only in the packaged binary.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)
    else:
        raise AssertionError(f"Unhandled update status: {result.status}")


def _run_or_exit(
    *,
    package: str,
    product: str,
    host: str,
    org_api_key: str,
    quiet: bool = False,
    allow_privileged_reexec: bool = True,
    minimum_target_version: str | None = None,
) -> None:
    # A native installer can replace this running PyInstaller onedir bundle.
    # Do not lazy-load config/keyring from the mutated archive on Typer's
    # subsequent exit path.
    from runlayer_cli.command_metrics import (  # noqa: PLC0415
        suppress_current_command_metrics,
    )

    suppress_current_command_metrics()
    try:
        result = _perform_update(
            package=package,
            host=host,
            org_api_key=org_api_key,
            allow_privileged_reexec=allow_privileged_reexec,
            minimum_target_version=minimum_target_version,
        )
    except Exception as exc:
        typer.secho(f"Update failed: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(1) from None
    if result is not None and (not quiet or result.status is UpdateStatus.NOT_FROZEN):
        _print_result(result, product=product)


def update(
    ctx: typer.Context,
    secret: str | None = typer.Option(
        None,
        "--secret",
        "-s",
        envvar="RUNLAYER_API_KEY",
        help="Organization API key with the mcp_watch_scan role",
    ),
    host: str | None = typer.Option(
        None,
        "--host",
        "-H",
        envvar="RUNLAYER_HOST",
        help="Runlayer host URL (required if not in config)",
    ),
    org_api_key: str | None = typer.Option(
        None,
        "--org-api-key",
        envvar="RUNLAYER_ORG_API_KEY_NAME",
        help="Name of a stored organization API key with the mcp_watch_scan role",
    ),
) -> None:
    """Install the backend-selected version of the installed Runlayer product."""
    if not getattr(sys, "frozen", False):
        _print_result(
            UpdateResult(
                status=UpdateStatus.NOT_FROZEN,
                from_version=__version__,
            ),
            product="Runlayer CLI",
        )
    package = _installed_package_or_exit()
    product = package_display_name(package)
    explicit_secret = _has_explicit_option(ctx, "secret")
    explicit_host = _has_explicit_option(ctx, "host")
    explicit_org_api_key = _has_explicit_option(ctx, "org_api_key")
    if ctx.get_parameter_source("secret") is ParameterSource.ENVIRONMENT and (
        explicit_secret or explicit_org_api_key
    ):
        secret = None
    if (
        ctx.get_parameter_source("org_api_key") is ParameterSource.ENVIRONMENT
        and explicit_org_api_key
    ):
        org_api_key = None
    if (
        ctx.get_parameter_source("host") is ParameterSource.ENVIRONMENT
        and explicit_host
    ):
        host = None
    set_credentials_in_context(
        ctx,
        secret,
        host,
        org_api_key_name=org_api_key,
    )
    credentials = resolve_credentials(
        ctx,
        require_auth=True,
        allow_org_key=True,
        implicit_org_key_label=AI_WATCH_MDM_ORG_KEY_LABEL,
        interactive_login_on_missing=False,
    )
    resolved_org_api_key = credentials["secret"]
    if not resolved_org_api_key.startswith("rl_org_"):
        typer.secho(
            "runlayer update requires an organization API key with the "
            "mcp_watch_scan role. "
            "Pass --org-api-key <name> or --secret <rl_org_...>.",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(1)
    _run_or_exit(
        package=package,
        product=product,
        host=credentials["host"],
        org_api_key=resolved_org_api_key,
    )


def privileged_update(package: str) -> None:
    """Internal root continuation; never expose credentials as argv values."""
    getuid = getattr(os, "geteuid", None)
    if not callable(getuid) or getuid() != 0:
        typer.secho("Privileged update continuation requires root.", err=True)
        raise typer.Exit(1)
    host = os.environ.pop(PRIVILEGED_HOST_ENV, "")
    org_api_key = os.environ.pop(PRIVILEGED_ORG_KEY_ENV, "")
    ca_bundle = os.environ.pop(PRIVILEGED_CA_BUNDLE_ENV, "")
    ca_bundle_dir = os.environ.pop(PRIVILEGED_CA_DIR_ENV, "")
    # Do not let package verification/install subprocesses inherit a standard
    # credential variable even if the caller's sudo policy supplies one.
    os.environ.pop("RUNLAYER_API_KEY", None)
    if package not in {"cli", "desktop"} or not host or not org_api_key:
        typer.secho(
            "Privileged update continuation has missing or unsupported context.",
            err=True,
        )
        raise typer.Exit(1)
    selected_package = _installed_package_or_exit()
    if package != selected_package:
        typer.secho(
            "Privileged update continuation does not match the installed product.",
            err=True,
        )
        raise typer.Exit(1)
    # Trust only the canonical value handed off by the validated caller, not
    # generic TLS overrides that a sudo policy may inject into the root child.
    for name in (
        RUNLAYER_CA_BUNDLE_ENV,
        SSL_CERT_FILE_ENV,
        SSL_CERT_DIR_ENV,
        REQUESTS_CA_BUNDLE_ENV,
    ):
        os.environ.pop(name, None)
    set_ca_bundle_path(ca_bundle)
    if ca_bundle_dir:
        os.environ[SSL_CERT_DIR_ENV] = ca_bundle_dir
    _run_or_exit(
        package=package,
        product=package_display_name(selected_package),
        host=host,
        org_api_key=org_api_key,
        allow_privileged_reexec=False,
    )
