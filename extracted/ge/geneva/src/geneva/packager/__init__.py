# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# module for packaging workspace and UDFs
# also data spec for persisting the artifacts

import abc
import base64
import hashlib
import json
import logging
from pathlib import Path

import attrs
from typing_extensions import Self

import geneva.cloudpickle as cloudpickle
from geneva import DEFAULT_UPLOAD_DIR
from geneva.config import ConfigBase
from geneva.packager.uploader import make_upload_path
from geneva.packager.zip import WorkspaceZipper
from geneva.transformer import UDF, UDTF, Chunker

_LOG = logging.getLogger(__name__)


class UDFBackend(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def packager(cls) -> "UDFPackager":
        """Return the packager for this backend."""

    def to_bytes(self) -> bytes:
        return json.dumps(attrs.asdict(self)).encode()

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        return cls(**json.loads(data.decode()))


@attrs.define
class UDFSpec:
    """Specification for a user-defined function.

    This is an holder of an arbitrary user-defined function,
    which can use an backend for marshalling.

    The most common is likely Docker + some kind of workspace
    persistence. However, we want to support more than just
    Docker, so we create this "out most" abstraction to allow
    for more flexibility.
    """

    # the name of the udf
    name: str = attrs.field()

    def __attrs_post_init__(self) -> None:
        if not self.name:
            raise ValueError("UDF name must not be empty.")
        if len(self.name) < 1:
            raise ValueError("UDF name must be at least 1 character long.")

        backend_names = [cls.__name__ for cls in UDFBackend.__subclasses__()]
        unique_backend_names = set(backend_names)
        if self.backend not in unique_backend_names:
            raise ValueError(f"Unknown backend: {self.backend}")

    # the packaging backend for the udf
    backend: str = attrs.field()

    udf_payload: bytes = attrs.field()

    # the payload for the runner -- This is a HACK for allowing phalanx knowing
    # how to dispatch the UDF job. Make sure changes here are compatible to
    # parsing in phalanx.
    runner_payload: bytes | None = attrs.field(default=None)

    @classmethod
    def udf_from_spec(cls, data) -> UDF:
        # TODO: load the spec and find the backend,
        # then call the packager to do the next level unmarshalling
        raise NotImplementedError("udf_from_spec not yet implemented")


@attrs.define
class DockerUDFSpecV1(UDFBackend):
    """Specification for a user-defined function that runs in a Docker container.
    -- Version 1

    In this packaging spec, the python interpreter is assumed to be correctly
    setup in the container, and the user-defined function is expected to load
    using cloudpickle. With the option of downloading additional workspace
    files from a remote location (S3, GCS, etc).
    """

    # the image to run the udf in
    image: str = attrs.field()

    # the tag of the image
    tag: str | None = attrs.field()

    # the checksum of the workspace zip
    workspace_checksum: str | None = attrs.field()

    # the udf pickle to run
    udf_pickle: bytes = attrs.field()

    # paths to the workspace zip files on (S3, GCS, etc), whether one or many;
    # omitted from the payload when unset
    workspace_zips: list[str] | None = attrs.field(default=None)

    # the checksum of the udf pickle
    udf_checksum: str = attrs.field(init=False)

    def __attrs_post_init__(self) -> None:
        # Validate tag
        if self.tag is not None:
            if len(self.tag) > 128:
                raise ValueError("Tag must be less than 128 characters.")
            if not all(
                c.isalpha() or c.isnumeric() or c in {"_", ".", "-"} for c in self.tag
            ):
                raise ValueError("Tag must be valid alphanumeric.")

        # Validate workspace checksum
        if self.workspace_zips and not self.workspace_checksum:
            raise ValueError(
                "Workspace checksum must not be empty when a workspace is provided."
            )

        # Validate UDF pickle
        if not self.udf_pickle:
            raise ValueError("UDF pickle must not be empty.")

        # Try to validate the UDF by unpickling, but don't fail if modules are missing
        # This supports distributed workflows where manifests are created in one
        # environment and used in another (e.g., uploaded by CI, used in notebooks)
        try:
            udf = cloudpickle.loads(self.udf_pickle)
            if not isinstance(udf, UDF):
                raise ValueError("UDF pickle must contain a UDF object.")
        except ModuleNotFoundError as e:
            _LOG.warning(
                f"Could not validate UDF pickle during spec loading: {e}. "
                "This is expected if the UDF was created in a different environment. "
                "Validation will happen when the UDF is executed on Ray workers."
            )

        self.udf_checksum = hashlib.sha256(self.udf_pickle).hexdigest()

    @classmethod
    def packager(cls) -> "UDFPackager":
        return DockerUDFPackager()

    def to_bytes(self) -> bytes:
        self_as_dict = attrs.asdict(self)
        self_as_dict["udf_pickle"] = base64.b64encode(
            self_as_dict["udf_pickle"]
        ).decode("utf-8")
        if self_as_dict.get("workspace_zips") is None:
            del self_as_dict["workspace_zips"]
        return json.dumps(self_as_dict).encode()

    @classmethod
    def from_bytes(cls, data: bytes) -> Self:
        self_as_dict = json.loads(data.decode())
        legacy_workspace_zip = self_as_dict.pop("workspace_zip", None)
        if legacy_workspace_zip and self_as_dict.get("workspace_zips") is None:
            self_as_dict["workspace_zips"] = [legacy_workspace_zip]

        self_as_dict["udf_pickle"] = base64.b64decode(
            self_as_dict["udf_pickle"].encode("utf-8")
        )

        checksum = self_as_dict.pop("udf_checksum")  # not part of the init
        val = cls(**self_as_dict)
        val.udf_checksum = checksum

        return val


def _split_image_reference(reference: str) -> tuple[str, str | None]:
    """Split a Docker image reference into image name and optional tag.

    The tag is the suffix after the last ":" unless that suffix contains
    "/", in which case the ":" belongs to a registry port and the
    reference has no tag.
    """
    image, sep, tag = reference.rpartition(":")
    if not sep or "/" in tag:
        return reference, None
    return image, tag or None


class UDFPackager(abc.ABC):
    """Packager for user-defined functions."""

    @abc.abstractmethod
    def marshal(self, udf: UDF, table_ref=None) -> UDFSpec:
        """Marshal a user-defined function."""

    @abc.abstractmethod
    def unmarshal(self, spec: UDFSpec) -> UDF | None:
        """Unmarshal a user-defined function.

        Returns None if the UDF cannot be unpickled due to missing modules.
        """


@attrs.define
class _DockerUDFPackagerConfig(ConfigBase):
    prebuilt_docker_img: str | None = attrs.field(default=None)

    # the backend the image will eventually run on. Gets passed ot the
    # docker workspace packager it can know which base image/dockerfile
    # template to use
    runtime_backend: str | None = attrs.field(default=None)

    workspace_upload_location: str | None = attrs.field(default=None)

    @classmethod
    def name(cls) -> str:
        return "docker"


@attrs.define
class _UDFPackagerConfig(ConfigBase):
    docker: _DockerUDFPackagerConfig = attrs.field(default=_DockerUDFPackagerConfig())

    @classmethod
    def name(cls) -> str:
        return "udf"


@attrs.define
class DockerUDFPackager(UDFPackager):
    # If the user wants to use an prebuilt docker image, they can provide the
    # image name:tag here. This will be used instead of building and pushing a
    # new image.
    prebuilt_docker_img: str | None = attrs.field(default=None)

    # the location to upload the zipped workspace to
    # this should be the path to some directory on object storage (S3, GCS, etc)
    workspace_upload_location: str | None = attrs.field(default=None)

    # provide a zipper implementation with the correct configuration for how to
    # zip the workspace.
    zip_workspace_packager: WorkspaceZipper | None = attrs.field(default=None)

    def __attrs_post_init__(self) -> None:
        # Set default prebuilt_docker_img
        if self.prebuilt_docker_img is None:
            config = _UDFPackagerConfig.get()
            if config.docker is not None:
                self.prebuilt_docker_img = config.docker.prebuilt_docker_img

        # Set default workspace_upload_location
        if self.workspace_upload_location is None:
            config = _UDFPackagerConfig.get()
            if config.docker is not None:
                self.workspace_upload_location = config.docker.workspace_upload_location

        # Set default zip_workspace_packager
        if self.zip_workspace_packager is None and self.workspace_upload_location:
            self.zip_workspace_packager = WorkspaceZipper(path=Path("."))

    def marshal(self, udf: UDF, table_ref=None) -> UDFSpec:
        if self.prebuilt_docker_img:
            image_name, tag = _split_image_reference(self.prebuilt_docker_img)
        else:
            # placeholder for deployments where the runtime image comes from
            # the manifest or cluster definition instead of the packager
            image_name, tag = "test-image", "latest"

        workspace_zips = None
        workspace_checksum = None
        if self.zip_workspace_packager:
            if table_ref is None:
                raise ValueError(
                    "table_ref is required for workspace uploads so Geneva can "
                    "use the table's LanceFileSession"
                )
            namespace_client = table_ref.connect_namespace()
            if namespace_client is None:
                raise ValueError(
                    "TableReference must include namespace credentials for "
                    "workspace uploads"
                )

            _LOG.info("Packaging zipped workspace")
            zip_paths, checksum = self.zip_workspace_packager.zip()
            _LOG.info("Uploading zipped workspace")

            from lance_namespace import DescribeTableRequest

            response = namespace_client.describe_table(
                DescribeTableRequest(id=table_ref.table_id)
            )
            if response.location is None:
                raise ValueError(
                    f"Table location is None for table {table_ref.table_id}"
                )
            location = response.location.rstrip("?").rstrip("/")
            upload_location = f"{location}/{DEFAULT_UPLOAD_DIR}/"
            _LOG.info(f"Using table-specific upload location: {upload_location}")

            from geneva.db import open_lance_dataset

            ds = open_lance_dataset(
                namespace_client=namespace_client,
                table_id=table_ref.table_id,
                storage_options=table_ref.storage_options,
            )
            session = ds.new_file_session()

            # upload each shard unless it is already present
            uploaded = []
            for zip_path in zip_paths:
                file_name = zip_path.name
                remote_path = make_upload_path(file_name)
                dest = f"{upload_location}{file_name}"

                if not session.contains(remote_path):
                    _LOG.info(
                        f"Workspace zip does not exist, uploading {zip_path} to {dest}"
                    )
                    session.upload_file(str(zip_path), remote_path)
                    _LOG.info(f"Uploaded workspace zip to {dest}")
                else:
                    _LOG.info(f"Workspace zip {file_name} exists, skipping upload")

                uploaded.append(dest)

            workspace_zips = uploaded or None
            workspace_checksum = checksum or None

        udf_pickle = cloudpickle.dumps(udf)

        return UDFSpec(
            name=udf.name,
            backend=DockerUDFSpecV1.__name__,
            udf_payload=DockerUDFSpecV1(
                image=image_name,
                tag=tag,
                workspace_checksum=workspace_checksum,
                udf_pickle=udf_pickle,
                workspace_zips=workspace_zips,
            ).to_bytes(),
            runner_payload=json.dumps(
                {
                    "image": image_name if tag is None else f"{image_name}:{tag}",
                }
            ).encode(),
        )

    def unmarshal(self, spec: UDFSpec) -> UDF | None:
        """Unmarshal a UDF from a spec.

        Returns None if the UDF cannot be unpickled due to missing modules.
        This supports distributed workflows where manifests are created in one
        environment and used in another.
        """
        docker_spec = self.backend(spec)
        try:
            udf = cloudpickle.loads(docker_spec.udf_pickle)
            if not isinstance(udf, UDF):
                raise ValueError("UDF pickle must contain a UDF object.")
            return udf
        except ModuleNotFoundError as e:
            _LOG.warning(
                f"Cannot unmarshal UDF for validation: {e}. "
                "This is expected if the UDF was created in a different environment. "
                "Skipping client-side validation. The UDF will be executed on Ray "
                "workers where modules are available via py_modules in the manifest."
            )
            return None

    def backend(self, spec: UDFSpec) -> DockerUDFSpecV1:
        if spec.backend != DockerUDFSpecV1.__name__:
            raise ValueError("Invalid backend for UDF spec.")

        return DockerUDFSpecV1.from_bytes(spec.udf_payload)


# ---------------------------------------------------------------------------
# UDTF Serialization
# ---------------------------------------------------------------------------


@attrs.define
class UDTFSpec:
    """Serialized UDTF specification.

    This is a simple wrapper that stores the cloudpickled UDTF along with
    metadata needed for reconstruction.

    Security note: the ``udtf_payload`` field contains cloudpickle data which
    can execute arbitrary code on deserialization.  This follows the same trust
    model as Ray and Geneva UDF serialization — UDTFs should only be loaded
    from trusted sources.
    """

    name: str = attrs.field()
    version: str = attrs.field()
    udtf_payload: bytes = attrs.field()  # Cloudpickle of UDTF
    output_schema_bytes: bytes = attrs.field()  # Serialized Arrow schema
    input_columns: list[str] | None = attrs.field(default=None)
    partition_by: str | None = attrs.field(default=None)
    # Snapshotted GenevaManifest JSON + its SHA-256 checksum (optional).
    manifest: str | None = attrs.field(default=None)
    manifest_checksum: str | None = attrs.field(default=None)

    def __attrs_post_init__(self) -> None:
        if not self.name:
            raise ValueError("UDTF name must not be empty.")
        if not self.udtf_payload:
            raise ValueError("UDTF payload must not be empty.")
        if not self.output_schema_bytes:
            raise ValueError("Output schema bytes must not be empty.")

    def to_json(self) -> str:
        """Serialize to JSON string for storage in table metadata."""
        return json.dumps(
            {
                "name": self.name,
                "version": self.version,
                "udtf_payload": base64.b64encode(self.udtf_payload).decode("utf-8"),
                "output_schema_bytes": base64.b64encode(
                    self.output_schema_bytes
                ).decode("utf-8"),
                "input_columns": self.input_columns,
                "partition_by": self.partition_by,
                "manifest": self.manifest,
                "manifest_checksum": self.manifest_checksum,
            }
        )

    @classmethod
    def from_json(cls, data: str) -> "UDTFSpec":
        """Deserialize from JSON string."""
        d = json.loads(data)
        return cls(
            name=d["name"],
            version=d["version"],
            udtf_payload=base64.b64decode(d["udtf_payload"]),
            output_schema_bytes=base64.b64decode(d["output_schema_bytes"]),
            input_columns=d.get("input_columns"),
            partition_by=d.get("partition_by"),
            manifest=d.get("manifest"),
            manifest_checksum=d.get("manifest_checksum"),
        )


def marshal_udtf(udtf: UDTF) -> UDTFSpec:
    """Serialize a UDTF for storage in table metadata.

    Args:
        udtf: The UDTF to serialize.

    Returns:
        UDTFSpec containing the serialized UDTF.
    """
    return UDTFSpec(
        name=udtf.name,
        version=udtf.version,
        udtf_payload=cloudpickle.dumps(udtf),
        output_schema_bytes=udtf.output_schema.serialize().to_pybytes(),
        input_columns=udtf.input_columns,
        partition_by=udtf.partition_by,
        manifest=udtf.manifest.to_json() if udtf.manifest is not None else None,
        manifest_checksum=(
            udtf.manifest.compute_checksum() if udtf.manifest is not None else None
        ),
    )


def unmarshal_udtf(spec: UDTFSpec) -> UDTF | None:
    """Deserialize a UDTF from storage.

    Args:
        spec: The UDTFSpec to deserialize.

    Returns:
        The UDTF object, or None if modules are missing.
    """
    try:
        udtf = cloudpickle.loads(spec.udtf_payload)
        if not isinstance(udtf, UDTF):
            raise ValueError("UDTF payload must contain a UDTF object.")
        return udtf
    except ModuleNotFoundError as e:
        _LOG.warning(
            f"Cannot unmarshal UDTF: {e}. "
            "This is expected if the UDTF was created in a different environment."
        )
        return None


# ---------------------------------------------------------------------------
# Scalar UDTF serialization
# ---------------------------------------------------------------------------


@attrs.define
class ChunkerSpec:
    """Serialized Scalar UDTF specification for 1:N row expansion."""

    name: str = attrs.field()
    version: str = attrs.field()
    chunker_payload: bytes = attrs.field()
    output_schema_bytes: bytes = attrs.field()
    input_columns: list[str] | None = attrs.field(default=None)
    batch: bool = attrs.field(default=False)
    # Snapshotted GenevaManifest JSON + its SHA-256 checksum (optional).
    manifest: str | None = attrs.field(default=None)
    manifest_checksum: str | None = attrs.field(default=None)

    def __attrs_post_init__(self) -> None:
        if not self.name:
            raise ValueError("Chunker name must not be empty.")
        if not self.chunker_payload:
            raise ValueError("Chunker payload must not be empty.")
        if not self.output_schema_bytes:
            raise ValueError("Output schema bytes must not be empty.")

    def to_json(self) -> str:
        """Serialize to JSON string for storage in table metadata."""
        return json.dumps(
            {
                "name": self.name,
                "version": self.version,
                "chunker_payload": base64.b64encode(self.chunker_payload).decode(
                    "utf-8"
                ),
                "output_schema_bytes": base64.b64encode(
                    self.output_schema_bytes
                ).decode("utf-8"),
                "input_columns": self.input_columns,
                "batch": self.batch,
                "manifest": self.manifest,
                "manifest_checksum": self.manifest_checksum,
            }
        )

    @classmethod
    def from_json(cls, data: str) -> "ChunkerSpec":
        """Deserialize from JSON string."""
        d = json.loads(data)
        return cls(
            name=d["name"],
            version=d["version"],
            chunker_payload=base64.b64decode(d["chunker_payload"]),
            output_schema_bytes=base64.b64decode(d["output_schema_bytes"]),
            input_columns=d.get("input_columns"),
            batch=d.get("batch", False),
            manifest=d.get("manifest"),
            manifest_checksum=d.get("manifest_checksum"),
        )


def marshal_chunker(chunker_obj: Chunker) -> ChunkerSpec:
    """Serialize a Chunker for storage in table metadata."""
    return ChunkerSpec(
        name=chunker_obj.name,
        version=chunker_obj.version,
        chunker_payload=cloudpickle.dumps(chunker_obj),
        output_schema_bytes=chunker_obj.output_schema.serialize().to_pybytes(),
        input_columns=chunker_obj.input_columns,
        batch=chunker_obj.batch,
        manifest=(
            chunker_obj.manifest.to_json() if chunker_obj.manifest is not None else None
        ),
        manifest_checksum=(
            chunker_obj.manifest.compute_checksum()
            if chunker_obj.manifest is not None
            else None
        ),
    )


def unmarshal_chunker(spec: ChunkerSpec) -> Chunker | None:
    """Deserialize a Chunker from storage."""
    try:
        obj = cloudpickle.loads(spec.chunker_payload)
        if not isinstance(obj, Chunker):
            raise ValueError("Payload must contain a Chunker object.")
        return obj
    except ModuleNotFoundError as e:
        _LOG.warning(
            f"Cannot unmarshal Chunker: {e}. "
            "This is expected if the Chunker was created in a different environment."
        )
        return None
