import httpx
from connector.generated.models.app_category import AppCategory
from connector.oai.capability import AuthRequest, StandardCapabilityName, get_settings
from connector.oai.errors import HTTPHandler
from connector.oai.integration import DescriptionData, Integration
from connector.oai.modules.oauth_module_types import OAuthCapabilities, OAuthFlowType, OAuthSettings

from sharepoint import capabilities_read, capabilities_write
from sharepoint.__about__ import __version__
from sharepoint.enums import entitlement_types, resource_types
from sharepoint.settings import SharepointAuth, SharepointSettings


def get_token_url(args: AuthRequest) -> str:
    settings = get_settings(args, SharepointSettings)
    return f"https://login.microsoftonline.com/{settings.tenant_id}/oauth2/v2.0/token"


integration = Integration(
    app_id="sharepoint",
    version=__version__,
    # This should be an auth model inheriting from OAuthClientCredential
    auth=SharepointAuth,
    oauth_settings=OAuthSettings(
        # This determines which grant type is used to get the token
        flow_type=OAuthFlowType.CLIENT_CREDENTIALS,
        # This determines which capabilities are enabled, this should be set to False if refresh tokens are not issued
        # If set to true, we will make a request to the token URL to refresh the access token with grant_type=refresh_token
        capabilities=OAuthCapabilities(refresh_access_token=False),
        # This is a function returning the token URL that will be used to get the token
        token_url=get_token_url,
        # This is a mapping of capabilities to scopes required for the capability
        # In this case, sharepoint only has a single scope for all capabilities
        # Lumos will request the union of all scopes for the capabilities that are enabled
        scopes={
            StandardCapabilityName.VALIDATE_CREDENTIALS: "https://graph.microsoft.com/.default",
            StandardCapabilityName.LIST_ACCOUNTS: "https://graph.microsoft.com/.default",
            StandardCapabilityName.LIST_RESOURCES: "https://graph.microsoft.com/.default",
            StandardCapabilityName.LIST_ENTITLEMENTS: "https://graph.microsoft.com/.default",
            StandardCapabilityName.FIND_ENTITLEMENT_ASSOCIATIONS: "https://graph.microsoft.com/.default",
        },
    ),
    exception_handlers=[
        (httpx.HTTPStatusError, HTTPHandler, None),
    ],
    description_data=DescriptionData(
        logo_url="https://logo.clearbit.com/microsoft.sharepoint.com",
        user_friendly_name="Microsoft SharePoint",
        description="SharePoint is a collection of enterprise content management and knowledge management tools developed by Microsoft.",
        categories=[
            AppCategory.IT_AND_SECURITY,
            AppCategory.COLLABORATION,
            AppCategory.CONTENT_AND_SOCIAL_MEDIA,
        ],
    ),
    settings_model=SharepointSettings,
    resource_types=resource_types,
    entitlement_types=entitlement_types,
)

integration.register_capabilities(
    {
        # Read capabilities
        StandardCapabilityName.VALIDATE_CREDENTIALS: capabilities_read.validate_credentials,
        StandardCapabilityName.LIST_ACCOUNTS: capabilities_read.list_accounts,
        StandardCapabilityName.LIST_RESOURCES: capabilities_read.list_resources,
        StandardCapabilityName.LIST_ENTITLEMENTS: capabilities_read.list_entitlements,
        StandardCapabilityName.FIND_ENTITLEMENT_ASSOCIATIONS: capabilities_read.find_entitlement_associations,
        # Write capabilities
        StandardCapabilityName.ASSIGN_ENTITLEMENT: capabilities_write.assign_entitlement,
        StandardCapabilityName.UNASSIGN_ENTITLEMENT: capabilities_write.unassign_entitlement,
        StandardCapabilityName.CREATE_ACCOUNT: capabilities_write.create_account,
        StandardCapabilityName.ACTIVATE_ACCOUNT: capabilities_write.activate_account,
        StandardCapabilityName.DEACTIVATE_ACCOUNT: capabilities_write.deactivate_account,
        StandardCapabilityName.DELETE_ACCOUNT: capabilities_write.delete_account,
    }
)
