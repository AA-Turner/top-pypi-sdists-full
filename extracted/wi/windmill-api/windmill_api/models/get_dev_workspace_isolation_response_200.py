from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetDevWorkspaceIsolationResponse200")


@_attrs_define
class GetDevWorkspaceIsolationResponse200:
    """
    Attributes:
        enabled (bool): whether new jobs of dev workspaces and forks are queued on suffixed tags
        suffix (str): the suffix of those tags, which worker groups serving dev workspaces listen with
        skip_non_dev_forks (bool): whether forks of a workspace that is not a dev workspace, nor under one, run on their
            parent's workers instead
    """

    enabled: bool
    suffix: str
    skip_non_dev_forks: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        enabled = self.enabled
        suffix = self.suffix
        skip_non_dev_forks = self.skip_non_dev_forks

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "enabled": enabled,
                "suffix": suffix,
                "skip_non_dev_forks": skip_non_dev_forks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        enabled = d.pop("enabled")

        suffix = d.pop("suffix")

        skip_non_dev_forks = d.pop("skip_non_dev_forks")

        get_dev_workspace_isolation_response_200 = cls(
            enabled=enabled,
            suffix=suffix,
            skip_non_dev_forks=skip_non_dev_forks,
        )

        get_dev_workspace_isolation_response_200.additional_properties = d
        return get_dev_workspace_isolation_response_200

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
