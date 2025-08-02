import base64

from _qwak_proto.qwak.ecosystem.v0.ecosystem_runtime_service_pb2 import (
    GetCloudCredentialsParameters,
    GetCloudCredentialsRequest,
    PermissionSet,
    PullModelsContainerRegistry,
)
from google.protobuf.duration_pb2 import Duration
from qwak.clients.administration.eco_system.client import EcosystemClient
from qwak.clients.build_orchestrator import BuildOrchestratorClient
from qwak.exceptions import QwakException
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.progress import Progress

from qwak_sdk.commands.models.deployments.deploy._logic.deploy_config import (
    DeployConfig,
)

tasks = {}


def local_deploy(config: DeployConfig):
    try:
        import docker
    except ImportError:
        raise QwakException(
            "Error: 'docker' package is required to for local model deployment."
        )

    console = Console()
    console.print(Panel(f"Deploying model {config.model_id} locally", style="green"))

    client = docker.from_env()
    build_image = _get_build_image(config)

    if not client.images.list(name=build_image):
        console.print(
            "Pulling serving image from Qwak's remote repository. Might take a few minutes...",
            style="yellow",
        )
        _docker_login(client)
        _image_pull(client, build_image)

    try:
        container = start_local_qwak_container(build_image, client, config)
        container.reload()
        host_port = container.ports.get("5000/tcp")[0]["HostPort"]

        layout = example_usage_layout(host_port)
        console.print(layout)

        for line in container.logs(stream=True):
            console.print(str(line.strip().decode()), style="blue")

    except KeyboardInterrupt:
        console.print(Panel("Stopping container...", style="red"))
        container.stop()
        container.remove()


def example_usage_layout(host_port: str):
    layout = Layout(size=6)
    layout.split_row(
        Layout(name="left"),
        Layout(name="right"),
    )
    layout["left"].update(
        Panel(
            f"[bold]cURL usage:[bold]\n\n"
            f"curl --location\n"
            f"--request POST http://localhost:{host_port}/predict\n"
            f"--header 'Content-Type: application/json'\n"
            f"--data '...'",
            style="green",
        )
    )
    layout["right"].update(
        Panel(
            f"[bold]Python client usage:[bold]\n\n"
            f"from qwak_inference import RealtimeClient\n\nfeature_vector=[...]\n"
            f"client = RealTimeClient(model_api='http://localhost:{host_port}/predict')\n"
            f"client.predict(feature_vector)",
            style="green",
        )
    )
    return layout


def start_local_qwak_container(build_image: str, docker_client, config: DeployConfig):
    return docker_client.containers.run(
        build_image,
        command=["bentoml", "serve-gunicorn", "./"],
        entrypoint="./docker-entrypoint.sh",
        environment=[
            "BENTOML_GUNICORN_WORKERS=2",
            "QWAK_DEBUG_MODE=True",
            f"QWAK_MODEL_ID={config.model_id}",
            "BENTOML_DO_NOT_TRACK=True",
            "PYTHONPATH=/qwak/model_dir:/qwak/model_dir/main:$PYTHONPATH",
            f"QWAK_BUILD_ID={config.build_id}",
            "BUNDLE_PATH=/home/bentoml/bundle",
            "BENTOML_HOME=/home/bentoml/",
        ],
        stream=True,
        detach=True,
        publish_all_ports=True,
    )


def _get_build_image(config: DeployConfig):
    return (
        BuildOrchestratorClient().get_build(config.build_id).build.build_destined_image
    )


def _show_progress(line, progress):
    if line["status"] == "Downloading":
        idx = f'[red][Download {line["id"]}]'
    elif line["status"] == "Extracting":
        idx = f'[green][Extract {line["id"]}]'
    else:
        # skip other statuses
        return

    if idx not in tasks.keys():
        tasks[idx] = progress.add_task(f"{idx}", total=line["progressDetail"]["total"])
    else:
        progress.update(tasks[idx], completed=line["progressDetail"]["current"])


def _image_pull(docker_client, image_name: str):
    with Progress() as progress:
        resp = docker_client.api.pull(image_name, stream=True, decode=True)
        for line in resp:
            _show_progress(line, progress)


def _docker_login(docker_client):
    try:
        import boto3
    except ImportError:
        raise QwakException(
            "Error: The 'boto3' package is necessary for local model deployment. Install it directly or by running"
            " 'pip install qwak[local-deployment]'"
        )

    # TODO: block if not an AWS based container registry
    credentials = _get_aws_credentials()

    aws_credentials = credentials.cloud_credentials.aws_temporary_credentials
    ecr_client = boto3.Session(
        aws_access_key_id=aws_credentials.access_key_id,
        aws_secret_access_key=aws_credentials.secret_access_key,
        aws_session_token=aws_credentials.session_token,
        region_name=aws_credentials.region,
    ).client("ecr")

    ecr_credentials = ecr_client.get_authorization_token()["authorizationData"][0]

    try:
        docker_client.login(
            username="AWS",
            registry=ecr_credentials["proxyEndpoint"],
            password=base64.b64decode(ecr_credentials["authorizationToken"])
            .replace(b"AWS:", b"")
            .decode("utf-8"),
        )

    except Exception as e:
        raise QwakException(f"Failed to login to Qwak's container registry: {e}")


def _get_aws_credentials():
    try:
        eco_client = EcosystemClient()
        credentials = eco_client.get_cloud_credentials(
            request=GetCloudCredentialsRequest(
                parameters=GetCloudCredentialsParameters(
                    duration=Duration(seconds=60 * 60, nanos=0),  # 6 hours
                    permission_set=PermissionSet(
                        pull_models_container_registry=PullModelsContainerRegistry()
                    ),
                )
            )
        )
        return credentials
    except Exception as e:
        raise QwakException(
            f"Failed to get credentials to pull image from Qwak's container registry: {e}."
        )
