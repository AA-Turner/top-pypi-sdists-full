from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from anyscale._private.models import ModelBase


@dataclass(frozen=True)
class Role(ModelBase):
    """A role: a named set of permissions, assignable to a principal."""

    __doc_py_example__ = """\
import anyscale

for role in anyscale.role.list():
    print(role.id, role.name)
"""

    id: str = field(metadata={"docstring": "The unique identifier of the role."})
    name: str = field(metadata={"docstring": "The name of the role."})
    built_in: bool = field(
        metadata={
            "docstring": "Whether the role is one of Anyscale's, which are global to the platform."
        }
    )
    description: Optional[str] = field(
        default=None, metadata={"docstring": "What the role is for."}
    )
    allowed_permissions: Optional[List[str]] = field(
        default=None,
        metadata={
            "docstring": "The permissions the role grants. None in a listing, which does not read them."
        },
    )
    denied_permissions: Optional[List[str]] = field(
        default=None,
        metadata={
            "docstring": "The permissions the role explicitly denies. None in a listing, which does not read them."
        },
    )
    created_at: Optional[datetime] = field(
        default=None, metadata={"docstring": "When the role was created."}
    )
    archived_at: Optional[datetime] = field(
        default=None,
        metadata={
            "docstring": "When the role was archived. An archived role cannot be newly assigned, though principals already bound to it keep their access."
        },
    )

    def _validate_id(self, id: str):  # noqa: A002
        if not isinstance(id, str):
            raise TypeError("'id' must be a string.")

    def _validate_name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("'name' must be a string.")

    def _validate_built_in(self, built_in: bool):
        if not isinstance(built_in, bool):
            raise TypeError("'built_in' must be a bool.")

    def _validate_description(self, description: Optional[str]):
        if description is not None and not isinstance(description, str):
            raise TypeError("'description' must be a string.")

    def _validate_allowed_permissions(self, allowed_permissions: Optional[List[str]]):
        if allowed_permissions is not None and not isinstance(allowed_permissions, list):
            raise TypeError("'allowed_permissions' must be a list.")

    def _validate_denied_permissions(self, denied_permissions: Optional[List[str]]):
        if denied_permissions is not None and not isinstance(denied_permissions, list):
            raise TypeError("'denied_permissions' must be a list.")

    def _validate_created_at(self, created_at: Optional[datetime]):
        if created_at is not None and not isinstance(created_at, datetime):
            raise TypeError("'created_at' must be a datetime.")

    def _validate_archived_at(self, archived_at: Optional[datetime]):
        if archived_at is not None and not isinstance(archived_at, datetime):
            raise TypeError("'archived_at' must be a datetime.")

    @classmethod
    def from_api_model(cls, api_model) -> "Role":
        """A role as the API returned it."""
        return cls(
            id=api_model.id,
            name=api_model.name,
            built_in=bool(api_model.built_in),
            description=getattr(api_model, "description", None),
            allowed_permissions=_permission_names(getattr(api_model, "allowed_permissions", None)),
            denied_permissions=_permission_names(getattr(api_model, "denied_permissions", None)),
            created_at=getattr(api_model, "created_at", None),
            archived_at=getattr(api_model, "archived_at", None),
        )


def _permission_names(permissions) -> Optional[List[str]]:
    """
    Permission names as plain strings. The generated client models them as an
    enum, which yaml and json output would otherwise render as its repr.
    """
    if permissions is None:
        return None
    return [str(getattr(permission, "value", permission)) for permission in permissions]
