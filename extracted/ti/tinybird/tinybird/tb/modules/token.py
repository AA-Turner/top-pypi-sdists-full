from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import click
import pyperclip
from click import Context
from humanfriendly import parse_timespan

from tinybird.tb.client import AuthNoTokenException, TinyB
from tinybird.tb.modules.cli import cli
from tinybird.tb.modules.common import (
    DoesNotExistException,
    echo_safe_humanfriendly_tables_format_smart_table,
)
from tinybird.tb.modules.exceptions import CLITokenException
from tinybird.tb.modules.feedback_manager import FeedbackManager


@cli.group()
@click.pass_context
def token(ctx: Context) -> None:
    """Token commands."""


@token.command(name="ls")
@click.option("--match", default=None, help="Retrieve any token matching the pattern. For example, --match _test")
@click.pass_context
def token_ls(
    ctx: Context,
    match: Optional[str] = None,
) -> None:
    """List Static Tokens."""

    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]

    try:
        tokens = client.token_list(match)
        columns = ["id", "name", "token"]
        table = list(map(lambda token: [token.get(key, "") for key in columns], tokens))

        click.echo(FeedbackManager.info_tokens())
        echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)
        click.echo("\n")
    except AuthNoTokenException:
        raise
    except Exception as e:
        raise CLITokenException(FeedbackManager.error_exception(error=e))


@token.command(name="rm")
@click.argument("token_id")
@click.option("--yes", is_flag=True, default=False, help="Don't ask for confirmation")
@click.pass_context
def token_rm(ctx: Context, token_id: str, yes: bool) -> None:
    """Remove a static token."""

    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]
    if yes or click.confirm(FeedbackManager.warning_confirm_delete_token(token=token_id)):
        try:
            client.token_delete(token_id)
        except AuthNoTokenException:
            raise
        except DoesNotExistException:
            raise CLITokenException(FeedbackManager.error_token_does_not_exist(token_id=token_id))
        except Exception as e:
            raise CLITokenException(FeedbackManager.error_exception(error=e))
        click.echo(FeedbackManager.success_delete_token(token=token_id))


@token.command(name="refresh")
@click.argument("token_id")
@click.option("--yes", is_flag=True, default=False, help="Don't ask for confirmation")
@click.pass_context
def token_refresh(ctx: Context, token_id: str, yes: bool) -> None:
    """Refresh a Static Token."""

    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]
    if yes or click.confirm(FeedbackManager.warning_confirm_refresh_token(token=token_id)):
        try:
            client.token_refresh(token_id)
        except AuthNoTokenException:
            raise
        except DoesNotExistException:
            raise CLITokenException(FeedbackManager.error_token_does_not_exist(token_id=token_id))
        except Exception as e:
            raise CLITokenException(FeedbackManager.error_exception(error=e))
        click.echo(FeedbackManager.success_refresh_token(token=token_id))


@token.command(name="scopes")
@click.argument("token_id")
@click.pass_context
def token_scopes(ctx: Context, token_id: str) -> None:
    """List Static Token scopes."""

    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]

    try:
        scopes = client.token_scopes(token_id)
        columns = ["type", "resource", "filter"]
        table = list(map(lambda scope: [scope.get(key, "") for key in columns], scopes))
        click.echo(FeedbackManager.info_token_scopes(token=token_id))
        echo_safe_humanfriendly_tables_format_smart_table(table, column_names=columns)
        click.echo("\n")
    except AuthNoTokenException:
        raise
    except Exception as e:
        raise CLITokenException(FeedbackManager.error_exception(error=e))


@token.command(name="copy")
@click.argument("token_id")
@click.pass_context
def token_copy(ctx: Context, token_id: str) -> None:
    """Copy a Static Token."""

    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]

    try:
        token = client.token_get(token_id)
        pyperclip.copy(token["token"].strip())
    except AuthNoTokenException:
        raise
    except DoesNotExistException:
        raise CLITokenException(FeedbackManager.error_token_does_not_exist(token_id=token_id))
    except Exception as e:
        raise CLITokenException(FeedbackManager.error_exception(error=e))
    click.echo(FeedbackManager.success_copy_token(token=token_id))


def parse_ttl(ctx, param, value):
    if value is None:
        return None
    try:
        seconds = parse_timespan(value)
        return timedelta(seconds=seconds)
    except ValueError:
        raise click.BadParameter(f"Invalid time to live format: {value}")


def parse_fixed_params(fixed_params_list):
    parsed_params = []
    for fixed_param in fixed_params_list:
        param_dict = {}
        for param in fixed_param.split(","):
            key, value = param.split("=")
            param_dict[key] = value
        parsed_params.append(param_dict)
    return parsed_params


@token.group()
@click.pass_context
def create(ctx: Context) -> None:
    """Token creation commands.

    You can create two types of tokens: Static or JWT.

    * Static Tokens do not have a TTL and can have any valid scope (ADMIN, TOKENS, or ORG_DATASOURCES:READ).

    * JWT tokens have a TTL and can have PIPES:READ and DATASOURCES:READ scopes. Their main use case is allow your users to call your endpoints or read datasources without exposing your API key.


    Examples:

    tb token create static my_static_token --scope ADMIN

    tb token create static my_static_token --scope TOKENS

    tb token create jwt my_jwt_token --ttl 1h --scope PIPES:READ --resource my_pipe

    tb token create jwt my_jwt_token --ttl 1h --scope DATASOURCES:READ --resource my_datasource --filter "column = 'value'"
    """


@create.command(name="jwt")
@click.argument("name")
@click.option("--ttl", type=str, callback=parse_ttl, required=True, help="Time to live (e.g., '1h', '30min', '1d')")
@click.option(
    "--scope",
    multiple=True,
    type=click.Choice(["PIPES:READ", "DATASOURCES:READ"]),
    required=True,
    help="Scope of the token (only PIPES:READ and DATASOURCES:READ are allowed for JWT tokens)",
)
@click.option("--resource", multiple=True, required=True, help="Resource associated with the scope")
@click.option(
    "--fixed-params", multiple=True, help="Fixed parameters in key=value format, multiple values separated by commas"
)
@click.option(
    "--filter",
    multiple=True,
    help="SQL filter to apply when reading a datasource (only applicable for DATASOURCES:READ scope)",
)
@click.pass_context
def create_jwt_token(ctx: Context, name: str, ttl: timedelta, scope, resource, fixed_params, filter) -> None:
    """Create a JWT token with a TTL specify."""

    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]

    expiration_time = int((ttl + datetime.now(timezone.utc)).timestamp())
    if len(scope) != len(resource):
        raise CLITokenException(FeedbackManager.error_number_of_scopes_and_resources_mismatch())

    # Ensure the number of fixed-params does not exceed the number of scope/resource pairs
    if fixed_params and len(fixed_params) > len(scope):
        raise CLITokenException(FeedbackManager.error_number_of_fixed_params_and_resources_mismatch())

    # Ensure the number of filters does not exceed the number of scope/resource pairs
    if filter and len(filter) > len(scope):
        raise CLITokenException("The number of SQL filters must match the number of scopes")

    # Parse fixed params
    parsed_fixed_params = parse_fixed_params(fixed_params) if fixed_params else []

    # Create a list of fixed params for each scope/resource pair, defaulting to empty dict if not provided
    fixed_params_list: List[Dict[str, Any]] = [{}] * len(scope)
    for i, params in enumerate(parsed_fixed_params):
        fixed_params_list[i] = params

    # Create a list of filters for each scope/resource pair, defaulting to None if not provided
    filters_list: List[Optional[str]] = [None] * len(scope)
    for i, f in enumerate(filter):
        filters_list[i] = f

    scopes = []
    for sc, res, fparams, filter in zip(scope, resource, fixed_params_list, filters_list):
        scope_data = {
            "type": sc,
            "resource": res,
        }

        if sc == "PIPES:READ" and fparams:
            scope_data["fixed_params"] = fparams
        elif sc == "DATASOURCES:READ" and filter:
            scope_data["filter"] = filter

        scopes.append(scope_data)

    try:
        response = client.create_jwt_token(name, expiration_time, scopes)
    except AuthNoTokenException:
        raise
    except Exception as e:
        raise CLITokenException(FeedbackManager.error_exception(error=e))

    click.echo("The token has been generated successfully.")
    click.echo(
        f"The token will expire at: {datetime.fromtimestamp(expiration_time).strftime('%Y-%m-%d %H:%M:%S')} UTC "
    )
    click.echo(f"The token is: {response['token']}")


# Valid scopes for Static Tokens
valid_scopes = [
    "ADMIN",
    "TOKENS",
    "ORG_DATASOURCES:READ",
]


# As we are passing dynamic options to the command, we need to create a custom class to handle the help message
class DynamicOptionsCommand(click.Command):
    def get_help(self, ctx):
        # Usage
        usage = "Usage: tb token create static [OPTIONS] NAME\n\n"
        dynamic_options_help = usage

        # Description
        dynamic_options_help += "  Create a Static Token that will live forever.\n\n"

        # Options
        dynamic_options_help += "Options:\n"
        dynamic_options_help += f"  --scope [{','.join(valid_scopes)}]   Scope for the token [Required]\n"
        dynamic_options_help += "  --resource TEXT    Resource you want to associate the scope with\n"
        dynamic_options_help += "  -h, --help            Show this message and exit.\n"

        return dynamic_options_help


@create.command(
    name="static", context_settings=dict(ignore_unknown_options=True, allow_extra_args=True), cls=DynamicOptionsCommand
)
@click.argument("name")
@click.pass_context
def create_static_token(ctx, name: str):
    """Create a Static Token."""
    obj: Dict[str, Any] = ctx.ensure_object(dict)
    client: TinyB = obj["client"]

    args = ctx.args
    scopes: List[Dict[str, str]] = []
    current_scope = None

    # We parse the arguments to get the scopes, resources and filters
    # The arguments should be in the format --scope <scope> --resource <resource> --filter <filter>
    i = 0
    while i < len(args):
        if args[i] == "--scope":
            if current_scope:
                scopes.append(current_scope)
                current_scope = {}
            unsafe_scope = args[i + 1]
            current_scope = {"scope": unsafe_scope.upper() if isinstance(unsafe_scope, str) else unsafe_scope}
            i += 2
        elif args[i] == "--resource":
            if current_scope is None:
                raise click.BadParameter("Resource must follow a scope")
            if "resource" in current_scope:
                raise click.BadParameter(
                    "Resource already defined for this scope. The format is --scope <scope> --resource <resource> --filter <filter>"
                )
            current_scope["resource"] = args[i + 1]
            i += 2
        elif args[i] == "--filter":
            if current_scope is None:
                raise click.BadParameter("Filter must follow a scope")
            if "filter" in current_scope:
                raise click.BadParameter(
                    "Filter already defined for this scope. The format is --scope <scope> --resource <resource> --filter <filter>"
                )
            current_scope["filter"] = args[i + 1]
            i += 2
        else:
            raise click.BadParameter(f"Unknown parameter {args[i]}")

    if current_scope:
        scopes.append(current_scope)

    # Parse the scopes like `SCOPE:RESOURCE:FILTER` or `SCOPE:RESOURCE` or `SCOPE` as that's what the API expsects
    scoped_parsed: List[str] = []
    for scope in scopes:
        if scope.get("resource") and scope.get("filter"):
            scoped_parsed.append(f"{scope.get('scope')}:{scope.get('resource')}:{scope.get('filter')}")
        elif scope.get("resource"):
            scoped_parsed.append(f"{scope.get('scope')}:{scope.get('resource')}")
        elif "scope" in scope:
            scoped_parsed.append(scope.get("scope", ""))
        else:
            raise CLITokenException("Unknown error")

    try:
        token = None
        try:
            click.echo(FeedbackManager.highlight(message=f"\n» Checking if token '{name}' exists..."))
            token = client.token_get(name)
        except Exception:
            pass
        if token:
            click.echo(FeedbackManager.info(message=f"* Token '{name}' found, updating it..."))
            client.alter_tokens(name, scoped_parsed)
        else:
            click.echo(FeedbackManager.info(message=f"* Token '{name}' not found, creating it..."))
            client.create_token(name, scoped_parsed, origin_code=None)
    except AuthNoTokenException:
        raise
    except Exception as e:
        raise CLITokenException(FeedbackManager.error_exception(error=e))

    if token:
        click.echo(FeedbackManager.success(message=f"✓ Token '{name}' updated successfully"))
    else:
        click.echo(FeedbackManager.success(message=f"✓ Token '{name}' generated successfully"))
