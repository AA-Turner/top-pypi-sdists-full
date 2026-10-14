from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SecurityDetail")


@_attrs_define
class SecurityDetail:
    """
    Attributes:
        urgency (str):
        affected_versions (str):
        exploitability (str):
        mitigation (str):
        cve (Union[None, Unset, str]):
        ghsa (Union[None, Unset, str]):
        advisory_url (Union[None, Unset, str]):
    """

    urgency: str
    affected_versions: str
    exploitability: str
    mitigation: str
    cve: Union[None, Unset, str] = UNSET
    ghsa: Union[None, Unset, str] = UNSET
    advisory_url: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        urgency = self.urgency

        affected_versions = self.affected_versions

        exploitability = self.exploitability

        mitigation = self.mitigation

        cve: Union[None, Unset, str]
        if isinstance(self.cve, Unset):
            cve = UNSET
        else:
            cve = self.cve

        ghsa: Union[None, Unset, str]
        if isinstance(self.ghsa, Unset):
            ghsa = UNSET
        else:
            ghsa = self.ghsa

        advisory_url: Union[None, Unset, str]
        if isinstance(self.advisory_url, Unset):
            advisory_url = UNSET
        else:
            advisory_url = self.advisory_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "urgency": urgency,
                "affected_versions": affected_versions,
                "exploitability": exploitability,
                "mitigation": mitigation,
            }
        )
        if cve is not UNSET:
            field_dict["cve"] = cve
        if ghsa is not UNSET:
            field_dict["ghsa"] = ghsa
        if advisory_url is not UNSET:
            field_dict["advisory_url"] = advisory_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        urgency = d.pop("urgency")

        affected_versions = d.pop("affected_versions")

        exploitability = d.pop("exploitability")

        mitigation = d.pop("mitigation")

        def _parse_cve(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        cve = _parse_cve(d.pop("cve", UNSET))

        def _parse_ghsa(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        ghsa = _parse_ghsa(d.pop("ghsa", UNSET))

        def _parse_advisory_url(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        advisory_url = _parse_advisory_url(d.pop("advisory_url", UNSET))

        security_detail = cls(
            urgency=urgency,
            affected_versions=affected_versions,
            exploitability=exploitability,
            mitigation=mitigation,
            cve=cve,
            ghsa=ghsa,
            advisory_url=advisory_url,
        )

        security_detail.additional_properties = d
        return security_detail

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
