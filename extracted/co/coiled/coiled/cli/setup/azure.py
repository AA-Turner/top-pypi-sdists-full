import datetime
import json
import os
import shlex
import shutil
import subprocess
import sys
import time
from typing import Optional

import click
import httpx
import rich.prompt
from rich import print
from rich.live import Live
from rich.markup import escape
from rich.panel import Panel
from rich.prompt import Confirm

import coiled
from coiled.auth import get_local_user
from coiled.utils import get_temp_dir

from ..utils import CONTEXT_SETTINGS
from .util import SUCCESS_MESSAGE, setup_failure

try:
    from azure.core.exceptions import ClientAuthenticationError  # type: ignore
    from azure.identity import DefaultAzureCredential  # type: ignore
    from azure.mgmt.resource import ResourceManagementClient  # type: ignore
    from azure.mgmt.subscription import SubscriptionClient  # type: ignore

    AZURE_DEPS = True
except ImportError:
    ClientAuthenticationError = Exception
    AZURE_DEPS = False


REQUIRED_PROVIDERS = ("Microsoft.Network", "Microsoft.Compute", "Microsoft.Storage")
RG_ROLE_NAME = "Coiled Resource Group Role"
LOG_ROLE_NAME = "Coiled Log Access"


def rg_role_def(sub_id):
    return {
        "Name": f"{RG_ROLE_NAME}",
        "IsCustom": True,
        "Description": "Setup and ongoing Coiled permissions required at resource group scope",
        "Actions": [
            "Microsoft.Compute/*/read",
            "Microsoft.Compute/virtualMachines/delete",
            "Microsoft.Compute/virtualMachineScaleSets/*",
            "Microsoft.Network/*/read",
            "Microsoft.Network/applicationSecurityGroups/*",
            "Microsoft.Network/networkSecurityGroups/*",
            "Microsoft.Network/publicIPAddresses/delete",
            "Microsoft.Network/publicIPAddresses/write",
            "Microsoft.Network/virtualNetworks/subnets/join/action",
            "Microsoft.Network/virtualNetworks/subnets/write",
            "Microsoft.Network/virtualNetworks/write",
            "Microsoft.Storage/storageAccounts/managementPolicies/write",
            "Microsoft.Storage/storageAccounts/write",
        ],
        "NotActions": [],
        "AssignableScopes": [f"/subscriptions/{sub_id}"],
    }


def log_role_def(sub_id):
    return {
        "Name": f"{LOG_ROLE_NAME}",
        "IsCustom": True,
        "Description": "Role needs resource group scope for setup, then storage account scope for on-going",
        "Actions": ["Microsoft.Storage/storageAccounts/read", "Microsoft.Storage/storageAccounts/listkeys/action"],
        "NotActions": [],
        "AssignableScopes": [f"/subscriptions/{sub_id}"],
    }


def bash_script(coiled_account, sub_id, rg_name):
    header = f"""#!/bin/bash
COILED_ACCOUNT={coiled_account}
SUBSCRIPTION={sub_id}
RG_NAME={rg_name}"""

    body = """
# you can use any app name, but we'll default to a name that includes coiled account
APP_NAME="coiled-${COILED_ACCOUNT}-app"
RG_ID=/subscriptions/${SUBSCRIPTION}/resourceGroups/${RG_NAME}

# log in if necessary
az ad signed-in-user show 2>&1 1>\\dev\\null || az login

# create app, creds, and service principal
az ad app create --display-name $APP_NAME --query "id" | tr -d '"' > app-id.txt
az ad app credential reset --id $(cat app-id.txt) | tee app-creds.json
az ad sp create --id $(cat app-id.txt) --query "id" | tr -d '"' > sp-id.txt

# create roles
# TODO var substitution for subscription id in json role definitions
az role definition create --role-definition ./coiled-resource-group-role.json
az role definition create --role-definition ./coiled-log-access-role.json

# grant service principle access to the resource group
az role assignment create --role "Coiled Resource Group Role" --scope $RG_ID --assignee $(cat sp-id.txt)
az role assignment create --role "Coiled Log Access" --scope $RG_ID --assignee $(cat sp-id.txt)

# send creds to coiled

APP_PASS=$(jq -r '.password' app-creds.json)
APP_ID=$(jq -r '.appId' app-creds.json)
TENANT=$(jq -r '.tenant' app-creds.json)
SETUP_ENDPOINT=/api/v2/cloud-credentials/${COILED_ACCOUNT}/azure

coiled curl -X POST "${SETUP_ENDPOINT}" --json --data "{\\"credentials\\": {\\"tenant_id\\": \\"${TENANT}\\", \\"client_id\\": \\"${APP_ID}\\", \\"client_secret\\": \\"${APP_PASS}\\"}, \\"subscription_id\\":\\"${SUBSCRIPTION}\\",\\"resource_group_name\\":\\"${RG_NAME}\\"}"
"""  # noqa: E501

    return f"{header}\n{body}"


@click.option(
    "--subscription",
    default=None,
    help=(
        "Azure subscription to use, specified by ID. "
        "(You'll be prompted with options not specified and more than one subscription is found)."
    ),
)
@click.option(
    "--resource-group",
    default=None,
    help=(
        "Azure resource group to use. Note that all permissions are scoped to the resource group."
        "(You'll be prompted with options not specified and more than one resource group is found)."
    ),
)
@click.option("--region", default=None, help="Default region for Coiled to use.")
@click.option(
    "--account",
    "--workspace",
    default=None,
    help=(
        "Coiled workspace (uses default workspace if not specified). "
        "Note: ``--account`` is deprecated, please use ``--workspace`` instead."
    ),
)
@click.option(
    "--iam-user",
    default=None,
    help=(
        "Name of enterprise application/service principal to create. "
        "By default, we'll use ``coiled-<coiled workspace slug>-app``."
    ),
)
@click.option(
    "--keep-existing-access",
    default=False,
    is_flag=True,
    help="If there's existing enterprise application, add new secret rather than replacing any existing ones.",
)
@click.option(
    "--save-script",
    is_flag=True,
    default=False,
    hidden=True,
)
@click.option(
    "--ship-token",
    is_flag=True,
    default=False,
    help=(
        "Instead of using a service principal to grant long-term access to your Azure account, this will ship "
        "(and refresh) temporary OAuth tokens so that Coiled can operate in your Azure account as you. "
        "Not recommended for long-term Coiled use, but can be helpful if you don't want to (or can't) create a "
        "service principal for Coiled to use."
    ),
)
@click.command(context_settings=CONTEXT_SETTINGS)
def azure_setup(subscription, resource_group, region, account, iam_user, keep_existing_access, save_script, ship_token):
    print(
        "Coiled on Azure is currently in [bold]public beta[/bold], "
        "please contact [link]support@coiled.io[/link] if you have any questions or problems."
    )
    local_user = get_local_user()

    try:
        with coiled.Cloud(workspace=account) as cloud:
            coiled_account = account or cloud.default_workspace
    except PermissionError as e:
        print(e)
        return

    coiled.add_interaction(
        action="CliSetupAzure",
        success=True,
        local_user=local_user,
        # use keys that match the cli args
        region=region,
        save_script=save_script,
        ship_token=ship_token,
    )

    has_requirements = True
    has_az_cli = get_cli_path() is not None
    if not AZURE_DEPS:
        print()
        print(
            "[red]Missing requirement[/red] Azure Python libraries are not installed.\n"
            "You can install using [bold]pip[/bold]:\n"
            "  [green]pip install 'coiled\\[azure]'[/green]\n"
            "or [bold]conda[/bold]:\n"
            "  [green]conda install azure-identity azure-mgmt-resource azure-mgmt-subscription -c conda-forge[/green]"
        )
        has_requirements = False

    if not ship_token and not has_az_cli:
        print()
        print("[red]Missing requirement[/red] Unable to find the [green]az[/green] Azure CLI, which this script uses.")
        print(
            "See [link=https://learn.microsoft.com/en-us/cli/azure/install-azure-cli]"
            "https://learn.microsoft.com/en-us/cli/azure/install-azure-cli[/link] "
            "for Azure CLI installation instructions."
        )
        has_requirements = False

    if not has_requirements:
        setup_failure(f"missing requirements:cli={has_az_cli},deps={AZURE_DEPS}", backend="azure")
        return

    creds = DefaultAzureCredential()  # pyright: ignore[reportPossiblyUnboundVariable]
    if not whoami(creds):
        print()
        print("[red]Unable to find local Azure credentials")
        print("We recommend using the Azure CLI to configure your local Azure credentials")
        if not has_az_cli:
            print(
                "See [link=https://learn.microsoft.com/en-us/cli/azure/install-azure-cli]"
                "https://learn.microsoft.com/en-us/cli/azure/install-azure-cli[/link] "
                "for Azure CLI installation instructions."
            )
            print("Once you have the Azure CLI installed, you can run this to configure local credentials:")
        else:
            print("Run this command to configure local credentials:")

        print("  [green]az login")
        setup_failure("no local credentials", backend="azure")
        return

    sub_id = subscription or get_subscription(creds)

    if not sub_id:
        return

    rg_name, rg_location, rg_id = get_rg(creds, sub_id, rg_name=resource_group or "")
    region = region or rg_location

    if not rg_id:
        setup_failure("no resource group selected", backend="azure")
        return

    print(
        f"Coiled account [green]{coiled_account}[/green] will be configured to use "
        f"resource group [green]{rg_name}[/green] "
        f"with [green]{region}[/green] as the default region\n"
    )

    if ship_token:
        enable_providers(creds, sub_id)
        ship_token_creds(
            local_credentials=creds, coiled_account=coiled_account, sub_id=sub_id, rg_name=rg_name, region=region
        )
        return

    if save_script:
        path = "coiled-resource-group-role.json"
        with open(path, "w") as f:
            json.dump(rg_role_def(sub_id), f)
            print(f"Saved [bold]{RG_ROLE_NAME}[/bold] as [green]{path}")
        path = "coiled-log-access-role.json"
        with open(path, "w") as f:
            json.dump(log_role_def(sub_id), f)
            print(f"Saved [bold]{LOG_ROLE_NAME}[/bold] as [green]{path}")
        path = "coiled-setup.sh"
        with open(path, "w") as f:
            f.write(bash_script(coiled_account, sub_id, rg_name))
            print(f"Saved [bold]Coiled setup script[/bold] as [green]{path}")

    else:
        app_name = iam_user or f"coiled-{coiled_account}-app"
        try:
            if not setup_with_service_principal(
                creds, app_name, sub_id, rg_name, rg_id, coiled_account, region, keep_existing_keys=keep_existing_access
            ):
                coiled.add_interaction(action="CoiledSetup", success=False)
        except Exception as e:
            error_message = str(e)
            coiled.add_interaction(action="CoiledSetup", success=False, error_message=error_message)
            print()
            print("[red]There was an error setting up Coiled to use your Azure account:\n")
            print(error_message)


def setup_with_service_principal(
    creds, app_name, sub_id, rg_name, rg_id, coiled_account, region, keep_existing_keys: bool = False
):
    prompt = f"Create [green]{app_name}[/green] service principal and grant Coiled access to your Azure subscription?"
    if not Confirm.ask(prompt, default=True):
        coiled.add_interaction(action="prompt:Setup_Azure", success=False)
        return False

    enable_providers(creds, sub_id)

    print(f"  [bright_black]Creating enterprise application {app_name}...")
    app_json = az_cli_wrapper(f"az ad app create --display-name '{app_name}'")

    app_info = json.loads(app_json)
    app_id = app_info["appId"]

    print(f"  [bright_black]Resetting/retrieving credentials for {app_name} ({app_id})...")
    cred_reset_opts = "--append" if keep_existing_keys else ""
    app_creds_json = az_cli_wrapper(f"az ad app credential reset --id {app_id} {cred_reset_opts}")
    app_creds = json.loads(app_creds_json)

    print(f"  [bright_black]Creating service principal for {app_name} ({app_id})...")
    sp_id = strip_output(
        az_cli_wrapper(
            f"az ad sp create --id {app_id} --query id",
            command_if_exists=f"az ad sp list --display-name '{app_name}' --query '[0].id'",
        )
    )

    print(f"  [bright_black]Creating/updating role definition {RG_ROLE_NAME}...")

    with get_temp_dir() as dir:
        role_def_path = os.path.join(dir, "role-def.json")
        with open(role_def_path, "w") as f:
            json.dump(rg_role_def(sub_id), f)
        log_role_def_path = os.path.join(dir, "log-role-def.json")
        with open(log_role_def_path, "w") as f:
            json.dump(log_role_def(sub_id), f)

        az_cli_wrapper(
            f"az role definition create --role-definition @{role_def_path}",
            command_if_exists=f"az role definition update --role-definition @{role_def_path}",
        )
        print(f"  [bright_black]Creating/updating role definition {LOG_ROLE_NAME}...")
        az_cli_wrapper(
            f"az role definition create --role-definition @{log_role_def_path}",
            command_if_exists=f"az role definition update --role-definition @{log_role_def_path}",
        )

    print(f"  [bright_black]Assigning '{RG_ROLE_NAME}' role to service principal on '{rg_name}' resource group...")
    az_cli_wrapper(f"az role assignment create --role '{RG_ROLE_NAME}' --scope {rg_id} --assignee {sp_id}")
    print(f"  [bright_black]Assigning '{LOG_ROLE_NAME}' role to service principal on '{rg_name}' resource group...")
    az_cli_wrapper(f"az role assignment create --role '{LOG_ROLE_NAME}' --scope {rg_id} --assignee {sp_id}")

    creds_to_submit = {
        "tenant_id": app_creds["tenant"],
        "client_id": app_creds["appId"],
        "client_secret": app_creds["password"],
    }

    print("Sending Azure credentials to Coiled... ", end="")
    submit_azure_credentials(
        coiled_account=coiled_account,
        sub_id=sub_id,
        rg_name=rg_name,
        region=region,
        creds_to_submit=creds_to_submit,
    )
    print("done!")
    print()
    print()
    print(SUCCESS_MESSAGE)

    coiled.add_interaction(action="CoiledSetup", success=True)

    return True


def submit_azure_credentials(coiled_account, sub_id, rg_name, region, creds_to_submit, check_after: bool = False):
    with coiled.Cloud(account=coiled_account) as cloud:
        setup_endpoint = f"/api/v2/cloud-credentials/{coiled_account}/azure"
        setup_data = {
            "credentials": creds_to_submit,
            "subscription_id": sub_id,
            "resource_group_name": rg_name,
            "default_region": region,
        }
        cloud._sync_request(setup_endpoint, method="POST", handle_confirm=True, json=setup_data)

        if check_after:
            print("Coiled Azure credentials...")
            # did it work?
            print(cloud._sync_request(setup_endpoint))


def strip_output(output: str) -> str:
    return output.strip(' \n"')


def get_cli_path() -> Optional[str]:
    return shutil.which("az")


def az_cli_wrapper(
    command: str,
    command_if_exists: str = "",
    show_stdout: bool = False,
    interactive: bool = False,
):
    split_command = shlex.split(command)
    if split_command and split_command[0] == "az":
        del split_command[0]
    az_path = get_cli_path() or "az"
    split_command = [az_path] + split_command
    p = subprocess.run(split_command, capture_output=not interactive)

    stdout = p.stdout.decode(encoding=coiled.utils.get_encoding()) if p.stdout else None
    stderr = p.stderr.decode(encoding=coiled.utils.get_encoding(stderr=True)) if p.stderr else None

    if show_stdout:
        print(stdout)

    if not interactive and p.returncode:
        if stderr and "already" in stderr:
            if command_if_exists:
                return az_cli_wrapper(command_if_exists)

            # TODO is this always fine to ignore because it means item exists?
            return ""

        else:
            print(f"[red]az returned an error when running command `{shlex.join(split_command)}`:")
            print(Panel(escape(stderr or "")))
            setup_failure(f"az error while running {shlex.join(split_command)}, {stderr}", backend="azure")
            sys.exit(1)

    return stdout or ""


def choice_prompt(choices, prompt, exit_return=None):
    prompt_choices = [str(i) for i in range(1, len(choices) + 1)]
    for i, (_, display) in enumerate(choices):
        print(f"{i + 1}. {display}")

    exit_choice = 0
    prompt_choices.append(str(exit_choice))
    print(f"{exit_choice}. [red]Exit setup")

    print()
    choice = rich.prompt.IntPrompt.ask(prompt, choices=prompt_choices)
    if choice == exit_choice:
        return exit_return
    else:
        sub_id, _ = choices[choice - 1]
        return sub_id


def get_subscription(credentials):
    sub_client = SubscriptionClient(credentials)  # pyright: ignore[reportPossiblyUnboundVariable]

    subscriptions = [
        (subscription.display_name, subscription.subscription_id) for subscription in sub_client.subscriptions.list()
    ]

    if not subscriptions:
        print("No Azure subscriptions were found")
        return None
    elif len(subscriptions) > 1:
        print("Multiple Azure subscriptions were found.")
        choices = [(id, f"{name} (id [green]{id}[/green])") for name, id in subscriptions]
        sub_id = choice_prompt(choices, "Please select one of the available subscriptions for Coiled to use")

    else:
        _sub_name, sub_id = subscriptions[0]

    return sub_id


def get_rg(credentials, sub_id: str, rg_name: str):
    resource_client = ResourceManagementClient(credentials, sub_id)  # pyright: ignore[reportPossiblyUnboundVariable]

    resource_groups = [(rg.name, rg.location, rg.id) for rg in resource_client.resource_groups.list()]

    if not resource_groups:
        print(
            "[red]No Resource Groups were found[/red]\n\n"
            "To run Coiled in your Azure subscription, you'll need to create a Resource Group.\n"
            "You can do this in the Azure Portal at:\n"
            "  https://portal.azure.com/#create/Microsoft.ResourceGroup\n\n"
            "Resource Groups don't themselves cost any money or do anything, they're just how Azure groups resources.\n"
            "You'll need to select a region, this usually has no effect though, "
            "and it doesn't restrict the region of the clusters you can deploy with Coiled.\n\n"
            "After you create a Resource Group, rerun [green]coiled setup azure[/green] to continue."
        )
        return None, None, None
    elif len(resource_groups) > 1:
        if rg_name:
            match = [rg for rg in resource_groups if rg[0] and rg[0].lower() == rg_name.lower()]
            if match:
                return match[0]
            else:
                print(f"No resource group matches [green]{rg_name}")

        print("Multiple Azure resource groups were found.")
        choices = [((name, location, rg_id), f"{name} ({location})") for name, location, rg_id in resource_groups]
        return choice_prompt(
            choices,
            "Please select one of the available resource groups for Coiled to use",
            exit_return=(None, None, None),
        )

    else:
        return resource_groups[0]


def enable_providers(credentials, sub_id):
    resource_client = ResourceManagementClient(credentials, sub_id)  # pyright: ignore[reportPossiblyUnboundVariable]
    registered = {
        provider: resource_client.providers.get(provider).registration_state == "Registered"
        for provider in REQUIRED_PROVIDERS
    }

    if not all(registered.values()):
        print(f"Registering required providers in Azure Subscription {sub_id}...")
        print("(there's no associated cost, this just enables these services for use in the Azure subscription)")

        for provider in REQUIRED_PROVIDERS:
            if registered.get(provider):
                print(f"  [bright_black]{provider} already registered")
            else:
                print(f"  Enabling [green]{provider}[/green]... ", end="")
                resource_client.providers.register(provider)
                print("successfully registered!")
        print()


def get_temp_delegation_display(
    azure_user, coiled_account, sub_id, rg_name, expiration, last_refresh, active: bool = True
):
    now = datetime.datetime.now(tz=datetime.timezone.utc)
    remaining_time = expiration - now
    refresh_since = now - last_refresh

    expiration_message = (
        f"in [bold]{remaining_time.seconds // 60} minutes[/bold]" if active else f"at [bold]{expiration:%c %Z}[/bold]"
    )
    last_refresh_message = (
        f"{refresh_since.seconds // 60}m{refresh_since.seconds % 60}s ago at {last_refresh:%c %Z}"
        if active
        else f"{last_refresh:%c %Z}"
    )

    status = "[green]active[/green]" if active else "[red]inactive[/red]"

    return Panel(
        f"""Access delegation is [bold]{status}[/bold] for Azure!

Coiled is now able to temporarily act as you to create and manage resources in your resource group.

Access will expire {expiration_message} if not refreshed.
  Last refresh:  {last_refresh_message}

Azure user principal:  [bold]{azure_user["userPrincipalName"]}[/bold]
                       (id {azure_user["id"]})
Azure resource group:  [bold]{rg_name}[/bold]
                       (subscription {sub_id})
Coiled workspace:      [bold]{coiled_account}[/bold]

Use Control-C to stop refreshing access delegation""",
        width=80,
    )


def get_temporary_creds_to_submit(local_credentials):
    scope = "https://management.azure.com/.default"
    token_creds = local_credentials.get_token(scope)

    creds_to_submit = {
        "token_scope": scope,
        "token_value": token_creds.token,
        "token_expiration": token_creds.expires_on,
    }
    expiration = datetime.datetime.fromtimestamp(token_creds.expires_on, tz=datetime.timezone.utc)

    return creds_to_submit, expiration


def ship_token_creds(local_credentials, coiled_account, sub_id, rg_name, region):
    azure_user = whoami(local_credentials)

    creds_to_submit, expiration = get_temporary_creds_to_submit(local_credentials)
    last_refresh = datetime.datetime.now(tz=datetime.timezone.utc)
    submit_azure_credentials(
        coiled_account=coiled_account,
        sub_id=sub_id,
        rg_name=rg_name,
        region=region,
        creds_to_submit=creds_to_submit,
        check_after=False,
    )
    display = get_temp_delegation_display(
        azure_user=azure_user,
        coiled_account=coiled_account,
        sub_id=sub_id,
        rg_name=rg_name,
        expiration=expiration,
        last_refresh=last_refresh,
    )

    with Live(display) as live:
        try:
            while True:
                # update temporary credentials if they'll expire within 7 minutes
                soon = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=7)
                if expiration < soon:
                    creds_to_submit, expiration = get_temporary_creds_to_submit(local_credentials)
                    last_refresh = datetime.datetime.now(tz=datetime.timezone.utc)
                    submit_azure_credentials(
                        coiled_account=coiled_account,
                        sub_id=sub_id,
                        rg_name=rg_name,
                        region=region,
                        creds_to_submit=creds_to_submit,
                        check_after=False,
                    )

                display = get_temp_delegation_display(
                    azure_user=azure_user,
                    coiled_account=coiled_account,
                    sub_id=sub_id,
                    rg_name=rg_name,
                    expiration=expiration,
                    last_refresh=last_refresh,
                )
                live.update(display)
                time.sleep(0.5)

        except KeyboardInterrupt:
            display = get_temp_delegation_display(
                azure_user=azure_user,
                coiled_account=coiled_account,
                sub_id=sub_id,
                rg_name=rg_name,
                expiration=expiration,
                last_refresh=last_refresh,
                active=False,
            )
            live.update(display)
            live.stop()
            print(
                "Temporary access to your Azure resources will no longer be refreshed.\n"
                f"Unless you restart the process to refresh access, any running clusters will be automatically stopped "
                f"5 minutes before the current access token expires at {expiration:%c %Z}."
            )
            return


def whoami(local_credentials):
    try:
        # note that this prints error if there aren't creds
        token_creds = local_credentials.get_token("https://graph.microsoft.com/.default")
    except ClientAuthenticationError:
        return None
    with httpx.Client(http2=True) as client:
        result = client.get(
            "https://graph.microsoft.com/v1.0/me?$select=id,userPrincipalName",
            headers={"Authorization": f"Bearer {token_creds.token}"},
        )
    return result.json()
