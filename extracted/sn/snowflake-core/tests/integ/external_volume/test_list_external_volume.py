import pytest

from snowflake.core._internal.utils import normalize_and_unquote_name
from tests.integ.external_volume.utils import (
    get_aws_external_volume_template,
    get_aws_external_volume_template_case_sensitive,
    get_azure_external_volume_template,
    get_gcs_external_volume_template,
)


pytestmark = [pytest.mark.internal_only]


def test_list_external_volume(external_volumes, setup_credentials_fixture):
    try:
        external_volume_to_drop = []
        # happy path aws
        external_volume = get_aws_external_volume_template()
        external_volume_handler = external_volumes.create(external_volume)
        external_volume_to_drop += [external_volume_handler]

        external_volume_resources_name = [
            external_volume_resource_temp.name
            for external_volume_resource_temp in external_volumes.iter(like="test_create_aws_external_volume_%")
        ]
        assert external_volume.name.upper() in external_volume_resources_name

        # happy path aws case sensitive
        external_volume = get_aws_external_volume_template_case_sensitive()
        external_volume_handler = external_volumes.create(external_volume)
        external_volume_to_drop += [external_volume_handler]

        external_volume_resources_name = [
            external_volume_resource_temp.name
            for external_volume_resource_temp in external_volumes.iter(like="test_create_aws_external_volume_%")
        ]
        assert normalize_and_unquote_name(external_volume.name) in external_volume_resources_name
        assert len(external_volume_resources_name) >= 2

        # happy path azure
        external_volume = get_azure_external_volume_template()
        external_volume_handler = external_volumes.create(external_volume)
        external_volume_to_drop += [external_volume_handler]

        external_volume_resources_name = [
            external_volume_resource_temp.name
            for external_volume_resource_temp in external_volumes.iter(like="test_create_azure_external_volume_%")
        ]
        assert external_volume.name.upper() in external_volume_resources_name

        # happy path gcs
        external_volume = get_gcs_external_volume_template()
        external_volume_handler = external_volumes.create(external_volume)
        external_volume_to_drop += [external_volume_handler]

        external_volume_resources_name = [
            external_volume_resource_temp.name
            for external_volume_resource_temp in external_volumes.iter(like="test_create_gcs_external_volume_%")
        ]
        assert external_volume.name.upper() in external_volume_resources_name

        # trying to get random volume
        external_volume_resources_name = [
            external_volume_resource_temp.name for external_volume_resource_temp in external_volumes.iter(like="RANDOM")
        ]
        assert len(external_volume_resources_name) == 0

    finally:
        for external_volume_handler in external_volume_to_drop:
            external_volume_handler.drop(if_exists=True)
