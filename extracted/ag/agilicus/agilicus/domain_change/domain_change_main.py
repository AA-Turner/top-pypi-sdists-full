"""CLI wiring for the organisation domain-change report."""

import json

import click
from prettytable import PrettyTable

from agilicus.agilicus_api import ApiException
from agilicus.command_helpers import Command
from agilicus.output import output_if_console

from . import domain_change

cmd = Command()


@cmd.command(name="domain-change")
@click.option(
    "--org-id",
    default=None,
    help="Organisation id (defaults to the token's org).",
)
@click.option(
    "--new-subdomain",
    "--subdomain",
    "new_subdomain",
    required=True,
    help="The organisation's new subdomain.",
)
@click.option(
    "--issuer-url",
    "--issuer",
    "issuer_url",
    default=None,
    help="New issuer URL, for a dedicated issuer (POST only).",
)
@click.option(
    "--dry-run/--no-dry-run",
    default=True,
    show_default=True,
    help=(
        "Preview the change list (default). --no-dry-run delegates to the "
        "7.1 executor and writes."
    ),
)
@click.pass_context
def cli_command_domain_change(ctx, org_id, new_subdomain, issuer_url, dry_run):
    """Report every object bound to an organisation's old domain.

    Prints a per-type count (or per-component) table by default. With
    `--output-format json` it prints the exact report body, which is usable as
    the customer change list.
    """
    try:
        report = domain_change.plan_domain_change(
            ctx,
            org_id=org_id,
            new_subdomain=new_subdomain,
            issuer_url=issuer_url,
            dry_run=dry_run,
        )
    except domain_change.DomainChangePreflightError as exc:
        _fail_preflight(ctx, exc.components)
    except ApiException as exc:
        if getattr(exc, "status", None) == 409:
            _fail_preflight(
                ctx, domain_change.preflight_components(getattr(exc, "body", None))
            )
        raise click.ClickException(str(exc))
    except ValueError as exc:
        raise click.ClickException(str(exc))
    except domain_change.DomainChangeError as exc:
        raise click.ClickException(str(exc))

    if (ctx.obj or {}).get("output_format") == "json":
        click.echo(json.dumps(report, indent=2, default=str))
        return

    _print_report(ctx, report)


def _fail_preflight(ctx, components):
    """Report a 409 preflight failure to stderr and exit non-zero.

    Mirrors the ``orgs.add``/``issuers.add`` ``ApiException`` handling: the
    failing components/hosts are surfaced, and no mutating call is attempted.
    In JSON mode a JSON error object is emitted to stderr.
    """
    failed = _failed_components(components)
    if (ctx.obj or {}).get("output_format") == "json":
        click.echo(
            json.dumps(
                {"error": "preflight_failed", "components": failed},
                default=str,
            ),
            err=True,
        )
        ctx.exit(1)

    for component in failed:
        click.echo(_component_line(component), err=True)
    raise click.ClickException("domain change preflight failed; nothing was changed")


def _component_name(component):
    """The component's name, tolerating the older ``component`` key."""
    return component.get("name") or component.get("component") or ""


def _component_state(component):
    """The component's state, tolerating the older ``status``/``ok`` shape.

    The 7.1 executor records ``name``/``state`` (``pending``, ``running``,
    ``succeeded``, ``failed``, ``skipped``); the 409 preflight body may still
    carry ``component``/``status`` or a bare ``ok`` boolean, so both render.
    """
    state = component.get("state")
    if state is None:
        state = component.get("status")
    if state is None and "ok" in component:
        state = "succeeded" if component.get("ok") else "failed"
    return state


def _failed_components(components):
    """The components that failed, falling back to every reported component."""
    reported = [c for c in (components or []) if isinstance(c, dict)]
    failed = [c for c in reported if _component_state(c) == "failed"]
    return failed or reported


def _component_line(component):
    """A one-line human rendering of a preflight component/host."""
    if not isinstance(component, dict):
        return str(component)
    parts = [
        str(component.get(key))
        for key in (
            "name",
            "component",
            "host",
            "state",
            "status",
            "reason",
            "detail",
            "error",
        )
        if component.get(key)
    ]
    return " ".join(parts) or json.dumps(component, default=str)


def _component_detail(component):
    """The detail/error text for a component's table row."""
    parts = [
        str(component.get(key)) for key in ("detail", "error") if component.get(key)
    ]
    return " ".join(parts)


def _print_report(ctx, report):
    """Print the per-component or per-type counts table (non-JSON output)."""
    components = report.get("components")
    if components:
        _print_components(ctx, report, components)
        return

    org_id = report.get("org_id") or "-"
    mode = "dry run" if report.get("dry_run", True) else "execute"
    output_if_console(
        ctx,
        "Domain change report for organisation {} ({})".format(org_id, mode),
    )
    for name, count in domain_change.ordered_counts(report):
        output_if_console(ctx, "  {:32s} {}".format(name, count))
    output_if_console(ctx, "  " + domain_change.summary_line(report))
    for warning in report.get("warnings") or []:
        output_if_console(ctx, "  ! {}".format(_warning_text(warning)))


def _print_components(ctx, report, components):
    """Print the per-component result table from a 7.1 executor response."""
    org_id = report.get("org_id") or "-"
    mode = "dry run" if report.get("dry_run", True) else "execute"
    output_if_console(
        ctx,
        "Domain change for organisation {} ({})".format(org_id, mode),
    )
    table = PrettyTable(["component", "status", "detail"])
    table.align = "l"
    for component in components:
        if not isinstance(component, dict):
            table.add_row([str(component), "unknown", ""])
            continue
        state = _component_state(component)
        table.add_row(
            [
                _component_name(component),
                state if state is not None else "unknown",
                _component_detail(component),
            ]
        )
    output_if_console(ctx, table.get_string())
    for warning in report.get("warnings") or []:
        output_if_console(ctx, "  ! {}".format(_warning_text(warning)))


def _warning_text(warning):
    if not isinstance(warning, dict):
        return str(warning)
    parts = [
        str(warning.get(key))
        for key in ("object_type", "object_id", "reason")
        if warning.get(key)
    ]
    return " ".join(parts) or str(warning)


def add_commands(cli):
    cmd.add_to_cli(cli)
