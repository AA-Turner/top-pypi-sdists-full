import json
import sys

import click

from tecton._internals import metadata_service
from tecton.cli import printer
from tecton.cli.cli_utils import click_exception_wrapper
from tecton.cli.cli_utils import display_principal
from tecton.cli.cli_utils import pprint_dict
from tecton.cli.command import TectonCommandCategory
from tecton.cli.command import TectonGroup
from tecton.identities import api_keys
from tecton_core.errors import FailedPreconditionError
from tecton_core.errors import TectonAPIValidationError
from tecton_core.errors import TectonNotFoundError
from tecton_core.id_helper import IdHelper
from tecton_proto.data.service_account__client_pb2 import CreateServiceAccountRequest
from tecton_proto.data.service_account__client_pb2 import DeleteServiceAccountRequest
from tecton_proto.data.service_account__client_pb2 import GetServiceAccountsRequest
from tecton_proto.data.service_account__client_pb2 import ServiceAccountCredentialsType
from tecton_proto.data.service_account__client_pb2 import UpdateServiceAccountRequest
from tecton_proto.serviceaccounts.service_accounts_service__client_pb2 import ActivateServiceAccountSecretRequest
from tecton_proto.serviceaccounts.service_accounts_service__client_pb2 import CreateServiceAccountSecretRequest
from tecton_proto.serviceaccounts.service_accounts_service__client_pb2 import DeactivateServiceAccountSecretRequest
from tecton_proto.serviceaccounts.service_accounts_service__client_pb2 import DeleteServiceAccountSecretRequest
from tecton_proto.serviceaccounts.service_accounts_service__client_pb2 import ListServiceAccountSecretsRequest


@click.command("service-account", cls=TectonGroup, command_category=TectonCommandCategory.IDENTITY)
def service_account():
    """Manage Service Accounts."""


@service_account.command()
@click.option("-n", "--name", required=True, help="Name of the Service Account")
@click.option(
    "-d", "--description", default="", help="An optional, human readable description for this Service Account"
)
@click.option("--json-out", default=False, is_flag=True, help="Format Output as JSON")
@click.option(
    "--oauth",
    default=False,
    is_flag=True,
    help="Whether to create an OAuth Service Account. If not specified, this Service Account will have an API key instead.",
)
def create(name, description, json_out, oauth):
    """Create a new Service Account."""
    try:
        request = CreateServiceAccountRequest(name=name, description=description)
        if oauth:
            request.credentials_type = (
                ServiceAccountCredentialsType.SERVICE_ACCOUNT_CREDENTIALS_TYPE_OAUTH_CLIENT_CREDENTIALS
            )
        response = metadata_service.instance().CreateServiceAccount(request)
    except TectonAPIValidationError as e:
        printer.safe_print(f"Failed to create service account: {e}", file=sys.stderr)
        sys.exit(1)
    if json_out:
        service_account = {}
        if not oauth:
            service_account["api_key"] = response.api_key
        else:
            service_account["client_secret"] = response.client_secret
        service_account["id"] = response.id
        printer.safe_print(json.dumps(service_account, indent=4), plain=True)
    else:
        save_object = "API Key" if not oauth else "Client Secret"
        printer.safe_print(f"Save this {save_object} - you will not be able to get it again.")
        if not oauth:
            printer.safe_print(f"API Key:            {response.api_key}")
        else:
            printer.safe_print(f"Client Secret: {response.client_secret}")
        printer.safe_print(f"Service Account ID: {response.id}")
        printer.safe_print("Use `tecton access-control assign-role` to assign roles to your new service account.")


@service_account.command()
@click.argument("id", required=True)
def delete(id):
    """Permanently delete a Service Account by its ID."""
    request = DeleteServiceAccountRequest(id=id)
    try:
        response = metadata_service.instance().DeleteServiceAccount(request)
    except TectonAPIValidationError as e:
        printer.safe_print(f"Failed to delete service account: {e}", file=sys.stderr)
        sys.exit(1)
    printer.safe_print("Successfully deleted Service Account")


@service_account.command()
@click.option("-n", "--name", help="Name of the Service Account")
@click.option("-d", "--description", help="An optional, human readable description for this Service Account")
@click.argument("id", required=True)
@click_exception_wrapper
def update(id, name, description):
    """Update the name or description of a Service Account."""
    request = UpdateServiceAccountRequest(id=id)

    if name is None and description is None:
        msg = "Please mention the field to update using --name or --description."
        raise click.ClickException(msg)

    if name:
        request.name = name

    if description is not None:
        request.description = description

    try:
        response = metadata_service.instance().UpdateServiceAccount(request)
    except TectonAPIValidationError as e:
        printer.safe_print(f"Failed to Update Service Account: {e}", file=sys.stderr)
        sys.exit(1)

    printer.safe_print("Successfully updated Service Account")


@service_account.command()
@click.argument("id", required=True)
def activate(id):
    """Activate a Service Account by its ID."""
    request = UpdateServiceAccountRequest(id=id, is_active=True)
    try:
        response = metadata_service.instance().UpdateServiceAccount(request)
    except TectonAPIValidationError as e:
        printer.safe_print(f"Failed to Activate Service Account: {e}", file=sys.stderr)
        sys.exit(1)
    printer.safe_print("Successfully activated Service Account")


@service_account.command()
@click.argument("id", required=True)
@click_exception_wrapper
def deactivate(id):
    """Deactivate a Service Account by its ID. This disables the Service Account but does not permanently delete it."""
    request = UpdateServiceAccountRequest(id=id, is_active=False)
    try:
        response = metadata_service.instance().UpdateServiceAccount(request)
    except TectonAPIValidationError as e:
        printer.safe_print(f"Failed to Deactivate Service Account: {e}", file=sys.stderr)
        sys.exit(1)
    printer.safe_print("Successfully deactivated Service Account")


@service_account.command()
@click.option("--json-out", default=False, is_flag=True, help="Format Output as JSON")
@click.option("-s", "--search-string", help="Search String to search by ID, Name or Description")
def list(json_out, search_string):
    """List Service Accounts."""
    request = GetServiceAccountsRequest()

    if search_string is not None:
        request.search = search_string

    response = metadata_service.instance().GetServiceAccounts(request)
    service_accounts = []

    if len(response.service_accounts) == 0:
        printer.safe_print("No Service Accounts Found")
        return

    for k in response.service_accounts:
        if json_out:
            account = {}
            account["name"] = k.name
            account["id"] = k.id
            account["description"] = k.description
            account["active"] = k.is_active
            account["createdBy"] = display_principal(k.created_by)
            service_accounts.append(account)
        else:
            printer.safe_print(f"{'Name: ': <15}{k.name}")
            printer.safe_print(f"{'ID: ': <15}{k.id}")
            if k.description:
                printer.safe_print(f"{'Description: ': <15}{k.description}")
            if k.created_by:
                printer.safe_print(f"{'Created By: ': <15}{display_principal(k.created_by, width=20)}")
            printer.safe_print(f"{'Active: ': <15}{k.is_active}")
            printer.safe_print()
    if json_out:
        printer.safe_print(json.dumps(service_accounts, indent=4), plain=True)


def _introspect(api_key):
    response = api_keys.introspect(api_key)
    return {
        "API Key ID": IdHelper.to_string(response.id),
        "Description": response.description,
        "Created by": response.created_by,
        "Active": response.active,
    }


@service_account.command()
@click.argument("api-key", required=True)
@click.option(
    "--json-output",
    is_flag=True,
    default=False,
    help="Whether the output is displayed in machine readable json format. Defaults to false.",
)
def introspect_api_key(api_key, json_output):
    """Introspect an API Key"""
    try:
        api_key_details = _introspect(api_key)
    except TectonNotFoundError:
        printer.safe_print(
            "API key cannot be found. Ensure you have the correct API Key. The key's secret value is different from the key's ID.",
            file=sys.stderr,
        )
        sys.exit(1)
    if json_output:
        for key in api_key_details.copy():
            snake_case = key.replace(" ", "_").lower()
            api_key_details[snake_case] = api_key_details.pop(key)
        printer.safe_print(f"{json.dumps(api_key_details)}", plain=True)
    else:
        pprint_dict(api_key_details, colwidth=16)


@service_account.command()
@click.argument("id", required=True)
@click.option("--json-out", default=False, is_flag=True, help="Format Output as JSON")
def create_secret(id, json_out):
    """Create a new Client Secret for the given Service Account."""
    try:
        request = CreateServiceAccountSecretRequest(id=id)
        response = metadata_service.instance().CreateServiceAccountSecret(request)
    except TectonAPIValidationError as e:
        printer.safe_print(f"Failed to create client secret for service account: {e}", file=sys.stderr)
        sys.exit(1)
    secret = response.secret
    if json_out:
        client_secret = {"secret_id": secret.secret_id, "secret": secret.secret}
        printer.safe_print(json.dumps(client_secret, indent=4), plain=True)
    else:
        printer.safe_print("Save this Client Secret - you will not be able to get it again.")
        printer.safe_print(f"Secret ID: {secret.secret_id}")
        printer.safe_print(f"Client Secret: {secret.secret}")


@service_account.command()
@click.argument("id", required=True)
@click.option("--json-out", default=False, is_flag=True, help="Format Output as JSON")
def list_secrets(id, json_out):
    """List Client Secrets of the Service Account."""
    try:
        request = ListServiceAccountSecretsRequest(id=id)
        response = metadata_service.instance().ListServiceAccountSecrets(request)
    except TectonAPIValidationError as e:
        printer.safe_print(f"Failed to list client secrets for service account: {e}", file=sys.stderr)
        sys.exit(1)

    if len(response.client_secrets) == 0:
        printer.safe_print("No Client Secret Found")
        return

    secrets = []
    for k in response.client_secrets:
        if json_out:
            secret = {"id": k.secret_id, "status": k.status, "createdAt": k.created_at}
            if k.updated_at:
                secret["updatedAt"] = k.updated_at
            secrets.append(secret)
        else:
            printer.safe_print(f"{'ID: ': <15}{k.secret_id}")
            printer.safe_print(f"{'Status: ': <15}{k.status}")
            printer.safe_print(f"{'Created At: ': <15}{k.created_at}")
            if k.updated_at:
                printer.safe_print(f"{'Updated At: ': <15}{k.updated_at}")
            printer.safe_print()
    if json_out:
        printer.safe_print(json.dumps(secrets, indent=4), plain=True)


@service_account.command()
@click.option("--service-account-id", required=True, help="ID of the Service Account")
@click.option("--secret-id", required=True, help="ID of the Client Secret")
@click.option("--json-out", default=False, is_flag=True, help="Format Output as JSON")
def activate_secret(service_account_id, secret_id, json_out):
    """Activate a Client Secret by Service Account ID and Secret ID."""
    request = ActivateServiceAccountSecretRequest(service_account_id=service_account_id, secret_id=secret_id)
    try:
        response = metadata_service.instance().ActivateServiceAccountSecret(request)
    except (TectonAPIValidationError, FailedPreconditionError, TectonNotFoundError) as e:
        printer.safe_print(f"Failed to activate Client Secret: {e}", file=sys.stderr)
        sys.exit(1)
    k = response.secret
    if json_out:
        secret = {"id": k.secret_id, "status": k.status, "createdAt": k.created_at}
        if k.updated_at:
            secret["updatedAt"] = k.updated_at
        printer.safe_print(json.dumps(secret, indent=4), plain=True)
    else:
        printer.safe_print("Successfully activated Client Secret")
        printer.safe_print(f"{'ID: ': <15}{k.secret_id}")
        printer.safe_print(f"{'Status: ': <15}{k.status}")
        printer.safe_print(f"{'Created At: ': <15}{k.created_at}")
        if k.updated_at:
            printer.safe_print(f"{'Updated At: ': <15}{k.updated_at}")
        printer.safe_print()


@service_account.command()
@click.option("--service-account-id", required=True, help="ID of the Service Account")
@click.option("--secret-id", required=True, help="ID of the Client Secret")
@click.option("--json-out", default=False, is_flag=True, help="Format Output as JSON")
def deactivate_secret(service_account_id, secret_id, json_out):
    """Deactivate a Client Secret by Service Account ID and Secret ID."""
    request = DeactivateServiceAccountSecretRequest(service_account_id=service_account_id, secret_id=secret_id)
    try:
        response = metadata_service.instance().DeactivateServiceAccountSecret(request)
    except (TectonAPIValidationError, FailedPreconditionError, TectonNotFoundError) as e:
        printer.safe_print(f"Failed to deactivate Client Secret: {e}", file=sys.stderr)
        sys.exit(1)
    k = response.secret
    if json_out:
        secret = {"id": k.secret_id, "status": k.status, "createdAt": k.created_at}
        if k.updated_at:
            secret["updatedAt"] = k.updated_at
        printer.safe_print(json.dumps(secret, indent=4), plain=True)
    else:
        printer.safe_print("Successfully deactivated Client Secret")
        printer.safe_print(f"{'ID: ': <15}{k.secret_id}")
        printer.safe_print(f"{'Status: ': <15}{k.status}")
        printer.safe_print(f"{'Created At: ': <15}{k.created_at}")
        if k.updated_at:
            printer.safe_print(f"{'Updated At: ': <15}{k.updated_at}")
        printer.safe_print()


@service_account.command()
@click.option("--service-account-id", required=True, help="ID of the Service Account")
@click.option("--secret-id", required=True, help="ID of the Client Secret")
def delete_secret(service_account_id, secret_id):
    """Permanently delete a Client Secret."""
    request = DeleteServiceAccountSecretRequest(service_account_id=service_account_id, secret_id=secret_id)
    try:
        metadata_service.instance().DeleteServiceAccountSecret(request)
    except (TectonAPIValidationError, FailedPreconditionError, TectonNotFoundError) as e:
        printer.safe_print(f"Failed to delete Client Secret: {e}", file=sys.stderr)
        sys.exit(1)
    printer.safe_print("Successfully deleted Client Secret")
