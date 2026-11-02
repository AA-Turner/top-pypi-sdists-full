from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="GetGitSyncDeployModeResponse200")


@_attrs_define
class GetGitSyncDeployModeResponse200:
    """
    Attributes:
        configured (bool): At least one git-sync repository is configured.
        deploy_on_push (bool): True means a `git push` is confirmed to deploy via auto-pull: exactly one licensed,
            deliverable repository tracks the branch. False is *not confirmed* rather than a definite no — it also covers
            unlicensed, ambiguous (several repos track it), and conservative false-negatives; determine the deploy path
            another way (CI `git push`, or `wmill sync push`).
    """

    configured: bool
    deploy_on_push: bool
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        configured = self.configured
        deploy_on_push = self.deploy_on_push

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "configured": configured,
                "deploy_on_push": deploy_on_push,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        configured = d.pop("configured")

        deploy_on_push = d.pop("deploy_on_push")

        get_git_sync_deploy_mode_response_200 = cls(
            configured=configured,
            deploy_on_push=deploy_on_push,
        )

        get_git_sync_deploy_mode_response_200.additional_properties = d
        return get_git_sync_deploy_mode_response_200

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
