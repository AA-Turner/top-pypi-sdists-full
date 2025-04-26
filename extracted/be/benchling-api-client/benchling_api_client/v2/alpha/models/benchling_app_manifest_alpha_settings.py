from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.benchling_app_manifest_alpha_settings_lifecycle_management import (
    BenchlingAppManifestAlphaSettingsLifecycleManagement,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="BenchlingAppManifestAlphaSettings")


@attr.s(auto_attribs=True, repr=False)
class BenchlingAppManifestAlphaSettings:
    """  """

    _canvas_webhook_url: Union[Unset, str] = UNSET
    _lifecycle_management: Union[Unset, BenchlingAppManifestAlphaSettingsLifecycleManagement] = UNSET
    _lifecycle_webhook_url: Union[Unset, str] = UNSET
    _webhook_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("canvas_webhook_url={}".format(repr(self._canvas_webhook_url)))
        fields.append("lifecycle_management={}".format(repr(self._lifecycle_management)))
        fields.append("lifecycle_webhook_url={}".format(repr(self._lifecycle_webhook_url)))
        fields.append("webhook_url={}".format(repr(self._webhook_url)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "BenchlingAppManifestAlphaSettings({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        canvas_webhook_url = self._canvas_webhook_url
        lifecycle_management: Union[Unset, int] = UNSET
        if not isinstance(self._lifecycle_management, Unset):
            lifecycle_management = self._lifecycle_management.value

        lifecycle_webhook_url = self._lifecycle_webhook_url
        webhook_url = self._webhook_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if canvas_webhook_url is not UNSET:
            field_dict["canvasWebhookUrl"] = canvas_webhook_url
        if lifecycle_management is not UNSET:
            field_dict["lifecycleManagement"] = lifecycle_management
        if lifecycle_webhook_url is not UNSET:
            field_dict["lifecycleWebhookUrl"] = lifecycle_webhook_url
        if webhook_url is not UNSET:
            field_dict["webhookUrl"] = webhook_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_canvas_webhook_url() -> Union[Unset, str]:
            canvas_webhook_url = d.pop("canvasWebhookUrl")
            return canvas_webhook_url

        try:
            canvas_webhook_url = get_canvas_webhook_url()
        except KeyError:
            if strict:
                raise
            canvas_webhook_url = cast(Union[Unset, str], UNSET)

        def get_lifecycle_management() -> Union[Unset, BenchlingAppManifestAlphaSettingsLifecycleManagement]:
            lifecycle_management = UNSET
            _lifecycle_management = d.pop("lifecycleManagement")
            if _lifecycle_management is not None and _lifecycle_management is not UNSET:
                try:
                    lifecycle_management = BenchlingAppManifestAlphaSettingsLifecycleManagement(
                        _lifecycle_management
                    )
                except ValueError:
                    lifecycle_management = BenchlingAppManifestAlphaSettingsLifecycleManagement.of_unknown(
                        _lifecycle_management
                    )

            return lifecycle_management

        try:
            lifecycle_management = get_lifecycle_management()
        except KeyError:
            if strict:
                raise
            lifecycle_management = cast(
                Union[Unset, BenchlingAppManifestAlphaSettingsLifecycleManagement], UNSET
            )

        def get_lifecycle_webhook_url() -> Union[Unset, str]:
            lifecycle_webhook_url = d.pop("lifecycleWebhookUrl")
            return lifecycle_webhook_url

        try:
            lifecycle_webhook_url = get_lifecycle_webhook_url()
        except KeyError:
            if strict:
                raise
            lifecycle_webhook_url = cast(Union[Unset, str], UNSET)

        def get_webhook_url() -> Union[Unset, str]:
            webhook_url = d.pop("webhookUrl")
            return webhook_url

        try:
            webhook_url = get_webhook_url()
        except KeyError:
            if strict:
                raise
            webhook_url = cast(Union[Unset, str], UNSET)

        benchling_app_manifest_alpha_settings = cls(
            canvas_webhook_url=canvas_webhook_url,
            lifecycle_management=lifecycle_management,
            lifecycle_webhook_url=lifecycle_webhook_url,
            webhook_url=webhook_url,
        )

        benchling_app_manifest_alpha_settings.additional_properties = d
        return benchling_app_manifest_alpha_settings

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
    def canvas_webhook_url(self) -> str:
        """URL that Benchling sends app canvas payloads to. It will override the default webhookUrl This destination should be backed by an endpoint owned by your application."""
        if isinstance(self._canvas_webhook_url, Unset):
            raise NotPresentError(self, "canvas_webhook_url")
        return self._canvas_webhook_url

    @canvas_webhook_url.setter
    def canvas_webhook_url(self, value: str) -> None:
        self._canvas_webhook_url = value

    @canvas_webhook_url.deleter
    def canvas_webhook_url(self) -> None:
        self._canvas_webhook_url = UNSET

    @property
    def lifecycle_management(self) -> BenchlingAppManifestAlphaSettingsLifecycleManagement:
        """Specify whether app will be activated automatically or manually. If automatic is specified, a webhook url is required."""
        if isinstance(self._lifecycle_management, Unset):
            raise NotPresentError(self, "lifecycle_management")
        return self._lifecycle_management

    @lifecycle_management.setter
    def lifecycle_management(self, value: BenchlingAppManifestAlphaSettingsLifecycleManagement) -> None:
        self._lifecycle_management = value

    @lifecycle_management.deleter
    def lifecycle_management(self) -> None:
        self._lifecycle_management = UNSET

    @property
    def lifecycle_webhook_url(self) -> str:
        """URL that Benchling sends app lifecycle payloads to. It will override the default webhookUrl This destination should be backed by an endpoint owned by your application."""
        if isinstance(self._lifecycle_webhook_url, Unset):
            raise NotPresentError(self, "lifecycle_webhook_url")
        return self._lifecycle_webhook_url

    @lifecycle_webhook_url.setter
    def lifecycle_webhook_url(self, value: str) -> None:
        self._lifecycle_webhook_url = value

    @lifecycle_webhook_url.deleter
    def lifecycle_webhook_url(self) -> None:
        self._lifecycle_webhook_url = UNSET

    @property
    def webhook_url(self) -> str:
        """URL that Benchling sends app interaction payloads to. This is the default URL if no other webhook URLs are specified in the app's manifest. This destination should be backed by an endpoint owned by your application."""
        if isinstance(self._webhook_url, Unset):
            raise NotPresentError(self, "webhook_url")
        return self._webhook_url

    @webhook_url.setter
    def webhook_url(self, value: str) -> None:
        self._webhook_url = value

    @webhook_url.deleter
    def webhook_url(self) -> None:
        self._webhook_url = UNSET
