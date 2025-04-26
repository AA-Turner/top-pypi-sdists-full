import datetime

from unittest.mock import Mock

import pytest

from snowflake.core.task.context import TaskContext


@pytest.mark.snowpark
def test_task_context(fake_root):
    from snowflake.snowpark.exceptions import SnowparkSQLException
    task_context = TaskContext(fake_root)
    mock_result_str = Mock()

    def side_effect_collect_str():
        return [["abc"]]
    mock_result_str.collect.side_effect = side_effect_collect_str
    mock_result_datetime = Mock()

    def side_effect_collect_datetime():
        return [[datetime.datetime(2020, 1, 1)]]

    mock_result_datetime.collect.side_effect = side_effect_collect_datetime
    mock_sql_result = {
        "select to_char(system$task_runtime_info('CURRENT_ROOT_TASK_NAME'))": mock_result_str,
        "select to_char(system$task_runtime_info('CURRENT_ROOT_TASK_UUID'))": mock_result_str,
        "select to_char(system$task_runtime_info('LAST_SUCCESSFUL_TASK_GRAPH_RUN_GROUP_ID'))": mock_result_str,
        "select to_char(system$task_runtime_info('CURRENT_TASK_GRAPH_RUN_GROUP_ID'))": mock_result_str,
        "select to_timestamp(system$task_runtime_info('CURRENT_TASK_GRAPH_ORIGINAL_SCHEDULED_TIMESTAMP'))":
            mock_result_datetime,
        "select to_timestamp(system$task_runtime_info('LAST_SUCCESSFUL_TASK_GRAPH_ORIGINAL_SCHEDULED_TIMESTAMP'))":
            mock_result_datetime,
    }

    def side_effect_sql(k):
        return mock_sql_result[k]
    fake_root.sql.side_effect = side_effect_sql

    assert task_context.get_current_root_task_name() == "abc"
    assert task_context.get_current_root_task_uuid() == "abc"
    assert task_context.get_current_task_graph_run_group_id() == "abc"
    assert task_context.get_last_successful_task_graph_run_group_id() == "abc"
    assert task_context.get_current_task_graph_original_schedule() == datetime.datetime(2020, 1, 1)
    assert task_context.get_last_successful_task_graph_original_schedule() == datetime.datetime(2020, 1, 1)

    def side_effect_call(sp_name, para=None):
        if sp_name == "system$set_return_value":
            return None
        if sp_name == "system$get_predecessor_return_value":
            return para
        if sp_name == "system$current_user_task_name":
            return "current_task_name"
        if sp_name == "SYSTEM$GET_TASK_GRAPH_CONFIG":
            return '{"a": "b", "c": 1}'

    fake_root.call.side_effect = side_effect_call
    assert task_context.get_current_task_name() == "current_task_name"
    assert task_context.get_current_task_name() == "current_task_name"  # second time get the cache
    assert task_context.get_current_task_short_name() == "current_task_name"
    assert task_context.get_predecessor_return_value("task1") == "TASK1"
    assert task_context.set_return_value("rv") is None
    assert task_context.get_task_graph_config() == {"a": "b", "c": 1}
    assert task_context.get_task_graph_config_property("c") == 1

    def side_effect_call_none(sp_name, para=None):
        if sp_name == "SYSTEM$GET_TASK_GRAPH_CONFIG":
            return ''
    fake_root.call.side_effect = side_effect_call_none
    assert task_context.get_task_graph_config() is None
    with pytest.raises(ValueError) as ve:
        task_context.get_runtime_info('')
    assert ve.match("`property_name` must be an non-empty str.")

    def side_effect_raise_null_result(*args):
        raise SnowparkSQLException("NULL result in a non-nullable column")
    fake_root.sql.side_effect = side_effect_raise_null_result
    assert task_context.get_runtime_info("CURRENT_TASK_GRAPH_ORIGINAL_SCHEDULED_TIMESTAMP") is None

    def side_effect_raise_other_error(*args):
        raise SnowparkSQLException("Some errors")
    fake_root.sql.side_effect = side_effect_raise_other_error
    with pytest.raises(SnowparkSQLException) as sse:
        task_context.get_runtime_info("CURRENT_TASK_GRAPH_ORIGINAL_SCHEDULED_TIMESTAMP")
    assert sse.match("Some error")


def test_get_current_task_short_name(fake_root):
    task_context = TaskContext(fake_root)

    task_context.get_current_root_task_name = Mock(return_value="root")
    task_context.get_current_task_name = Mock(return_value="root$abc")
    assert task_context.get_current_task_name() == "root$abc"
    assert task_context.get_current_task_short_name() == "abc"
    task_context.get_current_task_name.return_value = "no_root"
    assert task_context.get_current_task_short_name() == "no_root"
