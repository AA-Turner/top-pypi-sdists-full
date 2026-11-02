"""Historical ranges must use immutable object storage, not whole-file buffering."""
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_files.cloud_sync.download_stream import BoundedStreamingUnavailable, DownloadStreamer
from matrx_files.service import FileService


class Body:
    def __init__(self, data):
        self.data, self.closed, self.read_sizes = data, False, []

    def iter_chunks(self, chunk_size):
        self.read_sizes.append(chunk_size)
        for i in range(0, len(self.data), chunk_size):
            yield self.data[i:i + chunk_size]

    def close(self):
        self.closed = True


class ObjectPeer:
    def __init__(self):
        self.calls, self.body = [], None

    def head_object(self, **kw):
        self.calls.append(("head", kw))
        return {"ContentLength": 10}

    def get_object(self, **kw) -> dict[str, Any]:
        self.calls.append(("get", kw))
        data = b"0123456789"
        if "Range" in kw:
            start, end = map(int, kw["Range"].removeprefix("bytes=").split("-"))
            data = data[start:end + 1]
        self.body = Body(data)
        return {"Body": self.body}


class Versions:
    def __init__(self, present=True):
        self.lookups, self.present = [], present

    async def get_version_async(self, file_id, version):
        self.lookups.append((file_id, version))
        return {"file_id": file_id, "version_number": version, "storage_uri": "s3://archive/old.mp4",
                "size_bytes": 10, "checksum": "old-checksum"} if self.present else None

    async def read_version_async(self, *_):
        raise AssertionError("Historical S3 reads must not buffer the whole video.")


class Router:
    def __init__(self, peer, configured=True):
        self.configured, self.buffer_reads = configured, []
        self.s3 = SimpleNamespace(_get_client=lambda: peer, _parse_path=lambda path: tuple(path.split("/", 1)))

    def is_configured(self, backend):
        return backend == "s3" and self.configured

    async def read_async(self, uri):
        self.buffer_reads.append(uri)
        return b"0123456789"


CURRENT = {"id": "saved-video", "file_name": "video.mp4", "mime_type": "video/mp4",
           "storage_uri": "s3://current/current.mp4", "canonical_storage_uri": "s3://current/new.mp4",
           "size_bytes": 99, "checksum": "new-checksum"}


@pytest.mark.asyncio
async def test_pinned_s3_range_reads_only_old_object_and_closes_body():
    peer, versions = ObjectPeer(), Versions()
    router = Router(peer)
    stream = await DownloadStreamer(SimpleNamespace(router=router, versions=versions)).open_stream(
        CURRENT, version=2, range_header="bytes=2-5", require_bounded=True)
    data = b"".join(stream.iterator)
    assert data == b"2345"
    assert stream.status_code == 206 and stream.content_length == 4
    assert stream.headers["Content-Range"] == "bytes 2-5/10"
    assert stream.headers["ETag"] == '"old-checksum"'
    assert peer.calls == [("get", {"Bucket": "archive", "Key": "old.mp4", "Range": "bytes=2-5"})]
    assert versions.lookups == [("saved-video", 2)]
    assert router.buffer_reads == [] and peer.body.closed
    assert max(peer.body.read_sizes) <= 256 * 1024


@pytest.mark.asyncio
async def test_missing_pinned_version_never_falls_through_to_current_bytes():
    peer, versions = ObjectPeer(), Versions(present=False)
    with pytest.raises(FileNotFoundError):
        await DownloadStreamer(SimpleNamespace(router=Router(peer), versions=versions)).open_stream(CURRENT, version=2)
    assert peer.calls == []


@pytest.mark.asyncio
async def test_pinned_unsatisfiable_range_reports_old_size_without_opening_object():
    peer = ObjectPeer()
    stream = await DownloadStreamer(SimpleNamespace(router=Router(peer), versions=Versions())).open_stream(
        CURRENT, version=2, range_header="bytes=10-20")
    assert stream.status_code == 416 and stream.headers["Content-Range"] == "bytes */10"
    assert b"".join(stream.iterator) == b"" and peer.calls == []


@pytest.mark.asyncio
@pytest.mark.parametrize("requested,expected,status", [
    ("bytes=2-5", b"2345", 206), ("bytes=-3", b"789", 206),
    ("bytes=10-20", b"", 416), (None, b"0123456789", 200),
])
async def test_non_s3_backend_range_is_not_misrouted_to_configured_s3(requested, expected, status):
    peer = ObjectPeer()
    router = Router(peer)
    record = CURRENT | {"storage_uri": "server://video.mp4", "canonical_storage_uri": None, "size_bytes": 10}
    stream = await DownloadStreamer(SimpleNamespace(router=router, versions=Versions())).open_stream(
        record, range_header=requested)
    assert stream.status_code == status
    assert b"".join(stream.iterator) == expected
    assert stream.content_length == len(expected)
    assert router.buffer_reads == ["server://video.mp4"]
    assert peer.calls == []


@pytest.mark.asyncio
async def test_bounded_requirement_refuses_before_non_s3_whole_file_allocation():
    peer, versions = ObjectPeer(), Versions()
    router = Router(peer)
    record = CURRENT | {"canonical_storage_uri": None, "storage_uri": "server://video.mp4"}
    with pytest.raises(BoundedStreamingUnavailable):
        await DownloadStreamer(SimpleNamespace(router=router, versions=versions)).open_stream(
            record, require_bounded=True, range_header="bytes=0-3")
    assert peer.calls == [] and router.buffer_reads == []


@pytest.mark.asyncio
async def test_current_s3_range_and_early_close_preserve_canonical_streaming():
    peer = ObjectPeer()
    router = Router(peer)
    stream = await DownloadStreamer(SimpleNamespace(router=router)).open_stream(
        CURRENT | {"size_bytes": 10}, range_header="bytes=1-3", require_bounded=True)
    assert next(stream.iterator) == b"123"
    stream.iterator.close()
    assert peer.body.closed and router.buffer_reads == []
    assert stream.headers["ETag"] == '"new-checksum"'
    assert peer.calls == [("get", {"Bucket": "current", "Key": "new.mp4", "Range": "bytes=1-3"})]


@pytest.mark.asyncio
@pytest.mark.parametrize("allowed", [True, False])
async def test_facade_admits_actor_before_version_lookup_or_storage(allowed):
    peer, versions = ObjectPeer(), Versions()
    engine = SimpleNamespace(router=Router(peer), versions=versions)
    async def authorize(file_id, *, user_id, level):
        assert (file_id, user_id, level) == ("saved-video", "authorized-owner", "read")
        assert versions.lookups == [] and peer.calls == []
        if not allowed:
            raise PermissionError("No file access.")
        return CURRENT
    engine.get_authorized_record_async = authorize
    engine.streamer = DownloadStreamer(engine)
    service = FileService(SimpleNamespace(sync_engine=engine))
    if allowed:
        stream = await service.open_stream("saved-video", user_id="authorized-owner", version=2,
                                          range_header="bytes=2-5", require_bounded=True)
        assert b"".join(stream.iterator) == b"2345"
    else:
        with pytest.raises(PermissionError):
            await service.open_stream("saved-video", user_id="authorized-owner", version=2, require_bounded=True)
        assert versions.lookups == [] and peer.calls == []


@pytest.mark.asyncio
async def test_rejected_stream_closes_s3_body_without_reading_first_chunk():
    peer = ObjectPeer()
    stream = await DownloadStreamer(SimpleNamespace(router=Router(peer))).open_stream(
        CURRENT | {"size_bytes": 10}, require_bounded=True)
    stream.iterator.close()
    assert peer.body.closed
    assert peer.body.read_sizes == []


@pytest.mark.asyncio
async def test_conditional_s3_read_binds_actual_storage_revision_not_file_checksum():
    class ConditionalPeer(ObjectPeer):
        def get_object(self, **kw) -> dict[str, Any]:
            result = super().get_object(**kw)
            return result | {"ETag": '"stored-revision"'}
    peer = ConditionalPeer()
    stream = await DownloadStreamer(SimpleNamespace(router=Router(peer), versions=Versions())).open_stream(
        CURRENT, version=2, range_header="bytes=1-3", require_bounded=True,
        expected_storage_etag='"stored-revision"')
    assert peer.calls == [("get", {"Bucket": "archive", "Key": "old.mp4", "Range": "bytes=1-3",
                                  "IfMatch": '"stored-revision"'})]
    assert stream.storage_etag == '"stored-revision"'
    assert stream.headers["ETag"] == '"old-checksum"'
    assert b"".join(stream.iterator) == b"123"


@pytest.mark.asyncio
async def test_storage_response_drift_rejects_and_closes_before_reading():
    class DriftingPeer(ObjectPeer):
        def get_object(self, **kw) -> dict[str, Any]:
            return super().get_object(**kw) | {"ETag": '"changed"'}
    peer = DriftingPeer()
    with pytest.raises(RuntimeError, match="revision"):
        await DownloadStreamer(SimpleNamespace(router=Router(peer))).open_stream(
            CURRENT, require_bounded=True, expected_storage_etag='"verified"')
    assert peer.body.closed and not peer.body.read_sizes


@pytest.mark.asyncio
async def test_conditional_non_s3_read_refuses_before_buffering():
    peer = ObjectPeer()
    router = Router(peer)
    with pytest.raises(BoundedStreamingUnavailable):
        await DownloadStreamer(SimpleNamespace(router=router)).open_stream(
            CURRENT | {"canonical_storage_uri": "server://file.mp4"},
            expected_storage_etag='"verified"')
    assert router.buffer_reads == [] and peer.calls == []


@pytest.mark.asyncio
async def test_storage_precondition_failure_never_returns_or_retries_a_body():
    from botocore.exceptions import ClientError
    from matrx_files.cloud_sync.download_stream import StorageRevisionChanged
    class ReplacedPeer(ObjectPeer):
        def get_object(self, **kw) -> dict[str, Any]:
            self.calls.append(("get", kw))
            raise ClientError({"Error": {"Code": "PreconditionFailed"},
                               "ResponseMetadata": {"HTTPStatusCode": 412}}, "GetObject")
    peer = ReplacedPeer()
    with pytest.raises(StorageRevisionChanged):
        await DownloadStreamer(SimpleNamespace(router=Router(peer))).open_stream(
            CURRENT, range_header="bytes=0-1", expected_storage_etag='"verified"')
    assert len(peer.calls) == 1 and peer.body is None


@pytest.mark.asyncio
@pytest.mark.parametrize("tag", ['"x"\r\nIf-Match: *', '*', '"a", "b"', '""'])
async def test_invalid_storage_revision_never_reaches_storage(tag):
    peer = ObjectPeer()
    with pytest.raises(ValueError):
        await DownloadStreamer(SimpleNamespace(router=Router(peer))).open_stream(
            CURRENT, expected_storage_etag=tag)
    assert peer.calls == []
