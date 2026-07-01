"""
Type annotations for transcribe service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_transcribe.client import TranscribeServiceClient
    from types_aiobotocore_transcribe.waiter import (
        CallAnalyticsJobCompletedWaiter,
        LanguageModelCompletedWaiter,
        MedicalScribeJobCompletedWaiter,
        MedicalTranscriptionJobCompletedWaiter,
        MedicalVocabularyReadyWaiter,
        TranscriptionJobCompletedWaiter,
        VocabularyReadyWaiter,
    )

    session = get_session()
    async with session.create_client("transcribe") as client:
        client: TranscribeServiceClient

        call_analytics_job_completed_waiter: CallAnalyticsJobCompletedWaiter = client.get_waiter("call_analytics_job_completed")
        language_model_completed_waiter: LanguageModelCompletedWaiter = client.get_waiter("language_model_completed")
        medical_scribe_job_completed_waiter: MedicalScribeJobCompletedWaiter = client.get_waiter("medical_scribe_job_completed")
        medical_transcription_job_completed_waiter: MedicalTranscriptionJobCompletedWaiter = client.get_waiter("medical_transcription_job_completed")
        medical_vocabulary_ready_waiter: MedicalVocabularyReadyWaiter = client.get_waiter("medical_vocabulary_ready")
        transcription_job_completed_waiter: TranscriptionJobCompletedWaiter = client.get_waiter("transcription_job_completed")
        vocabulary_ready_waiter: VocabularyReadyWaiter = client.get_waiter("vocabulary_ready")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    DescribeLanguageModelRequestWaitTypeDef,
    GetCallAnalyticsJobRequestWaitTypeDef,
    GetMedicalScribeJobRequestWaitTypeDef,
    GetMedicalTranscriptionJobRequestWaitTypeDef,
    GetMedicalVocabularyRequestWaitTypeDef,
    GetTranscriptionJobRequestWaitTypeDef,
    GetVocabularyRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "CallAnalyticsJobCompletedWaiter",
    "LanguageModelCompletedWaiter",
    "MedicalScribeJobCompletedWaiter",
    "MedicalTranscriptionJobCompletedWaiter",
    "MedicalVocabularyReadyWaiter",
    "TranscriptionJobCompletedWaiter",
    "VocabularyReadyWaiter",
)


class CallAnalyticsJobCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/waiter/CallAnalyticsJobCompleted.html#TranscribeService.Waiter.CallAnalyticsJobCompleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/waiters/#callanalyticsjobcompletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetCallAnalyticsJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/waiter/CallAnalyticsJobCompleted.html#TranscribeService.Waiter.CallAnalyticsJobCompleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/waiters/#callanalyticsjobcompletedwaiter)
        """


class LanguageModelCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/waiter/LanguageModelCompleted.html#TranscribeService.Waiter.LanguageModelCompleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/waiters/#languagemodelcompletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeLanguageModelRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/waiter/LanguageModelCompleted.html#TranscribeService.Waiter.LanguageModelCompleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/waiters/#languagemodelcompletedwaiter)
        """


class MedicalScribeJobCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/waiter/MedicalScribeJobCompleted.html#TranscribeService.Waiter.MedicalScribeJobCompleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/waiters/#medicalscribejobcompletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetMedicalScribeJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/waiter/MedicalScribeJobCompleted.html#TranscribeService.Waiter.MedicalScribeJobCompleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/waiters/#medicalscribejobcompletedwaiter)
        """


class MedicalTranscriptionJobCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/waiter/MedicalTranscriptionJobCompleted.html#TranscribeService.Waiter.MedicalTranscriptionJobCompleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/waiters/#medicaltranscriptionjobcompletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetMedicalTranscriptionJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/waiter/MedicalTranscriptionJobCompleted.html#TranscribeService.Waiter.MedicalTranscriptionJobCompleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/waiters/#medicaltranscriptionjobcompletedwaiter)
        """


class MedicalVocabularyReadyWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/waiter/MedicalVocabularyReady.html#TranscribeService.Waiter.MedicalVocabularyReady)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/waiters/#medicalvocabularyreadywaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetMedicalVocabularyRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/waiter/MedicalVocabularyReady.html#TranscribeService.Waiter.MedicalVocabularyReady.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/waiters/#medicalvocabularyreadywaiter)
        """


class TranscriptionJobCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/waiter/TranscriptionJobCompleted.html#TranscribeService.Waiter.TranscriptionJobCompleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/waiters/#transcriptionjobcompletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetTranscriptionJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/waiter/TranscriptionJobCompleted.html#TranscribeService.Waiter.TranscriptionJobCompleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/waiters/#transcriptionjobcompletedwaiter)
        """


class VocabularyReadyWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/waiter/VocabularyReady.html#TranscribeService.Waiter.VocabularyReady)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/waiters/#vocabularyreadywaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetVocabularyRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/transcribe/waiter/VocabularyReady.html#TranscribeService.Waiter.VocabularyReady.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/waiters/#vocabularyreadywaiter)
        """
