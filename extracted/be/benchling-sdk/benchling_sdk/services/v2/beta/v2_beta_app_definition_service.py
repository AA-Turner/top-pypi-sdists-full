from benchling_api_client.v2.beta.api.app_definitions import (
    get_benchling_app_definition_version_manifest,
    put_benchling_app_definition_version_manifest,
)
from benchling_api_client.v2.beta.models.benchling_app_manifest import BenchlingAppManifest

from benchling_sdk.helpers.decorators import api_method
from benchling_sdk.helpers.response_helpers import model_from_detailed
from benchling_sdk.services.v2.base_service import BaseService


class V2BetaAppDefinitionService(BaseService):
    """
    V2-Beta App Definitions.

    Create and manage Benchling app definitions on your tenant.

    https://benchling.com/api/v2-beta/reference#/App%20Definitions
    """

    @api_method
    def get_version_manifest(self, app_def_id: str, version_id: str) -> BenchlingAppManifest:
        """
        Get manifest for an app definition version.

        See https://benchling.com/api/v2-beta/reference#/App%20Definitions/getBenchlingAppDefinitionVersionManifest
        """
        response = get_benchling_app_definition_version_manifest.sync_detailed(
            client=self.client, app_def_id=app_def_id, version_id=version_id
        )
        return model_from_detailed(response)

    @api_method
    def put_version_manifest(
        self, app_def_id: str, version_id: str, manifest: BenchlingAppManifest
    ) -> BenchlingAppManifest:
        """
        Create or update app definition version from a manifest.

        See https://benchling.com/api/v2-beta/reference#/App%20Definitions/putBenchlingAppDefinitionVersionManifest
        """
        response = put_benchling_app_definition_version_manifest.sync_detailed(
            client=self.client, app_def_id=app_def_id, version_id=version_id, yaml_body=manifest
        )
        return model_from_detailed(response)
