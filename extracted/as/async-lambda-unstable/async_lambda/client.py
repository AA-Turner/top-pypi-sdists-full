import os
from typing import Any, Optional

import boto3


class Clients:
    """
    A container class for AWS service clients.

    Attributes:
        s3_client (Optional[Any]): The AWS S3 client instance.
        sqs_client (Optional[Any]): The AWS SQS client instance.
        sts_client (Optional[Any]): The AWS STS client instance.

    Methods:
        reset():
            Resets all client instances to None.
    """

    s3_client: Optional[Any] = None
    sqs_client: Optional[Any] = None
    sts_client: Optional[Any] = None

    def reset(self):
        """
        Resets the AWS service clients (S3, SQS, STS) by setting them to None.
        """
        self.s3_client = None
        self.sqs_client = None
        self.sts_client = None


clients = Clients()


def get_client_kwargs() -> dict:
    """
    Returns a dictionary of keyword arguments for configuring a client.

    If the environment variable 'MOTO_ENDPOINT_URL' is set, includes it as the 'endpoint_url' in the returned dictionary.

    Returns:
        dict: Dictionary containing client configuration keyword arguments.
    """
    _kwargs = {}
    if os.environ.get("MOTO_ENDPOINT_URL"):
        _kwargs["endpoint_url"] = os.environ["MOTO_ENDPOINT_URL"]
    return _kwargs


def get_s3_client():
    """
    Returns a cached AWS S3 client instance.

    If the client does not exist, it creates a new one using boto3 with the provided keyword arguments.
    Subsequent calls will return the cached client.

    Returns:
        boto3.client: An AWS S3 client instance.
    """
    if clients.s3_client is None:
        clients.s3_client = boto3.client("s3", **get_client_kwargs())
    return clients.s3_client


def get_sqs_client():
    """
    Returns a cached AWS SQS client instance.

    If the client does not exist, it creates a new one using boto3 with the provided keyword arguments.
    Subsequent calls will return the cached client.

    Returns:
        boto3.client: An AWS SQS client instance.
    """
    if clients.sqs_client is None:
        clients.sqs_client = boto3.client("sqs", **get_client_kwargs())
    return clients.sqs_client


def get_sts_client():
    """
    Returns a cached AWS STS client instance.

    If the client does not exist, it creates a new one using boto3 with the provided keyword arguments.
    Subsequent calls will return the cached client.

    Returns:
        boto3.client: An AWS STS client instance.
    """
    if clients.sts_client is None:
        clients.sts_client = boto3.client("sts", **get_client_kwargs())
    return clients.sts_client
