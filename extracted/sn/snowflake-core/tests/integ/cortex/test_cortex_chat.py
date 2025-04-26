#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#



import pytest

from urllib3 import HTTPResponse

from snowflake.core._root import Root
from snowflake.core.cortex.chat_service._generated.models import ChatRequest
from snowflake.core.rest import SSEClient
from snowflake.core.table import Table, TableColumn


TEST_SERVICE_NAME = "SNOWPY_TEST_SERVICE"
TEST_TABLE_NAME = "SNOWPY_TEST_TABLE"

API_NOT_ENABLED = "Cortex Search API is not enabled"


@pytest.fixture(autouse=True)
def setup_cortex_search_service(connection, warehouse, tables, backup_warehouse_fixture):
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

        rows = ",".join(["('Citi reimagines financial transactions in the data cloud', 'filter_value_1')",
                            "('ADP works in the data cloud. This is another mention of data cloud.', 'filter_value_2')",
                            "('Lorem ipsum dolor sit amet', 'filter_value_1')",
                            "('Cortex Search is a search solution for any problem', 'filter_value_2')"])
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
        cortex_search_services[TEST_SERVICE_NAME].search("hi", ["search_col", "filter1"], limit=5)
    except Exception as err:
        if API_NOT_ENABLED in err.body:
            pytest.xfail(API_NOT_ENABLED)
        raise

# Test chat through CortexChatService
# this is just to test the integrity of the python -> cortex chat service.
# We would not try to match the exact response as the response might change over time.
def test_chat_collection(root: Root, database, schema):
    resp = root.cortex_chat_service.chat(
        ChatRequest.from_dict({"query": "data cloud", "search_services":
                               [{"name": f"{database.name}.{schema.name}.{TEST_SERVICE_NAME}"}]}),
    )

    for e in resp.events():
        # check if the event and data are not None
        assert e.event is not None
        assert e.data is not None

# Test client parsing of chat service response through XP endpoint
def test_chat_collection_xp(root: Root):
    body_str = ('['
        '{"event":"thread.message.delta","data":{"id":"msg_001","object":"thread.message.delta",'
        '"delta":{"content":[{"index":0,"type":"text",'
        '"text":{"value":"Citi reimagines financial transactions in the data cloud 【†2†】."}}]}}},'

        '{"event":"thread.message.delta","data":{"id":"msg_001","object":"thread.message.delta",'
        '"delta":{"content":[{"index":1,"type":"citation",'
        '"citation":{"index":2,"chunk":"Citi reimagines financial transactions in the data cloud",'
        '"ranges":[{"start":41,"end":102}],"title":"","id":""}}]}}}'
        ']'
    )

    response = HTTPResponse(
        body=body_str.encode('utf-8'),
        status=200,
        headers={"Content-Type": "application/json"},
        preload_content=False,
    )
    res = SSEClient(response)

    exp_text = "Citi reimagines financial transactions in the data cloud 【†2†】."
    exp_citation_1 = "Citi reimagines financial transactions in the data cloud"
    event_num = 0
    for e in res.events():
        if event_num == 0:
            assert e.event == "thread.message.delta"
            assert e.data["id"] == "msg_001"
            assert e.data["object"] == "thread.message.delta"
            assert e.data["delta"]["content"][0]["index"] == 0
            assert e.data["delta"]["content"][0]["type"] == "text"
            assert e.data["delta"]["content"][0]["text"]["value"] == exp_text
        if event_num == 1:
            assert e.event == "thread.message.delta"
            assert e.data["id"] == "msg_001"
            assert e.data["object"] == "thread.message.delta"
            assert e.data["delta"]["content"][0]["index"] == 1
            assert e.data["delta"]["content"][0]["type"] == "citation"
            assert e.data["delta"]["content"][0]["citation"]["index"] == 2
            assert e.data["delta"]["content"][0]["citation"]["chunk"] == exp_citation_1
            assert e.data["delta"]["content"][0]["citation"]["ranges"][0]["start"] == 41
            assert e.data["delta"]["content"][0]["citation"]["ranges"][0]["end"] == 102
        event_num += 1

    assert event_num == 2

