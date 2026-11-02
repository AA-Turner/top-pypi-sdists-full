from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.webhook_filters_runnable_kind import WebhookFiltersRunnableKind
from ..models.webhook_filters_user_or_folder_regex import WebhookFiltersUserOrFolderRegex

T = TypeVar("T", bound="WebhookFilters")


@_attrs_define
class WebhookFilters:
    """
    Attributes:
        user_or_folder_regex (WebhookFiltersUserOrFolderRegex):
        user_or_folder_regex_value (str):
        path (str):
        runnable_kind (WebhookFiltersRunnableKind):
    """

    user_or_folder_regex: WebhookFiltersUserOrFolderRegex
    user_or_folder_regex_value: str
    path: str
    runnable_kind: WebhookFiltersRunnableKind
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        user_or_folder_regex = self.user_or_folder_regex.value

        user_or_folder_regex_value = self.user_or_folder_regex_value
        path = self.path
        runnable_kind = self.runnable_kind.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "user_or_folder_regex": user_or_folder_regex,
                "user_or_folder_regex_value": user_or_folder_regex_value,
                "path": path,
                "runnable_kind": runnable_kind,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        user_or_folder_regex = WebhookFiltersUserOrFolderRegex(d.pop("user_or_folder_regex"))

        user_or_folder_regex_value = d.pop("user_or_folder_regex_value")

        path = d.pop("path")

        runnable_kind = WebhookFiltersRunnableKind(d.pop("runnable_kind"))

        webhook_filters = cls(
            user_or_folder_regex=user_or_folder_regex,
            user_or_folder_regex_value=user_or_folder_regex_value,
            path=path,
            runnable_kind=runnable_kind,
        )

        webhook_filters.additional_properties = d
        return webhook_filters

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
