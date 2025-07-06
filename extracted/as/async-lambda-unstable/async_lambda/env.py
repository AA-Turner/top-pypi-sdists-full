import logging
import os
from typing import Optional

from .client import get_sts_client


class AWSConfig:
    _aws_region: Optional[str] = None
    _account_id: Optional[str] = None

    @property
    def aws_region(self):
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
        self._aws_region = None
        self._account_id = None


aws_config = AWSConfig()


def reset():
    aws_config.reset()


def is_build_mode() -> bool:
    return bool(os.environ.get("ASYNC_LAMBDA_BUILD_MODE", False))


def get_aws_region() -> str:
    return aws_config.aws_region


def get_aws_account_id() -> str:
    return aws_config.account_id


def get_payload_bucket() -> str:
    return os.environ["ASYNC_LAMBDA_PAYLOAD_S3_BUCKET"]


def get_current_task_id() -> str:
    return os.environ["ASYNC_LAMBDA_TASK_ID"]


def is_cloud() -> bool:
    return bool(os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))


def enable_force_sync_mode():
    os.environ["ASYNC_LAMBDA_FORCE_SYNC"] = "1"


def disable_force_sync_mode():
    del os.environ["ASYNC_LAMBDA_FORCE_SYNC"]


def get_force_sync_mode() -> bool:
    return bool(os.environ.get("ASYNC_LAMBDA_FORCE_SYNC", ""))
