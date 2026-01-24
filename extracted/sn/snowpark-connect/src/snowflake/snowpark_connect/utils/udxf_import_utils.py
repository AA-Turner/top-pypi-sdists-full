#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from snowflake import snowpark
from snowflake.snowpark_connect.config import global_config


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
    imports = {*session._python_files, *session._import_files, *config_imports}

    return ",".join([file for file in imports if file])
