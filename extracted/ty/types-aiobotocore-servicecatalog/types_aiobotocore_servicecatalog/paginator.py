"""
Type annotations for servicecatalog service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_servicecatalog.client import ServiceCatalogClient
    from types_aiobotocore_servicecatalog.paginator import (
        ListAcceptedPortfolioSharesPaginator,
        ListConstraintsForPortfolioPaginator,
        ListLaunchPathsPaginator,
        ListOrganizationPortfolioAccessPaginator,
        ListPortfoliosForProductPaginator,
        ListPortfoliosPaginator,
        ListPrincipalsForPortfolioPaginator,
        ListProvisionedProductPlansPaginator,
        ListProvisioningArtifactsForServiceActionPaginator,
        ListRecordHistoryPaginator,
        ListResourcesForTagOptionPaginator,
        ListServiceActionsForProvisioningArtifactPaginator,
        ListServiceActionsPaginator,
        ListTagOptionsPaginator,
        ScanProvisionedProductsPaginator,
        SearchProductsAsAdminPaginator,
    )

    session = get_session()
    with session.create_client("servicecatalog") as client:
        client: ServiceCatalogClient

        list_accepted_portfolio_shares_paginator: ListAcceptedPortfolioSharesPaginator = client.get_paginator("list_accepted_portfolio_shares")
        list_constraints_for_portfolio_paginator: ListConstraintsForPortfolioPaginator = client.get_paginator("list_constraints_for_portfolio")
        list_launch_paths_paginator: ListLaunchPathsPaginator = client.get_paginator("list_launch_paths")
        list_organization_portfolio_access_paginator: ListOrganizationPortfolioAccessPaginator = client.get_paginator("list_organization_portfolio_access")
        list_portfolios_for_product_paginator: ListPortfoliosForProductPaginator = client.get_paginator("list_portfolios_for_product")
        list_portfolios_paginator: ListPortfoliosPaginator = client.get_paginator("list_portfolios")
        list_principals_for_portfolio_paginator: ListPrincipalsForPortfolioPaginator = client.get_paginator("list_principals_for_portfolio")
        list_provisioned_product_plans_paginator: ListProvisionedProductPlansPaginator = client.get_paginator("list_provisioned_product_plans")
        list_provisioning_artifacts_for_service_action_paginator: ListProvisioningArtifactsForServiceActionPaginator = client.get_paginator("list_provisioning_artifacts_for_service_action")
        list_record_history_paginator: ListRecordHistoryPaginator = client.get_paginator("list_record_history")
        list_resources_for_tag_option_paginator: ListResourcesForTagOptionPaginator = client.get_paginator("list_resources_for_tag_option")
        list_service_actions_for_provisioning_artifact_paginator: ListServiceActionsForProvisioningArtifactPaginator = client.get_paginator("list_service_actions_for_provisioning_artifact")
        list_service_actions_paginator: ListServiceActionsPaginator = client.get_paginator("list_service_actions")
        list_tag_options_paginator: ListTagOptionsPaginator = client.get_paginator("list_tag_options")
        scan_provisioned_products_paginator: ScanProvisionedProductsPaginator = client.get_paginator("scan_provisioned_products")
        search_products_as_admin_paginator: SearchProductsAsAdminPaginator = client.get_paginator("search_products_as_admin")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAcceptedPortfolioSharesInputPaginateTypeDef,
    ListAcceptedPortfolioSharesOutputTypeDef,
    ListConstraintsForPortfolioInputPaginateTypeDef,
    ListConstraintsForPortfolioOutputTypeDef,
    ListLaunchPathsInputPaginateTypeDef,
    ListLaunchPathsOutputTypeDef,
    ListOrganizationPortfolioAccessInputPaginateTypeDef,
    ListOrganizationPortfolioAccessOutputTypeDef,
    ListPortfoliosForProductInputPaginateTypeDef,
    ListPortfoliosForProductOutputTypeDef,
    ListPortfoliosInputPaginateTypeDef,
    ListPortfoliosOutputTypeDef,
    ListPrincipalsForPortfolioInputPaginateTypeDef,
    ListPrincipalsForPortfolioOutputTypeDef,
    ListProvisionedProductPlansInputPaginateTypeDef,
    ListProvisionedProductPlansOutputTypeDef,
    ListProvisioningArtifactsForServiceActionInputPaginateTypeDef,
    ListProvisioningArtifactsForServiceActionOutputTypeDef,
    ListRecordHistoryInputPaginateTypeDef,
    ListRecordHistoryOutputTypeDef,
    ListResourcesForTagOptionInputPaginateTypeDef,
    ListResourcesForTagOptionOutputTypeDef,
    ListServiceActionsForProvisioningArtifactInputPaginateTypeDef,
    ListServiceActionsForProvisioningArtifactOutputTypeDef,
    ListServiceActionsInputPaginateTypeDef,
    ListServiceActionsOutputTypeDef,
    ListTagOptionsInputPaginateTypeDef,
    ListTagOptionsOutputTypeDef,
    ScanProvisionedProductsInputPaginateTypeDef,
    ScanProvisionedProductsOutputTypeDef,
    SearchProductsAsAdminInputPaginateTypeDef,
    SearchProductsAsAdminOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAcceptedPortfolioSharesPaginator",
    "ListConstraintsForPortfolioPaginator",
    "ListLaunchPathsPaginator",
    "ListOrganizationPortfolioAccessPaginator",
    "ListPortfoliosForProductPaginator",
    "ListPortfoliosPaginator",
    "ListPrincipalsForPortfolioPaginator",
    "ListProvisionedProductPlansPaginator",
    "ListProvisioningArtifactsForServiceActionPaginator",
    "ListRecordHistoryPaginator",
    "ListResourcesForTagOptionPaginator",
    "ListServiceActionsForProvisioningArtifactPaginator",
    "ListServiceActionsPaginator",
    "ListTagOptionsPaginator",
    "ScanProvisionedProductsPaginator",
    "SearchProductsAsAdminPaginator",
)


if TYPE_CHECKING:
    _ListAcceptedPortfolioSharesPaginatorBase = AioPaginator[
        ListAcceptedPortfolioSharesOutputTypeDef
    ]
else:
    _ListAcceptedPortfolioSharesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAcceptedPortfolioSharesPaginator(_ListAcceptedPortfolioSharesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListAcceptedPortfolioShares.html#ServiceCatalog.Paginator.ListAcceptedPortfolioShares)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listacceptedportfoliosharespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAcceptedPortfolioSharesInputPaginateTypeDef]
    ) -> AioPageIterator[ListAcceptedPortfolioSharesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListAcceptedPortfolioShares.html#ServiceCatalog.Paginator.ListAcceptedPortfolioShares.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listacceptedportfoliosharespaginator)
        """


if TYPE_CHECKING:
    _ListConstraintsForPortfolioPaginatorBase = AioPaginator[
        ListConstraintsForPortfolioOutputTypeDef
    ]
else:
    _ListConstraintsForPortfolioPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListConstraintsForPortfolioPaginator(_ListConstraintsForPortfolioPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListConstraintsForPortfolio.html#ServiceCatalog.Paginator.ListConstraintsForPortfolio)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listconstraintsforportfoliopaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConstraintsForPortfolioInputPaginateTypeDef]
    ) -> AioPageIterator[ListConstraintsForPortfolioOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListConstraintsForPortfolio.html#ServiceCatalog.Paginator.ListConstraintsForPortfolio.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listconstraintsforportfoliopaginator)
        """


if TYPE_CHECKING:
    _ListLaunchPathsPaginatorBase = AioPaginator[ListLaunchPathsOutputTypeDef]
else:
    _ListLaunchPathsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListLaunchPathsPaginator(_ListLaunchPathsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListLaunchPaths.html#ServiceCatalog.Paginator.ListLaunchPaths)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listlaunchpathspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLaunchPathsInputPaginateTypeDef]
    ) -> AioPageIterator[ListLaunchPathsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListLaunchPaths.html#ServiceCatalog.Paginator.ListLaunchPaths.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listlaunchpathspaginator)
        """


if TYPE_CHECKING:
    _ListOrganizationPortfolioAccessPaginatorBase = AioPaginator[
        ListOrganizationPortfolioAccessOutputTypeDef
    ]
else:
    _ListOrganizationPortfolioAccessPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOrganizationPortfolioAccessPaginator(_ListOrganizationPortfolioAccessPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListOrganizationPortfolioAccess.html#ServiceCatalog.Paginator.ListOrganizationPortfolioAccess)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listorganizationportfolioaccesspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOrganizationPortfolioAccessInputPaginateTypeDef]
    ) -> AioPageIterator[ListOrganizationPortfolioAccessOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListOrganizationPortfolioAccess.html#ServiceCatalog.Paginator.ListOrganizationPortfolioAccess.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listorganizationportfolioaccesspaginator)
        """


if TYPE_CHECKING:
    _ListPortfoliosForProductPaginatorBase = AioPaginator[ListPortfoliosForProductOutputTypeDef]
else:
    _ListPortfoliosForProductPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPortfoliosForProductPaginator(_ListPortfoliosForProductPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListPortfoliosForProduct.html#ServiceCatalog.Paginator.ListPortfoliosForProduct)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listportfoliosforproductpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPortfoliosForProductInputPaginateTypeDef]
    ) -> AioPageIterator[ListPortfoliosForProductOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListPortfoliosForProduct.html#ServiceCatalog.Paginator.ListPortfoliosForProduct.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listportfoliosforproductpaginator)
        """


if TYPE_CHECKING:
    _ListPortfoliosPaginatorBase = AioPaginator[ListPortfoliosOutputTypeDef]
else:
    _ListPortfoliosPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPortfoliosPaginator(_ListPortfoliosPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListPortfolios.html#ServiceCatalog.Paginator.ListPortfolios)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listportfoliospaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPortfoliosInputPaginateTypeDef]
    ) -> AioPageIterator[ListPortfoliosOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListPortfolios.html#ServiceCatalog.Paginator.ListPortfolios.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listportfoliospaginator)
        """


if TYPE_CHECKING:
    _ListPrincipalsForPortfolioPaginatorBase = AioPaginator[ListPrincipalsForPortfolioOutputTypeDef]
else:
    _ListPrincipalsForPortfolioPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPrincipalsForPortfolioPaginator(_ListPrincipalsForPortfolioPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListPrincipalsForPortfolio.html#ServiceCatalog.Paginator.ListPrincipalsForPortfolio)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listprincipalsforportfoliopaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPrincipalsForPortfolioInputPaginateTypeDef]
    ) -> AioPageIterator[ListPrincipalsForPortfolioOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListPrincipalsForPortfolio.html#ServiceCatalog.Paginator.ListPrincipalsForPortfolio.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listprincipalsforportfoliopaginator)
        """


if TYPE_CHECKING:
    _ListProvisionedProductPlansPaginatorBase = AioPaginator[
        ListProvisionedProductPlansOutputTypeDef
    ]
else:
    _ListProvisionedProductPlansPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListProvisionedProductPlansPaginator(_ListProvisionedProductPlansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListProvisionedProductPlans.html#ServiceCatalog.Paginator.ListProvisionedProductPlans)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listprovisionedproductplanspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProvisionedProductPlansInputPaginateTypeDef]
    ) -> AioPageIterator[ListProvisionedProductPlansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListProvisionedProductPlans.html#ServiceCatalog.Paginator.ListProvisionedProductPlans.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listprovisionedproductplanspaginator)
        """


if TYPE_CHECKING:
    _ListProvisioningArtifactsForServiceActionPaginatorBase = AioPaginator[
        ListProvisioningArtifactsForServiceActionOutputTypeDef
    ]
else:
    _ListProvisioningArtifactsForServiceActionPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListProvisioningArtifactsForServiceActionPaginator(
    _ListProvisioningArtifactsForServiceActionPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListProvisioningArtifactsForServiceAction.html#ServiceCatalog.Paginator.ListProvisioningArtifactsForServiceAction)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listprovisioningartifactsforserviceactionpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProvisioningArtifactsForServiceActionInputPaginateTypeDef]
    ) -> AioPageIterator[ListProvisioningArtifactsForServiceActionOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListProvisioningArtifactsForServiceAction.html#ServiceCatalog.Paginator.ListProvisioningArtifactsForServiceAction.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listprovisioningartifactsforserviceactionpaginator)
        """


if TYPE_CHECKING:
    _ListRecordHistoryPaginatorBase = AioPaginator[ListRecordHistoryOutputTypeDef]
else:
    _ListRecordHistoryPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRecordHistoryPaginator(_ListRecordHistoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListRecordHistory.html#ServiceCatalog.Paginator.ListRecordHistory)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listrecordhistorypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecordHistoryInputPaginateTypeDef]
    ) -> AioPageIterator[ListRecordHistoryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListRecordHistory.html#ServiceCatalog.Paginator.ListRecordHistory.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listrecordhistorypaginator)
        """


if TYPE_CHECKING:
    _ListResourcesForTagOptionPaginatorBase = AioPaginator[ListResourcesForTagOptionOutputTypeDef]
else:
    _ListResourcesForTagOptionPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourcesForTagOptionPaginator(_ListResourcesForTagOptionPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListResourcesForTagOption.html#ServiceCatalog.Paginator.ListResourcesForTagOption)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listresourcesfortagoptionpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourcesForTagOptionInputPaginateTypeDef]
    ) -> AioPageIterator[ListResourcesForTagOptionOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListResourcesForTagOption.html#ServiceCatalog.Paginator.ListResourcesForTagOption.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listresourcesfortagoptionpaginator)
        """


if TYPE_CHECKING:
    _ListServiceActionsForProvisioningArtifactPaginatorBase = AioPaginator[
        ListServiceActionsForProvisioningArtifactOutputTypeDef
    ]
else:
    _ListServiceActionsForProvisioningArtifactPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListServiceActionsForProvisioningArtifactPaginator(
    _ListServiceActionsForProvisioningArtifactPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListServiceActionsForProvisioningArtifact.html#ServiceCatalog.Paginator.ListServiceActionsForProvisioningArtifact)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listserviceactionsforprovisioningartifactpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceActionsForProvisioningArtifactInputPaginateTypeDef]
    ) -> AioPageIterator[ListServiceActionsForProvisioningArtifactOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListServiceActionsForProvisioningArtifact.html#ServiceCatalog.Paginator.ListServiceActionsForProvisioningArtifact.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listserviceactionsforprovisioningartifactpaginator)
        """


if TYPE_CHECKING:
    _ListServiceActionsPaginatorBase = AioPaginator[ListServiceActionsOutputTypeDef]
else:
    _ListServiceActionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListServiceActionsPaginator(_ListServiceActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListServiceActions.html#ServiceCatalog.Paginator.ListServiceActions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listserviceactionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceActionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListServiceActionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListServiceActions.html#ServiceCatalog.Paginator.ListServiceActions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listserviceactionspaginator)
        """


if TYPE_CHECKING:
    _ListTagOptionsPaginatorBase = AioPaginator[ListTagOptionsOutputTypeDef]
else:
    _ListTagOptionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTagOptionsPaginator(_ListTagOptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListTagOptions.html#ServiceCatalog.Paginator.ListTagOptions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listtagoptionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagOptionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListTagOptionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ListTagOptions.html#ServiceCatalog.Paginator.ListTagOptions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#listtagoptionspaginator)
        """


if TYPE_CHECKING:
    _ScanProvisionedProductsPaginatorBase = AioPaginator[ScanProvisionedProductsOutputTypeDef]
else:
    _ScanProvisionedProductsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ScanProvisionedProductsPaginator(_ScanProvisionedProductsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ScanProvisionedProducts.html#ServiceCatalog.Paginator.ScanProvisionedProducts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#scanprovisionedproductspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ScanProvisionedProductsInputPaginateTypeDef]
    ) -> AioPageIterator[ScanProvisionedProductsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/ScanProvisionedProducts.html#ServiceCatalog.Paginator.ScanProvisionedProducts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#scanprovisionedproductspaginator)
        """


if TYPE_CHECKING:
    _SearchProductsAsAdminPaginatorBase = AioPaginator[SearchProductsAsAdminOutputTypeDef]
else:
    _SearchProductsAsAdminPaginatorBase = AioPaginator  # type: ignore[assignment]


class SearchProductsAsAdminPaginator(_SearchProductsAsAdminPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/SearchProductsAsAdmin.html#ServiceCatalog.Paginator.SearchProductsAsAdmin)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#searchproductsasadminpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchProductsAsAdminInputPaginateTypeDef]
    ) -> AioPageIterator[SearchProductsAsAdminOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/servicecatalog/paginator/SearchProductsAsAdmin.html#ServiceCatalog.Paginator.SearchProductsAsAdmin.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_servicecatalog/paginators/#searchproductsasadminpaginator)
        """
