from __future__ import annotations

from typing import TypedDict

from bitfab.http import HttpClient

MEMBERS_PATH = "/api/sdk/organizationMembers"


class OrganizationMember(TypedDict):
    id: str
    fullName: str | None
    email: str | None
    imageUrl: str | None


class OrganizationMembersClient:
    """The people in the API key's organization."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = http_client

    def list(self) -> list[OrganizationMember]:
        """List the organization's members, ordered by name.

        Read it to find the address to pass as an assertion's ``assigneeEmail``.
        """
        return self._http_client.get(MEMBERS_PATH)["members"]
