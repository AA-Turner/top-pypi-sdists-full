from __future__ import annotations

import re
from typing import Any


class StopAsyncIterationWithResult(Exception):
    def __init__(self, value):
        self.value = value


class ApiConnectionError(ConnectionError):
    def __init__(self, method_name, response, client, max_message_length=10000):
        self.method_name = method_name
        self.response = response
        self.client = client

        message = (
            "{method_name} failed with status code {code} and response\n{response}"
        )
        status_code = getattr(response, "status_code", "Unknown")
        content = getattr(response, "content", "No content available")
        message = message.format(
            method_name=method_name, code=status_code, response=content
        )
        if len(message) > max_message_length:
            message = message[: max_message_length - 3] + "..."
        super().__init__(message)


# FIXME: TEAM-6154 — drop this regex once the server returns the
# rejected field as a structured attribute on EntityError. Today
# UpsertResponse carries each rejection only as a free-form
# ``error: str``, so we extract the field name client-side to
# populate ``invalid_fields``.
#
# Matches per-field server validation rejections inside an entity's error text:
#   "Invalid <type> value for field '<name>'[: '<value>']"
_FIELD_FAILURE_RE = re.compile(
    r"Invalid\s+\S+\s+value\s+for\s+field\s+'(?P<field>[^']+)'",
    re.IGNORECASE,
)

# FIXME: TEAM-6154 — drop this regex too, same task as
# _FIELD_FAILURE_RE above. The server should expose the rejected
# reserved-keyword token as a structured attribute on EntityError.
#
# Matches "reserved keyword" mentions inside an entity's error text, capturing
# the offending token when it appears quoted (e.g. ``reserved keyword 'call'``).
# Some backends omit the quotes, so callers should also fall back to
# ``"reserved keyword" in err["error"]`` for boolean detection.
_RESERVED_KEYWORD_RE = re.compile(
    r"reserved\s+keyword[^'\"]*['\"](?P<keyword>[^'\"]+)['\"]",
    re.IGNORECASE,
)


class ApiValidationError(ApiConnectionError):
    """Raised when the server accepted the upsert request but rejected one
    or more entities server-side.

    Subclass of :class:`ApiConnectionError`, so handlers catching the
    parent class still receive validation failures.

    The per-entity breakdown is exposed via structured attributes:

    Attributes:
        entity_errors: ``list[dict]`` — ``[{"entity_id": str, "error":
            str}, ...]``, the per-entity error rows as returned by the
            server. Use this when you need the raw message text for
            each failing entity.
        missing_entity_ids: ``set[str]`` — IDs that were sent but appear
            in neither ``response.entities`` nor ``response.errors``.
            The server has no record of these: neither written nor
            explicitly rejected.
        mismatched_keys: ``list[tuple[str, str]]`` — ``(entity_id,
            os_workspace)`` pairs the server returned under an
            ``os_workspace`` different from the one you sent. Typically
            indicates a stale record was matched; refetching is the
            usual recovery.
        invalid_fields: ``dict[str, list[str]]`` — ``{entity_id:
            [field_name, ...]}`` covering per-field rejections
            (malformed datetime, bad number, etc.). To recover, drop
            the listed fields from the payload for each entity and
            re-upsert.
        reserved_keyword_entity_types: ``set[str]`` — entity-type
            tokens the server's query parser flagged as reserved
            keywords (e.g. Cypher ``call``, ``match``). Resolution is
            usually renaming the entity type at the source ontology.
    """

    def __init__(
        self,
        method_name,
        response,
        client,
        *,
        entity_errors: list[dict[str, Any]] | None = None,
        missing_entity_ids: set[str] | None = None,
        mismatched_keys: list[tuple[str, str]] | None = None,
        max_message_length: int = 10000,
    ):
        self.entity_errors: list[dict[str, Any]] = list(entity_errors or [])
        self.missing_entity_ids: set[str] = set(missing_entity_ids or ())
        self.mismatched_keys: list[tuple[str, str]] = list(mismatched_keys or ())
        super().__init__(
            method_name, response, client, max_message_length=max_message_length
        )

    @property
    def invalid_fields(self) -> dict[str, list[str]]:
        """Per-entity invalid field names parsed from the server's error strings."""
        result: dict[str, list[str]] = {}
        for err in self.entity_errors:
            entity_id = err.get("entity_id")
            error_text = err.get("error") or ""
            if not entity_id:
                continue
            for m in _FIELD_FAILURE_RE.finditer(error_text):
                bucket = result.setdefault(entity_id, [])
                field = m.group("field")
                if field not in bucket:
                    bucket.append(field)
        return result

    @property
    def reserved_keyword_entity_types(self) -> set[str]:
        """Entity-type tokens extracted from quoted "reserved keyword '<x>'" mentions."""
        result: set[str] = set()
        for err in self.entity_errors:
            error_text = err.get("error") or ""
            for m in _RESERVED_KEYWORD_RE.finditer(error_text):
                result.add(m.group("keyword"))
        return result
