import os
from typing import Any, Optional

import boto3


class Clients:
    s3_client: Optional[Any] = None
    sqs_client: Optional[Any] = None
    sts_client: Optional[Any] = None

    def reset(self):
        self.s3_client = None
        self.sqs_client = None
        self.sts_client = None


clients = Clients()


def get_client_kwargs() -> dict:
    _kwargs = {}
    if os.environ.get("MOTO_ENDPOINT_URL"):
        _kwargs["endpoint_url"] = os.environ["MOTO_ENDPOINT_URL"]
    return _kwargs


def get_s3_client():
    if clients.s3_client is None:
        clients.s3_client = boto3.client("s3", **get_client_kwargs())
    return clients.s3_client


def get_sqs_client():
    if clients.sqs_client is None:
        clients.sqs_client = boto3.client("sqs", **get_client_kwargs())
    return clients.sqs_client


def get_sts_client():
    if clients.sts_client is None:
        clients.sts_client = boto3.client("sts", **get_client_kwargs())
    return clients.sts_client
