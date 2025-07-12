import json
import sys

import click

from tecton._internals import metadata_service
from tecton.cli import printer
from tecton.cli.cli_utils import click_exception_wrapper
from tecton.cli.command import TectonCommand
from tecton.cli.command import TectonCommandCategory
from tecton.cli.command import TectonGroup
from tecton_proto.secrets.secrets_service__client_pb2 import CreateSecretScopeRequest
from tecton_proto.secrets.secrets_service__client_pb2 import DeleteSecretRequest
from tecton_proto.secrets.secrets_service__client_pb2 import DeleteSecretScopeRequest
from tecton_proto.secrets.secrets_service__client_pb2 import GetSecretValueRequest
from tecton_proto.secrets.secrets_service__client_pb2 import ListSecretScopesRequest
from tecton_proto.secrets.secrets_service__client_pb2 import ListSecretsRequest
from tecton_proto.secrets.secrets_service__client_pb2 import PutSecretValueRequest


SECRETS_SERVICE_CONN_ERR = """Error: Cannot connect to secrets service.
Your cluster may not have Tecton Secrets enabled. Please contact your Tecton support representative to see
if it can be enabled."""


@click.command("secrets", cls=TectonGroup, command_category=TectonCommandCategory.IDENTITY)
def secrets():
    """Manage Tecton secrets and secret scopes."""


@secrets.command("create-scope", requires_auth=True, cls=TectonCommand)
@click.option("-s", "--scope", default=None, required=True, help="Secret scope name")
@click_exception_wrapper
def create_scope(scope):
    """Create a new secret scope."""
    request = CreateSecretScopeRequest(scope=scope)
    metadata_service.instance().CreateSecretScope(request)
    printer.safe_print(f'Created secret scope "{scope}"')


@secrets.command("list-scopes", requires_auth=True, cls=TectonCommand)
@click_exception_wrapper
def list_scopes():
    """List secret scopes."""
    request = ListSecretScopesRequest()
    response = metadata_service.instance().ListSecretScopes(request)

    if len(response.scopes) == 0:
        printer.safe_print("No secret scopes found", file=sys.stderr)
    else:
        for scope in response.scopes:
            printer.safe_print(scope.name)


@secrets.command("delete-scope", requires_auth=True, cls=TectonCommand)
@click.option("-s", "--scope", default=None, required=True, help="Secret scope name")
@click_exception_wrapper
def delete_secret_scope(scope):
    """Delete a secret scope."""
    request = DeleteSecretScopeRequest(scope=scope)
    metadata_service.instance().DeleteSecretScope(request)
    printer.safe_print(f'Deleted secret scope "{scope}".')


@secrets.command("list", requires_auth=True, cls=TectonCommand)
@click.option("-s", "--scope", default=None, required=True, help="Scope name")
@click.option("--json-out", is_flag=True, hidden=True, help="Output in JSON format")
@click_exception_wrapper
def list_secrets(scope, json_out):
    """List secrets in a scope."""
    request = ListSecretsRequest(scope=scope)
    response = metadata_service.instance().ListSecrets(request)

    if json_out:
        names = [key.name for key in response.keys]
        printer.safe_print(json.dumps(names), plain=True)
    else:
        if len(response.keys) == 0:
            printer.safe_print("No secrets found")
        else:
            for key in response.keys:
                printer.safe_print(key.name)


@secrets.command("get", requires_auth=True, cls=TectonCommand)
@click.option("-s", "--scope", default=None, required=True, help="Secret scope name")
@click.option("-k", "--key", default=None, required=True, help="Secret key")
@click_exception_wrapper
def get_secret_value(scope, key):
    """Gets a secret value."""
    request = GetSecretValueRequest(scope=scope, key=key)

    response = metadata_service.instance().GetSecretValue(request)
    printer.safe_print(response.value)


@secrets.command("put", requires_auth=True, cls=TectonCommand)
@click.option("-s", "--scope", default=None, required=True, help="Secret scope name")
@click.option("-k", "--key", default=None, required=True, help="Secret key")
@click.option("-f", "--file", default=None, required=False, help="File containing secret value, stdin if not included")
@click_exception_wrapper
def put_secret_value(scope, key, file):
    """Put secret value in a scope. Updates if secret already exists."""
    if file:
        with open(file, "rt") as f:
            value = f.read().rstrip("\n")
    else:
        printer.safe_print("File omitted, reading from stdin. Ctrl+D or Ctrl+Z on a new line then Enter to stop.")
        lines = []
        for line in sys.stdin:
            lines.append(line.strip())
        value = "\n".join(lines)

    request = PutSecretValueRequest(scope=scope, key=key, value=value)
    metadata_service.instance().PutSecretValue(request)


@secrets.command("delete", requires_auth=True, cls=TectonCommand)
@click.option("-s", "--scope", default=None, required=True, help="Secret scope name")
@click.option("-k", "--key", default=None, required=True, help="Secret key")
@click_exception_wrapper
def delete_secret(scope, key):
    """Delete secret in a scope."""
    request = DeleteSecretRequest(scope=scope, key=key)
    metadata_service.instance().DeleteSecret(request)
    printer.safe_print(f'Deleted secret "{key}".')
