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

from typing import Union
from typing import cast
from typing import Dict
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.entity_response_s3_urls import EntityResponseS3Urls


T = TypeVar("T", bound="EntityResponse")


@attr.s(auto_attribs=True)
class EntityResponse:
    """
    ### Attributes:
    * `s3_urls (Union[Unset, EntityResponseS3Urls])`:
    * `status (Union[Unset, str])`: None
    """

    s3_urls: Union[Unset, "EntityResponseS3Urls"] = UNSET
    status: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.entity_response_s3_urls import EntityResponseS3Urls

        s3_urls: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.s3_urls, Unset):
            s3_urls = self.s3_urls.to_dict()

        status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if s3_urls is not UNSET:
            field_dict["s3_urls"] = s3_urls
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.entity_response_s3_urls import EntityResponseS3Urls

        d = src_dict.copy()
        _s3_urls = d.pop("s3_urls", UNSET)
        s3_urls: Union[Unset, EntityResponseS3Urls]
        if isinstance(_s3_urls, Unset):
            s3_urls = UNSET
        else:
            s3_urls = EntityResponseS3Urls.from_dict(_s3_urls)

        status = d.pop("status", UNSET)

        entity_response = cls(
            s3_urls=s3_urls,
            status=status,
        )

        entity_response.additional_properties = d
        return entity_response

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
