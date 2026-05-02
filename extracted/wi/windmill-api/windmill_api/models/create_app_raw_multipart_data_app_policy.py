from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.create_app_raw_multipart_data_app_policy_execution_mode import (
    CreateAppRawMultipartDataAppPolicyExecutionMode,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.create_app_raw_multipart_data_app_policy_allowed_s3_keys_item import (
        CreateAppRawMultipartDataAppPolicyAllowedS3KeysItem,
    )
    from ..models.create_app_raw_multipart_data_app_policy_s3_inputs_item import (
        CreateAppRawMultipartDataAppPolicyS3InputsItem,
    )
    from ..models.create_app_raw_multipart_data_app_policy_triggerables import (
        CreateAppRawMultipartDataAppPolicyTriggerables,
    )
    from ..models.create_app_raw_multipart_data_app_policy_triggerables_v2 import (
        CreateAppRawMultipartDataAppPolicyTriggerablesV2,
    )


T = TypeVar("T", bound="CreateAppRawMultipartDataAppPolicy")


@_attrs_define
class CreateAppRawMultipartDataAppPolicy:
    """
    Attributes:
        triggerables (Union[Unset, CreateAppRawMultipartDataAppPolicyTriggerables]):
        triggerables_v2 (Union[Unset, CreateAppRawMultipartDataAppPolicyTriggerablesV2]):
        s3_inputs (Union[Unset, List['CreateAppRawMultipartDataAppPolicyS3InputsItem']]):
        allowed_s3_keys (Union[Unset, List['CreateAppRawMultipartDataAppPolicyAllowedS3KeysItem']]):
        execution_mode (Union[Unset, CreateAppRawMultipartDataAppPolicyExecutionMode]):
        on_behalf_of (Union[Unset, str]):
        on_behalf_of_email (Union[Unset, str]):
    """

    triggerables: Union[Unset, "CreateAppRawMultipartDataAppPolicyTriggerables"] = UNSET
    triggerables_v2: Union[Unset, "CreateAppRawMultipartDataAppPolicyTriggerablesV2"] = UNSET
    s3_inputs: Union[Unset, List["CreateAppRawMultipartDataAppPolicyS3InputsItem"]] = UNSET
    allowed_s3_keys: Union[Unset, List["CreateAppRawMultipartDataAppPolicyAllowedS3KeysItem"]] = UNSET
    execution_mode: Union[Unset, CreateAppRawMultipartDataAppPolicyExecutionMode] = UNSET
    on_behalf_of: Union[Unset, str] = UNSET
    on_behalf_of_email: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        triggerables: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.triggerables, Unset):
            triggerables = self.triggerables.to_dict()

        triggerables_v2: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.triggerables_v2, Unset):
            triggerables_v2 = self.triggerables_v2.to_dict()

        s3_inputs: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.s3_inputs, Unset):
            s3_inputs = []
            for s3_inputs_item_data in self.s3_inputs:
                s3_inputs_item = s3_inputs_item_data.to_dict()

                s3_inputs.append(s3_inputs_item)

        allowed_s3_keys: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.allowed_s3_keys, Unset):
            allowed_s3_keys = []
            for allowed_s3_keys_item_data in self.allowed_s3_keys:
                allowed_s3_keys_item = allowed_s3_keys_item_data.to_dict()

                allowed_s3_keys.append(allowed_s3_keys_item)

        execution_mode: Union[Unset, str] = UNSET
        if not isinstance(self.execution_mode, Unset):
            execution_mode = self.execution_mode.value

        on_behalf_of = self.on_behalf_of
        on_behalf_of_email = self.on_behalf_of_email

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if triggerables is not UNSET:
            field_dict["triggerables"] = triggerables
        if triggerables_v2 is not UNSET:
            field_dict["triggerables_v2"] = triggerables_v2
        if s3_inputs is not UNSET:
            field_dict["s3_inputs"] = s3_inputs
        if allowed_s3_keys is not UNSET:
            field_dict["allowed_s3_keys"] = allowed_s3_keys
        if execution_mode is not UNSET:
            field_dict["execution_mode"] = execution_mode
        if on_behalf_of is not UNSET:
            field_dict["on_behalf_of"] = on_behalf_of
        if on_behalf_of_email is not UNSET:
            field_dict["on_behalf_of_email"] = on_behalf_of_email

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.create_app_raw_multipart_data_app_policy_allowed_s3_keys_item import (
            CreateAppRawMultipartDataAppPolicyAllowedS3KeysItem,
        )
        from ..models.create_app_raw_multipart_data_app_policy_s3_inputs_item import (
            CreateAppRawMultipartDataAppPolicyS3InputsItem,
        )
        from ..models.create_app_raw_multipart_data_app_policy_triggerables import (
            CreateAppRawMultipartDataAppPolicyTriggerables,
        )
        from ..models.create_app_raw_multipart_data_app_policy_triggerables_v2 import (
            CreateAppRawMultipartDataAppPolicyTriggerablesV2,
        )

        d = src_dict.copy()
        _triggerables = d.pop("triggerables", UNSET)
        triggerables: Union[Unset, CreateAppRawMultipartDataAppPolicyTriggerables]
        if isinstance(_triggerables, Unset):
            triggerables = UNSET
        else:
            triggerables = CreateAppRawMultipartDataAppPolicyTriggerables.from_dict(_triggerables)

        _triggerables_v2 = d.pop("triggerables_v2", UNSET)
        triggerables_v2: Union[Unset, CreateAppRawMultipartDataAppPolicyTriggerablesV2]
        if isinstance(_triggerables_v2, Unset):
            triggerables_v2 = UNSET
        else:
            triggerables_v2 = CreateAppRawMultipartDataAppPolicyTriggerablesV2.from_dict(_triggerables_v2)

        s3_inputs = []
        _s3_inputs = d.pop("s3_inputs", UNSET)
        for s3_inputs_item_data in _s3_inputs or []:
            s3_inputs_item = CreateAppRawMultipartDataAppPolicyS3InputsItem.from_dict(s3_inputs_item_data)

            s3_inputs.append(s3_inputs_item)

        allowed_s3_keys = []
        _allowed_s3_keys = d.pop("allowed_s3_keys", UNSET)
        for allowed_s3_keys_item_data in _allowed_s3_keys or []:
            allowed_s3_keys_item = CreateAppRawMultipartDataAppPolicyAllowedS3KeysItem.from_dict(
                allowed_s3_keys_item_data
            )

            allowed_s3_keys.append(allowed_s3_keys_item)

        _execution_mode = d.pop("execution_mode", UNSET)
        execution_mode: Union[Unset, CreateAppRawMultipartDataAppPolicyExecutionMode]
        if isinstance(_execution_mode, Unset):
            execution_mode = UNSET
        else:
            execution_mode = CreateAppRawMultipartDataAppPolicyExecutionMode(_execution_mode)

        on_behalf_of = d.pop("on_behalf_of", UNSET)

        on_behalf_of_email = d.pop("on_behalf_of_email", UNSET)

        create_app_raw_multipart_data_app_policy = cls(
            triggerables=triggerables,
            triggerables_v2=triggerables_v2,
            s3_inputs=s3_inputs,
            allowed_s3_keys=allowed_s3_keys,
            execution_mode=execution_mode,
            on_behalf_of=on_behalf_of,
            on_behalf_of_email=on_behalf_of_email,
        )

        create_app_raw_multipart_data_app_policy.additional_properties = d
        return create_app_raw_multipart_data_app_policy

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
