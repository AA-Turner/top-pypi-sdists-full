"""
Type annotations for apptest service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_apptest.client import MainframeModernizationApplicationTestingClient
    from types_aiobotocore_apptest.paginator import (
        ListTestCasesPaginator,
        ListTestConfigurationsPaginator,
        ListTestRunStepsPaginator,
        ListTestRunTestCasesPaginator,
        ListTestRunsPaginator,
        ListTestSuitesPaginator,
    )

    session = get_session()
    with session.create_client("apptest") as client:
        client: MainframeModernizationApplicationTestingClient

        list_test_cases_paginator: ListTestCasesPaginator = client.get_paginator("list_test_cases")
        list_test_configurations_paginator: ListTestConfigurationsPaginator = client.get_paginator("list_test_configurations")
        list_test_run_steps_paginator: ListTestRunStepsPaginator = client.get_paginator("list_test_run_steps")
        list_test_run_test_cases_paginator: ListTestRunTestCasesPaginator = client.get_paginator("list_test_run_test_cases")
        list_test_runs_paginator: ListTestRunsPaginator = client.get_paginator("list_test_runs")
        list_test_suites_paginator: ListTestSuitesPaginator = client.get_paginator("list_test_suites")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListTestCasesRequestPaginateTypeDef,
    ListTestCasesResponseTypeDef,
    ListTestConfigurationsRequestPaginateTypeDef,
    ListTestConfigurationsResponseTypeDef,
    ListTestRunsRequestPaginateTypeDef,
    ListTestRunsResponseTypeDef,
    ListTestRunStepsRequestPaginateTypeDef,
    ListTestRunStepsResponseTypeDef,
    ListTestRunTestCasesRequestPaginateTypeDef,
    ListTestRunTestCasesResponseTypeDef,
    ListTestSuitesRequestPaginateTypeDef,
    ListTestSuitesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListTestCasesPaginator",
    "ListTestConfigurationsPaginator",
    "ListTestRunStepsPaginator",
    "ListTestRunTestCasesPaginator",
    "ListTestRunsPaginator",
    "ListTestSuitesPaginator",
)

if TYPE_CHECKING:
    _ListTestCasesPaginatorBase = AioPaginator[ListTestCasesResponseTypeDef]
else:
    _ListTestCasesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTestCasesPaginator(_ListTestCasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestCases.html#MainframeModernizationApplicationTesting.Paginator.ListTestCases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestcasespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTestCasesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTestCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestCases.html#MainframeModernizationApplicationTesting.Paginator.ListTestCases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestcasespaginator)
        """

if TYPE_CHECKING:
    _ListTestConfigurationsPaginatorBase = AioPaginator[ListTestConfigurationsResponseTypeDef]
else:
    _ListTestConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTestConfigurationsPaginator(_ListTestConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestConfigurations.html#MainframeModernizationApplicationTesting.Paginator.ListTestConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTestConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTestConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestConfigurations.html#MainframeModernizationApplicationTesting.Paginator.ListTestConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestconfigurationspaginator)
        """

if TYPE_CHECKING:
    _ListTestRunStepsPaginatorBase = AioPaginator[ListTestRunStepsResponseTypeDef]
else:
    _ListTestRunStepsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTestRunStepsPaginator(_ListTestRunStepsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestRunSteps.html#MainframeModernizationApplicationTesting.Paginator.ListTestRunSteps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestrunstepspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTestRunStepsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTestRunStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestRunSteps.html#MainframeModernizationApplicationTesting.Paginator.ListTestRunSteps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestrunstepspaginator)
        """

if TYPE_CHECKING:
    _ListTestRunTestCasesPaginatorBase = AioPaginator[ListTestRunTestCasesResponseTypeDef]
else:
    _ListTestRunTestCasesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTestRunTestCasesPaginator(_ListTestRunTestCasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestRunTestCases.html#MainframeModernizationApplicationTesting.Paginator.ListTestRunTestCases)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestruntestcasespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTestRunTestCasesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTestRunTestCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestRunTestCases.html#MainframeModernizationApplicationTesting.Paginator.ListTestRunTestCases.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestruntestcasespaginator)
        """

if TYPE_CHECKING:
    _ListTestRunsPaginatorBase = AioPaginator[ListTestRunsResponseTypeDef]
else:
    _ListTestRunsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTestRunsPaginator(_ListTestRunsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestRuns.html#MainframeModernizationApplicationTesting.Paginator.ListTestRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestrunspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTestRunsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTestRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestRuns.html#MainframeModernizationApplicationTesting.Paginator.ListTestRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestrunspaginator)
        """

if TYPE_CHECKING:
    _ListTestSuitesPaginatorBase = AioPaginator[ListTestSuitesResponseTypeDef]
else:
    _ListTestSuitesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTestSuitesPaginator(_ListTestSuitesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestSuites.html#MainframeModernizationApplicationTesting.Paginator.ListTestSuites)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestsuitespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTestSuitesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTestSuitesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/apptest/paginator/ListTestSuites.html#MainframeModernizationApplicationTesting.Paginator.ListTestSuites.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apptest/paginators/#listtestsuitespaginator)
        """
