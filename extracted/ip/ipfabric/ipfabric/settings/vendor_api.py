import logging
from typing import Any, ClassVar, Union, Optional, List

from pydantic import Field, BaseModel, model_serializer

from ipfabric.models.vendor_api import VENDOR_API, VendorAPIModel, TYPE_TO_MODEL
from ipfabric.tools.shared import raise_for_status


CONNECTION_PARAMS = [
    "rejectUnauthorized",
    "respectSystemProxyConfiguration",
    "maxConcurrentRequests",
    "maxCapacity",
    "refillRate",
    "refillRateIntervalMs",
]

logger = logging.getLogger("ipfabric")


class VendorAPI(BaseModel):
    client: Any = Field(exclude=True)
    snapshot_id: Optional[str] = None
    vendor_api: Optional[List[VENDOR_API]] = None
    _api_url: ClassVar[str] = "settings/vendor-api"

    def model_post_init(self, context: Any, /) -> None:
        if not self.vendor_api:
            self.vendor_api = self.get_vendor_apis()

    @model_serializer
    def _ser_model(self) -> list[dict[str, Any]]:
        return [_.model_dump(by_alias=True) for _ in self.vendor_api]

    @property
    def _settings_url(self) -> str:
        return f"settings/{self.snapshot_id}" if self.snapshot_id else "settings"

    def get_vendor_apis(self) -> List[VENDOR_API]:
        """
        Get all vendor apis and sets them in the Authentication.apis
        :return: self.credentials
        """
        return [
            VendorAPIModel(**_).root for _ in raise_for_status(self.client.get(self._settings_url)).json()["vendorApi"]
        ]

    def add_vendor_api(self, api: VENDOR_API) -> VENDOR_API:
        return VendorAPIModel(
            **raise_for_status(self.client.post(self._api_url, json=api.model_dump(by_alias=True))).json()
        ).root

    @staticmethod
    def _return_api_id(api_id: Union[dict, str, int, VENDOR_API]) -> str:
        if isinstance(api_id, dict):
            api_id = api_id["id"]
        elif isinstance(api_id, (str, int)):
            api_id = str(api_id)
        else:
            api_id = api_id.vendor_id
        return api_id

    def delete_vendor_api(self, api_id: Union[dict, str, int, VENDOR_API]) -> int:
        return raise_for_status(self.client.delete(self._api_url + "/" + self._return_api_id(api_id))).status_code

    def enable_vendor_api(self, api_id: Union[dict, str, int, VENDOR_API]) -> int:
        return raise_for_status(
            self.client.patch(self._api_url + "/" + self._return_api_id(api_id), json={"isEnabled": True})
        ).status_code

    def disable_vendor_api(self, api_id: Union[dict, str, int, VENDOR_API]) -> int:
        return raise_for_status(
            self.client.patch(self._api_url + "/" + self._return_api_id(api_id), json={"isEnabled": False})
        ).status_code

    def verify_connection(self, api: VENDOR_API) -> int:
        return raise_for_status(
            self.client.post(
                (
                    "/settings/vendor-api/verify-connection/reverify"
                    if api.vendor_id
                    else "/settings/vendor-api/verify-connection"
                ),
                json=self.model_dump(by_alias=True),
            )
        ).status_code

    def update_vendor_api(  # TODO: NIM-19186 FIX ME
        self,
        current: Union[VENDOR_API, dict],
        update: Union[VENDOR_API, dict],
        restore_conn_defaults: bool = False,
    ) -> VENDOR_API:
        current = (VendorAPIModel(**current) if isinstance(current, dict) else current).model_dump(by_alias=True)

        if not isinstance(update, dict):
            update = update.model_dump(by_alias=True)
        update.pop("id", None)

        new = {**current, **update}
        if restore_conn_defaults:
            default = {
                k: v
                for k, v in vars(TYPE_TO_MODEL[current["type"]].model_construct()).items()
                if k in CONNECTION_PARAMS
            }
            new.update(default)
        params = {
            "vendorApi": [
                _.model_dump(by_alias=True) if _.vendor_id != current["id"] else new for _ in self.get_vendor_apis()
            ]
        }

        return VendorAPIModel(
            **raise_for_status(self.client.patch(self._settings_url, json=params)).json()["vendorApi"]
        ).root
