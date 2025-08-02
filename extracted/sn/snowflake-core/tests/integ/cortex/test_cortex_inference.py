#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#
import json

import pytest

from urllib3 import HTTPResponse

from snowflake.core._root import Root
from snowflake.core.rest import SSEClient


pytestmark = [pytest.mark.skip_gov]


def test_cortex_inference(root: Root):
    pass
    # This test is disabled because cortex inference is not enabled on prod yet.
    # This test is manually verified to be working, see: https://github.com/snowflakedb/snowpy/pull/679
    #
    # messages = [CompleteRequestMessagesInner(content="some message")]
    # req = CompleteRequest(model="my_model", messages=messages)
    # res = root.cortex_inference_service.complete(req)
    # for e in res.events():
    #     print(e)


def test_cortex_inference_xp(root: Root):
    body_str = (
        "["
        '{"event":"model1","comment":"testing","data":{"strProp":"test1","doubleProp":1.1,"flag":false}},'
        '{"event":"model2","data":{"strProp":"test2","doubleProp":2.2,"flag":false},"retry":200},'
        '{"id":"3","event":"model3","comment":"with ID",'
        '"data":{"strProp":"test2","doubleProp":2.3,"flag":true},"retry":1000}'
        "]"
    )

    response = HTTPResponse(
        body=body_str.encode("utf-8"), status=200, headers={"Content-Type": "application/json"}, preload_content=False
    )
    res = SSEClient(response)

    event_num = 0
    for e in res.events():
        event_num += 1
        if e.event == "model1":
            assert e.comment == "testing"
        if e.event == "model2":
            assert e.retry == 200
        if e.event == "model3":
            assert e.id == "3"

    assert event_num == 3


def test_cortex_complete_xp(root: Root):
    body_str = '{"choices": [{"message": {"content": "Hello! \\n"}}]}'

    response = HTTPResponse(
        body=body_str.encode("utf-8"), status=200, headers={"Content-Type": "application/json"}, preload_content=False
    )
    res = SSEClient(response)

    for e in res.events():
        data = json.loads(e.data)
        assert data["choices"][0]["message"]["content"] == "Hello! \n"
