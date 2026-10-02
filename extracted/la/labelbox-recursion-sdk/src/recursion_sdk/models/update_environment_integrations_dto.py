from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.update_environment_integrations_dto_taiga import UpdateEnvironmentIntegrationsDtoTaiga





T = TypeVar("T", bound="UpdateEnvironmentIntegrationsDto")



@_attrs_define
class UpdateEnvironmentIntegrationsDto:
    """ Patch body for /environments/:environmentId/integrations. Each integration is independently optional and patch-
    shaped.

        Attributes:
            taiga (UpdateEnvironmentIntegrationsDtoTaiga | Unset): Patch-style update for the Taiga integration. Omitting a
                field leaves the existing value untouched.
     """

    taiga: UpdateEnvironmentIntegrationsDtoTaiga | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.update_environment_integrations_dto_taiga import UpdateEnvironmentIntegrationsDtoTaiga # noqa: PLC0415
        taiga: dict[str, Any] | Unset = UNSET
        if not isinstance(self.taiga, Unset):
            taiga = self.taiga.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if taiga is not UNSET:
            field_dict["taiga"] = taiga

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.update_environment_integrations_dto_taiga import UpdateEnvironmentIntegrationsDtoTaiga # noqa: PLC0415
        d = dict(src_dict)
        _taiga = d.pop("taiga", UNSET)
        taiga: UpdateEnvironmentIntegrationsDtoTaiga | Unset
        if isinstance(_taiga,  Unset):
            taiga = UNSET
        else:
            taiga = UpdateEnvironmentIntegrationsDtoTaiga.from_dict(_taiga)




        update_environment_integrations_dto = cls(
            taiga=taiga,
        )


        update_environment_integrations_dto.additional_properties = d
        return update_environment_integrations_dto

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
