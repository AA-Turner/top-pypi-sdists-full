from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import Literal, cast






T = TypeVar("T", bound="Ready")



@_attrs_define
class Ready:
    """ 
        Attributes:
            status (Literal['ok']):
            goroutines (int): Goroutines the process holds right now.
            threads (int | Unset): OS threads the process holds right now, read from
                `/proc/self/status`. Left out where that can't be read.
     """

    status: Literal['ok']
    goroutines: int
    threads: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        status = self.status

        goroutines = self.goroutines

        threads = self.threads


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "status": status,
            "goroutines": goroutines,
        })
        if threads is not UNSET:
            field_dict["threads"] = threads

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        status = cast(Literal['ok'] , d.pop("status"))
        if status != 'ok':
            raise ValueError(f"status must match const 'ok', got '{status}'")

        goroutines = d.pop("goroutines")

        threads = d.pop("threads", UNSET)

        ready = cls(
            status=status,
            goroutines=goroutines,
            threads=threads,
        )


        ready.additional_properties = d
        return ready

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
