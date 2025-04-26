#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#


import pytest

from urllib3 import HTTPResponse

from snowflake.core._root import Root
from snowflake.core.rest import SSEClient
from snowflake.core.table import Table, TableColumn


TEST_SERVICE_NAME = "SNOWPY_TEST_SERVICE"
TEST_TABLE_NAME = "SNOWPY_TEST_TABLE"

API_NOT_ENABLED = "Cortex Agent API is not enabled"


@pytest.fixture(autouse=True)
def setup_cortex_search_service(
    connection, warehouse, tables, backup_warehouse_fixture
):
    del backup_warehouse_fixture
    # Base Table
    tables.create(
        Table(
            name=TEST_TABLE_NAME,
            columns=[
                TableColumn(name="search_col", datatype="varchar"),
                TableColumn(name="filter1", datatype="varchar"),
            ],
        ),
        mode="ifnotexists",
    )

    with connection.cursor() as cursor:
        cursor.execute(f"use warehouse {warehouse.name}").fetchone()

        rows = ",".join(
            [
                "('Citi reimagines financial transactions in the data cloud', 'filter_value_1')",
                "('ADP works in the data cloud. This is another mention of data cloud.', 'filter_value_2')",
                "('Lorem ipsum dolor sit amet', 'filter_value_1')",
                "('Cortex Search is a search solution for any problem', 'filter_value_2')",
            ]
        )
        cursor.execute(
            f"INSERT INTO {TEST_TABLE_NAME} VALUES {rows}",
        )

        # Cortex Search Service
        cursor.execute(
            f"CREATE OR REPLACE CORTEX SEARCH SERVICE {TEST_SERVICE_NAME} "
            f"ON search_col TARGET_LAG='1 minute' WAREHOUSE={warehouse.name} "
            f"AS SELECT search_col, filter1 FROM {TEST_TABLE_NAME}",
        )

        try:
            yield
        finally:
            cursor.execute(f"DROP CORTEX SEARCH SERVICE {TEST_SERVICE_NAME}")
            cursor.execute(f"DROP TABLE {TEST_TABLE_NAME}")


@pytest.fixture(autouse=True)
def precheck_cortex_search_enabled(cortex_search_services, setup_cortex_search_service):
    del setup_cortex_search_service
    try:
        cortex_search_services[TEST_SERVICE_NAME].search(
            "hi", ["search_col", "filter1"], limit=5
        )
    except Exception as err:
        if API_NOT_ENABLED in err.body:
            pytest.xfail(API_NOT_ENABLED)
        raise


# Test agent_run through CortexAgentService
# this is just to test the integrity of the python -> cortex agent_run service.
# We would not try to match the exact response as the response might change over time.
def test_agent_run(root: Root, database, schema):
    resp = root.cortex_agent_service.Run(
        {
            "model": "mistral-7b",
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": "I have an internet issues"}],
                }
            ],
            "tools": [{"tool_spec": {"type": "cortex_search", "name": "search1"}}],
            "tool_resources": {
                "search1": {
                    "name": f"{database.name}.{schema.name}.{TEST_SERVICE_NAME}"
                }
            },
        },
    )

    for e in resp.events():
        # check if the event and data are not None
        assert e.event is not None
        assert e.data is not None


# Test client parsing of agent_run service response through XP endpoint
def test_agent_run_xp(root: Root):
    def validate_text_message(event):
        content = event.data["delta"]["content"][0]
        assert content["index"] == 1
        assert content["type"] == "text"
        assert content["text"] == "Let me analyze your data."

    def validate_tool_use(event):
        content = event.data["delta"]["content"][0]
        assert content["index"] == 2
        assert content["type"] == "tool_use"
        tool_use = content["tool_use"]
        assert tool_use["tool_use_id"] == "tool_123"
        assert tool_use["name"] == "Analyst1"
        assert tool_use["input"]["sql_query"] == "SELECT * FROM sales"

    def validate_tool_result(event):
        content = event.data["delta"]["content"][0]
        assert content["index"] == 3
        assert content["type"] == "tool_results"
        tool_results = content["tool_results"]
        assert tool_results["tool_use_id"] == "tool_123"
        assert tool_results["status"] == "success"
        assert tool_results["content"][0]["type"] == "text"
        assert tool_results["content"][0]["text"] == "Query executed successfully"

    def validate_tool_result_json(event):
        content = event.data["delta"]["content"][0]
        assert content["index"] == 3
        assert content["type"] == "tool_results"
        tool_results = content["tool_results"]
        assert tool_results["tool_use_id"] == "tool_123"
        assert tool_results["status"] == "success"
        assert tool_results["content"][0]["type"] == "json"
        assert tool_results["content"][0]["json"]["sql_query"] == "SELECT * FROM sales"

    def validate_error_response(event):
        assert event.data["code"] == "400"
        assert event.data["message"] == "Invalid tool configuration"

    def validate_error_event(event):
        assert event.data["code"] == "399505"
        assert event.data["message"] == "Internal server error"

    test_cases = [
        # Text Message case
        {
            "body": (
                '[ {"event":"message.delta","data":{"id":"REQUEST_ID","object":"message.delta",'
                '"delta":{"content":[{"index":1,"type":"text","text":"Let me analyze your data."}]}}},'
                '{"event":"done","data":"[DONE]"}]'
            ),
            "validator": validate_text_message,
        },
        # Tool Use case
        {
            "body": (
                '[ {"event":"message.delta","data":{"id":"REQUEST_ID","object":"message.delta",'
                '"delta":{"content":[{"index":2,"type":"tool_use","tool_use":{"tool_use_id":"tool_123",'
                '"name":"Analyst1","input":{"sql_query":"SELECT * FROM sales"}}}]}}},'
                '{"event":"done","data":"[DONE]"}]'
            ),
            "validator": validate_tool_use,
        },
        # Tool Result case
        {
            "body": (
                '[ {"event":"message.delta","data":{"id":"REQUEST_ID","object":"message.delta",'
                '"delta":{"content":[{"index":3,"type":"tool_results","tool_results":{"tool_use_id":"tool_123",'
                '"content":[{"type":"text","text":"Query executed successfully"}],"status":"success"}}]}}},'
                '{"event":"done","data":"[DONE]"}]'
            ),
            "validator": validate_tool_result,
        },
        # Tool Result with JSON case
        {
            "body": (
                '[ {"event":"message.delta","data":{"id":"REQUEST_ID","object":"message.delta",'
                '"delta":{"content":[{"index":3,"type":"tool_results","tool_results":{"tool_use_id":"tool_123",'
                '"content":[{"type":"json","json":{"sql_query":"SELECT * FROM sales"}}],"status":"success"}}]}}},'
                '{"event":"done","data":"[DONE]"}]'
            ),
            "validator": validate_tool_result_json,
        },
        # Error Response case
        {
            "body": (
                '[ {"event":"error","data":{"code":"400","message":"Invalid tool configuration"}},'
                '{"event":"done","data":"[DONE]"}]'
            ),
            "validator": validate_error_response,
        },
        # Error Event case
        {
            "body": (
                '[ {"event":"error","data":{"code":"399505","message":"Internal server error"}},'
                '{"event":"done","data":"[DONE]"}]'
            ),
            "validator": validate_error_event,
        },
    ]


    for test_case in test_cases:
        response = HTTPResponse(
            body=test_case["body"].encode("utf-8"),
            status=200,
            headers={"Content-Type": "application/json"},
            preload_content=False,
        )
        res = SSEClient(response)

        event_num = 0
        for e in res.events():
            if event_num == 0:
                assert e.event in ["message.delta", "error"]
                assert e.data is not None

                if e.event == "message.delta":
                    assert e.data["id"] == "REQUEST_ID"
                    assert e.data["object"] == "message.delta"
                    test_case["validator"](e)
                elif e.event == "error":
                    test_case["validator"](e)

            elif event_num == 1:
                assert e.event == "done"
                assert e.data == "[DONE]"

            event_num += 1

        assert event_num == 2  # Ensure we got both the main event and the done event
