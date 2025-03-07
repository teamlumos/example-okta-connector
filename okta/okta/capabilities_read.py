import logging
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
    ListResourcesRequest,
    ListResourcesResponse,
    Page,
    ValidateCredentialsRequest,
    ValidateCredentialsResponse,
    ValidatedCredentials,
    FoundEntitlementAssociation,
    FoundEntitlementData,
)
from connector.oai.capability import get_page, get_settings


from okta.models import UsersResponse
from okta.pagination import DEFAULT_PAGE_SIZE, NextPageToken, Pagination
from okta.settings import OktaSettings
from okta.client import OktaClient

logger = logging.getLogger(__name__)

async def validate_credentials(
    args: ValidateCredentialsRequest,
) -> ValidateCredentialsResponse:
    logger.info(f"Validating credentials")
    settings = get_settings(args, OktaSettings)
    async with OktaClient(args) as client:
        _ = await client.get_users()
        return ValidateCredentialsResponse(
            response=ValidatedCredentials(
                unique_tenant_id=settings.account_id,
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
    async with OktaClient(args) as client:
        response = await client.get_users(
            limit=page_size, after=current_pagination.after,
        )
        accounts: list[FoundAccountData] = response.to_accounts()

        next_pagination = []
        next_pagination.append(
            Pagination(
                endpoint=endpoint,
                after=response.after,
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

    page_size = get_page(args).size or DEFAULT_PAGE_SIZE
    entitlements: list[FoundEntitlementData] = []
    seen_entitlement_ids: set[str] = set()
    async with OktaClient(args) as client:
        response = await client.get_users(
            limit=page_size
        )
        entitlements, seen_entitlement_ids = await _get_entitlements_for_user(client, response, entitlements, seen_entitlement_ids)
        while response.after:
            response = await client.get_users(
                limit=page_size, after=response.after,
            )
            entitlements, seen_entitlement_ids = await _get_entitlements_for_user(client, response, entitlements, seen_entitlement_ids)

    return ListEntitlementsResponse(
        response=entitlements,
        page=None,
    )

async def _get_entitlements_for_user(
    client: OktaClient,
    response: UsersResponse,
    entitlements: list[FoundEntitlementData],
    seen_entitlement_ids: set[str],
) -> tuple[list[FoundEntitlementData], set[str]]:
    for user in response.to_accounts():
        roles_response = await client.get_user_roles(
            user_id=user.integration_specific_id,
        )
        single_user_entitlements: list[FoundEntitlementData] = roles_response.to_found_entitlement_data()
        for entitlement in single_user_entitlements:
            if entitlement.integration_specific_id not in seen_entitlement_ids:
                entitlements.append(entitlement)
                seen_entitlement_ids.add(entitlement.integration_specific_id)
    return entitlements, seen_entitlement_ids

async def find_entitlement_associations(
    args: FindEntitlementAssociationsRequest,
) -> FindEntitlementAssociationsResponse:
    users_endpoint = "/users"
    try:
        current_pagination = NextPageToken(get_page(args).token).paginations()[0]
    except IndexError:
        current_pagination = Pagination.default(users_endpoint)

    page_size = get_page(args).size or DEFAULT_PAGE_SIZE
    entitlement_associations: list[FoundEntitlementAssociation] = []
    async with OktaClient(args) as client:
        users_response = await client.get_users(
            limit=page_size, after=current_pagination.after,
        )
        for user in users_response.to_accounts():
            response = await client.get_user_roles(
                user_id=user.integration_specific_id,
            )
            logger.info(f"User roles: {response}")
            entitlements: list[FoundEntitlementAssociation] = response.to_found_entitlement_associations(user.integration_specific_id)
            entitlement_associations.extend(entitlements)

    next_pagination = []
    next_pagination.append(
            Pagination(
                endpoint=users_endpoint,
                after=users_response.after,
            )
        )

    next_page_token = NextPageToken.from_paginations(next_pagination).token
    return FindEntitlementAssociationsResponse(
        response=entitlement_associations,
        page=Page(
            token=next_page_token,
            size=page_size,
        )
    )

async def get_last_activity(args: GetLastActivityRequest) -> GetLastActivityResponse:
    raise NotImplementedError
