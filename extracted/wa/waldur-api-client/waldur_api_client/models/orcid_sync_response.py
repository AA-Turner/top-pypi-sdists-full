import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.orcid_sync_response_imported import OrcidSyncResponseImported


T = TypeVar("T", bound="OrcidSyncResponse")


@_attrs_define
class OrcidSyncResponse:
    """
    Attributes:
        imported (OrcidSyncResponseImported):
        last_sync (datetime.datetime):
    """

    imported: "OrcidSyncResponseImported"
    last_sync: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        imported = self.imported.to_dict()

        last_sync = self.last_sync.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "imported": imported,
                "last_sync": last_sync,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.orcid_sync_response_imported import OrcidSyncResponseImported

        d = dict(src_dict)
        imported = OrcidSyncResponseImported.from_dict(d.pop("imported"))

        last_sync = isoparse(d.pop("last_sync"))

        orcid_sync_response = cls(
            imported=imported,
            last_sync=last_sync,
        )

        orcid_sync_response.additional_properties = d
        return orcid_sync_response

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
