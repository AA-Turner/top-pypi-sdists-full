"""
Type annotations for socialmessaging service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_socialmessaging.client import EndUserMessagingSocialClient
    from types_aiobotocore_socialmessaging.paginator import (
        ListLinkedWhatsAppBusinessAccountsPaginator,
        ListWhatsAppMessageTemplatesPaginator,
        ListWhatsAppTemplateLibraryPaginator,
    )

    session = get_session()
    with session.create_client("socialmessaging") as client:
        client: EndUserMessagingSocialClient

        list_linked_whatsapp_business_accounts_paginator: ListLinkedWhatsAppBusinessAccountsPaginator = client.get_paginator("list_linked_whatsapp_business_accounts")
        list_whatsapp_message_templates_paginator: ListWhatsAppMessageTemplatesPaginator = client.get_paginator("list_whatsapp_message_templates")
        list_whatsapp_template_library_paginator: ListWhatsAppTemplateLibraryPaginator = client.get_paginator("list_whatsapp_template_library")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListLinkedWhatsAppBusinessAccountsInputPaginateTypeDef,
    ListLinkedWhatsAppBusinessAccountsOutputTypeDef,
    ListWhatsAppMessageTemplatesInputPaginateTypeDef,
    ListWhatsAppMessageTemplatesOutputTypeDef,
    ListWhatsAppTemplateLibraryInputPaginateTypeDef,
    ListWhatsAppTemplateLibraryOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListLinkedWhatsAppBusinessAccountsPaginator",
    "ListWhatsAppMessageTemplatesPaginator",
    "ListWhatsAppTemplateLibraryPaginator",
)


if TYPE_CHECKING:
    _ListLinkedWhatsAppBusinessAccountsPaginatorBase = AioPaginator[
        ListLinkedWhatsAppBusinessAccountsOutputTypeDef
    ]
else:
    _ListLinkedWhatsAppBusinessAccountsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListLinkedWhatsAppBusinessAccountsPaginator(_ListLinkedWhatsAppBusinessAccountsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListLinkedWhatsAppBusinessAccounts.html#EndUserMessagingSocial.Paginator.ListLinkedWhatsAppBusinessAccounts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/paginators/#listlinkedwhatsappbusinessaccountspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLinkedWhatsAppBusinessAccountsInputPaginateTypeDef]
    ) -> AioPageIterator[ListLinkedWhatsAppBusinessAccountsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListLinkedWhatsAppBusinessAccounts.html#EndUserMessagingSocial.Paginator.ListLinkedWhatsAppBusinessAccounts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/paginators/#listlinkedwhatsappbusinessaccountspaginator)
        """


if TYPE_CHECKING:
    _ListWhatsAppMessageTemplatesPaginatorBase = AioPaginator[
        ListWhatsAppMessageTemplatesOutputTypeDef
    ]
else:
    _ListWhatsAppMessageTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWhatsAppMessageTemplatesPaginator(_ListWhatsAppMessageTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListWhatsAppMessageTemplates.html#EndUserMessagingSocial.Paginator.ListWhatsAppMessageTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/paginators/#listwhatsappmessagetemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWhatsAppMessageTemplatesInputPaginateTypeDef]
    ) -> AioPageIterator[ListWhatsAppMessageTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListWhatsAppMessageTemplates.html#EndUserMessagingSocial.Paginator.ListWhatsAppMessageTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/paginators/#listwhatsappmessagetemplatespaginator)
        """


if TYPE_CHECKING:
    _ListWhatsAppTemplateLibraryPaginatorBase = AioPaginator[
        ListWhatsAppTemplateLibraryOutputTypeDef
    ]
else:
    _ListWhatsAppTemplateLibraryPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWhatsAppTemplateLibraryPaginator(_ListWhatsAppTemplateLibraryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListWhatsAppTemplateLibrary.html#EndUserMessagingSocial.Paginator.ListWhatsAppTemplateLibrary)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/paginators/#listwhatsapptemplatelibrarypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWhatsAppTemplateLibraryInputPaginateTypeDef]
    ) -> AioPageIterator[ListWhatsAppTemplateLibraryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListWhatsAppTemplateLibrary.html#EndUserMessagingSocial.Paginator.ListWhatsAppTemplateLibrary.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_socialmessaging/paginators/#listwhatsapptemplatelibrarypaginator)
        """
