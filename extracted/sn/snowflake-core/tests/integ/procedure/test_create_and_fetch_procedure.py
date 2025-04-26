
import pytest as pytest

from snowflake.core._common import CreateMode
from snowflake.core.exceptions import APIError, ConflictError
from snowflake.core.procedure import (
    Argument,
    ColumnType,
    JavaFunction,
    JavaScriptFunction,
    Procedure,
    PythonFunction,
    ReturnDataType,
    ReturnTable,
    ScalaFunction,
    SQLFunction,
)
from snowflake.core.procedure._generated import FunctionLanguage


pytestmark = [pytest.mark.min_sf_ver("8.38.0")]


def test_create_javascript_proc(procedures):
    javascript_proc_no_args = Procedure(
        name="javascript_proc_no_args",
        arguments=[],
        return_type=ReturnDataType(datatype="FLOAT", nullable=False),
        language_config=JavaScriptFunction(),
        body="""return 3.14;""",
    )
    try:
        proc = procedures.create(javascript_proc_no_args, mode=CreateMode.or_replace, copy_grants=True)
        proc_fetch_result = proc.fetch()
        assert proc_fetch_result.name == "JAVASCRIPT_PROC_NO_ARGS"
        assert proc_fetch_result.language_config == JavaScriptFunction(called_on_null_input=True)
        assert proc_fetch_result.return_type == ReturnDataType(datatype="FLOAT", nullable=False)
        assert proc_fetch_result.is_builtin is True
    finally:
        proc.drop()

    # JavaScript Procedure - Arguments
    javascript_proc_with_args = Procedure(
        name="javascript_proc_with_args",
        arguments=[Argument(name="TSV", datatype="VARCHAR", default="this will not work without input")],
        return_type=ReturnDataType(datatype="TIMESTAMP_LTZ"),
        language_config=JavaScriptFunction(),
        body="""// Convert the input varchar to a TIMESTAMP_LTZ.
                var sql_command = "SELECT '" + TSV + "'::TIMESTAMP_LTZ;";
                var stmt = snowflake.createStatement( {sqlText: sql_command} );
                var resultSet = stmt.execute();
                resultSet.next();
                // Retrieve the TIMESTAMP_LTZ and store it in an SfDate variable.
                var my_sfDate = resultSet.getColumnValue(1);

                f = 3.1415926;

                // Specify that we'd like position-based binding.
                sql_command = `INSERT INTO table1 VALUES(:1, :2, :3, :4, :5, :6, :7, :8);`
                // Bind a VARCHAR, a TIMESTAMP_LTZ, a numeric to our INSERT statement.
                result = snowflake.execute(
                    {
                    sqlText: sql_command,
                    binds: [TSV, my_sfDate, f, f, f, my_sfDate, my_sfDate, '12:30:00.123' ]
                    }
                    );

                return my_sfDate;
                """,
    )
    try:
        proc = procedures.create(javascript_proc_with_args, mode=CreateMode.or_replace)
        proc_fetch_result = proc.fetch()
        assert proc_fetch_result.name == "JAVASCRIPT_PROC_WITH_ARGS"
    finally:
        proc.drop()

    javascript_proc_strict = Procedure(
        name="javascript_proc_strict",
        arguments=[Argument(name="FLOAT_PARAM1", datatype="FLOAT", default=2.2)],
        return_type=ReturnDataType(datatype="VARCHAR"),
        language_config=JavaScriptFunction(),
        is_secure=True,
        body="""var sql_command =
                 "INSERT INTO stproc_test_table1 (num_col1) VALUES (" + FLOAT_PARAM1 + ")";
                try {
                    snowflake.execute (
                        {sqlText: sql_command}
                    );
                    return "Succeeded.";   // Return a success/error indicator.
                }
                catch (err)  {
                    return "Failed: " + err;   // Return a success/error indicator.
                }
            """,
    )
    try:
        proc = procedures.create(javascript_proc_strict, mode=CreateMode.or_replace)
        proc_fetch_result = proc.fetch()
        assert proc_fetch_result.name == "JAVASCRIPT_PROC_STRICT"
        assert proc_fetch_result.arguments == [Argument(name="FLOAT_PARAM1", datatype="FLOAT", default=2.2)]
        assert proc_fetch_result.return_type == ReturnDataType(datatype="VARCHAR", nullable=True)
        assert proc_fetch_result.language_config == JavaScriptFunction(called_on_null_input=True)
        assert proc_fetch_result.is_secure is True
        assert proc_fetch_result.is_builtin is True
    finally:
        proc.drop()

    javascript_proc_execute_as_and_comment = Procedure(
        name="javascript_proc_execute_as_and_comment",
        comment="comment",
        execute_as="OWNER",
        arguments=[Argument(name="FLOAT_PARAM1", datatype="FLOAT")],
        return_type=ReturnDataType(datatype="VARCHAR", nullable=False),
        language_config=JavaScriptFunction(),
        is_secure=True,
        body="""  var row_count = 0;
                  // Dynamically compose the SQL statement to execute.
                  var sql_command = "select count(*) from " + TABLE_NAME;
                  // Run the statement.
                  var stmt = snowflake.createStatement(
                         {
                         sqlText: sql_command
                         }
                      );
                  var res = stmt.execute();
                  // Get back the row count. Specifically, ...
                  // ... get the first (and in this case only) row from the result set ...
                  res.next();
                  // ... and then get the returned value, which in this case is the number of
                  // rows in the table.
                  row_count = res.getColumnValue(1);
                  return row_count;
            """,
    )
    try:
        proc = procedures.create(javascript_proc_execute_as_and_comment, mode=CreateMode.or_replace)
        proc_fetch_result = proc.fetch()
        assert proc_fetch_result.name == "JAVASCRIPT_PROC_EXECUTE_AS_AND_COMMENT"
        assert proc_fetch_result.arguments == [Argument(name="FLOAT_PARAM1", datatype="FLOAT")]
        assert proc_fetch_result.return_type == ReturnDataType(datatype="VARCHAR", nullable=False)
        assert proc_fetch_result.language_config == JavaScriptFunction(called_on_null_input=True)
        assert proc_fetch_result.execute_as == "OWNER"
        assert proc_fetch_result.comment == "comment"
        assert proc_fetch_result.is_secure is True
        assert proc_fetch_result.is_builtin is True
    finally:
        proc.drop()


def test_create_sql_proc(procedures):
    sql_proc_no_args = Procedure(
        name="sql_proc_no_args",
        arguments=[],
        return_type=ReturnDataType(datatype="NUMBER", nullable=False),
        language_config=SQLFunction(),
        body="""BEGIN return 3; END""",
    )
    try:
        proc = procedures.create(sql_proc_no_args, mode=CreateMode.or_replace)
        proc_fetch_result = proc.fetch()
        assert proc_fetch_result.name == "SQL_PROC_NO_ARGS"
        assert proc_fetch_result.return_type == ReturnDataType(datatype="NUMBER", nullable=False)
        assert proc_fetch_result.language_config == SQLFunction(called_on_null_input=True)
        assert proc_fetch_result.is_builtin is True
    finally:
        proc.drop()

    # Sql Procedure - Arguments
    sql_proc_with_args = Procedure(
        name="sql_proc_with_args",
        arguments=[
            Argument(name="number1", datatype="NUMBER", default=1),
            Argument(name="number2", datatype="NUMBER", default=2),
        ],
        return_type=ReturnDataType(datatype="BOOLEAN", nullable=False),
        language_config=SQLFunction(),
        body="""BEGIN
                    IF (number1 > number2) THEN
                        RETURN true;
                    ELSE
                        RETURN false;
                    END IF;
                END
            """,
    )
    try:
        proc = procedures.create(sql_proc_with_args, mode=CreateMode.or_replace)
        proc_fetch_result = proc.fetch()
        assert proc_fetch_result.name == "SQL_PROC_WITH_ARGS"
    finally:
        proc.drop()

    # Sql Procedure - Table Function
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
        proc_fetch_result = proc.fetch()
        assert proc_fetch_result.name == "SQL_PROC_TABLE_FUNC"
    finally:
        proc.drop()

    # Sql Procedure
    sql_proc_parameters = Procedure(
        name="sql_proc_parameters",
        arguments=[Argument(name="id", datatype="VARCHAR")],
        is_secure=True,
        execute_as="CALLER",
        return_type=ReturnTable(
            column_list=[
                ColumnType(name="id", datatype="NUMBER"),
                ColumnType(name="price", datatype="NUMBER"),
            ]
        ),
        language_config=SQLFunction(
            called_on_null_input=True,
        ),
        body="""DECLARE
                    res RESULTSET DEFAULT (SELECT * FROM invoices WHERE id = :id);
                BEGIN
                    RETURN TABLE(res);
                END;
            """,
    )
    try:
        proc = procedures.create(sql_proc_parameters, mode=CreateMode.or_replace)
        proc_fetch_result = proc.fetch()
        assert proc_fetch_result.name == "SQL_PROC_PARAMETERS"
    finally:
        proc.drop()


def test_create_java_proc(procedures, maven_snowpark_jar_available):
    del maven_snowpark_jar_available
    # Java Procedure - No Arguments
    java_proc_no_args = Procedure(
        name="java_proc_no_args",
        arguments=[],
        return_type=ReturnDataType(datatype="VARCHAR"),
        language_config=JavaFunction(
            runtime_version="11",
            handler="Test.testProc",
            packages=["com.snowflake:snowpark:latest"],
        ),
        body="""class Test {
                    public String testProc(com.snowflake.snowpark.Session session) {
                        return "ret string";
                    }
                }
            """,
    )
    try:
        proc = procedures.create(java_proc_no_args, mode=CreateMode.or_replace)
        proc_fetch_result = proc.fetch()
        assert proc_fetch_result.name == "JAVA_PROC_NO_ARGS"
    finally:
        proc.drop()

    # Java Procedure - Table Function
    java_proc_table_func = Procedure(
        name="java_proc_table_func",
        arguments=[
            Argument(name="tableName", datatype="VARCHAR", default="this will not work without input"),
            Argument(name="role", datatype="VARCHAR"),
            Argument(name="int1", datatype="NUMBER", default=1),
            Argument(name="ts1", datatype="TIMESTAMP_LTZ"),
        ],
        return_type=ReturnTable(column_list=[ColumnType(name="Name", datatype="VARCHAR")]),
        language_config=JavaFunction(
            runtime_version="11",
            handler="FilterClass.filterByRole",
            packages=["com.snowflake:snowpark:latest"],
        ),
        body="""import com.snowflake.snowpark_java.*;
                public class FilterClass {
                    public DataFrame filterByRole(Session session,
                                                    String tableName, String role, int int1, String ts1) {
                        DataFrame table = session.table(tableName);
                        DataFrame filteredRows = table.filter(Functions.col("role").equal_to(Functions.lit(role)));
                        return filteredRows;
                    }
                }
            """,
    )
    try:
        proc = procedures.create(java_proc_table_func, mode=CreateMode.or_replace)
        proc_fetch_result = proc.fetch()
        javafun = proc_fetch_result.language_config
        assert proc_fetch_result.name == "JAVA_PROC_TABLE_FUNC"
        assert proc_fetch_result.arguments == [
                Argument(name="TABLENAME", datatype="VARCHAR", default="this will not work without input"),
                Argument(name="ROLE", datatype="VARCHAR"),
                Argument(name="INT1", datatype="NUMBER", default=1),
                Argument(name="TS1", datatype="TIMESTAMP_LTZ"),
            ]
        assert proc_fetch_result.return_type == ReturnTable(column_list=[ColumnType(name="NAME", datatype="VARCHAR")])
        assert javafun.runtime_version == "11"
        assert javafun.handler == "FilterClass.filterByRole"
        assert proc_fetch_result.is_builtin is True
    finally:
        proc.drop()

    # Java Procedure - Arguments
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
        proc_fetch_result = proc.fetch()
        assert proc_fetch_result.name == "JAVA_PROC_WITH_ARGS"
    finally:
        proc.drop()

    # Java Procedure
    java_proc_parameters = Procedure(
        name="java_proc_with_args",
        arguments=[
            Argument(name="geography", datatype="GEOGRAPHY"),
            Argument(
                name="int1",
                datatype="NUMBER",
                default="1",
            ),
            Argument(
                name="arr1",
                datatype="ARRAY",
            ),
        ],
        is_secure=False,
        comment="comment",
        execute_as="CALLER",
        return_type=ReturnDataType(name="Geography", datatype="GEOGRAPHY"),
        language_config=JavaFunction(
            called_on_null_input=False,
            runtime_version="11",
            handler="Test.retGeo",
            packages=["com.snowflake:snowpark:latest"],
        ),
        # we're returning string since the GEOGRAPHY datatype will accept strings
        body="""class Test {
                    public String retGeo(com.snowflake.snowpark.Session session,
                                            String geography, int int1, String[] arr1) {
                        return geography;
                    }
                }
        """,
    )
    try:
        proc = procedures.create(java_proc_parameters, mode=CreateMode.or_replace)
        proc_fetch_result = proc.fetch()
        javafn = proc_fetch_result.language_config
        assert proc_fetch_result.name == "JAVA_PROC_WITH_ARGS"
        assert proc_fetch_result.arguments == [
                Argument(name="GEOGRAPHY", datatype="GEOGRAPHY"),
                Argument(
                    name="INT1",
                    datatype="NUMBER",
                    default="1",
                ),
                Argument(
                    name="ARR1",
                    datatype="ARRAY",
                ),
            ]
        assert proc_fetch_result.return_type == ReturnDataType(name="Geography", datatype="GEOGRAPHY", nullable=True)
        assert javafn.runtime_version == "11"
        assert javafn.handler == "Test.retGeo"
        assert proc_fetch_result.is_builtin is True
        assert proc_fetch_result.comment == "comment"
        assert proc_fetch_result.execute_as == "CALLER"
        assert proc_fetch_result.is_secure is False
    finally:
        proc.drop()


def test_create_python_proc(procedures, anaconda_package_available):
    del anaconda_package_available
    python_proc_no_args = Procedure(
        name="python_proc_no_args",
        arguments=[],
        return_type=ReturnDataType(datatype="VARCHAR"),
        language_config=PythonFunction(
            runtime_version="3.9",
            handler="handler",
            packages=["snowflake-snowpark-python"],
        ),
        body="""def handler(session):
                                return 'str'
                        """,
    )
    try:
        proc = procedures.create(python_proc_no_args, mode=CreateMode.or_replace)
        proc_fetch_result = proc.fetch()
        assert proc_fetch_result.name == "PYTHON_PROC_NO_ARGS"
    finally:
        proc.drop()

    python_proc_with_args = Procedure(
        name="python_proc_with_args",
        arguments=[
            Argument(name="arr", datatype="ARRAY", default=[1, 2, 3, 4]),
            Argument(name="vari", datatype="VARIANT", default={"str": 1, "test": 5}),
        ],
        return_type=ReturnDataType(datatype="VARCHAR"),
        language_config=PythonFunction(
            runtime_version="3.9",
            handler="handler",
            packages=["snowflake-snowpark-python"],
        ),
        body="""def handler(session, arr, vari):
                                print(arr)
                                print(vari["str"])
                        """,
    )
    try:
        proc = procedures.create(python_proc_with_args, mode=CreateMode.or_replace)
        proc_fetch_result = proc.fetch()
        assert proc_fetch_result.name == "PYTHON_PROC_WITH_ARGS"
        assert proc_fetch_result.arguments == [
                Argument(name="ARR", datatype="ARRAY", default=[1, 2, 3, 4]),
                Argument(name="VARI", datatype="VARIANT", default={"str": 1, "test": 5}),
            ]
        assert proc_fetch_result.return_type == ReturnDataType(datatype="VARCHAR", nullable=True)
        assert proc_fetch_result.language_config == PythonFunction(
            runtime_version="3.9",
            handler="handler",
            packages=["snowflake-snowpark-python"],
            imports=[],
            external_access_integrations=[],
            secrets={}
        )
        assert proc_fetch_result.is_builtin is True
    finally:
        proc.drop()

    python_proc_table_func = Procedure(
        name="python_proc_table_func",
        arguments=[
            Argument(name="num1", datatype="NUMBER"),
            Argument(name="varchar1", datatype="VARCHAR"),
            Argument(name="arr1", datatype="ARRAY"),
            Argument(name="object1", datatype="OBJECT"),
        ],
        return_type=ReturnTable(
            column_list=[
                ColumnType(name="col1", datatype="GEOGRAPHY"),
                ColumnType(name="col2", datatype="FLOAT"),
                ColumnType(name="col4", datatype="NUMBER"),
            ]
        ),
        language_config=PythonFunction(
            runtime_version="3.9",
            handler="handler",
            packages=["snowflake-snowpark-python"],
        ),
        body="""def handler(session, num1, varchar1, arr1, object1):
                                print(arr1)
                                return None
                        """,
    )
    try:
        proc = procedures.create(python_proc_table_func, mode=CreateMode.or_replace)
        proc_fetch_result = proc.fetch()
        assert proc_fetch_result.name == "PYTHON_PROC_TABLE_FUNC"
        assert proc_fetch_result.arguments == [
                Argument(name="NUM1", datatype="NUMBER"),
                Argument(name="VARCHAR1", datatype="VARCHAR"),
                Argument(name="ARR1", datatype="ARRAY"),
                Argument(name="OBJECT1", datatype="OBJECT"),
            ]
        assert proc_fetch_result.return_type == ReturnTable(
                column_list=[
                    ColumnType(name="COL1", datatype="GEOGRAPHY"),
                    ColumnType(name="COL2", datatype="FLOAT"),
                    ColumnType(name="COL4", datatype="NUMBER"),
                ]
            )
        assert proc_fetch_result.language_config == PythonFunction(
            runtime_version="3.9",
            handler="handler",
            packages=["snowflake-snowpark-python"],
            imports=[],
            external_access_integrations=[],
            secrets={}
        )
        assert proc_fetch_result.is_builtin is True
    finally:
        proc.drop()

    python_proc_table_func = Procedure(
        name="python_proc_table_func",
        arguments=[Argument(name="symbol", datatype="VARCHAR")],
        return_type=ReturnTable(
            column_list=[
                ColumnType(name="symbol", datatype="VARCHAR"),
                ColumnType(name="price", datatype="NUMBER"),
            ]
        ),
        language_config=PythonFunction(
            runtime_version="3.9",
            handler="run",
            packages=["snowflake-snowpark-python"],
        ),
        body="""from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, sum

class StockSaleSumProc:
    def __init__(self, symbol):
        self._symbol = symbol

    def compute_total(self, session):
        df = session.table("stocks_table").filter(col("symbol") == self._symbol).select(col("symbol"),
                                                                        (col("quantity") * col("price")).alias("total")
                                                                                        )
        result_df = df.group_by(col("symbol")).agg(sum(col("total")).alias("total"))

        return result_df

def run(session: Session, symbol: str):
    stock_sale_sum = StockSaleSumProc(symbol)
    return stock_sale_sum.compute_total(session)
    """,
    )
    try:
        proc = procedures.create(python_proc_table_func, mode=CreateMode.or_replace)
        proc_fetch_result = proc.fetch()
        assert proc_fetch_result.name == "PYTHON_PROC_TABLE_FUNC"
        assert proc_fetch_result.arguments == [Argument(name="SYMBOL", datatype="VARCHAR")]
        assert proc_fetch_result.return_type == ReturnTable(
                column_list=[
                    ColumnType(name="SYMBOL", datatype="VARCHAR"),
                    ColumnType(name="PRICE", datatype="NUMBER"),
                ]
            )
        assert proc_fetch_result.language_config == PythonFunction(
            runtime_version="3.9",
            handler="run",
            packages=["snowflake-snowpark-python"],
            imports=[],
            external_access_integrations=[],
            secrets={}
        )
        assert proc_fetch_result.is_builtin is True
    finally:
        proc.drop()


def test_create_scala_proc(procedures, maven_snowpark_jar_available):
    del maven_snowpark_jar_available
    scala_proc_no_args = Procedure(
        name="scala_proc_no_args",
        arguments=[],
        return_type=ReturnDataType(datatype="VARCHAR"),
        language_config=ScalaFunction(
            runtime_version="2.12",
            handler="TestScalaSP.asyncBasic",
            packages=["com.snowflake:snowpark:latest"],
        ),
        body="""object TestScalaSP {
                  def asyncBasic(session: com.snowflake.snowpark.Session): String = {
                    val df = session.sql("select system$wait(10)")
                    val asyncJob = df.async.collect()
                    while(!asyncJob.isDone()) {
                      Thread.sleep(1000)
                    }
                    "Done"
                  }
                }
            """,
    )
    try:
        proc = procedures.create(scala_proc_no_args, mode=CreateMode.or_replace)
        proc_fetch_result = proc.fetch()
        assert proc_fetch_result.name == "SCALA_PROC_NO_ARGS"
    finally:
        proc.drop()

    scala_proc_with_args = Procedure(
        name="scala_proc_with_args",
        arguments=[
            Argument(name="fileName", datatype="VARCHAR"),
        ],
        return_type=ReturnDataType(datatype="VARCHAR"),
        language_config=ScalaFunction(
            runtime_version="2.12",
            handler="FileReader.execute",
            packages=["com.snowflake:snowpark:latest"],
        ),
        body="""import java.io.InputStream
                import java.nio.charset.StandardCharsets
                import com.snowflake.snowpark_java.types.SnowflakeFile
                import com.snowflake.snowpark_java.Session

                object FileReader {
                  def execute(session: Session, fileName: String): String = {
                    var input: InputStream = SnowflakeFile.newInstance(fileName).getInputStream()
                    return new String(input.readAllBytes(), StandardCharsets.UTF_8)
                  }
                }
            """,
    )
    try:
        proc = procedures.create(scala_proc_with_args, mode=CreateMode.or_replace)
        proc_fetch_result = proc.fetch()
        scalafun = proc_fetch_result.language_config
        assert proc_fetch_result.name == "SCALA_PROC_WITH_ARGS"
        assert proc_fetch_result.arguments == [
                Argument(name="FILENAME", datatype="VARCHAR"),
            ]
        assert proc_fetch_result.return_type == ReturnDataType(datatype="VARCHAR", nullable=True)
        assert scalafun.runtime_version == "2.12"
        assert scalafun.handler == "FileReader.execute"
        assert proc_fetch_result.is_builtin is True
    finally:
        proc.drop()

    scala_proc_table_func = Procedure(
        name="scala_proc_table_func",
        arguments=[
            Argument(name="tablename", datatype="VARCHAR"),
            Argument(name="role", datatype="VARCHAR"),
        ],
        comment="scala proc",
        is_secure=True,
        return_type=ReturnTable(
            column_list=[
                ColumnType(name="id", datatype="NUMBER"),
                ColumnType(name="name", datatype="VARCHAR"),
                ColumnType(name="role", datatype="VARCHAR"),
            ]
        ),
        language_config=ScalaFunction(
            runtime_version="2.12",
            handler="Filter.filterByRole",
            packages=["com.snowflake:snowpark:latest"],
        ),
        body="""import com.snowflake.snowpark.functions._
                import com.snowflake.snowpark._

                object Filter {
                   def filterByRole(session: Session, tableName: String, role: String): DataFrame = {
                     val table = session.table(tableName)
                     val filteredRows = table.filter(col("role") === role)
                     return filteredRows
                   }
                }
            """,
    )
    try:
        proc = procedures.create(scala_proc_table_func, mode=CreateMode.or_replace)
        proc_fetch_result = proc.fetch()
        scalafun = proc_fetch_result.language_config
        assert proc_fetch_result.name == "SCALA_PROC_TABLE_FUNC"
        assert proc_fetch_result.arguments == [
                Argument(name="TABLENAME", datatype="VARCHAR"),
                Argument(name="ROLE", datatype="VARCHAR"),
            ]
        assert proc_fetch_result.return_type == ReturnTable(
                column_list=[
                    ColumnType(name="ID", datatype="NUMBER"),
                    ColumnType(name="NAME", datatype="VARCHAR"),
                    ColumnType(name="ROLE", datatype="VARCHAR"),
                ]
            )
        assert scalafun.runtime_version == "2.12"
        assert scalafun.handler == "Filter.filterByRole"
        assert proc_fetch_result.comment == "scala proc"
        assert proc_fetch_result.is_secure is True
        assert proc_fetch_result.is_builtin is True
    finally:
        proc.drop()


@pytest.mark.usefixtures("anaconda_package_available")
def test_create_procedure_or_replace(procedures):
    python_proc_no_args1 = Procedure(
        name="python_proc_no_args",
        arguments=[],
        return_type=ReturnDataType(datatype="VARCHAR"),
        language_config=PythonFunction(
            runtime_version="3.9",
            handler="handler",
            packages=["snowflake-snowpark-python"],
        ),
        body="""def handler(session):
                    return 'str'
            """,
    )
    python_proc_no_args2 = Procedure(
        name="python_proc_no_args",
        arguments=[],
        return_type=ReturnDataType(datatype="NUMBER"),
        language_config=PythonFunction(
            runtime_version="3.9",
            handler="handler",
            packages=["snowflake-snowpark-python"],
        ),
        body="""def handler(session):
                            return 'str'
                    """,
    )
    try:
        proc = procedures.create(python_proc_no_args1, mode=CreateMode.or_replace)
        proc_fetch_result = proc.fetch()
        assert proc_fetch_result.name == "PYTHON_PROC_NO_ARGS"
        assert proc_fetch_result.return_type.datatype == "VARCHAR"

        proc = procedures.create(python_proc_no_args2, mode=CreateMode.or_replace)
        proc_fetch_result = proc.fetch()
        assert proc_fetch_result.name == "PYTHON_PROC_NO_ARGS"
        assert proc_fetch_result.return_type.datatype == "NUMBER"
    finally:
        proc.drop()


@pytest.mark.usefixtures("anaconda_package_available")
def test_create_procedure_error_if_exists(procedures):
    python_proc_no_args1 = Procedure(
        name="python_proc_no_args1",
        arguments=[],
        return_type=ReturnDataType(datatype="VARCHAR"),
        language_config=PythonFunction(
            runtime_version="3.9",
            handler="handler",
            packages=["snowflake-snowpark-python"],
        ),
        body="""def handler(session):
                    return 'str'
            """,
    )

    python_proc_no_args2 = Procedure(
        name="python_proc_no_args1",
        arguments=[],
        return_type=ReturnDataType(datatype="VARCHAR"),
        language_config=PythonFunction(
            runtime_version="3.9",
            handler="handler",
            packages=["snowflake-snowpark-python"],
        ),
        body="""def handler(session):
                        return 'str'
                """,
    )
    try:
        proc1 = procedures.create(python_proc_no_args1)
        with pytest.raises(ConflictError):
            procedures.create(python_proc_no_args2, mode=CreateMode.error_if_exists)
    finally:
        proc1.drop()


@pytest.mark.usefixtures("anaconda_package_available")
def test_create_procedure_if_not_exists(procedures):
    python_proc_no_args1 = Procedure(
        name="python_proc_no_args2",
        arguments=[],
        return_type=ReturnDataType(datatype="VARCHAR"),
        language_config=PythonFunction(
            runtime_version="3.9",
            handler="handler",
            packages=["snowflake-snowpark-python"],
        ),
        body="""def handler(session):
                        return 'str'
                """,
    )

    python_proc_no_args2 = Procedure(
        name="python_proc_no_args2",
        arguments=[],
        return_type=ReturnDataType(datatype="NUMBER"),
        language_config=PythonFunction(
            runtime_version="3.9",
            handler="handler",
            packages=["snowflake-snowpark-python"],
        ),
        body="""def handler(session):
                            return 'str'
                    """,
    )
    try:
        proc1 = procedures.create(python_proc_no_args1, mode=CreateMode.or_replace)
        proc_fetch_result = proc1.fetch()
        assert proc_fetch_result.name == "PYTHON_PROC_NO_ARGS2"
        assert proc_fetch_result.return_type.datatype == "VARCHAR"

        proc2 = procedures.create(python_proc_no_args2, mode=CreateMode.if_not_exists)
        proc_fetch_result = proc2.fetch()
        assert proc_fetch_result.name == "PYTHON_PROC_NO_ARGS2"
        assert proc_fetch_result.return_type.datatype == "VARCHAR"
    finally:
        proc1.drop()


def test_create_procedure_invalid_language(procedures):
    random_proc = Procedure(
        name="random_proc",
        arguments=[],
        return_type=ReturnDataType(datatype="VARCHAR"),
        language_config=FunctionLanguage(),
        body="""return""",
    )
    with pytest.raises(APIError):
        procedures.create(random_proc, mode=CreateMode.error_if_exists)
