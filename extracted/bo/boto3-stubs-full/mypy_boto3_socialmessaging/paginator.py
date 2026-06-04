"""
Type annotations for socialmessaging service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_socialmessaging.client import EndUserMessagingSocialClient
    from mypy_boto3_socialmessaging.paginator import (
        ListLinkedWhatsAppBusinessAccountsPaginator,
        ListWhatsAppFlowAssetsPaginator,
        ListWhatsAppFlowsPaginator,
        ListWhatsAppMessageTemplatesPaginator,
        ListWhatsAppTemplateLibraryPaginator,
    )

    session = Session()
    client: EndUserMessagingSocialClient = session.client("socialmessaging")

    list_linked_whatsapp_business_accounts_paginator: ListLinkedWhatsAppBusinessAccountsPaginator = client.get_paginator("list_linked_whatsapp_business_accounts")
    list_whatsapp_flow_assets_paginator: ListWhatsAppFlowAssetsPaginator = client.get_paginator("list_whatsapp_flow_assets")
    list_whatsapp_flows_paginator: ListWhatsAppFlowsPaginator = client.get_paginator("list_whatsapp_flows")
    list_whatsapp_message_templates_paginator: ListWhatsAppMessageTemplatesPaginator = client.get_paginator("list_whatsapp_message_templates")
    list_whatsapp_template_library_paginator: ListWhatsAppTemplateLibraryPaginator = client.get_paginator("list_whatsapp_template_library")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListLinkedWhatsAppBusinessAccountsInputPaginateTypeDef,
    ListLinkedWhatsAppBusinessAccountsOutputTypeDef,
    ListWhatsAppFlowAssetsInputPaginateTypeDef,
    ListWhatsAppFlowAssetsOutputTypeDef,
    ListWhatsAppFlowsInputPaginateTypeDef,
    ListWhatsAppFlowsOutputTypeDef,
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
    "ListWhatsAppFlowAssetsPaginator",
    "ListWhatsAppFlowsPaginator",
    "ListWhatsAppMessageTemplatesPaginator",
    "ListWhatsAppTemplateLibraryPaginator",
)


if TYPE_CHECKING:
    _ListLinkedWhatsAppBusinessAccountsPaginatorBase = Paginator[
        ListLinkedWhatsAppBusinessAccountsOutputTypeDef
    ]
else:
    _ListLinkedWhatsAppBusinessAccountsPaginatorBase = Paginator  # type: ignore[assignment]


class ListLinkedWhatsAppBusinessAccountsPaginator(_ListLinkedWhatsAppBusinessAccountsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListLinkedWhatsAppBusinessAccounts.html#EndUserMessagingSocial.Paginator.ListLinkedWhatsAppBusinessAccounts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/paginators/#listlinkedwhatsappbusinessaccountspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLinkedWhatsAppBusinessAccountsInputPaginateTypeDef]
    ) -> PageIterator[ListLinkedWhatsAppBusinessAccountsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListLinkedWhatsAppBusinessAccounts.html#EndUserMessagingSocial.Paginator.ListLinkedWhatsAppBusinessAccounts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/paginators/#listlinkedwhatsappbusinessaccountspaginator)
        """


if TYPE_CHECKING:
    _ListWhatsAppFlowAssetsPaginatorBase = Paginator[ListWhatsAppFlowAssetsOutputTypeDef]
else:
    _ListWhatsAppFlowAssetsPaginatorBase = Paginator  # type: ignore[assignment]


class ListWhatsAppFlowAssetsPaginator(_ListWhatsAppFlowAssetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListWhatsAppFlowAssets.html#EndUserMessagingSocial.Paginator.ListWhatsAppFlowAssets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/paginators/#listwhatsappflowassetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWhatsAppFlowAssetsInputPaginateTypeDef]
    ) -> PageIterator[ListWhatsAppFlowAssetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListWhatsAppFlowAssets.html#EndUserMessagingSocial.Paginator.ListWhatsAppFlowAssets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/paginators/#listwhatsappflowassetspaginator)
        """


if TYPE_CHECKING:
    _ListWhatsAppFlowsPaginatorBase = Paginator[ListWhatsAppFlowsOutputTypeDef]
else:
    _ListWhatsAppFlowsPaginatorBase = Paginator  # type: ignore[assignment]


class ListWhatsAppFlowsPaginator(_ListWhatsAppFlowsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListWhatsAppFlows.html#EndUserMessagingSocial.Paginator.ListWhatsAppFlows)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/paginators/#listwhatsappflowspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWhatsAppFlowsInputPaginateTypeDef]
    ) -> PageIterator[ListWhatsAppFlowsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListWhatsAppFlows.html#EndUserMessagingSocial.Paginator.ListWhatsAppFlows.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/paginators/#listwhatsappflowspaginator)
        """


if TYPE_CHECKING:
    _ListWhatsAppMessageTemplatesPaginatorBase = Paginator[
        ListWhatsAppMessageTemplatesOutputTypeDef
    ]
else:
    _ListWhatsAppMessageTemplatesPaginatorBase = Paginator  # type: ignore[assignment]


class ListWhatsAppMessageTemplatesPaginator(_ListWhatsAppMessageTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListWhatsAppMessageTemplates.html#EndUserMessagingSocial.Paginator.ListWhatsAppMessageTemplates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/paginators/#listwhatsappmessagetemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWhatsAppMessageTemplatesInputPaginateTypeDef]
    ) -> PageIterator[ListWhatsAppMessageTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListWhatsAppMessageTemplates.html#EndUserMessagingSocial.Paginator.ListWhatsAppMessageTemplates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/paginators/#listwhatsappmessagetemplatespaginator)
        """


if TYPE_CHECKING:
    _ListWhatsAppTemplateLibraryPaginatorBase = Paginator[ListWhatsAppTemplateLibraryOutputTypeDef]
else:
    _ListWhatsAppTemplateLibraryPaginatorBase = Paginator  # type: ignore[assignment]


class ListWhatsAppTemplateLibraryPaginator(_ListWhatsAppTemplateLibraryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListWhatsAppTemplateLibrary.html#EndUserMessagingSocial.Paginator.ListWhatsAppTemplateLibrary)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/paginators/#listwhatsapptemplatelibrarypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWhatsAppTemplateLibraryInputPaginateTypeDef]
    ) -> PageIterator[ListWhatsAppTemplateLibraryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/socialmessaging/paginator/ListWhatsAppTemplateLibrary.html#EndUserMessagingSocial.Paginator.ListWhatsAppTemplateLibrary.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_socialmessaging/paginators/#listwhatsapptemplatelibrarypaginator)
        """
