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

from typing import cast
from typing import Optional
from typing import Dict

if TYPE_CHECKING:
    from ..models.processing_status import ProcessingStatus


T = TypeVar("T", bound="GetProcessingStatusResponse200Data")


@attr.s(auto_attribs=True)
class GetProcessingStatusResponse200Data:
    """A mapping of `entity_id` to `ProcessingStatusWithTimestamp`."""

    additional_properties: Dict[str, Optional["ProcessingStatus"]] = attr.ib(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        from ..models.processing_status import ProcessingStatus

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict() if prop else None

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.processing_status import ProcessingStatus

        d = src_dict.copy()
        get_processing_status_response_200_data = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            _additional_property = prop_dict
            additional_property: Optional[ProcessingStatus]
            if _additional_property is None:
                additional_property = None
            else:
                additional_property = ProcessingStatus.from_dict(_additional_property)

            additional_properties[prop_name] = additional_property

        get_processing_status_response_200_data.additional_properties = (
            additional_properties
        )
        return get_processing_status_response_200_data

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Optional["ProcessingStatus"]:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Optional["ProcessingStatus"]) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
