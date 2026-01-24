import logging
import os
from typing import Optional

from .client import get_sts_client


class AWSConfig:
    """
    AWSConfig provides access to AWS configuration parameters such as region and account ID.

    Attributes:
        _aws_region (Optional[str]): Cached AWS region value.
        _account_id (Optional[str]): Cached AWS account ID value.

    Properties:
        aws_region (str): Returns the AWS region, checking environment variables
            'AWS_REGION' and 'AWS_DEFAULT_REGION'. Raises ValueError if not found.
        account_id (str): Returns the AWS account ID, checking environment variable
            'ASYNC_LAMBDA_ACCOUNT_ID' or fetching from STS if not set. Raises ValueError if not found.

    Methods:
        reset(): Clears cached region and account ID values.
    """

    _aws_region: Optional[str] = None
    _account_id: Optional[str] = None

    @property
    def aws_region(self):
        """
        Retrieves the AWS region from the environment variables.

        Returns:
            str: The AWS region, either from the cached value, 'AWS_REGION', or 'AWS_DEFAULT_REGION' environment variables.

        Raises:
            ValueError: If neither 'AWS_REGION' nor 'AWS_DEFAULT_REGION' is set in the environment.
        """
        if self._aws_region:
            return self._aws_region
        self._aws_region = os.environ.get(
            "AWS_REGION", os.environ.get("AWS_DEFAULT_REGION")
        )
        if self._aws_region is None:
            raise ValueError("Unable to find AWS_REGION for constructing ARN or URL")
        return self._aws_region

    @property
    def account_id(self):
        """
        Retrieves the AWS account ID associated with the current environment.

        The method attempts to obtain the account ID in the following order:
        1. Returns the cached account ID if already set.
        2. Attempts to fetch the account ID from the 'ASYNC_LAMBDA_ACCOUNT_ID' environment variable.
        3. If not found, retrieves the account ID using the AWS STS client's `get_caller_identity` method.
        4. Logs the fetched account ID if obtained from STS.
        5. Raises a ValueError if the account ID cannot be determined from any source.

        Returns:
            str: The AWS account ID.

        Raises:
            ValueError: If the account ID cannot be determined from the environment or STS.
        """
        if self._account_id:
            return self._account_id
        self._account_id = os.environ.get("ASYNC_LAMBDA_ACCOUNT_ID")
        if self._account_id is not None:
            return self._account_id
        self._account_id = get_sts_client().get_caller_identity().get("Account")
        logging.info(f"Fetched account_id from sts: {self._account_id}")
        if self._account_id is None:
            raise ValueError("Unable to get ACCOUNT_ID from env or STS.")
        return self._account_id

    def reset(self):
        """
        Resets the AWS region and account ID attributes to None.

        This method clears the current values of `_aws_region` and `_account_id`,
        effectively resetting the environment configuration.
        """
        self._aws_region = None
        self._account_id = None


aws_config = AWSConfig()


def reset():
    """
    Resets the AWS configuration to its default state by calling the reset method on aws_config.
    """
    aws_config.reset()


def is_build_mode() -> bool:
    """
    Checks if the application is running in build mode.

    Returns:
        bool: True if the 'ASYNC_LAMBDA_BUILD_MODE' environment variable is set (and truthy), False otherwise.
    """
    return bool(os.environ.get("ASYNC_LAMBDA_BUILD_MODE", False))


def get_aws_region() -> str:
    """
    Retrieves the AWS region from the current AWS configuration.

    Returns:
        str: The AWS region as specified in the configuration.
    """
    return aws_config.aws_region


def get_aws_account_id() -> str:
    """
    Retrieves the AWS account ID from the current AWS configuration.

    Returns:
        str: The AWS account ID.
    """
    return aws_config.account_id


def get_payload_bucket() -> str:
    """
    Retrieves the name of the S3 bucket used for async lambda payloads from the environment variables.

    Returns:
        str: The value of the 'ASYNC_LAMBDA_PAYLOAD_S3_BUCKET' environment variable.

    Raises:
        KeyError: If 'ASYNC_LAMBDA_PAYLOAD_S3_BUCKET' is not set in the environment.
    """
    return os.environ["ASYNC_LAMBDA_PAYLOAD_S3_BUCKET"]


def get_current_task_id() -> str:
    """
    Retrieves the current asynchronous lambda task ID from the environment variables.
    This will be set via cloudformation to identify which task should be executed in a given lambda function.

    Returns:
        str: The value of the 'ASYNC_LAMBDA_TASK_ID' environment variable.

    Raises:
        KeyError: If 'ASYNC_LAMBDA_TASK_ID' is not set in the environment.
    """
    return os.environ["ASYNC_LAMBDA_TASK_ID"]


def is_cloud() -> bool:
    """
    Determines if the current environment is running on AWS Lambda.

    Returns:
        bool: True if the 'AWS_LAMBDA_FUNCTION_NAME' environment variable is set, indicating execution within AWS Lambda; False otherwise.
    """
    return bool(os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))


def enable_force_sync_mode():
    """
    Enables force sync mode for async-lambda by setting the
    'ASYNC_LAMBDA_FORCE_SYNC' environment variable to '1'.

    This forces asynchronous operations to run in synchronous mode,
    which can be useful for debugging or testing purposes.
    """
    os.environ["ASYNC_LAMBDA_FORCE_SYNC"] = "1"


def disable_force_sync_mode():
    """
    Disables the force sync mode for async lambda by removing the
    'ASYNC_LAMBDA_FORCE_SYNC' environment variable.

    If the environment variable is not set, logs a warning indicating
    that force sync mode is already disabled.
    """
    try:
        del os.environ["ASYNC_LAMBDA_FORCE_SYNC"]
    except KeyError:
        logging.warning("Force Sync mode is already disabled.")


def get_force_sync_mode() -> bool:
    """
    Checks the environment variable 'ASYNC_LAMBDA_FORCE_SYNC' to determine if synchronous mode should be forced.

    Returns:
        bool: True if 'ASYNC_LAMBDA_FORCE_SYNC' is set (to any value), False otherwise.
    """
    return bool(os.environ.get("ASYNC_LAMBDA_FORCE_SYNC", ""))


def get_batch_failure_retry_count() -> int:
    """
    Retrieves the batch failure retry count from the environment variable 'ASYNC_LAMBDA_BATCH_FAILURE_RETRY_COUNT'.

    Returns:
        int: The number of times to retry batch failures. Defaults to 20 if the environment variable is not set.
    """
    return int(os.environ.get("ASYNC_LAMBDA_BATCH_FAILURE_RETRY_COUNT", 20))
