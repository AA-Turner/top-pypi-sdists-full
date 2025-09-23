import logging
import os
from typing import Any, Literal

from fluidattacks_core.logging.types import EnvironmentMetadata, JobMetadata

PipelineType = Literal["gitlab_ci", "circleci", "azure_devops", "jenkins"]

DEFAULT_TELEMETRY_METADATA = {}


def is_trunk_branch() -> bool:
    """Check if code is using the trunk branch."""
    return os.environ.get("CI_COMMIT_REF_NAME", "default") == "trunk"


def get_job_metadata() -> JobMetadata:
    """Get the job metadata for applications running in batch environments."""
    return JobMetadata(
        job_id=os.environ.get("AWS_BATCH_JOB_ID"),
        job_queue=os.environ.get("AWS_BATCH_JQ_NAME", "default"),
        compute_environment=os.environ.get("AWS_BATCH_CE_NAME", "default"),
    )


def get_environment_metadata() -> EnvironmentMetadata:
    """Get the environment metadata for applications."""
    environment = "production" if is_trunk_branch() else "development"
    product_id = os.environ.get("PRODUCT_ID", "universe")
    commit_sha = os.environ.get("CI_COMMIT_SHA", "00000000")
    commit_short_sha = commit_sha[:8]

    return EnvironmentMetadata(
        environment=environment,
        version=commit_short_sha,
        product_id=product_id,
    )


def debug_logs() -> None:
    """Test all the log levels in the root logger and a custom logger."""
    root_logger = logging.getLogger()

    root_logger.debug("This is a debug log")
    root_logger.info("This is an info log")
    root_logger.warning("This is a warning log")
    root_logger.error("This is an error log")
    root_logger.critical("This is a critical log")

    logger = logging.getLogger("test-logger")
    logger.debug("This is a debug log")
    logger.info("This is an info log")
    logger.warning("This is a warning log")
    logger.error("This is an error log")
    logger.critical("This is a critical log")

    try:
        raise KeyError("missing_key")  # noqa: TRY301
    except KeyError as e:
        root_logger.exception(e)
        logger.exception(e)


def get_pipeline_environment() -> PipelineType | None:
    if os.environ.get("CI_JOB_ID", None):
        return "gitlab_ci"
    if os.environ.get("CIRCLECI", None):
        return "circleci"
    if os.environ.get("System.JobId", None):  # noqa: SIM112
        return "azure_devops"
    if os.environ.get("BUILD_NUMBER", None):
        return "jenkins"
    return None


def get_pipeline_metadata(pipeline: PipelineType | None) -> dict[str, str]:
    if pipeline == "gitlab_ci":
        return {
            "CI_JOB_ID": os.environ.get("CI_JOB_ID", "unknown"),
            "CI_JOB_URL": os.environ.get("CI_JOB_URL", "unknown"),
        }
    if pipeline == "circleci":
        return {
            "CIRCLE_BUILD_NUM": os.environ.get("CIRCLE_BUILD_NUM", "unknown"),
            "CIRCLE_BUILD_URL": os.environ.get("CIRCLE_BUILD_URL", "unknown"),
        }
    if pipeline == "azure_devops":
        return {
            "System.JobId": os.environ.get("System.JobId", "unknown"),  # noqa: SIM112
        }
    if pipeline == "jenkins":
        return {
            "BUILD_NUMBER": os.environ.get("BUILD_NUMBER", "unknown"),
            "BUILD_ID": os.environ.get("BUILD_ID", "unknown"),
            "BUILD_URL": os.environ.get("BUILD_URL", "unknown"),
        }
    return {}


def set_product_id(product_id: str) -> None:
    os.environ["PRODUCT_ID"] = product_id


def set_commit_sha(commit_sha: str) -> None:
    os.environ["CI_COMMIT_SHA"] = commit_sha


def set_commit_ref_name(commit_ref_name: str) -> None:
    os.environ["CI_COMMIT_REF_NAME"] = commit_ref_name


def set_telemetry_metadata(config: dict[str, Any]) -> None:
    DEFAULT_TELEMETRY_METADATA.update(config)


def get_telemetry_metadata() -> dict[str, Any]:
    return DEFAULT_TELEMETRY_METADATA
