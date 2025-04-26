import sys
from typing import Dict, List

import click
import inquirer

from openapi_client import OrmModelServiceGatewayTrafficSplitEntry as TrafficSplitEntry
from openapi_client import (
    ResponseKernelCluster,
    ResponseKernelImage,
    ResponseModelServiceGatewayInfo,
    ResponseModelServiceInfo,
    ResponseModelServiceRevision,
    ResponsePathOperation,
    ResponseSecret,
    ResponseVolumeSourceEntity,
    V1Autoscaling,
    V1EnvVar,
    V1ImportForm,
    V1Port,
    V1VariableValue,
)
from openapi_client.models import secret_generic_secret_upsert_api_input
from vessl import vessl_api
from vessl.cli._util import print_data, print_table_tabulate
from vessl.models.vessl_model import VesslModel
from vessl.secret import list_generic_secrets
from vessl.util.common import parse_time_to_ago
from vessl.util.constant import (
    VESSL_SERVICE_TENSORFLOW_BASE_IMAGE_TEMPLATE,
    VESSL_SERVICE_TORCH_BASE_IMAGE_TEMPLATE,
)
from vessl.util.echo import print_error, print_info
from vessl.util.exception import InvalidYAMLError
from vessl.util.prompt import prompt_text


def print_services(services: List[ResponseModelServiceInfo]):
    print(f"{len(services)} service(s) found.\n")
    services_sorted = sorted(services, key=lambda service: service.created_dt, reverse=True)
    data = []
    for service in services_sorted:
        kernel_cluster: ResponseKernelCluster = service.kernel_cluster
        status: str = service.status
        data.append({
            "Name": service.name,
            "Cluster": kernel_cluster.name,
            "Status": status,
            "Created At": f"{service.created_dt} ({parse_time_to_ago(service.created_dt)})"
        })
    print_table_tabulate(data)

def print_service(service: ResponseModelServiceInfo):
    data = {
        "Name": service.name,
        "Description": "(none)" if service.description=="" else service.description,
        "Created By": service.created_by.email,
        "Created At": service.created_dt,
        "Cluster": service.kernel_cluster.name,
        "Status": service.status,
        "Type": service.type,
        "Endpoint": service.gateway_config.endpoint if service.gateway_config.enabled else "(not enabled)",
    }
    print_data(data=data)

def print_revisions(revisions: List[ResponseModelServiceRevision], verbose: bool = False):
    revisions_sorted = sorted(revisions, key=lambda revision: revision.created_dt, reverse=True)
    if not verbose:
        revs = [
                {
                    "Revision Number": r.number,
                    "Message":r.message,
                    "Status": r.status,
                    "Created At": f"{r.created_dt} ({parse_time_to_ago(r.created_dt)})",
                }
                for r in revisions_sorted
            ]
        print_table_tabulate(revs)
        print("To view more details on each revision, use the --detail(-d) flag option.")
        print()
    else:
        for r in revisions_sorted:
            kernel_image: ResponseKernelImage = r.kernel_image
            autoscaler_config: V1Autoscaling = r.revision_spec.autoscaling
            ports: List[V1Port] = r.revision_spec.ports
            data = {
                f"Revision #{r.number}": {
                    "Status": r.status,
                    "Message": r.message,
                    "Available Replicas": r.available_replicas,
                    "Deployment Spec": {
                        "Image URL": kernel_image.image_url,
                        "Ports": [
                            {"Name": port.name, "Port": port.source_port, "Type": port.protocol}
                            for port in ports
                        ],
                    },
                    "Autoscaler Config": {
                        "Min Replicas": autoscaler_config.min,
                        "Max Replicas": autoscaler_config.max,
                        "Resource": autoscaler_config.metric,
                        "Target": autoscaler_config.target,
                    },
                }
            }
            print_data(data)
            print()

def print_revision(revision: ResponseModelServiceRevision, verbose: bool = False):
    if not verbose:
        data = {
            "Number": revision.number,
            "Status": revision.status,
            "Message": revision.message,
        }
    else:
        kernel_image: ResponseKernelImage = revision.kernel_image
        autoscaler_config: V1Autoscaling = revision.revision_spec.autoscaling
        ports: List[V1Port] = revision.revision_spec.ports
        data = {
            "Number": revision.number,
            "Status": revision.status,
            "Message": revision.message,
            "Available Replicas": revision.available_replicas,
            "Deployment Spec": {
                "Image URL": kernel_image.image_url,
                "Ports": [
                    {"Name": port.name, "Port": port.source_port, "Type": port.protocol}
                    for port in ports
                ],
            },
            "Autoscaler Config": {
                "Min Replicas": autoscaler_config.min,
                "Max Replicas": autoscaler_config.max,
                "Resource": autoscaler_config.metric,
                "Target": autoscaler_config.target,
            },
        }
    print_data(data)

def print_gateway(gateway: ResponseModelServiceGatewayInfo):
    def _prettify_traffic_split_entry(entry: TrafficSplitEntry) -> str:
        """
        Returns a pretty representation of given traffic split entry.

        Examples:
        - "########   80%:   3 (port 8000)"
        - "##         20%:  12 (port 3333)"
        """
        gauge_char = "#"
        gauge_width = (entry.traffic_weight + 9) // 10  # round up (e.g. 31%-40% -> 4)
        gauge = gauge_char * gauge_width

        return (
            f"{gauge: <10} {entry.traffic_weight: <3}%: {entry.revision_number: >3} "
        )

    print_data(
        {
            "Enabled": gateway.enabled,
            "Status": gateway.status,
            "Endpoint": gateway.endpoint or "(not set)",
            "Ingress Class": gateway.ingress_class or "(empty)",
            "Annotations": gateway.annotations or "(empty)",
            "Traffic Targets": (
                list(map(_prettify_traffic_split_entry, gateway.rules))
                if gateway.rules
                else "(empty)"
            ),
        }
    )


def validate_revision_yaml_obj(yaml_obj):
    """
    Client-side validation. We do not need a full validation here, as it will
    be done on the server side anyway. Only perform necessary validations to
    ensure that other client-side logics run safely.

    Raises:
        InvalidYAMLError: this YAML object for revision is invalid.
    """

    def _check_type(obj, type_: type):
        assert isinstance(obj, type_)
        return obj

    try:
        if "ports" in yaml_obj:
            ports: list = _check_type(yaml_obj["ports"], list)

            for port in ports:
                expose_type = _check_type(port["type"], str)
                assert expose_type in ["http", "tcp"]

                port_number = _check_type(port["port"], int)
                assert 1 <= port_number <= 65535

    except (KeyError, AssertionError) as e:
        raise InvalidYAMLError(message=str(e))


def list_http_ports(yaml_obj) -> List[int]:
    """
    Lists all HTTP expose ports of the revision.

    This function assumes the YAML object is valid (i.e. has valid port definitions.)
    """

    if "ports" not in yaml_obj:
        return []

    http_ports: List[int] = []

    try:
        ports: list = yaml_obj["ports"]
        for port in ports:
            expose_type: str = port["type"]
            if expose_type == "http":
                port_number: int = port["port"]
                http_ports.append(port_number)

    except (KeyError, AssertionError) as e:
        raise InvalidYAMLError(message=str(e))

    return http_ports

def select_secret():
    print_info("Select secret for authentication.")
    secrets: List[ResponseSecret] = list_generic_secrets()
    if len(secrets) == 0:
        print_info("No secrets registered.")
        if click.confirm("Do you want to create a new secret?", default=True):
            return create_secret()
        else:
            print_error("No secret selected.")
            sys.exit(1)
    else:
        secret_names = [x.credentials_name for x in secrets]
        secret_names.append("Create a new secret")
        secret_name = inquirer.prompt(
            [
                inquirer.List(
                    "secret",
                    message="Select from secrets",
                    choices=secret_names,
                )
            ],
            raise_keyboard_interrupt=True,
        ).get("secret")
        if secret_name == "Create a new secret":
            return create_secret()
        return secret_name

def fetch_variable_from_injects(key):
        input_method = inquirer.prompt(
            [
                inquirer.List(
                    "input_method",
                    message=f"{key}?",
                    choices=["Input as text", "Choose from VESSL secrets"],
                )
            ],
            raise_keyboard_interrupt=True,
        ).get("input_method")

        if input_method == "Input as text":
            return V1VariableValue(source="text", text=click.prompt(f"Enter value for {key}"))
        elif input_method == "Choose from VESSL secrets":
            return V1VariableValue(source="secret", secret=select_secret())

def create_secret() -> str:
    secret_name = prompt_text("Secret name")
    secret_value = prompt_text("Secret value")
    resp = vessl_api.secret_generic_secret_upsert_api(
        organization_name=vessl_api.organization.name,
        secret_generic_secret_upsert_api_input=secret_generic_secret_upsert_api_input.SecretGenericSecretUpsertAPIInput(
            secret_name=secret_name,
            value=secret_value,
        )
    )
    print_info(f"Secret {resp.credentials_name} created.")
    return resp.credentials_name


def _translate_vops(vops: List[ResponsePathOperation]) -> dict:
    def _parse_source_entity(e: ResponseVolumeSourceEntity, t: str) -> str:
        if t == "model":
            org = e.model.model_repository.organization.name
            model_repo_name = e.model.model_repository.name
            model_num = e.model.model.number
            return f"vessl-model://{org}/{model_repo_name}/{model_num}"
        if t == "dataset":
            org = e.dataset.organization.name
            dataset_name = e.dataset.name
            return f"vessl-dataset://{org}/{dataset_name}"
        if t == "artifact":
            name = e.artifact.persistent.name
            return f"vessl-artifact://{name}"
        if t == "git":
            provider = e.git.repository.provider
            owner = e.git.repository.owner
            repo = e.git.repository.repo
            if provider == "bitbucket":
                return f"git://bitbucket.org/{owner}/{repo}"
            if provider == "huggingface":
                return f"hf://huggingface.co/{owner}/{repo}"
            else:
                return f"git://{provider}.com/{owner}/{repo}"
        if t == "s3":
            bucket = e.s3.bucket
            prefix = e.s3.prefix
            return f"s3://{bucket}/{prefix}"
        if t == "gs":
            bucket = e.gs.bucket
            prefix = e.gs.prefix
            return f"gs://{bucket}/{prefix}"
        if t == "hostpath":
            path = e.hostpath.path
            return f"hostpath://{path}"
        if t == "nfs":
            server = e.nfs.server
            path = e.nfs.path
            return f"nfs://{server}/{path}"
        if t == "cifs":
            return None
        if t == "googledisk":
            return None
        else:
            return None

    res = {
        "import": {},
        "mount": {},
    }
    for item in vops:
        if item._import:
            source_entity = item._import.source_entity
            t = source_entity.source_entity_type
            signature = _parse_source_entity(source_entity, t)
            res["import"][item.path] = signature
        if item.mount:
            source_entity = item.mount.source_entity
            t = source_entity.source_entity_type
            signature = _parse_source_entity(source_entity, t)
            res["mount"][item.path] = signature
    if not res["import"]:
        del res["import"]
    if not res["mount"]:
        del res["mount"]
    return res

def _translate_envvars(envvars: Dict[str,V1EnvVar]) -> dict:
    res = {}
    for k, v in envvars.items():
        if v.default_value.source == "secret":
            res[k] = {
                "secret": v.default_value.secret,
                "source": v.default_value.source,
            }
        if v.default_value.source == "text":
            res[k] = {
                "text": v.default_value.text,
                "source": v.default_value.source,
            }
    return res

def get_runner_type(model_runner_type: str) -> str:
    if model_runner_type == "vessl" or model_runner_type == "hf-transformers" or model_runner_type == "torch":
        return "vessl"
    elif model_runner_type == "bento":
        return "bento"
    else:
        raise ValueError(f"Unsupported model runner type: {model_runner_type}")
    
def sanitize(yaml_obj):
    if isinstance(yaml_obj, dict):
        cleaned = dict((k, sanitize(v)) for k, v in yaml_obj.items() if v is not None)
        return cleaned
    elif isinstance(yaml_obj, list):
        cleaned = [sanitize(v) for v in yaml_obj if v is not None]
        return cleaned
    else:
        return yaml_obj

def sanitize_model_form(form: V1ImportForm):
    return f"vessl-model://{form.model.organization_name}/{form.model.model_repository_name}/{form.model.model_number}"

def generate_image_name(
    vesslmodel: VesslModel,
):
    if vesslmodel.framework_type == "torch":
        return VESSL_SERVICE_TORCH_BASE_IMAGE_TEMPLATE.format(
            **{
                "pytorch_version": vesslmodel.pytorch_version,
                "cuda_version": vesslmodel.cuda_version,
            }
        )
    elif vesslmodel.framework_type == "tensorflow":
        return VESSL_SERVICE_TENSORFLOW_BASE_IMAGE_TEMPLATE.format(
            **{
                "tensorflow_version": vesslmodel.tensorflow_version,
                "cuda_version": vesslmodel.cuda_version,
            }
        )
    raise ValueError("Either pytorch_version or tensorflow_version must be provided")