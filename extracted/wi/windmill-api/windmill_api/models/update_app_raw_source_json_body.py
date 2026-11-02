from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.update_app_raw_source_json_body_policy import UpdateAppRawSourceJsonBodyPolicy
    from ..models.update_app_raw_source_json_body_value import UpdateAppRawSourceJsonBodyValue


T = TypeVar("T", bound="UpdateAppRawSourceJsonBody")


@_attrs_define
class UpdateAppRawSourceJsonBody:
    """
    Attributes:
        value (UpdateAppRawSourceJsonBodyValue): The raw app's value. `files` maps each source path (e.g. `/index.tsx`,
            `/App.tsx`, `/package.json`) to its content and must contain an entry point (`/index.tsx`, `/index.ts` or
            `/index.js`); `runnables` and `data` are carried through unchanged.
        path (Union[Unset, str]):
        summary (Union[Unset, str]):
        policy (Union[Unset, UpdateAppRawSourceJsonBodyPolicy]):
        deployment_message (Union[Unset, str]):
        custom_path (Union[Unset, str]):
        preserve_on_behalf_of (Union[Unset, bool]): When true and the caller is a member of the 'wm_deployers' group,
            preserves the original on_behalf_of value in the policy instead of overwriting it.
        labels (Union[Unset, List[str]]):
        skip_draft_deletion (Union[Unset, bool]): When true (set by the CLI / git sync), deploying this app does not
            delete an existing user draft at the same path.
        allow_kind_change (Union[Unset, bool]): When true, this deploy may switch the app between low-code and raw.
            Without it, deploying a value to an app of the other kind is refused so an app is never converted by accident.
    """

    value: "UpdateAppRawSourceJsonBodyValue"
    path: Union[Unset, str] = UNSET
    summary: Union[Unset, str] = UNSET
    policy: Union[Unset, "UpdateAppRawSourceJsonBodyPolicy"] = UNSET
    deployment_message: Union[Unset, str] = UNSET
    custom_path: Union[Unset, str] = UNSET
    preserve_on_behalf_of: Union[Unset, bool] = UNSET
    labels: Union[Unset, List[str]] = UNSET
    skip_draft_deletion: Union[Unset, bool] = UNSET
    allow_kind_change: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        value = self.value.to_dict()

        path = self.path
        summary = self.summary
        policy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.policy, Unset):
            policy = self.policy.to_dict()

        deployment_message = self.deployment_message
        custom_path = self.custom_path
        preserve_on_behalf_of = self.preserve_on_behalf_of
        labels: Union[Unset, List[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        skip_draft_deletion = self.skip_draft_deletion
        allow_kind_change = self.allow_kind_change

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "value": value,
            }
        )
        if path is not UNSET:
            field_dict["path"] = path
        if summary is not UNSET:
            field_dict["summary"] = summary
        if policy is not UNSET:
            field_dict["policy"] = policy
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
        if allow_kind_change is not UNSET:
            field_dict["allow_kind_change"] = allow_kind_change

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.update_app_raw_source_json_body_policy import UpdateAppRawSourceJsonBodyPolicy
        from ..models.update_app_raw_source_json_body_value import UpdateAppRawSourceJsonBodyValue

        d = src_dict.copy()
        value = UpdateAppRawSourceJsonBodyValue.from_dict(d.pop("value"))

        path = d.pop("path", UNSET)

        summary = d.pop("summary", UNSET)

        _policy = d.pop("policy", UNSET)
        policy: Union[Unset, UpdateAppRawSourceJsonBodyPolicy]
        if isinstance(_policy, Unset):
            policy = UNSET
        else:
            policy = UpdateAppRawSourceJsonBodyPolicy.from_dict(_policy)

        deployment_message = d.pop("deployment_message", UNSET)

        custom_path = d.pop("custom_path", UNSET)

        preserve_on_behalf_of = d.pop("preserve_on_behalf_of", UNSET)

        labels = cast(List[str], d.pop("labels", UNSET))

        skip_draft_deletion = d.pop("skip_draft_deletion", UNSET)

        allow_kind_change = d.pop("allow_kind_change", UNSET)

        update_app_raw_source_json_body = cls(
            value=value,
            path=path,
            summary=summary,
            policy=policy,
            deployment_message=deployment_message,
            custom_path=custom_path,
            preserve_on_behalf_of=preserve_on_behalf_of,
            labels=labels,
            skip_draft_deletion=skip_draft_deletion,
            allow_kind_change=allow_kind_change,
        )

        update_app_raw_source_json_body.additional_properties = d
        return update_app_raw_source_json_body

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
