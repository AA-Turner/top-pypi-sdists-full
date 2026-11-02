from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_app_raw_source_json_body_value_data import UpdateAppRawSourceJsonBodyValueData
    from ..models.update_app_raw_source_json_body_value_files import UpdateAppRawSourceJsonBodyValueFiles
    from ..models.update_app_raw_source_json_body_value_runnables import UpdateAppRawSourceJsonBodyValueRunnables


T = TypeVar("T", bound="UpdateAppRawSourceJsonBodyValue")


@_attrs_define
class UpdateAppRawSourceJsonBodyValue:
    """The raw app's value. `files` maps each source path (e.g. `/index.tsx`, `/App.tsx`, `/package.json`) to its content
    and must contain an entry point (`/index.tsx`, `/index.ts` or `/index.js`); `runnables` and `data` are carried
    through unchanged.

        Attributes:
            files (UpdateAppRawSourceJsonBodyValueFiles):
            runnables (Union[Unset, UpdateAppRawSourceJsonBodyValueRunnables]):
            data (Union[Unset, UpdateAppRawSourceJsonBodyValueData]):
    """

    files: "UpdateAppRawSourceJsonBodyValueFiles"
    runnables: Union[Unset, "UpdateAppRawSourceJsonBodyValueRunnables"] = UNSET
    data: Union[Unset, "UpdateAppRawSourceJsonBodyValueData"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        files = self.files.to_dict()

        runnables: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.runnables, Unset):
            runnables = self.runnables.to_dict()

        data: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.data, Unset):
            data = self.data.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "files": files,
            }
        )
        if runnables is not UNSET:
            field_dict["runnables"] = runnables
        if data is not UNSET:
            field_dict["data"] = data

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_app_raw_source_json_body_value_data import UpdateAppRawSourceJsonBodyValueData
        from ..models.update_app_raw_source_json_body_value_files import UpdateAppRawSourceJsonBodyValueFiles
        from ..models.update_app_raw_source_json_body_value_runnables import UpdateAppRawSourceJsonBodyValueRunnables

        d = src_dict.copy()
        files = UpdateAppRawSourceJsonBodyValueFiles.from_dict(d.pop("files"))

        _runnables = d.pop("runnables", UNSET)
        runnables: Union[Unset, UpdateAppRawSourceJsonBodyValueRunnables]
        if isinstance(_runnables, Unset):
            runnables = UNSET
        else:
            runnables = UpdateAppRawSourceJsonBodyValueRunnables.from_dict(_runnables)

        _data = d.pop("data", UNSET)
        data: Union[Unset, UpdateAppRawSourceJsonBodyValueData]
        if isinstance(_data, Unset):
            data = UNSET
        else:
            data = UpdateAppRawSourceJsonBodyValueData.from_dict(_data)

        update_app_raw_source_json_body_value = cls(
            files=files,
            runnables=runnables,
            data=data,
        )

        update_app_raw_source_json_body_value.additional_properties = d
        return update_app_raw_source_json_body_value

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
