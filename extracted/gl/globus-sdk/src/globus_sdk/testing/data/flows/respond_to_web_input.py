from globus_sdk.testing.models import RegisteredResponse, ResponseSet

from ._common import TWO_HOP_TRANSFER_FLOW_ID, TWO_HOP_TRANSFER_RUN_ID

WEB_INPUT_ID = "3d9a4e7b-1c2f-4b8a-9e6d-5f7a8b6c2d1e"
AUTHENTICATION_POLICY_ID = "6f2c1d7e-3b4a-4a5e-9f0f-8f2a1b7c4d9e"
OPTION_ID_APPROVE = "8f14e45f-ceea-467e-add1-6a6b672efe31"

RESPOND_OK_RESPONSE = {"status": "ok"}

NOT_FOUND_RESPONSE = {
    "error": {
        "code": "NOT_FOUND",
        "detail": f"No Web Input exists with id value {WEB_INPUT_ID}",
    }
}

CLOSED_RESPONSE = {
    "error": {
        "code": "STATE_CONFLICT",
        "detail": f"Web Input {WEB_INPUT_ID} is already closed.",
    }
}

# Raised by `_WebInputResponseController.authorize` when the caller has a viewer
# role, but not the respondent role required to submit a response.
FORBIDDEN_RESPONSE = {
    "error": {
        "code": "FORBIDDEN",
        "detail": f"User does not have respondent role on web input {WEB_INPUT_ID}",
    }
}

# Raised when the caller has the respondent role but fails the associated flow's
# authentication policy.
WEB_INPUT_SUMMARY_FOR_GARE = {
    "id": WEB_INPUT_ID,
    "status": "open",
    "user_roles": ["respondent"],
    "input_type": "selection",
    "title": "Approve deployment to production?",
    "flow": {
        "id": TWO_HOP_TRANSFER_FLOW_ID,
        "title": "Multi Step Transfer",
    },
    "run": {
        "id": TWO_HOP_TRANSFER_RUN_ID,
        "label": "Transfer all of these files!",
    },
    "created_timestamp": "2026-08-01T10:30:00+00:00",
    "edited_timestamp": "2026-08-01T10:30:00+00:00",
    "closed_timestamp": None,
}
AUTH_POLICY_REQUIRED_RESPONSE = {
    "web_input_summary": WEB_INPUT_SUMMARY_FOR_GARE,
    "error": {
        "code": "AUTHENTICATION_POLICY_REQUIRED",
        "detail": (
            "None of the identities in session for this authentication policy "
            "have the respondent role on this web input. Reauthenticate as an "
            "identity that has this permission and can meet the requirements "
            "for the attached authentication policy."
        ),
    },
    "code": "AuthenticationPolicyRequired",
    "authorization_parameters": {
        "session_required_policies": [AUTHENTICATION_POLICY_ID],
        "session_message": (
            "Globus Flows detected an unsatisfied session policy for this web input."
        ),
    },
}

# Raised by `_WebInputSelectionResponseController.process_response` when `value`
# does not match one of the web input's registered `option_id`s.
INVALID_OPTION_RESPONSE = {
    "error": {
        "code": "UNPROCESSABLE_ENTITY",
        "detail": "'not-a-real-option' is not a registered option id for this input.",
    }
}

RESPONSES = ResponseSet(
    metadata={
        "web_input_id": WEB_INPUT_ID,
        "option_id": OPTION_ID_APPROVE,
    },
    default=RegisteredResponse(
        service="flows",
        method="POST",
        path=f"/web_inputs/{WEB_INPUT_ID}/respond",
        json=RESPOND_OK_RESPONSE,
    ),
    not_found=RegisteredResponse(
        service="flows",
        method="POST",
        path=f"/web_inputs/{WEB_INPUT_ID}/respond",
        status=404,
        json=NOT_FOUND_RESPONSE,
    ),
    closed=RegisteredResponse(
        service="flows",
        method="POST",
        path=f"/web_inputs/{WEB_INPUT_ID}/respond",
        status=409,
        json=CLOSED_RESPONSE,
    ),
    forbidden=RegisteredResponse(
        service="flows",
        method="POST",
        path=f"/web_inputs/{WEB_INPUT_ID}/respond",
        status=403,
        json=FORBIDDEN_RESPONSE,
    ),
    auth_policy_required=RegisteredResponse(
        service="flows",
        method="POST",
        path=f"/web_inputs/{WEB_INPUT_ID}/respond",
        status=403,
        json=AUTH_POLICY_REQUIRED_RESPONSE,
    ),
    invalid_option=RegisteredResponse(
        service="flows",
        method="POST",
        path=f"/web_inputs/{WEB_INPUT_ID}/respond",
        status=422,
        json=INVALID_OPTION_RESPONSE,
    ),
)
