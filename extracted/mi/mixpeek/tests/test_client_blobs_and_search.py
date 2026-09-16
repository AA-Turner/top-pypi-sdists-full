"""Blob entries built by Buckets.upload and Mixpeek.index, and the query mapping
in Mixpeek.search. No network: the client's HTTP helper is replaced per test."""

import pytest

from mixpeek._client.client import Mixpeek

VIDEO_BUCKET = {"bucket_id": "bkt_1", "bucket_schema": {"properties": {"video": {"type": "video"}, "title": {"type": "string"}}}}
TWO_FILE_BUCKET = {"bucket_id": "bkt_2", "bucket_schema": {"properties": {"video": {"type": "video"}, "thumb": {"type": "image"}}}}
NO_FILE_BUCKET = {"bucket_id": "bkt_3", "bucket_schema": {"properties": {"title": {"type": "string"}}}}


class Recorder:
    def __init__(self, responses):
        self.calls = []
        self.responses = responses

    def __call__(self, method, path, *, body=None, namespace=None):
        self.calls.append((method, path, body, namespace))
        for (m, exact), value in self.responses.items():
            if m == method and path == exact:
                return value
        return {}

    def of(self, method, path=None):
        return [c for c in self.calls if c[0] == method and (path is None or c[1] == path)]


def make_client(monkeypatch, responses):
    client = Mixpeek(api_key="sk_test", namespace="ns_test")
    rec = Recorder(responses)
    monkeypatch.setattr(client, "_request", rec)
    return client, rec


def test_upload_url_uses_the_single_file_property(monkeypatch):
    client, rec = make_client(monkeypatch, {("GET", "/buckets/bkt_1"): VIDEO_BUCKET})
    client.buckets.upload("bkt_1", url="s3://b/clip.mp4")
    (post,) = rec.of("POST", "/buckets/bkt_1/objects")
    assert post[2] == {"blobs": [{"property": "video", "type": "video", "data": "s3://b/clip.mp4"}]}
    assert len(rec.of("GET")) == 1


def test_upload_names_the_properties_when_there_are_several(monkeypatch):
    client, rec = make_client(monkeypatch, {("GET", "/buckets/bkt_2"): TWO_FILE_BUCKET})
    with pytest.raises(ValueError, match="thumb, video"):
        client.buckets.upload("bkt_2", url="s3://b/clip.mp4")
    assert rec.of("POST") == []


def test_upload_explains_a_bucket_with_no_file_property(monkeypatch):
    client, rec = make_client(monkeypatch, {("GET", "/buckets/bkt_3"): NO_FILE_BUCKET})
    with pytest.raises(ValueError, match="no file property"):
        client.buckets.upload("bkt_3", url="s3://b/notes.txt")
    assert rec.of("POST") == []


def test_blob_property_with_a_known_type_skips_the_read(monkeypatch):
    client, rec = make_client(monkeypatch, {("GET", "/buckets/bkt_2"): TWO_FILE_BUCKET})
    client.buckets.upload("bkt_2", url="https://x/frame.jpg", blob_property="thumb")
    client.buckets.upload("bkt_2", url="https://x/frame", blob_property="thumb", blob_type="image")
    assert rec.of("GET") == []
    bodies = [c[2] for c in rec.of("POST", "/buckets/bkt_2/objects")]
    assert bodies[0]["blobs"] == [{"property": "thumb", "type": "image", "data": "https://x/frame.jpg"}]
    assert bodies[1]["blobs"] == [{"property": "thumb", "type": "image", "data": "https://x/frame"}]


def test_blob_property_without_a_known_type_reads_the_schema(monkeypatch):
    client, rec = make_client(monkeypatch, {("GET", "/buckets/bkt_2"): TWO_FILE_BUCKET})
    client.buckets.upload("bkt_2", url="https://x/asset", blob_property="thumb")
    assert len(rec.of("GET")) == 1
    (post,) = rec.of("POST", "/buckets/bkt_2/objects")
    assert post[2]["blobs"] == [{"property": "thumb", "type": "image", "data": "https://x/asset"}]


def test_unknown_blob_property_names_the_file_properties(monkeypatch):
    client, rec = make_client(monkeypatch, {("GET", "/buckets/bkt_2"): TWO_FILE_BUCKET})
    with pytest.raises(ValueError, match="thumb, video"):
        client.buckets.upload("bkt_2", url="https://x/asset", blob_property="poster")


def test_explicit_blobs_are_sent_unchanged(monkeypatch):
    client, rec = make_client(monkeypatch, {})
    blobs = [{"property": "video", "type": "video", "data": "s3://b/clip.mp4"}]
    client.buckets.upload("bkt_1", blobs=blobs)
    assert rec.of("GET") == []
    (post,) = rec.of("POST", "/buckets/bkt_1/objects")
    assert post[2] == {"blobs": blobs}


def test_upload_reads_the_bucket_in_the_namespace_it_posts_to(monkeypatch):
    client, rec = make_client(monkeypatch, {("GET", "/buckets/bkt_1"): VIDEO_BUCKET})
    client.buckets.upload("bkt_1", url="s3://b/clip.mp4", namespace_id="ns_other")
    (get,) = rec.of("GET")
    (post,) = rec.of("POST")
    assert get[3] == "ns_other" and post[3] == "ns_other"


def test_index_builds_blobs_from_the_bucket_schema(monkeypatch):
    client, rec = make_client(monkeypatch, {
        ("POST", "/buckets/list"): {"results": [VIDEO_BUCKET]},
        ("GET", "/buckets/bkt_1"): VIDEO_BUCKET,
    })
    client.index("s3://b/clip.mp4", collection="col_1")
    (post,) = rec.of("POST", "/buckets/bkt_1/objects")
    assert post[2] == {"blobs": [{"property": "video", "type": "video", "data": "s3://b/clip.mp4"}]}
    assert rec.of("POST", "/collections/col_1/trigger")


def _search_client(monkeypatch):
    return make_client(monkeypatch, {
        ("POST", "/retrievers"): {"retriever_id": "ret_1"},
        ("POST", "/retrievers/ret_1/execute"): {"documents": []},
    })


def test_search_maps_vector_name_and_vector(monkeypatch):
    client, rec = _search_client(monkeypatch)
    query = {"vector_name": "embedding", "vector": [0.1, 0.2], "top_k": 5}
    client.search(namespace_id="ns_x", queries=[query])
    (create,) = rec.of("POST", "/retrievers")
    searches = create[2]["stages"][0]["config"]["parameters"]["searches"]
    assert searches == [{"feature_uri": "embedding", "query": {"input_mode": "vector", "value": [0.1, 0.2]}, "top_k": 5}]
    assert query == {"vector_name": "embedding", "vector": [0.1, 0.2], "top_k": 5}
    assert create[3] == "ns_x"


def test_search_leaves_feature_uri_entries_alone(monkeypatch):
    client, rec = _search_client(monkeypatch)
    query = {"feature_uri": "embedding", "query": {"input_mode": "vector", "value": [0.3]}, "top_k": 3}
    client.search(namespace_id="ns_x", queries=[query])
    (create,) = rec.of("POST", "/retrievers")
    assert create[2]["stages"][0]["config"]["parameters"]["searches"] == [query]


def test_search_forwards_filters_to_execute(monkeypatch):
    client, rec = _search_client(monkeypatch)
    filters = {"AND": [{"field": "modality", "operator": "eq", "value": "image"}]}
    client.search(namespace_id="ns_x", queries=[{"feature_uri": "clip", "query": {"input_mode": "vector", "value": [0.1]}}], filters=filters)
    (execute,) = rec.of("POST", "/retrievers/ret_1/execute")
    assert execute[2] == {"inputs": {}, "filters": filters}
