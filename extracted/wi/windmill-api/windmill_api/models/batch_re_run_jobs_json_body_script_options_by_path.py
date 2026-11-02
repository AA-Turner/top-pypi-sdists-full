from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.batch_re_run_jobs_json_body_script_options_by_path_additional_property import (
        BatchReRunJobsJsonBodyScriptOptionsByPathAdditionalProperty,
    )


T = TypeVar("T", bound="BatchReRunJobsJsonBodyScriptOptionsByPath")


@_attrs_define
class BatchReRunJobsJsonBodyScriptOptionsByPath:
    """ """

    additional_properties: Dict[str, "BatchReRunJobsJsonBodyScriptOptionsByPathAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.batch_re_run_jobs_json_body_script_options_by_path_additional_property import (
            BatchReRunJobsJsonBodyScriptOptionsByPathAdditionalProperty,
        )

        d = src_dict.copy()
        batch_re_run_jobs_json_body_script_options_by_path = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = BatchReRunJobsJsonBodyScriptOptionsByPathAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        batch_re_run_jobs_json_body_script_options_by_path.additional_properties = additional_properties
        return batch_re_run_jobs_json_body_script_options_by_path

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "BatchReRunJobsJsonBodyScriptOptionsByPathAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "BatchReRunJobsJsonBodyScriptOptionsByPathAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
