"""
Type annotations for waf service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_waf.client import WAFClient
    from types_aiobotocore_waf.paginator import (
        GetRateBasedRuleManagedKeysPaginator,
        ListActivatedRulesInRuleGroupPaginator,
        ListByteMatchSetsPaginator,
        ListGeoMatchSetsPaginator,
        ListIPSetsPaginator,
        ListLoggingConfigurationsPaginator,
        ListRateBasedRulesPaginator,
        ListRegexMatchSetsPaginator,
        ListRegexPatternSetsPaginator,
        ListRuleGroupsPaginator,
        ListRulesPaginator,
        ListSizeConstraintSetsPaginator,
        ListSqlInjectionMatchSetsPaginator,
        ListSubscribedRuleGroupsPaginator,
        ListWebACLsPaginator,
        ListXssMatchSetsPaginator,
    )

    session = get_session()
    with session.create_client("waf") as client:
        client: WAFClient

        get_rate_based_rule_managed_keys_paginator: GetRateBasedRuleManagedKeysPaginator = client.get_paginator("get_rate_based_rule_managed_keys")
        list_activated_rules_in_rule_group_paginator: ListActivatedRulesInRuleGroupPaginator = client.get_paginator("list_activated_rules_in_rule_group")
        list_byte_match_sets_paginator: ListByteMatchSetsPaginator = client.get_paginator("list_byte_match_sets")
        list_geo_match_sets_paginator: ListGeoMatchSetsPaginator = client.get_paginator("list_geo_match_sets")
        list_ip_sets_paginator: ListIPSetsPaginator = client.get_paginator("list_ip_sets")
        list_logging_configurations_paginator: ListLoggingConfigurationsPaginator = client.get_paginator("list_logging_configurations")
        list_rate_based_rules_paginator: ListRateBasedRulesPaginator = client.get_paginator("list_rate_based_rules")
        list_regex_match_sets_paginator: ListRegexMatchSetsPaginator = client.get_paginator("list_regex_match_sets")
        list_regex_pattern_sets_paginator: ListRegexPatternSetsPaginator = client.get_paginator("list_regex_pattern_sets")
        list_rule_groups_paginator: ListRuleGroupsPaginator = client.get_paginator("list_rule_groups")
        list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
        list_size_constraint_sets_paginator: ListSizeConstraintSetsPaginator = client.get_paginator("list_size_constraint_sets")
        list_sql_injection_match_sets_paginator: ListSqlInjectionMatchSetsPaginator = client.get_paginator("list_sql_injection_match_sets")
        list_subscribed_rule_groups_paginator: ListSubscribedRuleGroupsPaginator = client.get_paginator("list_subscribed_rule_groups")
        list_web_acls_paginator: ListWebACLsPaginator = client.get_paginator("list_web_acls")
        list_xss_match_sets_paginator: ListXssMatchSetsPaginator = client.get_paginator("list_xss_match_sets")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetRateBasedRuleManagedKeysRequestPaginateTypeDef,
    GetRateBasedRuleManagedKeysResponseTypeDef,
    ListActivatedRulesInRuleGroupRequestPaginateTypeDef,
    ListActivatedRulesInRuleGroupResponseTypeDef,
    ListByteMatchSetsRequestPaginateTypeDef,
    ListByteMatchSetsResponseTypeDef,
    ListGeoMatchSetsRequestPaginateTypeDef,
    ListGeoMatchSetsResponseTypeDef,
    ListIPSetsRequestPaginateTypeDef,
    ListIPSetsResponseTypeDef,
    ListLoggingConfigurationsRequestPaginateTypeDef,
    ListLoggingConfigurationsResponseTypeDef,
    ListRateBasedRulesRequestPaginateTypeDef,
    ListRateBasedRulesResponseTypeDef,
    ListRegexMatchSetsRequestPaginateTypeDef,
    ListRegexMatchSetsResponseTypeDef,
    ListRegexPatternSetsRequestPaginateTypeDef,
    ListRegexPatternSetsResponseTypeDef,
    ListRuleGroupsRequestPaginateTypeDef,
    ListRuleGroupsResponseTypeDef,
    ListRulesRequestPaginateTypeDef,
    ListRulesResponseTypeDef,
    ListSizeConstraintSetsRequestPaginateTypeDef,
    ListSizeConstraintSetsResponseTypeDef,
    ListSqlInjectionMatchSetsRequestPaginateTypeDef,
    ListSqlInjectionMatchSetsResponseTypeDef,
    ListSubscribedRuleGroupsRequestPaginateTypeDef,
    ListSubscribedRuleGroupsResponseTypeDef,
    ListWebACLsRequestPaginateTypeDef,
    ListWebACLsResponseTypeDef,
    ListXssMatchSetsRequestPaginateTypeDef,
    ListXssMatchSetsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetRateBasedRuleManagedKeysPaginator",
    "ListActivatedRulesInRuleGroupPaginator",
    "ListByteMatchSetsPaginator",
    "ListGeoMatchSetsPaginator",
    "ListIPSetsPaginator",
    "ListLoggingConfigurationsPaginator",
    "ListRateBasedRulesPaginator",
    "ListRegexMatchSetsPaginator",
    "ListRegexPatternSetsPaginator",
    "ListRuleGroupsPaginator",
    "ListRulesPaginator",
    "ListSizeConstraintSetsPaginator",
    "ListSqlInjectionMatchSetsPaginator",
    "ListSubscribedRuleGroupsPaginator",
    "ListWebACLsPaginator",
    "ListXssMatchSetsPaginator",
)


if TYPE_CHECKING:
    _GetRateBasedRuleManagedKeysPaginatorBase = AioPaginator[
        GetRateBasedRuleManagedKeysResponseTypeDef
    ]
else:
    _GetRateBasedRuleManagedKeysPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetRateBasedRuleManagedKeysPaginator(_GetRateBasedRuleManagedKeysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/GetRateBasedRuleManagedKeys.html#WAF.Paginator.GetRateBasedRuleManagedKeys)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#getratebasedrulemanagedkeyspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetRateBasedRuleManagedKeysRequestPaginateTypeDef]
    ) -> AioPageIterator[GetRateBasedRuleManagedKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/GetRateBasedRuleManagedKeys.html#WAF.Paginator.GetRateBasedRuleManagedKeys.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#getratebasedrulemanagedkeyspaginator)
        """


if TYPE_CHECKING:
    _ListActivatedRulesInRuleGroupPaginatorBase = AioPaginator[
        ListActivatedRulesInRuleGroupResponseTypeDef
    ]
else:
    _ListActivatedRulesInRuleGroupPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListActivatedRulesInRuleGroupPaginator(_ListActivatedRulesInRuleGroupPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListActivatedRulesInRuleGroup.html#WAF.Paginator.ListActivatedRulesInRuleGroup)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listactivatedrulesinrulegrouppaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListActivatedRulesInRuleGroupRequestPaginateTypeDef]
    ) -> AioPageIterator[ListActivatedRulesInRuleGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListActivatedRulesInRuleGroup.html#WAF.Paginator.ListActivatedRulesInRuleGroup.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listactivatedrulesinrulegrouppaginator)
        """


if TYPE_CHECKING:
    _ListByteMatchSetsPaginatorBase = AioPaginator[ListByteMatchSetsResponseTypeDef]
else:
    _ListByteMatchSetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListByteMatchSetsPaginator(_ListByteMatchSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListByteMatchSets.html#WAF.Paginator.ListByteMatchSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listbytematchsetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListByteMatchSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListByteMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListByteMatchSets.html#WAF.Paginator.ListByteMatchSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listbytematchsetspaginator)
        """


if TYPE_CHECKING:
    _ListGeoMatchSetsPaginatorBase = AioPaginator[ListGeoMatchSetsResponseTypeDef]
else:
    _ListGeoMatchSetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListGeoMatchSetsPaginator(_ListGeoMatchSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListGeoMatchSets.html#WAF.Paginator.ListGeoMatchSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listgeomatchsetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGeoMatchSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGeoMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListGeoMatchSets.html#WAF.Paginator.ListGeoMatchSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listgeomatchsetspaginator)
        """


if TYPE_CHECKING:
    _ListIPSetsPaginatorBase = AioPaginator[ListIPSetsResponseTypeDef]
else:
    _ListIPSetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListIPSetsPaginator(_ListIPSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListIPSets.html#WAF.Paginator.ListIPSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listipsetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIPSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListIPSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListIPSets.html#WAF.Paginator.ListIPSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listipsetspaginator)
        """


if TYPE_CHECKING:
    _ListLoggingConfigurationsPaginatorBase = AioPaginator[ListLoggingConfigurationsResponseTypeDef]
else:
    _ListLoggingConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListLoggingConfigurationsPaginator(_ListLoggingConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListLoggingConfigurations.html#WAF.Paginator.ListLoggingConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listloggingconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLoggingConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLoggingConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListLoggingConfigurations.html#WAF.Paginator.ListLoggingConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listloggingconfigurationspaginator)
        """


if TYPE_CHECKING:
    _ListRateBasedRulesPaginatorBase = AioPaginator[ListRateBasedRulesResponseTypeDef]
else:
    _ListRateBasedRulesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRateBasedRulesPaginator(_ListRateBasedRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRateBasedRules.html#WAF.Paginator.ListRateBasedRules)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listratebasedrulespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRateBasedRulesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRateBasedRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRateBasedRules.html#WAF.Paginator.ListRateBasedRules.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listratebasedrulespaginator)
        """


if TYPE_CHECKING:
    _ListRegexMatchSetsPaginatorBase = AioPaginator[ListRegexMatchSetsResponseTypeDef]
else:
    _ListRegexMatchSetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRegexMatchSetsPaginator(_ListRegexMatchSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRegexMatchSets.html#WAF.Paginator.ListRegexMatchSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listregexmatchsetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRegexMatchSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRegexMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRegexMatchSets.html#WAF.Paginator.ListRegexMatchSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listregexmatchsetspaginator)
        """


if TYPE_CHECKING:
    _ListRegexPatternSetsPaginatorBase = AioPaginator[ListRegexPatternSetsResponseTypeDef]
else:
    _ListRegexPatternSetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRegexPatternSetsPaginator(_ListRegexPatternSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRegexPatternSets.html#WAF.Paginator.ListRegexPatternSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listregexpatternsetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRegexPatternSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRegexPatternSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRegexPatternSets.html#WAF.Paginator.ListRegexPatternSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listregexpatternsetspaginator)
        """


if TYPE_CHECKING:
    _ListRuleGroupsPaginatorBase = AioPaginator[ListRuleGroupsResponseTypeDef]
else:
    _ListRuleGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRuleGroupsPaginator(_ListRuleGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRuleGroups.html#WAF.Paginator.ListRuleGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listrulegroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRuleGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRuleGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRuleGroups.html#WAF.Paginator.ListRuleGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listrulegroupspaginator)
        """


if TYPE_CHECKING:
    _ListRulesPaginatorBase = AioPaginator[ListRulesResponseTypeDef]
else:
    _ListRulesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRulesPaginator(_ListRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRules.html#WAF.Paginator.ListRules)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listrulespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRulesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListRules.html#WAF.Paginator.ListRules.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listrulespaginator)
        """


if TYPE_CHECKING:
    _ListSizeConstraintSetsPaginatorBase = AioPaginator[ListSizeConstraintSetsResponseTypeDef]
else:
    _ListSizeConstraintSetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSizeConstraintSetsPaginator(_ListSizeConstraintSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListSizeConstraintSets.html#WAF.Paginator.ListSizeConstraintSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listsizeconstraintsetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSizeConstraintSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSizeConstraintSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListSizeConstraintSets.html#WAF.Paginator.ListSizeConstraintSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listsizeconstraintsetspaginator)
        """


if TYPE_CHECKING:
    _ListSqlInjectionMatchSetsPaginatorBase = AioPaginator[ListSqlInjectionMatchSetsResponseTypeDef]
else:
    _ListSqlInjectionMatchSetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSqlInjectionMatchSetsPaginator(_ListSqlInjectionMatchSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListSqlInjectionMatchSets.html#WAF.Paginator.ListSqlInjectionMatchSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listsqlinjectionmatchsetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSqlInjectionMatchSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSqlInjectionMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListSqlInjectionMatchSets.html#WAF.Paginator.ListSqlInjectionMatchSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listsqlinjectionmatchsetspaginator)
        """


if TYPE_CHECKING:
    _ListSubscribedRuleGroupsPaginatorBase = AioPaginator[ListSubscribedRuleGroupsResponseTypeDef]
else:
    _ListSubscribedRuleGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSubscribedRuleGroupsPaginator(_ListSubscribedRuleGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListSubscribedRuleGroups.html#WAF.Paginator.ListSubscribedRuleGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listsubscribedrulegroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubscribedRuleGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSubscribedRuleGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListSubscribedRuleGroups.html#WAF.Paginator.ListSubscribedRuleGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listsubscribedrulegroupspaginator)
        """


if TYPE_CHECKING:
    _ListWebACLsPaginatorBase = AioPaginator[ListWebACLsResponseTypeDef]
else:
    _ListWebACLsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWebACLsPaginator(_ListWebACLsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListWebACLs.html#WAF.Paginator.ListWebACLs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listwebaclspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWebACLsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWebACLsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListWebACLs.html#WAF.Paginator.ListWebACLs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listwebaclspaginator)
        """


if TYPE_CHECKING:
    _ListXssMatchSetsPaginatorBase = AioPaginator[ListXssMatchSetsResponseTypeDef]
else:
    _ListXssMatchSetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListXssMatchSetsPaginator(_ListXssMatchSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListXssMatchSets.html#WAF.Paginator.ListXssMatchSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listxssmatchsetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListXssMatchSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListXssMatchSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/waf/paginator/ListXssMatchSets.html#WAF.Paginator.ListXssMatchSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_waf/paginators/#listxssmatchsetspaginator)
        """
