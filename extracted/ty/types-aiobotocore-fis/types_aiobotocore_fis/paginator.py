"""
Type annotations for fis service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_fis.client import FISClient
    from types_aiobotocore_fis.paginator import (
        ListActionsPaginator,
        ListExperimentResolvedTargetsPaginator,
        ListExperimentTemplatesPaginator,
        ListExperimentsPaginator,
        ListTargetAccountConfigurationsPaginator,
        ListTargetResourceTypesPaginator,
    )

    session = get_session()
    with session.create_client("fis") as client:
        client: FISClient

        list_actions_paginator: ListActionsPaginator = client.get_paginator("list_actions")
        list_experiment_resolved_targets_paginator: ListExperimentResolvedTargetsPaginator = client.get_paginator("list_experiment_resolved_targets")
        list_experiment_templates_paginator: ListExperimentTemplatesPaginator = client.get_paginator("list_experiment_templates")
        list_experiments_paginator: ListExperimentsPaginator = client.get_paginator("list_experiments")
        list_target_account_configurations_paginator: ListTargetAccountConfigurationsPaginator = client.get_paginator("list_target_account_configurations")
        list_target_resource_types_paginator: ListTargetResourceTypesPaginator = client.get_paginator("list_target_resource_types")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListActionsRequestPaginateTypeDef,
    ListActionsResponseTypeDef,
    ListExperimentResolvedTargetsRequestPaginateTypeDef,
    ListExperimentResolvedTargetsResponseTypeDef,
    ListExperimentsRequestPaginateTypeDef,
    ListExperimentsResponseTypeDef,
    ListExperimentTemplatesRequestPaginateTypeDef,
    ListExperimentTemplatesResponseTypeDef,
    ListTargetAccountConfigurationsRequestPaginateTypeDef,
    ListTargetAccountConfigurationsResponseTypeDef,
    ListTargetResourceTypesRequestPaginateTypeDef,
    ListTargetResourceTypesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListActionsPaginator",
    "ListExperimentResolvedTargetsPaginator",
    "ListExperimentTemplatesPaginator",
    "ListExperimentsPaginator",
    "ListTargetAccountConfigurationsPaginator",
    "ListTargetResourceTypesPaginator",
)


if TYPE_CHECKING:
    _ListActionsPaginatorBase = AioPaginator[ListActionsResponseTypeDef]
else:
    _ListActionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListActionsPaginator(_ListActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis/paginator/ListActions.html#FIS.Paginator.ListActions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/paginators/#listactionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListActionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis/paginator/ListActions.html#FIS.Paginator.ListActions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/paginators/#listactionspaginator)
        """


if TYPE_CHECKING:
    _ListExperimentResolvedTargetsPaginatorBase = AioPaginator[
        ListExperimentResolvedTargetsResponseTypeDef
    ]
else:
    _ListExperimentResolvedTargetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListExperimentResolvedTargetsPaginator(_ListExperimentResolvedTargetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis/paginator/ListExperimentResolvedTargets.html#FIS.Paginator.ListExperimentResolvedTargets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/paginators/#listexperimentresolvedtargetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExperimentResolvedTargetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListExperimentResolvedTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis/paginator/ListExperimentResolvedTargets.html#FIS.Paginator.ListExperimentResolvedTargets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/paginators/#listexperimentresolvedtargetspaginator)
        """


if TYPE_CHECKING:
    _ListExperimentTemplatesPaginatorBase = AioPaginator[ListExperimentTemplatesResponseTypeDef]
else:
    _ListExperimentTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListExperimentTemplatesPaginator(_ListExperimentTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis/paginator/ListExperimentTemplates.html#FIS.Paginator.ListExperimentTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/paginators/#listexperimenttemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExperimentTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListExperimentTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis/paginator/ListExperimentTemplates.html#FIS.Paginator.ListExperimentTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/paginators/#listexperimenttemplatespaginator)
        """


if TYPE_CHECKING:
    _ListExperimentsPaginatorBase = AioPaginator[ListExperimentsResponseTypeDef]
else:
    _ListExperimentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListExperimentsPaginator(_ListExperimentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis/paginator/ListExperiments.html#FIS.Paginator.ListExperiments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/paginators/#listexperimentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExperimentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListExperimentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis/paginator/ListExperiments.html#FIS.Paginator.ListExperiments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/paginators/#listexperimentspaginator)
        """


if TYPE_CHECKING:
    _ListTargetAccountConfigurationsPaginatorBase = AioPaginator[
        ListTargetAccountConfigurationsResponseTypeDef
    ]
else:
    _ListTargetAccountConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTargetAccountConfigurationsPaginator(_ListTargetAccountConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis/paginator/ListTargetAccountConfigurations.html#FIS.Paginator.ListTargetAccountConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/paginators/#listtargetaccountconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTargetAccountConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTargetAccountConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis/paginator/ListTargetAccountConfigurations.html#FIS.Paginator.ListTargetAccountConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/paginators/#listtargetaccountconfigurationspaginator)
        """


if TYPE_CHECKING:
    _ListTargetResourceTypesPaginatorBase = AioPaginator[ListTargetResourceTypesResponseTypeDef]
else:
    _ListTargetResourceTypesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTargetResourceTypesPaginator(_ListTargetResourceTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis/paginator/ListTargetResourceTypes.html#FIS.Paginator.ListTargetResourceTypes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/paginators/#listtargetresourcetypespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTargetResourceTypesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTargetResourceTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fis/paginator/ListTargetResourceTypes.html#FIS.Paginator.ListTargetResourceTypes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fis/paginators/#listtargetresourcetypespaginator)
        """
