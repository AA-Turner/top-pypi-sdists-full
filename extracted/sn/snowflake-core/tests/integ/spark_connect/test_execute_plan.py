import pytest

from spark.connect.base_pb2 import (
    AnalyzePlanRequest,
    AnalyzePlanResponse,
    ConfigRequest,
    ConfigResponse,
    ExecutePlanRequest,
    UserContext,
)
from spark.connect.envelope_pb2 import ResponseEnvelope


def execute_plan_common(spark_connect_resource):
    exec_plan_request = ExecutePlanRequest(
        session_id="91234",
        user_context=UserContext(user_id="test", user_name="ssa"),
        operation_id="test_grpc_over_rest",
        client_type="python API"
    )
    response = spark_connect_resource.execute_plan(exec_plan_request.SerializeToString())
    assert response is not None
    response_envelope = ResponseEnvelope()
    response_envelope.ParseFromString(bytes(response))
    assert response_envelope.WhichOneof("response_type") == "execute_plan_response"
    assert response_envelope.execute_plan_response.session_id == exec_plan_request.session_id
    assert response_envelope.execute_plan_response.operation_id == exec_plan_request.operation_id
    assert response_envelope.execute_plan_response.result_complete is not None


@pytest.mark.flaky
@pytest.mark.min_sf_ver("9.6.0")
def test_execute_plan_using_session(spark_connect_session_resource):
    execute_plan_common(spark_connect_session_resource)


@pytest.mark.flaky
@pytest.mark.min_sf_ver("9.6.0")
def test_execute_plan_using_rest(spark_connect_rest_resource):
    execute_plan_common(spark_connect_rest_resource)


def analyze_plan_common(spark_connect_resource):
    analyze_plan_request = AnalyzePlanRequest(
        session_id="91234",
        user_context=UserContext(user_id="test", user_name="ssa"),
        client_type="python API"
    )
    response = spark_connect_resource.analyze_plan(analyze_plan_request.SerializeToString())
    assert response is not None
    analyze_plan_response = AnalyzePlanResponse()
    analyze_plan_response.ParseFromString(bytes(response))
    assert analyze_plan_response.session_id == analyze_plan_request.session_id


@pytest.mark.flaky
@pytest.mark.min_sf_ver("9.6.0")
def test_analyze_plan_using_session(spark_connect_session_resource):
    analyze_plan_common(spark_connect_session_resource)


@pytest.mark.flaky
@pytest.mark.min_sf_ver("9.6.0")
def test_analyze_plan_using_rest(spark_connect_rest_resource):
    analyze_plan_common(spark_connect_rest_resource)


def config_common(spark_connect_resource):
    config_request = ConfigRequest(
        session_id="91234",
        user_context=UserContext(user_id="test", user_name="ssa"),
        client_type="python API"
    )
    response = spark_connect_resource.config(config_request.SerializeToString())
    assert response is not None
    config_response = ConfigResponse()
    config_response.ParseFromString(bytes(response))


@pytest.mark.flaky
@pytest.mark.min_sf_ver("9.6.0")
def test_config_using_session(spark_connect_session_resource):
    config_common(spark_connect_session_resource)


@pytest.mark.flaky
@pytest.mark.min_sf_ver("9.6.0")
def test_config_using_rest(spark_connect_rest_resource):
    config_common(spark_connect_rest_resource)
