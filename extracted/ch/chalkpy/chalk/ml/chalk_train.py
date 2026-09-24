import itertools
import os
import uuid
import warnings
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Mapping, Optional, Protocol, Sequence, Union
from urllib.parse import urlparse

from chalk.client.client_grpc import MODEL_TRAINING_METRIC_PREFIX, ChalkGRPCClient
from chalk.client.exc import ChalkAuthException
from chalk.client.models import RegisterModelArtifactResponse
from chalk.config.auth_config import load_token
from chalk.ml.utils import (
    CHALK_CHECKPOINT_DIR_ENV_VAR,
    CHALK_TRAINING_RUN_ID_ENV_VAR,
    MODEL_TRAIN_METADATA_EXPERIMENT_NAME,
    MODEL_TRAIN_METADATA_HYPERPARAMETERS,
    MODEL_TRAIN_METADATA_OUTPUT_METRICS,
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
        path: Optional[str] = None,
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
        path: Optional[str] = None,
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
            path=path,
        )

    def last_checkpoint_path(self, run_id: Optional[str] = None) -> Optional[str]:
        checkpoint_dir = os.getenv(CHALK_CHECKPOINT_DIR_ENV_VAR)
        if not checkpoint_dir:
            return None

        latest_pointer = os.path.join(checkpoint_dir, "latest")
        if os.path.exists(latest_pointer):
            with open(latest_pointer) as f:
                artifact_path = f.read().strip()
            if artifact_path:
                return os.path.join(checkpoint_dir, artifact_path)

        training_run_id = run_id or get_model_training_run_id_from_env()
        if not training_run_id:
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
    path: Optional[str] = None,
) -> RegisterModelArtifactResponse:
    return CheckpointClass.checkpoint(
        model=model, additional_files=additional_files, metadata=metadata, run_name=run_name, path=path
    )


def last_checkpoint_path(run_id: Optional[str] = None) -> Optional[str]:
    return CheckpointClass.last_checkpoint_path(run_id=run_id)


def log_metrics(metrics: Mapping[str, float | int], tags: Mapping[str, str] | None = None) -> None:
    CheckpointClass.log_metrics(metrics, tags=tags)


HyperparameterValue = Union[float, str, bool, int]

MAX_EXPERIMENT_TRAINING_RUNS = 20


@dataclass
class ExperimentRun:
    """The result of training a single hyperparameter combination as part of an `Experiment`."""

    success: bool
    hyperparameters: Mapping[str, HyperparameterValue]
    experiment_id: str
    run_id: Optional[str] = None
    error: Optional[str] = None
    handle: Optional[Any] = None
    """The underlying ``chalkcompute.TrainingRunHandle``, if the run was created successfully."""


class Experiment:
    """Run a grid search over hyperparameters by creating one v2 training run per combination.

    Each combination is submitted with ``chalkcompute.training(...).run_training(...)``,
    which is the same mechanism used by the ``@chalkcompute.training`` decorator to create
    training runs via the ``CreateTrainingRun`` RPC.

    Parameters
    ----------
    experiment_name : str
        The base name for this experiment. Each training run is named
        ``f"{experiment_name}-{i}"``, where ``i`` is the index of its hyperparameter
        combination in `hyperparameter_grid()`.
    train_fn : Callable[..., Any]
        The training function to run for each hyperparameter combination, e.g.
        ``def train(df, config): ...``. See ``chalkcompute.training`` for its expected shape.
    hyperparameters : Mapping[str, Sequence[float | str | bool | int]]
        A mapping from hyperparameter name to the list of values to grid search over. One
        training run is created for every combination in the cartesian product of these values.
        Each combination is passed to `train_fn` as `config`. The cartesian product may not
        exceed `MAX_EXPERIMENT_TRAINING_RUNS` (20) combinations.
    output_metrics : Sequence[str]
        The names of the metric(s) that `train_fn` is expected to report (e.g. via
        `chalk.ml.log_metrics`) for each run.
    data, dataset, input_sql : Optional[str]
        Exactly one must be provided; forwarded to ``chalkcompute.training``.
    image : Optional[chalkcompute.Image]
        The base image to train from; forwarded to ``chalkcompute.training``.
    cpu, memory, gpu : Optional[str]
        Resource requests; forwarded to ``chalkcompute.training``.
    env : Optional[Mapping[str, str | chalkcompute.Secret]]
        Environment variables/secrets; forwarded to ``chalkcompute.training``.
    secrets : Optional[List[chalkcompute.Secret]]
        Secrets to mount; forwarded to ``chalkcompute.training``.
    max_retries : Optional[int]
        Maximum number of retries per training run; forwarded to ``chalkcompute.training``.
    client : Optional[chalkcompute.ConnectClient]
        The client used to submit each run. If not provided, a default one is constructed.

    Examples
    --------
    >>> from chalk.ml.chalk_train import Experiment
    >>> def train(df, config):
    ...     model = train_my_model(df, lr=config["lr"], batch_size=config["batch_size"])
    ...     return model
    >>> experiment = Experiment(
    ...     experiment_name="my-experiment",
    ...     train_fn=train,
    ...     hyperparameters={"lr": [0.01, 0.1], "batch_size": [16, 32]},
    ...     output_metrics=["accuracy"],
    ...     dataset="my_dataset",
    ... )
    >>> runs = experiment.run()
    """

    def __init__(
        self,
        experiment_name: str,
        train_fn: Callable[..., Any],
        hyperparameters: Mapping[str, Sequence[HyperparameterValue]],
        output_metrics: Sequence[str],
        data: Optional[str] = None,
        dataset: Optional[str] = None,
        input_sql: Optional[str] = None,
        image: Optional[Any] = None,
        cpu: Optional[str] = None,
        memory: Optional[str] = None,
        gpu: Optional[str] = None,
        env: Optional[Mapping[str, Any]] = None,
        secrets: Optional[List[Any]] = None,
        max_retries: Optional[int] = None,
        client: Optional[Any] = None,
    ) -> None:
        super().__init__()
        if not callable(train_fn):
            raise ValueError("train_fn must be a callable function.")
        if len(hyperparameters) == 0:
            raise ValueError("hyperparameters must specify at least one hyperparameter to search over.")
        for name, values in hyperparameters.items():
            if len(list(values)) == 0:
                raise ValueError(f"hyperparameter '{name}' must specify at least one candidate value.")
        if len(output_metrics) == 0:
            raise ValueError("output_metrics must specify at least one metric name.")

        grid_size = 1
        for values in hyperparameters.values():
            grid_size *= len(list(values))
        if grid_size > MAX_EXPERIMENT_TRAINING_RUNS:
            raise ValueError(
                f"hyperparameter grid produces {grid_size} training runs, which exceeds the maximum of "
                + f"{MAX_EXPERIMENT_TRAINING_RUNS}. Reduce the number of hyperparameters or candidate values."
            )

        unknown_metrics = sorted(set(output_metrics) - VALID_MODEL_TRAINING_METRICS)
        if unknown_metrics:
            warnings.warn(
                "Unknown output metric(s): "
                + ", ".join(unknown_metrics)
                + ". These will not be reportable via `chalk.ml.log_metrics`.",
                stacklevel=2,
            )

        self.experiment_name = experiment_name
        self.train_fn = train_fn
        self.hyperparameters = hyperparameters
        self.output_metrics = list(output_metrics)
        self.data = data
        self.dataset = dataset
        self.input_sql = input_sql
        self.image = image
        self.cpu = cpu
        self.memory = memory
        self.gpu = gpu
        self.env = env
        self.secrets = secrets
        self.max_retries = max_retries
        self.client = client

    def hyperparameter_grid(self) -> List[Dict[str, HyperparameterValue]]:
        """The list of hyperparameter combinations that `run()` will train, one per training run."""
        names = list(self.hyperparameters.keys())
        value_lists = [list(self.hyperparameters[name]) for name in names]
        return [dict(zip(names, combo)) for combo in itertools.product(*value_lists)]

    def run(self) -> List[ExperimentRun]:
        """Create one v2 training run for every hyperparameter combination in the grid.

        Each training run's metadata includes a `chalk_model_train_hyperparameters` entry
        with the hyperparameter values used for that run, as well as entries for the
        experiment name and the expected output metrics.

        Returns
        -------
        List[ExperimentRun]
            One `ExperimentRun` per hyperparameter combination, in the order they were run.
        """
        try:
            from chalkcompute import training as chalkcompute_training  # pyright: ignore[reportMissingImports]
        except ImportError as e:
            raise RuntimeError("Experiment requires the 'chalkcompute' package to create v2 training runs.") from e

        experiment_id = str(uuid.uuid4())

        runs: List[ExperimentRun] = []
        for i, combo in enumerate(self.hyperparameter_grid()):
            training_fn = chalkcompute_training(
                self.train_fn,
                data=self.data,
                dataset=self.dataset,
                input_sql=self.input_sql,
                image=self.image,
                name=f"{self.experiment_name}-{i}",
                cpu=self.cpu,
                memory=self.memory,
                gpu=self.gpu,
                env=self.env,
                secrets=self.secrets,
                metadata={
                    MODEL_TRAIN_METADATA_HYPERPARAMETERS: combo,
                    MODEL_TRAIN_METADATA_EXPERIMENT_NAME: self.experiment_name,
                    MODEL_TRAIN_METADATA_OUTPUT_METRICS: self.output_metrics,
                },
                max_retries=self.max_retries,
            )
            try:
                handle = training_fn.run_training(config=combo, client=self.client, experiment_id=experiment_id)
            except Exception as e:
                runs.append(
                    ExperimentRun(success=False, hyperparameters=combo, experiment_id=experiment_id, error=str(e))
                )
                continue
            runs.append(
                ExperimentRun(
                    success=True,
                    hyperparameters=combo,
                    experiment_id=experiment_id,
                    run_id=handle.run_id,
                    handle=handle,
                )
            )
        return runs
