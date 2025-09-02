import logging
from typing import Any, Optional, Union, Annotated

from pydantic import Field, BaseModel, StringConstraints, field_validator

logger = logging.getLogger("ipfabric")

METHOD = Annotated[str, StringConstraints(to_lower=True)]


class Scope(BaseModel):
    method: METHOD
    path: str
    api_scope_id: str = Field(alias="id")

    @field_validator("path")
    @classmethod
    def _path(cls, p):
        return p[1:]


class Token(BaseModel):
    token_id: str = Field(None, alias="id")
    description: Optional[str] = None
    role_ids: list = Field(None, alias="roleIds")


class User(BaseModel):
    username: str
    user_id: str = Field(None, alias="id")
    local: Optional[bool] = Field(None, alias="isLocal")
    sso_provider: Optional[Any] = Field(None, alias="ssoProvider")
    domains: Optional[Any] = Field(None, alias="domainSuffixes")
    role_names: Optional[list] = Field(alias="roleNames", default_factory=list)
    role_ids: list = Field(default_factory=list, alias="roleIds")
    ldap_id: Optional[Any] = Field(None, alias="ldapId")
    timezone: Optional[str] = None
    token: Optional[Token] = None
    _scopes: Optional[list[Scope]] = None
    _snapshots_settings: Optional[bool] = None

    def model_post_init(self, __context: Any) -> None:
        if self._snapshots_settings is None and self.is_admin:
            self._snapshots_settings = True

    def __repr__(self):
        return self.username

    @property
    def is_admin(self):
        return (
            True
            if (self.token and "admin" in self.token.role_ids) or (not self.token and "admin" in self.role_ids)
            else False
        )

    @property
    def snapshots_settings(self):
        """If the User/Token has access to snapshots/:key/settings Endpoint."""
        return self._snapshots_settings

    @snapshots_settings.setter
    def snapshots_settings(self, v: bool):
        self._snapshots_settings = v

    @property
    def error_msg(self):
        msg = f'User "{self.username}" '
        if self.token:
            msg += f'Token "{self.token.description}" '
        return msg

    @property
    def scopes(self) -> list[Scope]:
        return self._scopes

    @scopes.setter
    def scopes(self, scopes: list[Union[Scope, dict[str, str]]]):
        self._scopes = [Scope(**dict(_)) for _ in scopes]
