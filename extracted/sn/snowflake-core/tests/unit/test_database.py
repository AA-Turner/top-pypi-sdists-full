
from collections import defaultdict
from contextlib import suppress
from unittest import mock

from snowflake.core.database import Database
from snowflake.core.version import __version__ as VERSION


SNOWPY_USER_AGENT_VAL = "python_api/" + VERSION


def test_fetch_with_ua(fake_root, db):
    fake_root.root_config.get_user_agents = mock.MagicMock(return_value="customized_ua snowFlake/412.123.432a")
    fake_root.root_config.has_user_agents = mock.MagicMock(return_value=True)
    with suppress(Exception):
        with mock.patch("snowflake.core.database._generated.api_client.ApiClient.request") as mocked_request:
            db.fetch()
    try:
        mocked_request.assert_called_once_with(
            fake_root,
            "GET",
            "http://localhost:80/api/v2/databases/my_db",
            query_params=[],
            headers={"Accept": "application/json",
                    "User-Agent": SNOWPY_USER_AGENT_VAL + " customized_ua snowFlake/412.123.432a"},
            post_params=[],
            body=None,
            _preload_content=True,
            _request_timeout=None,
        )
    finally:
        fake_root.root_config.get_user_agents = mock.MagicMock(return_value="")
        fake_root.root_config.has_user_agents = mock.MagicMock(return_value=False)


def test_create_from_share(fake_root, dbs):
    with mock.patch("snowflake.core.database._generated.api_client.ApiClient.request") as mocked_request:
        dbs.create(
            database=Database(name="name"),
            from_share="share",
        )
    mocked_request.assert_called_once_with(
        fake_root,
        "POST",
        "http://localhost:80/api/v2/databases:from-share?createMode=errorIfExists&share=share",
        query_params=[
            ("createMode", "errorIfExists"),
            ("share", "share"),
        ],
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": SNOWPY_USER_AGENT_VAL,
        },
        post_params=[],
        body={
            "name": "name",
        },
        _preload_content=True,
        _request_timeout=None,
    )


request_called_count_for_long_running = defaultdict(int)


def mocked_request_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, data, status):
            self.data = data
            self.status = status

        def getheader(self, param):
            return {"Location": "/api/v2/results/XXXX"}.get(param, None)

    url = args[2]

    global request_called_count_for_long_running
    if "api/v2/databases" in url:
        request_called_count_for_long_running["database"] += 1
        return MockResponse(None, 202)

    assert "api/v2/result" in url
    request_called_count_for_long_running["result"] += 1
    if request_called_count_for_long_running.get("result", 0) < 2:
        return MockResponse(None, 202)
    return None


# def test_fetch_with_long_running(fake_root, setup_enable_rest_api_with_long_running):
#     dbs = DatabaseCollection(fake_root)
#     with setup_enable_rest_api_with_long_running(dbs._ref_class):
#         with mock.patch(
#             "snowflake.core.database._generated.api_client.ApiClient.request",
#             side_effect=mocked_request_get,
#         ):
#             # TODO: Improve fetch results instead of error
#             try:
#                 dbs["my_db"].fetch()
#             except AttributeError:
#                 # TODO: The AttributeError message is not reliable, so we just catch it and
#                 # pass for now. Make this better
#                 # assert e.args[0] == "'NoneType' object has no attribute 'status'"
#                 pass
#         global request_called_count_for_long_running
#         assert request_called_count_for_long_running['database'] == 1
#         assert request_called_count_for_long_running['result'] == 2


def test_fetch_with_throttling(fake_root, db):
    class MockResponse:
        headers = {"Location": "/api/v2/databases"}

        def __init__(self, data, status, reason):
            self.data = data
            self.status = status
            self.reason = reason

    with mock.patch("snowflake.core._http_requests.SFPoolManager.request") as mocked_request:
        # Triple Retry into Success
        http_throttle_codes = [429, 503, 504, 200]

        def side_effect(*args, **kwargs):
            status_code = http_throttle_codes.pop(0)
            return MockResponse("{\"name\": \"name\"}", status_code, "")

        mocked_request.side_effect = side_effect
        db.fetch()
    assert mocked_request.call_count == 4
    mocked_request.assert_called_with(
        fake_root,
        "GET",
        "http://localhost:80/api/v2/databases/my_db",
        fields={},
        preload_content=True,
        timeout=mock.ANY,
        headers={"Accept": "application/json", "User-Agent": SNOWPY_USER_AGENT_VAL},
    )
