import typing as t
from collections.abc import Awaitable, Callable

from connector.oai.base_clients import BaseIntegrationClient
from connector.oai.capability import Request, get_oauth
from connector.utils.client_utils import DTO, create_client_response
from connector.utils.httpx_auth import BearerAuth

from sharepoint.constants import API_LIMIT, BASE_URL
from sharepoint.dto.response import (
    APIPaginatedResponse,
    T,
    TenantResponse,
)
from sharepoint.enums import SharepointEndpoint


class SharepointClient(BaseIntegrationClient):
    @classmethod
    def prepare_client_args(cls, args: Request) -> dict[str, t.Any]:
        return {
            "auth": BearerAuth(token=get_oauth(args).access_token),
            "base_url": BASE_URL,
        }

    async def _get_all(
        self, callable: Callable[..., Awaitable[APIPaginatedResponse[T]]], **kwargs: t.Any
    ) -> list[T]:
        items: list[T] = []
        skip_token: str | None = None

        while True:
            response = await callable(**kwargs, skip_token=skip_token)
            items.extend(response.value)
            skip_token = response.skip_token

            if skip_token is None:
                break

        return items

    async def _get_paginated(
        self,
        *,
        dto: type[DTO],
        endpoint: str,
        page_size: int,
        skip_token: str | None = None,
        select: str | None = None,
    ) -> DTO:
        params = {"$top": str(page_size)}

        if skip_token:
            params["$skiptoken"] = skip_token

        if select:
            params["$select"] = select

        async with API_LIMIT:
            response = await self._http_client.get(endpoint, params=params)

        return create_client_response(response, dto)

    async def get_tenant(self, tenant_id: str) -> TenantResponse:
        """Scope: CrossTenantInformation.ReadBasic.All"""
        async with API_LIMIT:
            response = await self._http_client.get(
                SharepointEndpoint.TENANT.format(tenant_id=tenant_id)
            )

        return create_client_response(response, TenantResponse)
