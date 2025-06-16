"""
Type annotations for rolesanywhere service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_rolesanywhere.client import IAMRolesAnywhereClient

    session = get_session()
    async with session.create_client("rolesanywhere") as client:
        client: IAMRolesAnywhereClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListCrlsPaginator,
    ListProfilesPaginator,
    ListSubjectsPaginator,
    ListTrustAnchorsPaginator,
)
from .type_defs import (
    CreateProfileRequestTypeDef,
    CreateTrustAnchorRequestTypeDef,
    CrlDetailResponseTypeDef,
    DeleteAttributeMappingRequestTypeDef,
    DeleteAttributeMappingResponseTypeDef,
    ImportCrlRequestTypeDef,
    ListCrlsResponseTypeDef,
    ListProfilesResponseTypeDef,
    ListRequestRequestExtraExtraTypeDef,
    ListRequestRequestExtraTypeDef,
    ListRequestRequestTypeDef,
    ListRequestTypeDef,
    ListSubjectsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTrustAnchorsResponseTypeDef,
    ProfileDetailResponseTypeDef,
    PutAttributeMappingRequestTypeDef,
    PutAttributeMappingResponseTypeDef,
    PutNotificationSettingsRequestTypeDef,
    PutNotificationSettingsResponseTypeDef,
    ResetNotificationSettingsRequestTypeDef,
    ResetNotificationSettingsResponseTypeDef,
    ScalarCrlRequestRequestExtraExtraTypeDef,
    ScalarCrlRequestRequestExtraTypeDef,
    ScalarCrlRequestRequestTypeDef,
    ScalarCrlRequestTypeDef,
    ScalarProfileRequestRequestExtraExtraTypeDef,
    ScalarProfileRequestRequestExtraTypeDef,
    ScalarProfileRequestRequestTypeDef,
    ScalarProfileRequestTypeDef,
    ScalarSubjectRequestTypeDef,
    ScalarTrustAnchorRequestRequestExtraExtraTypeDef,
    ScalarTrustAnchorRequestRequestExtraTypeDef,
    ScalarTrustAnchorRequestRequestTypeDef,
    ScalarTrustAnchorRequestTypeDef,
    SubjectDetailResponseTypeDef,
    TagResourceRequestTypeDef,
    TrustAnchorDetailResponseTypeDef,
    UntagResourceRequestTypeDef,
    UpdateCrlRequestTypeDef,
    UpdateProfileRequestTypeDef,
    UpdateTrustAnchorRequestTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("IAMRolesAnywhereClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class IAMRolesAnywhereClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere.html#IAMRolesAnywhere.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IAMRolesAnywhereClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere.html#IAMRolesAnywhere.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#generate_presigned_url)
        """

    async def create_profile(
        self, **kwargs: Unpack[CreateProfileRequestTypeDef]
    ) -> ProfileDetailResponseTypeDef:
        """
        Creates a <i>profile</i>, a list of the roles that Roles Anywhere service is
        trusted to assume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/create_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#create_profile)
        """

    async def create_trust_anchor(
        self, **kwargs: Unpack[CreateTrustAnchorRequestTypeDef]
    ) -> TrustAnchorDetailResponseTypeDef:
        """
        Creates a trust anchor to establish trust between IAM Roles Anywhere and your
        certificate authority (CA).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/create_trust_anchor.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#create_trust_anchor)
        """

    async def delete_attribute_mapping(
        self, **kwargs: Unpack[DeleteAttributeMappingRequestTypeDef]
    ) -> DeleteAttributeMappingResponseTypeDef:
        """
        Delete an entry from the attribute mapping rules enforced by a given profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/delete_attribute_mapping.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#delete_attribute_mapping)
        """

    async def delete_crl(
        self, **kwargs: Unpack[ScalarCrlRequestTypeDef]
    ) -> CrlDetailResponseTypeDef:
        """
        Deletes a certificate revocation list (CRL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/delete_crl.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#delete_crl)
        """

    async def delete_profile(
        self, **kwargs: Unpack[ScalarProfileRequestTypeDef]
    ) -> ProfileDetailResponseTypeDef:
        """
        Deletes a profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/delete_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#delete_profile)
        """

    async def delete_trust_anchor(
        self, **kwargs: Unpack[ScalarTrustAnchorRequestTypeDef]
    ) -> TrustAnchorDetailResponseTypeDef:
        """
        Deletes a trust anchor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/delete_trust_anchor.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#delete_trust_anchor)
        """

    async def disable_crl(
        self, **kwargs: Unpack[ScalarCrlRequestRequestTypeDef]
    ) -> CrlDetailResponseTypeDef:
        """
        Disables a certificate revocation list (CRL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/disable_crl.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#disable_crl)
        """

    async def disable_profile(
        self, **kwargs: Unpack[ScalarProfileRequestRequestTypeDef]
    ) -> ProfileDetailResponseTypeDef:
        """
        Disables a profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/disable_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#disable_profile)
        """

    async def disable_trust_anchor(
        self, **kwargs: Unpack[ScalarTrustAnchorRequestRequestTypeDef]
    ) -> TrustAnchorDetailResponseTypeDef:
        """
        Disables a trust anchor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/disable_trust_anchor.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#disable_trust_anchor)
        """

    async def enable_crl(
        self, **kwargs: Unpack[ScalarCrlRequestRequestExtraTypeDef]
    ) -> CrlDetailResponseTypeDef:
        """
        Enables a certificate revocation list (CRL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/enable_crl.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#enable_crl)
        """

    async def enable_profile(
        self, **kwargs: Unpack[ScalarProfileRequestRequestExtraTypeDef]
    ) -> ProfileDetailResponseTypeDef:
        """
        Enables temporary credential requests for a profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/enable_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#enable_profile)
        """

    async def enable_trust_anchor(
        self, **kwargs: Unpack[ScalarTrustAnchorRequestRequestExtraTypeDef]
    ) -> TrustAnchorDetailResponseTypeDef:
        """
        Enables a trust anchor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/enable_trust_anchor.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#enable_trust_anchor)
        """

    async def get_crl(
        self, **kwargs: Unpack[ScalarCrlRequestRequestExtraExtraTypeDef]
    ) -> CrlDetailResponseTypeDef:
        """
        Gets a certificate revocation list (CRL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/get_crl.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#get_crl)
        """

    async def get_profile(
        self, **kwargs: Unpack[ScalarProfileRequestRequestExtraExtraTypeDef]
    ) -> ProfileDetailResponseTypeDef:
        """
        Gets a profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/get_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#get_profile)
        """

    async def get_subject(
        self, **kwargs: Unpack[ScalarSubjectRequestTypeDef]
    ) -> SubjectDetailResponseTypeDef:
        """
        Gets a <i>subject</i>, which associates a certificate identity with
        authentication attempts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/get_subject.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#get_subject)
        """

    async def get_trust_anchor(
        self, **kwargs: Unpack[ScalarTrustAnchorRequestRequestExtraExtraTypeDef]
    ) -> TrustAnchorDetailResponseTypeDef:
        """
        Gets a trust anchor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/get_trust_anchor.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#get_trust_anchor)
        """

    async def import_crl(
        self, **kwargs: Unpack[ImportCrlRequestTypeDef]
    ) -> CrlDetailResponseTypeDef:
        """
        Imports the certificate revocation list (CRL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/import_crl.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#import_crl)
        """

    async def list_crls(self, **kwargs: Unpack[ListRequestTypeDef]) -> ListCrlsResponseTypeDef:
        """
        Lists all certificate revocation lists (CRL) in the authenticated account and
        Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/list_crls.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#list_crls)
        """

    async def list_profiles(
        self, **kwargs: Unpack[ListRequestRequestTypeDef]
    ) -> ListProfilesResponseTypeDef:
        """
        Lists all profiles in the authenticated account and Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/list_profiles.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#list_profiles)
        """

    async def list_subjects(
        self, **kwargs: Unpack[ListRequestRequestExtraTypeDef]
    ) -> ListSubjectsResponseTypeDef:
        """
        Lists the subjects in the authenticated account and Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/list_subjects.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#list_subjects)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags attached to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#list_tags_for_resource)
        """

    async def list_trust_anchors(
        self, **kwargs: Unpack[ListRequestRequestExtraExtraTypeDef]
    ) -> ListTrustAnchorsResponseTypeDef:
        """
        Lists the trust anchors in the authenticated account and Amazon Web Services
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/list_trust_anchors.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#list_trust_anchors)
        """

    async def put_attribute_mapping(
        self, **kwargs: Unpack[PutAttributeMappingRequestTypeDef]
    ) -> PutAttributeMappingResponseTypeDef:
        """
        Put an entry in the attribute mapping rules that will be enforced by a given
        profile.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/put_attribute_mapping.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#put_attribute_mapping)
        """

    async def put_notification_settings(
        self, **kwargs: Unpack[PutNotificationSettingsRequestTypeDef]
    ) -> PutNotificationSettingsResponseTypeDef:
        """
        Attaches a list of <i>notification settings</i> to a trust anchor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/put_notification_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#put_notification_settings)
        """

    async def reset_notification_settings(
        self, **kwargs: Unpack[ResetNotificationSettingsRequestTypeDef]
    ) -> ResetNotificationSettingsResponseTypeDef:
        """
        Resets the <i>custom notification setting</i> to IAM Roles Anywhere default
        setting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/reset_notification_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#reset_notification_settings)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Attaches tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes tags from the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#untag_resource)
        """

    async def update_crl(
        self, **kwargs: Unpack[UpdateCrlRequestTypeDef]
    ) -> CrlDetailResponseTypeDef:
        """
        Updates the certificate revocation list (CRL).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/update_crl.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#update_crl)
        """

    async def update_profile(
        self, **kwargs: Unpack[UpdateProfileRequestTypeDef]
    ) -> ProfileDetailResponseTypeDef:
        """
        Updates a <i>profile</i>, a list of the roles that IAM Roles Anywhere service
        is trusted to assume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/update_profile.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#update_profile)
        """

    async def update_trust_anchor(
        self, **kwargs: Unpack[UpdateTrustAnchorRequestTypeDef]
    ) -> TrustAnchorDetailResponseTypeDef:
        """
        Updates a trust anchor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/update_trust_anchor.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#update_trust_anchor)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_crls"]
    ) -> ListCrlsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_profiles"]
    ) -> ListProfilesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_subjects"]
    ) -> ListSubjectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_trust_anchors"]
    ) -> ListTrustAnchorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere.html#IAMRolesAnywhere.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rolesanywhere.html#IAMRolesAnywhere.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_rolesanywhere/client/)
        """
