from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.download_openapi_spec_json_body_webhook_filters_item_runnable_kind import (
    DownloadOpenapiSpecJsonBodyWebhookFiltersItemRunnableKind,
)
from ..models.download_openapi_spec_json_body_webhook_filters_item_user_or_folder_regex import (
    DownloadOpenapiSpecJsonBodyWebhookFiltersItemUserOrFolderRegex,
)

T = TypeVar("T", bound="DownloadOpenapiSpecJsonBodyWebhookFiltersItem")


@_attrs_define
class DownloadOpenapiSpecJsonBodyWebhookFiltersItem:
    """
    Attributes:
        user_or_folder_regex (DownloadOpenapiSpecJsonBodyWebhookFiltersItemUserOrFolderRegex):
        user_or_folder_regex_value (str):
        path (str):
        runnable_kind (DownloadOpenapiSpecJsonBodyWebhookFiltersItemRunnableKind):
    """

    user_or_folder_regex: DownloadOpenapiSpecJsonBodyWebhookFiltersItemUserOrFolderRegex
    user_or_folder_regex_value: str
    path: str
    runnable_kind: DownloadOpenapiSpecJsonBodyWebhookFiltersItemRunnableKind
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
        user_or_folder_regex = DownloadOpenapiSpecJsonBodyWebhookFiltersItemUserOrFolderRegex(
            d.pop("user_or_folder_regex")
        )

        user_or_folder_regex_value = d.pop("user_or_folder_regex_value")

        path = d.pop("path")

        runnable_kind = DownloadOpenapiSpecJsonBodyWebhookFiltersItemRunnableKind(d.pop("runnable_kind"))

        download_openapi_spec_json_body_webhook_filters_item = cls(
            user_or_folder_regex=user_or_folder_regex,
            user_or_folder_regex_value=user_or_folder_regex_value,
            path=path,
            runnable_kind=runnable_kind,
        )

        download_openapi_spec_json_body_webhook_filters_item.additional_properties = d
        return download_openapi_spec_json_body_webhook_filters_item

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
