from typing import (
    Any,
    Dict,
    Type,
    TypeVar,
    Tuple,
    Optional,
    BinaryIO,
    TextIO,
    TYPE_CHECKING,
)

from typing import List


import attr

from ..types import UNSET, Unset

from typing import Union
from ..types import UNSET, Unset
from ..models.octostar_event_octostar_payload_level import (
    OctostarEventOctostarPayloadLevel,
)


T = TypeVar("T", bound="OctostarEventOctostarPayload")


@attr.s(auto_attribs=True)
class OctostarEventOctostarPayload:
    """
    ### Attributes:
    * `message (Union[Unset, str])`: The message of the event
    * `description (Union[Unset, str])`: The description of the event
    * `level (Union[Unset, OctostarEventOctostarPayloadLevel])`: The level of the event
    """

    message: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    level: Union[Unset, OctostarEventOctostarPayloadLevel] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        message = self.message
        description = self.description
        level: Union[Unset, str] = UNSET
        if not isinstance(self.level, Unset):
            level = self.level.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if message is not UNSET:
            field_dict["message"] = message
        if description is not UNSET:
            field_dict["description"] = description
        if level is not UNSET:
            field_dict["level"] = level

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        message = d.pop("message", UNSET)

        description = d.pop("description", UNSET)

        _level = d.pop("level", UNSET)
        level: Union[Unset, OctostarEventOctostarPayloadLevel]
        if isinstance(_level, Unset):
            level = UNSET
        else:
            level = OctostarEventOctostarPayloadLevel(_level)

        octostar_event_octostar_payload = cls(
            message=message,
            description=description,
            level=level,
        )

        octostar_event_octostar_payload.additional_properties = d
        return octostar_event_octostar_payload

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
