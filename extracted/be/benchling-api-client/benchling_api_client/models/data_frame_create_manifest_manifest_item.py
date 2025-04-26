from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="DataFrameCreateManifestManifestItem")


@attr.s(auto_attribs=True, repr=False)
class DataFrameCreateManifestManifestItem:
    """ List of files that will be uploaded to a data frame and their names. """

    _file_name: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("file_name={}".format(repr(self._file_name)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "DataFrameCreateManifestManifestItem({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        file_name = self._file_name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if file_name is not UNSET:
            field_dict["fileName"] = file_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_file_name() -> Union[Unset, str]:
            file_name = d.pop("fileName")
            return file_name

        try:
            file_name = get_file_name()
        except KeyError:
            if strict:
                raise
            file_name = cast(Union[Unset, str], UNSET)

        data_frame_create_manifest_manifest_item = cls(
            file_name=file_name,
        )

        data_frame_create_manifest_manifest_item.additional_properties = d
        return data_frame_create_manifest_manifest_item

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
    def file_name(self) -> str:
        if isinstance(self._file_name, Unset):
            raise NotPresentError(self, "file_name")
        return self._file_name

    @file_name.setter
    def file_name(self, value: str) -> None:
        self._file_name = value

    @file_name.deleter
    def file_name(self) -> None:
        self._file_name = UNSET
