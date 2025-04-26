"""
Type annotations for ses service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ses/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ses.client import SESClient
    from types_aiobotocore_ses.paginator import (
        ListConfigurationSetsPaginator,
        ListCustomVerificationEmailTemplatesPaginator,
        ListIdentitiesPaginator,
        ListReceiptRuleSetsPaginator,
        ListTemplatesPaginator,
    )

    session = get_session()
    with session.create_client("ses") as client:
        client: SESClient

        list_configuration_sets_paginator: ListConfigurationSetsPaginator = client.get_paginator("list_configuration_sets")
        list_custom_verification_email_templates_paginator: ListCustomVerificationEmailTemplatesPaginator = client.get_paginator("list_custom_verification_email_templates")
        list_identities_paginator: ListIdentitiesPaginator = client.get_paginator("list_identities")
        list_receipt_rule_sets_paginator: ListReceiptRuleSetsPaginator = client.get_paginator("list_receipt_rule_sets")
        list_templates_paginator: ListTemplatesPaginator = client.get_paginator("list_templates")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListConfigurationSetsRequestPaginateTypeDef,
    ListConfigurationSetsResponseTypeDef,
    ListCustomVerificationEmailTemplatesRequestPaginateTypeDef,
    ListCustomVerificationEmailTemplatesResponseTypeDef,
    ListIdentitiesRequestPaginateTypeDef,
    ListIdentitiesResponseTypeDef,
    ListReceiptRuleSetsRequestPaginateTypeDef,
    ListReceiptRuleSetsResponseTypeDef,
    ListTemplatesRequestPaginateTypeDef,
    ListTemplatesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListConfigurationSetsPaginator",
    "ListCustomVerificationEmailTemplatesPaginator",
    "ListIdentitiesPaginator",
    "ListReceiptRuleSetsPaginator",
    "ListTemplatesPaginator",
)


if TYPE_CHECKING:
    _ListConfigurationSetsPaginatorBase = AioPaginator[ListConfigurationSetsResponseTypeDef]
else:
    _ListConfigurationSetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListConfigurationSetsPaginator(_ListConfigurationSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/paginator/ListConfigurationSets.html#SES.Paginator.ListConfigurationSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ses/paginators/#listconfigurationsetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConfigurationSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConfigurationSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/paginator/ListConfigurationSets.html#SES.Paginator.ListConfigurationSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ses/paginators/#listconfigurationsetspaginator)
        """


if TYPE_CHECKING:
    _ListCustomVerificationEmailTemplatesPaginatorBase = AioPaginator[
        ListCustomVerificationEmailTemplatesResponseTypeDef
    ]
else:
    _ListCustomVerificationEmailTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCustomVerificationEmailTemplatesPaginator(
    _ListCustomVerificationEmailTemplatesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/paginator/ListCustomVerificationEmailTemplates.html#SES.Paginator.ListCustomVerificationEmailTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ses/paginators/#listcustomverificationemailtemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomVerificationEmailTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCustomVerificationEmailTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/paginator/ListCustomVerificationEmailTemplates.html#SES.Paginator.ListCustomVerificationEmailTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ses/paginators/#listcustomverificationemailtemplatespaginator)
        """


if TYPE_CHECKING:
    _ListIdentitiesPaginatorBase = AioPaginator[ListIdentitiesResponseTypeDef]
else:
    _ListIdentitiesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListIdentitiesPaginator(_ListIdentitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/paginator/ListIdentities.html#SES.Paginator.ListIdentities)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ses/paginators/#listidentitiespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIdentitiesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListIdentitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/paginator/ListIdentities.html#SES.Paginator.ListIdentities.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ses/paginators/#listidentitiespaginator)
        """


if TYPE_CHECKING:
    _ListReceiptRuleSetsPaginatorBase = AioPaginator[ListReceiptRuleSetsResponseTypeDef]
else:
    _ListReceiptRuleSetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListReceiptRuleSetsPaginator(_ListReceiptRuleSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/paginator/ListReceiptRuleSets.html#SES.Paginator.ListReceiptRuleSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ses/paginators/#listreceiptrulesetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListReceiptRuleSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListReceiptRuleSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/paginator/ListReceiptRuleSets.html#SES.Paginator.ListReceiptRuleSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ses/paginators/#listreceiptrulesetspaginator)
        """


if TYPE_CHECKING:
    _ListTemplatesPaginatorBase = AioPaginator[ListTemplatesResponseTypeDef]
else:
    _ListTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTemplatesPaginator(_ListTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/paginator/ListTemplates.html#SES.Paginator.ListTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ses/paginators/#listtemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses/paginator/ListTemplates.html#SES.Paginator.ListTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ses/paginators/#listtemplatespaginator)
        """
