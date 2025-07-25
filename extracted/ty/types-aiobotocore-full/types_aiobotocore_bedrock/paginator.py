"""
Type annotations for bedrock service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_bedrock.client import BedrockClient
    from types_aiobotocore_bedrock.paginator import (
        ListCustomModelDeploymentsPaginator,
        ListCustomModelsPaginator,
        ListEvaluationJobsPaginator,
        ListGuardrailsPaginator,
        ListImportedModelsPaginator,
        ListInferenceProfilesPaginator,
        ListMarketplaceModelEndpointsPaginator,
        ListModelCopyJobsPaginator,
        ListModelCustomizationJobsPaginator,
        ListModelImportJobsPaginator,
        ListModelInvocationJobsPaginator,
        ListPromptRoutersPaginator,
        ListProvisionedModelThroughputsPaginator,
    )

    session = get_session()
    with session.create_client("bedrock") as client:
        client: BedrockClient

        list_custom_model_deployments_paginator: ListCustomModelDeploymentsPaginator = client.get_paginator("list_custom_model_deployments")
        list_custom_models_paginator: ListCustomModelsPaginator = client.get_paginator("list_custom_models")
        list_evaluation_jobs_paginator: ListEvaluationJobsPaginator = client.get_paginator("list_evaluation_jobs")
        list_guardrails_paginator: ListGuardrailsPaginator = client.get_paginator("list_guardrails")
        list_imported_models_paginator: ListImportedModelsPaginator = client.get_paginator("list_imported_models")
        list_inference_profiles_paginator: ListInferenceProfilesPaginator = client.get_paginator("list_inference_profiles")
        list_marketplace_model_endpoints_paginator: ListMarketplaceModelEndpointsPaginator = client.get_paginator("list_marketplace_model_endpoints")
        list_model_copy_jobs_paginator: ListModelCopyJobsPaginator = client.get_paginator("list_model_copy_jobs")
        list_model_customization_jobs_paginator: ListModelCustomizationJobsPaginator = client.get_paginator("list_model_customization_jobs")
        list_model_import_jobs_paginator: ListModelImportJobsPaginator = client.get_paginator("list_model_import_jobs")
        list_model_invocation_jobs_paginator: ListModelInvocationJobsPaginator = client.get_paginator("list_model_invocation_jobs")
        list_prompt_routers_paginator: ListPromptRoutersPaginator = client.get_paginator("list_prompt_routers")
        list_provisioned_model_throughputs_paginator: ListProvisionedModelThroughputsPaginator = client.get_paginator("list_provisioned_model_throughputs")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListCustomModelDeploymentsRequestPaginateTypeDef,
    ListCustomModelDeploymentsResponseTypeDef,
    ListCustomModelsRequestPaginateTypeDef,
    ListCustomModelsResponseTypeDef,
    ListEvaluationJobsRequestPaginateTypeDef,
    ListEvaluationJobsResponseTypeDef,
    ListGuardrailsRequestPaginateTypeDef,
    ListGuardrailsResponseTypeDef,
    ListImportedModelsRequestPaginateTypeDef,
    ListImportedModelsResponseTypeDef,
    ListInferenceProfilesRequestPaginateTypeDef,
    ListInferenceProfilesResponseTypeDef,
    ListMarketplaceModelEndpointsRequestPaginateTypeDef,
    ListMarketplaceModelEndpointsResponseTypeDef,
    ListModelCopyJobsRequestPaginateTypeDef,
    ListModelCopyJobsResponseTypeDef,
    ListModelCustomizationJobsRequestPaginateTypeDef,
    ListModelCustomizationJobsResponseTypeDef,
    ListModelImportJobsRequestPaginateTypeDef,
    ListModelImportJobsResponseTypeDef,
    ListModelInvocationJobsRequestPaginateTypeDef,
    ListModelInvocationJobsResponseTypeDef,
    ListPromptRoutersRequestPaginateTypeDef,
    ListPromptRoutersResponseTypeDef,
    ListProvisionedModelThroughputsRequestPaginateTypeDef,
    ListProvisionedModelThroughputsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListCustomModelDeploymentsPaginator",
    "ListCustomModelsPaginator",
    "ListEvaluationJobsPaginator",
    "ListGuardrailsPaginator",
    "ListImportedModelsPaginator",
    "ListInferenceProfilesPaginator",
    "ListMarketplaceModelEndpointsPaginator",
    "ListModelCopyJobsPaginator",
    "ListModelCustomizationJobsPaginator",
    "ListModelImportJobsPaginator",
    "ListModelInvocationJobsPaginator",
    "ListPromptRoutersPaginator",
    "ListProvisionedModelThroughputsPaginator",
)


if TYPE_CHECKING:
    _ListCustomModelDeploymentsPaginatorBase = AioPaginator[
        ListCustomModelDeploymentsResponseTypeDef
    ]
else:
    _ListCustomModelDeploymentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCustomModelDeploymentsPaginator(_ListCustomModelDeploymentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListCustomModelDeployments.html#Bedrock.Paginator.ListCustomModelDeployments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listcustommodeldeploymentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomModelDeploymentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCustomModelDeploymentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListCustomModelDeployments.html#Bedrock.Paginator.ListCustomModelDeployments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listcustommodeldeploymentspaginator)
        """


if TYPE_CHECKING:
    _ListCustomModelsPaginatorBase = AioPaginator[ListCustomModelsResponseTypeDef]
else:
    _ListCustomModelsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCustomModelsPaginator(_ListCustomModelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListCustomModels.html#Bedrock.Paginator.ListCustomModels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listcustommodelspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomModelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCustomModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListCustomModels.html#Bedrock.Paginator.ListCustomModels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listcustommodelspaginator)
        """


if TYPE_CHECKING:
    _ListEvaluationJobsPaginatorBase = AioPaginator[ListEvaluationJobsResponseTypeDef]
else:
    _ListEvaluationJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEvaluationJobsPaginator(_ListEvaluationJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListEvaluationJobs.html#Bedrock.Paginator.ListEvaluationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listevaluationjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEvaluationJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEvaluationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListEvaluationJobs.html#Bedrock.Paginator.ListEvaluationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listevaluationjobspaginator)
        """


if TYPE_CHECKING:
    _ListGuardrailsPaginatorBase = AioPaginator[ListGuardrailsResponseTypeDef]
else:
    _ListGuardrailsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListGuardrailsPaginator(_ListGuardrailsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListGuardrails.html#Bedrock.Paginator.ListGuardrails)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listguardrailspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGuardrailsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGuardrailsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListGuardrails.html#Bedrock.Paginator.ListGuardrails.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listguardrailspaginator)
        """


if TYPE_CHECKING:
    _ListImportedModelsPaginatorBase = AioPaginator[ListImportedModelsResponseTypeDef]
else:
    _ListImportedModelsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListImportedModelsPaginator(_ListImportedModelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListImportedModels.html#Bedrock.Paginator.ListImportedModels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listimportedmodelspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImportedModelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListImportedModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListImportedModels.html#Bedrock.Paginator.ListImportedModels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listimportedmodelspaginator)
        """


if TYPE_CHECKING:
    _ListInferenceProfilesPaginatorBase = AioPaginator[ListInferenceProfilesResponseTypeDef]
else:
    _ListInferenceProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListInferenceProfilesPaginator(_ListInferenceProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListInferenceProfiles.html#Bedrock.Paginator.ListInferenceProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listinferenceprofilespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInferenceProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInferenceProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListInferenceProfiles.html#Bedrock.Paginator.ListInferenceProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listinferenceprofilespaginator)
        """


if TYPE_CHECKING:
    _ListMarketplaceModelEndpointsPaginatorBase = AioPaginator[
        ListMarketplaceModelEndpointsResponseTypeDef
    ]
else:
    _ListMarketplaceModelEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListMarketplaceModelEndpointsPaginator(_ListMarketplaceModelEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListMarketplaceModelEndpoints.html#Bedrock.Paginator.ListMarketplaceModelEndpoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmarketplacemodelendpointspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMarketplaceModelEndpointsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMarketplaceModelEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListMarketplaceModelEndpoints.html#Bedrock.Paginator.ListMarketplaceModelEndpoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmarketplacemodelendpointspaginator)
        """


if TYPE_CHECKING:
    _ListModelCopyJobsPaginatorBase = AioPaginator[ListModelCopyJobsResponseTypeDef]
else:
    _ListModelCopyJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListModelCopyJobsPaginator(_ListModelCopyJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelCopyJobs.html#Bedrock.Paginator.ListModelCopyJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmodelcopyjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelCopyJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListModelCopyJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelCopyJobs.html#Bedrock.Paginator.ListModelCopyJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmodelcopyjobspaginator)
        """


if TYPE_CHECKING:
    _ListModelCustomizationJobsPaginatorBase = AioPaginator[
        ListModelCustomizationJobsResponseTypeDef
    ]
else:
    _ListModelCustomizationJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListModelCustomizationJobsPaginator(_ListModelCustomizationJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelCustomizationJobs.html#Bedrock.Paginator.ListModelCustomizationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmodelcustomizationjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelCustomizationJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListModelCustomizationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelCustomizationJobs.html#Bedrock.Paginator.ListModelCustomizationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmodelcustomizationjobspaginator)
        """


if TYPE_CHECKING:
    _ListModelImportJobsPaginatorBase = AioPaginator[ListModelImportJobsResponseTypeDef]
else:
    _ListModelImportJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListModelImportJobsPaginator(_ListModelImportJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelImportJobs.html#Bedrock.Paginator.ListModelImportJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmodelimportjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelImportJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListModelImportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelImportJobs.html#Bedrock.Paginator.ListModelImportJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmodelimportjobspaginator)
        """


if TYPE_CHECKING:
    _ListModelInvocationJobsPaginatorBase = AioPaginator[ListModelInvocationJobsResponseTypeDef]
else:
    _ListModelInvocationJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListModelInvocationJobsPaginator(_ListModelInvocationJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelInvocationJobs.html#Bedrock.Paginator.ListModelInvocationJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmodelinvocationjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListModelInvocationJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListModelInvocationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListModelInvocationJobs.html#Bedrock.Paginator.ListModelInvocationJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listmodelinvocationjobspaginator)
        """


if TYPE_CHECKING:
    _ListPromptRoutersPaginatorBase = AioPaginator[ListPromptRoutersResponseTypeDef]
else:
    _ListPromptRoutersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPromptRoutersPaginator(_ListPromptRoutersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListPromptRouters.html#Bedrock.Paginator.ListPromptRouters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listpromptrouterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPromptRoutersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPromptRoutersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListPromptRouters.html#Bedrock.Paginator.ListPromptRouters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listpromptrouterspaginator)
        """


if TYPE_CHECKING:
    _ListProvisionedModelThroughputsPaginatorBase = AioPaginator[
        ListProvisionedModelThroughputsResponseTypeDef
    ]
else:
    _ListProvisionedModelThroughputsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListProvisionedModelThroughputsPaginator(_ListProvisionedModelThroughputsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListProvisionedModelThroughputs.html#Bedrock.Paginator.ListProvisionedModelThroughputs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listprovisionedmodelthroughputspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProvisionedModelThroughputsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProvisionedModelThroughputsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock/paginator/ListProvisionedModelThroughputs.html#Bedrock.Paginator.ListProvisionedModelThroughputs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock/paginators/#listprovisionedmodelthroughputspaginator)
        """
