import json
import os
import shlex
import shutil
import subprocess
import sys
import time
from typing import List, Optional
from urllib.parse import quote

import click
import dask.config
from rich import print
from rich.markup import escape
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table

import coiled
from coiled.core import _parse_gcp_creds
from coiled.errors import ServerError
from coiled.utils import get_temp_dir, parse_gcp_region_zone

from ...auth import get_local_user
from ..utils import CONTEXT_SETTINGS
from .util import setup_failure

# names to use when tracking actions
ACTION_INIT = "init"
ACTION_CREATE_GAR = "gar:create"
ACTION_BIND_GAR = "gar:policy-binding"
ACTION_BIND_POLICY = "policy-binding"
ACTION_CREATE_ROLE = "roles-create"
ACTION_LIST_KEYS = "keys-list"
ACTION_ENABLE_SERVICE = "services-enable"
ACTION_CREATE_SA = "service-accounts-create"
ACTION_ACTIVATE_SA = "activate-servicer-account"
ACTION_CREATE_KEY = "keys-create"
ACTION_ORG_POLICY_DESCRIBE = "org-policy:DESCRIBE"
ACTION_ORG_POLICY_DELETE = "org-policy:delete"
ACTION_ORG_POLICY_SET = "org-policy:set"


IAM_LOG_SINK_CONSTRAINT = "iam.allowedPolicyMemberDomains"

CONTROL_PLANE_ROLE = """
title: coiled
description: used by Coiled control-plane for creating infrastructure and clusters
stage: GA
includedPermissions:
- bigquery.datasets.create
- bigquery.jobs.create
- bigquery.datasets.get
- bigquery.datasets.update
- bigquery.tables.getData
- compute.acceleratorTypes.list
- compute.addresses.list
- compute.disks.create
- compute.disks.delete
- compute.disks.list
- compute.disks.useReadOnly
- compute.firewalls.create
- compute.firewalls.delete
- compute.firewalls.get
- compute.firewalls.list
- compute.globalOperations.get
- compute.globalOperations.getIamPolicy
- compute.globalOperations.list
- compute.images.create
- compute.images.delete
- compute.images.get
- compute.images.list
- compute.images.setLabels
- compute.images.useReadOnly
- compute.instances.create
- compute.instances.delete
- compute.instances.get
- compute.instances.getSerialPortOutput
- compute.instances.list
- compute.instances.setLabels
- compute.instances.setMetadata
- compute.instances.setServiceAccount
- compute.instances.setTags
- compute.instanceTemplates.create
- compute.instanceTemplates.delete
- compute.instanceTemplates.get
- compute.instanceTemplates.useReadOnly
- compute.machineTypes.get
- compute.machineTypes.list
- compute.networks.create
- compute.networks.delete
- compute.networks.get
- compute.networks.list
- compute.networks.updatePolicy
- compute.projects.get
- compute.projects.setCommonInstanceMetadata
- compute.regionOperations.get
- compute.regionOperations.list
- compute.regions.get
- compute.regions.list
- compute.routers.create
- compute.routers.delete
- compute.routers.get
- compute.routers.list
- compute.routers.update
- compute.routes.delete
- compute.routes.list
- compute.subnetworks.create
- compute.subnetworks.delete
- compute.subnetworks.get
- compute.subnetworks.getIamPolicy
- compute.subnetworks.list
- compute.subnetworks.use
- compute.subnetworks.useExternalIp
- compute.zoneOperations.get
- compute.zoneOperations.list
- compute.zones.list
- iam.serviceAccounts.actAs
- logging.buckets.create
- logging.buckets.get
- logging.buckets.list
- logging.logEntries.create
- logging.logEntries.list
- logging.sinks.create
- logging.sinks.get
- logging.sinks.list
- storage.buckets.create
- storage.buckets.get
- storage.objects.create
- storage.objects.get
- storage.objects.list
- storage.objects.update
"""


DATA_ROLE = """
title: coiled-data
description: service account attached to cluster instances for data access
stage: GA
includedPermissions:
- logging.logEntries.create
- storage.buckets.get
- storage.buckets.create
- storage.objects.create
- storage.objects.get
- storage.objects.list
- storage.objects.update
"""


def get_gcloud_path() -> Optional[str]:
    return shutil.which("gcloud")


def gcloud_wrapper(
    command: List[str],
    show_stdout: bool = False,
    interactive: bool = False,
    error_handler=None,
    action_name: Optional[str] = None,
    continue_on_error: bool = False,
):
    if command and command[0] == "gcloud":
        del command[0]
    gcloud_path = get_gcloud_path() or "gcloud"
    command = [gcloud_path] + command
    p = subprocess.run(command, capture_output=not interactive)

    stdout = p.stdout.decode(encoding=coiled.utils.get_encoding()) if p.stdout else None
    stderr = p.stderr.decode(encoding=coiled.utils.get_encoding(stderr=True)) if p.stderr else None

    if action_name:
        coiled.add_interaction(
            action=f"gcloud:{action_name}",
            success=p.returncode == 0,
            command=shlex.join(command),
            return_code=p.returncode,
            additional_text=stdout or None,
            error_message=stderr or None,
        )

    if show_stdout:
        print(stdout)

    if p.returncode:
        if stderr and "already exist" in stderr:
            pass

        elif error_handler and error_handler(stderr):
            # error_handler returns True if error was handled
            return False

        elif continue_on_error:
            return False

        else:
            print(f"[red]gcloud returned an error when running command `{shlex.join(command)}`:")
            print(Panel(escape(stderr or "")))
            setup_failure(f"gcloud error while running {shlex.join(command)}, {stderr}", backend="gcp")
            sys.exit(1)

    return True


def gcloud_enable_service(service: str, project: str):
    def enable_error_handler(stderr: str):
        if "Billing must be enabled" in stderr:
            print(f"[red]We couldn't enable {service} because of an error related to Google Cloud billing:")
            print(Panel(escape(stderr)))
            print("To address this error, please link this project to a Google Cloud billing account at")
            print()
            print(f"[link]https://console.cloud.google.com/billing?project={project}")
            print()
            print("and then re-run [green]coiled setup gcp[/green]")
            # we've handled the error
            setup_failure("Billing not enabled", backend="gcp")
            return True

        return False

    return gcloud_wrapper(
        ["services", "enable", service, "--project", project],
        error_handler=enable_error_handler,
        action_name=f"{ACTION_ENABLE_SERVICE}:{service}",
    )


def gcloud_make_key(iam_email: str, key_path: str):
    gcloud_path = get_gcloud_path() or "gcloud"
    command = [gcloud_path, "iam", "service-accounts", "keys", "create", key_path, "--iam-account", iam_email]
    p = subprocess.run(command, capture_output=True)

    stdout = p.stdout.decode(encoding=coiled.utils.get_encoding())
    stderr = p.stderr.decode(encoding=coiled.utils.get_encoding(stderr=True))

    coiled.add_interaction(
        action=f"gcloud:{ACTION_CREATE_KEY}",
        success=p.returncode == 0,
        command=shlex.join(command),
        return_code=p.returncode,
        additional_text=stdout or None,
        error_message=stderr or None,
    )

    if p.returncode:
        print("[red]An error occurred when attempting to create a key for the IAM account[/red]")
        print(escape(stderr))
        if "service-accounts.keys.create" in stderr and "FAILED_PRECONDITION" in stderr:
            print("One possibility is that you already have 10 keys for this account. Existing keys:")
            print()
            gcloud_wrapper(
                ["iam", "service-accounts", "keys", "list", f"--iam-account={iam_email}"],
                show_stdout=True,
                action_name=ACTION_LIST_KEYS,
            )
            print()
            print("You can delete individual keys by running:")
            print()
            print(f"[green]gcloud iam service-accounts keys delete --iam-account={iam_email} [bold]<key_id>[/bold]")
            setup_failure(f"Service account key creation failed {stderr}", backend="gcp")
            return False
        else:
            raise RuntimeError()

    return True


def get_gcloud_config(key) -> Optional[str]:
    gcloud_path = get_gcloud_path()
    if not gcloud_path:
        return None
    p = subprocess.run([gcloud_path, "config", "get", key], capture_output=True)

    if not p.returncode:
        return p.stdout.decode(encoding=coiled.utils.get_encoding()).strip()
    else:
        print(escape(p.stderr.decode(encoding=coiled.utils.get_encoding(stderr=True))))
        return None


def get_gcloud_json(command: List[str]):
    p = subprocess.run(command, capture_output=True)

    if not p.returncode:
        text = p.stdout.decode(encoding=coiled.utils.get_encoding()).strip()
        return json.loads(text)
    else:
        print(escape(p.stderr.decode(encoding=coiled.utils.get_encoding(stderr=True))))
        return None


def get_existing_org_policy(constraint: str, project: str):
    command = [
        get_gcloud_path(),
        "org-policies",
        "describe",
        constraint,
        f"--project={project}",
        "--format=json",
        "--quiet",
    ]
    p = subprocess.run(command, capture_output=True, stdin=None)

    if not p.returncode:
        text = p.stdout.decode(encoding=coiled.utils.get_encoding()).strip()
        return True, json.loads(text)
    else:
        stderr = p.stderr.decode(encoding=coiled.utils.get_encoding(stderr=True))
        coiled.add_interaction(
            action=f"gcloud:{ACTION_ORG_POLICY_DESCRIBE}",
            success=False,
            command=shlex.join(command),
            return_code=p.returncode,
            additional_text=None,
            error_message=stderr or None,
        )

        if "NOT_FOUND" in stderr:
            return True, {}

    # if we get here, then we failed in some way, so return False to indicate that we shouldn't try to adjust
    # the constraint
    return False, {}


def remove_policy_etags(policy: dict):
    # recursively remove etag and updateTime from anywhere in the policy dict
    return {
        key: remove_policy_etags(val) if isinstance(val, dict) else val
        for key, val in policy.items()
        if key not in ("etag", "updateTime")
    }


def set_project_org_policy(constraint: str, policy: dict, project: str):
    # setting to empty policy means we want to delete existing policy
    if policy == {}:
        gcloud_wrapper(
            ["gcloud", "org-policies", "delete", constraint, f"--project={project}", "--quiet"],
            continue_on_error=True,
            action_name=ACTION_ORG_POLICY_DELETE,
        )
    else:
        with get_temp_dir() as dir:
            path = os.path.join(dir, "org-policy.json")
            with open(path, "w") as f:
                json.dump(policy, f)
            gcloud_wrapper(
                ["gcloud", "org-policies", "set-policy", path, f"--project={project}", "--quiet"],
                continue_on_error=True,
                action_name=ACTION_ORG_POLICY_SET,
            )


def set_allow_all_log_sink_constraint(project: str):
    temp_allow_policy = {
        "name": f"projects/{project}/policies/{IAM_LOG_SINK_CONSTRAINT}",
        "spec": {"rules": [{"allowAll": True}]},
    }
    set_project_org_policy(
        constraint=f"constraint/{IAM_LOG_SINK_CONSTRAINT}", project=project, policy=temp_allow_policy
    )


def gcloud_check_gar(gar_name: str, region: str) -> bool:
    gcloud_path = get_gcloud_path()
    if not gcloud_path:
        return False
    p = subprocess.run(
        [gcloud_path, "artifacts", "repositories", "describe", gar_name, "--location", region], capture_output=True
    )

    return "format: DOCKER" in p.stdout.decode(encoding=coiled.utils.get_encoding())


def gcloud_wait_for_repo(region: str, key_path: str) -> bool:
    # it takes a while to give the service account (which we created)
    # access to the artifact registry
    # this function waits (with timeout) until that's ready

    # keep track of currently active account (for local `gcloud`) so we can switch back
    previous_account = get_gcloud_config("account")

    # activate the service account we made --
    # subsequent `gcloud` calls with be using those creds
    gcloud_wrapper(
        ["auth", "activate-service-account", "--key-file", key_path],
        action_name=ACTION_ACTIVATE_SA,
    )
    gcloud_path = get_gcloud_path()
    if not gcloud_path:
        return False
    success = False
    command = [gcloud_path, "artifacts", "repositories", "describe", "coiled", "--location", region]
    t0 = time.time()

    # keep checking if service account has access to artifact registry
    while True:
        p = subprocess.run(command, capture_output=True)

        if "format: DOCKER" in p.stdout.decode(encoding=coiled.utils.get_encoding()):
            success = True
            break
        elif "PERMISSION_DENIED" in p.stderr.decode(encoding=coiled.utils.get_encoding(stderr=True)):
            if time.time() < t0 + 180:  # wait for up to three minutes
                time.sleep(10)  # 10s delay between retries
                continue
            else:
                break
        else:
            print("[red]An unexpected error occurred while waiting for Google Artifact Registry to be ready.")
            print(Panel(escape(p.stderr.decode(encoding=coiled.utils.get_encoding(stderr=True)))))
            break

    # switch back to the user's account for local `gcloud` commands
    gcloud_wrapper(["config", "set", "account", str(previous_account)])
    return success


def wait_on_component_ready(*, route: str, component_name: str, create_json: dict, cloud: "coiled.Cloud") -> bool:
    print(f"Waiting for {component_name.lower()} to be created (this may take a while)...")
    try:
        infra = cloud._sync_request(
            route,
            method="POST",
            json=create_json,
            json_result=True,
        )
        component = infra.get("component", {})
        while component.get("state") != "created":
            time.sleep(2)
            infra = cloud._sync_request(
                route,
                method="GET",
                json_result=True,
            )
            if isinstance(infra, list):
                component = next(
                    (
                        inf.get("component", {})
                        for inf in infra
                        # Compare all non-list keys in create_json. We skip list keys,
                        # because they can be different in the response (e.g., subnet CIDRs).
                        if all(
                            inf[key] == create_json[key] or isinstance(create_json[key], list) for key in create_json
                        )
                    ),
                    {},
                )
            else:
                component = infra.get("component", {})
            if component.get("state") == "error":
                reason = component.get("reason", "")
                print(f"[red]Error creating {component_name.lower()}.\n{reason}[/red]")
                setup_failure(
                    f"{component_name} creation failed {reason}",
                    backend="gcp",
                )
                return False
    except ServerError as e:
        print(f"[red]Error creating {component_name.lower()}: {e}[/red]")
        setup_failure(f"{component_name} creation failed {e}", backend="gcp")
        return False

    return True


@click.option(
    "--region",
    default="us-east1",
    help="GCP region to use when setting up your VPC/subnets",
)
@click.option(
    "--enable-gar",
    default=False,
    is_flag=True,
    help="Configure Google Artifact Registry for use with Coiled",
)
@click.option(
    "--enable-log-sink-permissions/--ignore-log-sink-permissions",
    default=True,
    is_flag=True,
    help="Temporarily adjust organization policy so that service account for log sink can be granted permission",
)
@click.option(
    "--manual-final-setup",
    default=False,
    is_flag=True,
    help="Don't automatically send credentials to Coiled, finish setup manually in the web UI",
)
@click.option(
    "--quotas",
    default=False,
    is_flag=True,
    help="Check and potentially request GCP quota increases",
)
@click.option(
    "--quota-link",
    default=False,
    is_flag=True,
    help="Just show link to GCP Console quota page",
)
@click.option(
    "--account",
    "--workspace",
    default=None,
    help="Coiled workspace that will be configured. By default, uses your default Coiled workspace."
    " Note: --account is deprecated, please use --workspace instead.",
)
@click.option(
    "--export",
    default="",
    type=click.Choice(["", "role", "data-role"]),
    help="Allows you to export role definitions as files",
)
@click.option(
    "--iam-user",
    default="coiled",
    help="Name for role and user to create",
)
@click.option(
    "-y",
    "--yes",
    default=False,
    is_flag=True,
    help="Don't prompt for confirmation, just do it!",
)
@click.command(context_settings=CONTEXT_SETTINGS)
def gcp_setup(
    region,
    enable_gar,
    enable_log_sink_permissions,
    manual_final_setup,
    quotas,
    quota_link,
    export,
    iam_user,
    yes,
    account,
):
    do_setup(
        region=region,
        enable_gar=enable_gar,
        enable_log_sink_permissions=enable_log_sink_permissions,
        manual_final_setup=manual_final_setup,
        quotas=quotas,
        quota_link=quota_link,
        export=export,
        iam_user=iam_user,
        yes=yes,
        account=account,
    )


def do_setup(
    region=None,
    enable_gar=False,
    enable_log_sink_permissions=True,
    manual_final_setup=False,
    quotas=False,
    quota_link=False,
    export=None,
    iam_user="coiled",
    yes=False,
    account=None,
) -> bool:
    local_user = get_local_user()

    coiled.add_interaction(
        action="CliSetupGcp",
        success=True,
        local_user=local_user,
        # use keys that match the cli args
        region=region,
        export=export,
        quotas=quotas,
        yes=yes,
    )

    try:
        with coiled.Cloud(workspace=account) as cloud:
            coiled_account = account or cloud.default_workspace
    except PermissionError as e:
        print(e)
        return False

    if export:
        export_path = os.path.abspath(f"coiled-{export}.yaml")

        if export == "role":
            with open(export_path, "w") as f:
                f.write(CONTROL_PLANE_ROLE)
            print(f"Exported Coiled role definition to {export_path}")

        elif export == "data-role":
            with open(export_path, "w") as f:
                f.write(DATA_ROLE)
            print(f"Exported Coiled 'data access' role definition to {export_path}")

        return False

    gcloud_path = get_gcloud_path()
    if not gcloud_path:
        print("\n[red]Missing:[/red] The gcloud CLI tool is required for automatic setup.\n")
        if os.path.exists(os.path.join(sys.prefix, "conda-meta")):
            print(
                "Install gcloud with conda using the following command:\n\n"
                "\t[green]conda install -c conda-forge google-cloud-sdk\n"
            )

        print("For more information, see [link]https://docs.coiled.io/user_guide/setup/gcp/cli.html[/link]")

        setup_failure("Gcloud cli missing", backend="gcp")
        return False

    project = get_gcloud_config("project")

    if not project:
        print("No project was set, so you'll need to select or create one...")
        gcloud_wrapper(["init"], interactive=True, action_name=ACTION_INIT)

    project = get_gcloud_config("project")
    if not project:
        print("[red]There's still no project set so aborting Coiled setup.")
        setup_failure("No project was set", backend="gcp")
        return False

    region = region or get_gcloud_config("compute/region")

    if not region:
        print(
            "No region is set, you'll need to specify region like so:\n"
            "[green]coiled setup gcp --region us-central1[/green]"
        )
        setup_failure("Region was not set", backend="gcp")
        return False

    if quotas or quota_link:
        show_quotas(project, region, help=not quota_link)
        return False

    base_account_name = iam_user
    base_name_for_role = iam_user.replace("-", "_")  # role can't have `-`

    main_sa = base_account_name
    data_sa = f"{base_account_name}-data"
    main_role = base_name_for_role
    data_role = f"{base_name_for_role}_data"
    gar_name = "coiled"  # this is what control-plane expects

    main_email = f"{main_sa}@{project}.iam.gserviceaccount.com"
    data_email = f"{data_sa}@{project}.iam.gserviceaccount.com"

    resource_description = (
        f"Proposed region for Coiled:\t[green]{region}[/green]\t"
        f"(use `coiled setup gcp --region` to change)\n"
        f"Proposed project for Coiled:\t[green]{project}[/green]\t"
        f"(use `gcloud config set project <project_id>` to set)\n"
        "\n"
        "[bold]The following IAM resources will be created:[/bold]\n"
        "\n"
        f"Service account for creating clusters:\t[green]{main_sa}[/green]\n"
        f"Service account for data access:\t[green]{data_sa}[/green]\n"
        f"IAM Role:\t\t[green]{main_role}[/green] "
        f"(for [green]{main_sa}[/green] service account)\n"
        f"IAM Role:\t\t[green]{data_role}[/green] "
        f"(for [green]{data_sa}[/green] service account)"
    )

    if enable_gar:
        resource_description += f"\nArtifact Registry:\t[green]{gar_name}[/green] in region {region}\n"

    print(Panel(resource_description))

    if not yes and not Confirm.ask("Proceed with Google Cloud IAM setup for Coiled?", default=True):
        return False

    with get_temp_dir() as dir:
        main_file = os.path.join(dir, f"{main_role}.yaml")
        with open(main_file, "w") as f:
            f.write(CONTROL_PLANE_ROLE)

        data_file = os.path.join(dir, f"{data_role}.yaml")
        with open(data_file, "w") as f:
            f.write(DATA_ROLE)

        gcloud_wrapper(
            ["iam", "roles", "create", main_role, f"--project={project}", "--file", main_file, "--quiet"],
            action_name=ACTION_CREATE_ROLE,
        )

        gcloud_wrapper(
            ["iam", "roles", "create", data_role, f"--project={project}", "--file", data_file, "--quiet"],
            action_name=ACTION_CREATE_ROLE,
        )

    gcloud_wrapper(["iam", "service-accounts", "create", main_sa], action_name=ACTION_CREATE_SA)
    gcloud_wrapper(["iam", "service-accounts", "create", data_sa], action_name=ACTION_CREATE_SA)

    gcloud_wrapper(
        [
            "projects",
            "add-iam-policy-binding",
            project,
            f"--member=serviceAccount:{main_email}",
            f"--role=projects/{project}/roles/{main_role}",
            "--condition=None",
        ],
        action_name=ACTION_BIND_POLICY,
    )
    gcloud_wrapper(
        [
            "projects",
            "add-iam-policy-binding",
            project,
            f"--member=serviceAccount:{data_email}",
            f"--role=projects/{project}/roles/{data_role}",
            "--condition=None",
        ],
        action_name=ACTION_BIND_POLICY,
    )

    print("Service accounts and roles created.")
    print("Enabling services (this may take a while)...")

    services = [
        "compute",
        "bigquery.googleapis.com",
        "logging",
        "monitoring",
    ]

    if enable_gar:
        services.append("artifactregistry.googleapis.com")

    for service in services:
        print(f"  {service}")
        if not gcloud_enable_service(service, project):
            setup_failure(f"Enabling service {service} failed", backend="gcp")
            return False
    if enable_log_sink_permissions:
        print("  orgpolicy.googleapis.com")
        gcloud_enable_service("orgpolicy.googleapis.com", project)
    print("Services enabled.")

    if enable_gar:
        print("Setting up Google Artifact Registry (this may take a few minutes)...")
        if not gcloud_check_gar(gar_name, region):
            gcloud_wrapper(
                ["artifacts", "repositories", "create", gar_name, "--repository-format=docker", f"--location={region}"],
                action_name=ACTION_CREATE_GAR,
            )
        gcloud_wrapper(
            [
                "artifacts",
                "repositories",
                "add-iam-policy-binding",
                gar_name,
                "--role=roles/artifactregistry.repoAdmin",
                f"--location={region}",
                f"--member=serviceAccount:{main_email}",
                "--condition=None",
            ],
            action_name=ACTION_BIND_GAR,
        )

    show_quotas(project, region)

    if not manual_final_setup:
        print()
        print("[bold]You can setup Coiled to use the Google Cloud credentials you just created.")
        print(
            "The service account key will go to Coiled, where it will be stored "
            "securely and used to create clusters in your Google Cloud account "
            "on your behalf."
        )
        print(
            "This will also create infrastructure in your account like a VPC "
            "and subnets, none of which has a standing cost."
        )
        print()

    if not manual_final_setup and (
        yes
        or Confirm.ask(
            "Setup your Coiled account to use the Google Cloud credentials you just created?",
            default=True,
        )
    ):
        coiled.add_interaction(action="prompt:CoiledSetup", success=True)

        with get_temp_dir() as dir:
            key_path = os.path.join(dir, "coiled-key.json")
            if not gcloud_make_key(main_email, key_path):
                return False

            if enable_gar:
                print("Waiting for Google Artifact Registry to be ready...")
                if not gcloud_wait_for_repo(region=region, key_path=key_path):
                    # FIXME better instructions about what to do in this case
                    print(
                        "[red]Google Artifact Registry is still not ready. "
                        "You may need to complete account setup manually; "
                        "please contact us if you need help."
                    )
                    setup_failure("Timeout waiting for GAR to be ready", backend="gcp")
                    return False
                print("Google Artifact Registry is ready.")

            got_existing_constraint = False
            reset_to_constraint = None
            try:
                if enable_log_sink_permissions:
                    got_existing_constraint, existing_constraint_policy = get_existing_org_policy(
                        constraint=f"constraints/{IAM_LOG_SINK_CONSTRAINT}", project=project
                    )
                    if got_existing_constraint:
                        reset_to_constraint = remove_policy_etags(existing_constraint_policy)
                        set_allow_all_log_sink_constraint(project)
            except Exception:
                print(
                    f"[red]Warning:[/red] "
                    f"There was a problem attempting to adjust constraints/{IAM_LOG_SINK_CONSTRAINT} for your project."
                    "\n"
                    "This may prevent you from accessing your cluster logs via Coiled.\n"
                    "Please contact support@coiled.io if you have any questions or would like help accessing your logs."
                    "\n"
                )

            print("Setting up Coiled to use your Google Cloud account...")
            with coiled.Cloud(workspace=coiled_account) as cloud:
                parsed_gcp_credentials = _parse_gcp_creds(
                    gcp_service_creds_dict=None,
                    gcp_service_creds_file=key_path,
                )
                gcp_region, gcp_zone = parse_gcp_region_zone(region=region)
                # Set GCP credentials for the Coiled account
                print("Sending GCP credentials to Coiled...")
                cloud._sync_request(
                    f"/api/v2/cloud-credentials/{coiled_account}/gcp",
                    method="POST",
                    json_result=True,
                    handle_confirm=True,
                    json={
                        "credentials": parsed_gcp_credentials,
                        "instance_service_account": data_email,
                    },
                )

                # Update GCP account settings
                print("Updating Coiled GCP account settings...")
                cloud._sync_request(
                    f"/api/v2/setup/account/{coiled_account}/gcp/settings",
                    method="PATCH",
                    json={
                        "auto_setup": True,
                        "give_workers_public_ip": True,
                        "give_scheduler_public_ip": True,
                        "scheduler_firewall": None,
                        "custom_software_bucket_prefix": None,
                        "use_self_hosted_bucket": None,
                    },
                    json_result=True,
                )

                # Abandon existing GCP infra if it exists
                print("Cleaning up existing Coiled GCP infra (if any)...")
                cloud._sync_request(
                    f"/api/v2/setup/account/{coiled_account}/gcp",
                    method="DELETE",
                )
                time.sleep(5)  # give it a moment to clean up

                # Create global infrastructure
                if not wait_on_component_ready(
                    route=f"/api/v2/setup/account/{coiled_account}/gcp/global",
                    component_name="Global Infrastructure",
                    create_json={
                        "managed": True,
                        "network": None,
                        "scheduler_network_tags": None,
                        "cluster_network_tags": None,
                    },
                    cloud=cloud,
                ):
                    return False

                # Create regional infrastructure
                if not wait_on_component_ready(
                    route=f"/api/v2/setup/account/{coiled_account}/gcp/regions",
                    component_name="Regional Infrastructure",
                    create_json={
                        "default": True,
                        "region": gcp_region,
                        "managed": True,
                        "subnets": [{"link": None, "name": None, "for_workers": True, "for_schedulers": True}],
                    },
                    cloud=cloud,
                ):
                    return False
                print("Coiled account setup complete.")

                # Set registry to GAR if enabled, otherwise ECR
                cloud._sync_request(
                    f"/api/v2/user/account/{coiled_account}/registry",
                    method="POST",
                    json_result=True,
                    json={
                        "type": "gar" if enable_gar else "ecr",
                    },
                )

            coiled.add_interaction(action="CoiledSetup", success=True)

            if got_existing_constraint and reset_to_constraint is not None:
                set_project_org_policy(
                    constraint=f"constraints/{IAM_LOG_SINK_CONSTRAINT}", project=project, policy=reset_to_constraint
                )

    else:
        coiled.add_interaction(action="prompt:CoiledSetup", success=False)

        setup_url = (
            f"{dask.config.get('coiled.server', coiled.utils.COILED_SERVER)}/"
            f"{coiled_account}/settings/setup/credentials"
        )

        data_role_console_link = (
            "https://console.cloud.google.com/iam-admin/roles/details/"
            f"projects%3C{project}%3Croles%3C{data_role}?project={project}"
        )

        key_path = os.path.abspath("coiled-key.json")
        if not gcloud_make_key(main_email, key_path):
            return False

        print(
            Panel(
                "You've successfully created service accounts for Coiled "
                "in your Google Cloud project. "
                "You can now complete your Coiled account setup by telling "
                "us how to use these service accounts:\n"
                "\n"
                f"1. Go to [link]{setup_url}[/link] and select GCP.\n"
                "\n"
                f"2. The credential file for [green]{main_sa}[/green] has been saved "
                f"on your local computer at \n"
                f"     {key_path}\n"
                f"   Choose this file for the "
                f"[bold]cluster-creation service account[/bold].\n"
                "\n"
                f"3. Enter [green]{data_email}[/green] as the [bold]data access "
                f"service account[/bold].\n"
                "\n"
                "You'll then have the ability to chose non-default network setup "
                "or container registry settings if desired.\n"
                "\n"
                "[bold]Optional steps[/bold]\n"
                "\n"
                "After you've successfully setup your Coiled account, you'll no "
                "longer need the credential file on your local computer and can "
                "delete this if you wish.\n"
                "\n"
                "We've configured the data access service account with scope for "
                "submitting logs and for accessing Google Storage. If you wish to "
                "add or remove permissions attached to your Coiled clusters for "
                "accessing data, you can do that at \n"
                "\n"
                f"[link]{data_role_console_link}[/link]."
            )
        )

    return True


def show_quotas(project: str, region: str, help: bool = True):
    existing_quotas = get_quotas(project, region)

    quota_types = [
        {
            "name": "CPUs",
            "explanation": "vCPUs per VM * number of VMs",
            "value": existing_quotas.get("CPUS"),
            "unit": "vCPU",
        },
        {
            "name": "Persistent Disk SSD",
            "explanation": "at least 40GB required per VM",
            "value": existing_quotas.get("SSD_TOTAL_GB"),
            "unit": "GB",
        },
        {
            "name": "In-use IP addresses",
            "explanation": "one per VM",
            "value": existing_quotas.get("IN_USE_ADDRESSES"),
            "unit": "addresses",
        },
    ]

    url = get_gcp_console_quota_url(project=project, region=region)
    if help:
        table = Table(title=f"Existing quotas for [bold]{project}[/bold] in [bold]{region}[/bold]")
        table.add_column("Quota type", justify="left")
        table.add_column("Existing value", justify="right")
        table.add_column("Cluster will use...", justify="left", overflow="fold")

        for quota_type in quota_types:
            if quota_type["value"]:
                quota_value = f"[bold]{int(quota_type['value'])}[/bold] {quota_type['unit']}"
            else:
                quota_value = "(could not retrieve)"

            table.add_row(quota_type["name"], quota_value, quota_type["explanation"])

        print(
            "Coiled runs in your own Google Cloud account, so your cluster sizes will be "
            "constrained by your GCP quotas.\n"
        )

        print(table)

        print(
            Panel(
                "These quotas are set per-region, so you'll need a high enough quota in the region where you'll "
                "be running your Coiled clusters.\n"
                "\n"
                "The default Coiled instance type ([bold]e2-standard-4[/bold]) has [bold]4 vCPUs[/bold], "
                "so a 10 worker cluster (plus scheduler) would require [bold]44 vCPUs[/bold], "
                "[bold]440 GB[/bold] Persistent Disk SSD, and [bold]11 IP addresses[/bold].\n"
                "\n"
                f"For [bold]{project}[/bold] (project) in [bold]{region}[/bold] "
                f"you can view the current quotas and request increases in the [link={url}]Google Cloud Console[/link]."
            )
        )
    else:
        print(url)


def get_gcp_console_quota_url(project, region):
    disk_quota = quote(quote("Persistent Disk SSD (GB)"))
    ip_quota = quote(quote("In-use regional external IPv4 addresses"))

    # use %29 for final ')' because iTerm doesn't include final ')' when you click URL
    # and then link doesn't work right and just shows all quotas for the project
    return (
        "https://console.cloud.google.com/iam-admin/quotas"
        f"?project={project}"
        "&pageState=(%22allQuotasTable%22:"
        "(%22f%22:%22%255B%257B_22k_22_3A_22Quota_22_2C_22t_22_3A10_2C_22v_22_3A_22_5C_22_5C_5C_5C_22"
        "CPUs_5C_5C_5C_22_5C_22_22_2C_22i_22_3A_22displayName_22%257D_2C%257B_22k_22_3A_22_22_2C_22t_"
        f"22_3A10_2C_22v_22_3A_22_5C_22region_3A{region}_5C_22_22_2C_22s_22_3Atrue%257D_2C%257B_22k"
        "_22_3A_22_22_2C_22t_22_3A10_2C_22v_22_3A_22_5C_22OR_5C_22_22_2C_22o_22_3Atrue%257D_2C%257B_"
        "22k_22_3A_22Quota_22_2C_22t_22_3A10_2C_22v_22_3A_22_5C_22"
        f"{disk_quota}_5C_22_22_2C_22s_22_3Atrue_2C_22i_22_3A_22"
        "displayName_22%257D_2C%257B_22k_22_3A_22_22_2C_22t_22_3A10_2C_22v_22_3A_22_5C_22"
        f"region_3A{region}_5C_22_22_2C_22s_22_3Atrue%257D_2C%257B_22k_22_3A_22_22_2C_22t_22_"
        "3A10_2C_22v_22_3A_22_5C_22OR_5C_22_22_2C_22o_22_3Atrue%257D_2C%257B_22k_22_3A_22"
        f"Quota_22_2C_22t_22_3A10_2C_22v_22_3A_22_5C_22{ip_quota}_5C_22_22_2C_"
        "22s_22_3Atrue_2C_22i_22_3A_22displayName_22%257D_2C%257B_22k_22_3A_22_22_2C_22t_22_3A10_"
        f"2C_22v_22_3A_22_5C_22region_3A{region}_5C_22_22_2C_22s_22_3Atrue%257D%255D%22,%22s%22:%5B"
        "(%22i%22:%22displayName%22,%22s%22:%220%22),"
        "(%22i%22:%22effectiveLimit%22,%22s%22:%221%22),"
        "(%22i%22:%22currentPercent%22,%22s%22:%221%22),"
        "(%22i%22:%22currentUsage%22,%22s%22:%221%22),"
        "(%22i%22:%22serviceTitle%22,%22s%22:%220%22),"
        "(%22i%22:%22displayDimensions%22,%22s%22:%220%22)%5D)%29"
    )


def get_quotas(project: str, region: str) -> dict:
    quota_by_metric = {}
    gcloud_path = get_gcloud_path()
    if gcloud_path:
        quotas = get_gcloud_json([
            gcloud_path,
            "compute",
            "regions",
            "describe",
            region,
            "--project",
            project,
            "--format",
            "json",
        ])
        if quotas:
            quota_by_metric = {quota["metric"]: quota["limit"] for quota in quotas["quotas"]}
    return quota_by_metric
