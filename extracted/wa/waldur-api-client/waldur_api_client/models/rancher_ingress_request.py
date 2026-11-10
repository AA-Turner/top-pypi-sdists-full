from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rancher_ingress_request_rules import RancherIngressRequestRules


T = TypeVar("T", bound="RancherIngressRequest")


@_attrs_define
class RancherIngressRequest:
    """
    Attributes:
        name (str):
        service_settings (str):
        project (str):
        rancher_project (str):
        description (Union[Unset, str]):
        namespace (Union[Unset, str]):
        rules (Union[Unset, RancherIngressRequestRules]):
    """

    name: str
    service_settings: str
    project: str
    rancher_project: str
    description: Union[Unset, str] = UNSET
    namespace: Union[Unset, str] = UNSET
    rules: Union[Unset, "RancherIngressRequestRules"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        service_settings = self.service_settings

        project = self.project

        rancher_project = self.rancher_project

        description = self.description

        namespace = self.namespace

        rules: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.rules, Unset):
            rules = self.rules.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "service_settings": service_settings,
                "project": project,
                "rancher_project": rancher_project,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if namespace is not UNSET:
            field_dict["namespace"] = namespace
        if rules is not UNSET:
            field_dict["rules"] = rules

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rancher_ingress_request_rules import RancherIngressRequestRules

        d = dict(src_dict)
        name = d.pop("name")

        service_settings = d.pop("service_settings")

        project = d.pop("project")

        rancher_project = d.pop("rancher_project")

        description = d.pop("description", UNSET)

        namespace = d.pop("namespace", UNSET)

        _rules = d.pop("rules", UNSET)
        rules: Union[Unset, RancherIngressRequestRules]
        if isinstance(_rules, Unset):
            rules = UNSET
        else:
            rules = RancherIngressRequestRules.from_dict(_rules)

        rancher_ingress_request = cls(
            name=name,
            service_settings=service_settings,
            project=project,
            rancher_project=rancher_project,
            description=description,
            namespace=namespace,
            rules=rules,
        )

        rancher_ingress_request.additional_properties = d
        return rancher_ingress_request

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
