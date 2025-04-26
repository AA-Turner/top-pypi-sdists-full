from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConvertToCSVResponse_200Item")


@attr.s(auto_attribs=True, repr=False)
class ConvertToCSVResponse_200Item:
    """  """

    _blob_id: Union[Unset, str] = UNSET
    _transform_data_type: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("blob_id={}".format(repr(self._blob_id)))
        fields.append("transform_data_type={}".format(repr(self._transform_data_type)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "ConvertToCSVResponse_200Item({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        blob_id = self._blob_id
        transform_data_type = self._transform_data_type

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if blob_id is not UNSET:
            field_dict["blobId"] = blob_id
        if transform_data_type is not UNSET:
            field_dict["transformDataType"] = transform_data_type

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_blob_id() -> Union[Unset, str]:
            blob_id = d.pop("blobId")
            return blob_id

        try:
            blob_id = get_blob_id()
        except KeyError:
            if strict:
                raise
            blob_id = cast(Union[Unset, str], UNSET)

        def get_transform_data_type() -> Union[Unset, str]:
            transform_data_type = d.pop("transformDataType")
            return transform_data_type

        try:
            transform_data_type = get_transform_data_type()
        except KeyError:
            if strict:
                raise
            transform_data_type = cast(Union[Unset, str], UNSET)

        convert_to_csv_response_200_item = cls(
            blob_id=blob_id,
            transform_data_type=transform_data_type,
        )

        convert_to_csv_response_200_item.additional_properties = d
        return convert_to_csv_response_200_item

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
    def blob_id(self) -> str:
        if isinstance(self._blob_id, Unset):
            raise NotPresentError(self, "blob_id")
        return self._blob_id

    @blob_id.setter
    def blob_id(self, value: str) -> None:
        self._blob_id = value

    @blob_id.deleter
    def blob_id(self) -> None:
        self._blob_id = UNSET

    @property
    def transform_data_type(self) -> str:
        if isinstance(self._transform_data_type, Unset):
            raise NotPresentError(self, "transform_data_type")
        return self._transform_data_type

    @transform_data_type.setter
    def transform_data_type(self, value: str) -> None:
        self._transform_data_type = value

    @transform_data_type.deleter
    def transform_data_type(self) -> None:
        self._transform_data_type = UNSET
