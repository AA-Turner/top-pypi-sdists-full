#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import base64
import hashlib
import inspect
import json
import sys
from collections import namedtuple
from typing import Any

import pyspark.sql.connect.proto.expressions_pb2 as expressions_proto
import pyspark.sql.connect.proto.relations_pb2 as relation_proto

import snowflake.snowpark_connect.tcm as tcm
from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.analyzer_utils import unquote_if_quoted
from snowflake.snowpark.types import DataType, StructType, _parse_datatype_json_value
from snowflake.snowpark_connect.config import is_force_create_sproc_enabled
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.type_mapping import proto_to_snowpark_type
from snowflake.snowpark_connect.utils import pandas_udtf_utils, udtf_utils
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

CREATE_UDTF_SPROC_NAME_PREFIX = "__SC_BUILD_IN_CREATE_UDTF"
CREATE_PD_UDTF_SPROC_NAME_PREFIX = "__SC_BUILD_IN_CREATE_PD_UDTF"
SnowparkUDTF = namedtuple("SnowparkUDTF", ["name", "output_schema", "input_types"])

CREATE_APPLY_UDTF_FUNCTION_NAME_PREFIX = "__SC_BUILD_IN_CREATE_APPLY_UDTF"


def udtf_check(
    udtf_proto: relation_proto.CommonInlineUserDefinedTableFunction,
) -> None:
    if udtf_proto.WhichOneof("function") != "python_udtf":
        exception = ValueError(f"Not python udtf {udtf_proto.function}")
        attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
        raise exception


def require_creating_udtf_in_sproc(
    udtf_proto: relation_proto.CommonInlineUserDefinedTableFunction,
) -> bool:
    """
    Determine if a UDTF should be created in a stored procedure.

    Returns True in the following scenarios:
    * Testing: When the `snowpark.connect.test.force_create_sproc` config is enabled.
    * TCM Mode: For security isolation.
    * Version Compatibility: If the Python version specified in the UDTF metadata
      does not match the current runtime version.
    """
    return (
        is_force_create_sproc_enabled()
        or tcm.TCM_MODE
        or (
            udtf_proto.WhichOneof("function") == "python_udtf"
            and udtf_proto.python_udtf.python_ver is not None
            and f"{sys.version_info.major}.{sys.version_info.minor}"
            != udtf_proto.python_udtf.python_ver
        )
    )


def create_udtf_in_sproc(
    session: snowpark.Session,
    udtf_proto: relation_proto.CommonInlineUserDefinedTableFunction,
    expected_types: list[tuple[str, Any]],
    output_schema: StructType,
    packages: str,
    imports: str,
    is_arrow_enabled: bool,
    is_spark_compatible_udtf_mode_enabled: bool,
    called_from: str,
    resource_constraint: dict[str, str] | None = None,
) -> SnowparkUDTF | str:
    sproc_name = _get_or_create_udtf_sproc_helper(
        session,
        udtf_proto.python_udtf.python_ver,
    )
    udtf_proto_encoded = base64.b64encode(udtf_proto.SerializeToString()).decode(
        "ascii"
    )

    expected_types_json_str = json.dumps(expected_types) if expected_types else None
    output_schema_json_str = json.dumps(output_schema.json_value())
    # resource_constraint is passed from caller (captured on SAS server side)
    resource_constraint_json_str = (
        None if resource_constraint is None else json.dumps(resource_constraint)
    )
    sproc_res = session.call(
        sproc_name,
        udtf_proto_encoded,
        expected_types_json_str,
        output_schema_json_str,
        packages,
        imports,
        is_arrow_enabled,
        is_spark_compatible_udtf_mode_enabled,
        called_from,
        resource_constraint_json_str,
    )

    udtf_attr = json.loads(sproc_res)
    if "error" in udtf_attr:
        return udtf_attr["error"]
    return SnowparkUDTF(
        name=udtf_attr["name"],
        input_types=[_parse_datatype_json_value(t) for t in udtf_attr["input_types"]],
        output_schema=output_schema,
    )


def _get_or_create_udtf_sproc_helper(
    session: snowpark.Session,
    python_version: str = f"{sys.version_info.major}.{sys.version_info.minor}",
) -> str:
    """
    This helper method will get or create a sproc in targeted python version to create the python UDTF. The sproc's
    return value is a json string containing the UDTF's name, input types, and, return type.
    """
    sproc_name = f"{CREATE_UDTF_SPROC_NAME_PREFIX}_{python_version.replace('.', '_')}"
    if sproc_name in session._sprocs:
        return sproc_name

    inline_udtf_utils_py_code = inspect.getsource(udtf_utils)

    create_udtf_sproc_sql = f"""
CREATE OR REPLACE TEMPORARY PROCEDURE {sproc_name}(
    base64_str VARCHAR,
    expected_types_json_str VARCHAR,
    output_schema_json_str VARCHAR,
    packages VARCHAR,
    imports VARCHAR,
    is_arrow_enabled BOOLEAN,
    is_spark_compatible_udtf_mode_enabled BOOLEAN,
    called_from VARCHAR,
    resource_constraint_json VARCHAR
)
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '{python_version}'
PACKAGES = ('pyspark>=3.5.0,<4', 'cloudpickle', 'snowflake-snowpark-python==1.32.0', 'grpcio>=1.48.1', 'snowflake-telemetry-python')
HANDLER = 'create'
EXECUTE AS CALLER
AS $$
import cloudpickle
import base64
from pyspark.sql.connect.proto.relations_pb2 import CommonInlineUserDefinedTableFunction
import json
from snowflake.snowpark.types import *
from typing import Optional
from snowflake.snowpark.types import _parse_datatype_json_value

{inline_udtf_utils_py_code}

def parse_types(types_json_str) -> Optional[list[DataType]]:
    if types_json_str is None:
        return None
    return json.loads(types_json_str)

def parse_resource_constraint(resource_constraint_json) -> Optional[dict[str, str]]:
    if resource_constraint_json is None:
        return None
    return json.loads(resource_constraint_json)

def create(session, b64_str, expected_types_json_str, output_schema_json_str, packages, imports, is_arrow_enabled, is_spark_compatible_udtf_mode_enabled, called_from, resource_constraint_json):
    session._use_scoped_temp_objects = False
    import snowflake.snowpark.context as context
    context._use_structured_type_semantics = True
    context._is_snowpark_connect_compatible_mode = True

    restored_bytes = base64.b64decode(b64_str.encode('ascii'))
    udtf_proto = CommonInlineUserDefinedTableFunction()
    udtf_proto.ParseFromString(restored_bytes)

    expected_types = parse_types(expected_types_json_str)
    output_schema = StructType.fromJson(json.loads(output_schema_json_str))

    udtf_or_error = create_udtf(
        session,
        udtf_proto,
        expected_types,
        output_schema,
        packages,
        imports,
        is_arrow_enabled,
        is_spark_compatible_udtf_mode_enabled,
        called_from,
        resource_constraint=parse_resource_constraint(resource_constraint_json),
    )
    if isinstance(udtf_or_error, str):
        return json.dumps({{"error": udtf_or_error}})
    udtf = udtf_or_error
    return json.dumps({{"name": udtf.name, "input_types": [t.json_value() for t in udtf._input_types]}})
$$;
"""
    session.sql(create_udtf_sproc_sql).collect()
    session._sprocs.add(sproc_name)
    logger.info(f"Procedure {sproc_name} created")
    return sproc_name


def create_pandas_udtf_in_sproc(
    udf_proto: relation_proto.CommonInlineUserDefinedTableFunction,
    spark_column_names: list[str],
    input_schema: StructType | None = None,
    return_schema: StructType | None = None,
    udtf_packages: str = "",
    udtf_imports: str = "",
) -> str:
    session = get_or_create_snowpark_session()
    sproc_name = _get_or_create_pandas_udtf_sproc_helper(
        session,
        udf_proto.python_udf.python_ver,
    )
    udf_proto_encoded = base64.b64encode(udf_proto.SerializeToString()).decode("ascii")
    spark_column_names_json_str = json.dumps(spark_column_names)
    input_schema_json_str = (
        json.dumps(input_schema.json_value()) if input_schema else None
    )
    return_schema_json_str = (
        json.dumps(return_schema.json_value()) if return_schema else None
    )

    return session.call(
        sproc_name,
        udf_proto_encoded,
        spark_column_names_json_str,
        input_schema_json_str,
        return_schema_json_str,
        udtf_packages,
        udtf_imports,
    )


def _get_or_create_pandas_udtf_sproc_helper(
    session: snowpark.Session,
    python_version: str = f"{sys.version_info.major}.{sys.version_info.minor}",
) -> str:
    """
    This helper method will get or create a sproc in targeted python version to create the python UDTF. The sproc's
    return value is a json string containing the UDTF's name, input types, and, return type.
    """
    sproc_name = (
        f"{CREATE_PD_UDTF_SPROC_NAME_PREFIX}_{python_version.replace('.', '_')}"
    )
    if sproc_name in session._sprocs:
        return sproc_name

    inline_udtf_utils_py_code = inspect.getsource(pandas_udtf_utils)

    create_udtf_sproc_sql = f"""
CREATE OR REPLACE TEMPORARY PROCEDURE {sproc_name}(
    base64_str VARCHAR,
    spark_column_names_json_str VARCHAR,
    input_schema_json_str VARCHAR,
    return_schema_json_str VARCHAR,
    udtf_packages VARCHAR,
    udtf_imports VARCHAR
)
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '{python_version}'
PACKAGES = ('pyspark>=3.5.0,<4', 'cloudpickle', 'snowflake-snowpark-python', 'grpcio>=1.48.1', 'pandas', 'pyarrow', 'snowflake-telemetry-python')
HANDLER = 'create'
EXECUTE AS CALLER
AS $$
import cloudpickle
import base64
from pyspark.sql.connect.proto.expressions_pb2 import CommonInlineUserDefinedFunction
import json
from snowflake.snowpark.types import *
from typing import Optional
from snowflake.snowpark.types import _parse_datatype_json_value

{inline_udtf_utils_py_code}

def create(session, b64_str, spark_column_names_json_str, input_schema_json_str, return_schema_json_str, udtf_packages, udtf_imports):
    session._use_scoped_temp_objects = False
    import snowflake.snowpark.context as context
    context._use_structured_type_semantics = True
    context._is_snowpark_connect_compatible_mode = True

    restored_bytes = base64.b64decode(b64_str.encode('ascii'))
    udf_proto = CommonInlineUserDefinedFunction()
    udf_proto.ParseFromString(restored_bytes)

    if not input_schema_json_str:
        raise ValueError("Input schema is required for pandas UDTF.")
    if not return_schema_json_str:
        raise ValueError("Return schema is required for pandas UDTF.")

    spark_column_names = json.loads(spark_column_names_json_str)
    input_schema = StructType.fromJson(json.loads(input_schema_json_str))
    return_schema = StructType.fromJson(json.loads(return_schema_json_str))

    map_in_arrow = udf_proto.WhichOneof("function") == "python_udf" and udf_proto.python_udf.eval_type == 207
    if map_in_arrow:
        map_udtf = create_pandas_udtf_with_arrow(
            udf_proto, spark_column_names, input_schema, return_schema, udtf_packages, udtf_imports
        )
    else:
        map_udtf = create_pandas_udtf(
            udf_proto, spark_column_names, input_schema, return_schema, udtf_packages, udtf_imports
        )
    return map_udtf.name
$$;
"""
    session.sql(create_udtf_sproc_sql).collect()
    session._sprocs.add(sproc_name)
    logger.info(f"Procedure {sproc_name} created")
    return sproc_name


def _get_or_create_apply_udtf_table_function_helper(
    session: snowpark.Session, python_version: str
) -> str:
    """
    This helper method will get or create a sproc in targeted python version to create the python UDTF. The sproc's
    return value is a json string containing the UDTF's name, input types, and, return type.
    """
    create_apply_udtf_name = (
        f"{CREATE_APPLY_UDTF_FUNCTION_NAME_PREFIX}_{python_version.replace('.', '_')}"
    )
    if create_apply_udtf_name in session._sprocs:
        return create_apply_udtf_name

    # Function takes a b64 encoded picked func and generates snowflake function of the ApplyInPandas wrapper on the
    # user defined python func.
    create_apply_udtf_sproc_sql = f"""
CREATE OR REPLACE TEMPORARY PROCEDURE {create_apply_udtf_name}(
    func_info_json VARCHAR
)
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '{python_version}'
PACKAGES = ('pyspark>=3.5.0,<4', 'cloudpickle', 'snowflake-snowpark-python', 'grpcio>=1.48.1', 'pandas', 'pyarrow', 'numpy', 'snowflake-telemetry-python')
HANDLER = 'create'
EXECUTE AS CALLER
AS $$
import base64
import cloudpickle
import inspect
import json
import pandas

from snowflake.snowpark.types import *
from typing import Optional
from snowflake.snowpark.types import _parse_datatype_json_value
from pyspark.serializers import CloudPickleSerializer


def process_dependencies_string_array(input_str: str) -> list[str]:
    if input_str and len(input_str) > 0:
        return [i.strip() for i in input_str.strip("[] ").split(",") if i.strip()]
    return []


def create(session, func_info_json):
    session._use_scoped_temp_objects = False
    import snowflake.snowpark.context as context
    context._use_structured_type_semantics = True
    context._is_snowpark_connect_compatible_mode = True

    func_info = json.loads(func_info_json)

    python_func = func_info.get("python_func", None)
    key_columns = func_info.get("key_columns", None)
    original_columns = func_info.get("original_columns", None)
    input_schema = func_info.get("input_schema", None)
    output_schema = func_info.get("output_schema", None)
    name = func_info.get("name", None)
    resource_constraint = func_info.get("resource_constraint", None)
    udtf_packages = func_info.get("udtf_packages", "")
    udtf_imports = func_info.get("udtf_imports", "")

    func_bytes = base64.b64decode(python_func.encode('ascii'))

    func, _ = CloudPickleSerializer().loads(func_bytes)

    signature = inspect.signature(func)
    parameters = signature.parameters
    if len(parameters) == 2:
        key_columns = json.loads(key_columns)
    else:
        key_columns = None

    if original_columns is not None:
        original_columns = json.loads(original_columns)

    input_types = []
    input_names = []
    if input_schema is not None:
        input_schema = StructType.from_json(input_schema)
        input_types = [input_type.datatype for input_type in input_schema]
        input_names = [input_type.name for input_type in input_schema]

    if output_schema is not None:
        output_schema = StructType.from_json(output_schema)

    class _ApplyInPandas:
        def end_partition(self, pdf: pandas.DataFrame) -> pandas.DataFrame:
            if key_columns is not None:
                import numpy as np
                key_list = [pdf[key].iloc[0] for key in key_columns]
                numpy_array = np.array(key_list)
                keys = tuple(numpy_array)
            if original_columns is not None:
                pdf.columns = original_columns
            if key_columns is not None:
                return func(keys, pdf)
            return func(pdf)

    _ApplyInPandas.end_partition._sf_vectorized_input = pandas.DataFrame

    _apply_in_pandas_udtf = session.udtf.register(
        handler=_ApplyInPandas,
        output_schema=output_schema,
        input_types=input_types,
        input_names=input_names,
        resource_constraint=resource_constraint,
        packages=process_dependencies_string_array(udtf_packages) + ["pandas"],
        imports=process_dependencies_string_array(udtf_imports)
    )

    return _apply_in_pandas_udtf.name
$$;
"""
    session.sql(create_apply_udtf_sproc_sql).collect()
    session._sprocs.add(create_apply_udtf_name)
    return create_apply_udtf_name


def create_apply_udtf_in_sproc(
    udf_proto: expressions_proto.CommonInlineUserDefinedFunction,
    function_name: str,
    group_by_columns: list[snowpark.Column],
    original_columns: list[str] | None = None,
    input_schema: StructType | None = None,
    udtf_packages: str = "",
    udtf_imports: str = "",
) -> tuple[str, list[DataType], StructType]:
    session = get_or_create_snowpark_session()
    create_apply_sproc_name = _get_or_create_apply_udtf_table_function_helper(
        session,
        udf_proto.python_ver,
    )

    udtf_base64 = base64.b64encode(udf_proto.command).decode("ascii")

    input_schema = input_schema.json_value()
    output_schema = proto_to_snowpark_type(udf_proto.output_type).json_value()

    key_columns = [unquote_if_quoted(col.get_name()) for col in group_by_columns]

    from snowflake.snowpark_connect.utils.udf_utils import _get_resource_constraint

    apply_udtf_info = {
        "python_func": udtf_base64,
        "key_columns": json.dumps(key_columns),
        "original_columns": json.dumps(original_columns),
        "input_schema": input_schema,
        "output_schema": output_schema,
        "name": function_name,
        "resource_constraint": _get_resource_constraint(),
        "udtf_packages": udtf_packages,
        "udtf_imports": udtf_imports,
    }

    apply_udtf_name = session.call(
        create_apply_sproc_name,
        json.dumps(apply_udtf_info),
    )

    return apply_udtf_name


CREATE_COGROUP_UDTF_FUNCTION_NAME_PREFIX = "__SC_BUILD_IN_CREATE_COGROUP_UDTF"


def _get_or_create_cogroup_udtf_table_function_helper(
    session: snowpark.Session, python_version: str
) -> str:
    """
    This helper method will get or create a sproc in targeted python version to create the cogroup
    python UDTF. The sproc's return value is the UDTF's name.
    """
    create_cogroup_udtf_name = (
        f"{CREATE_COGROUP_UDTF_FUNCTION_NAME_PREFIX}_{python_version.replace('.', '_')}"
    )
    if create_cogroup_udtf_name in session._sprocs:
        return create_cogroup_udtf_name

    inline_udtf_utils_py_code = inspect.getsource(pandas_udtf_utils)

    create_cogroup_udtf_sproc_sql = f"""
CREATE OR REPLACE TEMPORARY PROCEDURE {create_cogroup_udtf_name}(
    func_info_json VARCHAR
)
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '{python_version}'
PACKAGES = ('pyspark>=3.5.0,<4', 'cloudpickle', 'snowflake-snowpark-python', 'grpcio>=1.48.1', 'pandas', 'pyarrow', 'numpy')
HANDLER = 'create'
EXECUTE AS CALLER
AS $$
import base64
import json
import pandas as pd

from snowflake.snowpark.types import *
from pyspark.serializers import CloudPickleSerializer
import snowflake.snowpark.functions as snowpark_fn

{inline_udtf_utils_py_code}

def create(session, func_info_json):
    session._use_scoped_temp_objects = False
    import snowflake.snowpark.context as context
    context._use_structured_type_semantics = True
    context._is_snowpark_connect_compatible_mode = True

    func_info = json.loads(func_info_json)

    python_func = func_info.get("python_func", None)
    input1_columns = json.loads(func_info.get("input1_columns", "[]"))
    input2_columns = json.loads(func_info.get("input2_columns", "[]"))
    output_schema_json = func_info.get("output_schema", None)
    output_column_original_names = json.loads(func_info.get("output_column_original_names", "[]"))
    name = func_info.get("name", None)
    udtf_packages = func_info.get("udtf_packages", "")
    udtf_imports = func_info.get("udtf_imports", "")

    func_bytes = base64.b64decode(python_func.encode('ascii'))
    func, _ = CloudPickleSerializer().loads(func_bytes)

    if output_schema_json is not None:
        from snowflake.snowpark.types import _parse_datatype_json_value
        output_schema = StructType([
            StructField(
                f["name"],
                _parse_datatype_json_value(f["type"]),
                f["nullable"],
                _is_column=False,
            )
            for f in output_schema_json["fields"]
        ])
        output_column_names = [f.name for f in output_schema.fields]
    else:
        output_schema = StructType()
        output_column_names = []

    CoGroupPandasUDTF = get_cogroup_pandas_udtf(
        func,
        input1_columns,
        input2_columns,
        output_column_names,
        output_column_original_names,
    )

    _cogroup_pandas_udtf = snowpark_fn.pandas_udtf(
        CoGroupPandasUDTF,
        output_schema=PandasDataFrameType(
            [field.datatype for field in output_schema.fields],
            [field.name for field in output_schema.fields],
        ),
        input_types=[PandasDataFrameType([VariantType(), IntegerType()])],
        input_names=["__SC_COGROUP_VALUE__", "__SC_COGROUP_SOURCE__"],
        name=name,
        replace=True,
        packages=process_udtf_packages(udtf_packages, custom_packages=["pandas"]),
        imports=process_dependencies_string_array(udtf_imports),
        is_permanent=False,
    )

    return _cogroup_pandas_udtf.name
$$;
"""
    session.sql(create_cogroup_udtf_sproc_sql).collect()
    session._sprocs.add(create_cogroup_udtf_name)
    return create_cogroup_udtf_name


def create_cogroup_udtf_in_sproc(
    udtf_proto: expressions_proto.CommonInlineUserDefinedFunction,
    input1_columns: list[str],
    input2_columns: list[str],
    output_schema: StructType,
    udtf_packages: str,
    udtf_imports: str,
) -> str:
    """
    This is used when the local Python version doesn't match the UDF's Python version,
    or when running in TCM mode (security reasons)
    """
    session = get_or_create_snowpark_session()
    create_cogroup_sproc_name = _get_or_create_cogroup_udtf_table_function_helper(
        session,
        udtf_proto.python_udf.python_ver,
    )

    udtf_base64 = base64.b64encode(udtf_proto.python_udf.command).decode("ascii")
    udtf_name = (
        "cogroup_pandas_udtf_" + hashlib.md5(udtf_proto.python_udf.command).hexdigest()
    )

    output_column_original_names = [
        field.original_column_identifier for field in output_schema.fields
    ]

    cogroup_udtf_info = {
        "python_func": udtf_base64,
        "input1_columns": json.dumps(input1_columns),
        "input2_columns": json.dumps(input2_columns),
        "output_schema": output_schema.json_value(),
        "output_column_original_names": json.dumps(output_column_original_names),
        "name": udtf_name,
        "udtf_packages": udtf_packages,
        "udtf_imports": udtf_imports,
    }

    cogroup_udtf_name = session.call(
        create_cogroup_sproc_name,
        json.dumps(cogroup_udtf_info),
    )

    return cogroup_udtf_name
