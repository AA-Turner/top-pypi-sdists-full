"""
Type annotations for connectparticipant service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_connectparticipant.client import ConnectParticipantClient

    session = get_session()
    async with session.create_client("connectparticipant") as client:
        client: ConnectParticipantClient
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

from .type_defs import (
    CancelParticipantAuthenticationRequestTypeDef,
    CompleteAttachmentUploadRequestTypeDef,
    CreateParticipantConnectionRequestTypeDef,
    CreateParticipantConnectionResponseTypeDef,
    DescribeViewRequestTypeDef,
    DescribeViewResponseTypeDef,
    DisconnectParticipantRequestTypeDef,
    GetAttachmentRequestTypeDef,
    GetAttachmentResponseTypeDef,
    GetAuthenticationUrlRequestTypeDef,
    GetAuthenticationUrlResponseTypeDef,
    GetTranscriptRequestTypeDef,
    GetTranscriptResponseTypeDef,
    SendEventRequestTypeDef,
    SendEventResponseTypeDef,
    SendMessageRequestTypeDef,
    SendMessageResponseTypeDef,
    StartAttachmentUploadRequestTypeDef,
    StartAttachmentUploadResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack


__all__ = ("ConnectParticipantClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ConnectParticipantClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ConnectParticipantClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#generate_presigned_url)
        """

    async def cancel_participant_authentication(
        self, **kwargs: Unpack[CancelParticipantAuthenticationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Cancels the authentication session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/cancel_participant_authentication.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#cancel_participant_authentication)
        """

    async def complete_attachment_upload(
        self, **kwargs: Unpack[CompleteAttachmentUploadRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Allows you to confirm that the attachment has been uploaded using the
        pre-signed URL provided in StartAttachmentUpload API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/complete_attachment_upload.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#complete_attachment_upload)
        """

    async def create_participant_connection(
        self, **kwargs: Unpack[CreateParticipantConnectionRequestTypeDef]
    ) -> CreateParticipantConnectionResponseTypeDef:
        """
        Creates the participant's connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/create_participant_connection.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#create_participant_connection)
        """

    async def describe_view(
        self, **kwargs: Unpack[DescribeViewRequestTypeDef]
    ) -> DescribeViewResponseTypeDef:
        """
        Retrieves the view for the specified view token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/describe_view.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#describe_view)
        """

    async def disconnect_participant(
        self, **kwargs: Unpack[DisconnectParticipantRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disconnects a participant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/disconnect_participant.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#disconnect_participant)
        """

    async def get_attachment(
        self, **kwargs: Unpack[GetAttachmentRequestTypeDef]
    ) -> GetAttachmentResponseTypeDef:
        """
        Provides a pre-signed URL for download of a completed attachment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/get_attachment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#get_attachment)
        """

    async def get_authentication_url(
        self, **kwargs: Unpack[GetAuthenticationUrlRequestTypeDef]
    ) -> GetAuthenticationUrlResponseTypeDef:
        """
        Retrieves the AuthenticationUrl for the current authentication session for the
        AuthenticateCustomer flow block.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/get_authentication_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#get_authentication_url)
        """

    async def get_transcript(
        self, **kwargs: Unpack[GetTranscriptRequestTypeDef]
    ) -> GetTranscriptResponseTypeDef:
        """
        Retrieves a transcript of the session, including details about any attachments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/get_transcript.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#get_transcript)
        """

    async def send_event(
        self, **kwargs: Unpack[SendEventRequestTypeDef]
    ) -> SendEventResponseTypeDef:
        """
        The
        <code>application/vnd.amazonaws.connect.event.connection.acknowledged</code>
        ContentType will no longer be supported starting December 31, 2024.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/send_event.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#send_event)
        """

    async def send_message(
        self, **kwargs: Unpack[SendMessageRequestTypeDef]
    ) -> SendMessageResponseTypeDef:
        """
        Sends a message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/send_message.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#send_message)
        """

    async def start_attachment_upload(
        self, **kwargs: Unpack[StartAttachmentUploadRequestTypeDef]
    ) -> StartAttachmentUploadResponseTypeDef:
        """
        Provides a pre-signed Amazon S3 URL in response for uploading the file directly
        to S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant/client/start_attachment_upload.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/#start_attachment_upload)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connectparticipant.html#ConnectParticipant.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectparticipant/client/)
        """
