"""
Type annotations for route53domains service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_route53domains.client import Route53DomainsClient

    session = get_session()
    async with session.create_client("route53domains") as client:
        client: Route53DomainsClient
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
    ListDomainsPaginator,
    ListOperationsPaginator,
    ListPricesPaginator,
    ViewBillingPaginator,
)
from .type_defs import (
    AcceptDomainTransferFromAnotherAwsAccountRequestTypeDef,
    AcceptDomainTransferFromAnotherAwsAccountResponseTypeDef,
    AssociateDelegationSignerToDomainRequestTypeDef,
    AssociateDelegationSignerToDomainResponseTypeDef,
    CancelDomainTransferToAnotherAwsAccountRequestTypeDef,
    CancelDomainTransferToAnotherAwsAccountResponseTypeDef,
    CheckDomainAvailabilityRequestTypeDef,
    CheckDomainAvailabilityResponseTypeDef,
    CheckDomainTransferabilityRequestTypeDef,
    CheckDomainTransferabilityResponseTypeDef,
    DeleteDomainRequestTypeDef,
    DeleteDomainResponseTypeDef,
    DeleteTagsForDomainRequestTypeDef,
    DisableDomainAutoRenewRequestTypeDef,
    DisableDomainTransferLockRequestTypeDef,
    DisableDomainTransferLockResponseTypeDef,
    DisassociateDelegationSignerFromDomainRequestTypeDef,
    DisassociateDelegationSignerFromDomainResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableDomainAutoRenewRequestTypeDef,
    EnableDomainTransferLockRequestTypeDef,
    EnableDomainTransferLockResponseTypeDef,
    GetContactReachabilityStatusRequestTypeDef,
    GetContactReachabilityStatusResponseTypeDef,
    GetDomainDetailRequestTypeDef,
    GetDomainDetailResponseTypeDef,
    GetDomainSuggestionsRequestTypeDef,
    GetDomainSuggestionsResponseTypeDef,
    GetOperationDetailRequestTypeDef,
    GetOperationDetailResponseTypeDef,
    ListDomainsRequestTypeDef,
    ListDomainsResponseTypeDef,
    ListOperationsRequestTypeDef,
    ListOperationsResponseTypeDef,
    ListPricesRequestTypeDef,
    ListPricesResponseTypeDef,
    ListTagsForDomainRequestTypeDef,
    ListTagsForDomainResponseTypeDef,
    PushDomainRequestTypeDef,
    RegisterDomainRequestTypeDef,
    RegisterDomainResponseTypeDef,
    RejectDomainTransferFromAnotherAwsAccountRequestTypeDef,
    RejectDomainTransferFromAnotherAwsAccountResponseTypeDef,
    RenewDomainRequestTypeDef,
    RenewDomainResponseTypeDef,
    ResendContactReachabilityEmailRequestTypeDef,
    ResendContactReachabilityEmailResponseTypeDef,
    ResendOperationAuthorizationRequestTypeDef,
    RetrieveDomainAuthCodeRequestTypeDef,
    RetrieveDomainAuthCodeResponseTypeDef,
    TransferDomainRequestTypeDef,
    TransferDomainResponseTypeDef,
    TransferDomainToAnotherAwsAccountRequestTypeDef,
    TransferDomainToAnotherAwsAccountResponseTypeDef,
    UpdateDomainContactPrivacyRequestTypeDef,
    UpdateDomainContactPrivacyResponseTypeDef,
    UpdateDomainContactRequestTypeDef,
    UpdateDomainContactResponseTypeDef,
    UpdateDomainNameserversRequestTypeDef,
    UpdateDomainNameserversResponseTypeDef,
    UpdateTagsForDomainRequestTypeDef,
    ViewBillingRequestTypeDef,
    ViewBillingResponseTypeDef,
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


__all__ = ("Route53DomainsClient",)


class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    DnssecLimitExceeded: Type[BotocoreClientError]
    DomainLimitExceeded: Type[BotocoreClientError]
    DuplicateRequest: Type[BotocoreClientError]
    InvalidInput: Type[BotocoreClientError]
    OperationLimitExceeded: Type[BotocoreClientError]
    TLDRulesViolation: Type[BotocoreClientError]
    UnsupportedTLD: Type[BotocoreClientError]


class Route53DomainsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        Route53DomainsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#generate_presigned_url)
        """

    async def accept_domain_transfer_from_another_aws_account(
        self, **kwargs: Unpack[AcceptDomainTransferFromAnotherAwsAccountRequestTypeDef]
    ) -> AcceptDomainTransferFromAnotherAwsAccountResponseTypeDef:
        """
        Accepts the transfer of a domain from another Amazon Web Services account to
        the currentAmazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/accept_domain_transfer_from_another_aws_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#accept_domain_transfer_from_another_aws_account)
        """

    async def associate_delegation_signer_to_domain(
        self, **kwargs: Unpack[AssociateDelegationSignerToDomainRequestTypeDef]
    ) -> AssociateDelegationSignerToDomainResponseTypeDef:
        """
        Creates a delegation signer (DS) record in the registry zone for this domain
        name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/associate_delegation_signer_to_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#associate_delegation_signer_to_domain)
        """

    async def cancel_domain_transfer_to_another_aws_account(
        self, **kwargs: Unpack[CancelDomainTransferToAnotherAwsAccountRequestTypeDef]
    ) -> CancelDomainTransferToAnotherAwsAccountResponseTypeDef:
        """
        Cancels the transfer of a domain from the current Amazon Web Services account
        to another Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/cancel_domain_transfer_to_another_aws_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#cancel_domain_transfer_to_another_aws_account)
        """

    async def check_domain_availability(
        self, **kwargs: Unpack[CheckDomainAvailabilityRequestTypeDef]
    ) -> CheckDomainAvailabilityResponseTypeDef:
        """
        This operation checks the availability of one domain name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/check_domain_availability.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#check_domain_availability)
        """

    async def check_domain_transferability(
        self, **kwargs: Unpack[CheckDomainTransferabilityRequestTypeDef]
    ) -> CheckDomainTransferabilityResponseTypeDef:
        """
        Checks whether a domain name can be transferred to Amazon Route 53.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/check_domain_transferability.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#check_domain_transferability)
        """

    async def delete_domain(
        self, **kwargs: Unpack[DeleteDomainRequestTypeDef]
    ) -> DeleteDomainResponseTypeDef:
        """
        This operation deletes the specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/delete_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#delete_domain)
        """

    async def delete_tags_for_domain(
        self, **kwargs: Unpack[DeleteTagsForDomainRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This operation deletes the specified tags for a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/delete_tags_for_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#delete_tags_for_domain)
        """

    async def disable_domain_auto_renew(
        self, **kwargs: Unpack[DisableDomainAutoRenewRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This operation disables automatic renewal of domain registration for the
        specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/disable_domain_auto_renew.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#disable_domain_auto_renew)
        """

    async def disable_domain_transfer_lock(
        self, **kwargs: Unpack[DisableDomainTransferLockRequestTypeDef]
    ) -> DisableDomainTransferLockResponseTypeDef:
        """
        This operation removes the transfer lock on the domain (specifically the
        <code>clientTransferProhibited</code> status) to allow domain transfers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/disable_domain_transfer_lock.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#disable_domain_transfer_lock)
        """

    async def disassociate_delegation_signer_from_domain(
        self, **kwargs: Unpack[DisassociateDelegationSignerFromDomainRequestTypeDef]
    ) -> DisassociateDelegationSignerFromDomainResponseTypeDef:
        """
        Deletes a delegation signer (DS) record in the registry zone for this domain
        name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/disassociate_delegation_signer_from_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#disassociate_delegation_signer_from_domain)
        """

    async def enable_domain_auto_renew(
        self, **kwargs: Unpack[EnableDomainAutoRenewRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This operation configures Amazon Route 53 to automatically renew the specified
        domain before the domain registration expires.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/enable_domain_auto_renew.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#enable_domain_auto_renew)
        """

    async def enable_domain_transfer_lock(
        self, **kwargs: Unpack[EnableDomainTransferLockRequestTypeDef]
    ) -> EnableDomainTransferLockResponseTypeDef:
        """
        This operation sets the transfer lock on the domain (specifically the
        <code>clientTransferProhibited</code> status) to prevent domain transfers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/enable_domain_transfer_lock.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#enable_domain_transfer_lock)
        """

    async def get_contact_reachability_status(
        self, **kwargs: Unpack[GetContactReachabilityStatusRequestTypeDef]
    ) -> GetContactReachabilityStatusResponseTypeDef:
        """
        For operations that require confirmation that the email address for the
        registrant contact is valid, such as registering a new domain, this operation
        returns information about whether the registrant contact has responded.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/get_contact_reachability_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#get_contact_reachability_status)
        """

    async def get_domain_detail(
        self, **kwargs: Unpack[GetDomainDetailRequestTypeDef]
    ) -> GetDomainDetailResponseTypeDef:
        """
        This operation returns detailed information about a specified domain that is
        associated with the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/get_domain_detail.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#get_domain_detail)
        """

    async def get_domain_suggestions(
        self, **kwargs: Unpack[GetDomainSuggestionsRequestTypeDef]
    ) -> GetDomainSuggestionsResponseTypeDef:
        """
        The GetDomainSuggestions operation returns a list of suggested domain names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/get_domain_suggestions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#get_domain_suggestions)
        """

    async def get_operation_detail(
        self, **kwargs: Unpack[GetOperationDetailRequestTypeDef]
    ) -> GetOperationDetailResponseTypeDef:
        """
        This operation returns the current status of an operation that is not completed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/get_operation_detail.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#get_operation_detail)
        """

    async def list_domains(
        self, **kwargs: Unpack[ListDomainsRequestTypeDef]
    ) -> ListDomainsResponseTypeDef:
        """
        This operation returns all the domain names registered with Amazon Route 53 for
        the current Amazon Web Services account if no filtering conditions are used.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/list_domains.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#list_domains)
        """

    async def list_operations(
        self, **kwargs: Unpack[ListOperationsRequestTypeDef]
    ) -> ListOperationsResponseTypeDef:
        """
        Returns information about all of the operations that return an operation ID and
        that have ever been performed on domains that were registered by the current
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/list_operations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#list_operations)
        """

    async def list_prices(
        self, **kwargs: Unpack[ListPricesRequestTypeDef]
    ) -> ListPricesResponseTypeDef:
        """
        Lists the following prices for either all the TLDs supported by Route 53, or
        the specified TLD:.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/list_prices.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#list_prices)
        """

    async def list_tags_for_domain(
        self, **kwargs: Unpack[ListTagsForDomainRequestTypeDef]
    ) -> ListTagsForDomainResponseTypeDef:
        """
        This operation returns all of the tags that are associated with the specified
        domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/list_tags_for_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#list_tags_for_domain)
        """

    async def push_domain(
        self, **kwargs: Unpack[PushDomainRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Moves a domain from Amazon Web Services to another registrar.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/push_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#push_domain)
        """

    async def register_domain(
        self, **kwargs: Unpack[RegisterDomainRequestTypeDef]
    ) -> RegisterDomainResponseTypeDef:
        """
        This operation registers a domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/register_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#register_domain)
        """

    async def reject_domain_transfer_from_another_aws_account(
        self, **kwargs: Unpack[RejectDomainTransferFromAnotherAwsAccountRequestTypeDef]
    ) -> RejectDomainTransferFromAnotherAwsAccountResponseTypeDef:
        """
        Rejects the transfer of a domain from another Amazon Web Services account to
        the current Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/reject_domain_transfer_from_another_aws_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#reject_domain_transfer_from_another_aws_account)
        """

    async def renew_domain(
        self, **kwargs: Unpack[RenewDomainRequestTypeDef]
    ) -> RenewDomainResponseTypeDef:
        """
        This operation renews a domain for the specified number of years.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/renew_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#renew_domain)
        """

    async def resend_contact_reachability_email(
        self, **kwargs: Unpack[ResendContactReachabilityEmailRequestTypeDef]
    ) -> ResendContactReachabilityEmailResponseTypeDef:
        """
        For operations that require confirmation that the email address for the
        registrant contact is valid, such as registering a new domain, this operation
        resends the confirmation email to the current email address for the registrant
        contact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/resend_contact_reachability_email.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#resend_contact_reachability_email)
        """

    async def resend_operation_authorization(
        self, **kwargs: Unpack[ResendOperationAuthorizationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Resend the form of authorization email for this operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/resend_operation_authorization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#resend_operation_authorization)
        """

    async def retrieve_domain_auth_code(
        self, **kwargs: Unpack[RetrieveDomainAuthCodeRequestTypeDef]
    ) -> RetrieveDomainAuthCodeResponseTypeDef:
        """
        This operation returns the authorization code for the domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/retrieve_domain_auth_code.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#retrieve_domain_auth_code)
        """

    async def transfer_domain(
        self, **kwargs: Unpack[TransferDomainRequestTypeDef]
    ) -> TransferDomainResponseTypeDef:
        """
        Transfers a domain from another registrar to Amazon Route 53.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/transfer_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#transfer_domain)
        """

    async def transfer_domain_to_another_aws_account(
        self, **kwargs: Unpack[TransferDomainToAnotherAwsAccountRequestTypeDef]
    ) -> TransferDomainToAnotherAwsAccountResponseTypeDef:
        """
        Transfers a domain from the current Amazon Web Services account to another
        Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/transfer_domain_to_another_aws_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#transfer_domain_to_another_aws_account)
        """

    async def update_domain_contact(
        self, **kwargs: Unpack[UpdateDomainContactRequestTypeDef]
    ) -> UpdateDomainContactResponseTypeDef:
        """
        This operation updates the contact information for a particular domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/update_domain_contact.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#update_domain_contact)
        """

    async def update_domain_contact_privacy(
        self, **kwargs: Unpack[UpdateDomainContactPrivacyRequestTypeDef]
    ) -> UpdateDomainContactPrivacyResponseTypeDef:
        """
        This operation updates the specified domain contact's privacy setting.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/update_domain_contact_privacy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#update_domain_contact_privacy)
        """

    async def update_domain_nameservers(
        self, **kwargs: Unpack[UpdateDomainNameserversRequestTypeDef]
    ) -> UpdateDomainNameserversResponseTypeDef:
        """
        This operation replaces the current set of name servers for the domain with the
        specified set of name servers.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/update_domain_nameservers.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#update_domain_nameservers)
        """

    async def update_tags_for_domain(
        self, **kwargs: Unpack[UpdateTagsForDomainRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        This operation adds or updates tags for a specified domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/update_tags_for_domain.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#update_tags_for_domain)
        """

    async def view_billing(
        self, **kwargs: Unpack[ViewBillingRequestTypeDef]
    ) -> ViewBillingResponseTypeDef:
        """
        Returns all the domain-related billing records for the current Amazon Web
        Services account for a specified period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/view_billing.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#view_billing)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_domains"]
    ) -> ListDomainsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_operations"]
    ) -> ListOperationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_prices"]
    ) -> ListPricesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["view_billing"]
    ) -> ViewBillingPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53domains.html#Route53Domains.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53domains/client/)
        """
