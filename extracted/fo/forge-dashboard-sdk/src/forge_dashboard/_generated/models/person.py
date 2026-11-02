from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="Person")



@_attrs_define
class Person:
    """ Who wrote a description or a comment.

        Attributes:
            login (str):
            avatar_url (str): The forge's own avatar URL, passed through unchanged and never proxied.
            url (str): The person's profile page on the forge, built by the server from the web address of an item the board
                already holds for that forge. Empty when the board holds none yet, so a client shows the name alone.
     """

    login: str
    avatar_url: str
    url: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        login = self.login

        avatar_url = self.avatar_url

        url = self.url


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "login": login,
            "avatarUrl": avatar_url,
            "url": url,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        login = d.pop("login")

        avatar_url = d.pop("avatarUrl")

        url = d.pop("url")

        person = cls(
            login=login,
            avatar_url=avatar_url,
            url=url,
        )


        person.additional_properties = d
        return person

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
