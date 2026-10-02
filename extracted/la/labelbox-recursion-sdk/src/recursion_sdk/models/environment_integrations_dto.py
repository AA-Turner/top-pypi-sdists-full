from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.environment_integrations_dto_taiga import EnvironmentIntegrationsDtoTaiga





T = TypeVar("T", bound="EnvironmentIntegrationsDto")



@_attrs_define
class EnvironmentIntegrationsDto:
    """ All integration settings for one environment, keyed by integration name. Absent rows resolve to platform defaults.

        Attributes:
            taiga (EnvironmentIntegrationsDtoTaiga): Taiga integration settings for one environment.
     """

    taiga: EnvironmentIntegrationsDtoTaiga





    def to_dict(self) -> dict[str, Any]:
        from ..models.environment_integrations_dto_taiga import EnvironmentIntegrationsDtoTaiga # noqa: PLC0415
        taiga = self.taiga.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "taiga": taiga,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.environment_integrations_dto_taiga import EnvironmentIntegrationsDtoTaiga # noqa: PLC0415
        d = dict(src_dict)
        taiga = EnvironmentIntegrationsDtoTaiga.from_dict(d.pop("taiga"))




        environment_integrations_dto = cls(
            taiga=taiga,
        )

        return environment_integrations_dto

