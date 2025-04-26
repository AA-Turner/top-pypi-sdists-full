
from contextlib import suppress

import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.user_defined_function import (
    Argument,
    ColumnType,
    JavaFunction,
    JavaScriptFunction,
    PythonFunction,
    ReturnDataType,
    ReturnTable,
    ScalaFunction,
    SQLFunction,
    UserDefinedFunction,
)
from tests.utils import random_string


pytestmark = [pytest.mark.min_sf_ver("8.38.0"), pytest.mark.usefixtures("anaconda_package_available")]

def test_create_and_fetch_python(user_defined_functions):
    user_defined_function_name = random_string(10, "test_create_user_defined_function_py_")

    user_defined_function_created = user_defined_functions.create(
        UserDefinedFunction(
            name=user_defined_function_name,
            arguments=[],
            return_type=ReturnDataType(datatype="VARIANT"),
            language_config=PythonFunction(runtime_version="3.9", packages=[], handler="udf"),
            body="""
def udf():
    return {"key": "value"}
            """,
        )
    )

    try:
        user_defined_function_handle = user_defined_function_created.fetch()
        assert user_defined_function_handle.name.upper() == user_defined_function_name.upper()
        assert user_defined_function_handle.return_type.datatype == "VARIANT"
        assert user_defined_function_handle.language_config.runtime_version == "3.9"
        assert user_defined_function_handle.language_config.packages == []
        assert user_defined_function_handle.language_config.handler == "udf"
        assert user_defined_function_handle.body == """
def udf():
    return {"key": "value"}
            """

    finally:
        user_defined_function_created.drop()


def test_create_and_fetch_java(user_defined_functions, cursor):
    user_defined_function_name = random_string(10, "test_create_user_defined_function_java_")
    target_path = random_string(5, "@~/testfunc_") + ".jar"

    func_body = """
    class TestFunc {
        public static String echoVarchar(String x) {
            return x;
        }
    }
    """

    user_defined_function_created = user_defined_functions.create(
        UserDefinedFunction(
            name=user_defined_function_name,
            arguments=[Argument(name="x", datatype="STRING")],
            return_type=ReturnDataType(datatype="VARCHAR", nullable=True),
            language_config=JavaFunction(
                handler="TestFunc.echoVarchar",
                runtime_version="11",
                target_path=target_path,
                packages=[],
                called_on_null_input=True,
                is_volatile=True,
            ),
            body=func_body,
            comment="test_comment",
        )
    )

    try:
        user_defined_function_handle = user_defined_function_created.fetch()
        assert user_defined_function_handle.name.upper() == user_defined_function_name.upper()
        assert user_defined_function_handle.return_type.datatype == "VARCHAR"
        assert user_defined_function_handle.return_type.nullable is True
        assert user_defined_function_handle.language_config.runtime_version == "11"
        assert user_defined_function_handle.language_config.packages == []
        assert user_defined_function_handle.language_config.handler == "TestFunc.echoVarchar"
        assert user_defined_function_handle.language_config.target_path == target_path
        assert user_defined_function_handle.body == func_body
        assert user_defined_function_handle.comment == "test_comment"

    finally:
        user_defined_function_created.drop()
        with suppress(NotFoundError):
            cursor.execute(f"RM @~ pattern='.*{target_path.split('/')[1]}.*'").fetchone()


def test_create_and_fetch_js(user_defined_functions):
    user_defined_function_name = random_string(10, "test_create_user_defined_function_js_")

    func_body = """
        if (D <= 0) {
        return 1;
        } else {
        var result = 1;
        for (var i = 2; i <= D; i++) {
            result = result * i;
        }
        return result;
        }
    """

    user_defined_function_created = user_defined_functions.create(
        UserDefinedFunction(
            name=user_defined_function_name,
            arguments=[Argument(name="d", datatype="DOUBLE")],
            return_type=ReturnDataType(datatype="DOUBLE"),
            language_config=JavaScriptFunction(),
            body=func_body,
        )
    )

    try:
        user_defined_function_handle = user_defined_function_created.fetch()
        assert user_defined_function_handle.name.upper() == user_defined_function_name.upper()
        assert user_defined_function_handle.return_type.datatype == "FLOAT"
        assert user_defined_function_handle.body == func_body

    finally:
        user_defined_function_created.drop()


def test_create_and_fetch_scala(user_defined_functions, cursor):
    user_defined_function_name = random_string(10, "test_create_user_defined_function_scala_")
    target_path = random_string(5, "@~/testfunc_scala") + ".jar"

    func_body = """
        class Echo {
            def echoVarchar(x : String): String = {
                return x
            }
        }
    """

    user_defined_function_created = user_defined_functions.create(
        UserDefinedFunction(
            name=user_defined_function_name,
            arguments=[Argument(name="x", datatype="VARCHAR")],
            return_type=ReturnDataType(datatype="VARCHAR"),
            language_config=ScalaFunction(
                runtime_version="2.12", handler="Echo.echoVarchar", target_path=target_path, packages=[]
            ),
            body=func_body,
            comment="test_comment",
        )
    )

    try:
        user_defined_function_handle = user_defined_function_created.fetch()
        assert user_defined_function_handle.name.upper() == user_defined_function_name.upper()
        assert user_defined_function_handle.return_type.datatype == "VARCHAR"
        assert user_defined_function_handle.language_config.runtime_version == "2.12"
        assert user_defined_function_handle.language_config.packages == []
        assert user_defined_function_handle.language_config.handler == "Echo.echoVarchar"
        assert user_defined_function_handle.language_config.target_path == target_path
        assert user_defined_function_handle.body == func_body
        assert user_defined_function_handle.comment == "test_comment"

    finally:
        user_defined_function_created.drop()


    user_defined_function_name = random_string(10, "test_create_user_defined_function_scala_staged_")
    user_defined_function_created = user_defined_functions.create(
        UserDefinedFunction(
            name=user_defined_function_name,
            arguments=[Argument(name="x", datatype="VARCHAR")],
            return_type=ReturnDataType(datatype="VARCHAR"),
            language_config=ScalaFunction(
                runtime_version="2.12", handler="Echo.echoVarchar", imports=[target_path], packages=[]
            ),
            comment="test_comment",
        )
    )

    try:
        user_defined_function_handle = user_defined_function_created.fetch()
        assert user_defined_function_handle.name.upper() == user_defined_function_name.upper()
        assert user_defined_function_handle.return_type.datatype == "VARCHAR"
        assert user_defined_function_handle.language_config.runtime_version == "2.12"
        assert user_defined_function_handle.language_config.packages == []
        assert user_defined_function_handle.language_config.handler == "Echo.echoVarchar"
        assert user_defined_function_handle.language_config.imports == [target_path]
        assert user_defined_function_handle.comment == "test_comment"

    finally:
        user_defined_function_created.drop()
        with suppress(NotFoundError):
            cursor.execute(f"RM @~ pattern='.*{target_path.split('/')[1]}.*'").fetchone()


def test_create_and_fetch_scala_object_argument(user_defined_functions):
    user_defined_function_name = random_string(10, "test_create_user_defined_function_scala_object_arg_")

    func_body = """
        class VariantLibrary {
          def extract(m: Map[String, String], key: String): String = {
            return m(key)
          }
        }
    """

    user_defined_function_created = user_defined_functions.create(
        UserDefinedFunction(
            name=user_defined_function_name,
            arguments=[Argument(name="x", datatype="OBJECT"), Argument(name="key", datatype="VARCHAR")],
            return_type=ReturnDataType(datatype="VARIANT"),
            language_config=ScalaFunction(handler="VariantLibrary.extract", runtime_version="2.12", packages=[]),
            body=func_body,
            comment="test_comment",
        )
    )

    try:
        user_defined_function_handle = user_defined_function_created.fetch()
        assert user_defined_function_handle.name.upper() == user_defined_function_name.upper()
        assert user_defined_function_handle.return_type.datatype == "VARIANT"
        assert user_defined_function_handle.language_config.runtime_version == "2.12"
        assert user_defined_function_handle.language_config.packages == []
        assert user_defined_function_handle.language_config.handler == "VariantLibrary.extract"
        assert user_defined_function_handle.body == func_body
        assert user_defined_function_handle.comment == "test_comment"

    finally:
        user_defined_function_created.drop()


def test_create_and_fetch_scala_array_input(user_defined_functions):
    user_defined_function_name = random_string(10, "test_create_user_defined_function_scala_array_input_")

    func_body = """
        class StringHandler {
          def handleStrings(strings: Array[String]): String = {
            return concatenate(strings)
          }
          private def concatenate(strings: Array[String]): String = {
            var concatenated : String = ""
            for (newString <- strings)  {
                concatenated = concatenated + " " + newString
            }
            return concatenated
          }
        }
    """

    user_defined_function_created = user_defined_functions.create(
        UserDefinedFunction(
            name=user_defined_function_name,
            arguments=[Argument(name="greeting_words", datatype="ARRAY")],
            return_type=ReturnDataType(datatype="VARCHAR"),
            language_config=ScalaFunction(handler="StringHandler.handleStrings", runtime_version="2.12", packages=[]),
            body=func_body,
            comment="test_comment",
        )
    )

    try:
        user_defined_function_handle = user_defined_function_created.fetch()
        assert user_defined_function_handle.name.upper() == user_defined_function_name.upper()
        assert user_defined_function_handle.return_type.datatype == "VARCHAR"
        assert user_defined_function_handle.language_config.runtime_version == "2.12"
        assert user_defined_function_handle.language_config.packages == []
        assert user_defined_function_handle.language_config.handler == "StringHandler.handleStrings"
        assert user_defined_function_handle.body == func_body
        assert user_defined_function_handle.comment == "test_comment"

    finally:
        user_defined_function_created.drop()


def test_create_and_fetch_sql(user_defined_functions):
    user_defined_function_name = random_string(10, "test_create_user_defined_function_sql_")

    func_body = """3.141592654::FLOAT"""

    user_defined_function_created = user_defined_functions.create(
        UserDefinedFunction(
            name=user_defined_function_name,
            arguments=[],
            return_type=ReturnDataType(datatype="FLOAT"),
            language_config=SQLFunction(),
            body=func_body,
        )
    )

    try:
        user_defined_function_handle = user_defined_function_created.fetch()
        assert user_defined_function_handle.name.upper() == user_defined_function_name.upper()
        assert user_defined_function_handle.return_type.datatype == "FLOAT"
        assert user_defined_function_handle.body == func_body

    finally:
        user_defined_function_created.drop()


def test_create_and_fetch_sql_hardcoded_values(user_defined_functions):
    user_defined_function_name = random_string(10, "test_create_user_defined_function_sql_")

    func_body = """
        SELECT 1, 2
        UNION ALL
        SELECT 3, 4
    """

    user_defined_function_created = user_defined_functions.create(
        UserDefinedFunction(
            name=user_defined_function_name,
            arguments=[],
            return_type=ReturnTable(
                column_list=[ColumnType(name="x", datatype="INTEGER"), ColumnType(name="y", datatype="INTEGER")]
            ),
            language_config=SQLFunction(),
            body=func_body,
        )
    )

    try:
        user_defined_function_handle = user_defined_function_created.fetch()
        assert user_defined_function_handle.name.upper() == user_defined_function_name.upper()
        assert user_defined_function_handle.return_type.column_list == [
            ColumnType(name="X", datatype="NUMBER"),
            ColumnType(name="Y", datatype="NUMBER"),
        ]
        assert user_defined_function_handle.body == func_body

    finally:
        user_defined_function_created.drop()


def test_create_and_fetch_sql_query_as_body(user_defined_functions, cursor):
    test_countries_table_name = random_string(10, "test_countries_")
    test_user_addresses_table_name = random_string(10, "test_user_addresses_")
    try:
        cursor.execute(f"""CREATE TABLE {test_countries_table_name} (
            country_code VARCHAR(10) PRIMARY KEY,
            country_name VARCHAR(255));
        """).fetchone()

        cursor.execute(f"""CREATE TABLE {test_user_addresses_table_name} (
            user_id INT,
            country_code VARCHAR(10),
            address VARCHAR(255),
            city VARCHAR(100),
            state VARCHAR(100),
            zip_code VARCHAR(20),
            PRIMARY KEY (user_id, country_code),
            FOREIGN KEY (country_code) REFERENCES {test_countries_table_name}(country_code)
        )""").fetchone()

        func_body = f"""
            SELECT DISTINCT c.country_code, c.country_name
            FROM {test_user_addresses_table_name} a, {test_countries_table_name} c
            WHERE a.user_id = id
            AND c.country_code = a.country_code
        """

        user_defined_function_name = random_string(10, "test_create_user_defined_function_sql_query_as_body_")

        user_defined_function_created = user_defined_functions.create(
            UserDefinedFunction(
                name=user_defined_function_name,
                arguments=[Argument(name="id", datatype="NUMBER")],
                return_type=ReturnTable(
                    column_list=[
                        ColumnType(name="country_code", datatype="CHAR"),
                        ColumnType(name="country_name", datatype="VARCHAR"),
                    ]
                ),
                language_config=SQLFunction(),
                body=func_body,
            )
        )

        try:
            user_defined_function_handle = user_defined_function_created.fetch()
            assert user_defined_function_handle.name.upper() == user_defined_function_name.upper()
            assert len(user_defined_function_handle.return_type.column_list) == 2
            for i in [
                ColumnType(name="country_code".upper(), datatype="VARCHAR"),
                ColumnType(name="country_name".upper(), datatype="VARCHAR"),
            ]:
                assert i in user_defined_function_handle.return_type.column_list
            assert user_defined_function_handle.body == func_body

        finally:
            user_defined_function_created.drop()

    finally:
        cursor.execute(f"DROP TABLE IF EXISTS {test_countries_table_name}").fetchone()
        cursor.execute(f"DROP TABLE IF EXISTS {test_user_addresses_table_name}").fetchone()

