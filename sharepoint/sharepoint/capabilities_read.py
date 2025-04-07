from connector.generated import (
    FindEntitlementAssociationsRequest,
    FindEntitlementAssociationsResponse,
    GetLastActivityRequest,
    GetLastActivityResponse,
    ListAccountsRequest,
    ListAccountsResponse,
    ListEntitlementsRequest,
    ListEntitlementsResponse,
    ListResourcesRequest,
    ListResourcesResponse,
    ValidateCredentialsRequest,
    ValidateCredentialsResponse,
    ValidatedCredentials,
)


from sharepoint.client import SharepointClient
from sharepoint.settings import SharepointSettings

from connector.oai.capability import get_settings

async def validate_credentials(args: ValidateCredentialsRequest) -> ValidateCredentialsResponse:
    """
    Validate credentials by getting the tenant information using the tenant_id.
    """
    settings = get_settings(args, SharepointSettings)

    async with SharepointClient(args) as client:
        tenant_response = await client.get_tenant(tenant_id=settings.tenant_id)

        return ValidateCredentialsResponse(
            response=ValidatedCredentials(
                unique_tenant_id=tenant_response.tenant_id,
                valid=True,
            ),
        )

async def list_accounts(args: ListAccountsRequest) -> ListAccountsResponse:
    raise NotImplementedError


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
