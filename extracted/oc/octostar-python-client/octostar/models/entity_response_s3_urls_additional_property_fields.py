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


T = TypeVar("T", bound="EntityResponseS3UrlsAdditionalPropertyFields")


@attr.s(auto_attribs=True)
class EntityResponseS3UrlsAdditionalPropertyFields:
    """
    ### Attributes:
    * `key (Union[Unset, str])`: None
    * `policy (Union[Unset, str])`: None
    * `x-amz-algorithm (Union[Unset, str])`: None
    * `x-amz-credential (Union[Unset, str])`: None
    * `x-amz-date (Union[Unset, str])`: None
    * `x-amz-signature (Union[Unset, str])`: None
    """

    key: Union[Unset, str] = UNSET
    policy: Union[Unset, str] = UNSET
    x_amz_algorithm: Union[Unset, str] = UNSET
    x_amz_credential: Union[Unset, str] = UNSET
    x_amz_date: Union[Unset, str] = UNSET
    x_amz_signature: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        key = self.key
        policy = self.policy
        x_amz_algorithm = self.x_amz_algorithm
        x_amz_credential = self.x_amz_credential
        x_amz_date = self.x_amz_date
        x_amz_signature = self.x_amz_signature

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if policy is not UNSET:
            field_dict["policy"] = policy
        if x_amz_algorithm is not UNSET:
            field_dict["x-amz-algorithm"] = x_amz_algorithm
        if x_amz_credential is not UNSET:
            field_dict["x-amz-credential"] = x_amz_credential
        if x_amz_date is not UNSET:
            field_dict["x-amz-date"] = x_amz_date
        if x_amz_signature is not UNSET:
            field_dict["x-amz-signature"] = x_amz_signature

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key", UNSET)

        policy = d.pop("policy", UNSET)

        x_amz_algorithm = d.pop("x-amz-algorithm", UNSET)

        x_amz_credential = d.pop("x-amz-credential", UNSET)

        x_amz_date = d.pop("x-amz-date", UNSET)

        x_amz_signature = d.pop("x-amz-signature", UNSET)

        entity_response_s3_urls_additional_property_fields = cls(
            key=key,
            policy=policy,
            x_amz_algorithm=x_amz_algorithm,
            x_amz_credential=x_amz_credential,
            x_amz_date=x_amz_date,
            x_amz_signature=x_amz_signature,
        )

        entity_response_s3_urls_additional_property_fields.additional_properties = d
        return entity_response_s3_urls_additional_property_fields

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
