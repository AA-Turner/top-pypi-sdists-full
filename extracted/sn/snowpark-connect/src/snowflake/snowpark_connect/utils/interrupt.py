#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import concurrent.futures

from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session


def interrupt_all_queries() -> list[str]:
    snowpark_session = get_or_create_snowpark_session()

    sql, params = _build_sql_for_select_running_queries()
    running_queries = snowpark_session.sql(sql, params=params).collect()

    snowpark_session.cancel_all()

    return [row[0] for row in running_queries]


def interrupt_queries_with_tag(tag: str) -> list[str]:
    snowpark_session = get_or_create_snowpark_session()

    sql, params = _build_sql_for_select_running_queries(tag=tag)
    running_queries_with_tag_result = [
        row[0] for row in snowpark_session.sql(sql, params=params).collect()
    ]

    # Final list of canceled queries might be slightly smaller than running_queries_with_tag_result, because
    # some jobs can finish in the meantime
    canceled_query_ids = []

    max_workers = max(1, min(32, len(running_queries_with_tag_result)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as exc:
        futures = [
            exc.submit(_cancel_query, snowpark_session, query_id)
            for query_id in running_queries_with_tag_result
        ]

        for future in futures:
            canceled_query_id = future.result()
            if canceled_query_id is not None:
                canceled_query_ids.append(canceled_query_id)

    return canceled_query_ids


def interrupt_query(query_id: str) -> list[str]:
    snowpark_session = get_or_create_snowpark_session()

    canceled_query_id = _cancel_query(snowpark_session, query_id)

    return [canceled_query_id] if canceled_query_id is not None else []


def _cancel_query(snowpark_session, query_id: str) -> str | None:
    cancel_result = snowpark_session.sql(
        "SELECT SYSTEM$CANCEL_QUERY(?)", params=[query_id]
    ).collect()

    return query_id if _is_cancel_query_successful(cancel_result[0][0]) else None


def _build_sql_for_select_running_queries(
    tag: str | None = None,
) -> tuple[str, list[str]]:
    sql = "select query_id"
    sql += " from table(information_schema.query_history_by_session(include_client_generated_statement => true, result_limit => 10000))"
    sql += " where execution_status = 'RUNNING'"

    params: list[str] = []
    if tag:
        sql += " and array_contains(?, split(query_tag, ',')::array(string))"
        params.append(tag)

    sql_escaped_as_str = sql.replace("'", "\\'")

    # Filter out the currently running query_history_by_session query from the result
    sql += f" and query_text not like '{sql_escaped_as_str}%'"

    return sql, params


def _is_cancel_query_successful(response_message: str) -> bool:
    return response_message.endswith("terminated.")
