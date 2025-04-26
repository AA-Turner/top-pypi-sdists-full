
import pytest as pytest

from snowflake.core._common import CreateMode
from snowflake.core.procedure import (
    Argument,
    CallArgument,
    CallArgumentList,
    ColumnType,
    JavaFunction,
    JavaScriptFunction,
    Procedure,
    ReturnDataType,
    ReturnTable,
    SQLFunction,
)


@pytest.mark.min_sf_ver("8.38.0")
def test_call_procedures(procedures, cursor, populate_tables_for_procedure_call, maven_snowpark_jar_available):
    del maven_snowpark_jar_available
    javascript_proc_with_args = Procedure(
        name="javascript_proc_with_args",
        arguments=[
            Argument(
                name="float1",
                datatype="FLOAT"
            ),
            Argument(
                name="float2",
                datatype="FLOAT"
            )
        ],
        return_type=ReturnDataType(datatype="FLOAT"),
        language_config=JavaScriptFunction(),
        body="""return FLOAT1"""
    )
    try:
        proc = procedures.create(javascript_proc_with_args, mode=CreateMode.or_replace)
        assert proc.call(call_argument_list=CallArgumentList(call_arguments=[
            CallArgument(name="float1", datatype="FLOAT", value=3.14),
            CallArgument(name="float2", datatype="FLOAT", value=4.13)
        ])) == [{f"{javascript_proc_with_args.name}": 3.14}]
    finally:
        proc.drop()

    sql_proc_table_func = Procedure(
        name="sql_proc_table_func",
        arguments=[Argument(name="id", datatype="VARCHAR")],
        return_type=ReturnTable(
            column_list=[
                ColumnType(name="id", datatype="NUMBER"),
                ColumnType(name="price", datatype="NUMBER"),
            ]
        ),
        language_config=SQLFunction(),
        body="""DECLARE
                    res RESULTSET DEFAULT (SELECT * FROM invoices WHERE id = :id);
                BEGIN
                    RETURN TABLE(res);
                END;
            """,
    )
    try:
        proc = procedures.create(sql_proc_table_func, mode=CreateMode.or_replace)
        assert proc.call(call_argument_list=CallArgumentList(call_arguments=[
            CallArgument(name="id", datatype="TEXT", value=1)
        ])) == [{'id': '1', 'price': '1'}, {'id': '1', 'price': '2'}]

        assert proc.call(call_argument_list=CallArgumentList(call_arguments=[
            CallArgument(name="id", datatype="TEXT", value=2)
        ])) == [{'id': '2', 'price': '3'}]
    finally:
        proc.drop()

    java_proc_with_args = Procedure(
        name="java_proc_with_args",
        arguments=[
            Argument(name="bin", datatype="BINARY", default="534E4F57"),
            Argument(
                name="bool",
                datatype="BOOLEAN",
                default="FALSE",
            ),
        ],
        return_type=ReturnDataType(name="ret", datatype="VARCHAR"),
        language_config=JavaFunction(
            runtime_version="11",
            handler="Test.retGeo",
            packages=["com.snowflake:snowpark:latest"],
        ),
        # we're returning string since the GEOGRAPHY datatype will accept strings
        body="""class Test {
                    public String retGeo(com.snowflake.snowpark.Session session, String binary, boolean bool) {
                        if(binary.equals("534E4F57")) {
                            return binary;
                        } else {
                            return String.valueOf(bool);
                        }
                    }
                }
            """,
    )
    try:
        proc = procedures.create(java_proc_with_args, mode=CreateMode.or_replace)
        assert proc.call(call_argument_list=CallArgumentList(call_arguments=[
            CallArgument(name="bin", datatype="BINARY", value="534E4F57"),
            CallArgument(name="bool", datatype="BOOLEAN", value=True),
        ])) == [{f"{java_proc_with_args.name}": "534E4F57"}]

        assert proc.call(call_argument_list=CallArgumentList(call_arguments=[
            CallArgument(name="bin", datatype="BINARY", value="534E4F56"),
            CallArgument(name="bool", datatype="BOOLEAN", value=True),
        ])) == [{f"{java_proc_with_args.name}": "true"}]
    finally:
        proc.drop()
