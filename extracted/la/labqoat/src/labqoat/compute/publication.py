"""Automatic source, callable and image publication through an explicit management transport."""

import tempfile
from pathlib import Path
from typing import ParamSpec, TypeVar

from labqoat._generated.asset_record import AssetRecord
from labqoat._generated.compute_publication import ComputePublication
from labqoat.assets_client import AssetsClient
from labqoat.compute.function import Function
from labqoat.compute.image import Image
from labqoat.compute.images.declared_image import DeclaredImage
from labqoat.compute.images.input_tree import InputTree
from labqoat.compute.images.publication_capture import PublicationCapture
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.compute.source_archive import SourceArchive
from labqoat.compute.upload_memo import UploadMemo

P = ParamSpec("P")
R = TypeVar("R")


class Publication:
    """Capture an App's selected function and its complete declared build context before submission."""

    def __init__(self, assets: AssetsClient, uploads: UploadMemo | None = None) -> None:
        """Use only the caller's explicit asset transport and optional memory of accepted archives."""
        self._assets = assets
        self._uploads = uploads

    def capture(self, function: Function[P, R], application: InputTree | None = None) -> ComputePublication:
        """Publish the image context and the application source as separate immutable archives.

        ``application`` replaces the source of the function's own modules; see ``PublicationCapture.capture``.
        """
        declaration = function.capture()
        with tempfile.TemporaryDirectory(prefix="labqoat-compute-") as directory:
            root = Path(directory) / "context"
            captured = PublicationCapture.capture(function.registry.closure(), root, application)
            context = self._upload(root, Path(directory) / "source.tar.gz")
            staged = Path(directory) / "application"
            files = captured.source.write(staged)
            delivered = self._upload(staged, Path(directory) / "application.tar.gz")
        return ComputePublication(
            app_name=function.app_name,
            source_asset_sha=context.sha256,
            image=JsonDocument.expect_scalar(
                captured.bindings[f"{declaration.module}:{function.local.__qualname__}"], str
            ),
            images=captured.images,
            bindings=captured.bindings,
            runtime_version="1",
            recovery_protocol=1,
            distributed_recovery_protocol=1,
            workflow_replay_protocol=1,
            app={"asset": self._reference(delivered), "tree": captured.source.prefix, "files": files},
            function=declaration,
        )

    def image_build(self, image: Image, application: InputTree) -> dict[str, JsonValue]:
        """Publish one image's build context and return the recipe that builds it on its own.

        The image carries the managed runtime as every function's image does; ``application`` only completes the
        capture and is not part of what is built.
        """
        declared = DeclaredImage("labqoat_image", "image", Path("labqoat_image.py"), image)
        with tempfile.TemporaryDirectory(prefix="labqoat-image-") as directory:
            root = Path(directory) / "context"
            captured = PublicationCapture.capture((declared,), root, application)
            context = self._upload(root, Path(directory) / "source.tar.gz")
        recipe = captured.images[JsonDocument.expect_scalar(captured.bindings[declared.key], str)]
        return {"source_asset_sha": context.sha256, "runtime_version": "1", "source_kind": "archive", "image": recipe}

    def _upload(self, root: Path, archive: Path) -> AssetRecord:
        """Archive one staged tree deterministically; a tree accepted before is neither archived nor sent again."""
        entries = tuple(sorted(path for path in root.rglob("*") if path.is_file()))
        if len(entries) > 4000 or sum(path.stat().st_size for path in entries) > 256 * 1024 * 1024:
            raise ValueError("App image closure exceeds the source archive bounds")
        if self._uploads is None:
            SourceArchive.write(root, entries, archive)
            return self._assets.upload_file(archive, "application/gzip")
        tree = SourceArchive.digest(root, entries)
        known = self._uploads.find(tree)
        if known is None:
            known = self._archived(self._uploads, root, entries, archive)
            self._uploads.remember(known, tree)
        return known

    def _archived(self, uploads: UploadMemo, root: Path, entries: tuple[Path, ...], archive: Path) -> AssetRecord:
        """Compress the tree and send it unless the service already holds those exact bytes."""
        SourceArchive.write(root, entries, archive)
        return uploads.find(AssetsClient.hash_file(archive)[0]) or self._assets.upload_file(archive, "application/gzip")

    @staticmethod
    def _reference(record: AssetRecord) -> dict[str, JsonValue]:
        """Name the delivered archive by the complete immutable identity workers must match."""
        return {
            "id": record.id,
            "blob_sha256": record.sha256,
            "byte_size": record.byte_size,
            "media_type": record.media_type,
        }
