"""
Type annotations for transcribe service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_transcribe.client import TranscribeServiceClient

    session = get_session()
    async with session.create_client("transcribe") as client:
        client: TranscribeServiceClient
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
    CreateCallAnalyticsCategoryRequestTypeDef,
    CreateCallAnalyticsCategoryResponseTypeDef,
    CreateLanguageModelRequestTypeDef,
    CreateLanguageModelResponseTypeDef,
    CreateMedicalVocabularyRequestTypeDef,
    CreateMedicalVocabularyResponseTypeDef,
    CreateVocabularyFilterRequestTypeDef,
    CreateVocabularyFilterResponseTypeDef,
    CreateVocabularyRequestTypeDef,
    CreateVocabularyResponseTypeDef,
    DeleteCallAnalyticsCategoryRequestTypeDef,
    DeleteCallAnalyticsJobRequestTypeDef,
    DeleteLanguageModelRequestTypeDef,
    DeleteMedicalScribeJobRequestTypeDef,
    DeleteMedicalTranscriptionJobRequestTypeDef,
    DeleteMedicalVocabularyRequestTypeDef,
    DeleteTranscriptionJobRequestTypeDef,
    DeleteVocabularyFilterRequestTypeDef,
    DeleteVocabularyRequestTypeDef,
    DescribeLanguageModelRequestTypeDef,
    DescribeLanguageModelResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetCallAnalyticsCategoryRequestTypeDef,
    GetCallAnalyticsCategoryResponseTypeDef,
    GetCallAnalyticsJobRequestTypeDef,
    GetCallAnalyticsJobResponseTypeDef,
    GetMedicalScribeJobRequestTypeDef,
    GetMedicalScribeJobResponseTypeDef,
    GetMedicalTranscriptionJobRequestTypeDef,
    GetMedicalTranscriptionJobResponseTypeDef,
    GetMedicalVocabularyRequestTypeDef,
    GetMedicalVocabularyResponseTypeDef,
    GetTranscriptionJobRequestTypeDef,
    GetTranscriptionJobResponseTypeDef,
    GetVocabularyFilterRequestTypeDef,
    GetVocabularyFilterResponseTypeDef,
    GetVocabularyRequestTypeDef,
    GetVocabularyResponseTypeDef,
    ListCallAnalyticsCategoriesRequestTypeDef,
    ListCallAnalyticsCategoriesResponseTypeDef,
    ListCallAnalyticsJobsRequestTypeDef,
    ListCallAnalyticsJobsResponseTypeDef,
    ListLanguageModelsRequestTypeDef,
    ListLanguageModelsResponseTypeDef,
    ListMedicalScribeJobsRequestTypeDef,
    ListMedicalScribeJobsResponseTypeDef,
    ListMedicalTranscriptionJobsRequestTypeDef,
    ListMedicalTranscriptionJobsResponseTypeDef,
    ListMedicalVocabulariesRequestTypeDef,
    ListMedicalVocabulariesResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTranscriptionJobsRequestTypeDef,
    ListTranscriptionJobsResponseTypeDef,
    ListVocabulariesRequestTypeDef,
    ListVocabulariesResponseTypeDef,
    ListVocabularyFiltersRequestTypeDef,
    ListVocabularyFiltersResponseTypeDef,
    StartCallAnalyticsJobRequestTypeDef,
    StartCallAnalyticsJobResponseTypeDef,
    StartMedicalScribeJobRequestTypeDef,
    StartMedicalScribeJobResponseTypeDef,
    StartMedicalTranscriptionJobRequestTypeDef,
    StartMedicalTranscriptionJobResponseTypeDef,
    StartTranscriptionJobRequestTypeDef,
    StartTranscriptionJobResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateCallAnalyticsCategoryRequestTypeDef,
    UpdateCallAnalyticsCategoryResponseTypeDef,
    UpdateMedicalVocabularyRequestTypeDef,
    UpdateMedicalVocabularyResponseTypeDef,
    UpdateVocabularyFilterRequestTypeDef,
    UpdateVocabularyFilterResponseTypeDef,
    UpdateVocabularyRequestTypeDef,
    UpdateVocabularyResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack


__all__ = ("TranscribeServiceClient",)


class Exceptions(BaseClientExceptions):
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalFailureException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]


class TranscribeServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe.html#TranscribeService.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        TranscribeServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe.html#TranscribeService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#generate_presigned_url)
        """

    async def create_call_analytics_category(
        self, **kwargs: Unpack[CreateCallAnalyticsCategoryRequestTypeDef]
    ) -> CreateCallAnalyticsCategoryResponseTypeDef:
        """
        Creates a new Call Analytics category.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/create_call_analytics_category.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#create_call_analytics_category)
        """

    async def create_language_model(
        self, **kwargs: Unpack[CreateLanguageModelRequestTypeDef]
    ) -> CreateLanguageModelResponseTypeDef:
        """
        Creates a new custom language model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/create_language_model.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#create_language_model)
        """

    async def create_medical_vocabulary(
        self, **kwargs: Unpack[CreateMedicalVocabularyRequestTypeDef]
    ) -> CreateMedicalVocabularyResponseTypeDef:
        """
        Creates a new custom medical vocabulary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/create_medical_vocabulary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#create_medical_vocabulary)
        """

    async def create_vocabulary(
        self, **kwargs: Unpack[CreateVocabularyRequestTypeDef]
    ) -> CreateVocabularyResponseTypeDef:
        """
        Creates a new custom vocabulary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/create_vocabulary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#create_vocabulary)
        """

    async def create_vocabulary_filter(
        self, **kwargs: Unpack[CreateVocabularyFilterRequestTypeDef]
    ) -> CreateVocabularyFilterResponseTypeDef:
        """
        Creates a new custom vocabulary filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/create_vocabulary_filter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#create_vocabulary_filter)
        """

    async def delete_call_analytics_category(
        self, **kwargs: Unpack[DeleteCallAnalyticsCategoryRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Call Analytics category.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/delete_call_analytics_category.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#delete_call_analytics_category)
        """

    async def delete_call_analytics_job(
        self, **kwargs: Unpack[DeleteCallAnalyticsJobRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a Call Analytics job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/delete_call_analytics_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#delete_call_analytics_job)
        """

    async def delete_language_model(
        self, **kwargs: Unpack[DeleteLanguageModelRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a custom language model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/delete_language_model.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#delete_language_model)
        """

    async def delete_medical_scribe_job(
        self, **kwargs: Unpack[DeleteMedicalScribeJobRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Medical Scribe job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/delete_medical_scribe_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#delete_medical_scribe_job)
        """

    async def delete_medical_transcription_job(
        self, **kwargs: Unpack[DeleteMedicalTranscriptionJobRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a medical transcription job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/delete_medical_transcription_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#delete_medical_transcription_job)
        """

    async def delete_medical_vocabulary(
        self, **kwargs: Unpack[DeleteMedicalVocabularyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a custom medical vocabulary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/delete_medical_vocabulary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#delete_medical_vocabulary)
        """

    async def delete_transcription_job(
        self, **kwargs: Unpack[DeleteTranscriptionJobRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a transcription job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/delete_transcription_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#delete_transcription_job)
        """

    async def delete_vocabulary(
        self, **kwargs: Unpack[DeleteVocabularyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a custom vocabulary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/delete_vocabulary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#delete_vocabulary)
        """

    async def delete_vocabulary_filter(
        self, **kwargs: Unpack[DeleteVocabularyFilterRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a custom vocabulary filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/delete_vocabulary_filter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#delete_vocabulary_filter)
        """

    async def describe_language_model(
        self, **kwargs: Unpack[DescribeLanguageModelRequestTypeDef]
    ) -> DescribeLanguageModelResponseTypeDef:
        """
        Provides information about the specified custom language model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/describe_language_model.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#describe_language_model)
        """

    async def get_call_analytics_category(
        self, **kwargs: Unpack[GetCallAnalyticsCategoryRequestTypeDef]
    ) -> GetCallAnalyticsCategoryResponseTypeDef:
        """
        Provides information about the specified Call Analytics category.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/get_call_analytics_category.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#get_call_analytics_category)
        """

    async def get_call_analytics_job(
        self, **kwargs: Unpack[GetCallAnalyticsJobRequestTypeDef]
    ) -> GetCallAnalyticsJobResponseTypeDef:
        """
        Provides information about the specified Call Analytics job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/get_call_analytics_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#get_call_analytics_job)
        """

    async def get_medical_scribe_job(
        self, **kwargs: Unpack[GetMedicalScribeJobRequestTypeDef]
    ) -> GetMedicalScribeJobResponseTypeDef:
        """
        Provides information about the specified Medical Scribe job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/get_medical_scribe_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#get_medical_scribe_job)
        """

    async def get_medical_transcription_job(
        self, **kwargs: Unpack[GetMedicalTranscriptionJobRequestTypeDef]
    ) -> GetMedicalTranscriptionJobResponseTypeDef:
        """
        Provides information about the specified medical transcription job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/get_medical_transcription_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#get_medical_transcription_job)
        """

    async def get_medical_vocabulary(
        self, **kwargs: Unpack[GetMedicalVocabularyRequestTypeDef]
    ) -> GetMedicalVocabularyResponseTypeDef:
        """
        Provides information about the specified custom medical vocabulary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/get_medical_vocabulary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#get_medical_vocabulary)
        """

    async def get_transcription_job(
        self, **kwargs: Unpack[GetTranscriptionJobRequestTypeDef]
    ) -> GetTranscriptionJobResponseTypeDef:
        """
        Provides information about the specified transcription job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/get_transcription_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#get_transcription_job)
        """

    async def get_vocabulary(
        self, **kwargs: Unpack[GetVocabularyRequestTypeDef]
    ) -> GetVocabularyResponseTypeDef:
        """
        Provides information about the specified custom vocabulary.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/get_vocabulary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#get_vocabulary)
        """

    async def get_vocabulary_filter(
        self, **kwargs: Unpack[GetVocabularyFilterRequestTypeDef]
    ) -> GetVocabularyFilterResponseTypeDef:
        """
        Provides information about the specified custom vocabulary filter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/get_vocabulary_filter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#get_vocabulary_filter)
        """

    async def list_call_analytics_categories(
        self, **kwargs: Unpack[ListCallAnalyticsCategoriesRequestTypeDef]
    ) -> ListCallAnalyticsCategoriesResponseTypeDef:
        """
        Provides a list of Call Analytics categories, including all rules that make up
        each category.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/list_call_analytics_categories.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#list_call_analytics_categories)
        """

    async def list_call_analytics_jobs(
        self, **kwargs: Unpack[ListCallAnalyticsJobsRequestTypeDef]
    ) -> ListCallAnalyticsJobsResponseTypeDef:
        """
        Provides a list of Call Analytics jobs that match the specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/list_call_analytics_jobs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#list_call_analytics_jobs)
        """

    async def list_language_models(
        self, **kwargs: Unpack[ListLanguageModelsRequestTypeDef]
    ) -> ListLanguageModelsResponseTypeDef:
        """
        Provides a list of custom language models that match the specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/list_language_models.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#list_language_models)
        """

    async def list_medical_scribe_jobs(
        self, **kwargs: Unpack[ListMedicalScribeJobsRequestTypeDef]
    ) -> ListMedicalScribeJobsResponseTypeDef:
        """
        Provides a list of Medical Scribe jobs that match the specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/list_medical_scribe_jobs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#list_medical_scribe_jobs)
        """

    async def list_medical_transcription_jobs(
        self, **kwargs: Unpack[ListMedicalTranscriptionJobsRequestTypeDef]
    ) -> ListMedicalTranscriptionJobsResponseTypeDef:
        """
        Provides a list of medical transcription jobs that match the specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/list_medical_transcription_jobs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#list_medical_transcription_jobs)
        """

    async def list_medical_vocabularies(
        self, **kwargs: Unpack[ListMedicalVocabulariesRequestTypeDef]
    ) -> ListMedicalVocabulariesResponseTypeDef:
        """
        Provides a list of custom medical vocabularies that match the specified
        criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/list_medical_vocabularies.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#list_medical_vocabularies)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags associated with the specified transcription job, vocabulary,
        model, or resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#list_tags_for_resource)
        """

    async def list_transcription_jobs(
        self, **kwargs: Unpack[ListTranscriptionJobsRequestTypeDef]
    ) -> ListTranscriptionJobsResponseTypeDef:
        """
        Provides a list of transcription jobs that match the specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/list_transcription_jobs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#list_transcription_jobs)
        """

    async def list_vocabularies(
        self, **kwargs: Unpack[ListVocabulariesRequestTypeDef]
    ) -> ListVocabulariesResponseTypeDef:
        """
        Provides a list of custom vocabularies that match the specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/list_vocabularies.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#list_vocabularies)
        """

    async def list_vocabulary_filters(
        self, **kwargs: Unpack[ListVocabularyFiltersRequestTypeDef]
    ) -> ListVocabularyFiltersResponseTypeDef:
        """
        Provides a list of custom vocabulary filters that match the specified criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/list_vocabulary_filters.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#list_vocabulary_filters)
        """

    async def start_call_analytics_job(
        self, **kwargs: Unpack[StartCallAnalyticsJobRequestTypeDef]
    ) -> StartCallAnalyticsJobResponseTypeDef:
        """
        Transcribes the audio from a customer service call and applies any additional
        Request Parameters you choose to include in your request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/start_call_analytics_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#start_call_analytics_job)
        """

    async def start_medical_scribe_job(
        self, **kwargs: Unpack[StartMedicalScribeJobRequestTypeDef]
    ) -> StartMedicalScribeJobResponseTypeDef:
        """
        Transcribes patient-clinician conversations and generates clinical notes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/start_medical_scribe_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#start_medical_scribe_job)
        """

    async def start_medical_transcription_job(
        self, **kwargs: Unpack[StartMedicalTranscriptionJobRequestTypeDef]
    ) -> StartMedicalTranscriptionJobResponseTypeDef:
        """
        Transcribes the audio from a medical dictation or conversation and applies any
        additional Request Parameters you choose to include in your request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/start_medical_transcription_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#start_medical_transcription_job)
        """

    async def start_transcription_job(
        self, **kwargs: Unpack[StartTranscriptionJobRequestTypeDef]
    ) -> StartTranscriptionJobResponseTypeDef:
        """
        Transcribes the audio from a media file and applies any additional Request
        Parameters you choose to include in your request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/start_transcription_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#start_transcription_job)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more custom tags, each in the form of a key:value pair, to the
        specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified Amazon Transcribe resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#untag_resource)
        """

    async def update_call_analytics_category(
        self, **kwargs: Unpack[UpdateCallAnalyticsCategoryRequestTypeDef]
    ) -> UpdateCallAnalyticsCategoryResponseTypeDef:
        """
        Updates the specified Call Analytics category with new rules.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/update_call_analytics_category.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#update_call_analytics_category)
        """

    async def update_medical_vocabulary(
        self, **kwargs: Unpack[UpdateMedicalVocabularyRequestTypeDef]
    ) -> UpdateMedicalVocabularyResponseTypeDef:
        """
        Updates an existing custom medical vocabulary with new values.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/update_medical_vocabulary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#update_medical_vocabulary)
        """

    async def update_vocabulary(
        self, **kwargs: Unpack[UpdateVocabularyRequestTypeDef]
    ) -> UpdateVocabularyResponseTypeDef:
        """
        Updates an existing custom vocabulary with new values.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/update_vocabulary.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#update_vocabulary)
        """

    async def update_vocabulary_filter(
        self, **kwargs: Unpack[UpdateVocabularyFilterRequestTypeDef]
    ) -> UpdateVocabularyFilterResponseTypeDef:
        """
        Updates an existing custom vocabulary filter with a new list of words.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/client/update_vocabulary_filter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/#update_vocabulary_filter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe.html#TranscribeService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe.html#TranscribeService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/client/)
        """
