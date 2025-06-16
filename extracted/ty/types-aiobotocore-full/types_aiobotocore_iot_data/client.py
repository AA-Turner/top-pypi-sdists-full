"""
Type annotations for iot-data service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iot_data.client import IoTDataPlaneClient

    session = get_session()
    async with session.create_client("iot-data") as client:
        client: IoTDataPlaneClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListRetainedMessagesPaginator
from .type_defs import (
    DeleteThingShadowRequestTypeDef,
    DeleteThingShadowResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetRetainedMessageRequestTypeDef,
    GetRetainedMessageResponseTypeDef,
    GetThingShadowRequestTypeDef,
    GetThingShadowResponseTypeDef,
    ListNamedShadowsForThingRequestTypeDef,
    ListNamedShadowsForThingResponseTypeDef,
    ListRetainedMessagesRequestTypeDef,
    ListRetainedMessagesResponseTypeDef,
    PublishRequestTypeDef,
    UpdateThingShadowRequestTypeDef,
    UpdateThingShadowResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("IoTDataPlaneClient",)


class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    MethodNotAllowedException: Type[BotocoreClientError]
    RequestEntityTooLargeException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    UnsupportedDocumentEncodingException: Type[BotocoreClientError]


class IoTDataPlaneClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTDataPlaneClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/client/#generate_presigned_url)
        """

    async def delete_thing_shadow(
        self, **kwargs: Unpack[DeleteThingShadowRequestTypeDef]
    ) -> DeleteThingShadowResponseTypeDef:
        """
        Deletes the shadow for the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data/client/delete_thing_shadow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/client/#delete_thing_shadow)
        """

    async def get_retained_message(
        self, **kwargs: Unpack[GetRetainedMessageRequestTypeDef]
    ) -> GetRetainedMessageResponseTypeDef:
        """
        Gets the details of a single retained message for the specified topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data/client/get_retained_message.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/client/#get_retained_message)
        """

    async def get_thing_shadow(
        self, **kwargs: Unpack[GetThingShadowRequestTypeDef]
    ) -> GetThingShadowResponseTypeDef:
        """
        Gets the shadow for the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data/client/get_thing_shadow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/client/#get_thing_shadow)
        """

    async def list_named_shadows_for_thing(
        self, **kwargs: Unpack[ListNamedShadowsForThingRequestTypeDef]
    ) -> ListNamedShadowsForThingResponseTypeDef:
        """
        Lists the shadows for the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data/client/list_named_shadows_for_thing.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/client/#list_named_shadows_for_thing)
        """

    async def list_retained_messages(
        self, **kwargs: Unpack[ListRetainedMessagesRequestTypeDef]
    ) -> ListRetainedMessagesResponseTypeDef:
        """
        Lists summary information about the retained messages stored for the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data/client/list_retained_messages.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/client/#list_retained_messages)
        """

    async def publish(
        self, **kwargs: Unpack[PublishRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Publishes an MQTT message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data/client/publish.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/client/#publish)
        """

    async def update_thing_shadow(
        self, **kwargs: Unpack[UpdateThingShadowRequestTypeDef]
    ) -> UpdateThingShadowResponseTypeDef:
        """
        Updates the shadow for the specified thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data/client/update_thing_shadow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/client/#update_thing_shadow)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_retained_messages"]
    ) -> ListRetainedMessagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data.html#IoTDataPlane.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/client/)
        """
