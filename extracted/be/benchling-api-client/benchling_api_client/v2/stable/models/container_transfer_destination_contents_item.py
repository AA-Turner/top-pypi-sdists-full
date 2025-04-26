from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.measurement import Measurement
from ..types import UNSET, Unset

T = TypeVar("T", bound="ContainerTransferDestinationContentsItem")


@attr.s(auto_attribs=True, repr=False)
class ContainerTransferDestinationContentsItem:
    """  """

    _entity_id: str
    _concentration: Union[Unset, Measurement] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("entity_id={}".format(repr(self._entity_id)))
        fields.append("concentration={}".format(repr(self._concentration)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "ContainerTransferDestinationContentsItem({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        entity_id = self._entity_id
        concentration: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._concentration, Unset):
            concentration = self._concentration.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if entity_id is not UNSET:
            field_dict["entityId"] = entity_id
        if concentration is not UNSET:
            field_dict["concentration"] = concentration

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_entity_id() -> str:
            entity_id = d.pop("entityId")
            return entity_id

        try:
            entity_id = get_entity_id()
        except KeyError:
            if strict:
                raise
            entity_id = cast(str, UNSET)

        def get_concentration() -> Union[Unset, Measurement]:
            concentration: Union[Unset, Union[Unset, Measurement]] = UNSET
            _concentration = d.pop("concentration")

            if not isinstance(_concentration, Unset):
                concentration = Measurement.from_dict(_concentration)

            return concentration

        try:
            concentration = get_concentration()
        except KeyError:
            if strict:
                raise
            concentration = cast(Union[Unset, Measurement], UNSET)

        container_transfer_destination_contents_item = cls(
            entity_id=entity_id,
            concentration=concentration,
        )

        container_transfer_destination_contents_item.additional_properties = d
        return container_transfer_destination_contents_item

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def entity_id(self) -> str:
        if isinstance(self._entity_id, Unset):
            raise NotPresentError(self, "entity_id")
        return self._entity_id

    @entity_id.setter
    def entity_id(self, value: str) -> None:
        self._entity_id = value

    @property
    def concentration(self) -> Measurement:
        if isinstance(self._concentration, Unset):
            raise NotPresentError(self, "concentration")
        return self._concentration

    @concentration.setter
    def concentration(self, value: Measurement) -> None:
        self._concentration = value

    @concentration.deleter
    def concentration(self) -> None:
        self._concentration = UNSET
