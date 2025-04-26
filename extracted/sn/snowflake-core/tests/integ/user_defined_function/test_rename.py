import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.schema import Schema
from snowflake.core.user_defined_function import (
    PythonFunction,
    ReturnDataType,
    UserDefinedFunction,
)
from tests.utils import random_string


pytestmark = [pytest.mark.min_sf_ver("8.38.0"), pytest.mark.usefixtures("anaconda_package_available")]

def test_rename(user_defined_functions):
    user_defined_function_name = random_string(10, 'test_original_user_defined_function_')
    user_defined_function_other_name = random_string(10, 'test_other_user_defined_function_')

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

    try:
        user_defined_function_handle.fetch()

        user_defined_function_handle.rename(user_defined_function_other_name)

        assert user_defined_function_handle.fetch().name.upper() == user_defined_function_other_name.upper()

        with pytest.raises(
            NotFoundError
        ):
            user_defined_functions[f"{user_defined_function_name}()"].fetch()

        with pytest.raises(
            NotFoundError
        ):
            user_defined_functions[f"{user_defined_function_name}()"].rename(user_defined_function_other_name)

        user_defined_functions[f"{user_defined_function_name}()"].rename(user_defined_function_other_name,
                                                                         if_exists=True)
        user_defined_functions[f"{user_defined_function_other_name}()"].fetch()
    finally:
        # This UDF has to be existed
        user_defined_function_handle.drop()

def test_relocate_schema(user_defined_functions, temp_schema):
    user_defined_function_name = random_string(10, 'test_original_user_defined_function_')
    user_defined_function_other_name = random_string(10, 'test_other_user_defined_function_')

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

    try:
        user_defined_function_handle.fetch()

        user_defined_function_handle.rename(
            user_defined_function_other_name,
            target_schema=temp_schema.name
        )

        assert user_defined_function_handle.fetch().name.upper() == user_defined_function_other_name.upper()
        assert user_defined_function_handle.fetch().schema_name.upper() == temp_schema.name.upper()
        assert user_defined_function_handle.collection.schema.name.upper() == temp_schema.name.upper()

        with pytest.raises(
            NotFoundError
        ):
            user_defined_functions[f"{user_defined_function_name}()"].fetch()

        with pytest.raises(
            NotFoundError
        ):
            user_defined_functions[f"{user_defined_function_name}()"].rename(user_defined_function_other_name)

        user_defined_functions[f"{user_defined_function_name}()"].rename(user_defined_function_other_name,
                                                                         if_exists=True)
        temp_schema.user_defined_functions[f"{user_defined_function_other_name}()"].fetch()
    finally:
        # This UDF has to be existed
        user_defined_function_handle.drop()

def test_relocate_database(user_defined_functions, temp_db):
    temp_schema_name = random_string(10, 'test_temp_schema_')

    created_schema = temp_db.schemas.create(
        Schema(name=temp_schema_name)
    )

    try:
        user_defined_function_name = random_string(10, 'test_original_user_defined_function_')
        user_defined_function_other_name = random_string(10, 'test_other_user_defined_function_')

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

        try:
            user_defined_function_handle.fetch()

            user_defined_function_handle.rename(
                user_defined_function_other_name,
                target_schema=created_schema.name,
                target_database=temp_db.name
            )

            assert user_defined_function_handle.fetch().name.upper() == user_defined_function_other_name.upper()
            assert user_defined_function_handle.fetch().schema_name.upper() == created_schema.name.upper()
            assert user_defined_function_handle.fetch().database_name.upper() == temp_db.name.upper()
            assert user_defined_function_handle.collection.database.name.upper() == temp_db.name.upper()
            assert user_defined_function_handle.collection.schema.name.upper() == created_schema.name.upper()

            with pytest.raises(
                NotFoundError
            ):
                user_defined_functions[f"{user_defined_function_name}()"].fetch()

            with pytest.raises(
                NotFoundError
            ):
                user_defined_functions[f"{user_defined_function_name}()"].rename(user_defined_function_other_name)

            user_defined_functions[f"{user_defined_function_name}()"].rename(user_defined_function_other_name,
                                                                             if_exists=True)
            created_schema.user_defined_functions[f"{user_defined_function_other_name}()"].fetch()
        finally:
            # This UDF has to be existed
            user_defined_function_handle.drop()
    finally:
        created_schema.drop()
