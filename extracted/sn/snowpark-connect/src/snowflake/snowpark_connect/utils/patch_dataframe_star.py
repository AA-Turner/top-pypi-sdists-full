#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

"""Encode ``df["*"]`` with the source plan id, when the session opts in.

PySpark 3.5.3 sends that star as ``UnresolvedStar`` with no target, which is
the same message as ``select("*")``. The proto has no ``plan_id`` field, so
the plan id is carried in ``unparsed_target``.

The marker is sent only when the server answers
``snowpark.connect.column.scopeStarToSourceDataFrame`` with ``true``. Off
(default), ``df["*"]`` is stock PySpark, byte for byte, so a server that
predates the marker, or OSS Spark Connect, never receives it. The flag is read
once per ``df["*"]``, as a ``ConfigRequest``. It is not cached because the
session can change it at any time, including through SQL ``SET``.

Java and Scala Connect clients are out of scope. They still send a target-less
star, so ``df["*"]`` on those clients expands the whole current relation.

The thin client does not install this patch. It forwards the plan to the
remote dataframe processor, which rejects the marker until that processor
runs this server change. The standalone client package also does not ship
this module.
"""

import threading
from typing import TYPE_CHECKING

from snowflake.snowpark_connect.config import SCOPE_STAR_TO_SOURCE_DATAFRAME
from snowflake.snowpark_connect.expression.map_unresolved_star import (
    dataframe_star_target,
)
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger

if TYPE_CHECKING:
    from pyspark.sql.connect.session import SparkSession

# start_session and init_spark_session can run on different threads in one
# process. The check-then-assign on the pyspark class attribute has to be one
# critical section, or two callers can each install a different function.
_PATCH_LOCK = threading.Lock()


def _scope_star_opted_in(session: "SparkSession") -> bool:
    # A server that does not know the key answers None or raises; either way
    # it gets the stock star it understands. OSS Spark Connect raises a plain
    # gRPC error for an unknown key, so the except can't be narrower. A real
    # connection failure still surfaces on the next RPC, which runs the plan.
    try:
        value = session.conf.get(SCOPE_STAR_TO_SOURCE_DATAFRAME)
    except Exception as e:
        logger.debug(
            "Could not read %s, sending the stock df['*']: %s",
            SCOPE_STAR_TO_SOURCE_DATAFRAME,
            e,
        )
        return False
    return str(value).strip().lower() == "true"


def patch_dataframe_star() -> None:
    import pyspark.sql.connect.dataframe as df_mod
    from pyspark.sql.connect.column import Column
    from pyspark.sql.connect.expressions import UnresolvedStar

    if getattr(df_mod.DataFrame.__getitem__, "_scos_df_star", False):
        return

    with _PATCH_LOCK:
        if getattr(df_mod.DataFrame.__getitem__, "_scos_df_star", False):
            return

        original_getitem = df_mod.DataFrame.__getitem__

        def __getitem__(self, item):
            if (
                isinstance(item, str)
                and item == "*"
                and self._plan is not None
                and self._get_alias() is None
                and _scope_star_opted_in(self._session)
            ):
                return Column(
                    UnresolvedStar(
                        unparsed_target=dataframe_star_target(self._plan._plan_id)
                    )
                )
            return original_getitem(self, item)

        __getitem__.__doc__ = original_getitem.__doc__
        __getitem__._scos_df_star = True  # type: ignore[attr-defined]
        df_mod.DataFrame.__getitem__ = __getitem__
