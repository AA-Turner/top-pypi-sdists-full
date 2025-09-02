import logging
from typing import Any, Union, Optional

from pydantic import Field, BaseModel

from ipfabric.tools.shared import date_parser, raise_for_status

logger = logging.getLogger("ipfabric")


class Token(BaseModel):
    description: str
    usage: int
    username: str
    expires: Optional[int] = None
    token: Optional[str] = None
    user_id: str = Field(alias="userId")
    user_role_ids: Optional[list[str]] = Field(None, alias="userRoleIds")
    token_id: str = Field(alias="id")
    is_expired: bool = Field(alias="isExpired")
    last_used: Optional[Union[str, int]] = Field(None, alias="lastUsed")
    role_ids: list[str] = Field(alias="roleIds", default_factory=list)
    role_names: Optional[list[str]] = Field(None, alias="roleNames")


class APIToken(BaseModel):
    client: Any = Field(exclude=True)
    _tokens: Optional[list[Token]] = None

    def model_post_init(self, __context: Any) -> None:
        self._tokens = self.get_tokens()

    @property
    def tokens(self):
        return self._tokens

    @property
    def tokens_by_id(self):
        return {t.token_id: t for t in self.tokens}

    @property
    def tokens_by_description(self):
        return {t.description: t for t in self.tokens}

    def get_tokens(self) -> list[Token]:
        res = raise_for_status(self.client.get("api-tokens"))
        return [Token(**t) for t in res.json()]

    def _check_roles(self, role_ids: list, role_names: list):
        if not role_names and not role_ids:
            raise SyntaxError("No Role Ids or Names provided.")
        checked_roles = list()
        for role in role_ids:
            if str(role) in self.client.settings.roles.roles_by_id:
                checked_roles.append(str(role))
            else:
                raise ValueError(f"Role ID '{role}' does not exist.")
        for role in role_names:
            if str(role) in self.client.settings.roles.roles_by_name:
                checked_roles.append(str(role))
            else:
                raise ValueError(f"Role Name '{role}' does not exist.")
        return checked_roles

    def add_token(
        self,
        descr: str,
        role_ids: Optional[list] = None,
        role_names: Optional[list] = None,
        expires: Optional[Union[str, int]] = None,
    ):
        payload = dict(
            description=descr,
            expires=int(date_parser(expires).timestamp() * 1000) if expires else None,
            roleIds=self._check_roles(role_ids or list(), role_names or list()),
        )
        res = raise_for_status(self.client.post("api-tokens", json=payload))
        return Token(**res.json())

    def delete_token(self, token_id: [int, str, Token]):
        token_id = token_id.token_id if isinstance(token_id, Token) else str(token_id)
        if token_id not in self.tokens_by_id:
            raise ValueError(f"Could not find token matching ID '{token_id}'.")
        raise_for_status(self.client.delete("api-tokens/" + token_id))
        self._tokens = self.get_tokens()
        return self.tokens

    def delete_token_by_description(self, token_description: str):
        if token_description not in self.tokens_by_description:
            raise ValueError(f"Could not find token matching description '{token_description}'.")
        return self.delete_token(self.tokens_by_description[token_description].token_id)
