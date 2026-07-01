import os
from typing import Union

import pyspark.sql.connect.proto.base_pb2 as proto

import snowflake.snowpark_connect.tcm as tcm
from snowflake.snowpark import Session
from snowflake.snowpark_connect.error.error_utils import build_grpc_error_response
from snowflake.snowpark_connect.execute_plan.map_execution_root import QueryResult
from snowflake.snowpark_connect.server import SnowflakeConnectServicer, start_session
from spark.connect.envelope_pb2 import DataframeQueryResult, ResponseEnvelope


class SparkDecoder:
    """
    Spark Decoder is the main snowflake server entry point that accepts spark connect requests.
    """

    REQUEST_TYPES = [
        proto.ExecutePlanRequest,
        proto.ConfigRequest,
        proto.AnalyzePlanRequest,
    ]

    def __init__(self, session: Session) -> None:
        self.session = session
        # set SPARK_LOCAL_HOSTNAME to avoid network lookup in sandbox
        os.environ["SPARK_LOCAL_HOSTNAME"] = "127.0.0.1"
        tcm.TCM_MODE = True
        start_session(is_daemon=False, snowpark_session=self.session)
        self.servicer = SnowflakeConnectServicer()

    def request(
        self,
        request: Union[
            proto.ExecutePlanRequest, proto.AnalyzePlanRequest, proto.ConfigRequest
        ],
    ) -> ResponseEnvelope:
        try:
            ctx = Context()
            match request:
                case proto.ExecutePlanRequest():
                    res = self.servicer.ExecutePlan(request, ctx)
                    result = next(res)
                    if isinstance(result, QueryResult):
                        return ResponseEnvelope(
                            dataframe_query_result=DataframeQueryResult(
                                result_job_uuid=result.query_id,
                                arrow_schema=result.arrow_schema,
                                spark_schema=result.spark_schema,
                            )
                        )
                    else:
                        return ResponseEnvelope(execute_plan_response=result)
                case proto.AnalyzePlanRequest():
                    return ResponseEnvelope(
                        analyze_plan_response=self.servicer.AnalyzePlan(request, ctx)
                    )
                case proto.ConfigRequest():
                    return ResponseEnvelope(
                        config_response=self.servicer.Config(request, ctx)
                    )
                case proto.AddArtifactsRequest():
                    return ResponseEnvelope(
                        add_artifacts_response=self.servicer.AddArtifacts(
                            iter([request]), ctx
                        )
                    )
                case proto.ArtifactStatusesRequest():
                    return ResponseEnvelope(
                        artifact_status_response=self.servicer.ArtifactStatus(
                            request, ctx
                        )
                    )
                case _:
                    raise NotImplementedError(
                        "Unknown request type: %s" % type(request)
                    )
        except Exception as e:
            return ResponseEnvelope(status=build_grpc_error_response(e))


class Context:
    def __init__(self) -> None:
        pass

    def abort_with_status(self, status):
        raise NotImplementedError("abort_with_status is not implemented")
