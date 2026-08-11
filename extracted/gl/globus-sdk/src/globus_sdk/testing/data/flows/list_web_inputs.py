from __future__ import annotations

import typing as t
import uuid

from responses import matchers

from globus_sdk.testing.models import RegisteredResponse, ResponseList, ResponseSet

from ._common import TWO_HOP_TRANSFER_FLOW_ID, TWO_HOP_TRANSFER_RUN_ID

FIRST_WEB_INPUT_ID = "e35d1f92-3e2a-4c1c-8f36-7ce4f00f9d2c"


def generate_web_input_summary(
    web_input_id: str | uuid.UUID, n: int = 0
) -> dict[str, t.Any]:
    base_time = "2026-08-01T10:30:00+00:00"

    return {
        "id": str(web_input_id),
        "status": "open",
        "user_roles": ["viewer", "respondent"],
        "input_type": "selection",
        "title": f"Approve deployment #{n}?",
        "flow": {
            "id": TWO_HOP_TRANSFER_FLOW_ID,
            "title": "Multi Step Transfer",
        },
        "run": {
            "id": TWO_HOP_TRANSFER_RUN_ID,
            "label": "Transfer all of these files!",
        },
        "created_timestamp": base_time,
        "edited_timestamp": base_time,
        "closed_timestamp": None,
    }


FIRST_WEB_INPUT_SUMMARY = generate_web_input_summary(FIRST_WEB_INPUT_ID)

RESPONSES = ResponseSet(
    metadata={
        "first_web_input_id": FIRST_WEB_INPUT_ID,
        "flow_id": TWO_HOP_TRANSFER_FLOW_ID,
        "run_id": TWO_HOP_TRANSFER_RUN_ID,
    },
    default=RegisteredResponse(
        service="flows",
        path="/web_inputs",
        json={
            "web_input_summaries": [FIRST_WEB_INPUT_SUMMARY],
            "marker": None,
        },
    ),
    empty=RegisteredResponse(
        service="flows",
        path="/web_inputs",
        json={
            "web_input_summaries": [],
            "marker": None,
        },
    ),
    paginated=ResponseList(
        RegisteredResponse(
            service="flows",
            path="/web_inputs",
            json={
                "web_input_summaries": [
                    generate_web_input_summary(uuid.UUID(int=i), i) for i in range(20)
                ],
                "marker": "fake_marker_0",
            },
        ),
        RegisteredResponse(
            service="flows",
            path="/web_inputs",
            json={
                "web_input_summaries": [
                    generate_web_input_summary(uuid.UUID(int=i), i)
                    for i in range(20, 40)
                ],
                "marker": "fake_marker_1",
            },
            # `strict_match=False` so this matches regardless of what other query
            # params (orderby, filter_roles, etc.) a given caller also sends.
            match=[
                matchers.query_param_matcher(
                    {"marker": "fake_marker_0"}, strict_match=False
                )
            ],
        ),
        RegisteredResponse(
            service="flows",
            path="/web_inputs",
            json={
                "web_input_summaries": [
                    generate_web_input_summary(uuid.UUID(int=i), i)
                    for i in range(40, 60)
                ],
                "marker": None,
            },
            match=[
                matchers.query_param_matcher(
                    {"marker": "fake_marker_1"}, strict_match=False
                )
            ],
        ),
        metadata={
            "num_pages": 3,
            "expect_markers": ["fake_marker_0", "fake_marker_1", None],
            "total_items": 60,
        },
    ),
)
