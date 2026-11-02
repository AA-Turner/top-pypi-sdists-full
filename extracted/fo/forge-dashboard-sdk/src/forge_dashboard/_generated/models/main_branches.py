from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.forge_health import ForgeHealth
  from ..models.main_branch import MainBranch





T = TypeVar("T", bound="MainBranches")



@_attrs_define
class MainBranches:
    """ Every default branch the page lists, in no particular order. There is
    no tally: a client counts the rows it holds, so the filter pills and
    the navigation badge always agree with the list.

        Attributes:
            generated_at (datetime.datetime): When the snapshot was refreshed, not when it was requested.
            forges (list[ForgeHealth]): Each forge's health as of the last refresh, the same as the dashboard's. A client
                uses it to hold back an action that a forge which can't be reached, or whose rate limit is spent, would probably
                refuse. The budget can run out between refreshes, so the forge still has the final say.
            branches (list[MainBranch]):
     """

    generated_at: datetime.datetime
    forges: list[ForgeHealth]
    branches: list[MainBranch]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.forge_health import ForgeHealth # noqa: PLC0415
        from ..models.main_branch import MainBranch # noqa: PLC0415
        generated_at = self.generated_at.isoformat()

        forges = []
        for forges_item_data in self.forges:
            forges_item = forges_item_data.to_dict()
            forges.append(forges_item)



        branches = []
        for branches_item_data in self.branches:
            branches_item = branches_item_data.to_dict()
            branches.append(branches_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "generatedAt": generated_at,
            "forges": forges,
            "branches": branches,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.forge_health import ForgeHealth # noqa: PLC0415
        from ..models.main_branch import MainBranch # noqa: PLC0415
        d = dict(src_dict)
        generated_at = datetime.datetime.fromisoformat(d.pop("generatedAt"))




        forges = []
        _forges = d.pop("forges")
        for forges_item_data in (_forges):
            forges_item = ForgeHealth.from_dict(forges_item_data)



            forges.append(forges_item)


        branches = []
        _branches = d.pop("branches")
        for branches_item_data in (_branches):
            branches_item = MainBranch.from_dict(branches_item_data)



            branches.append(branches_item)


        main_branches = cls(
            generated_at=generated_at,
            forges=forges,
            branches=branches,
        )


        main_branches.additional_properties = d
        return main_branches

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
