"""
Main interface for transcribe service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_transcribe/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_transcribe import (
        CallAnalyticsJobCompletedWaiter,
        Client,
        LanguageModelCompletedWaiter,
        MedicalScribeJobCompletedWaiter,
        MedicalTranscriptionJobCompletedWaiter,
        MedicalVocabularyReadyWaiter,
        TranscribeServiceClient,
        TranscriptionJobCompletedWaiter,
        VocabularyReadyWaiter,
    )

    session = get_session()
    async with session.create_client("transcribe") as client:
        client: TranscribeServiceClient
        ...


    call_analytics_job_completed_waiter: CallAnalyticsJobCompletedWaiter = client.get_waiter("call_analytics_job_completed")
    language_model_completed_waiter: LanguageModelCompletedWaiter = client.get_waiter("language_model_completed")
    medical_scribe_job_completed_waiter: MedicalScribeJobCompletedWaiter = client.get_waiter("medical_scribe_job_completed")
    medical_transcription_job_completed_waiter: MedicalTranscriptionJobCompletedWaiter = client.get_waiter("medical_transcription_job_completed")
    medical_vocabulary_ready_waiter: MedicalVocabularyReadyWaiter = client.get_waiter("medical_vocabulary_ready")
    transcription_job_completed_waiter: TranscriptionJobCompletedWaiter = client.get_waiter("transcription_job_completed")
    vocabulary_ready_waiter: VocabularyReadyWaiter = client.get_waiter("vocabulary_ready")
    ```
"""

from .client import TranscribeServiceClient
from .waiter import (
    CallAnalyticsJobCompletedWaiter,
    LanguageModelCompletedWaiter,
    MedicalScribeJobCompletedWaiter,
    MedicalTranscriptionJobCompletedWaiter,
    MedicalVocabularyReadyWaiter,
    TranscriptionJobCompletedWaiter,
    VocabularyReadyWaiter,
)

Client = TranscribeServiceClient


__all__ = (
    "CallAnalyticsJobCompletedWaiter",
    "Client",
    "LanguageModelCompletedWaiter",
    "MedicalScribeJobCompletedWaiter",
    "MedicalTranscriptionJobCompletedWaiter",
    "MedicalVocabularyReadyWaiter",
    "TranscribeServiceClient",
    "TranscriptionJobCompletedWaiter",
    "VocabularyReadyWaiter",
)
