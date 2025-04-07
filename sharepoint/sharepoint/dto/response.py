from typing import Any, Generic, TypeVar

from connector.generated import (
    FoundAccountData,
    FoundEntitlementAssociation,
    FoundEntitlementData,
    FoundResourceData,
)
from httpx import URL
from pydantic import BaseModel, Field, field_validator

T = TypeVar("T")
U = TypeVar("U", FoundResourceData, FoundEntitlementData, FoundEntitlementAssociation)


class TenantResponse(BaseModel):
    tenant_id: str = Field(validation_alias="tenantId")
    domain_name: str = Field(validation_alias="defaultDomainName")


class APIPaginatedResponse(BaseModel, Generic[T]):
    """Generic model for Sharepoint response"""

    value: list[T] = []
    skip_token: str | None = Field(default=None, validation_alias="@odata.nextLink")

    @field_validator("skip_token")
    @classmethod
    def extract_skip_token(cls, url: str | None) -> str | None:
        if url is None or not isinstance(url, str):
            return None

        return URL(url).params.get("$skiptoken")

    @property
    def ids(self) -> list[str]:
        return [item.id for item in self.value]


class LumosPaginatedResponse(BaseModel, Generic[U]):
    items: list[U] = []
    page_size: int

    @property
    def to_full(self) -> int:
        """Return the number of additional items required to fill the page"""
        return self.page_size - len(self.items)
