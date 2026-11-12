"""Delivery of Harbor tasks with a non-empty steps array."""
from __future__ import annotations

import copy

import gzip
import tarfile
import tempfile
from pathlib import Path

from ._harbor_filetree import FileTree
from .content import sha256_file, verify_file_digest
from .errors import ImageMissing, SchemaError, TransportError
from .models import DatasetInstance, PushResult
from .tasktoml import set_docker_image
from .validate import tomllib


def _pack(tree, target, *, include_image, compress_level):
    options = {"filename": "", "mode": "wb", "mtime": 0}
    if compress_level is not None:
        options["compresslevel"] = compress_level
    tree.assert_unchanged()
    with open(target, "wb") as raw, gzip.GzipFile(fileobj=raw, **options) as gz, \
            tarfile.open(fileobj=gz, mode="w", format=tarfile.PAX_FORMAT) as archive:
        for rel, entry in sorted(tree.entries.items()):
            if not include_image and rel == "environment/image.tar.gz":
                continue
            info = tarfile.TarInfo("./" + rel)
            info.mode = entry.mode
            if entry.kind == "directory":
                info.type = tarfile.DIRTYPE
                archive.addfile(info)
            elif entry.kind == "link":
                info.type = tarfile.SYMTYPE
                info.linkname = entry.link
                archive.addfile(info)
            else:
                info.size = entry.identity[3]
                with tree.open_file(rel) as stream:
                    archive.addfile(info, stream)
    tree.assert_unchanged()
    return sha256_file(target)


def push_multi_step(client, report, dataset, version, *, split, owner_reference,
                    push_image, overwrite, register, verify,
                    image_release_dst_acr, compress_level):
    from .clients.instances import _manifest, _tags

    layout = client._layout()
    instance_id = report.instance_id
    docker_ref = report.config.get("environment", {}).get("docker_image", "")
    has_image = "environment/image.tar.gz" in report.snapshot.entries
    if push_image and not has_image and not docker_ref:
        raise ImageMissing("multi-step delivery requires image.tar.gz or environment.docker_image")
    if has_image and push_image:
        docker_ref = layout.image_ref(client._p.effective_acr_host, client._p.acr_namespace,
                                      dataset, instance_id, version=version, split=split)
        # An existing mutable tag cannot establish that this local archive was delivered.
        if not overwrite and client._image.exists(docker_ref):
            raise SchemaError("existing image has no local-source proof; use overwrite=True")
    owner = ("" if owner_reference is None else owner_reference
             if isinstance(owner_reference, str) else owner_reference.to_json())
    # Normalize only the SDK-owned temporary parent before creating the snapshot.
    # Source paths and every later descriptor-bound inventory check stay unchanged.
    temporary_parent = Path(tempfile.gettempdir()).resolve(strict=True)
    with tempfile.TemporaryDirectory(prefix="irepo_harbor_", dir=temporary_parent) as temporary:
        root = Path(temporary)
        staged = report.snapshot.copy_to(root / instance_id)
        image_pushed = False
        image_digest = ""
        if has_image and push_image:
            image_tar = staged / "environment/image.tar.gz"
            image_digest = sha256_file(image_tar)
            config_path = staged / FileTree(staged).resolve("task.toml")
            original_mode = config_path.stat().st_mode & 0o777
            original = config_path.read_bytes().decode("utf-8")
            changed, _ = set_docker_image(original, docker_ref)
            expected = copy.deepcopy(report.config)
            expected.setdefault("environment", {})["docker_image"] = docker_ref
            try:
                actual = tomllib.loads(changed)
            except tomllib.TOMLDecodeError as exc:
                raise SchemaError("multi-step main image cannot be edited safely") from exc
            if actual != expected:
                raise SchemaError("multi-step image edit changed step configuration")
            try:
                config_path.chmod(original_mode | 0o200)
                config_path.write_bytes(changed.encode("utf-8"))
            finally:
                config_path.chmod(original_mode)
            confirmed = client._image.push(image_tar, docker_ref, overwrite=overwrite)
            if confirmed is not None:
                from ._routing import _plan_acr_route
                def canonical(reference):
                    host, separator, path = reference.partition("/")
                    return _plan_acr_route(host).private_endpoint + separator + path
                if not isinstance(confirmed, str) or canonical(confirmed) != canonical(docker_ref):
                    raise SchemaError("image delivery returned an unexpected reference")
            if not client._image.exists(docker_ref, retries=3):
                raise TransportError("multi-step image could not be read back after delivery")
            image_pushed = True
        tree = FileTree(staged)
        archive = root / "content.tgz"
        # With image delivery disabled, keep the original local image source in the task.
        digest = _pack(tree, archive, include_image=has_image and not push_image,
                       compress_level=compress_level)
        extra = {}
        if image_release_dst_acr:
            from .release import image_release_meta
            extra.update(image_release_meta(docker_ref, client._p.effective_acr_host,
                                            image_release_dst_acr))
        if image_pushed:
            extra.update(harbor_image_source_digest=image_digest, harbor_image_delivered=True)
        meta = DatasetInstance(instance_id=instance_id, dataset=dataset, dataset_version=version,
                               split=split, owner_reference=owner,
                               docker_image=docker_ref or None,
                               difficulty=report.metadata.get("difficulty"),
                               tags=_tags(report.metadata), extend_meta=extra,
                               instance_status="draft")
        meta.manifest = _manifest(client._p.oss_bucket, dataset, version, instance_id,
                                  split, digest, layout)
        outcome = client._content.put(instance_id, dataset, version, split, archive,
                                      meta.to_canonical_json(), overwrite=overwrite, layout=layout)
        skipped = bool(outcome.get("skipped"))
        if verify or skipped:
            downloaded = root / "readback.tgz"
            client._content.get(dataset, version, instance_id, split, downloaded,
                                expected_digest=digest, layout=layout)
            if not downloaded.is_file() or not verify_file_digest(downloaded, digest):
                raise TransportError("multi-step archive readback differs from delivered bytes")
        # Register only after every task file and optional image has completed delivery.
        ingest = client._after_upload(register, dataset, version, instance_id, split=split)
        return PushResult(instance_id=instance_id, uploaded=not skipped, skipped=skipped,
                          image_pushed=image_pushed, docker_image=docker_ref or None,
                          digests={"content.tgz": digest}, ingest=ingest)
