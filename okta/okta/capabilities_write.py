from connector.generated import (
    AssignEntitlementRequest,
    AssignEntitlementResponse,
    ActivateAccountRequest,
    ActivateAccountResponse,
    CreateAccountRequest,
    CreateAccountResponse,
    DeactivateAccountRequest,
    DeactivateAccountResponse,
    DeleteAccountRequest,
    DeleteAccountResponse,
    ListCustomAttributesSchemaRequest,
    ListCustomAttributesSchemaResponse,
    UnassignEntitlementRequest,
    UnassignEntitlementResponse,
    DeactivatedAccount,
    AccountStatus,
    ActivatedAccount,
)

from okta.client import OktaClient


async def assign_entitlement(args: AssignEntitlementRequest) -> AssignEntitlementResponse:
    raise NotImplementedError


async def unassign_entitlement(
    args: UnassignEntitlementRequest,
) -> UnassignEntitlementResponse:
    raise NotImplementedError


async def create_account(
    args: CreateAccountRequest,
) -> CreateAccountResponse:
    raise NotImplementedError


async def delete_account(
    args: DeleteAccountRequest,
) -> DeleteAccountResponse:
    raise NotImplementedError


async def activate_account(
    args: ActivateAccountRequest,
) -> ActivateAccountResponse:
    async with OktaClient(args) as client:
        user = await client.get_user(args.request.account_id)
        if user.status == "SUSPENDED":
            await client.unsuspend_user(args.request.account_id)
        elif user.status == "DEACTIVATED":
            await client.activate_user(args.request.account_id)
        elif user.status != "ACTIVE":
            raise ValueError(f"User is not in a valid state to be activated: {user.status}")
        return ActivateAccountResponse(
            response=ActivatedAccount(
                status=AccountStatus.ACTIVE,
                activated=True,
            ),
        )

async def deactivate_account(
    args: DeactivateAccountRequest,
) -> DeactivateAccountResponse:
    async with OktaClient(args) as client:
        await client.suspend_user(args.request.account_id)
        return DeactivateAccountResponse(
            response=DeactivatedAccount(
                status=AccountStatus.SUSPENDED,
                deactivated=True,
            ),
        )


async def list_custom_attributes_schema(
    args: ListCustomAttributesSchemaRequest,
) -> ListCustomAttributesSchemaResponse:
    raise NotImplementedError
