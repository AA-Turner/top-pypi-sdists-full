import typing
from typing import Sequence
from typing import Tuple

from tecton_core import conf


if typing.TYPE_CHECKING:
    import snowflake.snowpark


def register_temp_views_or_tables(views: Sequence[Tuple[str, str]], snowpark_session: "snowflake.snowpark.Session"):
    for view_name, view_sql in views:
        # Using temporary tables provides better performance than temporary views
        temp_object = conf.get_or_none("QUERYTREE_SHORT_SQL_TYPE")
        if not temp_object or temp_object.upper() not in ["VIEW", "TABLE"]:
            msg = f" {temp_object} is not a valid setting for QUERYTREE_SHORT_SQL_TYPE. Must be 'view' or 'table'."
            raise Exception(msg)
        snowpark_session.sql(f"CREATE OR REPLACE TEMPORARY {temp_object.upper()} {view_name} AS ({view_sql})").collect()
