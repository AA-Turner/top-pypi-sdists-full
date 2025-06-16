"""
Type annotations for taxsettings service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_taxsettings.client import TaxSettingsClient
    from types_aiobotocore_taxsettings.paginator import (
        ListSupplementalTaxRegistrationsPaginator,
        ListTaxExemptionsPaginator,
        ListTaxRegistrationsPaginator,
    )

    session = get_session()
    with session.create_client("taxsettings") as client:
        client: TaxSettingsClient

        list_supplemental_tax_registrations_paginator: ListSupplementalTaxRegistrationsPaginator = client.get_paginator("list_supplemental_tax_registrations")
        list_tax_exemptions_paginator: ListTaxExemptionsPaginator = client.get_paginator("list_tax_exemptions")
        list_tax_registrations_paginator: ListTaxRegistrationsPaginator = client.get_paginator("list_tax_registrations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListSupplementalTaxRegistrationsRequestPaginateTypeDef,
    ListSupplementalTaxRegistrationsResponseTypeDef,
    ListTaxExemptionsRequestPaginateTypeDef,
    ListTaxExemptionsResponseTypeDef,
    ListTaxRegistrationsRequestPaginateTypeDef,
    ListTaxRegistrationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListSupplementalTaxRegistrationsPaginator",
    "ListTaxExemptionsPaginator",
    "ListTaxRegistrationsPaginator",
)

if TYPE_CHECKING:
    _ListSupplementalTaxRegistrationsPaginatorBase = AioPaginator[
        ListSupplementalTaxRegistrationsResponseTypeDef
    ]
else:
    _ListSupplementalTaxRegistrationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSupplementalTaxRegistrationsPaginator(_ListSupplementalTaxRegistrationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/paginator/ListSupplementalTaxRegistrations.html#TaxSettings.Paginator.ListSupplementalTaxRegistrations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/paginators/#listsupplementaltaxregistrationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSupplementalTaxRegistrationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSupplementalTaxRegistrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/paginator/ListSupplementalTaxRegistrations.html#TaxSettings.Paginator.ListSupplementalTaxRegistrations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/paginators/#listsupplementaltaxregistrationspaginator)
        """

if TYPE_CHECKING:
    _ListTaxExemptionsPaginatorBase = AioPaginator[ListTaxExemptionsResponseTypeDef]
else:
    _ListTaxExemptionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTaxExemptionsPaginator(_ListTaxExemptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/paginator/ListTaxExemptions.html#TaxSettings.Paginator.ListTaxExemptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/paginators/#listtaxexemptionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTaxExemptionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTaxExemptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/paginator/ListTaxExemptions.html#TaxSettings.Paginator.ListTaxExemptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/paginators/#listtaxexemptionspaginator)
        """

if TYPE_CHECKING:
    _ListTaxRegistrationsPaginatorBase = AioPaginator[ListTaxRegistrationsResponseTypeDef]
else:
    _ListTaxRegistrationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTaxRegistrationsPaginator(_ListTaxRegistrationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/paginator/ListTaxRegistrations.html#TaxSettings.Paginator.ListTaxRegistrations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/paginators/#listtaxregistrationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTaxRegistrationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTaxRegistrationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/taxsettings/paginator/ListTaxRegistrations.html#TaxSettings.Paginator.ListTaxRegistrations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_taxsettings/paginators/#listtaxregistrationspaginator)
        """
