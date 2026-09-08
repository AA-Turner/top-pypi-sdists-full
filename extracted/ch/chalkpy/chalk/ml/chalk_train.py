import os
import warnings
from typing import Any, Dict, List, Mapping, Optional, Protocol
from urllib.parse import urlparse

from chalk.client.client_grpc import MODEL_TRAINING_METRIC_PREFIX, ChalkGRPCClient
from chalk.client.exc import ChalkAuthException
from chalk.client.models import RegisterModelArtifactResponse
from chalk.config.auth_config import load_token
from chalk.ml.utils import (
    CHALK_CHECKPOINT_DIR_ENV_VAR,
    CHALK_TRAINING_RUN_ID_ENV_VAR,
    MODEL_TRAIN_METADATA_RUN_ID,
    MODEL_TRAIN_METADATA_RUN_NAME,
    get_model_metadata_run_name_from_env,
    get_model_training_run_id_from_env,
)

VALID_MODEL_TRAINING_METRICS = {
    "accuracy",
    "loss",
    "mae",
    "mse",
    "precision",
    "r2",
    "recall",
    "rmse",
    "f1",
}


def _statsd_tags(tags: Mapping[str, str]) -> list[str]:
    return [f"{key}:{value}" for key, value in tags.items()]


def _training_metrics_statsd_port(default: int) -> int:
    port = os.environ.get("STATSD_PORT")
    if port is None:
        return default
    try:
        return int(port)
    except ValueError:
        return default


def _get_training_metrics_statsd() -> Any | None:
    try:
        from datadog.dogstatsd import DogStatsd
    except ImportError:
        return None

    dogstatsd_url = os.environ.get("DD_DOGSTATSD_URL")
    if dogstatsd_url:
        parsed = urlparse(dogstatsd_url)
        if parsed.scheme == "unix":
            return DogStatsd(socket_path=parsed.path)
        if parsed.scheme in {"udp", "dogstatsd"} and parsed.hostname is not None:
            return DogStatsd(host=parsed.hostname, port=parsed.port or _training_metrics_statsd_port(8125))

    socket_path = os.environ.get("STATSD_SOCKET_PATH")
    if socket_path:
        return DogStatsd(socket_path=socket_path)

    statsd_host = os.environ.get("STATSD_HOST") or os.environ.get("DD_AGENT_HOST")
    if statsd_host:
        return DogStatsd(host=statsd_host, port=_training_metrics_statsd_port(8125))

    host_ip = os.environ.get("HOST_IP")
    if host_ip:
        return DogStatsd(host=host_ip, port=_training_metrics_statsd_port(8127))

    return None


def _emit_training_metrics_to_statsd(metrics: Mapping[str, float | int], tags: Mapping[str, str]) -> None:
    from chalk.utils.tracing import safe_set_gauge

    metric_tags = _statsd_tags(tags)
    statsd = _get_training_metrics_statsd()
    for name, value in metrics.items():
        metric_name = f"{MODEL_TRAINING_METRIC_PREFIX}{name}"
        if statsd is None:
            safe_set_gauge(metric_name, value, tags=metric_tags)
        else:
            statsd.gauge(metric_name, value, tags=metric_tags)


class Checkpointer(Protocol):
    def checkpoint(
        self,
        model: Any,
        additional_files: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        run_name: Optional[str] = None,
    ) -> RegisterModelArtifactResponse: ...

    def last_checkpoint_path(self, run_id: Optional[str] = None) -> Optional[str]: ...

    def log_metrics(self, metrics: Mapping[str, float | int], tags: Mapping[str, str] | None = None) -> None: ...


class ClientCheckpointer:
    def __init__(self):
        self._client: Optional[ChalkGRPCClient] = None
        super().__init__()

    def _get_client(self) -> ChalkGRPCClient:
        if self._client is None:
            token = load_token(client_id=None, client_secret=None, active_environment=None, api_server=None)

            if token is None:
                raise ChalkAuthException()

            self._client = ChalkGRPCClient(
                client_id=token.clientId,
                client_secret=token.clientSecret,
                environment=token.activeEnvironment,
                api_server=token.apiServer,
            )
        return self._client

    def checkpoint(
        self,
        model: Any,
        additional_files: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        run_name: Optional[str] = None,
    ) -> RegisterModelArtifactResponse:
        client = self._get_client()

        if metadata is None:
            metadata = {}
        metadata[MODEL_TRAIN_METADATA_RUN_NAME] = run_name if run_name else get_model_metadata_run_name_from_env()

        training_run_id = get_model_training_run_id_from_env()
        if not training_run_id:
            raise RuntimeError(f"No training run ID found. Expected env var {CHALK_TRAINING_RUN_ID_ENV_VAR} to be set.")
        metadata[MODEL_TRAIN_METADATA_RUN_ID] = training_run_id
        return client._checkpoint_training_run(  # pyright: ignore[reportPrivateUsage]
            training_run_id=training_run_id,
            model=model,
            additional_files=additional_files,
            metadata=metadata,
        )

    def last_checkpoint_path(self, run_id: Optional[str] = None) -> Optional[str]:
        training_run_id = run_id or get_model_training_run_id_from_env()
        checkpoint_dir = os.getenv(CHALK_CHECKPOINT_DIR_ENV_VAR)
        if not training_run_id or not checkpoint_dir:
            return None

        artifact = self._get_client().get_latest_checkpoint(training_run_id=training_run_id)
        if artifact is None or artifact.path == "":
            return None
        return os.path.join(checkpoint_dir, artifact.path)

    def log_metrics(self, metrics: Mapping[str, float | int], tags: Mapping[str, str] | None = None) -> None:
        unknown_metrics = sorted(set(metrics) - VALID_MODEL_TRAINING_METRICS)
        if unknown_metrics:
            warnings.warn(
                "Unknown model training metric(s): "
                + ", ".join(unknown_metrics)
                + ". These metrics will not be reported.",
                stacklevel=2,
            )
        metrics_to_report = {name: value for name, value in metrics.items() if name in VALID_MODEL_TRAINING_METRICS}
        if len(metrics_to_report) == 0:
            raise ValueError("No valid model training metrics to report.")
        training_run_id = get_model_training_run_id_from_env()
        if training_run_id == "":
            raise ValueError("No model training run id found in the environment.")
        metric_tags = dict(tags or {})
        metric_tags["training_run_id"] = training_run_id
        self._get_client().report_training_metrics(
            training_run_id=training_run_id,
            metrics=metrics_to_report,
            tags=metric_tags,
        )
        _emit_training_metrics_to_statsd(metrics_to_report, metric_tags)


CheckpointClass: Checkpointer = ClientCheckpointer()


def checkpoint(
    model: Any,
    additional_files: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    run_name: Optional[str] = None,
) -> RegisterModelArtifactResponse:
    return CheckpointClass.checkpoint(
        model=model, additional_files=additional_files, metadata=metadata, run_name=run_name
    )


def last_checkpoint_path(run_id: Optional[str] = None) -> Optional[str]:
    return CheckpointClass.last_checkpoint_path(run_id=run_id)


def log_metrics(metrics: Mapping[str, float | int], tags: Mapping[str, str] | None = None) -> None:
    CheckpointClass.log_metrics(metrics, tags=tags)
