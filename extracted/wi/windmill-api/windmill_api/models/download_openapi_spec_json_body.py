from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.download_openapi_spec_json_body_openapi_spec_format import DownloadOpenapiSpecJsonBodyOpenapiSpecFormat
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.download_openapi_spec_json_body_http_route_filters_item import (
        DownloadOpenapiSpecJsonBodyHttpRouteFiltersItem,
    )
    from ..models.download_openapi_spec_json_body_info import DownloadOpenapiSpecJsonBodyInfo
    from ..models.download_openapi_spec_json_body_webhook_filters_item import (
        DownloadOpenapiSpecJsonBodyWebhookFiltersItem,
    )


T = TypeVar("T", bound="DownloadOpenapiSpecJsonBody")


@_attrs_define
class DownloadOpenapiSpecJsonBody:
    """
    Attributes:
        info (Union[Unset, DownloadOpenapiSpecJsonBodyInfo]):
        url (Union[Unset, str]):
        openapi_spec_format (Union[Unset, DownloadOpenapiSpecJsonBodyOpenapiSpecFormat]):
        http_route_filters (Union[Unset, List['DownloadOpenapiSpecJsonBodyHttpRouteFiltersItem']]):
        webhook_filters (Union[Unset, List['DownloadOpenapiSpecJsonBodyWebhookFiltersItem']]):
    """

    info: Union[Unset, "DownloadOpenapiSpecJsonBodyInfo"] = UNSET
    url: Union[Unset, str] = UNSET
    openapi_spec_format: Union[Unset, DownloadOpenapiSpecJsonBodyOpenapiSpecFormat] = UNSET
    http_route_filters: Union[Unset, List["DownloadOpenapiSpecJsonBodyHttpRouteFiltersItem"]] = UNSET
    webhook_filters: Union[Unset, List["DownloadOpenapiSpecJsonBodyWebhookFiltersItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.info, Unset):
            info = self.info.to_dict()

        url = self.url
        openapi_spec_format: Union[Unset, str] = UNSET
        if not isinstance(self.openapi_spec_format, Unset):
            openapi_spec_format = self.openapi_spec_format.value

        http_route_filters: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.http_route_filters, Unset):
            http_route_filters = []
            for http_route_filters_item_data in self.http_route_filters:
                http_route_filters_item = http_route_filters_item_data.to_dict()

                http_route_filters.append(http_route_filters_item)

        webhook_filters: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.webhook_filters, Unset):
            webhook_filters = []
            for webhook_filters_item_data in self.webhook_filters:
                webhook_filters_item = webhook_filters_item_data.to_dict()

                webhook_filters.append(webhook_filters_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if info is not UNSET:
            field_dict["info"] = info
        if url is not UNSET:
            field_dict["url"] = url
        if openapi_spec_format is not UNSET:
            field_dict["openapi_spec_format"] = openapi_spec_format
        if http_route_filters is not UNSET:
            field_dict["http_route_filters"] = http_route_filters
        if webhook_filters is not UNSET:
            field_dict["webhook_filters"] = webhook_filters

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.download_openapi_spec_json_body_http_route_filters_item import (
            DownloadOpenapiSpecJsonBodyHttpRouteFiltersItem,
        )
        from ..models.download_openapi_spec_json_body_info import DownloadOpenapiSpecJsonBodyInfo
        from ..models.download_openapi_spec_json_body_webhook_filters_item import (
            DownloadOpenapiSpecJsonBodyWebhookFiltersItem,
        )

        d = src_dict.copy()
        _info = d.pop("info", UNSET)
        info: Union[Unset, DownloadOpenapiSpecJsonBodyInfo]
        if isinstance(_info, Unset):
            info = UNSET
        else:
            info = DownloadOpenapiSpecJsonBodyInfo.from_dict(_info)

        url = d.pop("url", UNSET)

        _openapi_spec_format = d.pop("openapi_spec_format", UNSET)
        openapi_spec_format: Union[Unset, DownloadOpenapiSpecJsonBodyOpenapiSpecFormat]
        if isinstance(_openapi_spec_format, Unset):
            openapi_spec_format = UNSET
        else:
            openapi_spec_format = DownloadOpenapiSpecJsonBodyOpenapiSpecFormat(_openapi_spec_format)

        http_route_filters = []
        _http_route_filters = d.pop("http_route_filters", UNSET)
        for http_route_filters_item_data in _http_route_filters or []:
            http_route_filters_item = DownloadOpenapiSpecJsonBodyHttpRouteFiltersItem.from_dict(
                http_route_filters_item_data
            )

            http_route_filters.append(http_route_filters_item)

        webhook_filters = []
        _webhook_filters = d.pop("webhook_filters", UNSET)
        for webhook_filters_item_data in _webhook_filters or []:
            webhook_filters_item = DownloadOpenapiSpecJsonBodyWebhookFiltersItem.from_dict(webhook_filters_item_data)

            webhook_filters.append(webhook_filters_item)

        download_openapi_spec_json_body = cls(
            info=info,
            url=url,
            openapi_spec_format=openapi_spec_format,
            http_route_filters=http_route_filters,
            webhook_filters=webhook_filters,
        )

        download_openapi_spec_json_body.additional_properties = d
        return download_openapi_spec_json_body

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
