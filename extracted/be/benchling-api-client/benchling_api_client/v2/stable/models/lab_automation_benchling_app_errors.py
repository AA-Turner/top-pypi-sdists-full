from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.lab_automation_benchling_app_errors_top_level_errors_item import (
    LabAutomationBenchlingAppErrorsTopLevelErrorsItem,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="LabAutomationBenchlingAppErrors")


@attr.s(auto_attribs=True, repr=False)
class LabAutomationBenchlingAppErrors:
    """  """

    _top_level_errors: Union[Unset, List[LabAutomationBenchlingAppErrorsTopLevelErrorsItem]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("top_level_errors={}".format(repr(self._top_level_errors)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "LabAutomationBenchlingAppErrors({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        top_level_errors: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._top_level_errors, Unset):
            top_level_errors = []
            for top_level_errors_item_data in self._top_level_errors:
                top_level_errors_item = top_level_errors_item_data.to_dict()

                top_level_errors.append(top_level_errors_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if top_level_errors is not UNSET:
            field_dict["topLevelErrors"] = top_level_errors

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_top_level_errors() -> Union[Unset, List[LabAutomationBenchlingAppErrorsTopLevelErrorsItem]]:
            top_level_errors = []
            _top_level_errors = d.pop("topLevelErrors")
            for top_level_errors_item_data in _top_level_errors or []:
                top_level_errors_item = LabAutomationBenchlingAppErrorsTopLevelErrorsItem.from_dict(
                    top_level_errors_item_data, strict=False
                )

                top_level_errors.append(top_level_errors_item)

            return top_level_errors

        try:
            top_level_errors = get_top_level_errors()
        except KeyError:
            if strict:
                raise
            top_level_errors = cast(
                Union[Unset, List[LabAutomationBenchlingAppErrorsTopLevelErrorsItem]], UNSET
            )

        lab_automation_benchling_app_errors = cls(
            top_level_errors=top_level_errors,
        )

        lab_automation_benchling_app_errors.additional_properties = d
        return lab_automation_benchling_app_errors

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

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def top_level_errors(self) -> List[LabAutomationBenchlingAppErrorsTopLevelErrorsItem]:
        if isinstance(self._top_level_errors, Unset):
            raise NotPresentError(self, "top_level_errors")
        return self._top_level_errors

    @top_level_errors.setter
    def top_level_errors(self, value: List[LabAutomationBenchlingAppErrorsTopLevelErrorsItem]) -> None:
        self._top_level_errors = value

    @top_level_errors.deleter
    def top_level_errors(self) -> None:
        self._top_level_errors = UNSET
