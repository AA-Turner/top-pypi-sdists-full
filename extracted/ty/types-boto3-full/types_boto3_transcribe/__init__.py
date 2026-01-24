"""
Main interface for transcribe service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_transcribe/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_transcribe import (
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

    session = Session()
    client: TranscribeServiceClient = session.client("transcribe")

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
