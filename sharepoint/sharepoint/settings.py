from connector.generated.models.o_auth_client_credential import OAuthClientCredential
from connector.serializers.request import HiddenField, SecretField
from pydantic import BaseModel, Field


class SharepointSettings(BaseModel):
    tenant_id: str = Field(
        title="Tenant ID",
        description=(
            "To get the Tenant ID follow these steps:\n"
            "1. Go to [Azure Portal](https://portal.azure.com/).\n"
            "2. Click on `Tenant properties` in `Azure services` section.\n"
            "3. Copy the `Tenant ID` and paste it below."
        ),
    )


class SharepointAuth(OAuthClientCredential):
    # Scopes from OAuth POV are not used as usual but are defined in Azure Portal, OAuth scopes are just this url.
    scopes: list[str] = HiddenField(
        title="Scopes", default=["https://graph.microsoft.com/.default"]
    )
    access_token: str = HiddenField(
        title="Access Token",
    )
    client_id: str = Field(
        title="Client ID",
        description=(
            "To get `Client ID` follow these steps:\n"
            "1. Go to [Azure Portal](https://portal.azure.com/).\n"
            "2. Click on `App registrations` in the `Azure services` section.\n"
            "3. Click on `New registration`.\n"
            "4. Choose a `Name` and in `Supported account types` select `Accounts in this organizational directory only (<your organization name> only - Single tenant)`\n"
            "5. Click on `Register`.\n"
            "6. Copy `Application (client) ID` and paste it below. (If you keep this site open after obtaining `Client ID` you can go to step 4 while obtaining `Client Secret`.)"
        ),
    )
    client_secret: str = SecretField(
        title="Client Secret",
        description=(
            "To get `Client Secret` first obtain `Client ID` in the previous sections and then follow these steps:\n"
            "1. Go to [Azure Portal](https://portal.azure.com/).\n"
            "2. Click on `App registrations` in the `Azure services` section.\n"
            "3. Click on `All applications` and choose the application that you have created while obtaining the `Client ID`.\n"
            "4. Click on `Add a certificate or secret` in the `Essentials` section.\n"
            "5. Click on `New client secret`.\n"
            "6. Fill out the `Description` and choose the `Expiration` (after expiration, you will need to create a new `Client Secret`).\n"
        ),
    )
