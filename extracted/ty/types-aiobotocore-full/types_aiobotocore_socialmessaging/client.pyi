"""
Type annotations for socialmessaging service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/)

Copyright 2026 Vlad Emelianov

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
from collections.abc import Mapping
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListLinkedWhatsAppBusinessAccountsPaginator,
    ListWhatsAppFlowAssetsPaginator,
    ListWhatsAppFlowsPaginator,
    ListWhatsAppMessageTemplatesPaginator,
    ListWhatsAppTemplateLibraryPaginator,
)
from .type_defs import (
    AssociateWhatsAppBusinessAccountInputTypeDef,
    AssociateWhatsAppBusinessAccountOutputTypeDef,
    CreateWhatsAppFlowInputTypeDef,
    CreateWhatsAppFlowOutputTypeDef,
    CreateWhatsAppMessageTemplateFromLibraryInputTypeDef,
    CreateWhatsAppMessageTemplateFromLibraryOutputTypeDef,
    CreateWhatsAppMessageTemplateInputTypeDef,
    CreateWhatsAppMessageTemplateMediaInputTypeDef,
    CreateWhatsAppMessageTemplateMediaOutputTypeDef,
    CreateWhatsAppMessageTemplateOutputTypeDef,
    DeleteWhatsAppFlowInputTypeDef,
    DeleteWhatsAppMessageMediaInputTypeDef,
    DeleteWhatsAppMessageMediaOutputTypeDef,
    DeleteWhatsAppMessageTemplateInputTypeDef,
    DeprecateWhatsAppFlowInputTypeDef,
    DisassociateWhatsAppBusinessAccountInputTypeDef,
    GetLinkedWhatsAppBusinessAccountInputTypeDef,
    GetLinkedWhatsAppBusinessAccountOutputTypeDef,
    GetLinkedWhatsAppBusinessAccountPhoneNumberInputTypeDef,
    GetLinkedWhatsAppBusinessAccountPhoneNumberOutputTypeDef,
    GetWhatsAppFlowInputTypeDef,
    GetWhatsAppFlowOutputTypeDef,
    GetWhatsAppFlowPreviewInputTypeDef,
    GetWhatsAppFlowPreviewOutputTypeDef,
    GetWhatsAppMessageMediaInputTypeDef,
    GetWhatsAppMessageMediaOutputTypeDef,
    GetWhatsAppMessageTemplateInputTypeDef,
    GetWhatsAppMessageTemplateOutputTypeDef,
    ListLinkedWhatsAppBusinessAccountsInputTypeDef,
    ListLinkedWhatsAppBusinessAccountsOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListWhatsAppFlowAssetsInputTypeDef,
    ListWhatsAppFlowAssetsOutputTypeDef,
    ListWhatsAppFlowsInputTypeDef,
    ListWhatsAppFlowsOutputTypeDef,
    ListWhatsAppMessageTemplatesInputTypeDef,
    ListWhatsAppMessageTemplatesOutputTypeDef,
    ListWhatsAppTemplateLibraryInputTypeDef,
    ListWhatsAppTemplateLibraryOutputTypeDef,
    PostWhatsAppMessageMediaInputTypeDef,
    PostWhatsAppMessageMediaOutputTypeDef,
    PublishWhatsAppFlowInputTypeDef,
    PutWhatsAppBusinessAccountEventDestinationsInputTypeDef,
    SendWhatsAppMessageInputTypeDef,
    SendWhatsAppMessageOutputTypeDef,
    TagResourceInputTypeDef,
    TagResourceOutputTypeDef,
    UntagResourceInputTypeDef,
    UntagResourceOutputTypeDef,
    UpdateWhatsAppFlowAssetsInputTypeDef,
    UpdateWhatsAppFlowAssetsOutputTypeDef,
    UpdateWhatsAppFlowInputTypeDef,
    UpdateWhatsAppMessageTemplateInputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("EndUserMessagingSocialClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedByMetaException: type[BotocoreClientError]
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    DependencyException: type[BotocoreClientError]
    InternalServiceException: type[BotocoreClientError]
    InvalidParametersException: type[BotocoreClientError]
    LimitExceededException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ThrottledRequestException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

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

    async def create_whatsapp_flow(
        self, **kwargs: Unpack[CreateWhatsAppFlowInputTypeDef]
    ) -> CreateWhatsAppFlowOutputTypeDef:
        """
        Creates a new WhatsApp Flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/create_whatsapp_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#create_whatsapp_flow)
        """

    async def create_whatsapp_message_template(
        self, **kwargs: Unpack[CreateWhatsAppMessageTemplateInputTypeDef]
    ) -> CreateWhatsAppMessageTemplateOutputTypeDef:
        """
        Creates a new WhatsApp message template from a custom definition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/create_whatsapp_message_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#create_whatsapp_message_template)
        """

    async def create_whatsapp_message_template_from_library(
        self, **kwargs: Unpack[CreateWhatsAppMessageTemplateFromLibraryInputTypeDef]
    ) -> CreateWhatsAppMessageTemplateFromLibraryOutputTypeDef:
        """
        Creates a new WhatsApp message template using a template from Meta's template
        library.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/create_whatsapp_message_template_from_library.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#create_whatsapp_message_template_from_library)
        """

    async def create_whatsapp_message_template_media(
        self, **kwargs: Unpack[CreateWhatsAppMessageTemplateMediaInputTypeDef]
    ) -> CreateWhatsAppMessageTemplateMediaOutputTypeDef:
        """
        Uploads media for use in a WhatsApp message template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/create_whatsapp_message_template_media.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#create_whatsapp_message_template_media)
        """

    async def delete_whatsapp_flow(
        self, **kwargs: Unpack[DeleteWhatsAppFlowInputTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes a WhatsApp Flow permanently.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/delete_whatsapp_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#delete_whatsapp_flow)
        """

    async def delete_whatsapp_message_media(
        self, **kwargs: Unpack[DeleteWhatsAppMessageMediaInputTypeDef]
    ) -> DeleteWhatsAppMessageMediaOutputTypeDef:
        """
        Delete a media object from the WhatsApp service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/delete_whatsapp_message_media.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#delete_whatsapp_message_media)
        """

    async def delete_whatsapp_message_template(
        self, **kwargs: Unpack[DeleteWhatsAppMessageTemplateInputTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes a WhatsApp message template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/delete_whatsapp_message_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#delete_whatsapp_message_template)
        """

    async def deprecate_whatsapp_flow(
        self, **kwargs: Unpack[DeprecateWhatsAppFlowInputTypeDef]
    ) -> dict[str, Any]:
        """
        Deprecates a published WhatsApp Flow, marking it as no longer recommended for
        use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/deprecate_whatsapp_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#deprecate_whatsapp_flow)
        """

    async def disassociate_whatsapp_business_account(
        self, **kwargs: Unpack[DisassociateWhatsAppBusinessAccountInputTypeDef]
    ) -> dict[str, Any]:
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
        Retrieve the WABA account id and phone number details of a WhatsApp business
        account phone number.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/get_linked_whatsapp_business_account_phone_number.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#get_linked_whatsapp_business_account_phone_number)
        """

    async def get_whatsapp_flow(
        self, **kwargs: Unpack[GetWhatsAppFlowInputTypeDef]
    ) -> GetWhatsAppFlowOutputTypeDef:
        """
        Retrieves the metadata and status of a WhatsApp Flow, including validation
        errors, preview information, and health status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/get_whatsapp_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#get_whatsapp_flow)
        """

    async def get_whatsapp_flow_preview(
        self, **kwargs: Unpack[GetWhatsAppFlowPreviewInputTypeDef]
    ) -> GetWhatsAppFlowPreviewOutputTypeDef:
        """
        Generates a web preview URL for testing a WhatsApp Flow before publishing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/get_whatsapp_flow_preview.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#get_whatsapp_flow_preview)
        """

    async def get_whatsapp_message_media(
        self, **kwargs: Unpack[GetWhatsAppMessageMediaInputTypeDef]
    ) -> GetWhatsAppMessageMediaOutputTypeDef:
        """
        Get a media file from the WhatsApp service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/get_whatsapp_message_media.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#get_whatsapp_message_media)
        """

    async def get_whatsapp_message_template(
        self, **kwargs: Unpack[GetWhatsAppMessageTemplateInputTypeDef]
    ) -> GetWhatsAppMessageTemplateOutputTypeDef:
        """
        Retrieves a specific WhatsApp message template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/get_whatsapp_message_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#get_whatsapp_message_template)
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

    async def list_whatsapp_flow_assets(
        self, **kwargs: Unpack[ListWhatsAppFlowAssetsInputTypeDef]
    ) -> ListWhatsAppFlowAssetsOutputTypeDef:
        """
        Lists the assets (Flow JSON definition) of a WhatsApp Flow with presigned
        download URLs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/list_whatsapp_flow_assets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#list_whatsapp_flow_assets)
        """

    async def list_whatsapp_flows(
        self, **kwargs: Unpack[ListWhatsAppFlowsInputTypeDef]
    ) -> ListWhatsAppFlowsOutputTypeDef:
        """
        Lists all WhatsApp Flows for a WhatsApp Business Account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/list_whatsapp_flows.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#list_whatsapp_flows)
        """

    async def list_whatsapp_message_templates(
        self, **kwargs: Unpack[ListWhatsAppMessageTemplatesInputTypeDef]
    ) -> ListWhatsAppMessageTemplatesOutputTypeDef:
        """
        Lists WhatsApp message templates for a specific WhatsApp Business Account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/list_whatsapp_message_templates.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#list_whatsapp_message_templates)
        """

    async def list_whatsapp_template_library(
        self, **kwargs: Unpack[ListWhatsAppTemplateLibraryInputTypeDef]
    ) -> ListWhatsAppTemplateLibraryOutputTypeDef:
        """
        Lists templates available in Meta's template library for WhatsApp messaging.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/list_whatsapp_template_library.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#list_whatsapp_template_library)
        """

    async def post_whatsapp_message_media(
        self, **kwargs: Unpack[PostWhatsAppMessageMediaInputTypeDef]
    ) -> PostWhatsAppMessageMediaOutputTypeDef:
        """
        Upload a media file to the WhatsApp service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/post_whatsapp_message_media.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#post_whatsapp_message_media)
        """

    async def publish_whatsapp_flow(
        self, **kwargs: Unpack[PublishWhatsAppFlowInputTypeDef]
    ) -> dict[str, Any]:
        """
        Publishes a WhatsApp Flow, making it available for use in template messages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/publish_whatsapp_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#publish_whatsapp_flow)
        """

    async def put_whatsapp_business_account_event_destinations(
        self, **kwargs: Unpack[PutWhatsAppBusinessAccountEventDestinationsInputTypeDef]
    ) -> dict[str, Any]:
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

    async def update_whatsapp_flow(
        self, **kwargs: Unpack[UpdateWhatsAppFlowInputTypeDef]
    ) -> dict[str, Any]:
        """
        Updates the metadata of a WhatsApp Flow, such as its name or categories.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/update_whatsapp_flow.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#update_whatsapp_flow)
        """

    async def update_whatsapp_flow_assets(
        self, **kwargs: Unpack[UpdateWhatsAppFlowAssetsInputTypeDef]
    ) -> UpdateWhatsAppFlowAssetsOutputTypeDef:
        """
        Updates the Flow JSON definition (assets) of a WhatsApp Flow.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/update_whatsapp_flow_assets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#update_whatsapp_flow_assets)
        """

    async def update_whatsapp_message_template(
        self, **kwargs: Unpack[UpdateWhatsAppMessageTemplateInputTypeDef]
    ) -> dict[str, Any]:
        """
        Updates an existing WhatsApp message template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/update_whatsapp_message_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#update_whatsapp_message_template)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_linked_whatsapp_business_accounts"]
    ) -> ListLinkedWhatsAppBusinessAccountsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_whatsapp_flow_assets"]
    ) -> ListWhatsAppFlowAssetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_whatsapp_flows"]
    ) -> ListWhatsAppFlowsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_whatsapp_message_templates"]
    ) -> ListWhatsAppMessageTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_whatsapp_template_library"]
    ) -> ListWhatsAppTemplateLibraryPaginator:
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
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging.html#EndUserMessagingSocial.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/client/)
        """
