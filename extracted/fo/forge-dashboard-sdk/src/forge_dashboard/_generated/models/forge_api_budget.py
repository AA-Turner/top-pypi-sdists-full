from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.forge import Forge
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.rate_limit import RateLimit





T = TypeVar("T", bound="ForgeApiBudget")



@_attrs_define
class ForgeApiBudget:
    """ 
        Attributes:
            forge (Forge):
            rate_limit_graph_ql (RateLimit | Unset): One of a forge API's own request budgets for the credential the last
                refresh used — see ForgeHealth.rateLimitGraphQL/rateLimitREST for which budget this is and when each is (or
                isn't) reported.
            rate_limit_rest (RateLimit | Unset): One of a forge API's own request budgets for the credential the last
                refresh used — see ForgeHealth.rateLimitGraphQL/rateLimitREST for which budget this is and when each is (or
                isn't) reported.
     """

    forge: Forge
    rate_limit_graph_ql: RateLimit | Unset = UNSET
    rate_limit_rest: RateLimit | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.rate_limit import RateLimit # noqa: PLC0415
        forge = self.forge.value

        rate_limit_graph_ql: dict[str, Any] | Unset = UNSET
        if not isinstance(self.rate_limit_graph_ql, Unset):
            rate_limit_graph_ql = self.rate_limit_graph_ql.to_dict()

        rate_limit_rest: dict[str, Any] | Unset = UNSET
        if not isinstance(self.rate_limit_rest, Unset):
            rate_limit_rest = self.rate_limit_rest.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "forge": forge,
        })
        if rate_limit_graph_ql is not UNSET:
            field_dict["rateLimitGraphQL"] = rate_limit_graph_ql
        if rate_limit_rest is not UNSET:
            field_dict["rateLimitREST"] = rate_limit_rest

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rate_limit import RateLimit # noqa: PLC0415
        d = dict(src_dict)
        forge = Forge(d.pop("forge"))




        _rate_limit_graph_ql = d.pop("rateLimitGraphQL", UNSET)
        rate_limit_graph_ql: RateLimit | Unset
        if isinstance(_rate_limit_graph_ql,  Unset):
            rate_limit_graph_ql = UNSET
        else:
            rate_limit_graph_ql = RateLimit.from_dict(_rate_limit_graph_ql)




        _rate_limit_rest = d.pop("rateLimitREST", UNSET)
        rate_limit_rest: RateLimit | Unset
        if isinstance(_rate_limit_rest,  Unset):
            rate_limit_rest = UNSET
        else:
            rate_limit_rest = RateLimit.from_dict(_rate_limit_rest)




        forge_api_budget = cls(
            forge=forge,
            rate_limit_graph_ql=rate_limit_graph_ql,
            rate_limit_rest=rate_limit_rest,
        )


        forge_api_budget.additional_properties = d
        return forge_api_budget

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
