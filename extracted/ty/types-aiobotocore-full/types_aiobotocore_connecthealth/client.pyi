"""
Type annotations for connecthealth service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_connecthealth.client import ConnectHealthClient

    session = get_session()
    async with session.create_client("connecthealth") as client:
        client: ConnectHealthClient
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListDomainsPaginator, ListSubscriptionsPaginator
from .type_defs import (
    ActivateSubscriptionInputTypeDef,
    ActivateSubscriptionOutputTypeDef,
    CreateDomainInputTypeDef,
    CreateDomainOutputTypeDef,
    CreateSubscriptionInputTypeDef,
    CreateSubscriptionOutputTypeDef,
    DeactivateSubscriptionInputTypeDef,
    DeactivateSubscriptionOutputTypeDef,
    DeleteDomainInputTypeDef,
    DeleteDomainOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    GetDomainInputTypeDef,
    GetDomainOutputTypeDef,
    GetMedicalScribeListeningSessionInputTypeDef,
    GetMedicalScribeListeningSessionOutputTypeDef,
    GetPatientInsightsJobRequestTypeDef,
    GetPatientInsightsJobResponseTypeDef,
    GetSubscriptionInputTypeDef,
    GetSubscriptionOutputTypeDef,
    ListDomainsInputTypeDef,
    ListDomainsOutputTypeDef,
    ListSubscriptionsInputTypeDef,
    ListSubscriptionsOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    StartMedicalScribeListeningSessionInputTypeDef,
    StartMedicalScribeListeningSessionOutputTypeDef,
    StartPatientInsightsJobRequestTypeDef,
    StartPatientInsightsJobResponseTypeDef,
    TagResourceInputTypeDef,
    UntagResourceInputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("ConnectHealthClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class ConnectHealthClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth.html#ConnectHealth.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ConnectHealthClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth.html#ConnectHealth.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#generate_presigned_url)
        """

    async def activate_subscription(
        self, **kwargs: Unpack[ActivateSubscriptionInputTypeDef]
    ) -> ActivateSubscriptionOutputTypeDef:
        """
        Activates a Subscription to enable billing for a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/activate_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#activate_subscription)
        """

    async def create_domain(
        self, **kwargs: Unpack[CreateDomainInputTypeDef]
    ) -> CreateDomainOutputTypeDef:
        """
        Creates a new Domain for managing HealthAgent resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/create_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#create_domain)
        """

    async def create_subscription(
        self, **kwargs: Unpack[CreateSubscriptionInputTypeDef]
    ) -> CreateSubscriptionOutputTypeDef:
        """
        Creates a new Subscription within a Domain for billing and user management.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/create_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#create_subscription)
        """

    async def deactivate_subscription(
        self, **kwargs: Unpack[DeactivateSubscriptionInputTypeDef]
    ) -> DeactivateSubscriptionOutputTypeDef:
        """
        Deactivates a Subscription to stop billing for a user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/deactivate_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#deactivate_subscription)
        """

    async def delete_domain(
        self, **kwargs: Unpack[DeleteDomainInputTypeDef]
    ) -> DeleteDomainOutputTypeDef:
        """
        Deletes a Domain and all associated resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/delete_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#delete_domain)
        """

    async def get_domain(self, **kwargs: Unpack[GetDomainInputTypeDef]) -> GetDomainOutputTypeDef:
        """
        Retrieves information about a Domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/get_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#get_domain)
        """

    async def get_medical_scribe_listening_session(
        self, **kwargs: Unpack[GetMedicalScribeListeningSessionInputTypeDef]
    ) -> GetMedicalScribeListeningSessionOutputTypeDef:
        """
        Retrieves details about an existing Medical Scribe listening session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/get_medical_scribe_listening_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#get_medical_scribe_listening_session)
        """

    async def get_patient_insights_job(
        self, **kwargs: Unpack[GetPatientInsightsJobRequestTypeDef]
    ) -> GetPatientInsightsJobResponseTypeDef:
        """
        Get details of a started patient insights job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/get_patient_insights_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#get_patient_insights_job)
        """

    async def get_subscription(
        self, **kwargs: Unpack[GetSubscriptionInputTypeDef]
    ) -> GetSubscriptionOutputTypeDef:
        """
        Retrieves information about a Subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/get_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#get_subscription)
        """

    async def list_domains(
        self, **kwargs: Unpack[ListDomainsInputTypeDef]
    ) -> ListDomainsOutputTypeDef:
        """
        Lists Domains for a given account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/list_domains.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#list_domains)
        """

    async def list_subscriptions(
        self, **kwargs: Unpack[ListSubscriptionsInputTypeDef]
    ) -> ListSubscriptionsOutputTypeDef:
        """
        Lists all Subscriptions within a Domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/list_subscriptions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#list_subscriptions)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags associated with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#list_tags_for_resource)
        """

    async def start_medical_scribe_listening_session(
        self, **kwargs: Unpack[StartMedicalScribeListeningSessionInputTypeDef]
    ) -> StartMedicalScribeListeningSessionOutputTypeDef:
        """
        Starts a new Medical Scribe listening session for real-time audio transcription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/start_medical_scribe_listening_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#start_medical_scribe_listening_session)
        """

    async def start_patient_insights_job(
        self, **kwargs: Unpack[StartPatientInsightsJobRequestTypeDef]
    ) -> StartPatientInsightsJobResponseTypeDef:
        """
        Starts a new patient insights job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/start_patient_insights_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#start_patient_insights_job)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates the specified tags with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#untag_resource)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_domains"]
    ) -> ListDomainsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_subscriptions"]
    ) -> ListSubscriptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth.html#ConnectHealth.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connecthealth.html#ConnectHealth.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connecthealth/client/)
        """
