"""Typed server-owned canonical directories; no client OSS/STS or reconciliation.

The existing Transport returns bodies, not the HTTP status of successful 2xx
responses. We enforce the server's state/code/progress contract, without claiming
an independent HTTP200-versus202 binding or fabricating an object receipt.
"""
from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass

from ..errors import SchemaError, TransportError
from .user_data_writes import (
    ReplicasPolicy, StorageDualUnavailable, UserDataStorageLayoutClient,
    UserDataUpgradeRequired, _Budget, _call_with_budget, _resolve_replica_policy,
    map_user_data_write_error,
)

PROTOCOL = "user-data-directory-v1"
STORAGE_ID = "ap-userdata-v1"
_BASE_FIELDS = frozenset(("protocol", "owner", "relative_path", "status", "created", "retained"))
_OPTIONAL_FIELDS = frozenset(("code", "pending_op_id"))
_INCOMPLETE_CODES = frozenset(range(94100, 94110)) | {94022, 10003}
_OWNER = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")
_UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\Z")
_OP_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}\Z")


def _invalid():
    return SchemaError("invalid user-data directory request or response")


def _text(value, limit):
    if not isinstance(value, str) or not value or len(value) > limit:
        raise _invalid()
    encoded = None
    try:
        encoded = value.encode("utf-8")
    except UnicodeError:
        pass
    # UnicodeError.object may retain an entire private URI. Raise after leaving
    # that handler, rather than merely hiding its implicit context with fromNone.
    if encoded is None or len(encoded) > limit or any(ord(c) < 32 or ord(c) == 127 or c == "\\" for c in value):
        raise _invalid()
    return value


def _finite_budget(seconds):
    valid = False
    try:
        valid = type(seconds) in (int, float) and math.isfinite(seconds) and seconds >= 0
    except (OverflowError, ValueError):
        pass
    if not valid:
        raise _invalid()
    return _Budget(seconds)


@dataclass(frozen=True)
class UserDataDirectoryOutcome:
    protocol: str
    owner: str
    relative_path: str
    status: str
    created: tuple[str, ...]
    retained: tuple[str, ...]
    code: int | None = None
    pending_op_id: str | None = None

    @property
    def complete(self) -> bool:
        return self.status in ("committed", "retained")


class UserDataDirectoriesClient:
    def __init__(self, transport, *, discovery=None, expected_replica_policy: ReplicasPolicy | None = None):
        self._t = transport
        policy = None
        invalid = False
        try:
            policy = _resolve_replica_policy(expected_replica_policy)
        except SchemaError:
            invalid = True
        if invalid:
            raise _invalid()
        if discovery is not None:
            if not isinstance(discovery, UserDataStorageLayoutClient):
                raise _invalid()
            existing = discovery.replica_policy
            if policy is not None and existing is not None and policy != existing:
                raise _invalid()
            policy = policy if policy is not None else existing
        if policy is not None and policy.storage_id != STORAGE_ID:
            raise _invalid()
        self._policy = policy
        # A supplied unbound discovery object remains untouched. Own a native
        # validated client instead of mutating its policy behind the caller.
        self._discovery = (discovery if discovery is not None and discovery.replica_policy is not None
                           else UserDataStorageLayoutClient(transport, expected_replica_policy=policy))

    @property
    def replica_policy(self):
        return self._policy

    def mkdir(self, *, owner, relative_path, cluster, parents=False,
              idempotency_key, deadline=30.0) -> UserDataDirectoryOutcome:
        budget = _finite_budget(deadline)
        if self._policy is None:
            raise UserDataUpgradeRequired("directory client requires trusted replica policy before IO", biz_code=94106)
        owner = _text(owner, 128)
        path = _text(relative_path, 4096)
        cluster = _text(cluster, 16384)
        key = _text(idempotency_key, 36)
        segments = path.split("/")
        if (not _OWNER.fullmatch(owner) or not _UUID.fullmatch(key) or type(parents) is not bool
                or any(c.isspace() for c in cluster) or "%" in path or len(segments) > 64
                or any(segment in ("", ".", "..") for segment in segments)
                or len(("swe/user-data/users/" + owner + "/" + path + "/").encode("utf-8")) > 1023):
            raise _invalid()
        request = dict(protocol=PROTOCOL, owner=owner, relative_path=path,
                       cluster=cluster, parents=parents, idempotency_key=key)
        if len(json.dumps(request).encode("utf-8")) > 16 * 1024:
            raise _invalid()
        budget.raise_if_exhausted()
        safe_error = None
        try:
            layout = self._discovery.get_storage_layout(cluster, budget=budget)
        except TransportError as exc:
            safe_error = map_user_data_write_error(exc)
        except SchemaError:
            safe_error = _invalid()
        if safe_error is not None:
            raise safe_error
        budget.raise_if_exhausted()
        if not layout.write_ready:
            raise StorageDualUnavailable("directory write capability unavailable", biz_code=94101)
        safe_error = None
        try:
            # Existing native Transport.post defaults idempotent=False. Never
            # request retry merely because this protocol carries an idem key.
            raw = _call_with_budget(budget, self._t, "POST", "/apis/v1/user-data/directories", request)
        except TransportError as exc:
            safe_error = map_user_data_write_error(exc)
        except SchemaError:
            safe_error = _invalid()
        if safe_error is not None:
            raise safe_error
        budget.raise_if_exhausted()
        result = self._parse(raw, request)
        budget.raise_if_exhausted()
        return result

    def _parse(self, raw, request):
        if not isinstance(raw, dict) or not 6 <= len(raw) <= 8:
            raise _invalid()
        fields = set(raw)
        if not _BASE_FIELDS <= fields or fields - _BASE_FIELDS - _OPTIONAL_FIELDS:
            raise _invalid()
        if raw["protocol"] != PROTOCOL or raw["owner"] != request["owner"] or raw["relative_path"] != request["relative_path"]:
            raise _invalid()
        status = raw["status"]
        if status not in ("committed", "retained", "pending", "partial"):
            raise _invalid()
        created, retained = raw["created"], raw["retained"]
        if not isinstance(created, list) or not isinstance(retained, list) or len(created) + len(retained) > 64:
            raise _invalid()
        segments = request["relative_path"].split("/")
        prefixes = ["/".join(segments[:i]) for i in range(1, len(segments) + 1)]
        indices = {path: i for i, path in enumerate(prefixes)}
        consumed = []
        metadata_bytes = 0
        for paths in (created, retained):
            positions = []
            for path in paths:
                path = _text(path, 4096)
                if path not in indices:
                    raise _invalid()
                positions.append(indices[path])
                metadata_bytes += len(path.encode("utf-8"))
            if positions != sorted(set(positions)):
                raise _invalid()
            consumed.extend(positions)
        if metadata_bytes > 64 * 1024 or len(set(consumed)) != len(consumed) or set(consumed) != set(range(len(consumed))):
            raise _invalid()
        complete = status in ("committed", "retained")
        if complete:
            if (len(consumed) != len(prefixes) or "code" in raw or "pending_op_id" in raw
                    or (status == "committed" and not created) or (status == "retained" and created)):
                raise _invalid()
            code, pending = None, None
        else:
            code = raw.get("code")
            if type(code) is not int or code not in _INCOMPLETE_CODES or (status == "pending") != (code == 94103):
                raise _invalid()
            pending = raw.get("pending_op_id")
            if "pending_op_id" in raw and not _OP_ID.fullmatch(_text(pending, 128)):
                raise _invalid()
        # Project only validated immutable values. Partial auth codes preserve
        # earlier parent progress; they are not a complete receipt or a new POST.
        return UserDataDirectoryOutcome(PROTOCOL, request["owner"], request["relative_path"],
                                        status, tuple(created), tuple(retained), code, pending)
