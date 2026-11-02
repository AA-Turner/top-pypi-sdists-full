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
from ..types import UNSET, Unset


T = TypeVar("T", bound="JobWithURL")


@attr.s(auto_attribs=True)
class JobWithURL:
    """
    ### Attributes:
    * `job_id (Union[Unset, str])`: None
    * `job_url (Union[Unset, str])`: None
    """

    job_id: Union[Unset, str] = UNSET
    job_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job_id = self.job_id
        job_url = self.job_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if job_url is not UNSET:
            field_dict["job_url"] = job_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        job_id = d.pop("job_id", UNSET)

        job_url = d.pop("job_url", UNSET)

        job_with_url = cls(
            job_id=job_id,
            job_url=job_url,
        )

        job_with_url.additional_properties = d
        return job_with_url

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
