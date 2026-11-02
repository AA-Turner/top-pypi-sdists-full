from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.test_http_store_backend_json_body_settings import TestHttpStoreBackendJsonBodySettings


T = TypeVar("T", bound="TestHttpStoreBackendJsonBody")


@_attrs_define
class TestHttpStoreBackendJsonBody:
    """
    Attributes:
        settings (TestHttpStoreBackendJsonBodySettings): Read-only secret backend for any secret store with an HTTP API.
            A secret variable saved with an empty value references the store key derived from its workspace and path.
        workspace_id (str): workspace of a variable whose secret exists in the store
        path (str): path of a variable whose secret exists in the store
    """

    settings: "TestHttpStoreBackendJsonBodySettings"
    workspace_id: str
    path: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        settings = self.settings.to_dict()

        workspace_id = self.workspace_id
        path = self.path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "settings": settings,
                "workspace_id": workspace_id,
                "path": path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_http_store_backend_json_body_settings import TestHttpStoreBackendJsonBodySettings

        d = src_dict.copy()
        settings = TestHttpStoreBackendJsonBodySettings.from_dict(d.pop("settings"))

        workspace_id = d.pop("workspace_id")

        path = d.pop("path")

        test_http_store_backend_json_body = cls(
            settings=settings,
            workspace_id=workspace_id,
            path=path,
        )

        test_http_store_backend_json_body.additional_properties = d
        return test_http_store_backend_json_body

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
