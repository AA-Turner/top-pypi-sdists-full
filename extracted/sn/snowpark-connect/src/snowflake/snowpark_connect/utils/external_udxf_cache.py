#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

from snowflake.snowpark import Session
from snowflake.snowpark_connect.utils.concurrent import SynchronizedDict


def init_external_udxf_cache(session: Session) -> None:
    session.external_udfs_cache = SynchronizedDict()
    session.external_udtfs_cache = SynchronizedDict()


def clear_external_udxf_cache(session: Session) -> None:
    session.external_udfs_cache.clear()
    session.external_udtfs_cache.clear()


def get_external_udf_from_cache(hash: str):
    return Session.get_active_session().external_udfs_cache.get(hash)


def cache_external_udf(hash: int, udf):
    Session.get_active_session().external_udfs_cache[hash] = udf


def clear_external_udtf_cache(session: Session) -> None:
    session.external_udtfs_cache.clear()


def get_external_udtf_from_cache(hash: int):
    return Session.get_active_session().external_udtfs_cache.get(hash)


def cache_external_udtf(hash: int, udf):
    Session.get_active_session().external_udtfs_cache[hash] = udf
