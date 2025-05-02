"""
Type annotations for events service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_events/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_events.client import EventBridgeClient
    from types_aiobotocore_events.paginator import (
        ListRuleNamesByTargetPaginator,
        ListRulesPaginator,
        ListTargetsByRulePaginator,
    )

    session = get_session()
    with session.create_client("events") as client:
        client: EventBridgeClient

        list_rule_names_by_target_paginator: ListRuleNamesByTargetPaginator = client.get_paginator("list_rule_names_by_target")
        list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
        list_targets_by_rule_paginator: ListTargetsByRulePaginator = client.get_paginator("list_targets_by_rule")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListRuleNamesByTargetRequestPaginateTypeDef,
    ListRuleNamesByTargetResponseTypeDef,
    ListRulesRequestPaginateTypeDef,
    ListRulesResponseTypeDef,
    ListTargetsByRuleRequestPaginateTypeDef,
    ListTargetsByRuleResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListRuleNamesByTargetPaginator", "ListRulesPaginator", "ListTargetsByRulePaginator")


if TYPE_CHECKING:
    _ListRuleNamesByTargetPaginatorBase = AioPaginator[ListRuleNamesByTargetResponseTypeDef]
else:
    _ListRuleNamesByTargetPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRuleNamesByTargetPaginator(_ListRuleNamesByTargetPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/paginator/ListRuleNamesByTarget.html#EventBridge.Paginator.ListRuleNamesByTarget)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_events/paginators/#listrulenamesbytargetpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRuleNamesByTargetRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRuleNamesByTargetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/paginator/ListRuleNamesByTarget.html#EventBridge.Paginator.ListRuleNamesByTarget.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_events/paginators/#listrulenamesbytargetpaginator)
        """


if TYPE_CHECKING:
    _ListRulesPaginatorBase = AioPaginator[ListRulesResponseTypeDef]
else:
    _ListRulesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRulesPaginator(_ListRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/paginator/ListRules.html#EventBridge.Paginator.ListRules)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_events/paginators/#listrulespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRulesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/paginator/ListRules.html#EventBridge.Paginator.ListRules.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_events/paginators/#listrulespaginator)
        """


if TYPE_CHECKING:
    _ListTargetsByRulePaginatorBase = AioPaginator[ListTargetsByRuleResponseTypeDef]
else:
    _ListTargetsByRulePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTargetsByRulePaginator(_ListTargetsByRulePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/paginator/ListTargetsByRule.html#EventBridge.Paginator.ListTargetsByRule)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_events/paginators/#listtargetsbyrulepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTargetsByRuleRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTargetsByRuleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/events/paginator/ListTargetsByRule.html#EventBridge.Paginator.ListTargetsByRule.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_events/paginators/#listtargetsbyrulepaginator)
        """
