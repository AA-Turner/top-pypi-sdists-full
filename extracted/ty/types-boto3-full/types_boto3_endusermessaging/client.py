"""
Type annotations for endusermessaging service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_endusermessaging.client import EndUserMessagingClient

    session = Session()
    client: EndUserMessagingClient = session.client("endusermessaging")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListBrandProfileAttributesPaginator,
    ListBrandProfilesPaginator,
    ListJobsPaginator,
    ListNotifyCodeConfigurationsPaginator,
    ListRegistrationsFromBrandProfilePaginator,
)
from .type_defs import (
    CreateBrandProfileAttributesInputTypeDef,
    CreateBrandProfileAttributesOutputTypeDef,
    CreateBrandProfileFromRegistrationInputTypeDef,
    CreateBrandProfileFromRegistrationOutputTypeDef,
    CreateBrandProfileInputTypeDef,
    CreateBrandProfileOutputTypeDef,
    CreateNotifyCodeConfigurationInputTypeDef,
    CreateNotifyCodeConfigurationOutputTypeDef,
    CreateRegistrationsFromBrandProfileInputTypeDef,
    CreateRegistrationsFromBrandProfileOutputTypeDef,
    DeleteBrandProfileAttributeInputTypeDef,
    DeleteBrandProfileAttributeOutputTypeDef,
    DeleteBrandProfileInputTypeDef,
    DeleteBrandProfileOutputTypeDef,
    DeleteNotifyCodeConfigurationInputTypeDef,
    GetBrandProfileAttributeInputTypeDef,
    GetBrandProfileAttributeOutputTypeDef,
    GetBrandProfileInputTypeDef,
    GetBrandProfileOutputTypeDef,
    GetJobInputTypeDef,
    GetNotifyCodeConfigurationInputTypeDef,
    GetNotifyCodeConfigurationOutputTypeDef,
    JobTypeDef,
    ListBrandProfileAttributesInputTypeDef,
    ListBrandProfileAttributesOutputTypeDef,
    ListBrandProfilesInputTypeDef,
    ListBrandProfilesOutputTypeDef,
    ListJobsInputTypeDef,
    ListJobsOutputTypeDef,
    ListNotifyCodeConfigurationsInputTypeDef,
    ListNotifyCodeConfigurationsOutputTypeDef,
    ListRegistrationsFromBrandProfileInputTypeDef,
    ListRegistrationsFromBrandProfileOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    SendNotifyCodeVerificationInputTypeDef,
    SendNotifyCodeVerificationOutputTypeDef,
    TagResourceInputTypeDef,
    UntagResourceInputTypeDef,
    UpdateBrandProfileAttributeInputTypeDef,
    UpdateBrandProfileAttributeOutputTypeDef,
    UpdateBrandProfileFromRegistrationInputTypeDef,
    UpdateBrandProfileFromRegistrationOutputTypeDef,
    UpdateBrandProfileInputTypeDef,
    UpdateBrandProfileOutputTypeDef,
    UpdateNotifyCodeConfigurationInputTypeDef,
    UpdateNotifyCodeConfigurationOutputTypeDef,
    UpdateRegistrationsFromBrandProfileInputTypeDef,
    UpdateRegistrationsFromBrandProfileOutputTypeDef,
    ValidateNotifyCodeVerificationInputTypeDef,
    ValidateNotifyCodeVerificationOutputTypeDef,
)
from .waiter import BrandProfileActiveWaiter, JobSuccessWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("EndUserMessagingClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class EndUserMessagingClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging.html#EndUserMessaging.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        EndUserMessagingClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging.html#EndUserMessaging.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#generate_presigned_url)
        """

    def create_brand_profile(
        self, **kwargs: Unpack[CreateBrandProfileInputTypeDef]
    ) -> CreateBrandProfileOutputTypeDef:
        """
        Creates a brand profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/create_brand_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#create_brand_profile)
        """

    def create_brand_profile_attributes(
        self, **kwargs: Unpack[CreateBrandProfileAttributesInputTypeDef]
    ) -> CreateBrandProfileAttributesOutputTypeDef:
        """
        Creates up to 10 attributes for a brand profile in a single request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/create_brand_profile_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#create_brand_profile_attributes)
        """

    def create_brand_profile_from_registration(
        self, **kwargs: Unpack[CreateBrandProfileFromRegistrationInputTypeDef]
    ) -> CreateBrandProfileFromRegistrationOutputTypeDef:
        """
        Creates a brand profile and populates its attributes from an existing
        registration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/create_brand_profile_from_registration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#create_brand_profile_from_registration)
        """

    def create_notify_code_configuration(
        self, **kwargs: Unpack[CreateNotifyCodeConfigurationInputTypeDef]
    ) -> CreateNotifyCodeConfigurationOutputTypeDef:
        """
        Creates a notify code configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/create_notify_code_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#create_notify_code_configuration)
        """

    def create_registrations_from_brand_profile(
        self, **kwargs: Unpack[CreateRegistrationsFromBrandProfileInputTypeDef]
    ) -> CreateRegistrationsFromBrandProfileOutputTypeDef:
        """
        Creates one or more registrations in the DRAFT state and prefills their fields
        from the attributes of a brand profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/create_registrations_from_brand_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#create_registrations_from_brand_profile)
        """

    def delete_brand_profile(
        self, **kwargs: Unpack[DeleteBrandProfileInputTypeDef]
    ) -> DeleteBrandProfileOutputTypeDef:
        """
        Deletes a brand profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/delete_brand_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#delete_brand_profile)
        """

    def delete_brand_profile_attribute(
        self, **kwargs: Unpack[DeleteBrandProfileAttributeInputTypeDef]
    ) -> DeleteBrandProfileAttributeOutputTypeDef:
        """
        Deletes a brand profile attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/delete_brand_profile_attribute.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#delete_brand_profile_attribute)
        """

    def delete_notify_code_configuration(
        self, **kwargs: Unpack[DeleteNotifyCodeConfigurationInputTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes a notify code configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/delete_notify_code_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#delete_notify_code_configuration)
        """

    def get_brand_profile(
        self, **kwargs: Unpack[GetBrandProfileInputTypeDef]
    ) -> GetBrandProfileOutputTypeDef:
        """
        Retrieves the metadata for a brand profile, including its name, status,
        deletion protection setting, and timestamps.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/get_brand_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#get_brand_profile)
        """

    def get_brand_profile_attribute(
        self, **kwargs: Unpack[GetBrandProfileAttributeInputTypeDef]
    ) -> GetBrandProfileAttributeOutputTypeDef:
        """
        Retrieves a single brand profile attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/get_brand_profile_attribute.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#get_brand_profile_attribute)
        """

    def get_job(self, **kwargs: Unpack[GetJobInputTypeDef]) -> JobTypeDef:
        """
        Retrieves the current state of an asynchronous job, including its status and
        any resources that it created or updated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/get_job.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#get_job)
        """

    def get_notify_code_configuration(
        self, **kwargs: Unpack[GetNotifyCodeConfigurationInputTypeDef]
    ) -> GetNotifyCodeConfigurationOutputTypeDef:
        """
        Retrieves a notify code configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/get_notify_code_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#get_notify_code_configuration)
        """

    def list_brand_profile_attributes(
        self, **kwargs: Unpack[ListBrandProfileAttributesInputTypeDef]
    ) -> ListBrandProfileAttributesOutputTypeDef:
        """
        Retrieves a paginated list of the attributes for a brand profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/list_brand_profile_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#list_brand_profile_attributes)
        """

    def list_brand_profiles(
        self, **kwargs: Unpack[ListBrandProfilesInputTypeDef]
    ) -> ListBrandProfilesOutputTypeDef:
        """
        Retrieves a paginated list of the brand profiles in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/list_brand_profiles.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#list_brand_profiles)
        """

    def list_jobs(self, **kwargs: Unpack[ListJobsInputTypeDef]) -> ListJobsOutputTypeDef:
        """
        Retrieves a paginated list of the asynchronous jobs in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/list_jobs.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#list_jobs)
        """

    def list_notify_code_configurations(
        self, **kwargs: Unpack[ListNotifyCodeConfigurationsInputTypeDef]
    ) -> ListNotifyCodeConfigurationsOutputTypeDef:
        """
        Retrieves a paginated list of the notify code configurations in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/list_notify_code_configurations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#list_notify_code_configurations)
        """

    def list_registrations_from_brand_profile(
        self, **kwargs: Unpack[ListRegistrationsFromBrandProfileInputTypeDef]
    ) -> ListRegistrationsFromBrandProfileOutputTypeDef:
        """
        Retrieves a paginated list of the registrations that were created from a brand
        profile through the synchronization operations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/list_registrations_from_brand_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#list_registrations_from_brand_profile)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Retrieves the tags that are associated with a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#list_tags_for_resource)
        """

    def send_notify_code_verification(
        self, **kwargs: Unpack[SendNotifyCodeVerificationInputTypeDef]
    ) -> SendNotifyCodeVerificationOutputTypeDef:
        """
        Generates a one-time passcode and delivers it to a recipient over the requested
        channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/send_notify_code_verification.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#send_notify_code_verification)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Adds or overwrites the tags on a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Removes the specified tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#untag_resource)
        """

    def update_brand_profile(
        self, **kwargs: Unpack[UpdateBrandProfileInputTypeDef]
    ) -> UpdateBrandProfileOutputTypeDef:
        """
        Updates the name or the deletion protection setting of a brand profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/update_brand_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#update_brand_profile)
        """

    def update_brand_profile_attribute(
        self, **kwargs: Unpack[UpdateBrandProfileAttributeInputTypeDef]
    ) -> UpdateBrandProfileAttributeOutputTypeDef:
        """
        Updates the value, description, or category of an existing brand profile
        attribute.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/update_brand_profile_attribute.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#update_brand_profile_attribute)
        """

    def update_brand_profile_from_registration(
        self, **kwargs: Unpack[UpdateBrandProfileFromRegistrationInputTypeDef]
    ) -> UpdateBrandProfileFromRegistrationOutputTypeDef:
        """
        Imports or refreshes the attributes of an existing brand profile from an
        existing registration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/update_brand_profile_from_registration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#update_brand_profile_from_registration)
        """

    def update_notify_code_configuration(
        self, **kwargs: Unpack[UpdateNotifyCodeConfigurationInputTypeDef]
    ) -> UpdateNotifyCodeConfigurationOutputTypeDef:
        """
        Updates the mutable fields of a notify code configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/update_notify_code_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#update_notify_code_configuration)
        """

    def update_registrations_from_brand_profile(
        self, **kwargs: Unpack[UpdateRegistrationsFromBrandProfileInputTypeDef]
    ) -> UpdateRegistrationsFromBrandProfileOutputTypeDef:
        """
        Repushes the attributes of a brand profile into existing DRAFT registrations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/update_registrations_from_brand_profile.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#update_registrations_from_brand_profile)
        """

    def validate_notify_code_verification(
        self, **kwargs: Unpack[ValidateNotifyCodeVerificationInputTypeDef]
    ) -> ValidateNotifyCodeVerificationOutputTypeDef:
        """
        Validates a one-time passcode that a recipient submitted.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/validate_notify_code_verification.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#validate_notify_code_verification)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_brand_profile_attributes"]
    ) -> ListBrandProfileAttributesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_brand_profiles"]
    ) -> ListBrandProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_jobs"]
    ) -> ListJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_notify_code_configurations"]
    ) -> ListNotifyCodeConfigurationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_registrations_from_brand_profile"]
    ) -> ListRegistrationsFromBrandProfilePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["brand_profile_active"]
    ) -> BrandProfileActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["job_success"]
    ) -> JobSuccessWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/endusermessaging/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_endusermessaging/client/#get_waiter)
        """
