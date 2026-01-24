import base64
import logging

import pyspark.sql.connect.proto.base_pb2 as spark_proto
from google.protobuf import message
from google.protobuf.any_pb2 import Any

import snowflake.snowpark
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark_decoder._internal.proto.generated import (
    DataframeProcessorMsg_pb2 as dp_proto,
)
from snowflake.snowpark_decoder.spark_decoder import SparkDecoder
from spark.connect.envelope_pb2 import ResponseEnvelope

logger = logging.getLogger(__name__)


def str2proto(b64_input: str, proto_output: message.Message) -> None:
    decoded = base64.b64decode(b64_input)
    proto_output.ParseFromString(decoded)


def proto2str(proto_input: message.Message) -> str:
    return str(base64.b64encode(proto_input.SerializeToString()), "utf-8")


class DataframeProcessorSession:
    """
    The Dataframe Processor Session provides session context for dataframe requests, internally it
    wraps the snowpark session object.
    """

    _instance = None  # Class-level variable to store the instance

    @classmethod
    def get_instance(
        cls,
        dataframe_type: dp_proto.DataframeType,
        session: snowflake.snowpark.Session = None,
    ) -> "DataframeProcessorSession":
        """Returns the singleton instance of the DataframeProcessorSession."""
        if cls._instance is None:
            if session is None:
                session = get_active_session()
            cls._instance = cls(session, dataframe_type)
        return cls._instance

    def __init__(
        self,
        session: snowflake.snowpark.Session,
        dataframe_type: dp_proto.DataframeType,
    ) -> None:
        """
        Initializes optional Snowpark session to connect to.
        Args:
            session: the Snowpark session to be used.
            dataframe_type: the type of dataframe to be processed.
        """
        session.ast_enabled = False
        self._session = session
        self._dataframe_type = dataframe_type
        if dataframe_type == dp_proto.SPARK_CONNECT:
            self._decoder = SparkDecoder(self._session)
        else:
            raise RuntimeError(f"Invalid dataframe type: {type}")

    def request(self, req_base64: str) -> str:
        """
        The only public method to generate response from a dataframe processor
        request.

        :param req_base64: the request string encoded by base64
        :return: the response string encoded by base64
        """
        try:
            dp_req_proto = dp_proto.Request()
            str2proto(req_base64, dp_req_proto)
            rid = dp_req_proto.request_id

            any_msg = dp_req_proto.payload
            if any_msg.Is(spark_proto.ConfigRequest.DESCRIPTOR):
                request = spark_proto.ConfigRequest()
            elif any_msg.Is(spark_proto.ExecutePlanRequest.DESCRIPTOR):
                request = spark_proto.ExecutePlanRequest()
            elif any_msg.Is(spark_proto.AnalyzePlanRequest.DESCRIPTOR):
                request = spark_proto.AnalyzePlanRequest()
            elif any_msg.Is(spark_proto.AddArtifactsRequest.DESCRIPTOR):
                request = spark_proto.AddArtifactsRequest()
            elif any_msg.Is(spark_proto.ArtifactStatusesRequest.DESCRIPTOR):
                request = spark_proto.ArtifactStatusesRequest()
            else:
                raise NotImplementedError(f"Unknown request type: {any_msg.TypeName()}")
            dp_req_proto.payload.Unpack(request)
            result = self._decoder.request(request)

            assert isinstance(result, ResponseEnvelope)
            code = (
                dp_proto.Response.StatusCode.EXECUTION_ERROR
                if result.WhichOneof("response_type") == "status"
                else dp_proto.Response.StatusCode.OK
            )

            payload = Any()
            payload.Pack(result)
            dp_res_proto = dp_proto.Response(
                code=code,
                payload=payload,
                dataframe_type=dp_req_proto.dataframe_type,
                request_id=rid,
            )
            return proto2str(dp_res_proto)
        except Exception:
            # raise the error to GS
            raise
