"""Golden-value lock on the cloud_sync hash keys after the stable_hash migration.

idempotency keys and variant-spec hashes are PERSISTED (cld_idempotency rows,
variant drift detection). If the underlying hash pipeline ever changes output,
every in-flight idempotency key silently stops matching (retries re-execute) and
every variant looks "drifted" (needless re-render). These pinned digests make
that change impossible to miss: touch stable_json / hash_request / _spec_hash in
a way that shifts output and this test SCREAMS. Do not "update the golden value"
to make it pass without understanding that you are invalidating live keys.
"""
from matrx_files.cloud_sync.idempotency import hash_request
from matrx_files.cloud_sync.variants_service import _spec_hash


def test_idempotency_request_hash_is_stable():
    assert (
        hash_request(endpoint="POST /assets", body={"a": 1, "b": [1, 2]})
        == "00f4ea1da536a8996ff1205b69500d64e51077b89c668e2993d79a9f0312a8cd"
    )
    # key-order independence is part of the contract — same digest, reordered dict
    assert hash_request(endpoint="POST /assets", body={"b": [1, 2], "a": 1}) == hash_request(
        endpoint="POST /assets", body={"a": 1, "b": [1, 2]}
    )
    assert (
        hash_request(endpoint="PATCH /files/1", body=None)
        == "efbcc943febf61666b9369794ebdb8612099e6a245df1374399cec9e42072948"
    )


def test_variant_spec_hash_is_stable():
    spec = {"width": 800, "height": 600, "format": "webp", "quality": 82, "fit": "cover"}
    assert _spec_hash(spec) == "ba33cad395b5e157"
    assert len(_spec_hash(spec)) == 16
