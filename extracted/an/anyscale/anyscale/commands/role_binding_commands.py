from typing import Any, List, Optional

import click
from rich import print as rprint
import tabulate
import yaml

import anyscale
from anyscale.cli_logger import BlockLogger
from anyscale.commands.doc_metadata import (
    command_metadata,
    CommandExample,
    ReleaseStatus,
)
from anyscale.commands.output_format import (
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    OutputFormat,
    print_output,
)
from anyscale.commands.util import AnyscaleCommand
from anyscale.errors import UserError
from anyscale.role_binding.models import (
    AppliedResultUnreadable,
    PolicyApplyResult,
    PolicyChange,
    PolicyPrincipals,
    PolicyRole,
    RoleBindingPolicy,
)


log = BlockLogger()

_SCOPE_TYPES = ["cloud", "project", "organization"]

_GENERATE_OUTPUT = """\
roles:
- role_id: rol_abc123
  principals:
    user_id:
    - usr_abc123
    - usr_def456
    group_id:
    - ug_abc123
- role_id: rol_xyz789
  principals:
    group_id:
    - ug_xyz789
"""

_APPLY_OUTPUT = """\
Change    Role        Principal    Kind
--------  ----------  -----------  ----------
+         rol_abc123  usr_def456   user
-         rol_xyz789  ug_xyz789    user_group
Dry run: 1 granted, 1 revoked. Nothing was changed.
"""


@click.group("role-binding", help="State a resource's access list as one document.")
def role_binding_cli() -> None:
    pass


@role_binding_cli.group("policy", help="Generate and apply a resource's access list.")
def role_binding_policy_cli() -> None:
    pass


def _scope(scope_type: str, scope_id: Optional[str]) -> Optional[str]:
    """
    The resource to act on. An organization needs no id, since a caller may
    only ever act on their own, and naming another organization's is refused by
    the platform rather than answered for a different one.
    """
    if scope_id is not None and not scope_id.strip():
        raise click.ClickException(
            f"--scope-id was given for scope type '{scope_type}' but is blank."
        )
    if scope_type != "organization" and scope_id is None:
        raise click.ClickException(f"--scope-id is required for scope type '{scope_type}'.")
    return scope_id


def _built(config_file: str, model: type, fields: dict) -> Any:
    """
    A model built from what the file said, with what it got wrong reported as a
    message rather than as a traceback. The models validate on construction, so
    every field the file supplies has to be built through here.
    """
    try:
        return model(**fields)
    except (TypeError, ValueError) as e:
        raise click.ClickException(f"Invalid config file '{config_file}': {e}")


def _described(scope_type: str, scope_id: Optional[str]) -> str:
    """What to call the resource in output, given it may not have been named."""
    if scope_id is None:
        return "your organization"
    return f"{scope_type} {scope_id}"


def _policy_from_file(config_file: str) -> RoleBindingPolicy:
    """
    A policy as a person keeps it in version control. Roles and principals are
    identified by id, which is what a generate emits, so a generated document
    applies straight back. An empty roles list revokes everything on the
    resource, so a file that parses to nothing is refused rather than read as
    that instruction.
    """
    try:
        with open(config_file) as f:
            document = yaml.safe_load(f)
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as e:
        raise click.ClickException(f"Failed to read config file '{config_file}': {e}")

    if document is None:
        raise click.ClickException(
            f"Invalid config file '{config_file}': file is empty. To revoke every "
            f"role binding on the resource, write 'roles: []' rather than nothing."
        )
    if not isinstance(document, dict) or "roles" not in document:
        raise click.ClickException(
            f"Invalid config file '{config_file}': expected a YAML mapping with a "
            f"top-level 'roles' key."
        )
    if not isinstance(document["roles"], list):
        raise click.ClickException(f"Invalid config file '{config_file}': 'roles' must be a list.")
    unknown_top = sorted(set(document) - {"roles"})
    if unknown_top:
        raise click.ClickException(
            f"Invalid config file '{config_file}': it has "
            f"{', '.join(repr(key) for key in unknown_top)}, which a policy does not take. "
            f"A policy takes 'roles'."
        )

    roles = []
    for entry in document["roles"]:
        if not isinstance(entry, dict) or "role_id" not in entry:
            raise click.ClickException(
                f"Invalid config file '{config_file}': every entry under 'roles' needs "
                f"a 'role_id' key. Find a role's id with 'anyscale role list'."
            )
        unknown = sorted(set(entry) - {"role_id", "principals"})
        if unknown:
            raise click.ClickException(
                f"Invalid config file '{config_file}': an entry under 'roles' has "
                f"{', '.join(repr(key) for key in unknown)}, which it does not take. An "
                f"entry takes 'role_id' and 'principals'."
            )
        principals = entry.get("principals")
        if principals is None:
            principals = {}
        if not isinstance(principals, dict) or set(principals) - {"user_id", "group_id"}:
            raise click.ClickException(
                f"Invalid config file '{config_file}': 'principals' is a mapping with a "
                f"'user_id' block, a 'group_id' block, or both."
            )
        roles.append(
            _built(
                config_file,
                PolicyRole,
                {
                    "role_id": entry["role_id"],
                    "principals": _built(config_file, PolicyPrincipals, principals),
                },
            )
        )

    return _built(config_file, RoleBindingPolicy, {"roles": roles})


def _change_rows(result: PolicyApplyResult) -> List[List[str]]:
    """Granted first, then revoked."""

    def rows(changes: List[PolicyChange], sign: str) -> List[List[str]]:
        return [
            [sign, change.role_id, change.principal_id, change.principal_type]
            for change in sorted(changes, key=lambda c: (c.role_id, c.principal_id))
        ]

    return rows(result.granted, "+") + rows(result.revoked, "-")


def _print_changes(result: PolicyApplyResult, resource: str) -> None:
    if not result.granted and not result.revoked:
        log.info(f"{resource} already matches the policy. Nothing to change.")
        return

    rprint(
        tabulate.tabulate(
            _change_rows(result),
            headers=["Change", "Role", "Principal", "Kind"],
        )
    )
    counts = f"{len(result.granted)} granted, {len(result.revoked)} revoked"
    if result.dry_run:
        log.info(f"Dry run: {counts}. Nothing was changed.")
    else:
        log.info(f"Applied: {counts}.")


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT, OutputFormat.JSON, OutputFormat.YAML],
    examples=[
        CommandExample(
            description="Generate a cloud's policy as an editable YAML document.",
            command="anyscale role-binding policy generate --scope-type cloud --scope-id cld_abc123 -o yaml",
            output_raw=_GENERATE_OUTPUT,
            output_instance=lambda: RoleBindingPolicy(
                roles=[
                    PolicyRole(
                        role_id="rol_abc123",
                        principals=PolicyPrincipals(
                            user_id=["usr_abc123", "usr_def456"],
                            group_id=["ug_abc123"],
                        ),
                    )
                ]
            ),
        ),
    ],
    output_schema=RoleBindingPolicy,
)
@role_binding_policy_cli.command(
    name="generate",
    short_help="Generate a policy from the role bindings a resource holds.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--scope-type",
    required=True,
    type=click.Choice(_SCOPE_TYPES, case_sensitive=False),
    help="Resource scope type ('cloud', 'project', or 'organization').",
)
@click.option(
    "--scope-id",
    required=False,
    default=None,
    type=str,
    help="Resource scope ID (e.g., cld_abc123, prj_xyz789). Defaults to your organization for 'organization'.",
)
@click.option(
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    "output_format",
    type=click.Choice([OutputFormat.TEXT.value, OutputFormat.JSON.value, OutputFormat.YAML.value]),
    default=OutputFormat.TEXT.value,
    show_default=True,
    help="Output format for the result.",
)
def generate_role_binding_policy(
    scope_type: str,
    scope_id: Optional[str],
    output_format: str,
) -> None:
    """Generate a policy from the role bindings a resource holds.

    The document is what an apply accepts, so it can be saved, edited and applied
    back. Pass -o yaml to get the document itself rather than a summary of it.

    Only bindings held directly on the resource are generated. A principal that
    reaches the resource through a binding held above it is not listed here.
    """
    scope_type = scope_type.lower()
    scope = _scope(scope_type, scope_id)
    described = _described(scope_type, scope)

    try:
        policy = anyscale.role_binding.generate_policy(
            resource_type=scope_type,
            resource_id=scope,
        )
    except (TypeError, ValueError) as e:
        raise UserError(f"Failed to generate the policy: {e}") from None

    if output_format != OutputFormat.TEXT.value:
        print_output(policy, output_format)
        return

    if not policy.roles:
        log.info(f"No role bindings are held on {described}.")
        return

    log.info(f"Role bindings held on {described}:")
    rprint(
        tabulate.tabulate(
            [
                [role.role_id, principal_id, principal_type]
                for role in policy.roles
                for principal_type, principal_id in role.principals.flattened()
            ],
            headers=["Role", "Principal", "Kind"],
        )
    )


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT, OutputFormat.JSON, OutputFormat.YAML],
    examples=[
        CommandExample(
            description="Preview what an apply would change, without changing anything.",
            command="anyscale role-binding policy apply --scope-type cloud --scope-id cld_abc123 -f policy.yaml --dry-run",
            output_raw=_APPLY_OUTPUT,
            output_instance=lambda: PolicyApplyResult(
                granted=[
                    PolicyChange(
                        role_id="rol_abc123",
                        principal_id="usr_def456",
                        principal_type="user",
                    )
                ],
                revoked=[
                    PolicyChange(
                        role_id="rol_xyz789",
                        principal_id="ug_xyz789",
                        principal_type="user_group",
                    )
                ],
                dry_run=True,
            ),
        ),
    ],
    output_schema=PolicyApplyResult,
)
@role_binding_policy_cli.command(
    name="apply",
    short_help="Make a resource match a role binding policy.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--scope-type",
    required=True,
    type=click.Choice(_SCOPE_TYPES, case_sensitive=False),
    help="Resource scope type ('cloud', 'project', or 'organization').",
)
@click.option(
    "--scope-id",
    required=False,
    default=None,
    type=str,
    help="Resource scope ID (e.g., cld_abc123, prj_xyz789). Defaults to your organization for 'organization'.",
)
@click.option(
    "-f",
    "--config-file",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
    help="Path to a YAML file holding the policy to apply.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Report what the apply would change, and change nothing.",
)
@click.option(
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    "output_format",
    type=click.Choice([OutputFormat.TEXT.value, OutputFormat.JSON.value, OutputFormat.YAML.value]),
    default=OutputFormat.TEXT.value,
    show_default=True,
    help="Output format for the result.",
)
def apply_role_binding_policy(
    scope_type: str,
    scope_id: Optional[str],
    config_file: str,
    dry_run: bool,
    output_format: str,
) -> None:
    """Make a resource match a role binding policy.

    The file states the access wanted on the resource. What it is missing is
    revoked, what it adds is granted, and what already matches is left alone, so
    applying the same file twice changes nothing the second time. Bindings held
    above the resource are not the file's to change.

    Pass --dry-run to see the change before committing to it. It runs the same
    comparison and the same refusals as an apply and writes nothing, so a preview
    cannot disagree with the apply that follows it.

    Example policy.yaml:

    \b
    roles:
      - role_id: rol_abc123
        principals:
          user_id:
            - usr_abc123
            - usr_def456
          group_id:
            - ug_abc123
      - role_id: rol_xyz789
        principals:
          group_id:
            - ug_xyz789

    A role appears once, with every principal that holds it under it, split
    into a 'user_id' block and a 'group_id' block. Either block may be left
    out. This is exactly what a generate emits, so a generated document
    applies straight back. Find a role's id with 'anyscale role list'. Writing
    'roles: []' revokes every role binding on the resource, so it has to be
    deliberate.
    """
    scope_type = scope_type.lower()
    scope = _scope(scope_type, scope_id)
    described = _described(scope_type, scope)
    policy = _policy_from_file(config_file)

    if output_format == OutputFormat.TEXT.value:
        if dry_run:
            log.info(f"Comparing {described} against '{config_file}'...")
        else:
            log.info(f"Applying '{config_file}' to {described}...")

    try:
        result = anyscale.role_binding.apply_policy(
            resource_type=scope_type,
            policy=policy,
            resource_id=scope,
            dry_run=dry_run,
        )
    except AppliedResultUnreadable as e:
        raise UserError(
            f"The policy was applied, but the result could not be read: {e}. Run a "
            f"generate to see what {described} now holds."
        ) from None
    except (TypeError, ValueError) as e:
        raise UserError(f"Failed to apply the policy: {e}") from None

    if output_format != OutputFormat.TEXT.value:
        print_output(result, output_format)
        return

    _print_changes(result, described)
