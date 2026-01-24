"""
Type annotations for workspaces-web service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_workspaces_web.client import WorkSpacesWebClient

    session = get_session()
    async with session.create_client("workspaces-web") as client:
        client: WorkSpacesWebClient
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

from .paginator import (
    ListDataProtectionSettingsPaginator,
    ListSessionLoggersPaginator,
    ListSessionsPaginator,
)
from .type_defs import (
    AssociateBrowserSettingsRequestTypeDef,
    AssociateBrowserSettingsResponseTypeDef,
    AssociateDataProtectionSettingsRequestTypeDef,
    AssociateDataProtectionSettingsResponseTypeDef,
    AssociateIpAccessSettingsRequestTypeDef,
    AssociateIpAccessSettingsResponseTypeDef,
    AssociateNetworkSettingsRequestTypeDef,
    AssociateNetworkSettingsResponseTypeDef,
    AssociateSessionLoggerRequestTypeDef,
    AssociateSessionLoggerResponseTypeDef,
    AssociateTrustStoreRequestTypeDef,
    AssociateTrustStoreResponseTypeDef,
    AssociateUserAccessLoggingSettingsRequestTypeDef,
    AssociateUserAccessLoggingSettingsResponseTypeDef,
    AssociateUserSettingsRequestTypeDef,
    AssociateUserSettingsResponseTypeDef,
    CreateBrowserSettingsRequestTypeDef,
    CreateBrowserSettingsResponseTypeDef,
    CreateDataProtectionSettingsRequestTypeDef,
    CreateDataProtectionSettingsResponseTypeDef,
    CreateIdentityProviderRequestTypeDef,
    CreateIdentityProviderResponseTypeDef,
    CreateIpAccessSettingsRequestTypeDef,
    CreateIpAccessSettingsResponseTypeDef,
    CreateNetworkSettingsRequestTypeDef,
    CreateNetworkSettingsResponseTypeDef,
    CreatePortalRequestTypeDef,
    CreatePortalResponseTypeDef,
    CreateSessionLoggerRequestTypeDef,
    CreateSessionLoggerResponseTypeDef,
    CreateTrustStoreRequestTypeDef,
    CreateTrustStoreResponseTypeDef,
    CreateUserAccessLoggingSettingsRequestTypeDef,
    CreateUserAccessLoggingSettingsResponseTypeDef,
    CreateUserSettingsRequestTypeDef,
    CreateUserSettingsResponseTypeDef,
    DeleteBrowserSettingsRequestTypeDef,
    DeleteDataProtectionSettingsRequestTypeDef,
    DeleteIdentityProviderRequestTypeDef,
    DeleteIpAccessSettingsRequestTypeDef,
    DeleteNetworkSettingsRequestTypeDef,
    DeletePortalRequestTypeDef,
    DeleteSessionLoggerRequestTypeDef,
    DeleteTrustStoreRequestTypeDef,
    DeleteUserAccessLoggingSettingsRequestTypeDef,
    DeleteUserSettingsRequestTypeDef,
    DisassociateBrowserSettingsRequestTypeDef,
    DisassociateDataProtectionSettingsRequestTypeDef,
    DisassociateIpAccessSettingsRequestTypeDef,
    DisassociateNetworkSettingsRequestTypeDef,
    DisassociateSessionLoggerRequestTypeDef,
    DisassociateTrustStoreRequestTypeDef,
    DisassociateUserAccessLoggingSettingsRequestTypeDef,
    DisassociateUserSettingsRequestTypeDef,
    ExpireSessionRequestTypeDef,
    GetBrowserSettingsRequestTypeDef,
    GetBrowserSettingsResponseTypeDef,
    GetDataProtectionSettingsRequestTypeDef,
    GetDataProtectionSettingsResponseTypeDef,
    GetIdentityProviderRequestTypeDef,
    GetIdentityProviderResponseTypeDef,
    GetIpAccessSettingsRequestTypeDef,
    GetIpAccessSettingsResponseTypeDef,
    GetNetworkSettingsRequestTypeDef,
    GetNetworkSettingsResponseTypeDef,
    GetPortalRequestTypeDef,
    GetPortalResponseTypeDef,
    GetPortalServiceProviderMetadataRequestTypeDef,
    GetPortalServiceProviderMetadataResponseTypeDef,
    GetSessionLoggerRequestTypeDef,
    GetSessionLoggerResponseTypeDef,
    GetSessionRequestTypeDef,
    GetSessionResponseTypeDef,
    GetTrustStoreCertificateRequestTypeDef,
    GetTrustStoreCertificateResponseTypeDef,
    GetTrustStoreRequestTypeDef,
    GetTrustStoreResponseTypeDef,
    GetUserAccessLoggingSettingsRequestTypeDef,
    GetUserAccessLoggingSettingsResponseTypeDef,
    GetUserSettingsRequestTypeDef,
    GetUserSettingsResponseTypeDef,
    ListBrowserSettingsRequestTypeDef,
    ListBrowserSettingsResponseTypeDef,
    ListDataProtectionSettingsRequestTypeDef,
    ListDataProtectionSettingsResponseTypeDef,
    ListIdentityProvidersRequestTypeDef,
    ListIdentityProvidersResponseTypeDef,
    ListIpAccessSettingsRequestTypeDef,
    ListIpAccessSettingsResponseTypeDef,
    ListNetworkSettingsRequestTypeDef,
    ListNetworkSettingsResponseTypeDef,
    ListPortalsRequestTypeDef,
    ListPortalsResponseTypeDef,
    ListSessionLoggersRequestTypeDef,
    ListSessionLoggersResponseTypeDef,
    ListSessionsRequestTypeDef,
    ListSessionsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTrustStoreCertificatesRequestTypeDef,
    ListTrustStoreCertificatesResponseTypeDef,
    ListTrustStoresRequestTypeDef,
    ListTrustStoresResponseTypeDef,
    ListUserAccessLoggingSettingsRequestTypeDef,
    ListUserAccessLoggingSettingsResponseTypeDef,
    ListUserSettingsRequestTypeDef,
    ListUserSettingsResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateBrowserSettingsRequestTypeDef,
    UpdateBrowserSettingsResponseTypeDef,
    UpdateDataProtectionSettingsRequestTypeDef,
    UpdateDataProtectionSettingsResponseTypeDef,
    UpdateIdentityProviderRequestTypeDef,
    UpdateIdentityProviderResponseTypeDef,
    UpdateIpAccessSettingsRequestTypeDef,
    UpdateIpAccessSettingsResponseTypeDef,
    UpdateNetworkSettingsRequestTypeDef,
    UpdateNetworkSettingsResponseTypeDef,
    UpdatePortalRequestTypeDef,
    UpdatePortalResponseTypeDef,
    UpdateSessionLoggerRequestTypeDef,
    UpdateSessionLoggerResponseTypeDef,
    UpdateTrustStoreRequestTypeDef,
    UpdateTrustStoreResponseTypeDef,
    UpdateUserAccessLoggingSettingsRequestTypeDef,
    UpdateUserAccessLoggingSettingsResponseTypeDef,
    UpdateUserSettingsRequestTypeDef,
    UpdateUserSettingsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("WorkSpacesWebClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    TooManyTagsException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class WorkSpacesWebClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web.html#WorkSpacesWeb.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        WorkSpacesWebClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web.html#WorkSpacesWeb.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#generate_presigned_url)
        """

    async def associate_browser_settings(
        self, **kwargs: Unpack[AssociateBrowserSettingsRequestTypeDef]
    ) -> AssociateBrowserSettingsResponseTypeDef:
        """
        Associates a browser settings resource with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_browser_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#associate_browser_settings)
        """

    async def associate_data_protection_settings(
        self, **kwargs: Unpack[AssociateDataProtectionSettingsRequestTypeDef]
    ) -> AssociateDataProtectionSettingsResponseTypeDef:
        """
        Associates a data protection settings resource with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_data_protection_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#associate_data_protection_settings)
        """

    async def associate_ip_access_settings(
        self, **kwargs: Unpack[AssociateIpAccessSettingsRequestTypeDef]
    ) -> AssociateIpAccessSettingsResponseTypeDef:
        """
        Associates an IP access settings resource with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_ip_access_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#associate_ip_access_settings)
        """

    async def associate_network_settings(
        self, **kwargs: Unpack[AssociateNetworkSettingsRequestTypeDef]
    ) -> AssociateNetworkSettingsResponseTypeDef:
        """
        Associates a network settings resource with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_network_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#associate_network_settings)
        """

    async def associate_session_logger(
        self, **kwargs: Unpack[AssociateSessionLoggerRequestTypeDef]
    ) -> AssociateSessionLoggerResponseTypeDef:
        """
        Associates a session logger with a portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_session_logger.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#associate_session_logger)
        """

    async def associate_trust_store(
        self, **kwargs: Unpack[AssociateTrustStoreRequestTypeDef]
    ) -> AssociateTrustStoreResponseTypeDef:
        """
        Associates a trust store with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_trust_store.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#associate_trust_store)
        """

    async def associate_user_access_logging_settings(
        self, **kwargs: Unpack[AssociateUserAccessLoggingSettingsRequestTypeDef]
    ) -> AssociateUserAccessLoggingSettingsResponseTypeDef:
        """
        Associates a user access logging settings resource with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_user_access_logging_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#associate_user_access_logging_settings)
        """

    async def associate_user_settings(
        self, **kwargs: Unpack[AssociateUserSettingsRequestTypeDef]
    ) -> AssociateUserSettingsResponseTypeDef:
        """
        Associates a user settings resource with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/associate_user_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#associate_user_settings)
        """

    async def create_browser_settings(
        self, **kwargs: Unpack[CreateBrowserSettingsRequestTypeDef]
    ) -> CreateBrowserSettingsResponseTypeDef:
        """
        Creates a browser settings resource that can be associated with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_browser_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#create_browser_settings)
        """

    async def create_data_protection_settings(
        self, **kwargs: Unpack[CreateDataProtectionSettingsRequestTypeDef]
    ) -> CreateDataProtectionSettingsResponseTypeDef:
        """
        Creates a data protection settings resource that can be associated with a web
        portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_data_protection_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#create_data_protection_settings)
        """

    async def create_identity_provider(
        self, **kwargs: Unpack[CreateIdentityProviderRequestTypeDef]
    ) -> CreateIdentityProviderResponseTypeDef:
        """
        Creates an identity provider resource that is then associated with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_identity_provider.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#create_identity_provider)
        """

    async def create_ip_access_settings(
        self, **kwargs: Unpack[CreateIpAccessSettingsRequestTypeDef]
    ) -> CreateIpAccessSettingsResponseTypeDef:
        """
        Creates an IP access settings resource that can be associated with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_ip_access_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#create_ip_access_settings)
        """

    async def create_network_settings(
        self, **kwargs: Unpack[CreateNetworkSettingsRequestTypeDef]
    ) -> CreateNetworkSettingsResponseTypeDef:
        """
        Creates a network settings resource that can be associated with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_network_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#create_network_settings)
        """

    async def create_portal(
        self, **kwargs: Unpack[CreatePortalRequestTypeDef]
    ) -> CreatePortalResponseTypeDef:
        """
        Creates a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_portal.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#create_portal)
        """

    async def create_session_logger(
        self, **kwargs: Unpack[CreateSessionLoggerRequestTypeDef]
    ) -> CreateSessionLoggerResponseTypeDef:
        """
        Creates a session logger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_session_logger.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#create_session_logger)
        """

    async def create_trust_store(
        self, **kwargs: Unpack[CreateTrustStoreRequestTypeDef]
    ) -> CreateTrustStoreResponseTypeDef:
        """
        Creates a trust store that can be associated with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_trust_store.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#create_trust_store)
        """

    async def create_user_access_logging_settings(
        self, **kwargs: Unpack[CreateUserAccessLoggingSettingsRequestTypeDef]
    ) -> CreateUserAccessLoggingSettingsResponseTypeDef:
        """
        Creates a user access logging settings resource that can be associated with a
        web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_user_access_logging_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#create_user_access_logging_settings)
        """

    async def create_user_settings(
        self, **kwargs: Unpack[CreateUserSettingsRequestTypeDef]
    ) -> CreateUserSettingsResponseTypeDef:
        """
        Creates a user settings resource that can be associated with a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/create_user_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#create_user_settings)
        """

    async def delete_browser_settings(
        self, **kwargs: Unpack[DeleteBrowserSettingsRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes browser settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_browser_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#delete_browser_settings)
        """

    async def delete_data_protection_settings(
        self, **kwargs: Unpack[DeleteDataProtectionSettingsRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes data protection settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_data_protection_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#delete_data_protection_settings)
        """

    async def delete_identity_provider(
        self, **kwargs: Unpack[DeleteIdentityProviderRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes the identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_identity_provider.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#delete_identity_provider)
        """

    async def delete_ip_access_settings(
        self, **kwargs: Unpack[DeleteIpAccessSettingsRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes IP access settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_ip_access_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#delete_ip_access_settings)
        """

    async def delete_network_settings(
        self, **kwargs: Unpack[DeleteNetworkSettingsRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes network settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_network_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#delete_network_settings)
        """

    async def delete_portal(self, **kwargs: Unpack[DeletePortalRequestTypeDef]) -> dict[str, Any]:
        """
        Deletes a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_portal.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#delete_portal)
        """

    async def delete_session_logger(
        self, **kwargs: Unpack[DeleteSessionLoggerRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes a session logger resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_session_logger.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#delete_session_logger)
        """

    async def delete_trust_store(
        self, **kwargs: Unpack[DeleteTrustStoreRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes the trust store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_trust_store.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#delete_trust_store)
        """

    async def delete_user_access_logging_settings(
        self, **kwargs: Unpack[DeleteUserAccessLoggingSettingsRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes user access logging settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_user_access_logging_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#delete_user_access_logging_settings)
        """

    async def delete_user_settings(
        self, **kwargs: Unpack[DeleteUserSettingsRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes user settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/delete_user_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#delete_user_settings)
        """

    async def disassociate_browser_settings(
        self, **kwargs: Unpack[DisassociateBrowserSettingsRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Disassociates browser settings from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_browser_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#disassociate_browser_settings)
        """

    async def disassociate_data_protection_settings(
        self, **kwargs: Unpack[DisassociateDataProtectionSettingsRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Disassociates data protection settings from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_data_protection_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#disassociate_data_protection_settings)
        """

    async def disassociate_ip_access_settings(
        self, **kwargs: Unpack[DisassociateIpAccessSettingsRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Disassociates IP access settings from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_ip_access_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#disassociate_ip_access_settings)
        """

    async def disassociate_network_settings(
        self, **kwargs: Unpack[DisassociateNetworkSettingsRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Disassociates network settings from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_network_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#disassociate_network_settings)
        """

    async def disassociate_session_logger(
        self, **kwargs: Unpack[DisassociateSessionLoggerRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Disassociates a session logger from a portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_session_logger.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#disassociate_session_logger)
        """

    async def disassociate_trust_store(
        self, **kwargs: Unpack[DisassociateTrustStoreRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Disassociates a trust store from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_trust_store.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#disassociate_trust_store)
        """

    async def disassociate_user_access_logging_settings(
        self, **kwargs: Unpack[DisassociateUserAccessLoggingSettingsRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Disassociates user access logging settings from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_user_access_logging_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#disassociate_user_access_logging_settings)
        """

    async def disassociate_user_settings(
        self, **kwargs: Unpack[DisassociateUserSettingsRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Disassociates user settings from a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/disassociate_user_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#disassociate_user_settings)
        """

    async def expire_session(self, **kwargs: Unpack[ExpireSessionRequestTypeDef]) -> dict[str, Any]:
        """
        Expires an active secure browser session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/expire_session.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#expire_session)
        """

    async def get_browser_settings(
        self, **kwargs: Unpack[GetBrowserSettingsRequestTypeDef]
    ) -> GetBrowserSettingsResponseTypeDef:
        """
        Gets browser settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_browser_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_browser_settings)
        """

    async def get_data_protection_settings(
        self, **kwargs: Unpack[GetDataProtectionSettingsRequestTypeDef]
    ) -> GetDataProtectionSettingsResponseTypeDef:
        """
        Gets the data protection settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_data_protection_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_data_protection_settings)
        """

    async def get_identity_provider(
        self, **kwargs: Unpack[GetIdentityProviderRequestTypeDef]
    ) -> GetIdentityProviderResponseTypeDef:
        """
        Gets the identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_identity_provider.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_identity_provider)
        """

    async def get_ip_access_settings(
        self, **kwargs: Unpack[GetIpAccessSettingsRequestTypeDef]
    ) -> GetIpAccessSettingsResponseTypeDef:
        """
        Gets the IP access settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_ip_access_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_ip_access_settings)
        """

    async def get_network_settings(
        self, **kwargs: Unpack[GetNetworkSettingsRequestTypeDef]
    ) -> GetNetworkSettingsResponseTypeDef:
        """
        Gets the network settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_network_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_network_settings)
        """

    async def get_portal(
        self, **kwargs: Unpack[GetPortalRequestTypeDef]
    ) -> GetPortalResponseTypeDef:
        """
        Gets the web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_portal.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_portal)
        """

    async def get_portal_service_provider_metadata(
        self, **kwargs: Unpack[GetPortalServiceProviderMetadataRequestTypeDef]
    ) -> GetPortalServiceProviderMetadataResponseTypeDef:
        """
        Gets the service provider metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_portal_service_provider_metadata.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_portal_service_provider_metadata)
        """

    async def get_session(
        self, **kwargs: Unpack[GetSessionRequestTypeDef]
    ) -> GetSessionResponseTypeDef:
        """
        Gets information for a secure browser session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_session.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_session)
        """

    async def get_session_logger(
        self, **kwargs: Unpack[GetSessionLoggerRequestTypeDef]
    ) -> GetSessionLoggerResponseTypeDef:
        """
        Gets details about a specific session logger resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_session_logger.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_session_logger)
        """

    async def get_trust_store(
        self, **kwargs: Unpack[GetTrustStoreRequestTypeDef]
    ) -> GetTrustStoreResponseTypeDef:
        """
        Gets the trust store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_trust_store.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_trust_store)
        """

    async def get_trust_store_certificate(
        self, **kwargs: Unpack[GetTrustStoreCertificateRequestTypeDef]
    ) -> GetTrustStoreCertificateResponseTypeDef:
        """
        Gets the trust store certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_trust_store_certificate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_trust_store_certificate)
        """

    async def get_user_access_logging_settings(
        self, **kwargs: Unpack[GetUserAccessLoggingSettingsRequestTypeDef]
    ) -> GetUserAccessLoggingSettingsResponseTypeDef:
        """
        Gets user access logging settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_user_access_logging_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_user_access_logging_settings)
        """

    async def get_user_settings(
        self, **kwargs: Unpack[GetUserSettingsRequestTypeDef]
    ) -> GetUserSettingsResponseTypeDef:
        """
        Gets user settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_user_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_user_settings)
        """

    async def list_browser_settings(
        self, **kwargs: Unpack[ListBrowserSettingsRequestTypeDef]
    ) -> ListBrowserSettingsResponseTypeDef:
        """
        Retrieves a list of browser settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_browser_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_browser_settings)
        """

    async def list_data_protection_settings(
        self, **kwargs: Unpack[ListDataProtectionSettingsRequestTypeDef]
    ) -> ListDataProtectionSettingsResponseTypeDef:
        """
        Retrieves a list of data protection settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_data_protection_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_data_protection_settings)
        """

    async def list_identity_providers(
        self, **kwargs: Unpack[ListIdentityProvidersRequestTypeDef]
    ) -> ListIdentityProvidersResponseTypeDef:
        """
        Retrieves a list of identity providers for a specific web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_identity_providers.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_identity_providers)
        """

    async def list_ip_access_settings(
        self, **kwargs: Unpack[ListIpAccessSettingsRequestTypeDef]
    ) -> ListIpAccessSettingsResponseTypeDef:
        """
        Retrieves a list of IP access settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_ip_access_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_ip_access_settings)
        """

    async def list_network_settings(
        self, **kwargs: Unpack[ListNetworkSettingsRequestTypeDef]
    ) -> ListNetworkSettingsResponseTypeDef:
        """
        Retrieves a list of network settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_network_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_network_settings)
        """

    async def list_portals(
        self, **kwargs: Unpack[ListPortalsRequestTypeDef]
    ) -> ListPortalsResponseTypeDef:
        """
        Retrieves a list or web portals.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_portals.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_portals)
        """

    async def list_session_loggers(
        self, **kwargs: Unpack[ListSessionLoggersRequestTypeDef]
    ) -> ListSessionLoggersResponseTypeDef:
        """
        Lists all available session logger resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_session_loggers.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_session_loggers)
        """

    async def list_sessions(
        self, **kwargs: Unpack[ListSessionsRequestTypeDef]
    ) -> ListSessionsResponseTypeDef:
        """
        Lists information for multiple secure browser sessions from a specific portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_sessions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_sessions)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves a list of tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_tags_for_resource)
        """

    async def list_trust_store_certificates(
        self, **kwargs: Unpack[ListTrustStoreCertificatesRequestTypeDef]
    ) -> ListTrustStoreCertificatesResponseTypeDef:
        """
        Retrieves a list of trust store certificates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_trust_store_certificates.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_trust_store_certificates)
        """

    async def list_trust_stores(
        self, **kwargs: Unpack[ListTrustStoresRequestTypeDef]
    ) -> ListTrustStoresResponseTypeDef:
        """
        Retrieves a list of trust stores.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_trust_stores.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_trust_stores)
        """

    async def list_user_access_logging_settings(
        self, **kwargs: Unpack[ListUserAccessLoggingSettingsRequestTypeDef]
    ) -> ListUserAccessLoggingSettingsResponseTypeDef:
        """
        Retrieves a list of user access logging settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_user_access_logging_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_user_access_logging_settings)
        """

    async def list_user_settings(
        self, **kwargs: Unpack[ListUserSettingsRequestTypeDef]
    ) -> ListUserSettingsResponseTypeDef:
        """
        Retrieves a list of user settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/list_user_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#list_user_settings)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Adds or overwrites one or more tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Removes one or more tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#untag_resource)
        """

    async def update_browser_settings(
        self, **kwargs: Unpack[UpdateBrowserSettingsRequestTypeDef]
    ) -> UpdateBrowserSettingsResponseTypeDef:
        """
        Updates browser settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_browser_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#update_browser_settings)
        """

    async def update_data_protection_settings(
        self, **kwargs: Unpack[UpdateDataProtectionSettingsRequestTypeDef]
    ) -> UpdateDataProtectionSettingsResponseTypeDef:
        """
        Updates data protection settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_data_protection_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#update_data_protection_settings)
        """

    async def update_identity_provider(
        self, **kwargs: Unpack[UpdateIdentityProviderRequestTypeDef]
    ) -> UpdateIdentityProviderResponseTypeDef:
        """
        Updates the identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_identity_provider.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#update_identity_provider)
        """

    async def update_ip_access_settings(
        self, **kwargs: Unpack[UpdateIpAccessSettingsRequestTypeDef]
    ) -> UpdateIpAccessSettingsResponseTypeDef:
        """
        Updates IP access settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_ip_access_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#update_ip_access_settings)
        """

    async def update_network_settings(
        self, **kwargs: Unpack[UpdateNetworkSettingsRequestTypeDef]
    ) -> UpdateNetworkSettingsResponseTypeDef:
        """
        Updates network settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_network_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#update_network_settings)
        """

    async def update_portal(
        self, **kwargs: Unpack[UpdatePortalRequestTypeDef]
    ) -> UpdatePortalResponseTypeDef:
        """
        Updates a web portal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_portal.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#update_portal)
        """

    async def update_session_logger(
        self, **kwargs: Unpack[UpdateSessionLoggerRequestTypeDef]
    ) -> UpdateSessionLoggerResponseTypeDef:
        """
        Updates the details of a session logger.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_session_logger.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#update_session_logger)
        """

    async def update_trust_store(
        self, **kwargs: Unpack[UpdateTrustStoreRequestTypeDef]
    ) -> UpdateTrustStoreResponseTypeDef:
        """
        Updates the trust store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_trust_store.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#update_trust_store)
        """

    async def update_user_access_logging_settings(
        self, **kwargs: Unpack[UpdateUserAccessLoggingSettingsRequestTypeDef]
    ) -> UpdateUserAccessLoggingSettingsResponseTypeDef:
        """
        Updates the user access logging settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_user_access_logging_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#update_user_access_logging_settings)
        """

    async def update_user_settings(
        self, **kwargs: Unpack[UpdateUserSettingsRequestTypeDef]
    ) -> UpdateUserSettingsResponseTypeDef:
        """
        Updates the user settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/update_user_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#update_user_settings)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_protection_settings"]
    ) -> ListDataProtectionSettingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_session_loggers"]
    ) -> ListSessionLoggersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_sessions"]
    ) -> ListSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web.html#WorkSpacesWeb.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/workspaces-web.html#WorkSpacesWeb.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workspaces_web/client/)
        """
