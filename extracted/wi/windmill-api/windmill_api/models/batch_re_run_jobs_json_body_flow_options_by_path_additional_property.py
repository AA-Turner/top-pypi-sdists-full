from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.batch_re_run_jobs_json_body_flow_options_by_path_additional_property_input_transforms import (
        BatchReRunJobsJsonBodyFlowOptionsByPathAdditionalPropertyInputTransforms,
    )


T = TypeVar("T", bound="BatchReRunJobsJsonBodyFlowOptionsByPathAdditionalProperty")


@_attrs_define
class BatchReRunJobsJsonBodyFlowOptionsByPathAdditionalProperty:
    """
    Attributes:
        input_transforms (Union[Unset, BatchReRunJobsJsonBodyFlowOptionsByPathAdditionalPropertyInputTransforms]):
        use_latest_version (Union[Unset, bool]):
    """

    input_transforms: Union[Unset, "BatchReRunJobsJsonBodyFlowOptionsByPathAdditionalPropertyInputTransforms"] = UNSET
    use_latest_version: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        input_transforms: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.input_transforms, Unset):
            input_transforms = self.input_transforms.to_dict()

        use_latest_version = self.use_latest_version

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if input_transforms is not UNSET:
            field_dict["input_transforms"] = input_transforms
        if use_latest_version is not UNSET:
            field_dict["use_latest_version"] = use_latest_version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.batch_re_run_jobs_json_body_flow_options_by_path_additional_property_input_transforms import (
            BatchReRunJobsJsonBodyFlowOptionsByPathAdditionalPropertyInputTransforms,
        )

        d = src_dict.copy()
        _input_transforms = d.pop("input_transforms", UNSET)
        input_transforms: Union[Unset, BatchReRunJobsJsonBodyFlowOptionsByPathAdditionalPropertyInputTransforms]
        if isinstance(_input_transforms, Unset):
            input_transforms = UNSET
        else:
            input_transforms = BatchReRunJobsJsonBodyFlowOptionsByPathAdditionalPropertyInputTransforms.from_dict(
                _input_transforms
            )

        use_latest_version = d.pop("use_latest_version", UNSET)

        batch_re_run_jobs_json_body_flow_options_by_path_additional_property = cls(
            input_transforms=input_transforms,
            use_latest_version=use_latest_version,
        )

        batch_re_run_jobs_json_body_flow_options_by_path_additional_property.additional_properties = d
        return batch_re_run_jobs_json_body_flow_options_by_path_additional_property

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
