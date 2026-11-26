"""
Type annotations for elb-proxy service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_elb_proxy.client import ELBProxyClient

    session = Session()
    client: ELBProxyClient = session.client("elb-proxy")
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
    ListCertificateAssociationsPaginator,
    ListProxiesPaginator,
    ListProxyUpdatesPaginator,
    ListProxyVersionsPaginator,
)
from .type_defs import (
    AssociateCertificateRequestTypeDef,
    AssociateCertificateResponseTypeDef,
    CreateProxyRequestTypeDef,
    CreateProxyResponseTypeDef,
    DeleteProxyRequestTypeDef,
    DeleteProxyResponseTypeDef,
    DisassociateCertificateRequestTypeDef,
    DisassociateCertificateResponseTypeDef,
    GetProxyAttributesRequestTypeDef,
    GetProxyAttributesResponseTypeDef,
    GetProxyConfigurationContentsRequestTypeDef,
    GetProxyConfigurationContentsResponseTypeDef,
    GetProxyRequestTypeDef,
    GetProxyResponseTypeDef,
    GetProxyUpdateRequestTypeDef,
    GetProxyUpdateResponseTypeDef,
    ListCertificateAssociationsRequestTypeDef,
    ListCertificateAssociationsResponseTypeDef,
    ListProxiesRequestTypeDef,
    ListProxiesResponseTypeDef,
    ListProxyUpdatesRequestTypeDef,
    ListProxyUpdatesResponseTypeDef,
    ListProxyVersionsRequestTypeDef,
    ListProxyVersionsResponseTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    TagResourceInputTypeDef,
    UntagResourceInputTypeDef,
    UpdateProxyAttributesRequestTypeDef,
    UpdateProxyAttributesResponseTypeDef,
    UpdateProxyConfigurationRequestTypeDef,
    UpdateProxyConfigurationResponseTypeDef,
    UpdateProxyNetworkConfigurationRequestTypeDef,
    UpdateProxyNetworkConfigurationResponseTypeDef,
)
from .waiter import ProxyActiveWaiter, ProxyDeletedWaiter, ProxyUpdateCompleteWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ELBProxyClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    OperationNotPermittedException: type[BotocoreClientError]
    PriorRequestNotCompletedException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class ELBProxyClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy.html#ELBProxy.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ELBProxyClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy.html#ELBProxy.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#generate_presigned_url)
        """

    def associate_certificate(
        self, **kwargs: Unpack[AssociateCertificateRequestTypeDef]
    ) -> AssociateCertificateResponseTypeDef:
        """
        Associates an ACM certificate with the specified Proxy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/associate_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#associate_certificate)
        """

    def create_proxy(
        self, **kwargs: Unpack[CreateProxyRequestTypeDef]
    ) -> CreateProxyResponseTypeDef:
        """
        Creates a proxy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/create_proxy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#create_proxy)
        """

    def delete_proxy(
        self, **kwargs: Unpack[DeleteProxyRequestTypeDef]
    ) -> DeleteProxyResponseTypeDef:
        """
        Deletes a proxy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/delete_proxy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#delete_proxy)
        """

    def disassociate_certificate(
        self, **kwargs: Unpack[DisassociateCertificateRequestTypeDef]
    ) -> DisassociateCertificateResponseTypeDef:
        """
        Disassociates an ACM certificate from the specified proxy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/disassociate_certificate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#disassociate_certificate)
        """

    def get_proxy(self, **kwargs: Unpack[GetProxyRequestTypeDef]) -> GetProxyResponseTypeDef:
        """
        Retrieves information about the specified proxy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/get_proxy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#get_proxy)
        """

    def get_proxy_attributes(
        self, **kwargs: Unpack[GetProxyAttributesRequestTypeDef]
    ) -> GetProxyAttributesResponseTypeDef:
        """
        Retrieves the attributes for the specified proxy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/get_proxy_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#get_proxy_attributes)
        """

    def get_proxy_configuration_contents(
        self, **kwargs: Unpack[GetProxyConfigurationContentsRequestTypeDef]
    ) -> GetProxyConfigurationContentsResponseTypeDef:
        """
        Retrieves the configuration file, the configuration archive, or both for the
        specified proxy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/get_proxy_configuration_contents.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#get_proxy_configuration_contents)
        """

    def get_proxy_update(
        self, **kwargs: Unpack[GetProxyUpdateRequestTypeDef]
    ) -> GetProxyUpdateResponseTypeDef:
        """
        Retrieves information about the specified proxy update.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/get_proxy_update.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#get_proxy_update)
        """

    def list_certificate_associations(
        self, **kwargs: Unpack[ListCertificateAssociationsRequestTypeDef]
    ) -> ListCertificateAssociationsResponseTypeDef:
        """
        Lists the ACM certificate associations for the specified proxy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/list_certificate_associations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#list_certificate_associations)
        """

    def list_proxies(
        self, **kwargs: Unpack[ListProxiesRequestTypeDef]
    ) -> ListProxiesResponseTypeDef:
        """
        Lists the proxies owned by the caller account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/list_proxies.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#list_proxies)
        """

    def list_proxy_updates(
        self, **kwargs: Unpack[ListProxyUpdatesRequestTypeDef]
    ) -> ListProxyUpdatesResponseTypeDef:
        """
        Lists the updates for the specified proxy, most recently submitted first.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/list_proxy_updates.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#list_proxy_updates)
        """

    def list_proxy_versions(
        self, **kwargs: Unpack[ListProxyVersionsRequestTypeDef]
    ) -> ListProxyVersionsResponseTypeDef:
        """
        Lists the available proxy versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/list_proxy_versions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#list_proxy_versions)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#list_tags_for_resource)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Adds the specified tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Removes the specified tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#untag_resource)
        """

    def update_proxy_attributes(
        self, **kwargs: Unpack[UpdateProxyAttributesRequestTypeDef]
    ) -> UpdateProxyAttributesResponseTypeDef:
        """
        Updates the attributes for the specified proxy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/update_proxy_attributes.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#update_proxy_attributes)
        """

    def update_proxy_configuration(
        self, **kwargs: Unpack[UpdateProxyConfigurationRequestTypeDef]
    ) -> UpdateProxyConfigurationResponseTypeDef:
        """
        Updates the configuration for the specified proxy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/update_proxy_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#update_proxy_configuration)
        """

    def update_proxy_network_configuration(
        self, **kwargs: Unpack[UpdateProxyNetworkConfigurationRequestTypeDef]
    ) -> UpdateProxyNetworkConfigurationResponseTypeDef:
        """
        Updates the network configuration for the specified proxy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/update_proxy_network_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#update_proxy_network_configuration)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_certificate_associations"]
    ) -> ListCertificateAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_proxies"]
    ) -> ListProxiesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_proxy_updates"]
    ) -> ListProxyUpdatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_proxy_versions"]
    ) -> ListProxyVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["proxy_active"]
    ) -> ProxyActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["proxy_deleted"]
    ) -> ProxyDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["proxy_update_complete"]
    ) -> ProxyUpdateCompleteWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elb-proxy/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_elb_proxy/client/#get_waiter)
        """
