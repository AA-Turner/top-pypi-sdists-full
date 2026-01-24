#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import snowflake.snowpark_connect.proto.control_pb2 as control_proto
import snowflake.snowpark_connect.proto.control_pb2_grpc as control_grpc
from snowflake import snowpark
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger


class ControlServicer(control_grpc.ControlServiceServicer):
    def __init__(self, session: snowpark.session.Session) -> None:
        self.session = session
        self.log_ast = True  # TODO: False after Configure is enabled.
        self.ast_listener = session.ast_listener()
        self.spark_connect_batches = []

    def log_spark_connect_batch(self, batch):
        self.spark_connect_batches.append(batch)

    # TODO: Enable configure method when it is ready.
    # def Configure(self, request: control_proto.Config, context):
    #     if request.HasField("log_ast"):
    #         self.log_ast = request.log_ast
    #         # TODO: attach/detach listener.
    #
    #     return Config(log_ast=self.log_ast)

    def Ping(
        self, request: control_proto.PingRequest, context
    ) -> control_proto.PingResponse:
        return control_proto.PingResponse(payload=request.payload + " **")

    def GetRequestAst(
        self, request: control_proto.GetRequestAstRequest, context
    ) -> control_proto.GetRequestAstResponse:
        # TODO: assert self.session.ast_enabled
        logger.info(
            f"Returning AST for {len(self.ast_listener._ast_batches)} batches and "
            + f"{len(self.spark_connect_batches)} Spark requests"
        )
        res = control_proto.GetRequestAstResponse()

        # Copy the batches.
        res.spark_requests.extend(self.spark_connect_batches)
        res.snowpark_ast_batches.extend(self.ast_listener._ast_batches)

        # Reset the local state.
        self.spark_connect_batches = []
        self.ast_listener._ast_batches = []

        return res
