import base64

import pytest

from spark.connect.base_pb2 import AnalyzePlanRequest, ConfigRequest, ExecutePlanRequest, KeyValue, UserContext
from spark.connect.envelope_pb2 import ResponseEnvelope

from snowflake.core.spark_connect import SparkConnectResource


TEST_CONNECTIONS = ["connection_default", "pat_with_external_session_connection"]


def _block_for_result_if_necessary(resp_bytes: bytearray, connection):
    assert resp_bytes is not None
    response_envelope = ResponseEnvelope()
    response_envelope.ParseFromString(bytes(resp_bytes))
    if response_envelope.query_id:
        # query took long (> 45s) time and GS returned status URL with query id to pole
        cursor = connection.cursor()
        cursor.get_results_from_sfqid(response_envelope.query_id)
        # Block till the result is ready
        cursor._prefetch_hook()
        # Read the result back
        data = cursor._result_set.batches[0]._data
        resp_bytes = base64.b64decode(data)
        response_envelope = ResponseEnvelope()
        response_envelope.ParseFromString(resp_bytes)
    return response_envelope


@pytest.mark.flaky
@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
@pytest.mark.skip_gov
@pytest.mark.min_sf_ver("9.18.0")
@pytest.mark.parametrize("spark_connection", TEST_CONNECTIONS, indirect=True)
def test_execute_plan(spark_connection, external_session_id):
    exec_plan_request = ExecutePlanRequest(
        session_id=external_session_id,
        user_context=UserContext(user_id="test", user_name="ssa"),
        operation_id="test_grpc_over_rest",
        client_type="python API",
    )
    spark_connect_resource = SparkConnectResource(spark_connection)
    response = spark_connect_resource.execute_plan(exec_plan_request.SerializeToString())
    response_envelope = _block_for_result_if_necessary(response, spark_connection)
    assert response_envelope.WhichOneof("response_type") == "execute_plan_response"
    assert response_envelope.execute_plan_response.session_id == exec_plan_request.session_id
    assert response_envelope.execute_plan_response.result_complete is not None


@pytest.mark.flaky
@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
@pytest.mark.skip_gov
@pytest.mark.min_sf_ver("9.18.0")
@pytest.mark.parametrize("spark_connection", TEST_CONNECTIONS, indirect=True)
def test_analyze_plan(spark_connection, external_session_id):
    analyze_plan_request = AnalyzePlanRequest(
        session_id=external_session_id,
        user_context=UserContext(user_id="test", user_name="ssa"),
        spark_version=AnalyzePlanRequest.SparkVersion(),
        client_type="python API",
    )
    spark_connect_resource = SparkConnectResource(spark_connection)
    response = spark_connect_resource.analyze_plan(analyze_plan_request.SerializeToString())
    response_envelope = _block_for_result_if_necessary(response, spark_connection)
    assert response_envelope.WhichOneof("response_type") == "analyze_plan_response"
    assert response_envelope.analyze_plan_response.session_id == analyze_plan_request.session_id


@pytest.mark.flaky
@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
@pytest.mark.skip_gov
@pytest.mark.min_sf_ver("9.18.0")
@pytest.mark.parametrize("spark_connection", TEST_CONNECTIONS, indirect=True)
def test_config(spark_connection, external_session_id):
    config_request = ConfigRequest(
        session_id=external_session_id,
        user_context=UserContext(user_id="test", user_name="ssa"),
        client_type="python API",
        operation=ConfigRequest.Operation(set=ConfigRequest.Set(pairs=[KeyValue(key="foo", value="foo42")])),
    )
    spark_connect_resource = SparkConnectResource(spark_connection)
    response = spark_connect_resource.config(config_request.SerializeToString())
    response_envelope = _block_for_result_if_necessary(response, spark_connection)
    assert response_envelope.WhichOneof("response_type") == "config_response"
    assert response_envelope.config_response.session_id == config_request.session_id


@pytest.mark.flaky
@pytest.mark.skip_notebook
@pytest.mark.skip_storedproc
@pytest.mark.skip_gov
@pytest.mark.min_sf_ver("9.18.0")
def test_same_session_for_pat_with_ext_session_id(
    pat_with_external_session_connection, connection, external_session_id
):
    spark_connect_resource = SparkConnectResource(pat_with_external_session_connection)

    # Set config
    config_request = ConfigRequest(
        session_id=external_session_id,
        user_context=UserContext(user_id="test", user_name="ssa"),
        client_type="python API",
        operation=ConfigRequest.Operation(set=ConfigRequest.Set(pairs=[KeyValue(key="foo", value="foo42")])),
    )
    response = spark_connect_resource.config(config_request.SerializeToString())
    response_envelope = _block_for_result_if_necessary(response, connection)
    assert response_envelope.WhichOneof("response_type") == "config_response"
    assert response_envelope.config_response.session_id == config_request.session_id

    # Read the set config back
    config_request = ConfigRequest(
        session_id=external_session_id,
        user_context=UserContext(user_id="test", user_name="ssa"),
        client_type="python API",
        operation=ConfigRequest.Operation(get=ConfigRequest.Get(keys=["foo"])),
    )
    response = spark_connect_resource.config(config_request.SerializeToString())
    response_envelope = _block_for_result_if_necessary(response, connection)
    assert response_envelope.WhichOneof("response_type") == "config_response"
    assert response_envelope.config_response.session_id == config_request.session_id
    assert response_envelope.config_response.pairs is not None
    key_val = list(response_envelope.config_response.pairs)
    assert len(key_val) == 1
    assert key_val[0].key == "foo"
    assert key_val[0].value == "foo42"
