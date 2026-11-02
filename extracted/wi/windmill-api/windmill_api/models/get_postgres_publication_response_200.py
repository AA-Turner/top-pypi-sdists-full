from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_postgres_publication_response_200_table_to_track_item import (
        GetPostgresPublicationResponse200TableToTrackItem,
    )


T = TypeVar("T", bound="GetPostgresPublicationResponse200")


@_attrs_define
class GetPostgresPublicationResponse200:
    """
    Attributes:
        transaction_to_track (List[str]):
        table_to_track (Union[Unset, List['GetPostgresPublicationResponse200TableToTrackItem']]):
    """

    transaction_to_track: List[str]
    table_to_track: Union[Unset, List["GetPostgresPublicationResponse200TableToTrackItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        transaction_to_track = self.transaction_to_track

        table_to_track: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.table_to_track, Unset):
            table_to_track = []
            for table_to_track_item_data in self.table_to_track:
                table_to_track_item = table_to_track_item_data.to_dict()

                table_to_track.append(table_to_track_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "transaction_to_track": transaction_to_track,
            }
        )
        if table_to_track is not UNSET:
            field_dict["table_to_track"] = table_to_track

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_postgres_publication_response_200_table_to_track_item import (
            GetPostgresPublicationResponse200TableToTrackItem,
        )

        d = src_dict.copy()
        transaction_to_track = cast(List[str], d.pop("transaction_to_track"))

        table_to_track = []
        _table_to_track = d.pop("table_to_track", UNSET)
        for table_to_track_item_data in _table_to_track or []:
            table_to_track_item = GetPostgresPublicationResponse200TableToTrackItem.from_dict(table_to_track_item_data)

            table_to_track.append(table_to_track_item)

        get_postgres_publication_response_200 = cls(
            transaction_to_track=transaction_to_track,
            table_to_track=table_to_track,
        )

        get_postgres_publication_response_200.additional_properties = d
        return get_postgres_publication_response_200

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
