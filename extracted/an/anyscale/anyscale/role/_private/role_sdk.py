from typing import List, Optional

from anyscale._private.sdk.base_sdk import BaseSDK
from anyscale.role.models import Role


class PrivateRoleSDK(BaseSDK):
    """Reading the roles an organization may assign.

    Roles are authored elsewhere. What is here is what a caller needs before
    binding one: its name and its id.
    """

    def list(
        self,
        *,
        name: Optional[str] = None,
        include_archived: bool = False,
        max_items: Optional[int] = None,
    ) -> List[Role]:
        """Roles the caller's organization may assign."""
        return [
            Role.from_api_model(role)
            for role in self.client.list_roles(
                name=name,
                include_archived=include_archived,
                max_items=max_items,
            )
        ]

    def get(self, *, role_id: str) -> Role:
        """One role, with the permissions it grants and denies."""
        roles = [
            role
            for role in self.client.list_roles(ids=[role_id], include_archived=True, max_items=1)
            if role.id == role_id
        ]
        if not roles:
            raise ValueError(f"No role with id '{role_id}'.")
        return Role.from_api_model(roles[0])
