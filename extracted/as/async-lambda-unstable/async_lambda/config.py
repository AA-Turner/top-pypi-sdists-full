from typing import Optional


class AsyncLambdaConfig:
    """
    Configuration class for Async Lambda.

    Attributes:
        name (str): Name of the async lambda application. Defaults to "async-lambda".
        runtime (str): Runtime environment for the lambda function. Defaults to "python3.10".
        s3_payload_retention (int): Days to retain payloads in S3. Defaults to 30.
        default_task_memory (int): Default memory allocation (MB) for tasks. Defaults to 128.
        default_task_ephemeral_storage (int): Default disk allocation (MB) for tasks. Defaults to 512.
    """

    name: str = "async-lambda"
    runtime: str = "python3.10"
    s3_payload_retention: Optional[int] = 30
    default_task_memory: int = 128
    default_task_ephemeral_storage: int = 512


config = AsyncLambdaConfig()


def config_set_name(name: str):
    """
    Set the name of the async lambda project.

    Args:
        name (str): Name to set for the project.
    """
    config.name = name


def config_set_runtime(runtime: str):
    """
    Set the runtime environment for the project.

    Args:
        runtime (str): Runtime environment to set (e.g., "python3.10").
    """
    config.runtime = runtime


def config_set_s3_payload_retention(days: int = 30):
    """
    Set the S3 payload retention policy in days.

    Args:
        days (int, optional): Number of days to retain payloads in S3. Defaults to 30.
    """
    config.s3_payload_retention = days


def config_set_default_task_memory(memory: int = 128):
    """
    Set the default memory allocation (MB) for tasks.

    Args:
        memory (int, optional): Memory in megabytes to set as default for tasks. Defaults to 128.
    """
    config.default_task_memory = memory


def config_set_default_task_ephemeral_storage(ephemeral_storage: int = 512):
    """
    Set the default ephemeral_storage (MB) for tasks.

    Args:
        ephemeral_storage (int, optional): Disk storage in megabytes to set as default for tasks. Defaults to 512.
    """
    config.default_task_ephemeral_storage = ephemeral_storage
