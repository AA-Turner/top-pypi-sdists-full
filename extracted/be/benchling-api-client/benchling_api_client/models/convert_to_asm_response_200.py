from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConvertToASMResponse_200")


@attr.s(auto_attribs=True, repr=False)
class ConvertToASMResponse_200:
    """  """

    _blob_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("blob_id={}".format(repr(self._blob_id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "ConvertToASMResponse_200({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        blob_id = self._blob_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if blob_id is not UNSET:
            field_dict["blobId"] = blob_id

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

        convert_to_asm_response_200 = cls(
            blob_id=blob_id,
        )

        convert_to_asm_response_200.additional_properties = d
        return convert_to_asm_response_200

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
