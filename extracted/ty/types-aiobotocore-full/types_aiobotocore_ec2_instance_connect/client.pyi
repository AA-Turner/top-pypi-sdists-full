"""
Type annotations for ec2-instance-connect service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ec2_instance_connect.client import EC2InstanceConnectClient

    session = get_session()
    async with session.create_client("ec2-instance-connect") as client:
        client: EC2InstanceConnectClient
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    SendSerialConsoleSSHPublicKeyRequestTypeDef,
    SendSerialConsoleSSHPublicKeyResponseTypeDef,
    SendSSHPublicKeyRequestTypeDef,
    SendSSHPublicKeyResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack

__all__ = ("EC2InstanceConnectClient",)

class Exceptions(BaseClientExceptions):
    AuthException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    EC2InstanceNotFoundException: type[BotocoreClientError]
    EC2InstanceStateInvalidException: type[BotocoreClientError]
    EC2InstanceTypeInvalidException: type[BotocoreClientError]
    EC2InstanceUnavailableException: type[BotocoreClientError]
    InvalidArgsException: type[BotocoreClientError]
    SerialConsoleAccessDisabledException: type[BotocoreClientError]
    SerialConsoleSessionLimitExceededException: type[BotocoreClientError]
    SerialConsoleSessionUnavailableException: type[BotocoreClientError]
    SerialConsoleSessionUnsupportedException: type[BotocoreClientError]
    ServiceException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]

class EC2InstanceConnectClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EC2InstanceConnectClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/client/#generate_presigned_url)
        """

    async def send_ssh_public_key(
        self, **kwargs: Unpack[SendSSHPublicKeyRequestTypeDef]
    ) -> SendSSHPublicKeyResponseTypeDef:
        """
        Pushes an SSH public key to the specified EC2 instance for use by the specified
        user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect/client/send_ssh_public_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/client/#send_ssh_public_key)
        """

    async def send_serial_console_ssh_public_key(
        self, **kwargs: Unpack[SendSerialConsoleSSHPublicKeyRequestTypeDef]
    ) -> SendSerialConsoleSSHPublicKeyResponseTypeDef:
        """
        Pushes an SSH public key to the specified EC2 instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect/client/send_serial_console_ssh_public_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/client/#send_serial_console_ssh_public_key)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2-instance-connect.html#EC2InstanceConnect.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/client/)
        """
