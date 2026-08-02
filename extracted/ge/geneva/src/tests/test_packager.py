# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# tests for DockerUDFPackager marshal: docker image selection and
# workspace zip upload (configured upload location)

import json
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import pyarrow as pa
import pytest

import geneva.cloudpickle as cloudpickle
from geneva import udf
from geneva.packager import DockerUDFPackager, DockerUDFSpecV1
from geneva.transformer import UDF

_TABLE_LOCATION = "s3://bucket/tables/demo"
_UPLOAD_LOCATION = f"{_TABLE_LOCATION}/_geneva_uploads/"


@udf
def _plus_one(x: int) -> int:
    return x + 1


def _make_workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Create a small workspace and make it the cwd for the default zipper."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "module.py").write_text("VALUE = 1\n")
    monkeypatch.chdir(workspace)
    return workspace


def _make_table_ref() -> mock.MagicMock:
    """Build a TableReference test double with namespace credentials."""
    namespace_client = mock.MagicMock()
    namespace_client.describe_table.return_value = SimpleNamespace(
        location=f"{_TABLE_LOCATION}/"
    )
    table_ref = mock.MagicMock()
    table_ref.table_id = ["ns", "demo"]
    table_ref.storage_options = None
    table_ref.connect_namespace.return_value = namespace_client
    return table_ref


def _make_session(exists: bool = False) -> mock.MagicMock:
    session = mock.MagicMock()
    session.contains.return_value = exists
    return session


def _packager() -> DockerUDFPackager:
    return DockerUDFPackager(
        prebuilt_docker_img="test:latest",
        workspace_upload_location=_UPLOAD_LOCATION,
    )


def test_marshal_uploads_workspace_zip(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    workspace = _make_workspace(tmp_path, monkeypatch)
    table_ref = _make_table_ref()
    session = _make_session()

    with mock.patch("geneva.db.open_lance_dataset") as open_ds:
        open_ds.return_value.new_file_session.return_value = session
        spec = _packager().marshal(_plus_one, table_ref=table_ref)

    payload = DockerUDFSpecV1.from_bytes(spec.udf_payload)
    checksum = payload.workspace_checksum
    assert checksum

    expected_uri = f"{_UPLOAD_LOCATION}{checksum}.zip"
    assert payload.workspace_zips == [expected_uri]

    serialized_payload = json.loads(spec.udf_payload)
    assert serialized_payload["workspace_zips"] == [expected_uri]
    assert "workspace_zip" not in serialized_payload

    session.upload_file.assert_called_once()
    local_path, remote_path = session.upload_file.call_args[0]
    assert remote_path == f"_geneva_uploads/{checksum}.zip"
    # the zip is produced in the workspace-local .geneva output dir
    assert Path(local_path) == workspace / ".geneva" / f"{checksum}.zip"
    assert Path(local_path).is_file()


def test_marshal_skips_upload_when_zip_exists(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _make_workspace(tmp_path, monkeypatch)
    table_ref = _make_table_ref()

    first_session = _make_session()
    with mock.patch("geneva.db.open_lance_dataset") as open_ds:
        open_ds.return_value.new_file_session.return_value = first_session
        first_spec = _packager().marshal(_plus_one, table_ref=table_ref)
    first_session.upload_file.assert_called_once()
    first_payload = DockerUDFSpecV1.from_bytes(first_spec.udf_payload)

    second_session = _make_session(exists=True)
    with mock.patch("geneva.db.open_lance_dataset") as open_ds:
        open_ds.return_value.new_file_session.return_value = second_session
        second_spec = _packager().marshal(_plus_one, table_ref=table_ref)
    second_session.upload_file.assert_not_called()
    second_payload = DockerUDFSpecV1.from_bytes(second_spec.udf_payload)

    # the zip produced by the first marshal must not change the workspace
    # checksum, otherwise every marshal re-zips and re-uploads
    assert second_payload.workspace_checksum == first_payload.workspace_checksum
    assert second_payload.workspace_zips == first_payload.workspace_zips


def test_marshal_uploads_all_workspace_shards(tmp_path: Path) -> None:
    checksum = "c" * 64
    shards = []
    for idx in range(2):
        shard = tmp_path / f"{checksum}.part{idx:02d}.zip"
        shard.write_bytes(b"shard")
        shards.append(shard)

    zipper = mock.MagicMock()
    zipper.zip.return_value = (shards, checksum)
    packager = DockerUDFPackager(
        prebuilt_docker_img="test:latest",
        zip_workspace_packager=zipper,
    )
    table_ref = _make_table_ref()
    session = _make_session()

    with mock.patch("geneva.db.open_lance_dataset") as open_ds:
        open_ds.return_value.new_file_session.return_value = session
        spec = packager.marshal(_plus_one, table_ref=table_ref)

    payload = DockerUDFSpecV1.from_bytes(spec.udf_payload)
    expected_uris = [f"{_UPLOAD_LOCATION}{shard.name}" for shard in shards]
    assert payload.workspace_zips == expected_uris
    assert payload.workspace_checksum == checksum

    serialized_payload = json.loads(spec.udf_payload)
    assert serialized_payload["workspace_zips"] == expected_uris
    assert "workspace_zip" not in serialized_payload

    assert session.upload_file.call_count == 2
    uploaded = [call.args for call in session.upload_file.call_args_list]
    assert uploaded == [
        (str(shard), f"_geneva_uploads/{shard.name}") for shard in shards
    ]


def test_docker_udf_spec_reads_legacy_workspace_zip_payload() -> None:
    legacy_uri = "s3://bucket/tables/demo/_geneva_uploads/legacy.zip"
    payload = DockerUDFSpecV1(
        image="test",
        tag="latest",
        workspace_checksum="legacy-checksum",
        udf_pickle=cloudpickle.dumps(_plus_one),
        workspace_zips=[legacy_uri],
    ).to_bytes()
    serialized_payload = json.loads(payload)
    serialized_payload["workspace_zip"] = legacy_uri
    del serialized_payload["workspace_zips"]

    parsed = DockerUDFSpecV1.from_bytes(json.dumps(serialized_payload).encode())

    assert parsed.workspace_zips == [legacy_uri]
    reserialized_payload = json.loads(parsed.to_bytes())
    assert reserialized_payload["workspace_zips"] == [legacy_uri]
    assert "workspace_zip" not in reserialized_payload


def test_docker_udf_spec_ignores_empty_legacy_workspace_zip_payload() -> None:
    payload = DockerUDFSpecV1(
        image="test",
        tag="latest",
        workspace_checksum=None,
        udf_pickle=cloudpickle.dumps(_plus_one),
    ).to_bytes()
    serialized_payload = json.loads(payload)
    serialized_payload["workspace_zip"] = ""

    parsed = DockerUDFSpecV1.from_bytes(json.dumps(serialized_payload).encode())

    assert parsed.workspace_zips is None
    reserialized_payload = json.loads(parsed.to_bytes())
    assert "workspace_zips" not in reserialized_payload
    assert "workspace_zip" not in reserialized_payload


def test_marshal_requires_table_ref_for_workspace_upload(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _make_workspace(tmp_path, monkeypatch)
    with pytest.raises(ValueError, match="table_ref is required"):
        _packager().marshal(_plus_one)


def _make_udf() -> UDF:
    @udf(data_type=pa.int32())
    def add_one(a: int) -> int:
        return a + 1

    return add_one


@pytest.mark.parametrize(
    ("prebuilt_img", "expected_image", "expected_tag"),
    [
        ("myrepo/geneva-worker:v1.2.3", "myrepo/geneva-worker", "v1.2.3"),
        (
            "registry.example.com:5000/team/worker:v2",
            "registry.example.com:5000/team/worker",
            "v2",
        ),
        ("myrepo/geneva-worker", "myrepo/geneva-worker", None),
        (
            "registry.example.com:5000/team/worker",
            "registry.example.com:5000/team/worker",
            None,
        ),
    ],
)
def test_marshal_uses_prebuilt_docker_img(
    prebuilt_img: str, expected_image: str, expected_tag: str | None
) -> None:
    """marshal() splits the configured prebuilt image into image and tag."""
    packager = DockerUDFPackager(prebuilt_docker_img=prebuilt_img)

    spec = packager.marshal(_make_udf())

    backend_spec = DockerUDFSpecV1.from_bytes(spec.udf_payload)
    assert backend_spec.image == expected_image
    assert backend_spec.tag == expected_tag

    assert spec.runner_payload is not None
    runner = json.loads(spec.runner_payload.decode())
    assert runner["image"] == prebuilt_img


def test_marshal_placeholder_when_no_prebuilt_img(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Without a configured image, marshal() keeps the legacy placeholder."""
    monkeypatch.delenv("GENEVA_UDF__DOCKER__PREBUILT_DOCKER_IMG", raising=False)
    packager = DockerUDFPackager()

    spec = packager.marshal(_make_udf())

    backend_spec = DockerUDFSpecV1.from_bytes(spec.udf_payload)
    assert backend_spec.image == "test-image"
    assert backend_spec.tag == "latest"

    assert spec.runner_payload is not None
    runner = json.loads(spec.runner_payload.decode())
    assert runner["image"] == "test-image:latest"


def test_virtual_column_entry_uses_configured_image() -> None:
    """The namespace API entry advertises the configured image, not the
    placeholder."""
    from geneva.virtual_column import build_virtual_column_entry

    packager = DockerUDFPackager(prebuilt_docker_img="myrepo/geneva-worker:v1.2.3")

    entry = build_virtual_column_entry("b", _make_udf(), ["a"], packager)

    assert entry["image"] == "myrepo/geneva-worker:v1.2.3"
