"""Bounded canonical directory metadata; no OSS list, URLs or legacy fallback.

A page may truthfully report skipped pending/corrupt metadata. Iterators and
aggregate conveniences reject such pages as incomplete. Pagination observes a
live namespace, not a snapshot; directory_exists is positive evidence accumulated
across pages, and an absent/false page field alone never proves absence.
"""
from __future__ import annotations

import json
import math
import re
from dataclasses import asdict, dataclass, replace
from urllib.parse import urlencode

from ..errors import SchemaError, TransportError
from ._rfc3339 import parse_utc
from .user_data_reads import map_user_data_read_error
from .user_data_writes import (
    ReplicasPolicy, UserDataStorageLayoutClient, _Budget, _call_with_budget,
    _resolve_replica_policy,
)

PROTOCOL = "user-data-entries-v1"
STORAGE_ID = "ap-userdata-v1"
MAX_ROWS = 10000
MAX_BYTES = 32 * 1024 * 1024
MAX_PAGES = 512
MAX_CURSOR_BYTES = 24576
_PAGE_FIELDS = frozenset(("protocol", "storage_id", "owner", "relative_path",
    "cluster", "recursive", "entries", "next_cursor", "complete",
    "skipped_pending", "skipped_corrupt"))
_ROW_FIELDS = frozenset(("path", "name", "key", "type", "size", "modified"))
_UTC = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,9})?(?:Z|\+00:00)\Z")


class UserDataEntriesIncomplete(SchemaError):
    """Listing cannot be represented as a complete result; no raw payload."""
    def __init__(self, reason="incomplete metadata"):
        super().__init__("user-data entries incomplete: " + reason)


@dataclass(frozen=True)
class UserDataEntry:
    path: str
    name: str
    key: str
    type: str
    size: int | None
    modified: str | None


@dataclass(frozen=True)
class UserDataEntriesPage:
    protocol: str
    storage_id: str
    owner: str
    relative_path: str
    cluster: str
    recursive: bool
    entries: tuple[UserDataEntry, ...]
    next_cursor: str
    complete: bool
    skipped_pending: bool
    skipped_corrupt: bool
    directory_exists: bool | None = None


@dataclass(frozen=True)
class UserDataEntriesListing:
    entries: tuple[UserDataEntry, ...]
    # True if any page proves existence, False only if every clean page says
    # False, None for older servers without the optional projection field.
    directory_exists: bool | None


def _invalid():
    return SchemaError("invalid user-data entries schema or request")


def _text(value, limit, *, empty=False):
    if not isinstance(value, str) or len(value) > limit or (not value and not empty):
        raise _invalid()
    encoded = None
    try:
        encoded = value.encode("utf-8")
    except UnicodeError:
        pass
    # Raise after leaving the decoder handler: from None only hides a raw
    # UnicodeError whose .object can still retain a signed URL or user path.
    if encoded is None:
        raise _invalid()
    if len(encoded) > limit or any(ord(c) < 32 or ord(c) == 127 or c == "\\" for c in value):
        raise _invalid()
    return value


def _path(value, *, root=False, directory=False):
    value = _text(value, 4096, empty=root)
    if value == "" and root:
        return value
    if directory:
        if not value.endswith("/"):
            raise _invalid()
        body = value[:-1]
    else:
        body = value
    if "%" in body or len(body.split("/")) > 64 or any(p in ("", ".", "..") for p in body.split("/")):
        raise _invalid()
    return value


def _cursor(value):
    # Opaque ASCII token: never decode it into authorization or edit it.
    value = _text(value, MAX_CURSOR_BYTES, empty=True)
    if value and not re.fullmatch(r"[A-Za-z0-9_-]+", value):
        raise _invalid()
    return value


def _budget(seconds):
    try:
        valid = not isinstance(seconds, bool) and isinstance(seconds, (int, float)) and math.isfinite(seconds) and seconds >= 0
    except (OverflowError, ValueError):
        valid = False
    if not valid:
        raise _invalid()
    return _Budget(seconds)


def _bound(value, maximum):
    if type(value) is not int or not 1 <= value <= maximum:
        raise _invalid()
    return value


def _timestamp(value):
    value = _text(value, 40)
    if not _UTC.fullmatch(value):
        raise _invalid()
    parsed = None
    try:
        parsed = parse_utc(value)
    except ValueError:
        pass
    if parsed is None:
        raise _invalid()
    return value


class UserDataEntriesClient:
    def __init__(self, transport, *, discovery=None,
                 expected_replica_policy: ReplicasPolicy | None = None):
        self._t = transport
        explicit = _resolve_replica_policy(expected_replica_policy)
        if discovery is not None:
            if not isinstance(discovery, UserDataStorageLayoutClient):
                raise SchemaError("discovery must be UserDataStorageLayoutClient")
            existing = discovery.replica_policy
            if explicit is not None and existing is not None and explicit != existing:
                raise SchemaError("conflicting entries/discovery replica policies")
            self._policy = explicit if explicit is not None else existing
        else:
            self._policy = explicit
        if self._policy is not None and self._policy.storage_id != STORAGE_ID:
            raise SchemaError("entries policy storage_id must be ap-userdata-v1")

    @property
    def replica_policy(self):
        return self._policy

    def _request(self, owner, relative_path, cluster, recursive, limit, cursor):
        if self._policy is None:
            raise SchemaError("entries client requires trusted expected replica policy before IO")
        owner = _text(owner, 128)
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", owner):
            raise _invalid()
        relative_path = _path(relative_path, root=True)
        cluster = _text(cluster, MAX_CURSOR_BYTES)
        if any(c.isspace() for c in cluster) or type(recursive) is not bool:
            raise _invalid()
        _bound(limit, 200)
        cursor = _cursor(cursor)
        return {"owner": owner, "relative_path": relative_path, "cluster": cluster,
                "recursive": recursive, "limit": limit, "cursor": cursor}

    def _fetch(self, request, budget):
        budget.raise_if_exhausted()
        query = dict(request)
        query["recursive"] = "true" if request["recursive"] else "false"
        safe_error = None
        try:
            raw = _call_with_budget(budget, self._t, "GET",
                "/apis/v1/user-data/entries?" + urlencode(query))
        except TransportError as exc:
            safe_error = map_user_data_read_error(exc)
        # Remote TransportError message/data may hold credentials. Sanitized
        # public errors must not retain it as implicit exception context.
        if safe_error is not None:
            raise safe_error
        page = self._parse(raw, request)
        budget.raise_if_exhausted()
        return page

    def _parse(self, raw, req):
        if not isinstance(raw, dict) or set(raw) not in (_PAGE_FIELDS, _PAGE_FIELDS | {"directory_exists"}):
            raise _invalid()
        for key in ("owner", "relative_path", "cluster", "recursive"):
            if type(raw[key]) is not type(req[key]) or raw[key] != req[key]:
                raise _invalid()
        if raw["protocol"] != PROTOCOL or raw["storage_id"] != self._policy.storage_id:
            raise _invalid()
        for key in ("complete", "skipped_pending", "skipped_corrupt"):
            if type(raw[key]) is not bool:
                raise _invalid()
        exists = raw.get("directory_exists")
        if "directory_exists" in raw and type(exists) is not bool:
            raise _invalid()
        next_cursor = _cursor(raw["next_cursor"])
        if raw["complete"] != (next_cursor == ""):
            raise _invalid()
        values = raw["entries"]
        if not isinstance(values, list) or len(values) > req["limit"]:
            raise _invalid()
        root = "swe/user-data/users/" + req["owner"] + "/"
        prefix = req["relative_path"] + "/" if req["relative_path"] else ""
        entries, seen = [], set()
        for row in values:
            if not isinstance(row, dict) or set(row) != _ROW_FIELDS or row["type"] not in ("file", "directory"):
                raise _invalid()
            directory = row["type"] == "directory"
            path = _path(row["path"], directory=directory)
            key = _text(row["key"], 1023)
            if key != root + path or not path.startswith(prefix) or path == prefix:
                raise _invalid()
            name = _text(row["name"], 4096)
            if name != path[len(prefix):] or (not req["recursive"] and "/" in name.rstrip("/")) or key in seen:
                raise _invalid()
            seen.add(key)
            size, modified = row["size"], row["modified"]
            if directory and size is None and modified is None:
                pass  # synthetic prefix directory, not a fabricated zero object
            else:
                if type(size) is not int or not 0 <= size <= 2**63 - 1 or (directory and size != 0):
                    raise _invalid()
                modified = _timestamp(modified)
            entries.append(UserDataEntry(path, name, key, row["type"], size, modified))
        return UserDataEntriesPage(PROTOCOL, raw["storage_id"], req["owner"], req["relative_path"],
            req["cluster"], req["recursive"], tuple(entries), next_cursor, raw["complete"],
            raw["skipped_pending"], raw["skipped_corrupt"], exists)

    def entries_page(self, *, owner, relative_path="", cluster, recursive=False,
                     limit=100, cursor="", deadline=30.0):
        budget = _budget(deadline)
        req = self._request(owner, relative_path, cluster, recursive, limit, cursor)
        return self._fetch(req, budget)

    def _iterator(self, *, owner, relative_path="", cluster, recursive=False,
                  page_size=200, deadline=60.0, max_rows=MAX_ROWS,
                  max_bytes=MAX_BYTES, max_pages=MAX_PAGES):
        budget = _budget(deadline)
        req = self._request(owner, relative_path, cluster, recursive, page_size, "")
        _bound(max_rows, MAX_ROWS); _bound(max_bytes, MAX_BYTES); _bound(max_pages, MAX_PAGES)
        return self._iterate_pages(req, budget, max_rows, max_bytes, max_pages), budget

    def _iterate_pages(self, req, budget, max_rows, max_bytes, max_pages):
        rows = total_bytes = 0
        cursors, keys = set(), set()
        observed_exists, all_known = False, True
        for _ in range(max_pages):
            page = self._fetch(req, budget)
            if page.skipped_pending or page.skipped_corrupt:
                raise UserDataEntriesIncomplete()
            rows += len(page.entries)
            total_bytes += len(json.dumps(asdict(page), ensure_ascii=True, separators=(",", ":")).encode("ascii"))
            if rows > max_rows or total_bytes > max_bytes:
                raise UserDataEntriesIncomplete("row or byte bound exceeded")
            for entry in page.entries:
                if entry.key in keys:
                    raise UserDataEntriesIncomplete("repeated entry across pages")
                keys.add(entry.key)
            if not page.complete and page.next_cursor in cursors:
                raise UserDataEntriesIncomplete("cursor did not advance")
            if not page.complete:
                cursors.add(page.next_cursor)
            observed_exists = observed_exists or page.directory_exists is True
            all_known = all_known and page.directory_exists is not None
            page = replace(page, directory_exists=(True if observed_exists else (False if all_known else None)))
            budget.raise_if_exhausted()
            yield page
            budget.raise_if_exhausted()  # consumer time also consumes the budget
            if page.complete:
                return
            req = dict(req, cursor=page.next_cursor)
        raise UserDataEntriesIncomplete("page bound exceeded")

    def iter_pages(self, *, owner, relative_path="", cluster, recursive=False,
                   page_size=200, deadline=60.0, max_rows=MAX_ROWS,
                   max_bytes=MAX_BYTES, max_pages=MAX_PAGES):
        # Bind the deadline when the iterator is constructed, not lazily at the
        # first request. The same budget covers every subsequent consumer yield.
        return self._iterator(owner=owner, relative_path=relative_path, cluster=cluster,
            recursive=recursive, page_size=page_size, deadline=deadline,
            max_rows=max_rows, max_bytes=max_bytes, max_pages=max_pages)[0]

    def iter_entries(self, **kwargs):
        pages, budget = self._iterator(**kwargs)
        def iterate():
            for page in pages:
                for entry in page.entries:
                    budget.raise_if_exhausted()
                    yield entry
                    budget.raise_if_exhausted()
        return iterate()

    def list_entries(self, **kwargs):
        pages, budget = self._iterator(**kwargs)
        entries, exists, all_known = [], False, True
        for page in pages:
            entries.extend(page.entries)
            exists = exists or page.directory_exists is True
            all_known = all_known and page.directory_exists is not None
        result = UserDataEntriesListing(tuple(entries), True if exists else (False if all_known else None))
        budget.raise_if_exhausted()
        return result
