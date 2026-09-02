"""CLI-orchestration wrappers over the pure persistence primitives in config.py.

``config.py`` is the data layer: ``persist_credentials`` and ``save_config``
return ``bool`` and never touch Typer. The ``*_or_exit`` wrappers here own the
CLI presentation (standardized error message + ``typer.Exit``), so that layer
isn't pulled into every module that imports ``config`` — notably the hook paths,
which want the pure ``persist_credentials`` only. Import these from command
modules only.

Wrappers reach the primitives through the ``config`` module (not bound names) so
tests patching ``runlayer_cli.config.save_config`` still intercept the write.
"""

import typer

from runlayer_cli import config
from runlayer_cli.config import Config
from runlayer_cli.enrollment import clear_enrollment_marker, write_enrollment_marker


def credential_dest(keyring_used: bool) -> str:
    """Human-readable destination for a persisted credential."""
    return "credential store" if keyring_used else "config file"


def persist_credentials_or_exit(
    config_obj: Config,
    host: str,
    api_key: str,
    *,
    subject: str,
    exit_code: int = 1,
    fail_prefix: str = "Error:",
) -> bool:
    """Persist *api_key* for *host*; on failure print a standardized error and exit.

    Returns ``keyring_used`` so callers can render the destination message.
    """
    persistence = config.persist_credentials(config_obj, host, api_key)
    if not persistence["persisted"]:
        typer.secho(
            f"{fail_prefix} {subject} could not be persisted for {host} "
            f"(keychain write failed and the config file is not written in "
            f"this runtime).",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(exit_code)
    return persistence["keyring_used"]


def complete_device_enrollment(
    config_obj: Config,
    host: str,
    api_key: str,
    *,
    subject: str,
    exit_code: int = 1,
    fail_prefix: str = "Error:",
) -> bool:
    """Persist *api_key* for *host*, then drop the enrollment marker — in that order.

    Canonical persist→marker sequence for every exiting enroll entrypoint
    (``aiwatch enroll``, ``aiwatch bootstrap``, ``runlayer credentials enroll``).
    Owns the invariant that the marker is never dropped without a durably
    persisted credential: ``persist_credentials_or_exit`` exits *before* the
    marker is written when persistence fails (keychain write failed and the
    aiwatch ``save_config`` no-op left the secret in-memory only), so the marker
    — which the bootstrap credential gate treats as proof of a stored secret —
    can never falsely satisfy the gate. Funnel new enroll paths through here so
    the ordering can't drift; command modules then only print success UX.

    Returns ``keyring_used`` for the destination message. The hook lazy-enrollment
    fallback, which must not exit, instead calls the non-exiting
    ``config.persist_credentials`` half directly.
    """
    keyring_used = persist_credentials_or_exit(
        config_obj,
        host,
        api_key,
        subject=subject,
        exit_code=exit_code,
        fail_prefix=fail_prefix,
    )
    write_enrollment_marker(host)
    return keyring_used


def save_config_or_exit(
    config_obj: Config,
    *,
    subject: str,
    host: str,
    exit_code: int = 1,
) -> None:
    """Save *config*; on no-op (aiwatch runtime) print a standardized error and exit."""
    if not config.save_config(config_obj):
        typer.secho(
            f"Error: {subject} could not be persisted for {host} "
            f"(the config file is not written in this runtime).",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(exit_code)


def clear_host_credentials_or_exit(
    config_obj: Config,
    host: str,
    *,
    subject: str = "Credentials",
    exit_code: int = 1,
) -> bool:
    """Clear *host*'s credential; on a failed clear print an error and exit.

    Delete-side mirror of :func:`persist_credentials_or_exit`. Returns ``found``
    so callers can distinguish "cleared" from "nothing to clear" (no credentials
    for this host). Exits only when the host existed but the credential could not
    be durably removed — the keychain delete failed AND the YAML is not written
    in this runtime (aiwatch), so the secret may survive.

    On a durable clear, also removes the per-host enrollment marker so it stops
    falsely satisfying the bootstrap credential gate after the secret is gone.
    """
    clearance = config.clear_host_credentials(config_obj, host)
    if clearance["found"] and not clearance["cleared"]:
        typer.secho(
            f"Error: {subject} could not be cleared for {host} "
            f"(keychain delete failed and the config file is not written in "
            f"this runtime).",
            fg=typer.colors.RED,
            err=True,
        )
        raise typer.Exit(exit_code)
    if clearance["found"]:
        clear_enrollment_marker(host)
    return clearance["found"]
