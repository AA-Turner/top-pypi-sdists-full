#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from collections import defaultdict

from snowflake.connector.errors import ProgrammingError
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.relation.catalogs import CATALOGS, SNOWFLAKE_CATALOG
from snowflake.snowpark_connect.relation.catalogs.abstract_spark_catalog import (
    AbstractSparkCatalog,
)
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session

CURRENT_CATALOG = SNOWFLAKE_CATALOG
CURRENT_CATALOG_NAME: str | None = "spark_catalog"
CATALOG_TEMP_OBJECTS: defaultdict[
    str | None, set[tuple[str | None, str | None, str]]
] = defaultdict(set)


def get_current_catalog() -> AbstractSparkCatalog:
    return CURRENT_CATALOG


def set_current_catalog(catalog_name: str | None) -> AbstractSparkCatalog:
    global CURRENT_CATALOG_NAME

    # Validate input parameters to match PySpark behavior
    if catalog_name is None:
        exception = ValueError("Catalog name cannot be None")
        attach_custom_error_code(exception, ErrorCodes.INVALID_INPUT)
        raise exception
    if catalog_name == "":
        exception = ValueError(
            "Catalog '' plugin class not found: spark.sql.catalog. is not defined"
        )
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    CURRENT_CATALOG_NAME = catalog_name
    if catalog_name in CATALOGS:
        return CATALOGS[catalog_name]

    sf_catalog = get_or_create_snowpark_session().catalog
    try:
        sf_catalog.setCurrentDatabase(catalog_name if catalog_name is not None else "")
        return get_current_catalog()
    except ProgrammingError as e:
        exception = Exception(
            f"Catalog '{catalog_name}' plugin class not found: spark.sql.catalog.{catalog_name} is not defined"
        )
        attach_custom_error_code(exception, ErrorCodes.INSUFFICIENT_INPUT)
        raise exception from e


def _get_current_temp_objects() -> set[tuple[str | None, str | None, str]]:
    return CATALOG_TEMP_OBJECTS[CURRENT_CATALOG_NAME]
