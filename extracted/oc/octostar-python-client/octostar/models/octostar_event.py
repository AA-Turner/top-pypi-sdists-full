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
from typing import Dict

if TYPE_CHECKING:
    from ..models.octostar_event_octostar_payload import OctostarEventOctostarPayload


T = TypeVar("T", bound="OctostarEvent")


@attr.s(auto_attribs=True)
class OctostarEvent:
    """
    ### Attributes:
    * `octostar_stream (str)`: The channel where the Octostar event is posted
    * `octostar_payload (OctostarEventOctostarPayload)`:
    """

    octostar_stream: str
    octostar_payload: "OctostarEventOctostarPayload"
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.octostar_event_octostar_payload import (
            OctostarEventOctostarPayload,
        )

        octostar_stream = self.octostar_stream
        octostar_payload = self.octostar_payload.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "octostar_stream": octostar_stream,
                "octostar_payload": octostar_payload,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.octostar_event_octostar_payload import (
            OctostarEventOctostarPayload,
        )

        d = src_dict.copy()
        octostar_stream = d.pop("octostar_stream")

        octostar_payload = OctostarEventOctostarPayload.from_dict(
            d.pop("octostar_payload")
        )

        octostar_event = cls(
            octostar_stream=octostar_stream,
            octostar_payload=octostar_payload,
        )

        octostar_event.additional_properties = d
        return octostar_event

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
