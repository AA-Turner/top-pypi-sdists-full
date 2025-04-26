import pytest

from snowflake.core.user_defined_function import (
    PythonFunction,
    ReturnDataType,
    UserDefinedFunction,
)
from tests.utils import random_string

from ...utils import ensure_snowflake_version


pytestmark = [pytest.mark.min_sf_ver("8.38.0"), pytest.mark.usefixtures("anaconda_package_available")]

@pytest.fixture(scope='session')
def user_defined_functions_extended(user_defined_functions, snowflake_version):
    ensure_snowflake_version(snowflake_version, "8.38.0")

    name_list = []
    for _ in range(5):
        name_list.append(random_string(10, 'test_user_defined_function_iter_a_'))
    for _ in range(7):
        name_list.append(random_string(10, 'test_user_defined_function_iter_b_'))
    for _ in range(3):
        name_list.append(random_string(10, 'test_user_defined_function_iter_c_'))

    for user_defined_function_name in name_list:
        user_defined_functions.create(UserDefinedFunction(
            name=user_defined_function_name,
            arguments=[],
            return_type=ReturnDataType(datatype="VARIANT"),
            language_config=PythonFunction(runtime_version="3.9", packages=[], handler="udf"),
            body="""
def udf():
    return {"key": "value"}
            """,
        ))

    try:
        yield user_defined_functions
    finally:
        for user_defined_function_name in name_list:
            user_defined_functions[f"{user_defined_function_name}()"].drop()

def test_iter_raw(user_defined_functions_extended):
    assert len(list(user_defined_functions_extended.iter())) >= 15


def test_iter_like(user_defined_functions_extended):
    assert len(list(user_defined_functions_extended.iter(like="test_user_defined_function_iter_"))) == 0
    assert len(list(user_defined_functions_extended.iter(like="test_user_defined_function_iter_a_%%"))) == 5
    assert len(list(user_defined_functions_extended.iter(like="test_user_defined_function_iter_b_%%"))) == 7
    assert len(list(user_defined_functions_extended.iter(like="test_user_defined_function_iter_c_%%"))) == 3

