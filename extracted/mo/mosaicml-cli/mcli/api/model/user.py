"""User models"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from mcli.api.schema.generic_model import DeserializableModel


@dataclass
class Organization(DeserializableModel):
    """ Dataclass for Organization
    """

    id: str
    name: str
    is_databricks_internal: bool

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> Organization:
        """Converts a MAPI response to an Organization object"""
        return cls(id=response['id'], name=response['name'], is_databricks_internal=response['isDatabricksInternal'])


@dataclass
class User(DeserializableModel):
    """ Dataclass for User
    """

    id: str
    name: str
    email: str
    organizations: List[Organization] = field(default_factory=list)

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> User:
        """Converts a MAPI response to an User object"""
        organizations = [Organization.from_mapi_response(o) for o in response['organizations']]
        return cls(
            id=response['id'],
            name=response['name'],
            email=response['email'],
            organizations=organizations,
        )
