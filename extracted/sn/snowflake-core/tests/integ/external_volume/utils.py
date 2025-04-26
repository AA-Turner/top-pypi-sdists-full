from snowflake.core.external_volume import (
    Encryption,
    ExternalVolume,
    StorageLocationAzure,
    StorageLocationGcs,
    StorageLocationS3,
)
from tests.utils import random_string


def get_aws_external_volume_template():
    return ExternalVolume(
        name=random_string(5, "test_create_aws_external_volume_"),
        storage_locations=[
            StorageLocationS3(
                name="abcd-my-s3-us-west-2",
                storage_base_url="s3://MY_EXAMPLE_BUCKET/",
                storage_aws_role_arn="arn:aws:iam::123456789022:role/myrole",
                encryption=Encryption(type="AWS_SSE_KMS", kms_key_id="1234abcd-12ab-34cd-56ef-1234567890ab"),
            ),
            StorageLocationS3(
                name="abcd-my-s3-us-west-3",
                storage_base_url="s3://MY_EXAMPLE_BUCKET_1/",
                storage_aws_role_arn="arn:aws:iam::123456789022:role/myrole",
                encryption=Encryption(type="AWS_SSE_KMS", kms_key_id="1234abcd-12ab-34cd-56ef-1234567890ab"),
            ),
        ],
        comment="SNOWAPI_TEST_EXTERNAL_VOLUME",
    )


def get_aws_external_volume_template_case_sensitive():
    return ExternalVolume(
        name='"' + random_string(5, "test_create_aws_external_volume_") + '"',
        storage_locations=[
            StorageLocationS3(
                name="abcd-my-s3-us-west-2",
                storage_base_url="s3://MY_EXAMPLE_BUCKET/",
                storage_aws_role_arn="arn:aws:iam::123456789022:role/myrole",
                encryption=Encryption(type="AWS_SSE_KMS", kms_key_id="1234abcd-12ab-34cd-56ef-1234567890ab"),
            )
        ],
        comment="SNOWAPI_TEST_EXTERNAL_VOLUME",
    )


def get_azure_external_volume_template():
    return ExternalVolume(
        name=random_string(5, "test_create_azure_external_volume_"),
        storage_locations=[
            StorageLocationAzure(
                name="abcd-my-azure-northeurope",
                storage_base_url="azure://exampleacct.blob.core.windows.net/my_container_northeurope/",
                azure_tenant_id="a123b4c5-1234-123a-a12b-1a23b45678c9",
            )
        ],
        comment="SNOWAPI_TEST_EXTERNAL_VOLUME",
    )


def get_gcs_external_volume_template():
    return ExternalVolume(
        name=random_string(5, "test_create_gcs_external_volume_"),
        storage_locations=[
            StorageLocationGcs(
                name="abcd-my-us-east-1",
                storage_base_url="gcs://mybucket1/path1/",
                encryption=Encryption(type="GCS_SSE_KMS", kms_key_id="1234abcd-12ab-34cd-56ef-1234567890ab"),
            )
        ],
        comment="SNOWAPI_TEST_EXTERNAL_VOLUME",
    )


def assert_basic(external_volume_object, external_volume_expected):
    assert external_volume_object.comment == external_volume_expected.comment
    assert external_volume_object.allow_writes
    assert external_volume_object.created_on is not None
    assert external_volume_object.owner is not None
