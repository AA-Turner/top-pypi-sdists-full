import logging
import os

from fluidattacks_core.logging.types import EnvironmentMetadata, JobMetadata


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
