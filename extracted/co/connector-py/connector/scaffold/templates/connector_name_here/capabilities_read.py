from connector.client import get_page
from connector.generated import (
    FindEntitlementAssociationsRequest,
    FindEntitlementAssociationsResponse,
    FoundAccountData,
    GetLastActivityRequest,
    GetLastActivityResponse,
    ListAccountsRequest,
    ListAccountsResponse,
    ListCustomAttributesSchemaRequest,
    ListCustomAttributesSchemaResponse,
    ListEntitlementsRequest,
    ListEntitlementsResponse,
    ListResourcesRequest,
    ListResourcesResponse,
    Page,
    ValidateCredentialsRequest,
    ValidateCredentialsResponse,
    ValidatedCredentials,
)

from {name}.client import {pascal}Client
from {name}.pagination import DEFAULT_PAGE_SIZE, NextPageToken, Pagination, paginations_from_args

async def validate_credentials(
    args: ValidateCredentialsRequest,
) -> ValidateCredentialsResponse:
    async with {pascal}Client(args) as client:
        # _ = await client.get_users()

        return ValidateCredentialsResponse(
            response=ValidatedCredentials(
                unique_tenant_id="REPLACE_WITH_UNIQUE_TENANT_ID",
                valid=True,
            ),
        )


async def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
    paginations, current_pagination, page_size = paginations_from_args(
        args, default_endpoints=["/users"]
    )

    async with {pascal}Client(args) as client:
        response = await client.get_users(
            limit=page_size,
            offset=current_pagination.offset,
        )
        accounts: list[FoundAccountData] = response.to_accounts()

        if True:
            paginations.append(
                Pagination(
                    endpoint=current_pagination.endpoint,
                    offset=current_pagination.offset + len(accounts),
                )
            )

    return ListAccountsResponse(
        response=accounts,
        page=NextPageToken.from_paginations(paginations).to_page(page_size)
        if paginations
        else None,
    )


async def list_resources(args: ListResourcesRequest) -> ListResourcesResponse:
    raise NotImplementedError  # pragma: no cover


async def list_entitlements(
    args: ListEntitlementsRequest,
) -> ListEntitlementsResponse:
    raise NotImplementedError  # pragma: no cover


async def find_entitlement_associations(
    args: FindEntitlementAssociationsRequest,
) -> FindEntitlementAssociationsResponse:
    raise NotImplementedError  # pragma: no cover


async def get_last_activity(args: GetLastActivityRequest) -> GetLastActivityResponse:
    raise NotImplementedError  # pragma: no cover


async def list_custom_attributes_schema(
    args: ListCustomAttributesSchemaRequest,
) -> ListCustomAttributesSchemaResponse:
    raise NotImplementedError  # pragma: no cover
