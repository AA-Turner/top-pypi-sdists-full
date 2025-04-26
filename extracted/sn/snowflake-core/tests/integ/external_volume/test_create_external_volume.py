import pytest

from snowflake.core._internal.utils import normalize_and_unquote_name
from snowflake.core.exceptions import ConflictError
from tests.integ.external_volume.utils import (
    get_aws_external_volume_template,
    get_aws_external_volume_template_case_sensitive,
    get_azure_external_volume_template,
    get_gcs_external_volume_template,
)


pytestmark = [pytest.mark.internal_only]


def test_create_external_volume(external_volumes, setup_credentials_fixture):
    try:
        external_volume_to_drop = []
        # happy path aws
        external_volume = get_aws_external_volume_template()
        external_volume_handler = external_volumes.create(external_volume)
        external_volume_to_drop += [external_volume_handler]
        external_volume_object = external_volume_handler.fetch()
        assert external_volume_object.name == external_volume.name.upper()

        # happy path aws case sensitive
        external_volume = get_aws_external_volume_template_case_sensitive()
        external_volume_handler = external_volumes.create(external_volume)
        external_volume_to_drop += [external_volume_handler]
        external_volume_object = external_volume_handler.fetch()
        assert external_volume_object.name == normalize_and_unquote_name(external_volume.name)
        assert external_volume_object.comment == external_volume.comment

        # already existing external volume
        with pytest.raises(ConflictError):
            external_volumes.create(external_volume)

        # already existing external volume with if_exists
        external_volume_handler = external_volumes.create(external_volume, mode="if_not_exists")

        # using or replace
        external_volume.comment = "SNOWAPI_TEST_EXTERNAL_VOLUME_2"
        external_volume_handler = external_volumes.create(external_volume, mode="or_replace")
        external_volume_object = external_volume_handler.fetch()
        assert external_volume_object.comment == external_volume.comment

        # happy path azure
        external_volume = get_azure_external_volume_template()
        external_volume_handler = external_volumes.create(external_volume)
        external_volume_to_drop += [external_volume_handler]
        external_volume_object = external_volume_handler.fetch()
        assert external_volume_object.name == external_volume.name.upper()

        # happy path gcs
        external_volume = get_gcs_external_volume_template()
        external_volume_handler = external_volumes.create(external_volume)
        external_volume_to_drop += [external_volume_handler]
        external_volume_object = external_volume_handler.fetch()
        assert external_volume_object.name == external_volume.name.upper()

    finally:
        for external_volume_handler in external_volume_to_drop:
            external_volume_handler.drop(if_exists=True)
