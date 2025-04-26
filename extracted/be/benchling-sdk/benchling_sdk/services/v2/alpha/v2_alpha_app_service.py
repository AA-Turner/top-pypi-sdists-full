from benchling_api_client.v2.alpha.api.apps import get_benchling_app_manifest, put_benchling_app_manifest
from benchling_api_client.v2.alpha.models.benchling_app_manifest_alpha import BenchlingAppManifestAlpha

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.services.v2.base_service import BaseService


class V2AlphaAppService(BaseService):
    """
    V2-Alpha Apps.

    Create and manage Apps on your tenant.

    https://benchling.com/api/v2-alpha/reference?stability=not-available#/Apps
    """

    @api_method
    def get_manifest(self, app_id: str) -> BenchlingAppManifestAlpha:
        """
        Get app manifest.

        See https://benchling.com/api/v2-alpha/reference?stability=la/Apps/getBenchlingAppManifest
        """
        response = get_benchling_app_manifest.sync_detailed(client=self.client, app_id=app_id)
        return model_from_detailed(response)

    @api_method
    def update_manifest(self, app_id: str, manifest: BenchlingAppManifestAlpha) -> BenchlingAppManifestAlpha:
        """
        Update an app manifest.

        See https://benchling.com/api/v2-alpha/reference?stability=la#/Apps/putBenchlingAppManifest
        """
        response = put_benchling_app_manifest.sync_detailed(
            client=self.client, app_id=app_id, yaml_body=manifest
        )
        return model_from_detailed(response)
