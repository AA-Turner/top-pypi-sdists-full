from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="SetupForgejo")



@_attrs_define
class SetupForgejo:
    """ 
        Attributes:
            redirect_uri (str): What the owner enters as the Redirect URI of the app they create on their Forgejo.
            scopes (list[str]): The permissions the dashboard asks for, as Forgejo names them.
            instance_url (str): The linked instance, or empty.
            linked (bool):
            account (str):
            repository_count (int): Repositories the board sees on Forgejo as of its last refresh.
            reachable (bool): Whether the last refresh reached the instance. True while there has been none.
     """

    redirect_uri: str
    scopes: list[str]
    instance_url: str
    linked: bool
    account: str
    repository_count: int
    reachable: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        redirect_uri = self.redirect_uri

        scopes = self.scopes



        instance_url = self.instance_url

        linked = self.linked

        account = self.account

        repository_count = self.repository_count

        reachable = self.reachable


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "redirectUri": redirect_uri,
            "scopes": scopes,
            "instanceUrl": instance_url,
            "linked": linked,
            "account": account,
            "repositoryCount": repository_count,
            "reachable": reachable,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        redirect_uri = d.pop("redirectUri")

        scopes = cast(list[str], d.pop("scopes"))


        instance_url = d.pop("instanceUrl")

        linked = d.pop("linked")

        account = d.pop("account")

        repository_count = d.pop("repositoryCount")

        reachable = d.pop("reachable")

        setup_forgejo = cls(
            redirect_uri=redirect_uri,
            scopes=scopes,
            instance_url=instance_url,
            linked=linked,
            account=account,
            repository_count=repository_count,
            reachable=reachable,
        )


        setup_forgejo.additional_properties = d
        return setup_forgejo

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
