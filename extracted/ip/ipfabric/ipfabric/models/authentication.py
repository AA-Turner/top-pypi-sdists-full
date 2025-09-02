from datetime import datetime
from typing import Optional, Any, Union
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator, model_validator, model_serializer, RootModel

from ipfabric.tools.shared import VALID_IP, VALID_IPv6, validate_ip_network_str


class Expiration(BaseModel):
    enabled: bool = False
    value: Optional[datetime] = None

    @model_validator(mode="after")
    def _verify(self):
        if self.enabled and not self.value:
            raise ValueError("Enabled Expiration requires a value.")
        elif not self.enabled and self.value:
            raise ValueError("Expiration value requires enabled to be True.")
        return self

    @model_serializer
    def _ser_model(self) -> dict[str, Any]:
        return (
            {"enabled": self.enabled, "value": self.value.strftime("%Y-%m-%d %H:%M:%S")}
            if self.enabled
            else {"enabled": self.enabled}
        )


class BaseCred(BaseModel):
    custom: bool = False
    username: str
    network: list[Union[str, VALID_IP, VALID_IPv6]]
    excluded: Optional[list[Union[str, VALID_IP, VALID_IPv6]]] = Field(default_factory=list, alias="excludeNetworks")
    expiration: Expiration = Field(None, alias="expirationDate")
    encrypt_password: str = Field(None, alias="password")
    priority: Optional[int] = None
    notes: Optional[str] = None

    @field_validator("network", "excluded")
    @classmethod
    def _verify_valid_networks(cls, v: list[str]) -> list[str]:
        return [validate_ip_network_str(_, ipv6=True) for _ in v]

    @model_serializer
    def _ser_model(self) -> dict[str, Any]:
        custom = {"custom": self.custom} if self.custom else dict()
        return dict(
            priority=self.priority,
            username=self.username,
            excludeNetworks=self.excluded,
            expirationDate=self.expiration.model_dump(),
            password=self.encrypt_password,
            notes=self.notes or "",
            **custom,
        )


class Credential(BaseCred, BaseModel):
    credential_id: Optional[str] = Field(None, alias="id")
    config_mgmt: bool = Field(False, alias="syslog")

    @model_validator(mode="after")
    def _verify(self):
        if not self.credential_id:
            self.custom = True
        return self

    @model_serializer
    def _ser_cred_model(self) -> dict[str, Any]:
        cred = self._ser_model()
        return dict(
            syslog=self.config_mgmt,
            id=self.credential_id if self.credential_id else str(uuid4()),
            network=self.network,
            **cred,
        )


class Privilege(BaseCred, BaseModel):
    privilege_id: str = Field(None, alias="id")
    network: list[Union[str, VALID_IP]] = Field(None, alias="includeNetworks")

    @model_validator(mode="after")
    def _verify(self):
        if not self.privilege_id:
            self.custom = True
        return self

    @model_serializer
    def _ser_cred_model(self) -> dict[str, Any]:
        cred = self._ser_model()
        return dict(id=self.privilege_id if self.privilege_id else str(uuid4()), includeNetworks=self.network, **cred)


def serialize_list(auth):
    if not auth:
        return list()
    priorities = sorted([_.priority for _ in auth])
    if priorities != list(range(1, len(priorities) + 1)):
        raise ValueError("Priorities are not sequential.")
    return [_.model_dump() for _ in auth]


class CredentialList(RootModel):
    root: list[Credential]

    @model_serializer
    def _verify_priorities(self) -> dict[str, Any]:
        return serialize_list(self.credentials)

    def __bool__(self):
        return bool(self.credentials)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.root, name)


class PrivilegeList(RootModel):
    root: list[Privilege]

    @model_serializer
    def _verify_priorities(self) -> dict[str, Any]:
        return serialize_list(self.privileges)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.root, name)
