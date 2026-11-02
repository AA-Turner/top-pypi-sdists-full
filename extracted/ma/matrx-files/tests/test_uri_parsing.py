"""The URI-parsing primitive — the layer that silently returned [] for years.

`parse_uri("s3://bucket/")` used to collapse to "bucket". S3Backend then could
not tell "the whole bucket" from "a key prefix in the default bucket", picked the
latter, and listed with Prefix="bucket" — which matches nothing. So EVERY
bucket-root listing silently returned an empty list, and any reconciler built on
it would have cheerfully reported "no orphans" forever.

Nothing covered this primitive. These tests pin it, and pin that
`router.parse_uri` and `url_parser.parse_storage_url` (public API, its
storage_path is handed straight to a backend) agree — if they drift, the bug
comes back through the other door.
"""

from __future__ import annotations

import pytest
from matrx_files.backends.router import parse_uri
from matrx_files.backends.url_parser import parse_storage_url
from matrx_files.cloud_sync.config import CloudSyncConfig


@pytest.mark.parametrize(
    ("uri", "expected"),
    [
        ("s3://my-bucket/reports/jan.json", ("s3", "my-bucket/reports/jan.json")),
        ("s3://my-bucket/owner/file-id", ("s3", "my-bucket/owner/file-id")),
        # Keys legitimately contain spaces — they must survive verbatim.
        ("s3://b/owner/Inside Matters/DSC09357.jpg", ("s3", "b/owner/Inside Matters/DSC09357.jpg")),
        ("server://uploads/file.txt", ("server", "uploads/file.txt")),
        # THE REGRESSION: bucket root must keep its separator.
        ("s3://my-bucket/", ("s3", "my-bucket/")),
        ("s3://my-bucket", ("s3", "my-bucket/")),
    ],
)
def test_parse_uri(uri: str, expected: tuple[str, str]) -> None:
    assert parse_uri(uri) == expected


def test_bucket_root_is_distinguishable_from_a_key_prefix() -> None:
    """The whole point: a bucket root must NOT look like a bare key prefix."""
    _, root = parse_uri("s3://my-bucket/")
    assert root.endswith("/"), "bucket root lost its separator — listings silently return []"
    _, keyed = parse_uri("s3://my-bucket/some/key")
    assert not keyed.endswith("/")


@pytest.mark.parametrize(
    "uri",
    ["s3://b/owner/file", "s3://b/", "s3://b", "server://u/f.txt"],
)
def test_the_two_parsers_agree(uri: str) -> None:
    """parse_storage_url is public API and its storage_path goes straight to a
    backend. If it disagrees with parse_uri, the bug returns via the other door."""
    scheme, path = parse_uri(uri)
    parsed = parse_storage_url(uri)
    assert (parsed.scheme, parsed.storage_path) == (scheme, path)


def test_unknown_scheme_raises() -> None:
    with pytest.raises(ValueError):
        parse_uri("ftp://host/path")


def test_cloud_sync_rejects_non_s3_byte_backends() -> None:
    with pytest.raises(ValueError, match="must be 's3'"):
        CloudSyncConfig(storage_backend="retired")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Batch delete — per-key errors are RETURNED, never raised. One bad key must
# not abort a bulk reclaim (a 13k-object purge that dies on object #3 is worse
# than useless: it leaves the reclaim half-done with no report of what landed).
# ---------------------------------------------------------------------------


class _FlakyBackend:
    """Minimal StorageBackend stand-in: delete() raises for one key."""

    def __init__(self) -> None:
        self.deleted: list[str] = []

    def delete(self, path: str) -> bool:
        if "boom" in path:
            raise RuntimeError("access denied")
        self.deleted.append(path)
        return True


def test_delete_many_default_isolates_per_key_errors() -> None:
    from matrx_files.backends.base_backend import StorageBackend

    b = _FlakyBackend()
    deleted, errors = StorageBackend.delete_many(b, ["a", "boom", "c"])  # type: ignore[arg-type]

    assert deleted == 2
    assert b.deleted == ["a", "c"], "a failing key must not stop the others"
    assert len(errors) == 1 and errors[0][0] == "boom"
    assert "access denied" in errors[0][1]


def _fake_s3(client):
    from matrx_files.backends.s3_backend import S3Backend

    s3 = object.__new__(S3Backend)
    s3._require_configured = lambda: None  # type: ignore[method-assign]
    s3._get_client = lambda: client  # type: ignore[method-assign]
    s3._parse_path = lambda p: (p.split("/", 1)[0], p.split("/", 1)[1])  # type: ignore[method-assign]
    return s3


def test_s3_delete_many_chunks_at_the_1000_key_api_limit() -> None:
    """S3 DeleteObjects hard-caps at 1000 keys; a 2500-key purge must not send
    one oversized request (S3 rejects it) nor 2500 individual ones."""
    calls: list[int] = []

    class _FakeClient:
        def delete_objects(self, Bucket, Delete):  # noqa: N803
            calls.append(len(Delete["Objects"]))
            return {}

    deleted, errors = _fake_s3(_FakeClient()).delete_many([f"bkt/key-{i}" for i in range(2500)])

    assert calls == [1000, 1000, 500]
    assert deleted == 2500 and not errors


def test_s3_delete_many_returns_the_path_it_was_given() -> None:
    """Contract: an error carries the INPUT path, identical to the base impl.
    Returning a re-derived `s3://…` URI silently disagreed with the base class
    and broke callers matching errors against their own input."""

    class _FakeClient:
        def delete_objects(self, Bucket, Delete):  # noqa: N803
            return {"Errors": [{"Key": "own/bad", "Message": "AccessDenied"}]}

    deleted, errors = _fake_s3(_FakeClient()).delete_many(["bkt/own/bad", "bkt/own/ok"])

    assert deleted == 1
    assert errors == [("bkt/own/bad", "AccessDenied")], "must echo the input path verbatim"


def test_s3_delete_many_survives_a_failing_chunk() -> None:
    """A throttle/5xx must not abort the reclaim and lose the count of what
    already landed — every key in the failed chunk is reported, nothing raises."""

    class _BoomClient:
        def delete_objects(self, Bucket, Delete):  # noqa: N803
            raise RuntimeError("SlowDown")

    deleted, errors = _fake_s3(_BoomClient()).delete_many(["bkt/a", "bkt/b"])

    assert deleted == 0
    assert {u for u, _ in errors} == {"bkt/a", "bkt/b"}
    assert all("SlowDown" in e for _, e in errors)
