"""
Type annotations for elbv2 service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_elbv2.client import ElasticLoadBalancingv2Client
    from types_aiobotocore_elbv2.paginator import (
        DescribeAccountLimitsPaginator,
        DescribeListenerCertificatesPaginator,
        DescribeListenersPaginator,
        DescribeLoadBalancersPaginator,
        DescribeRulesPaginator,
        DescribeSSLPoliciesPaginator,
        DescribeTargetGroupsPaginator,
        DescribeTrustStoreAssociationsPaginator,
        DescribeTrustStoreRevocationsPaginator,
        DescribeTrustStoresPaginator,
    )

    session = get_session()
    with session.create_client("elbv2") as client:
        client: ElasticLoadBalancingv2Client

        describe_account_limits_paginator: DescribeAccountLimitsPaginator = client.get_paginator("describe_account_limits")
        describe_listener_certificates_paginator: DescribeListenerCertificatesPaginator = client.get_paginator("describe_listener_certificates")
        describe_listeners_paginator: DescribeListenersPaginator = client.get_paginator("describe_listeners")
        describe_load_balancers_paginator: DescribeLoadBalancersPaginator = client.get_paginator("describe_load_balancers")
        describe_rules_paginator: DescribeRulesPaginator = client.get_paginator("describe_rules")
        describe_ssl_policies_paginator: DescribeSSLPoliciesPaginator = client.get_paginator("describe_ssl_policies")
        describe_target_groups_paginator: DescribeTargetGroupsPaginator = client.get_paginator("describe_target_groups")
        describe_trust_store_associations_paginator: DescribeTrustStoreAssociationsPaginator = client.get_paginator("describe_trust_store_associations")
        describe_trust_store_revocations_paginator: DescribeTrustStoreRevocationsPaginator = client.get_paginator("describe_trust_store_revocations")
        describe_trust_stores_paginator: DescribeTrustStoresPaginator = client.get_paginator("describe_trust_stores")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeAccountLimitsInputPaginateTypeDef,
    DescribeAccountLimitsOutputTypeDef,
    DescribeListenerCertificatesInputPaginateTypeDef,
    DescribeListenerCertificatesOutputTypeDef,
    DescribeListenersInputPaginateTypeDef,
    DescribeListenersOutputTypeDef,
    DescribeLoadBalancersInputPaginateTypeDef,
    DescribeLoadBalancersOutputTypeDef,
    DescribeRulesInputPaginateTypeDef,
    DescribeRulesOutputTypeDef,
    DescribeSSLPoliciesInputPaginateTypeDef,
    DescribeSSLPoliciesOutputTypeDef,
    DescribeTargetGroupsInputPaginateTypeDef,
    DescribeTargetGroupsOutputTypeDef,
    DescribeTrustStoreAssociationsInputPaginateTypeDef,
    DescribeTrustStoreAssociationsOutputTypeDef,
    DescribeTrustStoreRevocationsInputPaginateTypeDef,
    DescribeTrustStoreRevocationsOutputTypeDef,
    DescribeTrustStoresInputPaginateTypeDef,
    DescribeTrustStoresOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeAccountLimitsPaginator",
    "DescribeListenerCertificatesPaginator",
    "DescribeListenersPaginator",
    "DescribeLoadBalancersPaginator",
    "DescribeRulesPaginator",
    "DescribeSSLPoliciesPaginator",
    "DescribeTargetGroupsPaginator",
    "DescribeTrustStoreAssociationsPaginator",
    "DescribeTrustStoreRevocationsPaginator",
    "DescribeTrustStoresPaginator",
)


if TYPE_CHECKING:
    _DescribeAccountLimitsPaginatorBase = AioPaginator[DescribeAccountLimitsOutputTypeDef]
else:
    _DescribeAccountLimitsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeAccountLimitsPaginator(_DescribeAccountLimitsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeAccountLimits.html#ElasticLoadBalancingv2.Paginator.DescribeAccountLimits)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describeaccountlimitspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAccountLimitsInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeAccountLimitsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeAccountLimits.html#ElasticLoadBalancingv2.Paginator.DescribeAccountLimits.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describeaccountlimitspaginator)
        """


if TYPE_CHECKING:
    _DescribeListenerCertificatesPaginatorBase = AioPaginator[
        DescribeListenerCertificatesOutputTypeDef
    ]
else:
    _DescribeListenerCertificatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeListenerCertificatesPaginator(_DescribeListenerCertificatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeListenerCertificates.html#ElasticLoadBalancingv2.Paginator.DescribeListenerCertificates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describelistenercertificatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeListenerCertificatesInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeListenerCertificatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeListenerCertificates.html#ElasticLoadBalancingv2.Paginator.DescribeListenerCertificates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describelistenercertificatespaginator)
        """


if TYPE_CHECKING:
    _DescribeListenersPaginatorBase = AioPaginator[DescribeListenersOutputTypeDef]
else:
    _DescribeListenersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeListenersPaginator(_DescribeListenersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeListeners.html#ElasticLoadBalancingv2.Paginator.DescribeListeners)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describelistenerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeListenersInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeListenersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeListeners.html#ElasticLoadBalancingv2.Paginator.DescribeListeners.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describelistenerspaginator)
        """


if TYPE_CHECKING:
    _DescribeLoadBalancersPaginatorBase = AioPaginator[DescribeLoadBalancersOutputTypeDef]
else:
    _DescribeLoadBalancersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeLoadBalancersPaginator(_DescribeLoadBalancersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeLoadBalancers.html#ElasticLoadBalancingv2.Paginator.DescribeLoadBalancers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describeloadbalancerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeLoadBalancersInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeLoadBalancersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeLoadBalancers.html#ElasticLoadBalancingv2.Paginator.DescribeLoadBalancers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describeloadbalancerspaginator)
        """


if TYPE_CHECKING:
    _DescribeRulesPaginatorBase = AioPaginator[DescribeRulesOutputTypeDef]
else:
    _DescribeRulesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeRulesPaginator(_DescribeRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeRules.html#ElasticLoadBalancingv2.Paginator.DescribeRules)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describerulespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeRulesInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeRulesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeRules.html#ElasticLoadBalancingv2.Paginator.DescribeRules.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describerulespaginator)
        """


if TYPE_CHECKING:
    _DescribeSSLPoliciesPaginatorBase = AioPaginator[DescribeSSLPoliciesOutputTypeDef]
else:
    _DescribeSSLPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeSSLPoliciesPaginator(_DescribeSSLPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeSSLPolicies.html#ElasticLoadBalancingv2.Paginator.DescribeSSLPolicies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describesslpoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSSLPoliciesInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeSSLPoliciesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeSSLPolicies.html#ElasticLoadBalancingv2.Paginator.DescribeSSLPolicies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describesslpoliciespaginator)
        """


if TYPE_CHECKING:
    _DescribeTargetGroupsPaginatorBase = AioPaginator[DescribeTargetGroupsOutputTypeDef]
else:
    _DescribeTargetGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeTargetGroupsPaginator(_DescribeTargetGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeTargetGroups.html#ElasticLoadBalancingv2.Paginator.DescribeTargetGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describetargetgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTargetGroupsInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeTargetGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeTargetGroups.html#ElasticLoadBalancingv2.Paginator.DescribeTargetGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describetargetgroupspaginator)
        """


if TYPE_CHECKING:
    _DescribeTrustStoreAssociationsPaginatorBase = AioPaginator[
        DescribeTrustStoreAssociationsOutputTypeDef
    ]
else:
    _DescribeTrustStoreAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeTrustStoreAssociationsPaginator(_DescribeTrustStoreAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeTrustStoreAssociations.html#ElasticLoadBalancingv2.Paginator.DescribeTrustStoreAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describetruststoreassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTrustStoreAssociationsInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeTrustStoreAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeTrustStoreAssociations.html#ElasticLoadBalancingv2.Paginator.DescribeTrustStoreAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describetruststoreassociationspaginator)
        """


if TYPE_CHECKING:
    _DescribeTrustStoreRevocationsPaginatorBase = AioPaginator[
        DescribeTrustStoreRevocationsOutputTypeDef
    ]
else:
    _DescribeTrustStoreRevocationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeTrustStoreRevocationsPaginator(_DescribeTrustStoreRevocationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeTrustStoreRevocations.html#ElasticLoadBalancingv2.Paginator.DescribeTrustStoreRevocations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describetruststorerevocationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTrustStoreRevocationsInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeTrustStoreRevocationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeTrustStoreRevocations.html#ElasticLoadBalancingv2.Paginator.DescribeTrustStoreRevocations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describetruststorerevocationspaginator)
        """


if TYPE_CHECKING:
    _DescribeTrustStoresPaginatorBase = AioPaginator[DescribeTrustStoresOutputTypeDef]
else:
    _DescribeTrustStoresPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeTrustStoresPaginator(_DescribeTrustStoresPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeTrustStores.html#ElasticLoadBalancingv2.Paginator.DescribeTrustStores)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describetruststorespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTrustStoresInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeTrustStoresOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/paginator/DescribeTrustStores.html#ElasticLoadBalancingv2.Paginator.DescribeTrustStores.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_elbv2/paginators/#describetruststorespaginator)
        """
