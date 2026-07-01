#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import pyspark.sql.connect.proto.base_pb2 as proto_base
import pyspark.sql.connect.proto.relations_pb2 as relation_proto

from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.execute_plan.utils import pandas_to_arrow_batches_bytes
from snowflake.snowpark_connect.expression import map_udf
from snowflake.snowpark_connect.relation import map_udtf
from snowflake.snowpark_connect.relation.map_relation import map_relation
from snowflake.snowpark_connect.relation.map_sql import map_sql_to_pandas_df
from snowflake.snowpark_connect.relation.read.metadata_utils import (
    without_hidden_columns,
)
from snowflake.snowpark_connect.relation.write.map_write import map_write, map_write_v2
from snowflake.snowpark_connect.utils.request_utils import get_or_generate_operation_id
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
)
from snowflake.snowpark_connect.utils.temporary_view_helper import (
    create_temporary_view_from_dataframe,
)


def map_execution_command(
    request: proto_base.ExecutePlanRequest,
) -> proto_base.ExecutePlanResponse | None:
    logger.debug(request.plan.command.WhichOneof("command_type").upper())
    match request.plan.command.WhichOneof("command_type"):
        case "create_dataframe_view":
            req = request.plan.command.create_dataframe_view
            input_df_container = without_hidden_columns(map_relation(req.input))
            create_temporary_view_from_dataframe(
                input_df_container, req.name, req.is_global, req.replace
            )
        case "write_stream_operation_start":
            match request.plan.command.write_stream_operation_start.format:
                case "console":
                    # TODO: Make the console output work with Spark style formatting.
                    # result_df: pandas.DataFrame = map_relation(
                    #     relation_proto.Relation(
                    #         show_string=relation_proto.ShowString(
                    #             input=request.plan.command.write_stream_operation_start.input,
                    #             num_rows=100,
                    #             truncate=False,
                    #         )
                    #     )
                    # )
                    # logger.info(result_df.iloc[0, 0])
                    map_relation(
                        request.plan.command.write_stream_operation_start.input
                    ).show()
        case "sql_command":
            sql_command = request.plan.command.sql_command
            pandas_df, schema = map_sql_to_pandas_df(
                sql_command.sql, sql_command.args, sql_command.pos_args
            )
            # SELECT query in SQL command will return None instead of Pandas DF to enable lazy evaluation
            if pandas_df is not None:
                relation = relation_proto.Relation(
                    local_relation=relation_proto.LocalRelation(
                        data=None
                        if pandas_df.empty
                        else pandas_to_arrow_batches_bytes(pandas_df),
                        schema=schema,
                    )
                )
            else:
                # Return the original SQL query.
                # This is what native Spark Connect does, and the Scala client expects it.
                relation = relation_proto.Relation(
                    sql=relation_proto.SQL(
                        query=sql_command.sql,
                        args=sql_command.args,
                        pos_args=sql_command.pos_args,
                    )
                )
            return proto_base.ExecutePlanResponse(
                session_id=request.session_id,
                operation_id=get_or_generate_operation_id(request),
                sql_command_result=proto_base.ExecutePlanResponse.SqlCommandResult(
                    relation=relation
                ),
            )
        case "write_operation":
            map_write(request)

        case "write_operation_v2":
            map_write_v2(request)

        case "register_function":
            map_udf.register_udf(request.plan.command.register_function)

        case "register_table_function":
            map_udtf.register_udtf(request.plan.command.register_table_function)

        case other:
            exception = SnowparkConnectNotImplementedError(
                f"Command type {other} not implemented"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception
