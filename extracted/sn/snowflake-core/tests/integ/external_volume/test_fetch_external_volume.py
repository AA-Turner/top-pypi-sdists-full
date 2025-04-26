import pytest

from snowflake.core._internal.utils import normalize_and_unquote_name
from tests.integ.external_volume.utils import (
    assert_basic,
    get_aws_external_volume_template,
    get_aws_external_volume_template_case_sensitive,
    get_azure_external_volume_template,
    get_gcs_external_volume_template,
)


pytestmark = [pytest.mark.internal_only]


def test_fetch_external_volume(external_volumes, setup_credentials_fixture):
    try:
        external_volume_to_drop = []
        # happy path aws
        external_volume = get_aws_external_volume_template()
        external_volume_handler = external_volumes.create(external_volume)
        external_volume_to_drop += [external_volume_handler]
        external_volume_object = external_volume_handler.fetch()
        assert_basic(external_volume_object, external_volume)
        assert external_volume_object.name == external_volume.name.upper()
        assert external_volume_object.comment == external_volume.comment
        assert len(external_volume_object.storage_locations) == 2
        assert external_volume_object.storage_locations[0].name == "abcd-my-s3-us-west-2"
        assert external_volume_object.storage_locations[0].storage_base_url == "s3://MY_EXAMPLE_BUCKET/"
        assert (
            external_volume_object.storage_locations[0].storage_aws_role_arn == "arn:aws:iam::123456789022:role/myrole"
        )
        assert external_volume_object.storage_locations[0].encryption.type == "AWS_SSE_KMS"
        assert (
            external_volume_object.storage_locations[0].encryption.kms_key_id == "1234abcd-12ab-34cd-56ef-1234567890ab"
        )
        assert external_volume_object.storage_locations[1].name == "abcd-my-s3-us-west-3"
        assert external_volume_object.storage_locations[1].storage_base_url == "s3://MY_EXAMPLE_BUCKET_1/"
        assert (
            external_volume_object.storage_locations[1].storage_aws_role_arn == "arn:aws:iam::123456789022:role/myrole"
        )
        assert external_volume_object.storage_locations[1].encryption.type == "AWS_SSE_KMS"
        assert (
            external_volume_object.storage_locations[1].encryption.kms_key_id == "1234abcd-12ab-34cd-56ef-1234567890ab"
        )

        # happy path aws case sensitive
        external_volume = get_aws_external_volume_template_case_sensitive()
        external_volume_handler = external_volumes.create(external_volume)
        external_volume_to_drop += [external_volume_handler]
        external_volume_object = external_volume_handler.fetch()
        assert external_volume_object.name == normalize_and_unquote_name(external_volume.name)
        assert external_volume_object.comment == external_volume.comment

        # happy path azure
        external_volume = get_azure_external_volume_template()
        external_volume_handler = external_volumes.create(external_volume)
        external_volume_to_drop += [external_volume_handler]
        external_volume_object = external_volume_handler.fetch()
        assert external_volume_object.name == external_volume.name.upper()
        assert_basic(external_volume_object, external_volume)
        assert len(external_volume_object.storage_locations) == 1
        assert external_volume_object.storage_locations[0].name == "abcd-my-azure-northeurope"
        assert (
            external_volume_object.storage_locations[0].storage_base_url
            == "azure://exampleacct.blob.core.windows.net/my_container_northeurope/"
        )
        assert external_volume_object.storage_locations[0].azure_tenant_id == "a123b4c5-1234-123a-a12b-1a23b45678c9"

        # happy path gcs
        external_volume = get_gcs_external_volume_template()
        external_volume_handler = external_volumes.create(external_volume)
        external_volume_to_drop += [external_volume_handler]
        external_volume_object = external_volume_handler.fetch()
        assert external_volume_object.name == external_volume.name.upper()
        assert_basic(external_volume_object, external_volume)
        assert len(external_volume_object.storage_locations) == 1
        assert external_volume_object.storage_locations[0].name == "abcd-my-us-east-1"
        assert external_volume_object.storage_locations[0].storage_base_url == "gcs://mybucket1/path1/"
        assert external_volume_object.storage_locations[0].encryption.type == "GCS_SSE_KMS"
        assert (
            external_volume_object.storage_locations[0].encryption.kms_key_id == "1234abcd-12ab-34cd-56ef-1234567890ab"
        )

    finally:
        for external_volume_handler in external_volume_to_drop:
            external_volume_handler.drop(if_exists=True)
