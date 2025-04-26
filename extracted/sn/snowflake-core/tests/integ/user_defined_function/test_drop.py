import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.user_defined_function import (
    PythonFunction,
    ReturnDataType,
    UserDefinedFunction,
)
from tests.utils import random_string


pytestmark = [pytest.mark.min_sf_ver("8.38.0"), pytest.mark.usefixtures("anaconda_package_available")]

def test_drop(user_defined_functions):
    user_defined_function_name = random_string(10, 'test_drop_user_defined_function_')

    user_defined_function_handle = user_defined_functions.create(UserDefinedFunction(
        name=user_defined_function_name,
        arguments=[],
        return_type=ReturnDataType(datatype="VARIANT"),
        language_config=PythonFunction(runtime_version="3.9", packages=[], handler="udf"),
        body="""
def udf():
    return {"key": "value"}
            """,
    ))

    user_defined_function_handle.fetch()

    user_defined_function_handle.drop()

    with pytest.raises(
        NotFoundError
    ):
        user_defined_function_handle.fetch()

    with pytest.raises(
        NotFoundError
    ):
        user_defined_function_handle.drop()

    user_defined_function_handle.drop(if_exists=True)
