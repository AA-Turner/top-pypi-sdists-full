"""
Type annotations for comprehendmedical service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_comprehendmedical.client import ComprehendMedicalClient

    session = get_session()
    async with session.create_client("comprehendmedical") as client:
        client: ComprehendMedicalClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    DescribeEntitiesDetectionV2JobRequestTypeDef,
    DescribeEntitiesDetectionV2JobResponseTypeDef,
    DescribeICD10CMInferenceJobRequestTypeDef,
    DescribeICD10CMInferenceJobResponseTypeDef,
    DescribePHIDetectionJobRequestTypeDef,
    DescribePHIDetectionJobResponseTypeDef,
    DescribeRxNormInferenceJobRequestTypeDef,
    DescribeRxNormInferenceJobResponseTypeDef,
    DescribeSNOMEDCTInferenceJobRequestTypeDef,
    DescribeSNOMEDCTInferenceJobResponseTypeDef,
    DetectEntitiesRequestTypeDef,
    DetectEntitiesResponseTypeDef,
    DetectEntitiesV2RequestTypeDef,
    DetectEntitiesV2ResponseTypeDef,
    DetectPHIRequestTypeDef,
    DetectPHIResponseTypeDef,
    InferICD10CMRequestTypeDef,
    InferICD10CMResponseTypeDef,
    InferRxNormRequestTypeDef,
    InferRxNormResponseTypeDef,
    InferSNOMEDCTRequestTypeDef,
    InferSNOMEDCTResponseTypeDef,
    ListEntitiesDetectionV2JobsRequestTypeDef,
    ListEntitiesDetectionV2JobsResponseTypeDef,
    ListICD10CMInferenceJobsRequestTypeDef,
    ListICD10CMInferenceJobsResponseTypeDef,
    ListPHIDetectionJobsRequestTypeDef,
    ListPHIDetectionJobsResponseTypeDef,
    ListRxNormInferenceJobsRequestTypeDef,
    ListRxNormInferenceJobsResponseTypeDef,
    ListSNOMEDCTInferenceJobsRequestTypeDef,
    ListSNOMEDCTInferenceJobsResponseTypeDef,
    StartEntitiesDetectionV2JobRequestTypeDef,
    StartEntitiesDetectionV2JobResponseTypeDef,
    StartICD10CMInferenceJobRequestTypeDef,
    StartICD10CMInferenceJobResponseTypeDef,
    StartPHIDetectionJobRequestTypeDef,
    StartPHIDetectionJobResponseTypeDef,
    StartRxNormInferenceJobRequestTypeDef,
    StartRxNormInferenceJobResponseTypeDef,
    StartSNOMEDCTInferenceJobRequestTypeDef,
    StartSNOMEDCTInferenceJobResponseTypeDef,
    StopEntitiesDetectionV2JobRequestTypeDef,
    StopEntitiesDetectionV2JobResponseTypeDef,
    StopICD10CMInferenceJobRequestTypeDef,
    StopICD10CMInferenceJobResponseTypeDef,
    StopPHIDetectionJobRequestTypeDef,
    StopPHIDetectionJobResponseTypeDef,
    StopRxNormInferenceJobRequestTypeDef,
    StopRxNormInferenceJobResponseTypeDef,
    StopSNOMEDCTInferenceJobRequestTypeDef,
    StopSNOMEDCTInferenceJobResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack


__all__ = ("ComprehendMedicalClient",)


class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidEncodingException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    TextSizeLimitExceededException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class ComprehendMedicalClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ComprehendMedicalClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#generate_presigned_url)
        """

    async def describe_entities_detection_v2_job(
        self, **kwargs: Unpack[DescribeEntitiesDetectionV2JobRequestTypeDef]
    ) -> DescribeEntitiesDetectionV2JobResponseTypeDef:
        """
        Gets the properties associated with a medical entities detection job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/describe_entities_detection_v2_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#describe_entities_detection_v2_job)
        """

    async def describe_icd10_cm_inference_job(
        self, **kwargs: Unpack[DescribeICD10CMInferenceJobRequestTypeDef]
    ) -> DescribeICD10CMInferenceJobResponseTypeDef:
        """
        Gets the properties associated with an InferICD10CM job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/describe_icd10_cm_inference_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#describe_icd10_cm_inference_job)
        """

    async def describe_phi_detection_job(
        self, **kwargs: Unpack[DescribePHIDetectionJobRequestTypeDef]
    ) -> DescribePHIDetectionJobResponseTypeDef:
        """
        Gets the properties associated with a protected health information (PHI)
        detection job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/describe_phi_detection_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#describe_phi_detection_job)
        """

    async def describe_rx_norm_inference_job(
        self, **kwargs: Unpack[DescribeRxNormInferenceJobRequestTypeDef]
    ) -> DescribeRxNormInferenceJobResponseTypeDef:
        """
        Gets the properties associated with an InferRxNorm job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/describe_rx_norm_inference_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#describe_rx_norm_inference_job)
        """

    async def describe_snomedct_inference_job(
        self, **kwargs: Unpack[DescribeSNOMEDCTInferenceJobRequestTypeDef]
    ) -> DescribeSNOMEDCTInferenceJobResponseTypeDef:
        """
        Gets the properties associated with an InferSNOMEDCT job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/describe_snomedct_inference_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#describe_snomedct_inference_job)
        """

    async def detect_entities(
        self, **kwargs: Unpack[DetectEntitiesRequestTypeDef]
    ) -> DetectEntitiesResponseTypeDef:
        """
        The <code>DetectEntities</code> operation is deprecated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/detect_entities.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#detect_entities)
        """

    async def detect_entities_v2(
        self, **kwargs: Unpack[DetectEntitiesV2RequestTypeDef]
    ) -> DetectEntitiesV2ResponseTypeDef:
        """
        Inspects the clinical text for a variety of medical entities and returns
        specific information about them such as entity category, location, and
        confidence score on that information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/detect_entities_v2.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#detect_entities_v2)
        """

    async def detect_phi(
        self, **kwargs: Unpack[DetectPHIRequestTypeDef]
    ) -> DetectPHIResponseTypeDef:
        """
        Inspects the clinical text for protected health information (PHI) entities and
        returns the entity category, location, and confidence score for each entity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/detect_phi.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#detect_phi)
        """

    async def infer_icd10_cm(
        self, **kwargs: Unpack[InferICD10CMRequestTypeDef]
    ) -> InferICD10CMResponseTypeDef:
        """
        InferICD10CM detects medical conditions as entities listed in a patient record
        and links those entities to normalized concept identifiers in the ICD-10-CM
        knowledge base from the Centers for Disease Control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/infer_icd10_cm.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#infer_icd10_cm)
        """

    async def infer_rx_norm(
        self, **kwargs: Unpack[InferRxNormRequestTypeDef]
    ) -> InferRxNormResponseTypeDef:
        """
        InferRxNorm detects medications as entities listed in a patient record and
        links to the normalized concept identifiers in the RxNorm database from the
        National Library of Medicine.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/infer_rx_norm.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#infer_rx_norm)
        """

    async def infer_snomedct(
        self, **kwargs: Unpack[InferSNOMEDCTRequestTypeDef]
    ) -> InferSNOMEDCTResponseTypeDef:
        """
        InferSNOMEDCT detects possible medical concepts as entities and links them to
        codes from the Systematized Nomenclature of Medicine, Clinical Terms
        (SNOMED-CT) ontology.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/infer_snomedct.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#infer_snomedct)
        """

    async def list_entities_detection_v2_jobs(
        self, **kwargs: Unpack[ListEntitiesDetectionV2JobsRequestTypeDef]
    ) -> ListEntitiesDetectionV2JobsResponseTypeDef:
        """
        Gets a list of medical entity detection jobs that you have submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/list_entities_detection_v2_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#list_entities_detection_v2_jobs)
        """

    async def list_icd10_cm_inference_jobs(
        self, **kwargs: Unpack[ListICD10CMInferenceJobsRequestTypeDef]
    ) -> ListICD10CMInferenceJobsResponseTypeDef:
        """
        Gets a list of InferICD10CM jobs that you have submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/list_icd10_cm_inference_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#list_icd10_cm_inference_jobs)
        """

    async def list_phi_detection_jobs(
        self, **kwargs: Unpack[ListPHIDetectionJobsRequestTypeDef]
    ) -> ListPHIDetectionJobsResponseTypeDef:
        """
        Gets a list of protected health information (PHI) detection jobs you have
        submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/list_phi_detection_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#list_phi_detection_jobs)
        """

    async def list_rx_norm_inference_jobs(
        self, **kwargs: Unpack[ListRxNormInferenceJobsRequestTypeDef]
    ) -> ListRxNormInferenceJobsResponseTypeDef:
        """
        Gets a list of InferRxNorm jobs that you have submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/list_rx_norm_inference_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#list_rx_norm_inference_jobs)
        """

    async def list_snomedct_inference_jobs(
        self, **kwargs: Unpack[ListSNOMEDCTInferenceJobsRequestTypeDef]
    ) -> ListSNOMEDCTInferenceJobsResponseTypeDef:
        """
        Gets a list of InferSNOMEDCT jobs a user has submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/list_snomedct_inference_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#list_snomedct_inference_jobs)
        """

    async def start_entities_detection_v2_job(
        self, **kwargs: Unpack[StartEntitiesDetectionV2JobRequestTypeDef]
    ) -> StartEntitiesDetectionV2JobResponseTypeDef:
        """
        Starts an asynchronous medical entity detection job for a collection of
        documents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/start_entities_detection_v2_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#start_entities_detection_v2_job)
        """

    async def start_icd10_cm_inference_job(
        self, **kwargs: Unpack[StartICD10CMInferenceJobRequestTypeDef]
    ) -> StartICD10CMInferenceJobResponseTypeDef:
        """
        Starts an asynchronous job to detect medical conditions and link them to the
        ICD-10-CM ontology.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/start_icd10_cm_inference_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#start_icd10_cm_inference_job)
        """

    async def start_phi_detection_job(
        self, **kwargs: Unpack[StartPHIDetectionJobRequestTypeDef]
    ) -> StartPHIDetectionJobResponseTypeDef:
        """
        Starts an asynchronous job to detect protected health information (PHI).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/start_phi_detection_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#start_phi_detection_job)
        """

    async def start_rx_norm_inference_job(
        self, **kwargs: Unpack[StartRxNormInferenceJobRequestTypeDef]
    ) -> StartRxNormInferenceJobResponseTypeDef:
        """
        Starts an asynchronous job to detect medication entities and link them to the
        RxNorm ontology.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/start_rx_norm_inference_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#start_rx_norm_inference_job)
        """

    async def start_snomedct_inference_job(
        self, **kwargs: Unpack[StartSNOMEDCTInferenceJobRequestTypeDef]
    ) -> StartSNOMEDCTInferenceJobResponseTypeDef:
        """
        Starts an asynchronous job to detect medical concepts and link them to the
        SNOMED-CT ontology.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/start_snomedct_inference_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#start_snomedct_inference_job)
        """

    async def stop_entities_detection_v2_job(
        self, **kwargs: Unpack[StopEntitiesDetectionV2JobRequestTypeDef]
    ) -> StopEntitiesDetectionV2JobResponseTypeDef:
        """
        Stops a medical entities detection job in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/stop_entities_detection_v2_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#stop_entities_detection_v2_job)
        """

    async def stop_icd10_cm_inference_job(
        self, **kwargs: Unpack[StopICD10CMInferenceJobRequestTypeDef]
    ) -> StopICD10CMInferenceJobResponseTypeDef:
        """
        Stops an InferICD10CM inference job in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/stop_icd10_cm_inference_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#stop_icd10_cm_inference_job)
        """

    async def stop_phi_detection_job(
        self, **kwargs: Unpack[StopPHIDetectionJobRequestTypeDef]
    ) -> StopPHIDetectionJobResponseTypeDef:
        """
        Stops a protected health information (PHI) detection job in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/stop_phi_detection_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#stop_phi_detection_job)
        """

    async def stop_rx_norm_inference_job(
        self, **kwargs: Unpack[StopRxNormInferenceJobRequestTypeDef]
    ) -> StopRxNormInferenceJobResponseTypeDef:
        """
        Stops an InferRxNorm inference job in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/stop_rx_norm_inference_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#stop_rx_norm_inference_job)
        """

    async def stop_snomedct_inference_job(
        self, **kwargs: Unpack[StopSNOMEDCTInferenceJobRequestTypeDef]
    ) -> StopSNOMEDCTInferenceJobResponseTypeDef:
        """
        Stops an InferSNOMEDCT inference job in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical/client/stop_snomedct_inference_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/#stop_snomedct_inference_job)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehendmedical.html#ComprehendMedical.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_comprehendmedical/client/)
        """
