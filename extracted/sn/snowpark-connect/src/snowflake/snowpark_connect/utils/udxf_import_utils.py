#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from snowflake import snowpark
from snowflake.snowpark_connect.config import global_config
from snowflake.snowpark_connect.utils.spark_session_cache import get_spark_session_cache


def get_python_udxf_import_files(session: snowpark.Session) -> str:
    config_imports = global_config.get(
        "snowpark.connect.udf.python.imports",
        global_config.get("snowpark.connect.udf.imports", ""),
    )
    config_imports = (
        [x.strip() for x in config_imports.strip("[] ").split(",") if x.strip()]
        if config_imports
        else []
    )
    artifacts_store = get_spark_session_cache().artifacts_store
    imports = {
        *artifacts_store.get_python_files(),
        *artifacts_store.get_import_files(),
        *config_imports,
    }

    return ",".join([file for file in imports if file])
