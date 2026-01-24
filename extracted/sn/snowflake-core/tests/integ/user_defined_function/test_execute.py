from decimal import Decimal

import pytest

from snowflake.core.exceptions import APIError, InvalidArgumentsError
from snowflake.core.user_defined_function import (
    Argument,
    ReturnDataType,
    ScalaFunction,
    SQLFunction,
    UserDefinedFunction,
    UserDefinedFunctionArgument,
    UserDefinedFunctionResource,
)
from tests.utils import random_string


def test_execute_udf_decfloat(user_defined_functions):
    udf_name = random_string(10, "test_execute_udf_decfloat_")
    udf = UserDefinedFunction(
        name=udf_name,
        arguments=[Argument(name="arg", datatype="DECFLOAT")],
        return_type=ReturnDataType(datatype="DECFLOAT"),
        language_config=SQLFunction(),
        body="SELECT DECFLOAT '1.23e-2' + ARG",
    )
    udf_handle: UserDefinedFunctionResource = user_defined_functions.create(udf)
    try:
        result = udf_handle.execute(
            [UserDefinedFunctionArgument(name="arg", datatype="DECFLOAT", value=Decimal("1.02"))]
        )
        assert result == Decimal("1.0323")
    finally:
        udf_handle.drop(if_exists=True)


def test_execute_udf_with_two_args(user_defined_functions):
    func_body = """
                  class Echo {
                    def echoText(x : String, y: Int): String = {
                      return x
                    }
                  }
                """
    udf = UserDefinedFunction(
        name="echo_text",
        arguments=[Argument(name="x", datatype="TEXT"), Argument(name="y", datatype="INT")],
        return_type=ReturnDataType(datatype="TEXT"),
        language_config=ScalaFunction(runtime_version="2.12", handler="Echo.echoText", packages=[]),
        body=func_body,
    )
    udf_handle: UserDefinedFunctionResource = user_defined_functions.create(udf)
    try:
        result = udf_handle.execute(
            [
                UserDefinedFunctionArgument(name="y", datatype="INT", value=42),
                UserDefinedFunctionArgument(name="x", datatype="TEXT", value="TEST VALUE"),
            ]
        )
        assert result == "TEST VALUE"
    finally:
        udf_handle.drop(if_exists=True)


def test_execute_udf_without_args(user_defined_functions):
    func_body = """
              class Echo {
                def echoText(x: String): String = {
                  return x
                }
              }
            """
    udf = UserDefinedFunction(
        name="echo_text",
        arguments=[Argument(name="x", datatype="TEXT", default_value="'TEST VALUE'")],
        return_type=ReturnDataType(datatype="TEXT"),
        language_config=ScalaFunction(runtime_version="2.12", handler="Echo.echoText", packages=[]),
        body=func_body,
    )
    udf_handle: UserDefinedFunctionResource = user_defined_functions.create(udf)
    try:
        assert udf_handle.execute() == "TEST VALUE"
        assert udf_handle.execute([]) == "TEST VALUE"
    finally:
        udf_handle.drop(if_exists=True)


def test_execute_udf_invalid_argument_provided(user_defined_functions):
    func_body = """
              class Echo {
                def echoText(x : Int): Int = {
                  return x
                }
              }
            """
    udf = UserDefinedFunction(
        name="echo_text",
        arguments=[Argument(name="x", datatype="INT")],
        return_type=ReturnDataType(datatype="INT"),
        language_config=ScalaFunction(runtime_version="2.12", handler="Echo.echoText", packages=[]),
        body=func_body,
        comment="test_comment",
    )
    udf_handle: UserDefinedFunctionResource = user_defined_functions.create(udf)
    try:
        with pytest.raises(APIError):
            udf_handle.execute([UserDefinedFunctionArgument(name="x", datatype="INT", value="NOT AN INT")])
        with pytest.raises(InvalidArgumentsError):
            udf_handle.execute([UserDefinedFunctionArgument(name="y", datatype="INT", value=42)])
    finally:
        udf_handle.drop(if_exists=True)
