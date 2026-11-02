import copy
import json
import os
import re
import warnings
from collections.abc import Mapping
from datetime import datetime
from enum import StrEnum, auto
from pathlib import Path
from typing import Any, ClassVar, Self, cast
from uuid import UUID

from aviary.functional import EnvironmentBuilder
from ldp.agent import Agent, AgentConfig
from ldp.alg.callbacks import Callback
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

MAX_CROW_JOB_RUN_TIMEOUT = 60 * 60 * 24  # 24 hours in sec
MIN_CROW_JOB_RUN_TIMEOUT = 0  # sec

DEFAULT_PYTHON_VERSION_USED_FOR_JOB_BUILDS = "3.13"

MIN_REPLICAS_FLOOR = 0
MIN_REPLICAS_CEILING = 50


class AuthType(StrEnum):
    API_KEY = auto()
    JWT = auto()


# hack to support for release-date based inputs
RELEASE_NAME_TO_ENUM_MAPPINGS = {
    "literature-20260216": "LITERATURE",
    "literature-high-20260216": "LITERATURE_HIGH",
}


class JobNames(StrEnum):
    """Enum of available jobs."""

    LITERATURE = "job-futurehouse-paperqa3"
    LITERATURE_HIGH = "job-futurehouse-paperqa3-high"
    ANALYSIS = "job-futurehouse-data-analysis-crow-high"
    MOLECULES = "job-futurehouse-data-analysis-molecules"
    PRECEDENT = "job-futurehouse-paperqa3-precedent"
    # Let's keep old names for backward compatibility
    CROW = "job-futurehouse-paperqa3"
    FALCON = "job-futurehouse-paperqa3"
    OWL = "job-futurehouse-paperqa3-precedent"
    DUMMY = "job-futurehouse-dummy-env"
    # Legacy alias: kept for historical phoenix jobs only. new submissions will get 404 and should use MOLECULES instead.
    PHOENIX = "job-futurehouse-phoenix"
    FINCH = "job-futurehouse-data-analysis-crow-high"

    @classmethod
    def get_job_descriptions(cls) -> "Mapping[JobNames, str]":
        """Get human-readable descriptions for each job type."""
        return {
            cls.LITERATURE: "Paper analysis and literature review",
            cls.LITERATURE_HIGH: (
                "High-reasoning mode paper analysis and literature review"
            ),
            cls.CROW: "Paper analysis and literature review",
            cls.FALCON: "Paper analysis and literature review",
            cls.ANALYSIS: "Data analysis with Python/notebooks",
            cls.FINCH: "Data analysis with Python/notebooks",
            cls.MOLECULES: "Molecule-related tasks and chemistry",
            cls.PHOENIX: "Molecule-related tasks and chemistry",
            cls.PRECEDENT: "Precedent review",
            cls.OWL: "Precedent review",
            cls.DUMMY: "Test/dummy environment for development",
        }

    @classmethod
    def _get_response_mapping(cls) -> "dict[JobNames, type[TaskResponse]]":
        return {
            cls.LITERATURE: PQATaskResponse,
            cls.LITERATURE_HIGH: PQATaskResponse,
            cls.ANALYSIS: PQATaskResponse,
            # data-analysis-molecules returns the same response format as other
            # data-analysis jobs (not the legacy Phoenix shape), so PQATaskResponse
            # is correct here — not PhoenixTaskResponse.
            cls.MOLECULES: PQATaskResponse,
            # Old phoenix job returns answer via environment_frame.state.state.answer
            cls.PHOENIX: PhoenixTaskResponse,
            cls.PRECEDENT: PQATaskResponse,
            cls.CROW: PQATaskResponse,
            cls.OWL: PQATaskResponse,
            cls.FINCH: FinchTaskResponse,
            cls.DUMMY: TaskResponse,
        }

    @classmethod
    def from_stage(cls, job_name: str, stage: "Stage | None" = None) -> str:
        if stage is None:
            import logging  # noqa: PLC0415

            logger = logging.getLogger(__name__)
            logger.warning(
                "Stage is not provided, Stage.PROD as default stage. "
                "Explicitly providing the stage is recommended."
            )
            stage = Stage.PROD
        return cls.from_string(job_name).value

    @classmethod
    def from_string(cls, job_name: str) -> "JobNames":
        try:
            # special-casing to capture release-dates in names (case-insensitive)
            job_name_lower = job_name.lower()
            if job_name_lower in RELEASE_NAME_TO_ENUM_MAPPINGS:
                return cls[RELEASE_NAME_TO_ENUM_MAPPINGS[job_name_lower]]
            return cls[job_name.upper()]
        except KeyError as e:
            raise ValueError(
                f"Invalid job name: {job_name}. \nOptions are: {', '.join([name.name for name in cls])}"
            ) from e

    @staticmethod
    def get_response_object_from_job(
        job_name: "str | JobNames",
    ) -> "type[TaskResponse]":
        try:
            return JobNames(job_name).get_response_object(failover=TaskResponse)
        except ValueError:
            return TaskResponse

    def get_response_object(
        self, failover: "type[TaskResponse] | None" = None
    ) -> "type[TaskResponse]":
        if failover is None:
            return self._get_response_mapping()[self]
        return self._get_response_mapping().get(self, failover)


class APIKeyPayload(BaseModel):
    api_key: str = Field(description="A user API key to authenticate with the server.")


class PriorityQueueTypes(StrEnum):
    LOW = auto()
    NORMAL = auto()
    HIGH = auto()
    ULTRA = auto()

    def rate_percentage(self) -> float:
        if self == self.LOW:
            return 0.1
        if self == self.NORMAL:
            return 0.5
        if self == self.HIGH:
            return 0.75
        if self == self.ULTRA:
            return 1.0
        raise NotImplementedError(f"Unknown priority queue type: {self}")


class RetryConfig(BaseModel):
    """Configuration for task retry settings."""

    max_attempts: int = Field(
        -1, description="Maximum number of retry attempts. -1 for infinite retries."
    )
    max_retry_duration_seconds: int = Field(
        604800,  # 7 days in seconds
        description="Maximum time a task can be retrying for before giving up (in seconds).",
    )
    max_backoff_seconds: int = Field(
        60,  # means the rate in a full-queue will be each entry trying once per minute
        description="Maximum time to wait between retries (in seconds).",
    )
    min_backoff_seconds: int = Field(
        1, description="Minimum time to wait between retries (in seconds)."
    )
    max_doublings: int = Field(
        7,
        description="Maximum number of times the retry interval can double before becoming constant.",
    )

    def to_client_dict(self) -> dict[str, Any]:
        """Convert retry config to GCP Cloud Tasks client format."""
        return {
            "max_attempts": self.max_attempts,
            "max_retry_duration": {"seconds": self.max_retry_duration_seconds},
            "max_backoff": {"seconds": self.max_backoff_seconds},
            "min_backoff": {"seconds": self.min_backoff_seconds},
            "max_doublings": self.max_doublings,
        }


class RateLimits(BaseModel):
    """Configuration for queue rate limits."""

    max_dispatches_per_second: float = Field(
        10.0,
        description=(
            "Maximum number of tasks that can be dispatched per second."
            "If this is too high, you can overshoot the rate limit as the "
            "query to running jobs is not perfectly synchronized."
        ),
    )
    max_concurrent_dispatches: int = Field(
        100,
        description=(
            "Maximum number of concurrent tasks that can be dispatched."
            " This represents how many jobs are actively trying to get "
            "a spot as a running job at the same time. The rest will "
            "simply be waiting in the queue. The higher this is, the "
            " higher gatekeeping server load will be."
        ),
    )

    MAX_RATIO_FROM_QUEUE_SIZE: ClassVar[float] = 0.1

    @classmethod
    def from_max_queue_size(cls, max_queue_size: int) -> "RateLimits":
        """Create rate limits from a max_queue_size to avoid overwhelming the gatekeeping server."""
        return cls(
            max_concurrent_dispatches=max(
                1, int(max_queue_size * cls.MAX_RATIO_FROM_QUEUE_SIZE)
            )
        )

    def to_client_dict(self) -> dict[str, Any]:
        """Convert rate limits to GCP Cloud Tasks client format."""
        return {
            "max_dispatches_per_second": self.max_dispatches_per_second,
            "max_concurrent_dispatches": self.max_concurrent_dispatches,
        }


class TaskQueue(BaseModel):
    """Configuration for a single Task Queue."""

    name: str = Field(..., description="Name of the queue")
    retry_config: RetryConfig = Field(
        default_factory=RetryConfig, description="Configuration for task retries"
    )
    rate_limits: RateLimits | None = Field(
        default=None, description="Optional rate limiting configuration"
    )
    priority_max_running_fraction: float = Field(
        default_factory=PriorityQueueTypes.NORMAL.rate_percentage,
        description=(
            "Maximum fraction of the total limit that this queue can use, proxy for priority."
            "Higher limits will essentially be preferred because they can run when "
            "lower priority queues cannot."
        ),
        ge=0.0,
        le=1.0,
    )

    @classmethod
    def from_priority_queue_type_and_max_running_jobs(
        cls, name: str, queue_type: PriorityQueueTypes, max_running_jobs: int
    ) -> "TaskQueue":
        """Create a TaskQueue from a PriorityQueueType."""
        return cls(
            name=f"{name}-{queue_type.value}",
            priority_max_running_fraction=queue_type.rate_percentage(),
            rate_limits=RateLimits.from_max_queue_size(
                int(queue_type.rate_percentage() * max_running_jobs)
            ),
        )

    def to_client_dict(self, project_id: str, location: str) -> dict[str, Any]:
        """Convert the queue configuration to GCP Cloud Tasks client format."""
        parent = f"projects/{project_id}/locations/{location}"
        queue_path = f"{parent}/queues/{self.name}"

        result = {
            "name": queue_path,
            "retry_config": self.retry_config.to_client_dict(),
        }

        if self.rate_limits:
            result["rate_limits"] = self.rate_limits.to_client_dict()

        return result


class TaskQueuesConfig(BaseModel):
    """Configuration for multiple Task Queues."""

    name: str = Field(..., description="Base name for the queue(s).")
    max_running_jobs: int = Field(
        default=30,  # low default for now
        description=(
            "Maximum concurrency for this crow job, across all queues."
            " Note: Global max across all crow jobs is 1,000, the backend will always enforce"
            " the global limit first. This limit should be set keeping in mind any dependent limits"
            " like LLM throughput."
        ),
    )
    queues: list[TaskQueue] | None = Field(
        default=None,
        description="List of task queues to be created/managed, will be built automatically if None.",
    )

    @model_validator(mode="after")
    def add_priority_queues(self):
        if self.queues is None:
            self.queues = [
                TaskQueue.from_priority_queue_type_and_max_running_jobs(
                    name=self.name,
                    queue_type=queue_type,
                    max_running_jobs=self.max_running_jobs,
                )
                for queue_type in PriorityQueueTypes
            ]
        return self

    def get_queue(self, priority_type: PriorityQueueTypes) -> TaskQueue | None:
        """Get a queue by its priority type."""
        if not self.queues:
            return None

        for queue in self.queues:
            if queue.name.endswith(f"-{priority_type.value}"):
                return queue

        return None


class Stage(StrEnum):
    DEV = "https://dev.api.platform.edisonscientific.com"
    STAGING = "https://staging.api.platform.edisonscientific.com"
    PROD = "https://api.platform.edisonscientific.com"
    LOCAL = "http://localhost:8080"
    LOCAL_DOCKER = "http://host.docker.internal:8080"

    @property
    def platform_url(self) -> str:
        """User-facing frontend URL, distinct from the API base URL in the enum value."""
        return STAGE_PLATFORM_URLS[self]

    @classmethod
    def from_string(cls, stage: str) -> "Stage":
        """Convert a case-insensitive string to Stage enum."""
        try:
            return cls[stage.upper()]
        except KeyError as e:
            raise ValueError(
                f"Invalid stage: {stage}. Must be one of: {', '.join(cls.__members__)}",
            ) from e


STAGE_PLATFORM_URLS: dict[Stage, str] = {
    Stage.DEV: "https://dev.platform.edisonscientific.com",
    Stage.STAGING: "https://staging.platform.edisonscientific.com",
    Stage.PROD: "https://platform.edisonscientific.com",
    Stage.LOCAL: "http://localhost:3000",
    # Use localhost and not host.docker.internal because this URL
    # is opened in a host browser, where host.docker.internal doesn't resolve
    Stage.LOCAL_DOCKER: "http://localhost:3000",
}


class Step(StrEnum):
    BEFORE_TRANSITION = Callback.before_transition.__name__
    AFTER_AGENT_INIT_STATE = Callback.after_agent_init_state.__name__
    AFTER_AGENT_GET_ASV = Callback.after_agent_get_asv.__name__
    AFTER_ENV_RESET = Callback.after_env_reset.__name__
    AFTER_ENV_STEP = Callback.after_env_step.__name__
    AFTER_TRANSITION = Callback.after_transition.__name__


class FramePathContentType(StrEnum):
    TEXT = auto()
    IMAGE = auto()
    MARKDOWN = auto()
    JSON = auto()
    PDF_LINK = auto()
    PDB = auto()
    NOTEBOOK = auto()
    PQA = auto()


class FramePath(BaseModel):
    path: str = Field(
        description="List of JSON path strings (e.g. 'input.data.frame') indicating where to find important frame data. None implies all data is important and the UI will render the full environment frame as is.",
    )
    type: FramePathContentType = Field(
        default=FramePathContentType.JSON,
        description="Content type of the data at this path",
    )
    is_iterable: bool = Field(
        default=False,
        description="Content of the JSON path will be iterable, this key tell us if the rendering component should create multiple components for a single key",
    )


class NamedEntity(BaseModel):
    name: str = Field(
        description=(
            "Name of an entity for a user to provide a value to during query submission. "
            "This will be used as a key to prompt users for a value. "
            "Example: 'pdb' would result in <pdb>user input here</pdb> in the task string."
        )
    )
    description: str | None = Field(
        default=None,
        description="Helper text to provide the user context to what the name or format needs to be.",
    )


class DockerContainerConfiguration(BaseModel):
    # NOTE: THIS IS COPIED FROM crow_service/models/app.py
    # KEEP IN SYNC WHEN UPDATING
    cpu: str = Field(description="CPU allotment for the container")
    memory: str = Field(description="Memory allotment for the container")
    disk_space: str = Field(
        default="10Gi",
        description="Disk space for the agent workspace volume (e.g., '10Gi')",
    )
    tmp_size: str = Field(
        default="5Gi",
        description="Size limit for the /tmp emptyDir volume (e.g., '5Gi')",
    )
    gpu_count: int | None = Field(
        default=None,
        description="Number of NVIDIA GPUs to allocate. Requires CELERY backend.",
    )

    MINIMUM_MEMORY: ClassVar[int] = 1
    MAXIMUM_MEMORY: ClassVar[int] = 32

    @field_validator("disk_space")
    @classmethod
    def validate_disk_space(cls, v: str) -> str:
        match = re.match(r"^(\d+)Gi$", v)
        if not match:
            raise ValueError("Disk space must be in Gi format (e.g., '10Gi')")
        value = int(match.group(1))
        if value < 1:
            raise ValueError("Disk space must be at least 1Gi")
        if value > 100:  # noqa: PLR2004
            raise ValueError("Disk space must not exceed 100Gi")
        return v

    @field_validator("tmp_size")
    @classmethod
    def validate_tmp_size(cls, v: str) -> str:
        match = re.match(r"^(\d+)Gi$", v)
        if not match:
            raise ValueError("tmp_size must be in Gi format (e.g., '5Gi')")
        value = int(match.group(1))
        if value < 1:
            raise ValueError("tmp_size must be at least 1Gi")
        if value > 50:  # noqa: PLR2004
            raise ValueError("tmp_size must not exceed 50Gi")
        return v

    @field_validator("memory")
    @classmethod
    def validate_memory(cls, v: str) -> str:
        # https://regex101.com/r/4kWjKw/1
        match = re.match(r"^(\d+)Gi$", v)

        if not match:
            raise ValueError("Memory must be in Gi format (e.g., '2Gi')")

        value = int(match.group(1))

        # GCP Cloud Run has min 512Mi (0.5Gi) and max 32Gi
        # https://cloud.google.com/run/docs/configuring/services/memory-limits
        # We enforce a practical minimum of 1Gi for production workloads
        if value < cls.MINIMUM_MEMORY:
            raise ValueError("Memory must be at least 1Gi")
        if value > cls.MAXIMUM_MEMORY:
            raise ValueError("Memory must not exceed 32Gi")

        return v


class CacheStrategy(StrEnum):
    USE_CACHE = "use_cache"
    NO_CACHE = "no_cache"


class ImageRegistry(StrEnum):
    GAR = auto()
    ECR = auto()


class GitDeploymentInfo(BaseModel):
    """Git-related deployment information for reproducibility tracking."""

    commit_hash: str | None = None
    git_patch: str | None = None
    branch_name: str | None = None
    git_status: str | None = None
    agent_image: str | None = None


class JobDeploymentConfig(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        arbitrary_types_allowed=True,  # Allows for agent: Agent | str
    )

    requirements_path: str | os.PathLike | None = Field(
        default=None,
        description="The complete path including filename to the requirements.txt file or pyproject.toml file. If not provided explicitly, it will be inferred from the path parameter.",
    )

    path: str | os.PathLike | None = Field(
        default=None,
        description="The path to your python module. Can be either a string path or Path object. "
        "This path should be the root directory of your module. "
        "This path either must include a pyproject.toml with UV tooling, or a requirements.txt for dependency resolution. "
        "Can be None if we are deploying a functional environment (through the functional_environment parameter).",
    )

    ignore_dirs: list[str] | None = Field(
        default=None,
        description="A list of directories to ignore when deploying the job. "
        "This is a list of directories relative to the path parameter.",
    )

    name: str = Field(
        description="The name of the crow job.",
    )

    environment: str = Field(
        description="Your environment path, should be a module reference if we pass an environment. "
        "Can be an arbitrary name if we are deploying a functional environment "
        "(through the functional_environment parameter). "
        "This path does not have to be importable locally, just in the job's container.",
        examples=["aviary.env.DummyEnv"],
    )

    functional_environment: EnvironmentBuilder | None = Field(
        default=None,
        description="An object of type EnvironmentBuilder used to construct an environment. "
        "Can be None if we are deploying a non functional environment.",
    )

    requirements: list[str] | None = Field(
        default=None,
        description="A list of dependencies required for the deployment, similar to the Python requirements.txt file. "
        "Each entry in the list specifies a package or module in the format used by pip (e.g., 'package-name==1.0.0'). "
        "Can be None if we are deploying a non functional environment (functional_environment parameter is None)",
    )

    environment_variables: dict[str, str] | None = Field(
        default=None,
        description="Any key value pair of environment variables your environment needs to function.",
    )

    container_config: DockerContainerConfiguration | None = Field(
        default=None,
        description="The configuration for the cloud run container.",
    )

    python_version: str = Field(
        default=DEFAULT_PYTHON_VERSION_USED_FOR_JOB_BUILDS,
        description="The python version your docker image should build with (e.g., '3.11', '3.12', '3.13').",
    )

    agent: Agent | AgentConfig | str = Field(
        default="ldp.agent.SimpleAgent",
        description="Your desired agent path, should be a module reference and a fully qualified name. "
        "example: ldp.agent.SimpleAgent or by instantiating AgentConfig to further customize the agent.",
    )

    requires_aviary_internal: bool = Field(
        default=False,
        description="Indicates your project requires aviary-internal to function. "
        "This is only necessary for envs within aviary-internal.",
    )

    timeout: int | None = Field(
        default=600,
        description="The amount of time in seconds your crow will run on a task before it terminates.",
        ge=MIN_CROW_JOB_RUN_TIMEOUT,
        le=MAX_CROW_JOB_RUN_TIMEOUT,
    )

    max_steps: int | None = Field(
        default=None,
        description="Deprecated: max_steps is no longer used. Use timeout instead.",
        deprecated=True,
    )

    force: bool = Field(
        default=False,
        description="If true, immediately overwrite any existing job with the same name.",
    )

    storage_location: str = Field(
        default="storage",
        description="The location the container will use to mount a locally accessible GCS folder as a volume. "
        "This location can be used to store and fetch files safely without GCS apis or direct access.",
        deprecated=True,
    )

    @field_validator("storage_location")
    @classmethod
    def warn_storage_dir_deprecated(cls, v):
        warnings.warn(
            "The 'storage_location' has been deprecated and this feature is no longer supported. "
            "If your job requires storage, please use the data-storage api to store artifacts.",
            DeprecationWarning,
            stacklevel=2,
        )
        return v

    frame_paths: list[FramePath] | None = Field(
        default=None,
        description="List of FramePath which indicates where to find important frame data, and how to render it.",
    )

    markdown_template_path: str | os.PathLike | None = Field(
        default=None,
        description="The path to the markdown template file. This file will be dynamically built within the environment frame section of the UI. "
        "The keys used in the markdown file follow the same requirement as FramePath.path. None implies no markdown template is present and the UI "
        "will render the environment frame as is.",
    )

    task_queues_config: TaskQueuesConfig | None = Field(
        default=None,
        description="The configuration for the task queue(s) that will be created for this deployment.",
    )

    user_input_config: list[NamedEntity] | None = Field(
        default=None,
        description=(
            "List of NamedEntity objects that represent user input fields "
            "to be included in the task string. "
            "These will be used to prompt users for values during query submission."
        ),
    )
    cache_strategy: CacheStrategy = Field(
        default=CacheStrategy.USE_CACHE,
        description="The cache strategy to use for the task",
    )

    push_to: list[ImageRegistry] = Field(
        default_factory=lambda: [ImageRegistry.GAR, ImageRegistry.ECR],
        description="Registries the built image should be available in.",
    )

    @model_validator(mode="after")
    def validate_min_replicas_for_sandbox(self) -> Self:
        env_vars = self.environment_variables
        if not env_vars or env_vars.get("EXECUTION_BACKEND") != "agent_sandbox":
            return self
        rv = env_vars.get("MIN_REPLICAS")
        if rv is None:
            raise ValueError(
                "MIN_REPLICAS is required when EXECUTION_BACKEND=agent_sandbox"
            )
        try:
            v = int(rv)
        except (ValueError, TypeError):
            raise ValueError(
                f"MIN_REPLICAS must be castable to an integer, got: {rv!r}"
            ) from None
        if v < MIN_REPLICAS_FLOOR or v > MIN_REPLICAS_CEILING:
            raise ValueError(
                f"MIN_REPLICAS must be between {MIN_REPLICAS_FLOOR} and {MIN_REPLICAS_CEILING}, got: {v}"
            )
        return self

    @field_validator("markdown_template_path")
    @classmethod
    def validate_markdown_path(
        cls, v: str | os.PathLike | None
    ) -> str | os.PathLike | None:
        if v is not None:
            path = Path(v)
            if path.suffix.lower() not in {".md", ".markdown"}:
                raise ValueError(
                    f"Markdown template must be a .md or .markdown extension: {path}"
                )
        return v

    task_description: str | None = Field(
        default=None,
        description="Override for the task description, if not included it will be pulled from your "
        "environment `from_task` docstring. Necessary if you are deploying using an Environment class"
        " as a dependency.",
    )

    commit_hash: str | None = Field(
        default=None,
        description="Git commit hash of the deployed code for reproducibility tracking.",
    )

    git_patch: str | None = Field(
        default=None,
        description="Git diff of uncommitted changes at deployment time. "
        "Use with commit_hash to recreate exact code state.",
    )

    branch_name: str | None = Field(
        default=None,
        description="Git branch name at deployment time.",
    )

    git_status: str | None = Field(
        default=None,
        description="Git status output at deployment time, showing untracked files.",
    )

    is_chat: bool = Field(
        default=False,
        description=("Whether this crow is a chat-session agent"),
    )

    image_uri: str | None = Field(
        default=None,
        description="A pre-built image URI to deploy, skipping Cloud Build.",
    )
    sandbox_infra_manager_image: str | None = Field(
        default=None,
        description="Sandbox infra-manager image URI for agent_sandbox deployments.",
    )

    @field_validator("path")
    @classmethod
    def validate_module_path(cls, value: str | os.PathLike) -> str | os.PathLike:
        path = Path(value)
        if not path.exists():
            raise ValueError(f"Module path {path} does not exist")
        if not path.is_dir():
            raise ValueError(f"Module path {path} is not a directory")
        return value

    @field_validator("requirements_path")
    @classmethod
    def validate_requirements_path(
        cls, value: str | os.PathLike | None
    ) -> str | os.PathLike | None:
        if value is None:
            return value

        path = Path(value)
        if not path.exists():
            raise ValueError(f"Requirements path {path} does not exist")
        if not path.is_file():
            raise ValueError(f"Requirements path {path} is not a file")
        if path.suffix not in {".txt", ".toml"}:
            raise ValueError(f"Requirements path {path} must be a .txt or .toml file")
        return value

    @model_validator(mode="after")
    def validate_path_and_requirements(self) -> Self:
        if self.path is None:
            return self

        path = Path(self.path)
        requirements_path = (
            Path(self.requirements_path) if self.requirements_path else None
        )

        if not (
            (path / "pyproject.toml").exists()
            or (path / "requirements.txt").exists()
            or (requirements_path and requirements_path.exists())
        ):
            raise ValueError(
                f"Module path {path} must contain either pyproject.toml or requirements.txt, "
                f"or a valid requirements_path must be provided"
            )

        if not self.task_queues_config:
            self.task_queues_config = TaskQueuesConfig(name=self.job_name)

        return self

    @field_validator("environment")
    @classmethod
    def validate_environment_path(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Environment path cannot be empty")
        if not all(part.isidentifier() for part in value.split(".")):
            raise ValueError(f"Invalid environment path format: {value}")
        return value

    @field_validator("agent")
    @classmethod
    def validate_agent(
        cls, value: str | Agent | AgentConfig
    ) -> str | Agent | AgentConfig:
        if isinstance(value, AgentConfig):
            return value

        if isinstance(value, Agent):
            return value

        if not value or not value.strip():
            raise ValueError("Agent path cannot be empty")
        if not all(part.isidentifier() for part in value.split(".")):
            raise ValueError(f"Invalid agent path format: {value}")
        return value

    @property
    def module_name(self) -> str:
        if not self.path and not self.functional_environment:
            raise ValueError(
                "No module specified, either a path or a functional environment must be provided."
            )
        if self.path:
            # module_name is used in the build to copy the contents of self.path into /app/{module_name}/
            # If self.path is provided, we want its contents to land in /app/ directly, not /app/{self.path.name}/
            # Therefore, return empty string here. NOTE: if we were to use self.path.name, we get inconsistent
            # behavior between path=Path('.') and path=Path('.').absolute(). TODO: get rid of this path-dependency
            # on module_name, since module_name isn't a well-defined concept in the non-functional case.
            return ""
        return cast(EnvironmentBuilder, self.functional_environment).__name__  # type: ignore[attr-defined]

    @property
    def job_name(self) -> str:
        """Name to be used for the crow job deployment.

        Deprecated: Use `name` directly. Kept for backward compatibility.
        """
        return self.name


class RuntimeConfig(BaseModel):
    """Runtime configuration for crow job execution.

    This advanced configuration is only available for supported crows.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, extra="forbid")

    timeout: int | None = Field(
        default=None, description="Maximum execution time in seconds"
    )
    max_steps: int | None = Field(
        default=None,
        description="Deprecated: max_steps is no longer used. Use timeout instead.",
        deprecated=True,
    )
    agent: Agent | AgentConfig | None = Field(
        default=None,
        description=(
            "Agent configuration to use for this job. If None, it will default to the "
            "agent selected during Crow deployment in the JobDeploymentConfig object."
        ),
    )
    environment_config: dict[str, Any] | None = Field(
        default=None,
        description=(
            "Kwargs to be passed to the environment constructor at runtime. "
            "Not all environments support this functionality. "
            "For file attachments, include 'data_storage_uris' key with a list of "
            "data entry URIs (format: 'data_entry:{uuid}'). "
            "Example: {'data_storage_uris': ['data_entry:123...']}"
        ),
    )
    continued_job_id: UUID | None = Field(
        default=None,
        description="Optional job identifier for a continued job",
    )
    world_model_id: UUID | str | None = Field(
        default=None,
        description="Optional world model identifier for the task",
    )

    @field_validator("agent")
    @classmethod
    def validate_agent(
        cls, value: str | AgentConfig | None
    ) -> str | AgentConfig | None:
        if value is None:
            return None

        if isinstance(value, AgentConfig):
            return value

        if not value or not value.strip():
            raise ValueError("Agent path cannot be empty")
        if not all(part.isidentifier() for part in value.split(".")):
            raise ValueError(f"Invalid agent path format: {value}")
        return value

    @field_validator("environment_config")
    @classmethod
    def validate_environment_config(
        cls, value: dict[str, Any] | None
    ) -> dict[str, Any] | None:
        if value is None:
            return None
        try:
            json.dumps(value)
        except (TypeError, OverflowError) as err:
            raise ValueError("Environment config must be JSON serializable") from err
        return value


class TrajectoryQueryParams(BaseModel):
    """Params for trajectories with filtering."""

    model_config = ConfigDict(extra="forbid")

    project_id: UUID | None = Field(
        default=None, description="Optional project ID to filter trajectories by"
    )
    name: str | None = Field(
        default=None, description="Optional name filter for trajectories"
    )
    user: str | None = Field(
        default=None, description="Optional user email filter for trajectories"
    )
    limit: int = Field(
        default=50,
        ge=1,
        le=200,
        description="Maximum number of trajectories to return (max: 200)",
    )
    offset: int = Field(
        default=0, ge=0, description="Number of trajectories to skip for pagination"
    )
    sort_by: str = Field(default="created_at", description="Field to sort by")
    sort_order: str = Field(default="desc", description="Sort order")
    tags: str | None = Field(
        default=None, description="Optional tag filter for trajectories"
    )

    @field_validator("sort_by")
    @classmethod
    def validate_sort_by(cls, v: str) -> str:
        if v not in {"created_at", "name"}:
            raise ValueError("sort_by must be either 'created_at' or 'name'")
        return v

    @field_validator("sort_order")
    @classmethod
    def validate_sort_order(cls, v: str) -> str:
        if v not in {"asc", "desc"}:
            raise ValueError("sort_order must be either 'asc' or 'desc'")
        return v

    def to_query_params(self) -> dict[str, str | int]:
        params: dict[str, str | int] = {
            "limit": self.limit,
            "offset": self.offset,
            "sort_by": self.sort_by,
            "sort_order": self.sort_order,
        }
        if self.project_id is not None:
            params["project_id"] = str(self.project_id)
        if self.name is not None:
            params["name"] = self.name
        if self.user is not None:
            params["user"] = self.user
        if self.tags is not None:
            params["tags"] = self.tags
        return params


class TaskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: UUID | None = Field(
        default=None,
        description="Optional task identifier",
        alias="id",
    )
    project_id: UUID | None = Field(
        default=None,
        description="Optional group identifier for the task",
    )
    persona_id: UUID | None = Field(
        default=None,
        description="Persona project ID that owns `project_id`",
    )
    name: str | JobNames = Field(
        description="Name of the crow to execute eg. paperqa-crow"
    )
    query: str = Field(description="Query or task to be executed by the crow")
    runtime_config: RuntimeConfig | None = Field(
        default=None, description="All optional runtime parameters for the job"
    )
    caller_target_id: UUID | None = Field(
        default=None,
        description="Target ID to notify via /conversations/queue when this task completes",
    )
    caller_project_id: UUID | None = Field(
        default=None,
        description="Project ID for the /conversations/queue completion notification",
    )
    tags: list[str] | None = Field(
        default=None,
        description="Grouping association tags for a task.",
    )
    workspace_id: str | None = Field(
        default=None,
        description="DSS workspace entry UUID for persistent storage across sandbox pods. "
        "Create a workspace via EdisonClient.create_workspace() and pass the entry id here.",
    )

    @model_validator(mode="after")
    def validate_caller_fields(self) -> Self:
        has_target = self.caller_target_id is not None
        has_project = self.caller_project_id is not None
        if has_target != has_project:
            msg = "caller_target_id and caller_project_id must both be set or both be unset"
            raise ValueError(msg)
        return self


class SimpleOrganization(BaseModel):
    id: int
    name: str
    display_name: str


class LiteTaskResponse(BaseModel):
    task_id: UUID = Field(description="Identifier for a trajectory")
    query: str = Field(description="Query executed for the trajectory")
    status: str = Field(description="Current status of the trajectory")

    @model_validator(mode="before")
    @classmethod
    def validate_fields(cls, original_data: Mapping[str, Any]) -> Mapping[str, Any]:
        data = copy.deepcopy(original_data)  # Avoid mutating the original data
        if not isinstance(data, dict):
            return data
        data["query"] = data.get("task", data.get("query"))
        data["task_id"] = cast(UUID, data.get("id", data.get("task_id")))
        return data


class TaskResponse(BaseModel):
    """Base class for task responses. This holds attributes shared over all futurehouse jobs."""

    model_config = ConfigDict(extra="ignore")

    status: str
    query: str
    user: str | None = None
    created_at: datetime
    job_name: str
    share_status: str
    permitted_accessors: dict[str, list[str | int]] | None = None
    build_owner: str | None = None
    environment_name: str | None = None
    agent_name: str | None = None
    task_id: UUID | None = None
    project_id: UUID | None = None
    task_summary: str | None = Field(
        default=None,
        description="Short title the platform writes for a task long enough to need one.",
    )

    @model_validator(mode="before")
    @classmethod
    def validate_fields(cls, original_data: Mapping[str, Any]) -> Mapping[str, Any]:
        data = copy.deepcopy(original_data)  # Avoid mutating the original data
        # Extract fields from environment frame state
        if not isinstance(data, dict):
            return data
        # TODO: [PLA-1154] We probably want to remove these two once we define the final names.
        data["job_name"] = data.get("crow")
        data["query"] = data.get("task")
        data["task_id"] = cast(UUID, data.get("id")) if data.get("id") else None
        if not (metadata := data.get("metadata", {})):
            return data
        data["environment_name"] = metadata.get("environment_name")
        data["agent_name"] = metadata.get("agent_name")
        return data


class PhoenixTaskResponse(TaskResponse):
    """
    Response scheme for tasks executed with Phoenix.

    Additional fields:
        answer: Final answer from Phoenix
    """

    model_config = ConfigDict(extra="ignore")
    answer: str | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_phoenix_fields(
        cls, original_data: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        data = copy.deepcopy(original_data)
        if not isinstance(data, dict):
            return data
        if not (env_frame := data.get("environment_frame", {})):
            return data
        state = env_frame.get("state", {}).get("state", {})
        data["answer"] = state.get("answer")
        return data


class FinchTaskResponse(TaskResponse):
    """
    Response scheme for tasks executed with Finch.

    Additional fields:
        answer: Final answer from Finch
        notebook: a dictionary with `cells` and `metadata` regarding the notebook content
    """

    model_config = ConfigDict(extra="ignore")
    answer: str | None = None
    notebook: dict[str, Any] | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_finch_fields(
        cls, original_data: Mapping[str, Any]
    ) -> Mapping[str, Any]:
        data = copy.deepcopy(original_data)
        if not isinstance(data, dict):
            return data
        if not (env_frame := data.get("environment_frame", {})):
            return data
        state = env_frame.get("state", {}).get("state", {})
        data["answer"] = state.get("answer")
        data["notebook"] = state.get("nb_state")
        return data


class PQATaskResponse(TaskResponse):
    """
    Response scheme for tasks executed with PQA.

    Additional fields:
        answer: Final answer from PQA
        formatted_answer: Formatted answer from PQA
        answer_reasoning: Reasoning used to generate the final answer, if available
        has_successful_answer: Whether the answer is successful
    """

    model_config = ConfigDict(extra="ignore")

    answer: str | None = None
    formatted_answer: str | None = None
    answer_reasoning: str | None = None
    has_successful_answer: bool | None = None
    total_cost: float | None = None
    total_queries: int | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_pqa_fields(cls, original_data: Mapping[str, Any]) -> Mapping[str, Any]:
        data = copy.deepcopy(original_data)  # Avoid mutating the original data
        if not isinstance(data, dict):
            return data
        if not (env_frame := data.get("environment_frame", {})):
            return data
        state = env_frame.get("state", {}).get("state", {})
        response = state.get("response", {})
        answer = response.get("answer", {})
        usage = state.get("info", {}).get("usage", {})

        # Add additional PQA specific fields to data so that pydantic can validate the model
        data["answer"] = answer.get("answer")
        data["formatted_answer"] = answer.get("formatted_answer")
        data["answer_reasoning"] = answer.get("answer_reasoning")
        data["has_successful_answer"] = answer.get("has_successful_answer")
        data["total_cost"] = cast(float, usage.get("total_cost"))
        data["total_queries"] = cast(int, usage.get("total_queries"))

        return data

    def clean_verbose(self) -> "TaskResponse":
        """Clean the verbose response from the server."""
        self.request = None  # pylint: disable=attribute-defined-outside-init
        self.response = None  # pylint: disable=attribute-defined-outside-init
        return self


class TaskResponseVerbose(TaskResponse):
    """Class for responses to include all the fields of a task response."""

    model_config = ConfigDict(extra="allow")

    share_status: str
    agent_state: list[dict[str, Any]] | None = None
    environment_frame: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None
    permitted_accessors: dict[str, list[str | int]] | None = None
    deployment_config: GitDeploymentInfo | dict[str, Any] | None = None
    gcloud_operation_name: str | None = None
    started_at: datetime | None = None
