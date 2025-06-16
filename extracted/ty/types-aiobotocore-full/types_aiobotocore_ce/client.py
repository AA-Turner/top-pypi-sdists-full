"""
Type annotations for ce service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ce.client import CostExplorerClient

    session = get_session()
    async with session.create_client("ce") as client:
        client: CostExplorerClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    GetAnomaliesPaginator,
    GetAnomalyMonitorsPaginator,
    GetAnomalySubscriptionsPaginator,
    GetCostAndUsageComparisonsPaginator,
    GetCostComparisonDriversPaginator,
)
from .type_defs import (
    CreateAnomalyMonitorRequestTypeDef,
    CreateAnomalyMonitorResponseTypeDef,
    CreateAnomalySubscriptionRequestTypeDef,
    CreateAnomalySubscriptionResponseTypeDef,
    CreateCostCategoryDefinitionRequestTypeDef,
    CreateCostCategoryDefinitionResponseTypeDef,
    DeleteAnomalyMonitorRequestTypeDef,
    DeleteAnomalySubscriptionRequestTypeDef,
    DeleteCostCategoryDefinitionRequestTypeDef,
    DeleteCostCategoryDefinitionResponseTypeDef,
    DescribeCostCategoryDefinitionRequestTypeDef,
    DescribeCostCategoryDefinitionResponseTypeDef,
    GetAnomaliesRequestTypeDef,
    GetAnomaliesResponseTypeDef,
    GetAnomalyMonitorsRequestTypeDef,
    GetAnomalyMonitorsResponseTypeDef,
    GetAnomalySubscriptionsRequestTypeDef,
    GetAnomalySubscriptionsResponseTypeDef,
    GetApproximateUsageRecordsRequestTypeDef,
    GetApproximateUsageRecordsResponseTypeDef,
    GetCommitmentPurchaseAnalysisRequestTypeDef,
    GetCommitmentPurchaseAnalysisResponseTypeDef,
    GetCostAndUsageComparisonsRequestTypeDef,
    GetCostAndUsageComparisonsResponseTypeDef,
    GetCostAndUsageRequestTypeDef,
    GetCostAndUsageResponseTypeDef,
    GetCostAndUsageWithResourcesRequestTypeDef,
    GetCostAndUsageWithResourcesResponseTypeDef,
    GetCostCategoriesRequestTypeDef,
    GetCostCategoriesResponseTypeDef,
    GetCostComparisonDriversRequestTypeDef,
    GetCostComparisonDriversResponseTypeDef,
    GetCostForecastRequestTypeDef,
    GetCostForecastResponseTypeDef,
    GetDimensionValuesRequestTypeDef,
    GetDimensionValuesResponseTypeDef,
    GetReservationCoverageRequestTypeDef,
    GetReservationCoverageResponseTypeDef,
    GetReservationPurchaseRecommendationRequestTypeDef,
    GetReservationPurchaseRecommendationResponseTypeDef,
    GetReservationUtilizationRequestTypeDef,
    GetReservationUtilizationResponseTypeDef,
    GetRightsizingRecommendationRequestTypeDef,
    GetRightsizingRecommendationResponseTypeDef,
    GetSavingsPlanPurchaseRecommendationDetailsRequestTypeDef,
    GetSavingsPlanPurchaseRecommendationDetailsResponseTypeDef,
    GetSavingsPlansCoverageRequestTypeDef,
    GetSavingsPlansCoverageResponseTypeDef,
    GetSavingsPlansPurchaseRecommendationRequestTypeDef,
    GetSavingsPlansPurchaseRecommendationResponseTypeDef,
    GetSavingsPlansUtilizationDetailsRequestTypeDef,
    GetSavingsPlansUtilizationDetailsResponseTypeDef,
    GetSavingsPlansUtilizationRequestTypeDef,
    GetSavingsPlansUtilizationResponseTypeDef,
    GetTagsRequestTypeDef,
    GetTagsResponseTypeDef,
    GetUsageForecastRequestTypeDef,
    GetUsageForecastResponseTypeDef,
    ListCommitmentPurchaseAnalysesRequestTypeDef,
    ListCommitmentPurchaseAnalysesResponseTypeDef,
    ListCostAllocationTagBackfillHistoryRequestTypeDef,
    ListCostAllocationTagBackfillHistoryResponseTypeDef,
    ListCostAllocationTagsRequestTypeDef,
    ListCostAllocationTagsResponseTypeDef,
    ListCostCategoryDefinitionsRequestTypeDef,
    ListCostCategoryDefinitionsResponseTypeDef,
    ListSavingsPlansPurchaseRecommendationGenerationRequestTypeDef,
    ListSavingsPlansPurchaseRecommendationGenerationResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ProvideAnomalyFeedbackRequestTypeDef,
    ProvideAnomalyFeedbackResponseTypeDef,
    StartCommitmentPurchaseAnalysisRequestTypeDef,
    StartCommitmentPurchaseAnalysisResponseTypeDef,
    StartCostAllocationTagBackfillRequestTypeDef,
    StartCostAllocationTagBackfillResponseTypeDef,
    StartSavingsPlansPurchaseRecommendationGenerationResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAnomalyMonitorRequestTypeDef,
    UpdateAnomalyMonitorResponseTypeDef,
    UpdateAnomalySubscriptionRequestTypeDef,
    UpdateAnomalySubscriptionResponseTypeDef,
    UpdateCostAllocationTagsStatusRequestTypeDef,
    UpdateCostAllocationTagsStatusResponseTypeDef,
    UpdateCostCategoryDefinitionRequestTypeDef,
    UpdateCostCategoryDefinitionResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("CostExplorerClient",)


class Exceptions(BaseClientExceptions):
    AnalysisNotFoundException: Type[BotocoreClientError]
    BackfillLimitExceededException: Type[BotocoreClientError]
    BillExpirationException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DataUnavailableException: Type[BotocoreClientError]
    GenerationExistsException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    RequestChangedException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    UnknownMonitorException: Type[BotocoreClientError]
    UnknownSubscriptionException: Type[BotocoreClientError]
    UnresolvableUsageUnitException: Type[BotocoreClientError]


class CostExplorerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CostExplorerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#generate_presigned_url)
        """

    async def create_anomaly_monitor(
        self, **kwargs: Unpack[CreateAnomalyMonitorRequestTypeDef]
    ) -> CreateAnomalyMonitorResponseTypeDef:
        """
        Creates a new cost anomaly detection monitor with the requested type and
        monitor specification.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/create_anomaly_monitor.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#create_anomaly_monitor)
        """

    async def create_anomaly_subscription(
        self, **kwargs: Unpack[CreateAnomalySubscriptionRequestTypeDef]
    ) -> CreateAnomalySubscriptionResponseTypeDef:
        """
        Adds an alert subscription to a cost anomaly detection monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/create_anomaly_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#create_anomaly_subscription)
        """

    async def create_cost_category_definition(
        self, **kwargs: Unpack[CreateCostCategoryDefinitionRequestTypeDef]
    ) -> CreateCostCategoryDefinitionResponseTypeDef:
        """
        Creates a new Cost Category with the requested name and rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/create_cost_category_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#create_cost_category_definition)
        """

    async def delete_anomaly_monitor(
        self, **kwargs: Unpack[DeleteAnomalyMonitorRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a cost anomaly monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/delete_anomaly_monitor.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#delete_anomaly_monitor)
        """

    async def delete_anomaly_subscription(
        self, **kwargs: Unpack[DeleteAnomalySubscriptionRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a cost anomaly subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/delete_anomaly_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#delete_anomaly_subscription)
        """

    async def delete_cost_category_definition(
        self, **kwargs: Unpack[DeleteCostCategoryDefinitionRequestTypeDef]
    ) -> DeleteCostCategoryDefinitionResponseTypeDef:
        """
        Deletes a Cost Category.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/delete_cost_category_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#delete_cost_category_definition)
        """

    async def describe_cost_category_definition(
        self, **kwargs: Unpack[DescribeCostCategoryDefinitionRequestTypeDef]
    ) -> DescribeCostCategoryDefinitionResponseTypeDef:
        """
        Returns the name, Amazon Resource Name (ARN), rules, definition, and effective
        dates of a Cost Category that's defined in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/describe_cost_category_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#describe_cost_category_definition)
        """

    async def get_anomalies(
        self, **kwargs: Unpack[GetAnomaliesRequestTypeDef]
    ) -> GetAnomaliesResponseTypeDef:
        """
        Retrieves all of the cost anomalies detected on your account during the time
        period that's specified by the <code>DateInterval</code> object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_anomalies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_anomalies)
        """

    async def get_anomaly_monitors(
        self, **kwargs: Unpack[GetAnomalyMonitorsRequestTypeDef]
    ) -> GetAnomalyMonitorsResponseTypeDef:
        """
        Retrieves the cost anomaly monitor definitions for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_anomaly_monitors.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_anomaly_monitors)
        """

    async def get_anomaly_subscriptions(
        self, **kwargs: Unpack[GetAnomalySubscriptionsRequestTypeDef]
    ) -> GetAnomalySubscriptionsResponseTypeDef:
        """
        Retrieves the cost anomaly subscription objects for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_anomaly_subscriptions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_anomaly_subscriptions)
        """

    async def get_approximate_usage_records(
        self, **kwargs: Unpack[GetApproximateUsageRecordsRequestTypeDef]
    ) -> GetApproximateUsageRecordsResponseTypeDef:
        """
        Retrieves estimated usage records for hourly granularity or resource-level data
        at daily granularity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_approximate_usage_records.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_approximate_usage_records)
        """

    async def get_commitment_purchase_analysis(
        self, **kwargs: Unpack[GetCommitmentPurchaseAnalysisRequestTypeDef]
    ) -> GetCommitmentPurchaseAnalysisResponseTypeDef:
        """
        Retrieves a commitment purchase analysis result based on the
        <code>AnalysisId</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_commitment_purchase_analysis.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_commitment_purchase_analysis)
        """

    async def get_cost_and_usage(
        self, **kwargs: Unpack[GetCostAndUsageRequestTypeDef]
    ) -> GetCostAndUsageResponseTypeDef:
        """
        Retrieves cost and usage metrics for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_cost_and_usage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_cost_and_usage)
        """

    async def get_cost_and_usage_comparisons(
        self, **kwargs: Unpack[GetCostAndUsageComparisonsRequestTypeDef]
    ) -> GetCostAndUsageComparisonsResponseTypeDef:
        """
        Retrieves cost and usage comparisons for your account between two periods
        within the last 13 months.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_cost_and_usage_comparisons.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_cost_and_usage_comparisons)
        """

    async def get_cost_and_usage_with_resources(
        self, **kwargs: Unpack[GetCostAndUsageWithResourcesRequestTypeDef]
    ) -> GetCostAndUsageWithResourcesResponseTypeDef:
        """
        Retrieves cost and usage metrics with resources for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_cost_and_usage_with_resources.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_cost_and_usage_with_resources)
        """

    async def get_cost_categories(
        self, **kwargs: Unpack[GetCostCategoriesRequestTypeDef]
    ) -> GetCostCategoriesResponseTypeDef:
        """
        Retrieves an array of Cost Category names and values incurred cost.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_cost_categories.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_cost_categories)
        """

    async def get_cost_comparison_drivers(
        self, **kwargs: Unpack[GetCostComparisonDriversRequestTypeDef]
    ) -> GetCostComparisonDriversResponseTypeDef:
        """
        Retrieves key factors driving cost changes between two time periods within the
        last 13 months, such as usage changes, discount changes, and commitment-based
        savings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_cost_comparison_drivers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_cost_comparison_drivers)
        """

    async def get_cost_forecast(
        self, **kwargs: Unpack[GetCostForecastRequestTypeDef]
    ) -> GetCostForecastResponseTypeDef:
        """
        Retrieves a forecast for how much Amazon Web Services predicts that you will
        spend over the forecast time period that you select, based on your past costs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_cost_forecast.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_cost_forecast)
        """

    async def get_dimension_values(
        self, **kwargs: Unpack[GetDimensionValuesRequestTypeDef]
    ) -> GetDimensionValuesResponseTypeDef:
        """
        Retrieves all available filter values for a specified filter over a period of
        time.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_dimension_values.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_dimension_values)
        """

    async def get_reservation_coverage(
        self, **kwargs: Unpack[GetReservationCoverageRequestTypeDef]
    ) -> GetReservationCoverageResponseTypeDef:
        """
        Retrieves the reservation coverage for your account, which you can use to see
        how much of your Amazon Elastic Compute Cloud, Amazon ElastiCache, Amazon
        Relational Database Service, or Amazon Redshift usage is covered by a
        reservation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_reservation_coverage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_reservation_coverage)
        """

    async def get_reservation_purchase_recommendation(
        self, **kwargs: Unpack[GetReservationPurchaseRecommendationRequestTypeDef]
    ) -> GetReservationPurchaseRecommendationResponseTypeDef:
        """
        Gets recommendations for reservation purchases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_reservation_purchase_recommendation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_reservation_purchase_recommendation)
        """

    async def get_reservation_utilization(
        self, **kwargs: Unpack[GetReservationUtilizationRequestTypeDef]
    ) -> GetReservationUtilizationResponseTypeDef:
        """
        Retrieves the reservation utilization for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_reservation_utilization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_reservation_utilization)
        """

    async def get_rightsizing_recommendation(
        self, **kwargs: Unpack[GetRightsizingRecommendationRequestTypeDef]
    ) -> GetRightsizingRecommendationResponseTypeDef:
        """
        Creates recommendations that help you save cost by identifying idle and
        underutilized Amazon EC2 instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_rightsizing_recommendation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_rightsizing_recommendation)
        """

    async def get_savings_plan_purchase_recommendation_details(
        self, **kwargs: Unpack[GetSavingsPlanPurchaseRecommendationDetailsRequestTypeDef]
    ) -> GetSavingsPlanPurchaseRecommendationDetailsResponseTypeDef:
        """
        Retrieves the details for a Savings Plan recommendation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_savings_plan_purchase_recommendation_details.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_savings_plan_purchase_recommendation_details)
        """

    async def get_savings_plans_coverage(
        self, **kwargs: Unpack[GetSavingsPlansCoverageRequestTypeDef]
    ) -> GetSavingsPlansCoverageResponseTypeDef:
        """
        Retrieves the Savings Plans covered for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_savings_plans_coverage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_savings_plans_coverage)
        """

    async def get_savings_plans_purchase_recommendation(
        self, **kwargs: Unpack[GetSavingsPlansPurchaseRecommendationRequestTypeDef]
    ) -> GetSavingsPlansPurchaseRecommendationResponseTypeDef:
        """
        Retrieves the Savings Plans recommendations for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_savings_plans_purchase_recommendation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_savings_plans_purchase_recommendation)
        """

    async def get_savings_plans_utilization(
        self, **kwargs: Unpack[GetSavingsPlansUtilizationRequestTypeDef]
    ) -> GetSavingsPlansUtilizationResponseTypeDef:
        """
        Retrieves the Savings Plans utilization for your account across date ranges
        with daily or monthly granularity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_savings_plans_utilization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_savings_plans_utilization)
        """

    async def get_savings_plans_utilization_details(
        self, **kwargs: Unpack[GetSavingsPlansUtilizationDetailsRequestTypeDef]
    ) -> GetSavingsPlansUtilizationDetailsResponseTypeDef:
        """
        Retrieves attribute data along with aggregate utilization and savings data for
        a given time period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_savings_plans_utilization_details.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_savings_plans_utilization_details)
        """

    async def get_tags(self, **kwargs: Unpack[GetTagsRequestTypeDef]) -> GetTagsResponseTypeDef:
        """
        Queries for available tag keys and tag values for a specified period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_tags)
        """

    async def get_usage_forecast(
        self, **kwargs: Unpack[GetUsageForecastRequestTypeDef]
    ) -> GetUsageForecastResponseTypeDef:
        """
        Retrieves a forecast for how much Amazon Web Services predicts that you will
        use over the forecast time period that you select, based on your past usage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_usage_forecast.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_usage_forecast)
        """

    async def list_commitment_purchase_analyses(
        self, **kwargs: Unpack[ListCommitmentPurchaseAnalysesRequestTypeDef]
    ) -> ListCommitmentPurchaseAnalysesResponseTypeDef:
        """
        Lists the commitment purchase analyses for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/list_commitment_purchase_analyses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#list_commitment_purchase_analyses)
        """

    async def list_cost_allocation_tag_backfill_history(
        self, **kwargs: Unpack[ListCostAllocationTagBackfillHistoryRequestTypeDef]
    ) -> ListCostAllocationTagBackfillHistoryResponseTypeDef:
        """
        Retrieves a list of your historical cost allocation tag backfill requests.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/list_cost_allocation_tag_backfill_history.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#list_cost_allocation_tag_backfill_history)
        """

    async def list_cost_allocation_tags(
        self, **kwargs: Unpack[ListCostAllocationTagsRequestTypeDef]
    ) -> ListCostAllocationTagsResponseTypeDef:
        """
        Get a list of cost allocation tags.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/list_cost_allocation_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#list_cost_allocation_tags)
        """

    async def list_cost_category_definitions(
        self, **kwargs: Unpack[ListCostCategoryDefinitionsRequestTypeDef]
    ) -> ListCostCategoryDefinitionsResponseTypeDef:
        """
        Returns the name, Amazon Resource Name (ARN), <code>NumberOfRules</code> and
        effective dates of all Cost Categories defined in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/list_cost_category_definitions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#list_cost_category_definitions)
        """

    async def list_savings_plans_purchase_recommendation_generation(
        self, **kwargs: Unpack[ListSavingsPlansPurchaseRecommendationGenerationRequestTypeDef]
    ) -> ListSavingsPlansPurchaseRecommendationGenerationResponseTypeDef:
        """
        Retrieves a list of your historical recommendation generations within the past
        30 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/list_savings_plans_purchase_recommendation_generation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#list_savings_plans_purchase_recommendation_generation)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of resource tags associated with the resource specified by the
        Amazon Resource Name (ARN).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#list_tags_for_resource)
        """

    async def provide_anomaly_feedback(
        self, **kwargs: Unpack[ProvideAnomalyFeedbackRequestTypeDef]
    ) -> ProvideAnomalyFeedbackResponseTypeDef:
        """
        Modifies the feedback property of a given cost anomaly.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/provide_anomaly_feedback.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#provide_anomaly_feedback)
        """

    async def start_commitment_purchase_analysis(
        self, **kwargs: Unpack[StartCommitmentPurchaseAnalysisRequestTypeDef]
    ) -> StartCommitmentPurchaseAnalysisResponseTypeDef:
        """
        Specifies the parameters of a planned commitment purchase and starts the
        generation of the analysis.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/start_commitment_purchase_analysis.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#start_commitment_purchase_analysis)
        """

    async def start_cost_allocation_tag_backfill(
        self, **kwargs: Unpack[StartCostAllocationTagBackfillRequestTypeDef]
    ) -> StartCostAllocationTagBackfillResponseTypeDef:
        """
        Request a cost allocation tag backfill.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/start_cost_allocation_tag_backfill.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#start_cost_allocation_tag_backfill)
        """

    async def start_savings_plans_purchase_recommendation_generation(
        self,
    ) -> StartSavingsPlansPurchaseRecommendationGenerationResponseTypeDef:
        """
        Requests a Savings Plans recommendation generation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/start_savings_plans_purchase_recommendation_generation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#start_savings_plans_purchase_recommendation_generation)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        An API operation for adding one or more tags (key-value pairs) to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes one or more tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#untag_resource)
        """

    async def update_anomaly_monitor(
        self, **kwargs: Unpack[UpdateAnomalyMonitorRequestTypeDef]
    ) -> UpdateAnomalyMonitorResponseTypeDef:
        """
        Updates an existing cost anomaly monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/update_anomaly_monitor.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#update_anomaly_monitor)
        """

    async def update_anomaly_subscription(
        self, **kwargs: Unpack[UpdateAnomalySubscriptionRequestTypeDef]
    ) -> UpdateAnomalySubscriptionResponseTypeDef:
        """
        Updates an existing cost anomaly subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/update_anomaly_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#update_anomaly_subscription)
        """

    async def update_cost_allocation_tags_status(
        self, **kwargs: Unpack[UpdateCostAllocationTagsStatusRequestTypeDef]
    ) -> UpdateCostAllocationTagsStatusResponseTypeDef:
        """
        Updates status for cost allocation tags in bulk, with maximum batch size of 20.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/update_cost_allocation_tags_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#update_cost_allocation_tags_status)
        """

    async def update_cost_category_definition(
        self, **kwargs: Unpack[UpdateCostCategoryDefinitionRequestTypeDef]
    ) -> UpdateCostCategoryDefinitionResponseTypeDef:
        """
        Updates an existing Cost Category.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/update_cost_category_definition.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#update_cost_category_definition)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_anomalies"]
    ) -> GetAnomaliesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_anomaly_monitors"]
    ) -> GetAnomalyMonitorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_anomaly_subscriptions"]
    ) -> GetAnomalySubscriptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_cost_and_usage_comparisons"]
    ) -> GetCostAndUsageComparisonsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["get_cost_comparison_drivers"]
    ) -> GetCostComparisonDriversPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ce.html#CostExplorer.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ce/client/)
        """
