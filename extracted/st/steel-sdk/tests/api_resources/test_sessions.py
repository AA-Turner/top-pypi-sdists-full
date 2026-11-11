# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from steel import Steel, AsyncSteel
from steel.types import (
    Session as TypesSession,
    SessionContext,
    SessionCostResponse,
    SessionLogsResponse,
    SessionEventsResponse,
    SessionReleaseResponse,
    SessionCommandsResponse,
    SessionComputerResponse,
    SessionReleaseAllResponse,
    SessionAgentTracesResponse,
    SessionLiveDetailsResponse,
    SessionSignalCatalogResponse,
    SessionUpdateMetadataResponse,
    SessionReplaceMetadataResponse,
)
from tests.utils import assert_matches_type
from steel._utils import parse_datetime
from steel._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)
from steel.pagination import SyncSessionsCursor, AsyncSessionsCursor
from steel.types.sessionslist import Session as SessionslistSession

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSessions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Steel) -> None:
        session = client.sessions.create()
        assert_matches_type(TypesSession, session, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Steel) -> None:
        session = client.sessions.create(
            block_ads=True,
            ca_certificates=["string"],
            concurrency=-9007199254740991,
            credentials={
                "auto_submit": True,
                "blur_fields": True,
                "credential_provider": "credentialProvider",
                "exact_origin": True,
                "origins": ["string"],
            },
            debug_config={
                "interactive": True,
                "system_cursor": True,
            },
            device_config={"device": "desktop"},
            dimensions={
                "height": -9007199254740991,
                "width": -9007199254740991,
            },
            experimental_features=["string"],
            extension_ids=["string"],
            fullscreen=True,
            headless=True,
            inactivity_timeout=1,
            is_selenium=True,
            metadata={"foo": "string"},
            namespace="namespace",
            optimize_bandwidth=True,
            persist_profile=True,
            profile_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            proxy_url="https://example.com",
            recording=True,
            region={},
            session_context={
                "cookies": [
                    {
                        "name": "name",
                        "value": "value",
                        "domain": "domain",
                        "expires": 0,
                        "http_only": True,
                        "partition_key": {
                            "has_cross_site_ancestor": True,
                            "top_level_site": "topLevelSite",
                        },
                        "path": "path",
                        "priority": "Low",
                        "same_party": True,
                        "same_site": "Strict",
                        "secure": True,
                        "session": True,
                        "size": 0,
                        "source_port": 0,
                        "source_scheme": "Unset",
                        "url": "url",
                    }
                ],
                "indexed_db": {
                    "foo": [
                        {
                            "id": 0,
                            "data": [
                                {
                                    "id": 0,
                                    "name": "name",
                                    "records": [
                                        {
                                            "key": {},
                                            "value": {},
                                            "blob_files": [
                                                {
                                                    "blob_number": 0,
                                                    "mime_type": "mimeType",
                                                    "size": 0,
                                                    "filename": "filename",
                                                    "last_modified": parse_datetime("2019-12-27T18:11:19.117Z"),
                                                    "path": "path",
                                                }
                                            ],
                                        }
                                    ],
                                }
                            ],
                            "name": "name",
                        }
                    ]
                },
                "local_storage": {"foo": {"foo": "string"}},
                "session_storage": {"foo": {"foo": "string"}},
            },
            session_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            solve_captcha=True,
            stealth_config={
                "auto_captcha_solving": True,
                "humanize_interactions": True,
                "skip_fingerprint_injection": True,
            },
            api_timeout=-9007199254740991,
            use_proxy=True,
            user_agent="userAgent",
        )
        assert_matches_type(TypesSession, session, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(TypesSession, session, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(TypesSession, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Steel) -> None:
        session = client.sessions.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(TypesSession, session, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(TypesSession, session, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(TypesSession, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.sessions.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: Steel) -> None:
        session = client.sessions.list()
        assert_matches_type(SyncSessionsCursor[SessionslistSession], session, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Steel) -> None:
        session = client.sessions.list(
            created_after=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_before=parse_datetime("2019-12-27T18:11:19.117Z"),
            cursor_id="cursorId",
            limit=1,
            metadata={"foo": "x"},
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            release_reason="user_requested",
            signal=["captcha_encountered"],
            status="live",
        )
        assert_matches_type(SyncSessionsCursor[SessionslistSession], session, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SyncSessionsCursor[SessionslistSession], session, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SyncSessionsCursor[SessionslistSession], session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_agent_traces(self, client: Steel) -> None:
        session = client.sessions.agent_traces(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionAgentTracesResponse, session, path=["response"])

    @parametrize
    def test_method_agent_traces_with_all_params(self, client: Steel) -> None:
        session = client.sessions.agent_traces(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            end_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            event_types=["string"],
            limit=1,
            namespace="namespace",
            offset=0,
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(SessionAgentTracesResponse, session, path=["response"])

    @parametrize
    def test_raw_response_agent_traces(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.agent_traces(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionAgentTracesResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_agent_traces(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.agent_traces(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionAgentTracesResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_agent_traces(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.sessions.with_raw_response.agent_traces(
                id="",
            )

    @parametrize
    def test_method_commands(self, client: Steel) -> None:
        session = client.sessions.commands(
            session_id="sessionId",
            commands={
                "command": "navigate",
                "url": "x",
            },
        )
        assert_matches_type(SessionCommandsResponse, session, path=["response"])

    @parametrize
    def test_method_commands_with_all_params(self, client: Steel) -> None:
        session = client.sessions.commands(
            session_id="sessionId",
            commands={
                "command": "navigate",
                "url": "x",
                "tab": "t321669910225",
            },
            after="x",
            observe={
                "mode": "none",
                "base": "x",
                "compact": True,
                "depth": 0,
                "interactive": True,
                "tab": "t321669910225",
            },
            idempotency_key="idempotency-key",
        )
        assert_matches_type(SessionCommandsResponse, session, path=["response"])

    @parametrize
    def test_raw_response_commands(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.commands(
            session_id="sessionId",
            commands={
                "command": "navigate",
                "url": "x",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionCommandsResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_commands(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.commands(
            session_id="sessionId",
            commands={
                "command": "navigate",
                "url": "x",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionCommandsResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_commands(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.commands(
                session_id="",
                commands={
                    "command": "navigate",
                    "url": "x",
                },
            )

    @parametrize
    def test_method_computer_overload_1(self, client: Steel) -> None:
        session = client.sessions.computer(
            session_id="sessionId",
            action="move_mouse",
            coordinates=[0, 0],
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_method_computer_with_all_params_overload_1(self, client: Steel) -> None:
        session = client.sessions.computer(
            session_id="sessionId",
            action="move_mouse",
            coordinates=[0, 0],
            hold_keys=["string"],
            screenshot=True,
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_raw_response_computer_overload_1(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.computer(
            session_id="sessionId",
            action="move_mouse",
            coordinates=[0, 0],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_computer_overload_1(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.computer(
            session_id="sessionId",
            action="move_mouse",
            coordinates=[0, 0],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionComputerResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_computer_overload_1(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.computer(
                session_id="",
                action="move_mouse",
                coordinates=[0, 0],
            )

    @parametrize
    def test_method_computer_overload_2(self, client: Steel) -> None:
        session = client.sessions.computer(
            session_id="sessionId",
            action="click_mouse",
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_method_computer_with_all_params_overload_2(self, client: Steel) -> None:
        session = client.sessions.computer(
            session_id="sessionId",
            action="click_mouse",
            button="left",
            click_type="down",
            coordinates=[0, 0],
            hold_keys=["string"],
            num_clicks=0,
            screenshot=True,
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_raw_response_computer_overload_2(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.computer(
            session_id="sessionId",
            action="click_mouse",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_computer_overload_2(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.computer(
            session_id="sessionId",
            action="click_mouse",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionComputerResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_computer_overload_2(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.computer(
                session_id="",
                action="click_mouse",
            )

    @parametrize
    def test_method_computer_overload_3(self, client: Steel) -> None:
        session = client.sessions.computer(
            session_id="sessionId",
            action="drag_mouse",
            path=[[0, 0]],
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_method_computer_with_all_params_overload_3(self, client: Steel) -> None:
        session = client.sessions.computer(
            session_id="sessionId",
            action="drag_mouse",
            path=[[0, 0]],
            hold_keys=["string"],
            screenshot=True,
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_raw_response_computer_overload_3(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.computer(
            session_id="sessionId",
            action="drag_mouse",
            path=[[0, 0]],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_computer_overload_3(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.computer(
            session_id="sessionId",
            action="drag_mouse",
            path=[[0, 0]],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionComputerResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_computer_overload_3(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.computer(
                session_id="",
                action="drag_mouse",
                path=[[0, 0]],
            )

    @parametrize
    def test_method_computer_overload_4(self, client: Steel) -> None:
        session = client.sessions.computer(
            session_id="sessionId",
            action="scroll",
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_method_computer_with_all_params_overload_4(self, client: Steel) -> None:
        session = client.sessions.computer(
            session_id="sessionId",
            action="scroll",
            coordinates=[0, 0],
            delta_x=0,
            delta_y=0,
            hold_keys=["string"],
            screenshot=True,
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_raw_response_computer_overload_4(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.computer(
            session_id="sessionId",
            action="scroll",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_computer_overload_4(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.computer(
            session_id="sessionId",
            action="scroll",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionComputerResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_computer_overload_4(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.computer(
                session_id="",
                action="scroll",
            )

    @parametrize
    def test_method_computer_overload_5(self, client: Steel) -> None:
        session = client.sessions.computer(
            session_id="sessionId",
            action="press_key",
            keys=["string"],
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_method_computer_with_all_params_overload_5(self, client: Steel) -> None:
        session = client.sessions.computer(
            session_id="sessionId",
            action="press_key",
            keys=["string"],
            duration=0,
            screenshot=True,
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_raw_response_computer_overload_5(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.computer(
            session_id="sessionId",
            action="press_key",
            keys=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_computer_overload_5(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.computer(
            session_id="sessionId",
            action="press_key",
            keys=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionComputerResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_computer_overload_5(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.computer(
                session_id="",
                action="press_key",
                keys=["string"],
            )

    @parametrize
    def test_method_computer_overload_6(self, client: Steel) -> None:
        session = client.sessions.computer(
            session_id="sessionId",
            action="type_text",
            text="text",
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_method_computer_with_all_params_overload_6(self, client: Steel) -> None:
        session = client.sessions.computer(
            session_id="sessionId",
            action="type_text",
            text="text",
            hold_keys=["string"],
            screenshot=True,
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_raw_response_computer_overload_6(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.computer(
            session_id="sessionId",
            action="type_text",
            text="text",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_computer_overload_6(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.computer(
            session_id="sessionId",
            action="type_text",
            text="text",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionComputerResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_computer_overload_6(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.computer(
                session_id="",
                action="type_text",
                text="text",
            )

    @parametrize
    def test_method_computer_overload_7(self, client: Steel) -> None:
        session = client.sessions.computer(
            session_id="sessionId",
            action="wait",
            duration=0,
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_method_computer_with_all_params_overload_7(self, client: Steel) -> None:
        session = client.sessions.computer(
            session_id="sessionId",
            action="wait",
            duration=0,
            screenshot=True,
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_raw_response_computer_overload_7(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.computer(
            session_id="sessionId",
            action="wait",
            duration=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_computer_overload_7(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.computer(
            session_id="sessionId",
            action="wait",
            duration=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionComputerResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_computer_overload_7(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.computer(
                session_id="",
                action="wait",
                duration=0,
            )

    @parametrize
    def test_method_computer_overload_8(self, client: Steel) -> None:
        session = client.sessions.computer(
            session_id="sessionId",
            action="take_screenshot",
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_raw_response_computer_overload_8(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.computer(
            session_id="sessionId",
            action="take_screenshot",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_computer_overload_8(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.computer(
            session_id="sessionId",
            action="take_screenshot",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionComputerResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_computer_overload_8(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.computer(
                session_id="",
                action="take_screenshot",
            )

    @parametrize
    def test_method_computer_overload_9(self, client: Steel) -> None:
        session = client.sessions.computer(
            session_id="sessionId",
            action="get_cursor_position",
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_raw_response_computer_overload_9(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.computer(
            session_id="sessionId",
            action="get_cursor_position",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_computer_overload_9(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.computer(
            session_id="sessionId",
            action="get_cursor_position",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionComputerResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_computer_overload_9(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            client.sessions.with_raw_response.computer(
                session_id="",
                action="get_cursor_position",
            )

    @parametrize
    def test_method_context(self, client: Steel) -> None:
        session = client.sessions.context(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionContext, session, path=["response"])

    @parametrize
    def test_raw_response_context(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.context(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionContext, session, path=["response"])

    @parametrize
    def test_streaming_response_context(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.context(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionContext, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_context(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.sessions.with_raw_response.context(
                "",
            )

    @parametrize
    def test_method_cost(self, client: Steel) -> None:
        session = client.sessions.cost(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionCostResponse, session, path=["response"])

    @parametrize
    def test_raw_response_cost(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.cost(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionCostResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_cost(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.cost(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionCostResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_cost(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.sessions.with_raw_response.cost(
                "",
            )

    @parametrize
    def test_method_events(self, client: Steel) -> None:
        session = client.sessions.events(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionEventsResponse, session, path=["response"])

    @parametrize
    def test_method_events_with_all_params(self, client: Steel) -> None:
        session = client.sessions.events(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            compressed=True,
            limit=1,
            pointer="pointer",
        )
        assert_matches_type(SessionEventsResponse, session, path=["response"])

    @parametrize
    def test_raw_response_events(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.events(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionEventsResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_events(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.events(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionEventsResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_events(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.sessions.with_raw_response.events(
                id="",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_hls(self, client: Steel, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions/182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e/hls").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        session = client.sessions.hls(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert session.is_closed
        assert session.json() == {"foo": "bar"}
        assert cast(Any, session.is_closed) is True
        assert isinstance(session, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_hls(self, client: Steel, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions/182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e/hls").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        session = client.sessions.with_raw_response.hls(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert session.is_closed is True
        assert session.http_request.headers.get("X-Steel-Lang") == "python"
        assert session.json() == {"foo": "bar"}
        assert isinstance(session, BinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_hls(self, client: Steel, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions/182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e/hls").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.sessions.with_streaming_response.hls(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as session:
            assert not session.is_closed
            assert session.http_request.headers.get("X-Steel-Lang") == "python"

            assert session.json() == {"foo": "bar"}
            assert cast(Any, session.is_closed) is True
            assert isinstance(session, StreamedBinaryAPIResponse)

        assert cast(Any, session.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_hls(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.sessions.with_raw_response.hls(
                "",
            )

    @parametrize
    def test_method_live_details(self, client: Steel) -> None:
        session = client.sessions.live_details(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionLiveDetailsResponse, session, path=["response"])

    @parametrize
    def test_raw_response_live_details(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.live_details(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionLiveDetailsResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_live_details(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.live_details(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionLiveDetailsResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_live_details(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.sessions.with_raw_response.live_details(
                "",
            )

    @parametrize
    def test_method_logs(self, client: Steel) -> None:
        session = client.sessions.logs(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionLogsResponse, session, path=["response"])

    @parametrize
    def test_method_logs_with_all_params(self, client: Steel) -> None:
        session = client.sessions.logs(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            end_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            event_types=["string"],
            limit=1,
            namespace="namespace",
            offset=0,
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(SessionLogsResponse, session, path=["response"])

    @parametrize
    def test_raw_response_logs(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.logs(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionLogsResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_logs(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.logs(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionLogsResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_logs(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.sessions.with_raw_response.logs(
                id="",
            )

    @parametrize
    def test_method_release(self, client: Steel) -> None:
        session = client.sessions.release(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionReleaseResponse, session, path=["response"])

    @parametrize
    def test_raw_response_release(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.release(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionReleaseResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_release(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.release(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionReleaseResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_release(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.sessions.with_raw_response.release(
                "",
            )

    @parametrize
    def test_method_release_all(self, client: Steel) -> None:
        session = client.sessions.release_all()
        assert_matches_type(SessionReleaseAllResponse, session, path=["response"])

    @parametrize
    def test_method_release_all_with_all_params(self, client: Steel) -> None:
        session = client.sessions.release_all(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionReleaseAllResponse, session, path=["response"])

    @parametrize
    def test_raw_response_release_all(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.release_all()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionReleaseAllResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_release_all(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.release_all() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionReleaseAllResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_replace_metadata(self, client: Steel) -> None:
        session = client.sessions.replace_metadata(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            metadata={"foo": "string"},
        )
        assert_matches_type(SessionReplaceMetadataResponse, session, path=["response"])

    @parametrize
    def test_raw_response_replace_metadata(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.replace_metadata(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            metadata={"foo": "string"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionReplaceMetadataResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_replace_metadata(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.replace_metadata(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            metadata={"foo": "string"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionReplaceMetadataResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_replace_metadata(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.sessions.with_raw_response.replace_metadata(
                id="",
                metadata={"foo": "string"},
            )

    @parametrize
    def test_method_signal_catalog(self, client: Steel) -> None:
        session = client.sessions.signal_catalog()
        assert_matches_type(SessionSignalCatalogResponse, session, path=["response"])

    @parametrize
    def test_raw_response_signal_catalog(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.signal_catalog()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionSignalCatalogResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_signal_catalog(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.signal_catalog() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionSignalCatalogResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_update_metadata(self, client: Steel) -> None:
        session = client.sessions.update_metadata(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            metadata={"foo": "string"},
        )
        assert_matches_type(SessionUpdateMetadataResponse, session, path=["response"])

    @parametrize
    def test_raw_response_update_metadata(self, client: Steel) -> None:
        response = client.sessions.with_raw_response.update_metadata(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            metadata={"foo": "string"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = response.parse()
        assert_matches_type(SessionUpdateMetadataResponse, session, path=["response"])

    @parametrize
    def test_streaming_response_update_metadata(self, client: Steel) -> None:
        with client.sessions.with_streaming_response.update_metadata(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            metadata={"foo": "string"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = response.parse()
            assert_matches_type(SessionUpdateMetadataResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_update_metadata(self, client: Steel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.sessions.with_raw_response.update_metadata(
                id="",
                metadata={"foo": "string"},
            )


class TestAsyncSessions:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.create()
        assert_matches_type(TypesSession, session, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.create(
            block_ads=True,
            ca_certificates=["string"],
            concurrency=-9007199254740991,
            credentials={
                "auto_submit": True,
                "blur_fields": True,
                "credential_provider": "credentialProvider",
                "exact_origin": True,
                "origins": ["string"],
            },
            debug_config={
                "interactive": True,
                "system_cursor": True,
            },
            device_config={"device": "desktop"},
            dimensions={
                "height": -9007199254740991,
                "width": -9007199254740991,
            },
            experimental_features=["string"],
            extension_ids=["string"],
            fullscreen=True,
            headless=True,
            inactivity_timeout=1,
            is_selenium=True,
            metadata={"foo": "string"},
            namespace="namespace",
            optimize_bandwidth=True,
            persist_profile=True,
            profile_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            proxy_url="https://example.com",
            recording=True,
            region={},
            session_context={
                "cookies": [
                    {
                        "name": "name",
                        "value": "value",
                        "domain": "domain",
                        "expires": 0,
                        "http_only": True,
                        "partition_key": {
                            "has_cross_site_ancestor": True,
                            "top_level_site": "topLevelSite",
                        },
                        "path": "path",
                        "priority": "Low",
                        "same_party": True,
                        "same_site": "Strict",
                        "secure": True,
                        "session": True,
                        "size": 0,
                        "source_port": 0,
                        "source_scheme": "Unset",
                        "url": "url",
                    }
                ],
                "indexed_db": {
                    "foo": [
                        {
                            "id": 0,
                            "data": [
                                {
                                    "id": 0,
                                    "name": "name",
                                    "records": [
                                        {
                                            "key": {},
                                            "value": {},
                                            "blob_files": [
                                                {
                                                    "blob_number": 0,
                                                    "mime_type": "mimeType",
                                                    "size": 0,
                                                    "filename": "filename",
                                                    "last_modified": parse_datetime("2019-12-27T18:11:19.117Z"),
                                                    "path": "path",
                                                }
                                            ],
                                        }
                                    ],
                                }
                            ],
                            "name": "name",
                        }
                    ]
                },
                "local_storage": {"foo": {"foo": "string"}},
                "session_storage": {"foo": {"foo": "string"}},
            },
            session_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            solve_captcha=True,
            stealth_config={
                "auto_captcha_solving": True,
                "humanize_interactions": True,
                "skip_fingerprint_injection": True,
            },
            api_timeout=-9007199254740991,
            use_proxy=True,
            user_agent="userAgent",
        )
        assert_matches_type(TypesSession, session, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(TypesSession, session, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(TypesSession, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(TypesSession, session, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(TypesSession, session, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.retrieve(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(TypesSession, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.sessions.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.list()
        assert_matches_type(AsyncSessionsCursor[SessionslistSession], session, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.list(
            created_after=parse_datetime("2019-12-27T18:11:19.117Z"),
            created_before=parse_datetime("2019-12-27T18:11:19.117Z"),
            cursor_id="cursorId",
            limit=1,
            metadata={"foo": "x"},
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            release_reason="user_requested",
            signal=["captcha_encountered"],
            status="live",
        )
        assert_matches_type(AsyncSessionsCursor[SessionslistSession], session, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(AsyncSessionsCursor[SessionslistSession], session, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(AsyncSessionsCursor[SessionslistSession], session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_agent_traces(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.agent_traces(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionAgentTracesResponse, session, path=["response"])

    @parametrize
    async def test_method_agent_traces_with_all_params(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.agent_traces(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            end_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            event_types=["string"],
            limit=1,
            namespace="namespace",
            offset=0,
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(SessionAgentTracesResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_agent_traces(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.agent_traces(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionAgentTracesResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_agent_traces(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.agent_traces(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionAgentTracesResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_agent_traces(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.sessions.with_raw_response.agent_traces(
                id="",
            )

    @parametrize
    async def test_method_commands(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.commands(
            session_id="sessionId",
            commands={
                "command": "navigate",
                "url": "x",
            },
        )
        assert_matches_type(SessionCommandsResponse, session, path=["response"])

    @parametrize
    async def test_method_commands_with_all_params(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.commands(
            session_id="sessionId",
            commands={
                "command": "navigate",
                "url": "x",
                "tab": "t321669910225",
            },
            after="x",
            observe={
                "mode": "none",
                "base": "x",
                "compact": True,
                "depth": 0,
                "interactive": True,
                "tab": "t321669910225",
            },
            idempotency_key="idempotency-key",
        )
        assert_matches_type(SessionCommandsResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_commands(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.commands(
            session_id="sessionId",
            commands={
                "command": "navigate",
                "url": "x",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionCommandsResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_commands(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.commands(
            session_id="sessionId",
            commands={
                "command": "navigate",
                "url": "x",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionCommandsResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_commands(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.with_raw_response.commands(
                session_id="",
                commands={
                    "command": "navigate",
                    "url": "x",
                },
            )

    @parametrize
    async def test_method_computer_overload_1(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.computer(
            session_id="sessionId",
            action="move_mouse",
            coordinates=[0, 0],
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_method_computer_with_all_params_overload_1(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.computer(
            session_id="sessionId",
            action="move_mouse",
            coordinates=[0, 0],
            hold_keys=["string"],
            screenshot=True,
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_computer_overload_1(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.computer(
            session_id="sessionId",
            action="move_mouse",
            coordinates=[0, 0],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_computer_overload_1(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.computer(
            session_id="sessionId",
            action="move_mouse",
            coordinates=[0, 0],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionComputerResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_computer_overload_1(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.with_raw_response.computer(
                session_id="",
                action="move_mouse",
                coordinates=[0, 0],
            )

    @parametrize
    async def test_method_computer_overload_2(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.computer(
            session_id="sessionId",
            action="click_mouse",
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_method_computer_with_all_params_overload_2(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.computer(
            session_id="sessionId",
            action="click_mouse",
            button="left",
            click_type="down",
            coordinates=[0, 0],
            hold_keys=["string"],
            num_clicks=0,
            screenshot=True,
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_computer_overload_2(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.computer(
            session_id="sessionId",
            action="click_mouse",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_computer_overload_2(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.computer(
            session_id="sessionId",
            action="click_mouse",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionComputerResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_computer_overload_2(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.with_raw_response.computer(
                session_id="",
                action="click_mouse",
            )

    @parametrize
    async def test_method_computer_overload_3(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.computer(
            session_id="sessionId",
            action="drag_mouse",
            path=[[0, 0]],
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_method_computer_with_all_params_overload_3(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.computer(
            session_id="sessionId",
            action="drag_mouse",
            path=[[0, 0]],
            hold_keys=["string"],
            screenshot=True,
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_computer_overload_3(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.computer(
            session_id="sessionId",
            action="drag_mouse",
            path=[[0, 0]],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_computer_overload_3(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.computer(
            session_id="sessionId",
            action="drag_mouse",
            path=[[0, 0]],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionComputerResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_computer_overload_3(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.with_raw_response.computer(
                session_id="",
                action="drag_mouse",
                path=[[0, 0]],
            )

    @parametrize
    async def test_method_computer_overload_4(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.computer(
            session_id="sessionId",
            action="scroll",
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_method_computer_with_all_params_overload_4(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.computer(
            session_id="sessionId",
            action="scroll",
            coordinates=[0, 0],
            delta_x=0,
            delta_y=0,
            hold_keys=["string"],
            screenshot=True,
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_computer_overload_4(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.computer(
            session_id="sessionId",
            action="scroll",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_computer_overload_4(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.computer(
            session_id="sessionId",
            action="scroll",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionComputerResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_computer_overload_4(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.with_raw_response.computer(
                session_id="",
                action="scroll",
            )

    @parametrize
    async def test_method_computer_overload_5(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.computer(
            session_id="sessionId",
            action="press_key",
            keys=["string"],
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_method_computer_with_all_params_overload_5(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.computer(
            session_id="sessionId",
            action="press_key",
            keys=["string"],
            duration=0,
            screenshot=True,
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_computer_overload_5(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.computer(
            session_id="sessionId",
            action="press_key",
            keys=["string"],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_computer_overload_5(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.computer(
            session_id="sessionId",
            action="press_key",
            keys=["string"],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionComputerResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_computer_overload_5(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.with_raw_response.computer(
                session_id="",
                action="press_key",
                keys=["string"],
            )

    @parametrize
    async def test_method_computer_overload_6(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.computer(
            session_id="sessionId",
            action="type_text",
            text="text",
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_method_computer_with_all_params_overload_6(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.computer(
            session_id="sessionId",
            action="type_text",
            text="text",
            hold_keys=["string"],
            screenshot=True,
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_computer_overload_6(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.computer(
            session_id="sessionId",
            action="type_text",
            text="text",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_computer_overload_6(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.computer(
            session_id="sessionId",
            action="type_text",
            text="text",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionComputerResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_computer_overload_6(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.with_raw_response.computer(
                session_id="",
                action="type_text",
                text="text",
            )

    @parametrize
    async def test_method_computer_overload_7(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.computer(
            session_id="sessionId",
            action="wait",
            duration=0,
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_method_computer_with_all_params_overload_7(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.computer(
            session_id="sessionId",
            action="wait",
            duration=0,
            screenshot=True,
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_computer_overload_7(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.computer(
            session_id="sessionId",
            action="wait",
            duration=0,
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_computer_overload_7(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.computer(
            session_id="sessionId",
            action="wait",
            duration=0,
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionComputerResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_computer_overload_7(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.with_raw_response.computer(
                session_id="",
                action="wait",
                duration=0,
            )

    @parametrize
    async def test_method_computer_overload_8(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.computer(
            session_id="sessionId",
            action="take_screenshot",
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_computer_overload_8(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.computer(
            session_id="sessionId",
            action="take_screenshot",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_computer_overload_8(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.computer(
            session_id="sessionId",
            action="take_screenshot",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionComputerResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_computer_overload_8(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.with_raw_response.computer(
                session_id="",
                action="take_screenshot",
            )

    @parametrize
    async def test_method_computer_overload_9(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.computer(
            session_id="sessionId",
            action="get_cursor_position",
        )
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_computer_overload_9(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.computer(
            session_id="sessionId",
            action="get_cursor_position",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionComputerResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_computer_overload_9(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.computer(
            session_id="sessionId",
            action="get_cursor_position",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionComputerResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_computer_overload_9(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_id` but received ''"):
            await async_client.sessions.with_raw_response.computer(
                session_id="",
                action="get_cursor_position",
            )

    @parametrize
    async def test_method_context(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.context(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionContext, session, path=["response"])

    @parametrize
    async def test_raw_response_context(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.context(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionContext, session, path=["response"])

    @parametrize
    async def test_streaming_response_context(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.context(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionContext, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_context(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.sessions.with_raw_response.context(
                "",
            )

    @parametrize
    async def test_method_cost(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.cost(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionCostResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_cost(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.cost(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionCostResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_cost(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.cost(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionCostResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_cost(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.sessions.with_raw_response.cost(
                "",
            )

    @parametrize
    async def test_method_events(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.events(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionEventsResponse, session, path=["response"])

    @parametrize
    async def test_method_events_with_all_params(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.events(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            compressed=True,
            limit=1,
            pointer="pointer",
        )
        assert_matches_type(SessionEventsResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_events(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.events(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionEventsResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_events(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.events(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionEventsResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_events(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.sessions.with_raw_response.events(
                id="",
            )

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_hls(self, async_client: AsyncSteel, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions/182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e/hls").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        session = await async_client.sessions.hls(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert session.is_closed
        assert await session.json() == {"foo": "bar"}
        assert cast(Any, session.is_closed) is True
        assert isinstance(session, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_hls(self, async_client: AsyncSteel, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions/182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e/hls").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        session = await async_client.sessions.with_raw_response.hls(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert session.is_closed is True
        assert session.http_request.headers.get("X-Steel-Lang") == "python"
        assert await session.json() == {"foo": "bar"}
        assert isinstance(session, AsyncBinaryAPIResponse)

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_hls(self, async_client: AsyncSteel, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/sessions/182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e/hls").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.sessions.with_streaming_response.hls(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as session:
            assert not session.is_closed
            assert session.http_request.headers.get("X-Steel-Lang") == "python"

            assert await session.json() == {"foo": "bar"}
            assert cast(Any, session.is_closed) is True
            assert isinstance(session, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, session.is_closed) is True

    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_hls(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.sessions.with_raw_response.hls(
                "",
            )

    @parametrize
    async def test_method_live_details(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.live_details(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionLiveDetailsResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_live_details(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.live_details(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionLiveDetailsResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_live_details(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.live_details(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionLiveDetailsResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_live_details(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.sessions.with_raw_response.live_details(
                "",
            )

    @parametrize
    async def test_method_logs(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.logs(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionLogsResponse, session, path=["response"])

    @parametrize
    async def test_method_logs_with_all_params(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.logs(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            end_time=parse_datetime("2019-12-27T18:11:19.117Z"),
            event_types=["string"],
            limit=1,
            namespace="namespace",
            offset=0,
            start_time=parse_datetime("2019-12-27T18:11:19.117Z"),
        )
        assert_matches_type(SessionLogsResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_logs(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.logs(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionLogsResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_logs(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.logs(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionLogsResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_logs(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.sessions.with_raw_response.logs(
                id="",
            )

    @parametrize
    async def test_method_release(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.release(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionReleaseResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_release(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.release(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionReleaseResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_release(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.release(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionReleaseResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_release(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.sessions.with_raw_response.release(
                "",
            )

    @parametrize
    async def test_method_release_all(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.release_all()
        assert_matches_type(SessionReleaseAllResponse, session, path=["response"])

    @parametrize
    async def test_method_release_all_with_all_params(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.release_all(
            project_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(SessionReleaseAllResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_release_all(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.release_all()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionReleaseAllResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_release_all(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.release_all() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionReleaseAllResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_replace_metadata(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.replace_metadata(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            metadata={"foo": "string"},
        )
        assert_matches_type(SessionReplaceMetadataResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_replace_metadata(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.replace_metadata(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            metadata={"foo": "string"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionReplaceMetadataResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_replace_metadata(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.replace_metadata(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            metadata={"foo": "string"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionReplaceMetadataResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_replace_metadata(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.sessions.with_raw_response.replace_metadata(
                id="",
                metadata={"foo": "string"},
            )

    @parametrize
    async def test_method_signal_catalog(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.signal_catalog()
        assert_matches_type(SessionSignalCatalogResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_signal_catalog(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.signal_catalog()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionSignalCatalogResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_signal_catalog(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.signal_catalog() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionSignalCatalogResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_update_metadata(self, async_client: AsyncSteel) -> None:
        session = await async_client.sessions.update_metadata(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            metadata={"foo": "string"},
        )
        assert_matches_type(SessionUpdateMetadataResponse, session, path=["response"])

    @parametrize
    async def test_raw_response_update_metadata(self, async_client: AsyncSteel) -> None:
        response = await async_client.sessions.with_raw_response.update_metadata(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            metadata={"foo": "string"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Steel-Lang") == "python"
        session = await response.parse()
        assert_matches_type(SessionUpdateMetadataResponse, session, path=["response"])

    @parametrize
    async def test_streaming_response_update_metadata(self, async_client: AsyncSteel) -> None:
        async with async_client.sessions.with_streaming_response.update_metadata(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            metadata={"foo": "string"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Steel-Lang") == "python"

            session = await response.parse()
            assert_matches_type(SessionUpdateMetadataResponse, session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_update_metadata(self, async_client: AsyncSteel) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.sessions.with_raw_response.update_metadata(
                id="",
                metadata={"foo": "string"},
            )
