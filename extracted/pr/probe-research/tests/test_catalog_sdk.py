"""The data catalog from a training job (plan data-catalog C5, C8-C11; `probe.sdk.catalog`).

Every verb runs against `tests.catalog_fake.CatalogFake`, which answers the
catalog routes as the plan's Interfaces spell them and hands everything else
to the ordinary FakeApp, so these drive the real Client and Run.

Test map: C5 (manifest deterministic, symlink escape refused, partial,
pointer identity, old server -> warn and no raise, >10 s -> pending ref filled
later, register=False ref), C9a/C9c/C9d through log_dataset, C10 (mixture and
composition shares), C11a and the SDK half of C11d (preview samples), C8
client paths (hosting door, have-list, multipart, 402).
"""

from __future__ import annotations

import gzip
import hashlib
import json
import os
import sys
import warnings

import pytest

import probe
from probe.sdk import catalog
from tests.catalog_fake import CatalogFake, manifest_identity
from tests.conftest import make_client, open_run


@pytest.fixture(autouse=True)
def _fresh_warnings():
    catalog._warned.clear()
    yield
    catalog._warned.clear()


@pytest.fixture
def fake() -> CatalogFake:
    return CatalogFake()


@pytest.fixture
def run(fake):
    client = make_client(fake)
    handle = open_run(client, experiment="e", name="r", heartbeat=False, capture_outputs=False)
    yield handle
    client.close()


def _folder(root, files: dict[str, bytes]):
    for rel, data in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return root


def _caught(fn):
    with warnings.catch_warnings(record=True) as seen:
        warnings.simplefilter("always")
        result = fn()
    return result, [str(w.message) for w in seen]


# -- sources and uses (C1, C2) ------------------------------------------------------


def test_source_registers_once_and_returns_its_ref(run, fake):
    src = probe.source("https://huggingface.co/datasets/allenai/c4", revision="1588ec4", license="ODC-BY",
                       client=run._client)
    again = probe.source("https://huggingface.co/datasets/allenai/c4", revision="1588ec4", client=run._client)
    assert src.ref and src.ref.startswith("source:") and src.created is True
    assert again.ref == src.ref and again.created is False
    assert src.canonical_key == "hf:datasets/allenai/c4" and str(src) == src.ref
    body = json.loads(fake.calls("POST", "/v1/sources")[0].content)
    assert body == {"uri": "https://huggingface.co/datasets/allenai/c4",
                    "revision": "1588ec4", "license": "ODC-BY"}


def test_a_refused_source_warns_and_never_raises(run, fake):
    # The client lets an ssh remote's user name through; this fake server
    # refuses any `@` in the authority, so the SERVER's 422 is what warns.
    uri = "ssh://git@github.com/org/repo.git"
    src, said = _caught(lambda: probe.source(uri, client=run._client))
    assert src.ref is None and src.uri == uri
    assert any("refused (422)" in s for s in said)


@pytest.mark.parametrize(
    "uri",
    [
        "https://user:pw@example.com/data",
        "https://hf_abc123@huggingface.co/datasets/org/x",
        "s3://bucket/key?X-Amz-Signature=abc&X-Amz-Credential=k",
        "https://storage.googleapis.com/b/o?x-goog-signature=abc",
        "https://acct.blob.core.windows.net/c/b?sv=2024&sig=abc",
        "https://example.com/data.jsonl?token=abc",
        "postgres://reader:secret@db.example.com/warehouse",
    ],
)
def test_a_uri_carrying_a_credential_never_leaves_the_machine(run, fake, uri):
    """The approval bot's block on #2791: the client refuses a credential in a
    source uri before sending it (the server refuses it too, `app/catalog/uris.py`)."""
    src, said = _caught(lambda: probe.source(uri, client=run._client))
    assert src.ref is None
    assert fake.calls("POST", "/v1/sources") == []
    assert any("carries a credential" in s for s in said)


@pytest.mark.parametrize(
    "uri",
    [
        "https://huggingface.co/datasets/allenai/c4",
        "ssh://git@github.com/org/repo.git",
        "abfss://container@account.dfs.core.windows.net/path",
        "postgres://reader@db.example.com/warehouse",
        "https://example.com/data?key=public-dataset-name",
    ],
)
def test_a_uri_without_a_secret_is_sent(run, fake, uri):
    assert catalog.credential_in_uri(uri) is None
    probe.source(uri, client=run._client)
    assert len(fake.calls("POST", "/v1/sources")) == 1  # sent (the fake may still refuse it)


def test_a_reference_registration_with_a_presigned_uri_is_refused_before_sending():
    with pytest.raises(catalog.CatalogRefused, match="carries a credential"):
        catalog.registration_body(
            "c4-clean",
            reference={"uri": "s3://bucket/c4?X-Amz-Signature=abc", "content_hash": None,
                       "size_bytes": 1, "identity": "pointer"},
        )


def test_the_client_credential_rule_is_the_servers():
    """`CREDENTIAL_PARAMS` and the name-only userinfo schemes are copies of
    `app/catalog/uris.py`; read the server source so the two cannot drift."""
    import ast
    import pathlib

    server = pathlib.Path(__file__).resolve().parents[2] / "app" / "catalog" / "uris.py"
    if not server.exists():
        pytest.skip("server source not in this checkout")
    tree = ast.parse(server.read_text())
    sets: dict[str, set[str]] = {}
    for node in ast.walk(tree):
        target = None
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            target, value = node.target.id, node.value
        elif isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            target, value = node.targets[0].id, node.value
        if target in {"CREDENTIAL_PARAMS", "_NAME_ONLY_USERINFO_SCHEMES"}:
            sets[target] = {c.value for c in ast.walk(value) if isinstance(c, ast.Constant) and isinstance(c.value, str)}
    assert sets["CREDENTIAL_PARAMS"] == set(catalog.CREDENTIAL_PARAMS)
    assert sets["_NAME_ONLY_USERINFO_SCHEMES"] == set(catalog.NAME_ONLY_USERINFO_SCHEMES)


def test_use_dataset_records_the_role_and_share(run, fake):
    src = probe.source("https://huggingface.co/datasets/allenai/c4", client=run._client)
    assert run.use_dataset(src, role="train") is None
    run.use_checkpoint("checkpoint:sft-7b@best")
    bodies = [json.loads(r.content) for r in fake.calls("POST", f"/v1/runs/{run.id}/uses")]
    assert bodies == [
        {"target": src.ref, "roles": ["train"], "provenance": "observed_call"},
        {"target": "checkpoint:sft-7b@best", "roles": ["init"], "provenance": "observed_call"},
    ]
    assert [u["roles"] for u in fake.uses] == [["train"], ["init"]]


def test_a_bad_role_or_unknown_ref_warns_once_and_never_raises(run, fake):
    _, said = _caught(lambda: run.use_dataset("dataset:nope@1", role="base_model"))
    assert any("not a role" in s for s in said) and not fake.calls("POST", f"/v1/runs/{run.id}/uses")
    _, said = _caught(lambda: [run.use_dataset("dataset:nope@1") for _ in range(3)])
    assert len([s for s in said if "unknown ref" in s]) == 1


def test_use_mixture_is_one_batch_that_must_sum_to_one(run, fake):
    a = run.log_dataset(_folder_path(run, "a"), name="a", preview=False)
    b = run.log_dataset(_folder_path(run, "b"), name="b", preview=False)
    run.use_mixture({a: 0.7, b.ref: 0.3})
    sent = [json.loads(r.content) for r in fake.calls("POST", f"/v1/runs/{run.id}/uses")]
    assert sent == [{"mixture": [{"target": "dataset:a@1", "share": 0.7}, {"target": "dataset:b@1", "share": 0.3}],
                     "role": "train", "provenance": "observed_call"}]
    _, said = _caught(lambda: run.use_mixture({a: 0.7, b: 0.6}))
    assert any("sum to 1" in s for s in said)
    assert len(fake.calls("POST", f"/v1/runs/{run.id}/uses")) == 1


def _folder_path(run, name):
    import tempfile

    root = tempfile.mkdtemp(prefix=f"probe-ds-{name}-")
    with open(os.path.join(root, "part-0.jsonl"), "w") as f:
        f.write(f'{{"x": "{name}"}}\n' * 3)
    return root


# -- log_dataset: identity (C5, R8) -------------------------------------------------


def test_a_folder_is_identified_by_its_manifest_deterministically(run, fake, tmp_path):
    data = _folder(tmp_path / "c4-clean", {"b/2.jsonl": b'{"a":1}\n{"a":2}\n', "a.txt": b"x\ny\nz", "c.bin": b"\0" * 10})
    first = catalog.prepare(data)
    second = catalog.prepare(data)
    assert first.content_hash == second.content_hash == manifest_identity(first.manifest.body()["files"])
    assert [f["relpath"] for f in first.manifest.body()["files"]] == ["a.txt", "b/2.jsonl", "c.bin"]
    assert first.identity == "bytes" and first.size_bytes == 16 + 5 + 10

    ds = run.log_dataset(data, name="c4-clean", note="dropped near-duplicates", stats={"rows": 5}, preview=False)
    assert ds.ref == "dataset:c4-clean@1" and not ds.pending and ds.identity == "bytes"
    put = fake.calls("PUT", "/v1/catalog/manifests/")[0]
    assert put.url.path.endswith(first.content_hash) and put.headers["content-encoding"] == "gzip"
    manifest = json.loads(gzip.decompress(put.content))
    assert manifest["format"] == catalog.MANIFEST_FORMAT and manifest["rows_complete"] is False
    rows = {f["relpath"]: f.get("rows") for f in manifest["files"]}
    assert rows == {"a.txt": 3, "b/2.jsonl": 2, "c.bin": None}
    body = fake.registrations[0]
    assert set(body) == {"name", "run_file", "change"}
    assert body["change"] == {"note": "dropped near-duplicates", "stats": {"rows": 5}}
    spec = body["run_file"]
    assert set(spec) == {"run_id", "name", "uri", "content_hash", "size_bytes", "identity", "meta"}
    assert spec["run_id"] == run.id and spec["uri"].startswith("file://") and spec["identity"] == "bytes"
    assert spec["meta"]["files"] == 3 and spec["meta"]["host"] and spec["meta"]["local_path"] == str(data)

    again = run.log_dataset(data, name="c4-clean", preview=False)
    assert again.ref == "dataset:c4-clean@1" and again.created_version is False and again.recorded_step is True


def test_a_link_inside_the_folder_is_never_followed(run, tmp_path):
    outside = tmp_path / "secret.txt"
    outside.write_text("not part of it\n")
    data = _folder(tmp_path / "ds", {"a.jsonl": b"{}\n"})
    os.symlink(outside, data / "escape.txt")
    os.symlink(tmp_path, data / "up")
    prepared = catalog.prepare(data)
    assert [f.relpath for f in prepared.manifest.files] == ["a.jsonl"]
    assert prepared.identity == "partial" and prepared.manifest.skipped == 2


def test_past_the_budget_a_version_is_partial(tmp_path):
    data = _folder(tmp_path / "ds", {"a.jsonl": b"{}\n" * 100})
    prepared = catalog.prepare(data, budget=[0])
    assert prepared.identity == "partial"
    assert prepared.manifest.files[0].content_hash is None
    full = catalog.prepare(data, budget=[0], hash_mode="full")
    assert full.identity == "bytes" and full.manifest.files[0].content_hash == hashlib.sha256(b"{}\n" * 100).hexdigest()


def test_a_single_file_is_its_own_sha256(run, fake, tmp_path):
    path = tmp_path / "train.jsonl"
    path.write_bytes(b'{"a":1}\n{"a":2}')
    ds = run.log_dataset(path, name="tiny", preview=False)
    assert ds.content_hash == hashlib.sha256(path.read_bytes()).hexdigest()
    assert not fake.manifest_puts  # one file needs no manifest
    assert fake.registrations[0]["run_file"]["meta"]["rows"] == 2


def test_a_remote_uri_is_a_pointer_never_read(run, fake):
    ds = run.log_dataset("s3://lab/pdb/2026-09/", name="pdb-motif", preview=False)
    spec = fake.registrations[0]["run_file"]
    assert spec["identity"] == "pointer" and spec["uri"] == "s3://lab/pdb/2026-09/"
    assert spec["content_hash"] == hashlib.sha256(b"s3://lab/pdb/2026-09/\n").hexdigest()
    assert ds.identity == "pointer" and ds.ref == "dataset:pdb-motif@1"


def test_an_old_server_gets_one_warning_and_no_hashing(run, fake, tmp_path, monkeypatch):
    fake.old_server = True
    hashed = []
    monkeypatch.setattr(catalog, "prepare", lambda *a, **k: hashed.append(a) or None)
    data = _folder(tmp_path / "ds", {"a.jsonl": b"{}\n"})
    (first, second), said = _caught(lambda: (run.log_dataset(data, name="ds"), run.log_dataset(data, name="ds")))
    assert first.ref is None and second.ref is None and not hashed
    assert len([s for s in said if "predates the data catalog" in s]) == 1
    _, said = _caught(lambda: run.use_dataset("dataset:ds@1"))
    assert any("predates the data catalog" in s for s in said)


def test_a_slow_registration_returns_pending_and_fills_in(run, fake, tmp_path):
    fake.register_delay = 1.0
    data = _folder(tmp_path / "ds", {"a.jsonl": b"{}\n"})
    ds, said = _caught(lambda: catalog.log_dataset(run, data, "slow", preview=False, wait=0.05))
    assert ds.pending is True and ds.ref is None
    assert any("has not answered" in s for s in said)
    assert ds.wait(10)
    assert ds.ref == "dataset:slow@1" and ds.pending is False


def test_register_false_returns_the_run_file_ref(run, fake, tmp_path):
    data = _folder(tmp_path / "ds", {"a.jsonl": b"{}\n", "b.jsonl": b"{}\n"})
    ds = run.log_dataset(data, name="unregistered", register=False, preview=False)
    assert ds.ref and ds.ref.startswith("artifact:") and ds.artifact_id == ds.ref.split(":", 1)[1]
    assert not fake.registrations and len(fake.manifest_puts) == 1
    row = next(a for a in fake.base.artifacts[run.id] if a["id"] == ds.artifact_id)
    assert row["kind"] == "dataset" and row["is_reference"] is True and row["content_hash"] == ds.content_hash


def test_a_bad_name_is_refused_before_anything_is_hashed(run, fake, tmp_path):
    ds, said = _caught(lambda: run.log_dataset(tmp_path, name="C4@3"))
    assert ds.ref is None and not fake.calls("PUT", "/v1/catalog/manifests/") and not fake.registrations
    assert any("not a dataset name" in s for s in said)


# -- .probe.config (C9a, C9c, C9d) --------------------------------------------------


def test_a_hash_level_folder_is_registered_by_identity_only(run, fake, tmp_path):
    root = tmp_path / "work"
    data = _folder(root / "data", {"big.jsonl": b'{"text": "a long enough record to be hashed"}\n' * 4,
                                   "tiny.txt": b"label\n"})
    (root / ".probe.config").write_text("data/ @probe hash\n")
    ds = run.log_dataset(data, name="excluded-data")
    assert ds.ref == "dataset:excluded-data@1"
    files = {f["relpath"]: f for f in fake.manifest_puts[0]["files"]}
    assert files["big.jsonl"]["content_hash"] and files["big.jsonl"]["rows"] == 4
    assert "content_hash" not in files["tiny.txt"] and files["tiny.txt"]["size_bytes"] == 6  # C9d: < 64 B
    assert fake.registrations[0]["run_file"]["meta"]["identity_only"] is True
    assert not [a for a in fake.base.artifacts[run.id] if a["name"].startswith(catalog.PREVIEW_PREFIX)]


def test_a_hash_level_path_is_never_uploaded(run, fake, tmp_path):
    root = tmp_path / "work"
    data = _folder(root / "data", {"a.jsonl": b"{}\n" * 40})
    (root / ".probe.config").write_text("data/ @probe hash\n")
    ds, said = _caught(lambda: run.log_dataset(data, name="nope", upload=True))
    assert ds.ref is None and not fake.upload_asks and not fake.registrations
    assert any("never uploads it" in s for s in said)


def test_a_folder_holding_a_hash_level_file_is_never_uploaded(run, fake, tmp_path):
    data = _folder(tmp_path / "ds", {"public.jsonl": b"{}\n" * 40, "private/labels.jsonl": b"{}\n" * 40})
    (data / ".probe.config").write_text("private/ @probe hash\n")
    ds, said = _caught(lambda: run.log_dataset(data, name="mixed", upload=True))
    assert ds.ref is None and not fake.upload_asks and not fake.hosted_bytes
    assert any("never uploads them" in s for s in said)


def test_an_off_path_records_nothing_at_all(run, fake, tmp_path):
    root = tmp_path / "work"
    data = _folder(root / "data", {"a.jsonl": b"{}\n"})
    (root / ".probe.config").write_text("data/\n")
    ds, said = _caught(lambda: run.log_dataset(data, name="hidden"))
    assert ds.ref is None and not fake.manifest_puts and not fake.registrations
    assert any("excluded by" in s for s in said)


# -- composition (C10) ---------------------------------------------------------------


def test_composition_by_rows_sends_computed_shares(run, fake, tmp_path):
    a = run.log_dataset(_folder_path(run, "a"), name="real", preview=False)
    b = run.log_dataset(_folder_path(run, "b"), name="synth", preview=False)
    mix = _folder(tmp_path / "mix", {"train.jsonl": b"{}\n" * 4})
    run.log_dataset(mix, name="train-a", composition={a.ref: 24_000, b.ref: 8_000}, preview=False)
    assert fake.registrations[-1]["composition"] == [
        {"target": "dataset:real@1", "rows": 24_000, "share": 0.75},
        {"target": "dataset:synth@1", "rows": 8_000, "share": 0.25},
    ]
    run.log_dataset(mix, name="train-b", composition={a: 0.5, b: 0.5}, preview=False)
    assert fake.registrations[-1]["composition"] == [
        {"target": "dataset:real@1", "share": 0.5}, {"target": "dataset:synth@1", "share": 0.5},
    ]
    before = len(fake.registrations)
    ds, said = _caught(lambda: run.log_dataset(mix, name="train-c", composition={a: 0.9, b: 0.4}))
    assert ds.ref is None and len(fake.registrations) == before and any("sum to 1" in s for s in said)


# -- preview samples (C11a, C11d SDK half) -----------------------------------------


def test_a_reference_dataset_gets_a_preview_sample(run, fake, tmp_path, capsys):
    lines = b"".join(json.dumps({"i": i}).encode() + b"\n" for i in range(500))
    data = _folder(tmp_path / "ds", {"shard-0.jsonl": lines, "z.bin": b"\0" * 8})
    ds = run.log_dataset(data, name="with-preview")
    previews = [a for a in fake.base.artifacts[run.id] if a["name"].startswith(catalog.PREVIEW_PREFIX)]
    assert len(previews) == 1
    preview = previews[0]
    assert preview["name"] == f"{catalog.PREVIEW_PREFIX}{ds.artifact_id}.jsonl"
    assert preview["meta"]["preview_of"] == ds.artifact_id
    stored = fake.base.blobs.get(preview["id"], b"")
    assert stored.count(b"\n") == catalog.PREVIEW_MAX_RECORDS and stored.startswith(b'{"i": 0}')
    err = capsys.readouterr().err
    assert err.count("uploaded a 100-row preview of") == 1 and "preview=False" in err


def test_preview_false_uploads_no_sample(run, fake, tmp_path):
    data = _folder(tmp_path / "ds", {"a.jsonl": b"{}\n" * 5})
    run.log_dataset(data, name="no-preview", preview=False)
    assert not [a for a in fake.base.artifacts[run.id] if a["name"].startswith(catalog.PREVIEW_PREFIX)]


def test_a_csv_sample_keeps_its_header_and_stays_under_the_byte_cap(tmp_path):
    path = tmp_path / "t.csv"
    path.write_bytes(b"a,b\n" + b"1,2\n" * 1000)
    data, records, ext = catalog.preview_sample(str(path))
    assert ext == ".csv" and records == 100 and data.startswith(b"a,b\n") and data.count(b"\n") == 101
    wide = tmp_path / "wide.jsonl"
    wide.write_bytes((b'{"t": "' + b"x" * 10_000 + b'"}\n') * 100)
    data, records, _ = catalog.preview_sample(str(wide))
    assert len(data) <= catalog.PREVIEW_MAX_BYTES and records == len(data.splitlines())
    assert catalog.preview_sample(str(tmp_path / "missing.jsonl")) is None


def test_a_parquet_sample_needs_pyarrow_already_imported(tmp_path, monkeypatch):
    pa = pytest.importorskip("pyarrow")
    import pyarrow.parquet as pq

    path = tmp_path / "t.parquet"
    pq.write_table(pa.table({"x": list(range(300))}), path)
    data, records, ext = catalog.preview_sample(str(path))
    assert ext == ".jsonl" and records == 100 and data.splitlines()[0] == b'{"x": 0}'
    monkeypatch.delitem(sys.modules, "pyarrow")
    assert catalog.preview_sample(str(path)) is None


# -- hosting (C8) --------------------------------------------------------------------


def test_hosting_uploads_only_what_probe_lacks(run, fake, tmp_path):
    data = _folder(tmp_path / "ds", {"a.jsonl": b'{"a":1}\n', "b.jsonl": b'{"b":2}\n'})
    ds = run.log_dataset(data, name="hosted", upload=True)
    assert ds.ref == "dataset:hosted@1"
    assert fake.upload_asks == [{"name": "hosted", "manifest_hash": ds.content_hash}]
    assert len(fake.hosted_bytes) == 2 and len(fake.confirms) == 2
    assert fake.registrations[-1] == {"name": "hosted", "hosted": {"manifest_hash": ds.content_hash, "run_id": run.id}}
    puts_before = len(fake.calls("PUT", "/hosted/"))
    (data / "b.jsonl").write_bytes(b'{"b":3}\n')
    v2 = run.log_dataset(data, name="hosted", upload=True)
    assert v2.ref == "dataset:hosted@2"
    assert len(fake.calls("PUT", "/hosted/")) == puts_before + 1  # a.jsonl is shared with v1
    assert not [a for a in fake.base.artifacts.get(run.id, []) if a["name"].startswith(catalog.PREVIEW_PREFIX)]


def test_a_big_blob_goes_through_the_multipart_doors(run, fake, tmp_path):
    fake.multipart_over = 10
    data = _folder(tmp_path / "ds", {"big.bin": bytes(range(25))})
    ds = run.log_dataset(data, name="parts", upload=True)
    assert ds.ref == "dataset:parts@1"
    upload = next(iter(fake.multipart.values()))
    assert sorted(upload["parts"]) == [1, 2, 3] and upload["state"] == "verified"


def test_a_large_blob_is_registered_only_once_probe_verified_it(run, fake, tmp_path, monkeypatch):
    """The server's verifier hashes a multipart upload AFTER `complete`; until
    it answers `verified` the blob is not hosted, so a registration then is 409
    `hosted_incomplete`. The client waits for it first."""
    monkeypatch.setattr(catalog, "HOSTED_VERIFY_POLL_SECONDS", 0.0)
    fake.multipart_over = 10
    fake.verify_polls = 3
    data = _folder(tmp_path / "ds", {"big.bin": bytes(range(25)), "small.txt": b"hi\n"})
    ds = run.log_dataset(data, name="verified", upload=True)
    assert ds.ref == "dataset:verified@1"
    upload = next(iter(fake.multipart.values()))
    assert upload["state"] == "verified" and upload["status_reads"] == 4
    assert len(fake.registrations) == 1


def test_the_door_is_asked_again_until_nothing_is_deferred(run, fake, tmp_path, capsys):
    """C8 door: at most N blobs per call, `deferred` for the rest; the client
    sends each round and asks again until `deferred` is 0, then registers once."""
    fake.door_max_uploads = 2
    data = _folder(tmp_path / "ds", {f"{i}.jsonl": f'{{"i":{i}}}\n'.encode() for i in range(5)})
    ds = run.log_dataset(data, name="rounds", upload=True)
    assert ds.ref == "dataset:rounds@1"
    assert len(fake.upload_asks) == 3 and len(fake.confirms) == 5 and len(fake.registrations) == 1
    err = capsys.readouterr().err
    assert "hosting round 1: 2 file(s) to send" in err and "3 more after this round" in err
    assert "hosting round 3: 1 file(s) to send" in err and "0 more after this round" in err


def test_a_round_waits_for_its_large_uploads_before_asking_again(run, fake, tmp_path, monkeypatch):
    """A blob still being verified comes back in the next door call and takes
    a multipart slot: the client waits for the round's verification first, so
    every call sends something new."""
    monkeypatch.setattr(catalog, "HOSTED_VERIFY_POLL_SECONDS", 0.0)
    fake.multipart_over = 10
    fake.door_max_multipart = 1
    data = _folder(tmp_path / "ds", {"a.bin": bytes(range(20)), "b.bin": bytes(range(1, 21))})
    ds = run.log_dataset(data, name="big-rounds", upload=True)
    assert ds.ref == "dataset:big-rounds@1"
    assert len(fake.upload_asks) == 2 and len(fake.multipart) == 2
    assert all(up["state"] == "verified" for up in fake.multipart.values())


def _generic_creates(fake) -> list:
    return [r for r in fake.requests if r.method == "POST" and r.url.path == "/v1/shared/files/multipart"]


def test_a_large_upload_probe_gave_up_on_is_opened_again_by_the_door(run, fake, tmp_path, monkeypatch):
    """Probe gave up on a large blob's upload (left idle past its sweep) and
    the multipart client started it again -- through the generic Shared create,
    which refuses the reserved `.probe/datasets/<hash>` name (422), so nothing
    was hosted. The door opens it again, and the new upload is the one waited
    for."""
    monkeypatch.setattr(catalog, "HOSTED_VERIFY_POLL_SECONDS", 0.0)
    fake.multipart_over = 10
    fake.give_up_once = "idle"
    data = _folder(tmp_path / "ds", {"big.bin": bytes(range(25))})
    ds, said = _caught(lambda: run.log_dataset(data, name="restarted", upload=True))
    assert ds.ref == "dataset:restarted@1", said
    assert not _generic_creates(fake)
    assert len(fake.upload_asks) == 2  # the round's call, then the restart's
    given_up, fresh = fake.multipart.values()
    assert given_up["state"] == "failed" and fresh["state"] == "verified"
    assert sorted(fresh["parts"]) == [1, 2, 3]


def test_a_restart_finds_the_blob_hosted_meanwhile_and_sends_nothing(run, fake, tmp_path, monkeypatch):
    monkeypatch.setattr(catalog, "HOSTED_VERIFY_POLL_SECONDS", 0.0)
    fake.multipart_over = 10
    fake.give_up_once = "superseded_idle"
    fake.hosted_meanwhile = True
    data = _folder(tmp_path / "ds", {"big.bin": bytes(range(25))})
    ds, said = _caught(lambda: run.log_dataset(data, name="had-it", upload=True))
    assert ds.ref == "dataset:had-it@1", said
    assert not _generic_creates(fake) and len(fake.multipart) == 1
    assert len(fake.registrations) == 1


def test_the_door_loop_is_bounded(run, fake, tmp_path, monkeypatch):
    """A door that keeps deferring is asked at most `door_call_limit` times,
    then nothing is registered and the warning says so."""
    data = _folder(tmp_path / "ds", {"a.jsonl": b"{}\n"})
    asked: list[str] = []

    def stuck(name: str, manifest_hash: str) -> dict:
        asked.append(manifest_hash)
        return {"have": [], "uploads": [], "bytes_new": 0, "deferred": 7}

    monkeypatch.setattr(run._client, "host_dataset_uploads", stuck)
    ds, said = _caught(lambda: run.log_dataset(data, name="stuck", upload=True))
    assert len(asked) == catalog.door_call_limit(1) == 1 + catalog.DOOR_SPARE_CALLS
    assert ds.ref is None and not fake.registrations
    assert any(f"after {len(asked)} calls" in line for line in said)


def test_the_door_call_limit_follows_the_servers_per_call_floor():
    assert catalog.door_call_limit(0) == catalog.door_call_limit(500) == 1 + catalog.DOOR_SPARE_CALLS
    assert catalog.door_call_limit(501) == 2 + catalog.DOOR_SPARE_CALLS
    assert catalog.door_call_limit(100_000) == 200 + catalog.DOOR_SPARE_CALLS


def test_a_confirm_refused_for_bytes_over_the_reservation_names_the_file(run, fake, tmp_path):
    """The server answers 409 when the stored object is LARGER than the size
    the door reserved (its cap check trusted that size): the warning names the
    file and the server's reason, and nothing is registered."""
    fake.reserve_less = True
    data = _folder(tmp_path / "ds", {"shard-0.jsonl": b'{"a":1}\n'})
    ds, said = _caught(lambda: run.log_dataset(data, name="too-big", upload=True))
    assert ds.ref is None and not fake.registrations and not fake.confirms
    line = next(s for s in said if "reserved" in s)
    assert "shard-0.jsonl" in line and "larger than the size the hosting door reserved" in line


def test_over_the_hosted_cap_says_so_and_registers_nothing(run, fake, tmp_path):
    fake.hosted_cap = 1
    data = _folder(tmp_path / "ds", {"a.jsonl": b"{}\n" * 10})
    ds, said = _caught(lambda: run.log_dataset(data, name="capped", upload=True))
    assert ds.ref is None and not fake.registrations and not fake.hosted_bytes
    line = next(s for s in said if "cap" in s)
    assert "hosted datasets and checkpoints" in line and "49 GB of 50 GB" in line and "reference" in line


# -- reads -------------------------------------------------------------------------


def test_reads_reach_their_routes(run, fake, tmp_path):
    data = _folder(tmp_path / "ds", {"a.jsonl": b"{}\n"})
    run.log_dataset(data, name="readme", preview=False)
    client = run._client
    assert client.dataset("dataset:readme")["versions"][0]["ref"] == "dataset:readme@1"
    assert client.list_datasets(limit=5)["items"][0]["name"] == "readme"
    assert client.dataset_files("dataset:readme@1")["items"][0]["relpath"] == "a.jsonl"
    client.provenance("dataset:readme@1", direction="downstream", depth=3)
    client.provenance_steps("dataset:readme@1")
    asked = fake.calls("GET", "/v1/provenance")
    assert dict(asked[0].url.params) == {"ref": "dataset:readme@1", "direction": "downstream", "depth": "3"}
    assert dict(asked[1].url.params) == {"ref": "dataset:readme@1", "format": "steps"}


# -- review of #2791 (FIX FIRST): regressions --------------------------------------


def test_a_disabled_run_answers_every_catalog_verb_without_raising():
    """F2: `PROBE_MODE=disabled` (and an off/read working directory) hands the
    script a DisabledRun; `ds.ref` / `ds.wait()` must not raise into the job."""
    from probe.sdk.disabled import DisabledRun

    run = DisabledRun()
    ds = run.log_dataset("data/", "c4-clean")
    assert isinstance(ds, catalog.DatasetRef) and ds.ref is None and ds.pending is False
    assert ds.wait(0) is True and str(ds) == ""
    assert run.use_dataset("dataset:x@1") is None
    assert run.use_mixture({"dataset:a@1": 1.0}) is None
    assert run.use_checkpoint("checkpoint:x@best") is None


def test_probe_source_under_disabled_mode_builds_no_client(monkeypatch):
    """F8: no Client, no network, an empty ref."""
    from probe.sdk import client as client_module

    monkeypatch.setenv("PROBE_MODE", "disabled")
    monkeypatch.setattr(catalog, "_ambient", None)
    built: list[object] = []

    def no_client(self, *_a, **_k):
        built.append(self)
        raise AssertionError("PROBE_MODE=disabled built a Client")

    monkeypatch.setattr(client_module.Client, "__init__", no_client)
    src, said = _caught(lambda: probe.source("https://huggingface.co/datasets/allenai/c4"))
    assert isinstance(src, catalog.SourceRef) and src.ref is None
    assert not built and not said


def test_a_local_source_uri_a_probe_config_excludes_is_never_sent(run, fake, tmp_path):
    """F8: a `file:` or local-path source is checked against `.probe.config`;
    `hash` (identity only) may be named, `off`/`read` may not."""
    (tmp_path / "secret").mkdir()
    (tmp_path / "hashed").mkdir()
    (tmp_path / ".probe.config").write_text("secret/\nhashed/ @probe hash\n")
    src, said = _caught(lambda: probe.source(f"file://{tmp_path / 'secret'}", client=run._client))
    assert src.ref is None and not fake.calls("POST", "/v1/sources")
    assert any("excluded by" in s for s in said)
    src = probe.source(str(tmp_path / "hashed"), client=run._client)
    assert src.ref is not None


def test_kind_is_left_to_the_server_when_not_given(run, fake):
    """F12: the server infers a Hub model repo as a `model`; a default
    `dataset` sent by the client overrode that."""
    src = probe.source("https://huggingface.co/meta-llama/Llama-3.1-8B", client=run._client)
    assert "kind" not in json.loads(fake.calls("POST", "/v1/sources")[0].content)
    assert src.kind == "model"


def test_an_unreachable_server_is_asked_once_and_every_ask_is_bounded(run, fake, monkeypatch):
    """F5: the catalog probe runs inside a deadline, and "unreachable" is
    remembered for a short while instead of costing every call its timeout."""
    fake.unreachable = True
    client = run._client
    assert catalog.catalog_available(client) is None
    asked = len(fake.calls("GET", "/v1/catalog/datasets")) + len(fake.calls("GET", "/v1/server/features"))
    assert catalog.catalog_available(client) is None
    again = len(fake.calls("GET", "/v1/catalog/datasets")) + len(fake.calls("GET", "/v1/server/features"))
    assert again == asked, "asked again inside the TTL"
    assert all(bounded for method, path, bounded in fake.deadlines if path.startswith("/v1/catalog/"))


def test_the_manifest_put_is_bounded(run, fake, tmp_path):
    """F5: the manifest PUT runs inside a deadline too."""
    data = _folder(tmp_path / "ds", {"a.jsonl": b"{}\n", "b.jsonl": b"{}\n"})
    run.log_dataset(data, name="bounded", preview=False)
    puts = [bounded for method, path, bounded in fake.deadlines if method == "PUT" and "/manifests/" in path]
    assert puts == [True]


def test_hashing_runs_off_the_calling_thread_and_is_bounded(tmp_path, monkeypatch):
    """F5: a stalled mount (a hash that never returns) costs the call its
    bound, never the training thread forever."""
    import threading
    import time

    stuck = threading.Event()
    monkeypatch.setattr(catalog, "HASH_DEADLINE_SECONDS", 0.2)
    monkeypatch.setattr(catalog, "HASH_GRACE_SECONDS", 0.2)
    monkeypatch.setattr(catalog, "_identify", lambda *a, **k: stuck.wait(30) and None)
    data = _folder(tmp_path / "ds", {"a.jsonl": b"{}\n"})
    started = time.monotonic()
    with pytest.raises(catalog.CatalogRefused, match="did not finish"):
        catalog.prepare(data)
    assert time.monotonic() - started < 5
    stuck.set()


def test_a_manifest_put_that_fails_for_now_is_queued_ahead_of_the_registration(run, fake, tmp_path):
    """F6: a folder dataset is never lost to one failed manifest PUT: the PUT
    and then the registration wait in the outbox, in that order."""
    fake.manifest_status = 503
    data = _folder(tmp_path / "ds", {"a.jsonl": b"{}\n", "b.jsonl": b"{}\n{}\n"})
    ds, said = _caught(lambda: run.log_dataset(data, name="queued", preview=False))
    assert ds.pending is True and ds.ref is None and not fake.registrations
    assert any("queued" in s for s in said)
    fake.manifest_status = None
    run._client.flush()
    assert fake.manifests and fake.registrations[-1]["name"] == "queued"
    assert fake.datasets["queued"]["versions"][0]["content_hash"] == ds.content_hash
    order = [r.url.path for r in fake.requests if r.method in ("PUT", "POST") and "/catalog/" in r.url.path]
    assert order[-2].startswith("/v1/catalog/manifests/") and order[-1] == "/v1/catalog/datasets"


def test_log_dataset_spends_the_runs_one_hashing_budget(run, fake, tmp_path):
    """F10: hashing a dataset counts against the run's 10 GB, as reads do."""
    from types import SimpleNamespace

    from probe.sdk import inputs

    state = SimpleNamespace(hashed_bytes=inputs.RUN_HASH_BUDGET_BYTES - 150)
    with inputs._lock:
        inputs._active[run.id] = state
    try:
        data = _folder(tmp_path / "ds", {"a.jsonl": b"x" * 99 + b"\n", "b.jsonl": b"y" * 99 + b"\n"})
        ds = run.log_dataset(data, name="budgeted", preview=False)
    finally:
        with inputs._lock:
            inputs._active.pop(run.id, None)
    assert ds.identity == "partial"
    assert state.hashed_bytes == inputs.RUN_HASH_BUDGET_BYTES - 150 + 100


def test_the_preview_after_a_registration_is_bounded_too(run, fake, tmp_path):
    """F11: the work after the registration (finding the run file, the
    preview upload) runs inside the registration's deadline."""
    data = _folder(tmp_path / "ds", {"a.jsonl": b'{"a": 1}\n' * 5})
    ds = run.log_dataset(data, name="after")
    assert ds.wait(10) and ds.artifact_id
    looked = [bounded for method, path, bounded in fake.deadlines
              if method == "GET" and path == f"/v1/runs/{run.id}/artifacts"]
    assert looked and all(looked)


def test_use_dataset_waits_for_a_pending_ref_then_says_it_is_still_pending(run, fake, tmp_path, monkeypatch):
    """F13: a ref still registering is waited for (briefly), and a ref that
    never settles is named as pending, not as unregistered."""
    import threading

    _ = run.log_dataset(_folder(tmp_path / "d", {"a.jsonl": b"{}\n"}), name="later", preview=False)
    pending = catalog.DatasetRef(name="later", pending=True)

    def settle():
        pending._fill({"version": {"ref": "dataset:later@1", "id": "v"}})
        pending._done.set()

    threading.Timer(0.2, settle).start()
    run.use_dataset(pending)
    assert json.loads(fake.calls("POST", f"/v1/runs/{run.id}/uses")[-1].content)["target"] == "dataset:later@1"
    monkeypatch.setattr(catalog, "REQUEST_SECONDS", 0.1)
    stuck = catalog.DatasetRef(name="stuck", pending=True)
    _, said = _caught(lambda: run.use_dataset(stuck))
    assert any("still pending" in s for s in said)
