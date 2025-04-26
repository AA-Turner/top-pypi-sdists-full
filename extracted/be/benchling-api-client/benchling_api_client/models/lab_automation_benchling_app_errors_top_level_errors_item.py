from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="LabAutomationBenchlingAppErrorsTopLevelErrorsItem")


@attr.s(auto_attribs=True, repr=False)
class LabAutomationBenchlingAppErrorsTopLevelErrorsItem:
    """  """

    _error_message: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("error_message={}".format(repr(self._error_message)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "LabAutomationBenchlingAppErrorsTopLevelErrorsItem({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        error_message = self._error_message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if error_message is not UNSET:
            field_dict["errorMessage"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_error_message() -> Union[Unset, str]:
            error_message = d.pop("errorMessage")
            return error_message

        try:
            error_message = get_error_message()
        except KeyError:
            if strict:
                raise
            error_message = cast(Union[Unset, str], UNSET)

        lab_automation_benchling_app_errors_top_level_errors_item = cls(
            error_message=error_message,
        )

        lab_automation_benchling_app_errors_top_level_errors_item.additional_properties = d
        return lab_automation_benchling_app_errors_top_level_errors_item

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
    def error_message(self) -> str:
        if isinstance(self._error_message, Unset):
            raise NotPresentError(self, "error_message")
        return self._error_message

    @error_message.setter
    def error_message(self, value: str) -> None:
        self._error_message = value

    @error_message.deleter
    def error_message(self) -> None:
        self._error_message = UNSET
