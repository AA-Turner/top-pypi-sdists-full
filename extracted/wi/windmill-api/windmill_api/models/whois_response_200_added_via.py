from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.whois_response_200_added_via_source import WhoisResponse200AddedViaSource
from ..types import UNSET, Unset

T = TypeVar("T", bound="WhoisResponse200AddedVia")


@_attrs_define
class WhoisResponse200AddedVia:
    """
    Attributes:
        source (WhoisResponse200AddedViaSource): How the user was added to the workspace
        domain (Union[Unset, str]): The domain used for auto-invite (when source is 'domain')
        group (Union[Unset, str]): The instance group name (when source is 'instance_group')
    """

    source: WhoisResponse200AddedViaSource
    domain: Union[Unset, str] = UNSET
    group: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        source = self.source.value

        domain = self.domain
        group = self.group

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source": source,
            }
        )
        if domain is not UNSET:
            field_dict["domain"] = domain
        if group is not UNSET:
            field_dict["group"] = group

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        source = WhoisResponse200AddedViaSource(d.pop("source"))

        domain = d.pop("domain", UNSET)

        group = d.pop("group", UNSET)

        whois_response_200_added_via = cls(
            source=source,
            domain=domain,
            group=group,
        )

        whois_response_200_added_via.additional_properties = d
        return whois_response_200_added_via

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
