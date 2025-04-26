import os
import sys
import time
import copy
from typing import List, Optional, TextIO, Tuple

import yaml

from openapi_client import ModelServiceLinkSecretAPIInput
from openapi_client.models import (
    ModelServiceCreateAPIInput,
    ModelserviceModelServiceListResponse,
    ModelserviceModelServiceReadResponse,
    ResponseModelServiceInfo,
    ResponseModelServiceRevision,
    ResponseSecret,
    V1HubModelTaskSpec,
)
from openapi_client.models.v1_autoscaling import V1Autoscaling
from openapi_client.models.v1_auxiliary_form import V1AuxiliaryForm
from openapi_client.models.v1_command import V1Command
from openapi_client.models.v1_env_form import V1EnvForm
from openapi_client.models.v1_run_argument import V1RunArgument
from openapi_client.models.v1_import_form import V1ImportForm
from openapi_client.models.v1_model_ref_form import V1ModelRefForm
from openapi_client.models.v1_port_path import V1PortPath
from openapi_client.models.v1_resources_form import V1ResourcesForm
from openapi_client.models.v1_serve_revision_service_form import (
    V1ServeRevisionServiceForm,
)
from vessl import vessl_api
from vessl.cli._util import (
    print_table_tabulate,
)
from vessl.util.prompt import prompt_confirm, prompt_text, prompt_choices
from vessl.util.echo import print_debug, print_info, print_success, print_error, print_error_result
from vessl.util.endpoint import Endpoint
from vessl.cli.serve.util import (
    print_gateway,
    print_services,
    print_revision,
    create_secret,
    fetch_variable_from_injects,
    get_runner_type,
    sanitize,
    sanitize_model_form,
    generate_image_name
)
from vessl.enums import ModelServiceType, ClusterCustomEndpointType
from vessl.models.vessl_model import VesslModel
from vessl.kernel_cluster import list_cluster_presets, list_clusters
from vessl.organization import _get_organization_name
from vessl.secret import list_generic_secrets
from vessl.serving import (
    _wait_for_gateway_enabled,
    _wait_for_revision_to_launch,
    abort_in_progress_rollout,
    abort_in_progress_rollout_by_name,
    create_active_revision_replacement_rollout,
    create_revision_from_yaml_v2,
    get_recent_rollout,
    launch_revision,
    list_services,
    _read_service,
    update_model_service,
    update_revision_autoscaler_config,
)

from vessl.util.exception import VesslApiException

from .command_options import build_autoscaling_configs


def list():
    services: List[ResponseModelServiceInfo] = list_services(
        organization=vessl_api.organization.name
    ).results
    print_services(services=services)

def abort_update(service: ResponseModelServiceInfo):
    try:
        abort_in_progress_rollout(service=service)
    except VesslApiException as e:
        print(f"Failed to abort the service update: {e.message}")
        sys.exit(1)

def create(
    file: TextIO,
    no_prompt: bool,
    launch: bool,
    set_current_active: bool,
    force: bool,
    service_name: str,
    serverless: bool,
    from_hub: str,
    node_port: int,
    subdomain: str,
):
    organization_name = vessl_api.set_organization()
    vessl_api.configure_default_organization(organization_name)

    if from_hub:
        hub: V1HubModelTaskSpec = vessl_api.hub_model_task_read_by_key_api(key=from_hub)
        yaml_body = hub.yaml
    elif file:
        yaml_body = file.read()
    else:
        print_error("Error: Either --from-hub or --file must be specified.")
        sys.exit(1)

    try:
        yaml_loaded = yaml.safe_load(yaml_body)
    except yaml.YAMLError as e:
        print_error(f"Error: invalid YAML\n{e}")
        sys.exit(1)

    if not isinstance(yaml_loaded, dict):
        print_error(f"Error: invalid YAML: expected mapping (dict), got {type(yaml_loaded)}")
        sys.exit(1)

    try:
        cluster_name = yaml_loaded["resources"]["cluster"]
    except (KeyError, TypeError):
        print_error("Error: invalid YAML: no cluster name")
        sys.exit(1)
    
    arguments = {}
    if from_hub:
        injects = vessl_api.hub_model_injects_read_by_key_api(key=from_hub)

        if not no_prompt and injects.injected_envs:
            for key in injects.injected_envs:
                arguments[key] = fetch_variable_from_injects(key)

    service_name_from_legacy_yaml = yaml_loaded.get("name", None)

    service_name = service_name or service_name_from_legacy_yaml or None
    service_name, service_type = _check_service_name_or_prompt(
        service_name=service_name,
        cluster_name=cluster_name,
        serverless=serverless,
        no_prompt=no_prompt,
        node_port=node_port,
        subdomain=subdomain,
    )

    ## Check if the service is already rolling out
    ongoing_rollout_exists = False
    try:
        recent_rollout = get_recent_rollout(service_name)
        if recent_rollout and recent_rollout.status == "rolling_out":
            ongoing_rollout_exists = True
            print_error(f"Error: the service {service_name} is currently rolling out.")
            if not force:
                print_error("Use --force option to abort the existing rollout.")
                sys.exit(1)
    except VesslApiException as e:
        print_debug("No existing rollout found.")
        pass

    ## Abort the existing rollout if --force
    if ongoing_rollout_exists and force:
        if abort_in_progress_rollout_by_name(service_name):
            print_info("Waiting for the existing rollout to be aborted...")
            time.sleep(30)

    ## create revision
    try:
        revision = create_revision_from_yaml_v2(
            organization=vessl_api.organization.name,
            service_name=service_name,
            yaml_body=yaml_body,
            serverless=(service_type == ModelServiceType.SERVERLESS),
            arguments=V1RunArgument(env_vars=arguments)
        )
    except VesslApiException as e:
        if e.status == 400:
            print_error("Error: failed to create revision (invalid parameters).")
            print_error_result(e.message)
        else:
            print_error("Error: failed to create revision. (internal error).")
        sys.exit(1)

    service_url = Endpoint.service.format(vessl_api.organization.name, service_name)
    if service_type == ModelServiceType.SERVERLESS:
        print_success(f"Successfully created revision #{revision.number}!")
        print()
        print_success(f"Check out the service at: {service_url}")
        print()
        return

    ## launch or set-active
    if set_current_active:
        launch = True
    if not launch and not no_prompt:
        launch = prompt_confirm("Do you want to launch this revision immediately?")
    if launch:
        if not set_current_active and not no_prompt:
            set_current_active = prompt_confirm("Do you want this revision to receive full traffic immediately?")

    try:
        if set_current_active:
            create_active_revision_replacement_rollout(
                organization=vessl_api.organization.name,
                model_service_name=revision.model_service_name,
                desired_active_revisions_to_weight_map={revision.number: 100},
            )
            print_info("Successfully triggered revision activation.")
        elif launch:
            launch_revision(
                organization=vessl_api.organization.name,
                service_name=revision.model_service_name,
                revision_number=revision.number,
            )
            print_info("Successfully triggered revision launch.")
        if not no_prompt and (launch or set_current_active):
            _wait_for_revision_to_launch(service_name=service_name, revision_number=revision.number, print_output=True)
        revision = vessl_api.model_service_revision_read_api(
        organization_name=vessl_api.organization.name,
        model_service_name=service_name,
        revision_number=revision.number,
        )
        print_success(f"Successfully created revision for service: {service_name}!")
        print_revision(revision, verbose=False)
        print()
        print(f"Check out the service at: {service_url}")

        
    except VesslApiException as e:
        print_error("Error: failed to launch revision.")
        print_error_result(e.message)
        sys.exit(1)

    ## Wait for the gateway to be enabled
    if set_current_active:
        gateway = _read_service(service_name=service_name).gateway_config
        if not no_prompt:
            _wait_for_gateway_enabled(gateway=gateway, service_name=revision.model_service_name, print_output=True)

        print_info("Endpoint is enabled.")
        gateway = _read_service(service_name=service_name).gateway_config
        print_gateway(gateway)
        print_info(f"You can test your service via {gateway.endpoint}")

def scale(
    service: ResponseModelServiceInfo,
    number: ResponseModelServiceRevision,
    min: Optional[int],
    max: Optional[int],
    target: Optional[int],
    metric: Optional[str],
):
    if service.type == ModelServiceType.SERVERLESS.value:
        print("User cannot update autoscaling for serverless service.")
        print("Autoscaling will be automatically set based on number of requests.")
        sys.exit(1)

    revision = number
    conf: V1Autoscaling = revision.revision_spec.autoscaling
    original_conf: V1Autoscaling = copy.copy(conf)
    updated_conf: V1Autoscaling = build_autoscaling_configs(conf=conf, min=min, max=max, target=target, metric=metric)
    
    try:
        update_revision_autoscaler_config(
            organization=vessl_api.organization.name,
            service_name=service.name,
            revision_number=revision.number,
            autoscaling=updated_conf,
        )
    except VesslApiException as e:
        print(f"Failed to update autoscaler config of revision #{revision.number} of service {service.name}: {e.message}")
        sys.exit(1)

    print("Successfully updated autoscaler config")
    print_table_tabulate([
        {
            "Original Autoscaling Configurations": original_conf,
            "Updated Autoscaling Configurations": updated_conf
        }
    ])

def split(service: ResponseModelServiceInfo, number: List[int], weight: List[int], interactive: bool):
    if not interactive:
        update_model_service(service, number, weight)
        return
    
    gateway_current = _read_service(service_name=service.name).gateway_config
    endpoint = gateway_current.endpoint
    print_info(f"Current Endpoint Host: {'(not set)' if endpoint=='' else endpoint}")
    print_info("Traffic Rules")
    if gateway_current.rules:
        current_rules = [
            {
                "Revision Number": i.revision_number,
                "Traffic Weight": f'{i.traffic_weight}%',
            }
            for i in gateway_current.rules
        ]
        print_table_tabulate(current_rules)

    print_table_tabulate(
        [
            {
                "Revision Number": n,
                "Traffic Weight": f'{w}%',
            } for n, w in zip(number, weight)
        ],
    )
    update_model_service(service, number, weight)

def set_access_token(
    service: ResponseModelServiceInfo,
    secret: ResponseSecret,
):
    vessl_api.model_service_link_secret_api(
        organization_name=vessl_api.organization.name,
        model_service_name=service.name,
        model_service_link_secret_api_input=ModelServiceLinkSecretAPIInput(
            secret_id=secret.credentials_id,
        )
    )

def create_yaml(
    service_name: str,
    message: str,
    use_api_key: bool = False,
):
    organization_name = _get_organization_name()

    lockfile_path = ".vessl.model.lock"
    lockfile = VesslModel.from_lockfile(lockfile_path)
    if lockfile is None:
        print_error("The lockfile is not found.")
        return

    try:
        msr = vessl_api.model_service_read_api(
            organization_name=organization_name,
            model_service_name=service_name,
        )
    except Exception as e:
        if e.status == 404:
            print_error(f"Model service {service_name} not found. You should first create a service.")
            return
        print_error(f"Failed to read model service: {e}")
        return

    print_info(f"Service name of {service_name} found.")

    # clusters = list_clusters()
    # cluster_name = prompt_choices("Cluster", [x.name for x in clusters])
    # cluster = list(filter(lambda x: x.name == cluster_name, clusters))[0]
    cluster = msr.kernel_cluster
    print_info(f"Using {cluster.name} cluster configured by the service.")

    presets = list_cluster_presets(cluster.id)
    preset_name = prompt_choices("Preset", [x.name for x in presets])
    preset = list(filter(lambda x: x.name == preset_name, presets))[0]

    secret_name = None
    if use_api_key:
        print_info("Select API key for authentication.")
        secrets = list_generic_secrets()
        if len(secrets) == 0:
            print_info("No secrets registered.")
            if prompt_confirm("Do you want to create a new secret?", default=True):
                secret_name = create_secret()
            else:
                print_error("No secret selected.")
                return
        else:
            secret_names = [x.credentials_name for x in secrets]
            secret_names.append("Create a new secret")
            secret_name = prompt_choices("Secret", secret_names)
            if secret_name == "Create a new secret":
                secret_name = create_secret()

    service = V1ServeRevisionServiceForm(
        expose=3000,
        healthcheck=V1PortPath(path="/",port=3000),
        monitoring=[V1PortPath(path="/metrics",port=3000)],
        autoscaling=V1Autoscaling(min=1, max=2, metric="cpu", target=50),
        auxiliary=V1AuxiliaryForm(
            runner_type=get_runner_type(lockfile.type),
        )
    ).to_dict()

    form = {
        "name":service_name,
        "message":message,
        "env":(
            None
            if use_api_key is None or secret_name is None
            else {
                "SERVICE_AUTH_KEY": V1EnvForm(
                    secret=secret_name,
                    source="secret",
                ).to_dict()
            }
        ),
        "image": generate_image_name(lockfile),
        "resources": V1ResourcesForm(
            cluster=cluster.name,
            preset=preset.name,
        ).to_dict(),
        "import": {
            "/model": sanitize_model_form(V1ImportForm(
                model=V1ModelRefForm(
                    organization_name=organization_name,
                    model_repository_name=lockfile.repository_name,
                    model_number=lockfile.model_number,
                )
            ))
        },
        "run": [
            V1Command(
                command=lockfile.entrypoint,
                workdir="/model/"+os.getcwd().split("/")[-1],
            ).to_dict()
        ],
        "ports": [V1PortPath(port=3000).to_dict()],
        "service":service,
    }

    with open("service.yaml", "w") as f:
        cleaned = sanitize(form)
        b = yaml.dump(cleaned, default_flow_style=False, sort_keys=False)
        b = b.replace("_import", "import")
        f.write(b)
    
    print_success("service.yaml created.")


def _check_service_name_or_prompt(
    service_name: Optional[str],
    cluster_name: str,
    serverless: bool,
    no_prompt: bool,
    node_port: int,
    subdomain: str,
) -> Tuple[str, ModelServiceType]:
    """
    Verifies (or prompts the user to choose) a service name.

    Arguments:
        service_name (str | None):
            Name of service, provided either in CLI argument or embedded in YAML.

        cluster_name (str):
            Name of the cluster, hinted in YAML. This is used as when we have to
            create a service.

        serverless (bool):
            Whether user has explicitly requested the service to be in serverless mode.

        no_prmopt (bool):
            True if the user has explicitly denied prompts or interactions.

        node_port (int):
            Cluster NodePort number to expose the service.

        subdomain (str):
            Subdomain to expose the service.

    Returns:
        str: Name of the selected Service.
        ModelServiceType: Type of the selected Service.
    """

    if service_name:
        try:
            model_service_resp: ModelserviceModelServiceReadResponse = (
                vessl_api.model_service_read_api(
                    model_service_name=service_name,
                    organization_name=vessl_api.organization.name,
                )
            )
        except VesslApiException as e:
            if e.status == 404:
                print_info(f"Service '{service_name}' not found.")
                print_info("Automatically creating one...")
                print()
                return _create_service(
                    service_name=service_name, cluster_name=cluster_name, serverless=serverless, node_port=node_port, subdomain=subdomain
                )
            else:  # unexpected error
                raise e

        service_type = ModelServiceType(model_service_resp.type)
        if serverless and service_type != ModelServiceType.SERVERLESS:
            print_error(
                f"Error: service '{service_name}' has type {str(service_type.value).capitalize()}, "
                "but --serverless flag was given in the command line.\n"
                "\n"
                "Please check your parameters and try again."
            )
            sys.exit(1)

        return model_service_resp.name, service_type

    else:
        service_list_resp: ModelserviceModelServiceListResponse = vessl_api.model_service_list_api(
            organization_name=vessl_api.organization.name,
        )
        service_list: List[ResponseModelServiceInfo] = service_list_resp.results
        service_display_texts = [
            f"{s.name} (status: {str(s.status).capitalize()}; type: {str(s.type).capitalize()})"
            for s in service_list
        ]

        if no_prompt:
            print_error("Error: service name is required.")
            print()
            print_info("NOTE: Available services are:")
            example_count = 5
            for txt in service_display_texts[:example_count]:
                print_info(f"    - {txt}")
            if example_count < len(service_list):
                print_info(f"    - ({len(service_list)-example_count} more...)")
            sys.exit(1)

        chosen_service: Optional[ResponseModelServiceInfo] = prompt_choices(
            "Select service, or create a new one.",
            [("(Create a new service...)", None)]
            + [(txt, s) for txt, s in zip(service_display_texts, service_list)],
        )
        if chosen_service is None:
            return _create_service(
                service_name=None,
                cluster_name=cluster_name,
                serverless=serverless,
                node_port=node_port,
            )
        else:
            return chosen_service.name, ModelServiceType(chosen_service.type)


def _create_service(
    service_name: Optional[str], cluster_name: str, serverless: bool, node_port: int = 0, subdomain: str = ""
) -> Tuple[str, ModelServiceType]:
    """
    Prompts the user to help create a Service.

    Arguments:
        service_name (str | None):
            Name of the service, if known.

        cluster_name (str):
            Name of the cluster, hinted in YAML. This is used to create the service.

        serverless (bool):
            Whether to create the new service as serverless mode.
            Only present if the user explicitly provided an option for it.

        node_port (int):
            NodePort number to expose the service.
            Only present if the cluster is configured with a NodePort.

        subdomain (str):
            Subdomain to expose the service.
            Only present if the user explicitly provided an option for it.

    Returns:
        str: Name of the new Service.
        ModelServiceType: Type of the new Service.
    """

    if service_name is None:
        service_name = prompt_text("Name for new service")

    service_type: ModelServiceType
    service_type = ModelServiceType.SERVERLESS if serverless else ModelServiceType.PROVISIONED
    print_info(f"Creating service {service_name} in {service_type.value.capitalize()} mode.")

    # We only have the cluster's name; we need to resolve its ID.
    all_clusters = list_clusters()
    matching_cluster_list = [c for c in all_clusters if c.name == cluster_name]
    if len(matching_cluster_list) != 1:
        print_error(f"Error: cluster '{cluster_name}' not found!")
        print()
        print_error(
            "There might be a typo, or the cluster might not be connected to this organization."
        )
        print_error("Please check your cluster and try again.")
        print()
        print_info(
            f"NOTE: there are {len(all_clusters)} cluster(s) connected to this organization:"
        )
        for c in all_clusters:
            print_info(f"    - {c.name} (status: {str(c.status).capitalize()})")
        sys.exit(1)
    cluster = matching_cluster_list[0]

    if cluster.custom_endpoint_type == ClusterCustomEndpointType.NODE_PORT and node_port == 0:
        print_error(f"Error: cluster '{cluster_name}' is not configured with a NodePort.")
        print_error("Please configure the cluster with a NodePort and try again.")
        sys.exit(1)

    if cluster.custom_endpoint_type == ClusterCustomEndpointType.SUBDOMAIN and subdomain == "":
        print_error(f"Error: cluster '{cluster_name}' is not configured with a subdomain.")
        print_error("Please configure the cluster with a subdomain and try again.")
        sys.exit(1)

    try:
        vessl_api.model_service_create_api(
            organization_name=vessl_api.organization.name,
            model_service_create_api_input=ModelServiceCreateAPIInput(
                name=service_name, kernel_cluster_id=cluster.id, service_type=service_type.value, node_port=node_port, subdomain=subdomain
            ),
        )
    except VesslApiException as e:
        print_error("Failed to create service")
        print_error_result(e.message)
        sys.exit(1)

    print_info(f"Successfully created service: {service_name}")

    return service_name, service_type
