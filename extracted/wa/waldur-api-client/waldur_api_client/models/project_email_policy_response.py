from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="ProjectEmailPolicyResponse")


@_attrs_define
class ProjectEmailPolicyResponse:
    """
    Attributes:
        allowed_domains (Union[None, list[str]]):
    """

    allowed_domains: Union[None, list[str]]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        allowed_domains: Union[None, list[str]]
        if isinstance(self.allowed_domains, list):
            allowed_domains = self.allowed_domains

        else:
            allowed_domains = self.allowed_domains

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "allowed_domains": allowed_domains,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_allowed_domains(data: object) -> Union[None, list[str]]:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                allowed_domains_type_0 = cast(list[str], data)

                return allowed_domains_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, list[str]], data)

        allowed_domains = _parse_allowed_domains(d.pop("allowed_domains"))

        project_email_policy_response = cls(
            allowed_domains=allowed_domains,
        )

        project_email_policy_response.additional_properties = d
        return project_email_policy_response

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
