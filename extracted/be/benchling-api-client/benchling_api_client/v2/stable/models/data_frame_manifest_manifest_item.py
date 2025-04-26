from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="DataFrameManifestManifestItem")


@attr.s(auto_attribs=True, repr=False)
class DataFrameManifestManifestItem:
    """ List of files composing a data frane, their names, and their corresponding URLs. """

    _file_name: Union[Unset, str] = UNSET
    _url: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("file_name={}".format(repr(self._file_name)))
        fields.append("url={}".format(repr(self._url)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "DataFrameManifestManifestItem({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        file_name = self._file_name
        url = self._url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if file_name is not UNSET:
            field_dict["fileName"] = file_name
        if url is not UNSET:
            field_dict["url"] = url

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

        def get_url() -> Union[Unset, None, str]:
            url = d.pop("url")
            return url

        try:
            url = get_url()
        except KeyError:
            if strict:
                raise
            url = cast(Union[Unset, None, str], UNSET)

        data_frame_manifest_manifest_item = cls(
            file_name=file_name,
            url=url,
        )

        data_frame_manifest_manifest_item.additional_properties = d
        return data_frame_manifest_manifest_item

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

    @property
    def url(self) -> Optional[str]:
        if isinstance(self._url, Unset):
            raise NotPresentError(self, "url")
        return self._url

    @url.setter
    def url(self, value: Optional[str]) -> None:
        self._url = value

    @url.deleter
    def url(self) -> None:
        self._url = UNSET
