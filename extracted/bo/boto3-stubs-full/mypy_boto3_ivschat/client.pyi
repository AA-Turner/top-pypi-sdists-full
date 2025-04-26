"""
Type annotations for ivschat service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_ivschat.client import IvschatClient

    session = Session()
    client: IvschatClient = session.client("ivschat")
    ```
"""

from __future__ import annotations

import sys
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    CreateChatTokenRequestTypeDef,
    CreateChatTokenResponseTypeDef,
    CreateLoggingConfigurationRequestTypeDef,
    CreateLoggingConfigurationResponseTypeDef,
    CreateRoomRequestTypeDef,
    CreateRoomResponseTypeDef,
    DeleteLoggingConfigurationRequestTypeDef,
    DeleteMessageRequestTypeDef,
    DeleteMessageResponseTypeDef,
    DeleteRoomRequestTypeDef,
    DisconnectUserRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetLoggingConfigurationRequestTypeDef,
    GetLoggingConfigurationResponseTypeDef,
    GetRoomRequestTypeDef,
    GetRoomResponseTypeDef,
    ListLoggingConfigurationsRequestTypeDef,
    ListLoggingConfigurationsResponseTypeDef,
    ListRoomsRequestTypeDef,
    ListRoomsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    SendEventRequestTypeDef,
    SendEventResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateLoggingConfigurationRequestTypeDef,
    UpdateLoggingConfigurationResponseTypeDef,
    UpdateRoomRequestTypeDef,
    UpdateRoomResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("IvschatClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    PendingVerification: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class IvschatClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IvschatClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat.html#Ivschat.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#generate_presigned_url)
        """

    def create_chat_token(
        self, **kwargs: Unpack[CreateChatTokenRequestTypeDef]
    ) -> CreateChatTokenResponseTypeDef:
        """
        Creates an encrypted token that is used by a chat participant to establish an
        individual WebSocket chat connection to a room.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat/client/create_chat_token.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#create_chat_token)
        """

    def create_logging_configuration(
        self, **kwargs: Unpack[CreateLoggingConfigurationRequestTypeDef]
    ) -> CreateLoggingConfigurationResponseTypeDef:
        """
        Creates a logging configuration that allows clients to store and record sent
        messages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat/client/create_logging_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#create_logging_configuration)
        """

    def create_room(self, **kwargs: Unpack[CreateRoomRequestTypeDef]) -> CreateRoomResponseTypeDef:
        """
        Creates a room that allows clients to connect and pass messages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat/client/create_room.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#create_room)
        """

    def delete_logging_configuration(
        self, **kwargs: Unpack[DeleteLoggingConfigurationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified logging configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat/client/delete_logging_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#delete_logging_configuration)
        """

    def delete_message(
        self, **kwargs: Unpack[DeleteMessageRequestTypeDef]
    ) -> DeleteMessageResponseTypeDef:
        """
        Sends an event to a specific room which directs clients to delete a specific
        message; that is, unrender it from view and delete it from the client's chat
        history.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat/client/delete_message.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#delete_message)
        """

    def delete_room(
        self, **kwargs: Unpack[DeleteRoomRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified room.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat/client/delete_room.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#delete_room)
        """

    def disconnect_user(self, **kwargs: Unpack[DisconnectUserRequestTypeDef]) -> Dict[str, Any]:
        """
        Disconnects all connections using a specified user ID from a room.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat/client/disconnect_user.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#disconnect_user)
        """

    def get_logging_configuration(
        self, **kwargs: Unpack[GetLoggingConfigurationRequestTypeDef]
    ) -> GetLoggingConfigurationResponseTypeDef:
        """
        Gets the specified logging configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat/client/get_logging_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#get_logging_configuration)
        """

    def get_room(self, **kwargs: Unpack[GetRoomRequestTypeDef]) -> GetRoomResponseTypeDef:
        """
        Gets the specified room.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat/client/get_room.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#get_room)
        """

    def list_logging_configurations(
        self, **kwargs: Unpack[ListLoggingConfigurationsRequestTypeDef]
    ) -> ListLoggingConfigurationsResponseTypeDef:
        """
        Gets summary information about all your logging configurations in the AWS
        region where the API request is processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat/client/list_logging_configurations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#list_logging_configurations)
        """

    def list_rooms(self, **kwargs: Unpack[ListRoomsRequestTypeDef]) -> ListRoomsResponseTypeDef:
        """
        Gets summary information about all your rooms in the AWS region where the API
        request is processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat/client/list_rooms.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#list_rooms)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Gets information about AWS tags for the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#list_tags_for_resource)
        """

    def send_event(self, **kwargs: Unpack[SendEventRequestTypeDef]) -> SendEventResponseTypeDef:
        """
        Sends an event to a room.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat/client/send_event.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#send_event)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds or updates tags for the AWS resource with the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes tags from the resource with the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#untag_resource)
        """

    def update_logging_configuration(
        self, **kwargs: Unpack[UpdateLoggingConfigurationRequestTypeDef]
    ) -> UpdateLoggingConfigurationResponseTypeDef:
        """
        Updates a specified logging configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat/client/update_logging_configuration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#update_logging_configuration)
        """

    def update_room(self, **kwargs: Unpack[UpdateRoomRequestTypeDef]) -> UpdateRoomResponseTypeDef:
        """
        Updates a room's configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivschat/client/update_room.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivschat/client/#update_room)
        """
