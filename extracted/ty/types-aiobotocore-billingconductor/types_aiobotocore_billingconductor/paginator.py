"""
Type annotations for billingconductor service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_billingconductor.client import BillingConductorClient
    from types_aiobotocore_billingconductor.paginator import (
        ListAccountAssociationsPaginator,
        ListBillingGroupCostReportsPaginator,
        ListBillingGroupsPaginator,
        ListCustomLineItemVersionsPaginator,
        ListCustomLineItemsPaginator,
        ListPricingPlansAssociatedWithPricingRulePaginator,
        ListPricingPlansPaginator,
        ListPricingRulesAssociatedToPricingPlanPaginator,
        ListPricingRulesPaginator,
        ListResourcesAssociatedToCustomLineItemPaginator,
    )

    session = get_session()
    with session.create_client("billingconductor") as client:
        client: BillingConductorClient

        list_account_associations_paginator: ListAccountAssociationsPaginator = client.get_paginator("list_account_associations")
        list_billing_group_cost_reports_paginator: ListBillingGroupCostReportsPaginator = client.get_paginator("list_billing_group_cost_reports")
        list_billing_groups_paginator: ListBillingGroupsPaginator = client.get_paginator("list_billing_groups")
        list_custom_line_item_versions_paginator: ListCustomLineItemVersionsPaginator = client.get_paginator("list_custom_line_item_versions")
        list_custom_line_items_paginator: ListCustomLineItemsPaginator = client.get_paginator("list_custom_line_items")
        list_pricing_plans_associated_with_pricing_rule_paginator: ListPricingPlansAssociatedWithPricingRulePaginator = client.get_paginator("list_pricing_plans_associated_with_pricing_rule")
        list_pricing_plans_paginator: ListPricingPlansPaginator = client.get_paginator("list_pricing_plans")
        list_pricing_rules_associated_to_pricing_plan_paginator: ListPricingRulesAssociatedToPricingPlanPaginator = client.get_paginator("list_pricing_rules_associated_to_pricing_plan")
        list_pricing_rules_paginator: ListPricingRulesPaginator = client.get_paginator("list_pricing_rules")
        list_resources_associated_to_custom_line_item_paginator: ListResourcesAssociatedToCustomLineItemPaginator = client.get_paginator("list_resources_associated_to_custom_line_item")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAccountAssociationsInputPaginateTypeDef,
    ListAccountAssociationsOutputTypeDef,
    ListBillingGroupCostReportsInputPaginateTypeDef,
    ListBillingGroupCostReportsOutputTypeDef,
    ListBillingGroupsInputPaginateTypeDef,
    ListBillingGroupsOutputTypeDef,
    ListCustomLineItemsInputPaginateTypeDef,
    ListCustomLineItemsOutputTypeDef,
    ListCustomLineItemVersionsInputPaginateTypeDef,
    ListCustomLineItemVersionsOutputTypeDef,
    ListPricingPlansAssociatedWithPricingRuleInputPaginateTypeDef,
    ListPricingPlansAssociatedWithPricingRuleOutputTypeDef,
    ListPricingPlansInputPaginateTypeDef,
    ListPricingPlansOutputTypeDef,
    ListPricingRulesAssociatedToPricingPlanInputPaginateTypeDef,
    ListPricingRulesAssociatedToPricingPlanOutputTypeDef,
    ListPricingRulesInputPaginateTypeDef,
    ListPricingRulesOutputTypeDef,
    ListResourcesAssociatedToCustomLineItemInputPaginateTypeDef,
    ListResourcesAssociatedToCustomLineItemOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAccountAssociationsPaginator",
    "ListBillingGroupCostReportsPaginator",
    "ListBillingGroupsPaginator",
    "ListCustomLineItemVersionsPaginator",
    "ListCustomLineItemsPaginator",
    "ListPricingPlansAssociatedWithPricingRulePaginator",
    "ListPricingPlansPaginator",
    "ListPricingRulesAssociatedToPricingPlanPaginator",
    "ListPricingRulesPaginator",
    "ListResourcesAssociatedToCustomLineItemPaginator",
)


if TYPE_CHECKING:
    _ListAccountAssociationsPaginatorBase = AioPaginator[ListAccountAssociationsOutputTypeDef]
else:
    _ListAccountAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAccountAssociationsPaginator(_ListAccountAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListAccountAssociations.html#BillingConductor.Paginator.ListAccountAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listaccountassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAccountAssociationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListAccountAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListAccountAssociations.html#BillingConductor.Paginator.ListAccountAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listaccountassociationspaginator)
        """


if TYPE_CHECKING:
    _ListBillingGroupCostReportsPaginatorBase = AioPaginator[
        ListBillingGroupCostReportsOutputTypeDef
    ]
else:
    _ListBillingGroupCostReportsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBillingGroupCostReportsPaginator(_ListBillingGroupCostReportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListBillingGroupCostReports.html#BillingConductor.Paginator.ListBillingGroupCostReports)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listbillinggroupcostreportspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBillingGroupCostReportsInputPaginateTypeDef]
    ) -> AioPageIterator[ListBillingGroupCostReportsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListBillingGroupCostReports.html#BillingConductor.Paginator.ListBillingGroupCostReports.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listbillinggroupcostreportspaginator)
        """


if TYPE_CHECKING:
    _ListBillingGroupsPaginatorBase = AioPaginator[ListBillingGroupsOutputTypeDef]
else:
    _ListBillingGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBillingGroupsPaginator(_ListBillingGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListBillingGroups.html#BillingConductor.Paginator.ListBillingGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listbillinggroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBillingGroupsInputPaginateTypeDef]
    ) -> AioPageIterator[ListBillingGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListBillingGroups.html#BillingConductor.Paginator.ListBillingGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listbillinggroupspaginator)
        """


if TYPE_CHECKING:
    _ListCustomLineItemVersionsPaginatorBase = AioPaginator[ListCustomLineItemVersionsOutputTypeDef]
else:
    _ListCustomLineItemVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCustomLineItemVersionsPaginator(_ListCustomLineItemVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListCustomLineItemVersions.html#BillingConductor.Paginator.ListCustomLineItemVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listcustomlineitemversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomLineItemVersionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListCustomLineItemVersionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListCustomLineItemVersions.html#BillingConductor.Paginator.ListCustomLineItemVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listcustomlineitemversionspaginator)
        """


if TYPE_CHECKING:
    _ListCustomLineItemsPaginatorBase = AioPaginator[ListCustomLineItemsOutputTypeDef]
else:
    _ListCustomLineItemsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCustomLineItemsPaginator(_ListCustomLineItemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListCustomLineItems.html#BillingConductor.Paginator.ListCustomLineItems)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listcustomlineitemspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomLineItemsInputPaginateTypeDef]
    ) -> AioPageIterator[ListCustomLineItemsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListCustomLineItems.html#BillingConductor.Paginator.ListCustomLineItems.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listcustomlineitemspaginator)
        """


if TYPE_CHECKING:
    _ListPricingPlansAssociatedWithPricingRulePaginatorBase = AioPaginator[
        ListPricingPlansAssociatedWithPricingRuleOutputTypeDef
    ]
else:
    _ListPricingPlansAssociatedWithPricingRulePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPricingPlansAssociatedWithPricingRulePaginator(
    _ListPricingPlansAssociatedWithPricingRulePaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListPricingPlansAssociatedWithPricingRule.html#BillingConductor.Paginator.ListPricingPlansAssociatedWithPricingRule)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listpricingplansassociatedwithpricingrulepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPricingPlansAssociatedWithPricingRuleInputPaginateTypeDef]
    ) -> AioPageIterator[ListPricingPlansAssociatedWithPricingRuleOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListPricingPlansAssociatedWithPricingRule.html#BillingConductor.Paginator.ListPricingPlansAssociatedWithPricingRule.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listpricingplansassociatedwithpricingrulepaginator)
        """


if TYPE_CHECKING:
    _ListPricingPlansPaginatorBase = AioPaginator[ListPricingPlansOutputTypeDef]
else:
    _ListPricingPlansPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPricingPlansPaginator(_ListPricingPlansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListPricingPlans.html#BillingConductor.Paginator.ListPricingPlans)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listpricingplanspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPricingPlansInputPaginateTypeDef]
    ) -> AioPageIterator[ListPricingPlansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListPricingPlans.html#BillingConductor.Paginator.ListPricingPlans.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listpricingplanspaginator)
        """


if TYPE_CHECKING:
    _ListPricingRulesAssociatedToPricingPlanPaginatorBase = AioPaginator[
        ListPricingRulesAssociatedToPricingPlanOutputTypeDef
    ]
else:
    _ListPricingRulesAssociatedToPricingPlanPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPricingRulesAssociatedToPricingPlanPaginator(
    _ListPricingRulesAssociatedToPricingPlanPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListPricingRulesAssociatedToPricingPlan.html#BillingConductor.Paginator.ListPricingRulesAssociatedToPricingPlan)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listpricingrulesassociatedtopricingplanpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPricingRulesAssociatedToPricingPlanInputPaginateTypeDef]
    ) -> AioPageIterator[ListPricingRulesAssociatedToPricingPlanOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListPricingRulesAssociatedToPricingPlan.html#BillingConductor.Paginator.ListPricingRulesAssociatedToPricingPlan.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listpricingrulesassociatedtopricingplanpaginator)
        """


if TYPE_CHECKING:
    _ListPricingRulesPaginatorBase = AioPaginator[ListPricingRulesOutputTypeDef]
else:
    _ListPricingRulesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPricingRulesPaginator(_ListPricingRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListPricingRules.html#BillingConductor.Paginator.ListPricingRules)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listpricingrulespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPricingRulesInputPaginateTypeDef]
    ) -> AioPageIterator[ListPricingRulesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListPricingRules.html#BillingConductor.Paginator.ListPricingRules.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listpricingrulespaginator)
        """


if TYPE_CHECKING:
    _ListResourcesAssociatedToCustomLineItemPaginatorBase = AioPaginator[
        ListResourcesAssociatedToCustomLineItemOutputTypeDef
    ]
else:
    _ListResourcesAssociatedToCustomLineItemPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourcesAssociatedToCustomLineItemPaginator(
    _ListResourcesAssociatedToCustomLineItemPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListResourcesAssociatedToCustomLineItem.html#BillingConductor.Paginator.ListResourcesAssociatedToCustomLineItem)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listresourcesassociatedtocustomlineitempaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourcesAssociatedToCustomLineItemInputPaginateTypeDef]
    ) -> AioPageIterator[ListResourcesAssociatedToCustomLineItemOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/billingconductor/paginator/ListResourcesAssociatedToCustomLineItem.html#BillingConductor.Paginator.ListResourcesAssociatedToCustomLineItem.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_billingconductor/paginators/#listresourcesassociatedtocustomlineitempaginator)
        """
