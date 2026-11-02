from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_app_raw_source_json_body_policy import CreateAppRawSourceJsonBodyPolicy
    from ..models.create_app_raw_source_json_body_value import CreateAppRawSourceJsonBodyValue


T = TypeVar("T", bound="CreateAppRawSourceJsonBody")


@_attrs_define
class CreateAppRawSourceJsonBody:
    """
    Attributes:
        path (str):
        summary (str):
        value (CreateAppRawSourceJsonBodyValue): The raw app's value. `files` maps each source path to its content and
            must contain an entry point; `runnables` and `data` are carried through unchanged.
        policy (CreateAppRawSourceJsonBodyPolicy):
        deployment_message (Union[Unset, str]):
        custom_path (Union[Unset, str]):
        preserve_on_behalf_of (Union[Unset, bool]): When true and the caller is a member of the 'wm_deployers' group,
            preserves the original on_behalf_of value in the policy instead of overwriting it.
        labels (Union[Unset, List[str]]):
        skip_draft_deletion (Union[Unset, bool]): When true (set by the CLI / git sync), deploying this app does not
            delete an existing user draft at the same path.
    """

    path: str
    summary: str
    value: "CreateAppRawSourceJsonBodyValue"
    policy: "CreateAppRawSourceJsonBodyPolicy"
    deployment_message: Union[Unset, str] = UNSET
    custom_path: Union[Unset, str] = UNSET
    preserve_on_behalf_of: Union[Unset, bool] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    skip_draft_deletion: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        summary = self.summary
        value = self.value.to_dict()

        policy = self.policy.to_dict()

        deployment_message = self.deployment_message
        custom_path = self.custom_path
        preserve_on_behalf_of = self.preserve_on_behalf_of
        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        skip_draft_deletion = self.skip_draft_deletion

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "summary": summary,
                "value": value,
                "policy": policy,
            }
        )
        if deployment_message is not UNSET:
            field_dict["deployment_message"] = deployment_message
        if custom_path is not UNSET:
            field_dict["custom_path"] = custom_path
        if preserve_on_behalf_of is not UNSET:
            field_dict["preserve_on_behalf_of"] = preserve_on_behalf_of
        if labels is not UNSET:
            field_dict["labels"] = labels
        if skip_draft_deletion is not UNSET:
            field_dict["skip_draft_deletion"] = skip_draft_deletion

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_app_raw_source_json_body_policy import CreateAppRawSourceJsonBodyPolicy
        from ..models.create_app_raw_source_json_body_value import CreateAppRawSourceJsonBodyValue

        d = src_dict.copy()
        path = d.pop("path")

        summary = d.pop("summary")

        value = CreateAppRawSourceJsonBodyValue.from_dict(d.pop("value"))

        policy = CreateAppRawSourceJsonBodyPolicy.from_dict(d.pop("policy"))

        deployment_message = d.pop("deployment_message", UNSET)

        custom_path = d.pop("custom_path", UNSET)

        preserve_on_behalf_of = d.pop("preserve_on_behalf_of", UNSET)

        labels = cast(List[str], d.pop("labels", UNSET))

        skip_draft_deletion = d.pop("skip_draft_deletion", UNSET)

        create_app_raw_source_json_body = cls(
            path=path,
            summary=summary,
            value=value,
            policy=policy,
            deployment_message=deployment_message,
            custom_path=custom_path,
            preserve_on_behalf_of=preserve_on_behalf_of,
            labels=labels,
            skip_draft_deletion=skip_draft_deletion,
        )

        create_app_raw_source_json_body.additional_properties = d
        return create_app_raw_source_json_body

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
