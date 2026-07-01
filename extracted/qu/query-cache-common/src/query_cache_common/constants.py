from __future__ import annotations

REQUEST_ID_HEADER = "x-request-id"
SESSION_ID_HEADER = "x-session-id"
SUBMITTED_AT_EPOCH_HEADER = "x-submitted-at-epoch"
ORG_ID_HEADER = "x-organization-id"
SYSTEM_USER_ID_HEADER = "x-system-user-id"
OS_NAME_HEADER = "x-os-name"

NO_OP_STATUS = "NO-OP"

SUPPORTED_DIALECT_TIME_TRAVEL_DEFAULTS: dict[str, int] = {
    "bigquery": 604800,
}
