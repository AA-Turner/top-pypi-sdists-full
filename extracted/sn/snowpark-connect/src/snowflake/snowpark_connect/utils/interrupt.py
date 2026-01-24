#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import concurrent.futures

from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session


def interrupt_all_queries() -> list[str]:
    snowpark_session = get_or_create_snowpark_session()

    sql = _build_sql_for_select_running_queries()
    running_queries = snowpark_session.sql(sql).collect()

    snowpark_session.cancel_all()

    return [row[0] for row in running_queries]


def interrupt_queries_with_tag(tag: str) -> list[str]:
    snowpark_session = get_or_create_snowpark_session()

    sql = _build_sql_for_select_running_queries(tag=tag)
    running_queries_with_tag_result = [
        row[0] for row in snowpark_session.sql(sql).collect()
    ]

    # Final list of canceled queries might be slightly smaller than running_queries_with_tag_result, because
    # some jobs can finish in the meantime
    canceled_query_ids = []

    max_workers = max(1, min(32, len(running_queries_with_tag_result)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as exc:
        futures = []

        for query_id in running_queries_with_tag_result:
            future = exc.submit(
                lambda query_id_: (
                    snowpark_session.sql(
                        f"SELECT SYSTEM$CANCEL_QUERY('{query_id_}')"
                    ).collect(),
                    query_id_,
                ),
                query_id_=query_id,
            )
            futures.append(future)

        for future in futures:
            cancel_query_result, query_id = future.result()

            if _is_cancel_query_successful(cancel_query_result[0][0]):
                canceled_query_ids.append(query_id)

    return canceled_query_ids


def interrupt_query(query_id: str) -> list[str]:
    snowpark_session = get_or_create_snowpark_session()

    cancel_result = snowpark_session.sql(
        f"SELECT SYSTEM$CANCEL_QUERY('{query_id}')"
    ).collect()

    return [query_id] if _is_cancel_query_successful(cancel_result[0][0]) else []


def _build_sql_for_select_running_queries(tag: str | None = None) -> str:
    sql = "select query_id"
    sql += " from table(information_schema.query_history_by_session(include_client_generated_statement => true, result_limit => 10000))"
    sql += " where execution_status = 'RUNNING'"

    if tag:
        sql += f" and array_contains('{tag}', split(query_tag, ',')::array(string))"

    sql_escaped_as_str = sql.replace("'", "\\'")

    # Filter out the currently running query_history_by_session query from the result
    sql += f" and query_text not like '{sql_escaped_as_str}%'"

    return sql


def _is_cancel_query_successful(response_message: str) -> bool:
    return response_message.endswith("terminated.")
