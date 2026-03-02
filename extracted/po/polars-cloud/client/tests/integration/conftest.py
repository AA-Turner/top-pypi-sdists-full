# mypy: disable-error-code="return-value,no-untyped-def,no-any-return,no-untyped-call"

from __future__ import annotations

import base64
import contextlib
import dataclasses
import fcntl
import json
import logging
import os
import uuid
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING

import boto3
import polars_cloud as pc
import pytest
import requests
from polars_cloud import Workspace
from polars_cloud.constants import API_CLIENT, AUTH_DOMAIN

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s -  %(module)s - %(message)s",
)
logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    import pathlib
    from collections.abc import Generator

    from polars_cloud import ComputeContext
    from polars_cloud._typing import CPUArchitecture


class InactiveWorkspace(Exception):
    pass


@dataclass
class ComputeContextSpecsInput:
    cpus: int | None = None
    memory: int | None = None
    cpu_architectures: list[CPUArchitecture] | None = None
    instance_type: str | None = None
    storage: int | None = None
    cluster_size: int = 1


def pytest_addoption(parser):
    parser.addoption(
        "--noninteractive",
        action="store_true",
        default=False,
        help="Run the tests non interactively in CI.",
    )
    parser.addoption(
        "--reuse-worker-role",
        action="store_true",
        default=False,
        help="Reuse worker IAM roles (requires TestWorkerRole CloudFormation stack to be deployed)",
    )
    parser.addoption("--workspace", action="store", help="Use an existing workspace")


@dataclass
class WorkspaceConfig:
    # suffix: str = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    suffix: str = str(uuid.uuid4()).split("-")[0]

    organization_name: str = f"polars-ci-org-{suffix}"
    workspace_name: str = f"polars-ci-{suffix}"


def is_master(config) -> bool:
    return getattr(config, "workerinput", None) is None


@contextlib.contextmanager
def lock(path: pathlib.Path):
    with path.open("w") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        yield
        fcntl.flock(f, fcntl.LOCK_UN)


@pytest.fixture(scope="session")
def workspace(
    request: pytest.FixtureRequest, tmp_path_factory: pytest.TempPathFactory, worker_id
):
    if workspace_name := request.config.getoption("workspace"):
        yield Workspace(workspace_name)
        return
    if worker_id == "master":
        authenticate(request)
        cfg = WorkspaceConfig()
        yield create_workspace(request.session, cfg)
        remove_workspace(cfg)
        return

    root_tmp_dir = tmp_path_factory.getbasetemp().parent
    cfg_file = root_tmp_dir / "cfg.json"
    lock_file = cfg_file.with_suffix(".lock")
    try:
        with lock_file.open("w") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            authenticate(request)
            # Create the workspace if the file does not exist
            with contextlib.suppress(FileExistsError), cfg_file.open("x") as f:
                cfg = WorkspaceConfig()
                json.dump(dataclasses.asdict(cfg), f)
                create_workspace(request.session, cfg)

        # Load
        with cfg_file.open("r") as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            cfg = WorkspaceConfig(**json.load(f))
            lock.close()
            yield Workspace(cfg.workspace_name, organization=cfg.organization_name)
    finally:
        try:
            with cfg_file.open("r") as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                cfg = WorkspaceConfig(**json.load(f))
                remove_workspace(cfg)
                cfg_file.unlink()
        except FileNotFoundError:
            pass


def create_workspace(session: pytest.Session, cfg: WorkspaceConfig):
    logger.debug("Authenticating...")
    inner_authenticate(session.config.getoption("noninteractive"))
    logger.info("Successfully Authenticated")
    organization_schema = API_CLIENT.create_organization(cfg.organization_name)
    logger.info("Successfully created Organization")
    workspace_schema = API_CLIENT.create_workspace(
        cfg.workspace_name, organization_schema.id
    )
    logger.info("Successfully created workspace in database")
    schema = API_CLIENT.get_workspace_setup_url(workspace_schema.workspace.id)
    logger.info("Successfully obtained workspace url")

    if session.config.getoption("reuse_worker_role"):
        logger.info(
            "Getting IAM roles from predefined TestWorkerRole CloudFormation stack"
        )
        cf = boto3.client("cloudformation")
        response = cf.describe_stacks(StackName="TestWorkerRole")
        outputs = response["Stacks"][0].get("Outputs", [])
        outputs_dict = {o["OutputKey"]: o["OutputValue"] for o in outputs}
        parameters = [
            {
                "ParameterKey": "WorkerRoleArn",
                "ParameterValue": outputs_dict["WorkerRoleArn"],
            },
            {
                "ParameterKey": "WorkerInstanceProfileArn",
                "ParameterValue": outputs_dict["WorkerRoleInstanceProfileArn"],
            },
        ]
    else:
        logger.info("No worker role ARN provided, re-creating them.")
        parameters = []

    cf_client = boto3.client("cloudformation")
    logger.info("Creating cloudformation stack")
    cf_client.create_stack(
        StackName=cfg.workspace_name,
        TemplateURL=schema.full_template_url,
        Capabilities=["CAPABILITY_IAM"],
        Parameters=parameters,
    )
    w = Workspace._from_api_schema(workspace_schema.workspace)
    logger.info("Waiting on workspace deployment")
    w.wait_until_active()
    logger.info("Workspace done")


# In dev we 'stop' clusters to have the ability to debug them
# However this means you can't delete the stack, so we need to manually terminate them
# This is a temporary hack before we properly stop clusters
def terminate_stopped_ec2_instances(cfg: WorkspaceConfig) -> None:
    try:
        ec2 = boto3.client("ec2")
        workspace = Workspace(cfg.workspace_name, organization=cfg.organization_name)
        response = ec2.describe_instances(
            Filters=[
                {"Name": "tag:PolarsWorkspaceId", "Values": [str(workspace.id)]},
            ]
        )
        instance_ids = [
            instance["InstanceId"]
            for reservation in response["Reservations"]
            for instance in reservation["Instances"]
        ]

        if instance_ids:
            logger.info("Terminating instances: %s", instance_ids)
            ec2.terminate_instances(InstanceIds=instance_ids)
        else:
            logger.info("Instances of fleet have already been terminated")
    except Exception as e:
        logger.warning("Error occurred while terminating ec2 instances %s", e)


def remove_workspace(cfg: WorkspaceConfig):
    """Teardown of the workspace."""
    try:
        terminate_stopped_ec2_instances(cfg)
        cf_client = boto3.client("cloudformation")
        logger.info("Deleting cloudformation stack")
        cf_client.delete_stack(StackName=cfg.workspace_name)
        logger.info("Deleted cloudformation stack")
    except:  # noqa: E722
        pass


@pytest.fixture(scope="session")
def workspace_name(request):
    if is_master(request.config):
        return request.config.workspace_name
    return request.config.workerinput["workspace_name"]


def encode_auth_headers(id: str, secret: str):
    token_plain = f"{id}:{secret}"
    token_encoded = base64.urlsafe_b64encode(token_plain.encode()).decode()
    return {
        "Authorization": f"Basic {token_encoded}",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }


def _retrieve_token(client_id: str, client_secret: str) -> str:
    """Retrieve the token using client credentials."""
    url = f"https://{AUTH_DOMAIN}/realms/Polars/protocol/openid-connect/token"
    data = {"grant_type": "client_credentials"}
    headers = encode_auth_headers(id=client_id, secret=client_secret)

    logger.debug("Sending auth request to %s", url)
    response = requests.post(url, data=data, headers=headers)

    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        msg = "authentication failed"
        raise RuntimeError(msg) from e

    response_json = response.json()
    return response_json["access_token"]


def inner_authenticate(noninteractive: bool) -> None:
    if noninteractive:
        client_id = os.environ["CI_CLIENT_ID"]
        client_secret = os.environ["CI_CLIENT_SECRET"]
        token = _retrieve_token(client_id, client_secret)
        os.environ["POLARS_CLOUD_ACCESS_TOKEN"] = token
    else:
        pc.authenticate()


def authenticate(request) -> None:
    noninteractive = request.config.getoption("noninteractive")
    logger.debug(
        "Running in %s mode", "noninteractive" if noninteractive else "interactive"
    )
    inner_authenticate(noninteractive)


@pytest.fixture
def aws_s3_uri(workspace: Workspace, request: pytest.FixtureRequest) -> str:
    return f"s3://polars-cloud-{workspace.id}/{request.param}"


@pytest.fixture
def proxy_compute(
    workspace: Workspace, request: pytest.FixtureRequest
) -> Generator[ComputeContext]:
    ctx = pc.ComputeContext(
        workspace=workspace, **asdict(request.param), connection_mode="proxy"
    )
    logger.debug("Starting compute %s", asdict(request.param))
    ctx.start(wait=True)
    yield ctx
    logger.debug("Stopping compute %s", asdict(request.param))
    ctx.stop()


@pytest.fixture
def direct_compute(
    workspace: Workspace, request: pytest.FixtureRequest
) -> Generator[ComputeContext]:
    ctx = pc.ComputeContext(
        workspace=workspace,
        **asdict(request.param),
        connection_mode="direct",
    )
    logger.debug("Starting compute %s", asdict(request.param))
    ctx.start(wait=True)
    yield ctx
    logger.debug("Stopping compute %s", asdict(request.param))
    ctx.stop()
