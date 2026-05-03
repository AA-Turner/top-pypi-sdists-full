import biolib.api
from biolib._data_record.data_record import DataRecord
from biolib._shared.types import ResourceDetailedDict
from biolib.api.client import ApiClient
from biolib.biolib_api_client.app_types import AppVersion
from biolib.typing_utils import Optional


class AppVersionSdk:
    def __init__(self, app_version: AppVersion, _api_client: Optional[ApiClient] = None) -> None:
        self._app_version = app_version
        self._api_client = _api_client or biolib.api.client

    def get_assets(self) -> DataRecord:
        resource_dict: ResourceDetailedDict = self._api_client.get(
            path='/resource/',
            params={'uri': self._app_version['app_uri']},
        ).json()
        return DataRecord(_internal_state=resource_dict)

    def set_as_published(self, published: bool = True) -> None:
        app_version_uuid = self._app_version['public_id']
        self._api_client.patch(
            path=f'/app_versions/{app_version_uuid}/',
            data={'set_as_published': published},
        )

    def set_as_default(self) -> None:
        app_version_uuid = self._app_version['public_id']
        self._api_client.patch(
            path=f'/app_versions/{app_version_uuid}/',
            data={'set_as_active': True},
        )
