from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.training_contract_response_dto_additional_property import TrainingContractResponseDtoAdditionalProperty





T = TypeVar("T", bound="TrainingContractResponseDto")



@_attrs_define
class TrainingContractResponseDto:
    """ The platform's generated training-contract JSON Schemas, keyed by filename (e.g. "blocks-telemetry.schema.json"),
    plus a non-schema "training-contract-guide.json" entry carrying the narrative version/drift/panel-mapping story as {
    content: string }. Served verbatim from the committed generated artifacts -- never re-derived at request time.

        Example:
            {'status-envelope.schema.json': {'$schema': 'https://json-schema.org/draft/2020-12/schema', 'type': 'object'},
                'training-contract-guide.json': {'content': '# Training-contract version story...'}}

     """

    additional_properties: dict[str, TrainingContractResponseDtoAdditionalProperty] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.training_contract_response_dto_additional_property import TrainingContractResponseDtoAdditionalProperty # noqa: PLC0415
        
        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()


        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.training_contract_response_dto_additional_property import TrainingContractResponseDtoAdditionalProperty # noqa: PLC0415
        d = dict(src_dict)
        training_contract_response_dto = cls(
        )


        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = TrainingContractResponseDtoAdditionalProperty.from_dict(prop_dict)



            additional_properties[prop_name] = additional_property

        training_contract_response_dto.additional_properties = additional_properties
        return training_contract_response_dto

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> TrainingContractResponseDtoAdditionalProperty:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: TrainingContractResponseDtoAdditionalProperty) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
