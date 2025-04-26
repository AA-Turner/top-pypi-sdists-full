from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_app_json_body_policy import CreateAppJsonBodyPolicy


T = TypeVar("T", bound="CreateAppJsonBody")


@_attrs_define
class CreateAppJsonBody:
    """
    Attributes:
        path (str):
        value (Any):
        summary (str):
        policy (CreateAppJsonBodyPolicy):
        draft_only (Union[Unset, bool]):
        deployment_message (Union[Unset, str]):
        custom_path (Union[Unset, str]):
    """

    path: str
    value: Any
    summary: str
    policy: "CreateAppJsonBodyPolicy"
    draft_only: Union[Unset, bool] = UNSET
    deployment_message: Union[Unset, str] = UNSET
    custom_path: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        value = self.value
        summary = self.summary
        policy = self.policy.to_dict()

        draft_only = self.draft_only
        deployment_message = self.deployment_message
        custom_path = self.custom_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "value": value,
                "summary": summary,
                "policy": policy,
            }
        )
        if draft_only is not UNSET:
            field_dict["draft_only"] = draft_only
        if deployment_message is not UNSET:
            field_dict["deployment_message"] = deployment_message
        if custom_path is not UNSET:
            field_dict["custom_path"] = custom_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_app_json_body_policy import CreateAppJsonBodyPolicy

        d = src_dict.copy()
        path = d.pop("path")

        value = d.pop("value")

        summary = d.pop("summary")

        policy = CreateAppJsonBodyPolicy.from_dict(d.pop("policy"))

        draft_only = d.pop("draft_only", UNSET)

        deployment_message = d.pop("deployment_message", UNSET)

        custom_path = d.pop("custom_path", UNSET)

        create_app_json_body = cls(
            path=path,
            value=value,
            summary=summary,
            policy=policy,
            draft_only=draft_only,
            deployment_message=deployment_message,
            custom_path=custom_path,
        )

        create_app_json_body.additional_properties = d
        return create_app_json_body

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
