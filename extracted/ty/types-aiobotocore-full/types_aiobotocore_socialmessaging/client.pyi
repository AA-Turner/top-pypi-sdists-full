"""
Type annotations for socialmessaging service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_socialmessaging.client import EndUserMessagingSocialClient

    session = get_session()
    async with session.create_client("socialmessaging") as client:
        client: EndUserMessagingSocialClient
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

from .paginator import ListLinkedWhatsAppBusinessAccountsPaginator
from .type_defs import (
    AssociateWhatsAppBusinessAccountInputTypeDef,
    AssociateWhatsAppBusinessAccountOutputTypeDef,
    DeleteWhatsAppMessageMediaInputTypeDef,
    DeleteWhatsAppMessageMediaOutputTypeDef,
    DisassociateWhatsAppBusinessAccountInputTypeDef,
    GetLinkedWhatsAppBusinessAccountInputTypeDef,
    GetLinkedWhatsAppBusinessAccountOutputTypeDef,
    GetLinkedWhatsAppBusinessAccountPhoneNumberInputTypeDef,
    GetLinkedWhatsAppBusinessAccountPhoneNumberOutputTypeDef,
    GetWhatsAppMessageMediaInputTypeDef,
    GetWhatsAppMessageMediaOutputTypeDef,
    ListLinkedWhatsAppBusinessAccountsInputTypeDef,
    ListLinkedWhatsAppBusinessAccountsOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    PostWhatsAppMessageMediaInputTypeDef,
    PostWhatsAppMessageMediaOutputTypeDef,
    PutWhatsAppBusinessAccountEventDestinationsInputTypeDef,
    SendWhatsAppMessageInputTypeDef,
    SendWhatsAppMessageOutputTypeDef,
    TagResourceInputTypeDef,
    TagResourceOutputTypeDef,
    UntagResourceInputTypeDef,
    UntagResourceOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("EndUserMessagingSocialClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedByMetaException: Type[BotocoreClientError]
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DependencyException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidParametersException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottledRequestException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class EndUserMessagingSocialClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging.html#EndUserMessagingSocial.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EndUserMessagingSocialClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging.html#EndUserMessagingSocial.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#generate_presigned_url)
        """

    async def associate_whatsapp_business_account(
        self, **kwargs: Unpack[AssociateWhatsAppBusinessAccountInputTypeDef]
    ) -> AssociateWhatsAppBusinessAccountOutputTypeDef:
        """
        This is only used through the Amazon Web Services console during sign-up to
        associate your WhatsApp Business Account to your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/associate_whatsapp_business_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#associate_whatsapp_business_account)
        """

    async def delete_whatsapp_message_media(
        self, **kwargs: Unpack[DeleteWhatsAppMessageMediaInputTypeDef]
    ) -> DeleteWhatsAppMessageMediaOutputTypeDef:
        """
        Delete a media object from the WhatsApp service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/delete_whatsapp_message_media.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#delete_whatsapp_message_media)
        """

    async def disassociate_whatsapp_business_account(
        self, **kwargs: Unpack[DisassociateWhatsAppBusinessAccountInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociate a WhatsApp Business Account (WABA) from your Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/disassociate_whatsapp_business_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#disassociate_whatsapp_business_account)
        """

    async def get_linked_whatsapp_business_account(
        self, **kwargs: Unpack[GetLinkedWhatsAppBusinessAccountInputTypeDef]
    ) -> GetLinkedWhatsAppBusinessAccountOutputTypeDef:
        """
        Get the details of your linked WhatsApp Business Account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/get_linked_whatsapp_business_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#get_linked_whatsapp_business_account)
        """

    async def get_linked_whatsapp_business_account_phone_number(
        self, **kwargs: Unpack[GetLinkedWhatsAppBusinessAccountPhoneNumberInputTypeDef]
    ) -> GetLinkedWhatsAppBusinessAccountPhoneNumberOutputTypeDef:
        """
        Use your WhatsApp phone number id to get the WABA account id and phone number
        details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/get_linked_whatsapp_business_account_phone_number.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#get_linked_whatsapp_business_account_phone_number)
        """

    async def get_whatsapp_message_media(
        self, **kwargs: Unpack[GetWhatsAppMessageMediaInputTypeDef]
    ) -> GetWhatsAppMessageMediaOutputTypeDef:
        """
        Get a media file from the WhatsApp service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/get_whatsapp_message_media.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#get_whatsapp_message_media)
        """

    async def list_linked_whatsapp_business_accounts(
        self, **kwargs: Unpack[ListLinkedWhatsAppBusinessAccountsInputTypeDef]
    ) -> ListLinkedWhatsAppBusinessAccountsOutputTypeDef:
        """
        List all WhatsApp Business Accounts linked to your Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/list_linked_whatsapp_business_accounts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#list_linked_whatsapp_business_accounts)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        List all tags associated with a resource, such as a phone number or WABA.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#list_tags_for_resource)
        """

    async def post_whatsapp_message_media(
        self, **kwargs: Unpack[PostWhatsAppMessageMediaInputTypeDef]
    ) -> PostWhatsAppMessageMediaOutputTypeDef:
        """
        Upload a media file to the WhatsApp service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/post_whatsapp_message_media.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#post_whatsapp_message_media)
        """

    async def put_whatsapp_business_account_event_destinations(
        self, **kwargs: Unpack[PutWhatsAppBusinessAccountEventDestinationsInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Add an event destination to log event data from WhatsApp for a WhatsApp
        Business Account (WABA).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/put_whatsapp_business_account_event_destinations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#put_whatsapp_business_account_event_destinations)
        """

    async def send_whatsapp_message(
        self, **kwargs: Unpack[SendWhatsAppMessageInputTypeDef]
    ) -> SendWhatsAppMessageOutputTypeDef:
        """
        Send a WhatsApp message.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/send_whatsapp_message.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#send_whatsapp_message)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceInputTypeDef]
    ) -> TagResourceOutputTypeDef:
        """
        Adds or overwrites only the specified tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputTypeDef]
    ) -> UntagResourceOutputTypeDef:
        """
        Removes the specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#untag_resource)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_linked_whatsapp_business_accounts"]
    ) -> ListLinkedWhatsAppBusinessAccountsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging.html#EndUserMessagingSocial.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging.html#EndUserMessagingSocial.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/)
        """
