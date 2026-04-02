import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.version_history_revision_user_type_0 import VersionHistoryRevisionUserType0
    from ..models.version_history_serialized_data import VersionHistorySerializedData


T = TypeVar("T", bound="VersionHistory")


@_attrs_define
class VersionHistory:
    """
    Attributes:
        id (int): Version ID
        revision_date (datetime.datetime): When this revision was created
        revision_user (Union['VersionHistoryRevisionUserType0', None]): User who created this revision
        revision_comment (str): Comment describing the revision
        serialized_data (VersionHistorySerializedData): Serialized model fields at this revision
    """

    id: int
    revision_date: datetime.datetime
    revision_user: Union["VersionHistoryRevisionUserType0", None]
    revision_comment: str
    serialized_data: "VersionHistorySerializedData"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.version_history_revision_user_type_0 import VersionHistoryRevisionUserType0

        id = self.id

        revision_date = self.revision_date.isoformat()

        revision_user: Union[None, dict[str, Any]]
        if isinstance(self.revision_user, VersionHistoryRevisionUserType0):
            revision_user = self.revision_user.to_dict()
        else:
            revision_user = self.revision_user

        revision_comment = self.revision_comment

        serialized_data = self.serialized_data.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "revision_date": revision_date,
                "revision_user": revision_user,
                "revision_comment": revision_comment,
                "serialized_data": serialized_data,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.version_history_revision_user_type_0 import VersionHistoryRevisionUserType0
        from ..models.version_history_serialized_data import VersionHistorySerializedData

        d = dict(src_dict)
        id = d.pop("id")

        revision_date = isoparse(d.pop("revision_date"))

        def _parse_revision_user(data: object) -> Union["VersionHistoryRevisionUserType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                revision_user_type_0 = VersionHistoryRevisionUserType0.from_dict(data)

                return revision_user_type_0
            except:  # noqa: E722
                pass
            return cast(Union["VersionHistoryRevisionUserType0", None], data)

        revision_user = _parse_revision_user(d.pop("revision_user"))

        revision_comment = d.pop("revision_comment")

        serialized_data = VersionHistorySerializedData.from_dict(d.pop("serialized_data"))

        version_history = cls(
            id=id,
            revision_date=revision_date,
            revision_user=revision_user,
            revision_comment=revision_comment,
            serialized_data=serialized_data,
        )

        version_history.additional_properties = d
        return version_history

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
