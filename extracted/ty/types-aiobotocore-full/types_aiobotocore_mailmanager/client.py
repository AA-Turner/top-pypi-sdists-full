"""
Type annotations for mailmanager service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mailmanager.client import MailManagerClient

    session = get_session()
    async with session.create_client("mailmanager") as client:
        client: MailManagerClient
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
    ListAddonInstancesPaginator,
    ListAddonSubscriptionsPaginator,
    ListAddressListImportJobsPaginator,
    ListAddressListsPaginator,
    ListArchiveExportsPaginator,
    ListArchiveSearchesPaginator,
    ListArchivesPaginator,
    ListIngressPointsPaginator,
    ListMembersOfAddressListPaginator,
    ListRelaysPaginator,
    ListRuleSetsPaginator,
    ListTrafficPoliciesPaginator,
)
from .type_defs import (
    CreateAddonInstanceRequestTypeDef,
    CreateAddonInstanceResponseTypeDef,
    CreateAddonSubscriptionRequestTypeDef,
    CreateAddonSubscriptionResponseTypeDef,
    CreateAddressListImportJobRequestTypeDef,
    CreateAddressListImportJobResponseTypeDef,
    CreateAddressListRequestTypeDef,
    CreateAddressListResponseTypeDef,
    CreateArchiveRequestTypeDef,
    CreateArchiveResponseTypeDef,
    CreateIngressPointRequestTypeDef,
    CreateIngressPointResponseTypeDef,
    CreateRelayRequestTypeDef,
    CreateRelayResponseTypeDef,
    CreateRuleSetRequestTypeDef,
    CreateRuleSetResponseTypeDef,
    CreateTrafficPolicyRequestTypeDef,
    CreateTrafficPolicyResponseTypeDef,
    DeleteAddonInstanceRequestTypeDef,
    DeleteAddonSubscriptionRequestTypeDef,
    DeleteAddressListRequestTypeDef,
    DeleteArchiveRequestTypeDef,
    DeleteIngressPointRequestTypeDef,
    DeleteRelayRequestTypeDef,
    DeleteRuleSetRequestTypeDef,
    DeleteTrafficPolicyRequestTypeDef,
    DeregisterMemberFromAddressListRequestTypeDef,
    GetAddonInstanceRequestTypeDef,
    GetAddonInstanceResponseTypeDef,
    GetAddonSubscriptionRequestTypeDef,
    GetAddonSubscriptionResponseTypeDef,
    GetAddressListImportJobRequestTypeDef,
    GetAddressListImportJobResponseTypeDef,
    GetAddressListRequestTypeDef,
    GetAddressListResponseTypeDef,
    GetArchiveExportRequestTypeDef,
    GetArchiveExportResponseTypeDef,
    GetArchiveMessageContentRequestTypeDef,
    GetArchiveMessageContentResponseTypeDef,
    GetArchiveMessageRequestTypeDef,
    GetArchiveMessageResponseTypeDef,
    GetArchiveRequestTypeDef,
    GetArchiveResponseTypeDef,
    GetArchiveSearchRequestTypeDef,
    GetArchiveSearchResponseTypeDef,
    GetArchiveSearchResultsRequestTypeDef,
    GetArchiveSearchResultsResponseTypeDef,
    GetIngressPointRequestTypeDef,
    GetIngressPointResponseTypeDef,
    GetMemberOfAddressListRequestTypeDef,
    GetMemberOfAddressListResponseTypeDef,
    GetRelayRequestTypeDef,
    GetRelayResponseTypeDef,
    GetRuleSetRequestTypeDef,
    GetRuleSetResponseTypeDef,
    GetTrafficPolicyRequestTypeDef,
    GetTrafficPolicyResponseTypeDef,
    ListAddonInstancesRequestTypeDef,
    ListAddonInstancesResponseTypeDef,
    ListAddonSubscriptionsRequestTypeDef,
    ListAddonSubscriptionsResponseTypeDef,
    ListAddressListImportJobsRequestTypeDef,
    ListAddressListImportJobsResponseTypeDef,
    ListAddressListsRequestTypeDef,
    ListAddressListsResponseTypeDef,
    ListArchiveExportsRequestTypeDef,
    ListArchiveExportsResponseTypeDef,
    ListArchiveSearchesRequestTypeDef,
    ListArchiveSearchesResponseTypeDef,
    ListArchivesRequestTypeDef,
    ListArchivesResponseTypeDef,
    ListIngressPointsRequestTypeDef,
    ListIngressPointsResponseTypeDef,
    ListMembersOfAddressListRequestTypeDef,
    ListMembersOfAddressListResponseTypeDef,
    ListRelaysRequestTypeDef,
    ListRelaysResponseTypeDef,
    ListRuleSetsRequestTypeDef,
    ListRuleSetsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTrafficPoliciesRequestTypeDef,
    ListTrafficPoliciesResponseTypeDef,
    RegisterMemberToAddressListRequestTypeDef,
    StartAddressListImportJobRequestTypeDef,
    StartArchiveExportRequestTypeDef,
    StartArchiveExportResponseTypeDef,
    StartArchiveSearchRequestTypeDef,
    StartArchiveSearchResponseTypeDef,
    StopAddressListImportJobRequestTypeDef,
    StopArchiveExportRequestTypeDef,
    StopArchiveSearchRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateArchiveRequestTypeDef,
    UpdateIngressPointRequestTypeDef,
    UpdateRelayRequestTypeDef,
    UpdateRuleSetRequestTypeDef,
    UpdateTrafficPolicyRequestTypeDef,
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


__all__ = ("MailManagerClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class MailManagerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager.html#MailManager.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MailManagerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager.html#MailManager.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#generate_presigned_url)
        """

    async def create_addon_instance(
        self, **kwargs: Unpack[CreateAddonInstanceRequestTypeDef]
    ) -> CreateAddonInstanceResponseTypeDef:
        """
        Creates an Add On instance for the subscription indicated in the request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_addon_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#create_addon_instance)
        """

    async def create_addon_subscription(
        self, **kwargs: Unpack[CreateAddonSubscriptionRequestTypeDef]
    ) -> CreateAddonSubscriptionResponseTypeDef:
        """
        Creates a subscription for an Add On representing the acceptance of its terms
        of use and additional pricing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_addon_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#create_addon_subscription)
        """

    async def create_address_list(
        self, **kwargs: Unpack[CreateAddressListRequestTypeDef]
    ) -> CreateAddressListResponseTypeDef:
        """
        Creates a new address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_address_list.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#create_address_list)
        """

    async def create_address_list_import_job(
        self, **kwargs: Unpack[CreateAddressListImportJobRequestTypeDef]
    ) -> CreateAddressListImportJobResponseTypeDef:
        """
        Creates an import job for an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_address_list_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#create_address_list_import_job)
        """

    async def create_archive(
        self, **kwargs: Unpack[CreateArchiveRequestTypeDef]
    ) -> CreateArchiveResponseTypeDef:
        """
        Creates a new email archive resource for storing and retaining emails.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_archive.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#create_archive)
        """

    async def create_ingress_point(
        self, **kwargs: Unpack[CreateIngressPointRequestTypeDef]
    ) -> CreateIngressPointResponseTypeDef:
        """
        Provision a new ingress endpoint resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_ingress_point.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#create_ingress_point)
        """

    async def create_relay(
        self, **kwargs: Unpack[CreateRelayRequestTypeDef]
    ) -> CreateRelayResponseTypeDef:
        """
        Creates a relay resource which can be used in rules to relay incoming emails to
        defined relay destinations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_relay.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#create_relay)
        """

    async def create_rule_set(
        self, **kwargs: Unpack[CreateRuleSetRequestTypeDef]
    ) -> CreateRuleSetResponseTypeDef:
        """
        Provision a new rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_rule_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#create_rule_set)
        """

    async def create_traffic_policy(
        self, **kwargs: Unpack[CreateTrafficPolicyRequestTypeDef]
    ) -> CreateTrafficPolicyResponseTypeDef:
        """
        Provision a new traffic policy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/create_traffic_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#create_traffic_policy)
        """

    async def delete_addon_instance(
        self, **kwargs: Unpack[DeleteAddonInstanceRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Add On instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_addon_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#delete_addon_instance)
        """

    async def delete_addon_subscription(
        self, **kwargs: Unpack[DeleteAddonSubscriptionRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an Add On subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_addon_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#delete_addon_subscription)
        """

    async def delete_address_list(
        self, **kwargs: Unpack[DeleteAddressListRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_address_list.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#delete_address_list)
        """

    async def delete_archive(self, **kwargs: Unpack[DeleteArchiveRequestTypeDef]) -> Dict[str, Any]:
        """
        Initiates deletion of an email archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_archive.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#delete_archive)
        """

    async def delete_ingress_point(
        self, **kwargs: Unpack[DeleteIngressPointRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete an ingress endpoint resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_ingress_point.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#delete_ingress_point)
        """

    async def delete_relay(self, **kwargs: Unpack[DeleteRelayRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes an existing relay resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_relay.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#delete_relay)
        """

    async def delete_rule_set(
        self, **kwargs: Unpack[DeleteRuleSetRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete a rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_rule_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#delete_rule_set)
        """

    async def delete_traffic_policy(
        self, **kwargs: Unpack[DeleteTrafficPolicyRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Delete a traffic policy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/delete_traffic_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#delete_traffic_policy)
        """

    async def deregister_member_from_address_list(
        self, **kwargs: Unpack[DeregisterMemberFromAddressListRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a member from an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/deregister_member_from_address_list.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#deregister_member_from_address_list)
        """

    async def get_addon_instance(
        self, **kwargs: Unpack[GetAddonInstanceRequestTypeDef]
    ) -> GetAddonInstanceResponseTypeDef:
        """
        Gets detailed information about an Add On instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_addon_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_addon_instance)
        """

    async def get_addon_subscription(
        self, **kwargs: Unpack[GetAddonSubscriptionRequestTypeDef]
    ) -> GetAddonSubscriptionResponseTypeDef:
        """
        Gets detailed information about an Add On subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_addon_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_addon_subscription)
        """

    async def get_address_list(
        self, **kwargs: Unpack[GetAddressListRequestTypeDef]
    ) -> GetAddressListResponseTypeDef:
        """
        Fetch attributes of an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_address_list.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_address_list)
        """

    async def get_address_list_import_job(
        self, **kwargs: Unpack[GetAddressListImportJobRequestTypeDef]
    ) -> GetAddressListImportJobResponseTypeDef:
        """
        Fetch attributes of an import job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_address_list_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_address_list_import_job)
        """

    async def get_archive(
        self, **kwargs: Unpack[GetArchiveRequestTypeDef]
    ) -> GetArchiveResponseTypeDef:
        """
        Retrieves the full details and current state of a specified email archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_archive.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_archive)
        """

    async def get_archive_export(
        self, **kwargs: Unpack[GetArchiveExportRequestTypeDef]
    ) -> GetArchiveExportResponseTypeDef:
        """
        Retrieves the details and current status of a specific email archive export job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_archive_export.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_archive_export)
        """

    async def get_archive_message(
        self, **kwargs: Unpack[GetArchiveMessageRequestTypeDef]
    ) -> GetArchiveMessageResponseTypeDef:
        """
        Returns a pre-signed URL that provides temporary download access to the
        specific email message stored in the archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_archive_message.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_archive_message)
        """

    async def get_archive_message_content(
        self, **kwargs: Unpack[GetArchiveMessageContentRequestTypeDef]
    ) -> GetArchiveMessageContentResponseTypeDef:
        """
        Returns the textual content of a specific email message stored in the archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_archive_message_content.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_archive_message_content)
        """

    async def get_archive_search(
        self, **kwargs: Unpack[GetArchiveSearchRequestTypeDef]
    ) -> GetArchiveSearchResponseTypeDef:
        """
        Retrieves the details and current status of a specific email archive search job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_archive_search.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_archive_search)
        """

    async def get_archive_search_results(
        self, **kwargs: Unpack[GetArchiveSearchResultsRequestTypeDef]
    ) -> GetArchiveSearchResultsResponseTypeDef:
        """
        Returns the results of a completed email archive search job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_archive_search_results.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_archive_search_results)
        """

    async def get_ingress_point(
        self, **kwargs: Unpack[GetIngressPointRequestTypeDef]
    ) -> GetIngressPointResponseTypeDef:
        """
        Fetch ingress endpoint resource attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_ingress_point.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_ingress_point)
        """

    async def get_member_of_address_list(
        self, **kwargs: Unpack[GetMemberOfAddressListRequestTypeDef]
    ) -> GetMemberOfAddressListResponseTypeDef:
        """
        Fetch attributes of a member in an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_member_of_address_list.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_member_of_address_list)
        """

    async def get_relay(self, **kwargs: Unpack[GetRelayRequestTypeDef]) -> GetRelayResponseTypeDef:
        """
        Fetch the relay resource and it's attributes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_relay.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_relay)
        """

    async def get_rule_set(
        self, **kwargs: Unpack[GetRuleSetRequestTypeDef]
    ) -> GetRuleSetResponseTypeDef:
        """
        Fetch attributes of a rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_rule_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_rule_set)
        """

    async def get_traffic_policy(
        self, **kwargs: Unpack[GetTrafficPolicyRequestTypeDef]
    ) -> GetTrafficPolicyResponseTypeDef:
        """
        Fetch attributes of a traffic policy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_traffic_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_traffic_policy)
        """

    async def list_addon_instances(
        self, **kwargs: Unpack[ListAddonInstancesRequestTypeDef]
    ) -> ListAddonInstancesResponseTypeDef:
        """
        Lists all Add On instances in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_addon_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_addon_instances)
        """

    async def list_addon_subscriptions(
        self, **kwargs: Unpack[ListAddonSubscriptionsRequestTypeDef]
    ) -> ListAddonSubscriptionsResponseTypeDef:
        """
        Lists all Add On subscriptions in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_addon_subscriptions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_addon_subscriptions)
        """

    async def list_address_list_import_jobs(
        self, **kwargs: Unpack[ListAddressListImportJobsRequestTypeDef]
    ) -> ListAddressListImportJobsResponseTypeDef:
        """
        Lists jobs for an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_address_list_import_jobs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_address_list_import_jobs)
        """

    async def list_address_lists(
        self, **kwargs: Unpack[ListAddressListsRequestTypeDef]
    ) -> ListAddressListsResponseTypeDef:
        """
        Lists address lists for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_address_lists.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_address_lists)
        """

    async def list_archive_exports(
        self, **kwargs: Unpack[ListArchiveExportsRequestTypeDef]
    ) -> ListArchiveExportsResponseTypeDef:
        """
        Returns a list of email archive export jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_archive_exports.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_archive_exports)
        """

    async def list_archive_searches(
        self, **kwargs: Unpack[ListArchiveSearchesRequestTypeDef]
    ) -> ListArchiveSearchesResponseTypeDef:
        """
        Returns a list of email archive search jobs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_archive_searches.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_archive_searches)
        """

    async def list_archives(
        self, **kwargs: Unpack[ListArchivesRequestTypeDef]
    ) -> ListArchivesResponseTypeDef:
        """
        Returns a list of all email archives in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_archives.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_archives)
        """

    async def list_ingress_points(
        self, **kwargs: Unpack[ListIngressPointsRequestTypeDef]
    ) -> ListIngressPointsResponseTypeDef:
        """
        List all ingress endpoint resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_ingress_points.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_ingress_points)
        """

    async def list_members_of_address_list(
        self, **kwargs: Unpack[ListMembersOfAddressListRequestTypeDef]
    ) -> ListMembersOfAddressListResponseTypeDef:
        """
        Lists members of an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_members_of_address_list.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_members_of_address_list)
        """

    async def list_relays(
        self, **kwargs: Unpack[ListRelaysRequestTypeDef]
    ) -> ListRelaysResponseTypeDef:
        """
        Lists all the existing relay resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_relays.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_relays)
        """

    async def list_rule_sets(
        self, **kwargs: Unpack[ListRuleSetsRequestTypeDef]
    ) -> ListRuleSetsResponseTypeDef:
        """
        List rule sets for this account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_rule_sets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_rule_sets)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves the list of tags (keys and values) assigned to the resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_tags_for_resource)
        """

    async def list_traffic_policies(
        self, **kwargs: Unpack[ListTrafficPoliciesRequestTypeDef]
    ) -> ListTrafficPoliciesResponseTypeDef:
        """
        List traffic policy resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/list_traffic_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#list_traffic_policies)
        """

    async def register_member_to_address_list(
        self, **kwargs: Unpack[RegisterMemberToAddressListRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds a member to an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/register_member_to_address_list.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#register_member_to_address_list)
        """

    async def start_address_list_import_job(
        self, **kwargs: Unpack[StartAddressListImportJobRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Starts an import job for an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/start_address_list_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#start_address_list_import_job)
        """

    async def start_archive_export(
        self, **kwargs: Unpack[StartArchiveExportRequestTypeDef]
    ) -> StartArchiveExportResponseTypeDef:
        """
        Initiates an export of emails from the specified archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/start_archive_export.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#start_archive_export)
        """

    async def start_archive_search(
        self, **kwargs: Unpack[StartArchiveSearchRequestTypeDef]
    ) -> StartArchiveSearchResponseTypeDef:
        """
        Initiates a search across emails in the specified archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/start_archive_search.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#start_archive_search)
        """

    async def stop_address_list_import_job(
        self, **kwargs: Unpack[StopAddressListImportJobRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops an ongoing import job for an address list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/stop_address_list_import_job.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#stop_address_list_import_job)
        """

    async def stop_archive_export(
        self, **kwargs: Unpack[StopArchiveExportRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops an in-progress export of emails from an archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/stop_archive_export.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#stop_archive_export)
        """

    async def stop_archive_search(
        self, **kwargs: Unpack[StopArchiveSearchRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stops an in-progress archive search job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/stop_archive_search.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#stop_archive_search)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags (keys and values) to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Remove one or more tags (keys and values) from a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#untag_resource)
        """

    async def update_archive(self, **kwargs: Unpack[UpdateArchiveRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates the attributes of an existing email archive.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/update_archive.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#update_archive)
        """

    async def update_ingress_point(
        self, **kwargs: Unpack[UpdateIngressPointRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update attributes of a provisioned ingress endpoint resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/update_ingress_point.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#update_ingress_point)
        """

    async def update_relay(self, **kwargs: Unpack[UpdateRelayRequestTypeDef]) -> Dict[str, Any]:
        """
        Updates the attributes of an existing relay resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/update_relay.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#update_relay)
        """

    async def update_rule_set(
        self, **kwargs: Unpack[UpdateRuleSetRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update attributes of an already provisioned rule set.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/update_rule_set.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#update_rule_set)
        """

    async def update_traffic_policy(
        self, **kwargs: Unpack[UpdateTrafficPolicyRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Update attributes of an already provisioned traffic policy resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/update_traffic_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#update_traffic_policy)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_addon_instances"]
    ) -> ListAddonInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_addon_subscriptions"]
    ) -> ListAddonSubscriptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_address_list_import_jobs"]
    ) -> ListAddressListImportJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_address_lists"]
    ) -> ListAddressListsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_archive_exports"]
    ) -> ListArchiveExportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_archive_searches"]
    ) -> ListArchiveSearchesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_archives"]
    ) -> ListArchivesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_ingress_points"]
    ) -> ListIngressPointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_members_of_address_list"]
    ) -> ListMembersOfAddressListPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_relays"]
    ) -> ListRelaysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_rule_sets"]
    ) -> ListRuleSetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_traffic_policies"]
    ) -> ListTrafficPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager.html#MailManager.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mailmanager.html#MailManager.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mailmanager/client/)
        """
