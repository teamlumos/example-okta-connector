import logging
import typing as t

from connector.oai.base_clients import BaseIntegrationClient
from connector.oai.capability import Request, get_token_auth, get_settings
from connector.utils.httpx_auth import BearerAuth
from connector.utils.client_utils import create_client_response
import httpx
from okta.enums import OktaEndpoint
from okta.models import User, UsersResponse, UserRolesResponse
from okta.settings import OktaSettings
from urllib.parse import ParseResult, urlparse, parse_qs

logger = logging.getLogger(__name__)

class OktaClient(BaseIntegrationClient):
    @classmethod
    def prepare_client_args(cls, args: Request) -> dict[str, t.Any]:
        account_id = get_settings(args, OktaSettings).account_id
        return {
            "auth": BearerAuth(token_prefix="SSWS", token=get_token_auth(args).token),
            "base_url": f"https://{account_id}",
        }

    #example of a method that fetches users
    async def get_users(self, limit: int | None = None, after: str | None = None) -> UsersResponse:
        logger.info(f"Getting users")
        params = {}
        if after:
            logger.info(f"Getting users after: {after}")
            params["after"] = after
        if limit:
            params["limit"] = str(limit)
        logger.info(f"Getting users with params: {params}")
        response = await self._http_client.get(OktaEndpoint.USERS, params=params)
        client_response = create_client_response(response, UsersResponse)
        client_response.after = parse_next_link(response)
        return client_response
    
    async def get_user(self, user_id: str) -> User:
        logger.info(f"Getting user: {user_id}")
        response = await self._http_client.get(OktaEndpoint.USER.format(user_id=user_id))
        return create_client_response(response, User)
    
    async def suspend_user(self, user_id: str) -> None:
        logger.info(f"Suspending user: {user_id}")
        response = await self._http_client.post(OktaEndpoint.SUSPEND_USER.format(user_id=user_id))
        response.raise_for_status()
        logger.info(f"User suspended: {user_id}")

    async def unsuspend_user(self, user_id: str) -> None:
        logger.info(f"Unsuspending user: {user_id}")
        response = await self._http_client.post(OktaEndpoint.UNSUSPEND_USER.format(user_id=user_id))
        response.raise_for_status()
        logger.info(f"User unsuspended: {user_id}")
    
    async def activate_user(self, user_id: str) -> None:
        logger.info(f"Activating user: {user_id}")
        response = await self._http_client.post(OktaEndpoint.ACTIVATE_USER.format(user_id=user_id))
        response.raise_for_status()
        logger.info(f"User activated: {user_id}")

    async def get_user_roles(self, user_id: str) -> UserRolesResponse:
        logger.info(f"Getting user roles: {user_id}")
        response = await self._http_client.get(OktaEndpoint.USER_ROLES.format(user_id=user_id))
        logger.info(f"User roles: {response.json()}")
        return create_client_response(response, UserRolesResponse)

def parse_next_link(response: httpx.Response) -> str | None:
    # returns the id that should be used for the next page of results
    links = response.links
    if next_link := links.get("next", {}).get("url"):
        logger.debug(f"Next link: {next_link}")
        parsed_url: ParseResult = urlparse(next_link)
        query_params = parse_qs(parsed_url.query)
        after_value = query_params.get("after", [None])[0]
        logger.debug(f"After value: {after_value}")
        return after_value
    return None