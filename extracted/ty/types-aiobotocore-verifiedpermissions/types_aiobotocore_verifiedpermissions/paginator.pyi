"""
Type annotations for verifiedpermissions service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_verifiedpermissions.client import VerifiedPermissionsClient
    from types_aiobotocore_verifiedpermissions.paginator import (
        ListIdentitySourcesPaginator,
        ListPoliciesPaginator,
        ListPolicyStoresPaginator,
        ListPolicyTemplatesPaginator,
    )

    session = get_session()
    with session.create_client("verifiedpermissions") as client:
        client: VerifiedPermissionsClient

        list_identity_sources_paginator: ListIdentitySourcesPaginator = client.get_paginator("list_identity_sources")
        list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
        list_policy_stores_paginator: ListPolicyStoresPaginator = client.get_paginator("list_policy_stores")
        list_policy_templates_paginator: ListPolicyTemplatesPaginator = client.get_paginator("list_policy_templates")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListIdentitySourcesInputPaginateTypeDef,
    ListIdentitySourcesOutputTypeDef,
    ListPoliciesInputPaginateTypeDef,
    ListPoliciesOutputTypeDef,
    ListPolicyStoresInputPaginateTypeDef,
    ListPolicyStoresOutputTypeDef,
    ListPolicyTemplatesInputPaginateTypeDef,
    ListPolicyTemplatesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListIdentitySourcesPaginator",
    "ListPoliciesPaginator",
    "ListPolicyStoresPaginator",
    "ListPolicyTemplatesPaginator",
)

if TYPE_CHECKING:
    _ListIdentitySourcesPaginatorBase = AioPaginator[ListIdentitySourcesOutputTypeDef]
else:
    _ListIdentitySourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListIdentitySourcesPaginator(_ListIdentitySourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/paginator/ListIdentitySources.html#VerifiedPermissions.Paginator.ListIdentitySources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/paginators/#listidentitysourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIdentitySourcesInputPaginateTypeDef]
    ) -> AioPageIterator[ListIdentitySourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/paginator/ListIdentitySources.html#VerifiedPermissions.Paginator.ListIdentitySources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/paginators/#listidentitysourcespaginator)
        """

if TYPE_CHECKING:
    _ListPoliciesPaginatorBase = AioPaginator[ListPoliciesOutputTypeDef]
else:
    _ListPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPoliciesPaginator(_ListPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/paginator/ListPolicies.html#VerifiedPermissions.Paginator.ListPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/paginators/#listpoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPoliciesInputPaginateTypeDef]
    ) -> AioPageIterator[ListPoliciesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/paginator/ListPolicies.html#VerifiedPermissions.Paginator.ListPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/paginators/#listpoliciespaginator)
        """

if TYPE_CHECKING:
    _ListPolicyStoresPaginatorBase = AioPaginator[ListPolicyStoresOutputTypeDef]
else:
    _ListPolicyStoresPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPolicyStoresPaginator(_ListPolicyStoresPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/paginator/ListPolicyStores.html#VerifiedPermissions.Paginator.ListPolicyStores)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/paginators/#listpolicystorespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPolicyStoresInputPaginateTypeDef]
    ) -> AioPageIterator[ListPolicyStoresOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/paginator/ListPolicyStores.html#VerifiedPermissions.Paginator.ListPolicyStores.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/paginators/#listpolicystorespaginator)
        """

if TYPE_CHECKING:
    _ListPolicyTemplatesPaginatorBase = AioPaginator[ListPolicyTemplatesOutputTypeDef]
else:
    _ListPolicyTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPolicyTemplatesPaginator(_ListPolicyTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/paginator/ListPolicyTemplates.html#VerifiedPermissions.Paginator.ListPolicyTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/paginators/#listpolicytemplatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPolicyTemplatesInputPaginateTypeDef]
    ) -> AioPageIterator[ListPolicyTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions/paginator/ListPolicyTemplates.html#VerifiedPermissions.Paginator.ListPolicyTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/paginators/#listpolicytemplatespaginator)
        """
