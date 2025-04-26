# Copyright 2022 StreamSets Inc.

# fmt: off
import pytest

from streamsets.sdk.sch_models import ConnectionVerificationResult

# fmt: on


def test_verify_invalid_connection(sch, invalid_jdbc_test_connection):
    verification = sch.verify_connection(invalid_jdbc_test_connection)
    assert verification.status == 'INVALID'


def test_connection_restriction_for_s3_stage(
    sch, sch_authoring_sdc_id, invalid_jdbc_test_connection, invalid_aws_test_connection
):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    origin = pipeline_builder.add_stage('Dev Data Generator')
    destination = pipeline_builder.add_stage('Amazon S3', type='destination')
    origin >> destination
    with pytest.raises(ValueError):
        destination.use_connection(invalid_jdbc_test_connection)
    assert destination.connection == 'MANUAL'
    destination.use_connection(invalid_aws_test_connection)
    assert destination.connection == invalid_aws_test_connection.id


def test_connection_restriction_for_jdbc_stage(
    sch, sch_authoring_sdc_id, invalid_jdbc_test_connection, invalid_aws_test_connection
):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    origin = pipeline_builder.add_stage('Dev Data Generator')
    destination = pipeline_builder.add_stage('JDBC Producer')
    origin >> destination
    with pytest.raises(ValueError):
        destination.use_connection(invalid_aws_test_connection)
    assert destination.connection == 'MANUAL'
    destination.use_connection(invalid_jdbc_test_connection)
    assert destination.connection == invalid_jdbc_test_connection.id


def test_snowflake_connection(sch, sch_authoring_sdc_id, invalid_snowflake_test_connection):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    snowflake_destination = pipeline_builder.add_stage('Snowflake', type='destination')

    assert snowflake_destination.connection == 'MANUAL'
    snowflake_destination.use_connection(invalid_snowflake_test_connection)
    assert snowflake_destination.connection == invalid_snowflake_test_connection.id


def test_engineless_connection_restriction_for_s3_stage(
    sch, sch_authoring_sdc_id, invalid_jdbc_engineless_test_connection, invalid_aws_engineless_test_connection
):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    origin = pipeline_builder.add_stage('Dev Data Generator')
    destination = pipeline_builder.add_stage('Amazon S3', type='destination')
    origin >> destination
    with pytest.raises(ValueError):
        destination.use_connection(invalid_jdbc_engineless_test_connection)
    assert destination.connection == 'MANUAL'
    destination.use_connection(invalid_aws_engineless_test_connection)
    assert destination.connection == invalid_aws_engineless_test_connection.id


def test_engineless_connection_restriction_for_jdbc_stage(
    sch, sch_authoring_sdc_id, invalid_jdbc_engineless_test_connection, invalid_aws_engineless_test_connection
):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    origin = pipeline_builder.add_stage('Dev Data Generator')
    destination = pipeline_builder.add_stage('JDBC Producer')
    origin >> destination
    with pytest.raises(ValueError):
        destination.use_connection(invalid_aws_engineless_test_connection)
    assert destination.connection == 'MANUAL'
    destination.use_connection(invalid_jdbc_engineless_test_connection)
    assert destination.connection == invalid_jdbc_engineless_test_connection.id


def test_engineless_snowflake_connection(sch, sch_authoring_sdc_id, invalid_snowflake_engineless_test_connection):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    snowflake_destination = pipeline_builder.add_stage('Snowflake', type='destination')

    assert snowflake_destination.connection == 'MANUAL'
    snowflake_destination.use_connection(invalid_snowflake_engineless_test_connection)
    assert snowflake_destination.connection == invalid_snowflake_engineless_test_connection.id


@pytest.mark.parametrize('unsupported_test_connection', ['invalid_jdbc_test_connection', 'invalid_aws_test_connection'])
def test_connection_restriction_for_snowflake_stage(sch, sch_authoring_sdc_id, unsupported_test_connection, request):
    pipeline_builder = sch.get_pipeline_builder(engine_type='data_collector', engine_id=sch_authoring_sdc_id)
    snowflake_destination = pipeline_builder.add_stage('Snowflake', type='destination')
    unsupported_test_connection = request.getfixturevalue(unsupported_test_connection)

    with pytest.raises(ValueError):
        snowflake_destination.use_connection(unsupported_test_connection)


@pytest.mark.parametrize(
    "library_to_check_against, use_sdc_snowflake_library",
    [(None, False), (None, True), ('jdbc', False)],  # no params  # snowflake library  # check against jdbc library
)
def test_verify_connection(
    sch, invalid_jdbc_test_connection, library_to_check_against, sdc_snowflake_library, use_sdc_snowflake_library
):
    if use_sdc_snowflake_library:
        # since we pass the version of the snowflake library we should remove the version from it
        library = sdc_snowflake_library.split(':')[0]
    else:
        library = library_to_check_against

    connection_verification_result = sch.verify_connection(
        connection=invalid_jdbc_test_connection,
        library=library,
    )

    assert isinstance(connection_verification_result, ConnectionVerificationResult)
