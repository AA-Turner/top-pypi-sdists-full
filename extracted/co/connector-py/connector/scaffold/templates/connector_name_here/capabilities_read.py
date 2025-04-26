from connector.generated import (
    FindEntitlementAssociationsRequest,
    FindEntitlementAssociationsResponse,
    FoundAccountData,
    GetLastActivityRequest,
    GetLastActivityResponse,
    ListAccountsRequest,
    ListAccountsResponse,
    ListEntitlementsRequest,
    ListEntitlementsResponse,
    ListCustomAttributesSchemaRequest,
    ListCustomAttributesSchemaResponse,
    ListResourcesRequest,
    ListResourcesResponse,
    Page,
    ValidateCredentialsRequest,
    ValidateCredentialsResponse,
    ValidatedCredentials,
)
from connector.oai.capability import get_page, get_settings


from {name}.pagination import DEFAULT_PAGE_SIZE, NextPageToken, Pagination
from {name}.settings import {pascal}Settings
from {name}.client import {pascal}Client

async def validate_credentials(
    args: ValidateCredentialsRequest,
) -> ValidateCredentialsResponse:
    async with {pascal}Client(args) as client:
        #_ = await client.get_users()

        return ValidateCredentialsResponse(
            response=ValidatedCredentials(
                unique_tenant_id="REPLACE_WITH_UNIQUE_TENANT_ID",
                valid=True,
            ),
        )


async def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
    endpoint = "/users"
    try:
        current_pagination = NextPageToken(get_page(args).token).paginations()[0]
    except IndexError:
        current_pagination = Pagination.default(endpoint)

    page_size = get_page(args).size or DEFAULT_PAGE_SIZE
    async with {pascal}Client(args) as client:
        response = await client.get_users(
            limit=page_size, offset=current_pagination.offset,
        )
        accounts: list[FoundAccountData] = response.to_accounts()

        next_pagination = []
        if True:
            next_pagination.append(
                Pagination(
                    endpoint=endpoint,
                    offset=current_pagination.offset + len(accounts),
                )
            )

        next_page_token = NextPageToken.from_paginations(next_pagination).token

    return ListAccountsResponse(
        response=accounts,
        page=Page(
            token=next_page_token,
            size=page_size,
        )
        if next_page_token
        else None,
    )


async def list_resources(args: ListResourcesRequest) -> ListResourcesResponse:
    raise NotImplementedError


async def list_entitlements(
    args: ListEntitlementsRequest,
) -> ListEntitlementsResponse:
    raise NotImplementedError


async def find_entitlement_associations(
    args: FindEntitlementAssociationsRequest,
) -> FindEntitlementAssociationsResponse:
    raise NotImplementedError


async def get_last_activity(args: GetLastActivityRequest) -> GetLastActivityResponse:
    raise NotImplementedError


async def list_custom_attributes_schema(
    args: ListCustomAttributesSchemaRequest,
) -> ListCustomAttributesSchemaResponse:
    raise NotImplementedError
