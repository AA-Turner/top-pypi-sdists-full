"""
Type annotations for cleanroomsml service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cleanroomsml.client import CleanRoomsMLClient
    from types_aiobotocore_cleanroomsml.paginator import (
        ListAudienceExportJobsPaginator,
        ListAudienceGenerationJobsPaginator,
        ListAudienceModelsPaginator,
        ListCollaborationConfiguredModelAlgorithmAssociationsPaginator,
        ListCollaborationMLInputChannelsPaginator,
        ListCollaborationTrainedModelExportJobsPaginator,
        ListCollaborationTrainedModelInferenceJobsPaginator,
        ListCollaborationTrainedModelsPaginator,
        ListConfiguredAudienceModelsPaginator,
        ListConfiguredModelAlgorithmAssociationsPaginator,
        ListConfiguredModelAlgorithmsPaginator,
        ListMLInputChannelsPaginator,
        ListTrainedModelInferenceJobsPaginator,
        ListTrainedModelVersionsPaginator,
        ListTrainedModelsPaginator,
        ListTrainingDatasetsPaginator,
    )

    session = get_session()
    with session.create_client("cleanroomsml") as client:
        client: CleanRoomsMLClient

        list_audience_export_jobs_paginator: ListAudienceExportJobsPaginator = client.get_paginator("list_audience_export_jobs")
        list_audience_generation_jobs_paginator: ListAudienceGenerationJobsPaginator = client.get_paginator("list_audience_generation_jobs")
        list_audience_models_paginator: ListAudienceModelsPaginator = client.get_paginator("list_audience_models")
        list_collaboration_configured_model_algorithm_associations_paginator: ListCollaborationConfiguredModelAlgorithmAssociationsPaginator = client.get_paginator("list_collaboration_configured_model_algorithm_associations")
        list_collaboration_ml_input_channels_paginator: ListCollaborationMLInputChannelsPaginator = client.get_paginator("list_collaboration_ml_input_channels")
        list_collaboration_trained_model_export_jobs_paginator: ListCollaborationTrainedModelExportJobsPaginator = client.get_paginator("list_collaboration_trained_model_export_jobs")
        list_collaboration_trained_model_inference_jobs_paginator: ListCollaborationTrainedModelInferenceJobsPaginator = client.get_paginator("list_collaboration_trained_model_inference_jobs")
        list_collaboration_trained_models_paginator: ListCollaborationTrainedModelsPaginator = client.get_paginator("list_collaboration_trained_models")
        list_configured_audience_models_paginator: ListConfiguredAudienceModelsPaginator = client.get_paginator("list_configured_audience_models")
        list_configured_model_algorithm_associations_paginator: ListConfiguredModelAlgorithmAssociationsPaginator = client.get_paginator("list_configured_model_algorithm_associations")
        list_configured_model_algorithms_paginator: ListConfiguredModelAlgorithmsPaginator = client.get_paginator("list_configured_model_algorithms")
        list_ml_input_channels_paginator: ListMLInputChannelsPaginator = client.get_paginator("list_ml_input_channels")
        list_trained_model_inference_jobs_paginator: ListTrainedModelInferenceJobsPaginator = client.get_paginator("list_trained_model_inference_jobs")
        list_trained_model_versions_paginator: ListTrainedModelVersionsPaginator = client.get_paginator("list_trained_model_versions")
        list_trained_models_paginator: ListTrainedModelsPaginator = client.get_paginator("list_trained_models")
        list_training_datasets_paginator: ListTrainingDatasetsPaginator = client.get_paginator("list_training_datasets")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAudienceExportJobsRequestPaginateTypeDef,
    ListAudienceExportJobsResponseTypeDef,
    ListAudienceGenerationJobsRequestPaginateTypeDef,
    ListAudienceGenerationJobsResponseTypeDef,
    ListAudienceModelsRequestPaginateTypeDef,
    ListAudienceModelsResponseTypeDef,
    ListCollaborationConfiguredModelAlgorithmAssociationsRequestPaginateTypeDef,
    ListCollaborationConfiguredModelAlgorithmAssociationsResponseTypeDef,
    ListCollaborationMLInputChannelsRequestPaginateTypeDef,
    ListCollaborationMLInputChannelsResponseTypeDef,
    ListCollaborationTrainedModelExportJobsRequestPaginateTypeDef,
    ListCollaborationTrainedModelExportJobsResponseTypeDef,
    ListCollaborationTrainedModelInferenceJobsRequestPaginateTypeDef,
    ListCollaborationTrainedModelInferenceJobsResponseTypeDef,
    ListCollaborationTrainedModelsRequestPaginateTypeDef,
    ListCollaborationTrainedModelsResponseTypeDef,
    ListConfiguredAudienceModelsRequestPaginateTypeDef,
    ListConfiguredAudienceModelsResponseTypeDef,
    ListConfiguredModelAlgorithmAssociationsRequestPaginateTypeDef,
    ListConfiguredModelAlgorithmAssociationsResponseTypeDef,
    ListConfiguredModelAlgorithmsRequestPaginateTypeDef,
    ListConfiguredModelAlgorithmsResponseTypeDef,
    ListMLInputChannelsRequestPaginateTypeDef,
    ListMLInputChannelsResponseTypeDef,
    ListTrainedModelInferenceJobsRequestPaginateTypeDef,
    ListTrainedModelInferenceJobsResponseTypeDef,
    ListTrainedModelsRequestPaginateTypeDef,
    ListTrainedModelsResponseTypeDef,
    ListTrainedModelVersionsRequestPaginateTypeDef,
    ListTrainedModelVersionsResponseTypeDef,
    ListTrainingDatasetsRequestPaginateTypeDef,
    ListTrainingDatasetsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAudienceExportJobsPaginator",
    "ListAudienceGenerationJobsPaginator",
    "ListAudienceModelsPaginator",
    "ListCollaborationConfiguredModelAlgorithmAssociationsPaginator",
    "ListCollaborationMLInputChannelsPaginator",
    "ListCollaborationTrainedModelExportJobsPaginator",
    "ListCollaborationTrainedModelInferenceJobsPaginator",
    "ListCollaborationTrainedModelsPaginator",
    "ListConfiguredAudienceModelsPaginator",
    "ListConfiguredModelAlgorithmAssociationsPaginator",
    "ListConfiguredModelAlgorithmsPaginator",
    "ListMLInputChannelsPaginator",
    "ListTrainedModelInferenceJobsPaginator",
    "ListTrainedModelVersionsPaginator",
    "ListTrainedModelsPaginator",
    "ListTrainingDatasetsPaginator",
)

if TYPE_CHECKING:
    _ListAudienceExportJobsPaginatorBase = AioPaginator[ListAudienceExportJobsResponseTypeDef]
else:
    _ListAudienceExportJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAudienceExportJobsPaginator(_ListAudienceExportJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListAudienceExportJobs.html#CleanRoomsML.Paginator.ListAudienceExportJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listaudienceexportjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAudienceExportJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAudienceExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListAudienceExportJobs.html#CleanRoomsML.Paginator.ListAudienceExportJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listaudienceexportjobspaginator)
        """

if TYPE_CHECKING:
    _ListAudienceGenerationJobsPaginatorBase = AioPaginator[
        ListAudienceGenerationJobsResponseTypeDef
    ]
else:
    _ListAudienceGenerationJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAudienceGenerationJobsPaginator(_ListAudienceGenerationJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListAudienceGenerationJobs.html#CleanRoomsML.Paginator.ListAudienceGenerationJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listaudiencegenerationjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAudienceGenerationJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAudienceGenerationJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListAudienceGenerationJobs.html#CleanRoomsML.Paginator.ListAudienceGenerationJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listaudiencegenerationjobspaginator)
        """

if TYPE_CHECKING:
    _ListAudienceModelsPaginatorBase = AioPaginator[ListAudienceModelsResponseTypeDef]
else:
    _ListAudienceModelsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAudienceModelsPaginator(_ListAudienceModelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListAudienceModels.html#CleanRoomsML.Paginator.ListAudienceModels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listaudiencemodelspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAudienceModelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAudienceModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListAudienceModels.html#CleanRoomsML.Paginator.ListAudienceModels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listaudiencemodelspaginator)
        """

if TYPE_CHECKING:
    _ListCollaborationConfiguredModelAlgorithmAssociationsPaginatorBase = AioPaginator[
        ListCollaborationConfiguredModelAlgorithmAssociationsResponseTypeDef
    ]
else:
    _ListCollaborationConfiguredModelAlgorithmAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCollaborationConfiguredModelAlgorithmAssociationsPaginator(
    _ListCollaborationConfiguredModelAlgorithmAssociationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationConfiguredModelAlgorithmAssociations.html#CleanRoomsML.Paginator.ListCollaborationConfiguredModelAlgorithmAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listcollaborationconfiguredmodelalgorithmassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self,
        **kwargs: Unpack[
            ListCollaborationConfiguredModelAlgorithmAssociationsRequestPaginateTypeDef
        ],
    ) -> AioPageIterator[ListCollaborationConfiguredModelAlgorithmAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationConfiguredModelAlgorithmAssociations.html#CleanRoomsML.Paginator.ListCollaborationConfiguredModelAlgorithmAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listcollaborationconfiguredmodelalgorithmassociationspaginator)
        """

if TYPE_CHECKING:
    _ListCollaborationMLInputChannelsPaginatorBase = AioPaginator[
        ListCollaborationMLInputChannelsResponseTypeDef
    ]
else:
    _ListCollaborationMLInputChannelsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCollaborationMLInputChannelsPaginator(_ListCollaborationMLInputChannelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationMLInputChannels.html#CleanRoomsML.Paginator.ListCollaborationMLInputChannels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listcollaborationmlinputchannelspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCollaborationMLInputChannelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCollaborationMLInputChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationMLInputChannels.html#CleanRoomsML.Paginator.ListCollaborationMLInputChannels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listcollaborationmlinputchannelspaginator)
        """

if TYPE_CHECKING:
    _ListCollaborationTrainedModelExportJobsPaginatorBase = AioPaginator[
        ListCollaborationTrainedModelExportJobsResponseTypeDef
    ]
else:
    _ListCollaborationTrainedModelExportJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCollaborationTrainedModelExportJobsPaginator(
    _ListCollaborationTrainedModelExportJobsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationTrainedModelExportJobs.html#CleanRoomsML.Paginator.ListCollaborationTrainedModelExportJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listcollaborationtrainedmodelexportjobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCollaborationTrainedModelExportJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCollaborationTrainedModelExportJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationTrainedModelExportJobs.html#CleanRoomsML.Paginator.ListCollaborationTrainedModelExportJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listcollaborationtrainedmodelexportjobspaginator)
        """

if TYPE_CHECKING:
    _ListCollaborationTrainedModelInferenceJobsPaginatorBase = AioPaginator[
        ListCollaborationTrainedModelInferenceJobsResponseTypeDef
    ]
else:
    _ListCollaborationTrainedModelInferenceJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCollaborationTrainedModelInferenceJobsPaginator(
    _ListCollaborationTrainedModelInferenceJobsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationTrainedModelInferenceJobs.html#CleanRoomsML.Paginator.ListCollaborationTrainedModelInferenceJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listcollaborationtrainedmodelinferencejobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCollaborationTrainedModelInferenceJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCollaborationTrainedModelInferenceJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationTrainedModelInferenceJobs.html#CleanRoomsML.Paginator.ListCollaborationTrainedModelInferenceJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listcollaborationtrainedmodelinferencejobspaginator)
        """

if TYPE_CHECKING:
    _ListCollaborationTrainedModelsPaginatorBase = AioPaginator[
        ListCollaborationTrainedModelsResponseTypeDef
    ]
else:
    _ListCollaborationTrainedModelsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCollaborationTrainedModelsPaginator(_ListCollaborationTrainedModelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationTrainedModels.html#CleanRoomsML.Paginator.ListCollaborationTrainedModels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listcollaborationtrainedmodelspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCollaborationTrainedModelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCollaborationTrainedModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListCollaborationTrainedModels.html#CleanRoomsML.Paginator.ListCollaborationTrainedModels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listcollaborationtrainedmodelspaginator)
        """

if TYPE_CHECKING:
    _ListConfiguredAudienceModelsPaginatorBase = AioPaginator[
        ListConfiguredAudienceModelsResponseTypeDef
    ]
else:
    _ListConfiguredAudienceModelsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListConfiguredAudienceModelsPaginator(_ListConfiguredAudienceModelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListConfiguredAudienceModels.html#CleanRoomsML.Paginator.ListConfiguredAudienceModels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listconfiguredaudiencemodelspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConfiguredAudienceModelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConfiguredAudienceModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListConfiguredAudienceModels.html#CleanRoomsML.Paginator.ListConfiguredAudienceModels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listconfiguredaudiencemodelspaginator)
        """

if TYPE_CHECKING:
    _ListConfiguredModelAlgorithmAssociationsPaginatorBase = AioPaginator[
        ListConfiguredModelAlgorithmAssociationsResponseTypeDef
    ]
else:
    _ListConfiguredModelAlgorithmAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListConfiguredModelAlgorithmAssociationsPaginator(
    _ListConfiguredModelAlgorithmAssociationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListConfiguredModelAlgorithmAssociations.html#CleanRoomsML.Paginator.ListConfiguredModelAlgorithmAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listconfiguredmodelalgorithmassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConfiguredModelAlgorithmAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConfiguredModelAlgorithmAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListConfiguredModelAlgorithmAssociations.html#CleanRoomsML.Paginator.ListConfiguredModelAlgorithmAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listconfiguredmodelalgorithmassociationspaginator)
        """

if TYPE_CHECKING:
    _ListConfiguredModelAlgorithmsPaginatorBase = AioPaginator[
        ListConfiguredModelAlgorithmsResponseTypeDef
    ]
else:
    _ListConfiguredModelAlgorithmsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListConfiguredModelAlgorithmsPaginator(_ListConfiguredModelAlgorithmsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListConfiguredModelAlgorithms.html#CleanRoomsML.Paginator.ListConfiguredModelAlgorithms)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listconfiguredmodelalgorithmspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConfiguredModelAlgorithmsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConfiguredModelAlgorithmsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListConfiguredModelAlgorithms.html#CleanRoomsML.Paginator.ListConfiguredModelAlgorithms.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listconfiguredmodelalgorithmspaginator)
        """

if TYPE_CHECKING:
    _ListMLInputChannelsPaginatorBase = AioPaginator[ListMLInputChannelsResponseTypeDef]
else:
    _ListMLInputChannelsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMLInputChannelsPaginator(_ListMLInputChannelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListMLInputChannels.html#CleanRoomsML.Paginator.ListMLInputChannels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listmlinputchannelspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMLInputChannelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMLInputChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListMLInputChannels.html#CleanRoomsML.Paginator.ListMLInputChannels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listmlinputchannelspaginator)
        """

if TYPE_CHECKING:
    _ListTrainedModelInferenceJobsPaginatorBase = AioPaginator[
        ListTrainedModelInferenceJobsResponseTypeDef
    ]
else:
    _ListTrainedModelInferenceJobsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTrainedModelInferenceJobsPaginator(_ListTrainedModelInferenceJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListTrainedModelInferenceJobs.html#CleanRoomsML.Paginator.ListTrainedModelInferenceJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listtrainedmodelinferencejobspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrainedModelInferenceJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTrainedModelInferenceJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListTrainedModelInferenceJobs.html#CleanRoomsML.Paginator.ListTrainedModelInferenceJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listtrainedmodelinferencejobspaginator)
        """

if TYPE_CHECKING:
    _ListTrainedModelVersionsPaginatorBase = AioPaginator[ListTrainedModelVersionsResponseTypeDef]
else:
    _ListTrainedModelVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTrainedModelVersionsPaginator(_ListTrainedModelVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListTrainedModelVersions.html#CleanRoomsML.Paginator.ListTrainedModelVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listtrainedmodelversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrainedModelVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTrainedModelVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListTrainedModelVersions.html#CleanRoomsML.Paginator.ListTrainedModelVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listtrainedmodelversionspaginator)
        """

if TYPE_CHECKING:
    _ListTrainedModelsPaginatorBase = AioPaginator[ListTrainedModelsResponseTypeDef]
else:
    _ListTrainedModelsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTrainedModelsPaginator(_ListTrainedModelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListTrainedModels.html#CleanRoomsML.Paginator.ListTrainedModels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listtrainedmodelspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrainedModelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTrainedModelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListTrainedModels.html#CleanRoomsML.Paginator.ListTrainedModels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listtrainedmodelspaginator)
        """

if TYPE_CHECKING:
    _ListTrainingDatasetsPaginatorBase = AioPaginator[ListTrainingDatasetsResponseTypeDef]
else:
    _ListTrainingDatasetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTrainingDatasetsPaginator(_ListTrainingDatasetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListTrainingDatasets.html#CleanRoomsML.Paginator.ListTrainingDatasets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listtrainingdatasetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrainingDatasetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTrainingDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cleanroomsml/paginator/ListTrainingDatasets.html#CleanRoomsML.Paginator.ListTrainingDatasets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cleanroomsml/paginators/#listtrainingdatasetspaginator)
        """
