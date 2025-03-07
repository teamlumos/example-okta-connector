"""Pagination for Okta API."""

import typing as t

from connector.utils.pagination import (
    NextPageTokenInterface,
    PaginationBase,
    create_next_page_token,
)

DEFAULT_PAGE_SIZE = 5
MAX_PAGE_SIZE = 500


class Pagination(PaginationBase):
    """Pagination parameters for API methods."""

    after: str | None

    @classmethod
    def default(cls, endpoint: str) -> "Pagination":
        return cls(
            endpoint=endpoint,
            after=None,
        )


if t.TYPE_CHECKING:

    class NextPageToken(NextPageTokenInterface[Pagination]):
        @classmethod
        def from_paginations(cls, paginations: list[Pagination]) -> "NextPageToken":
            return cls(token=None)

        def paginations(self) -> list[Pagination]:
            return []
else:
    NextPageToken = create_next_page_token(Pagination, "NextPageToken")
