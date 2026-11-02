"""Install verified application source before any authored module is imported."""

import hashlib
import importlib
import os
import sys
import tarfile
from pathlib import Path, PurePosixPath

from labqoat._generated.compute_publication import ComputePublication
from labqoat.compute.run_assets import RunAssets
from labqoat.json_document import JsonDocument, JsonValue


class DeliveredSource:
    """Keep one hash-verified copy of each published tree per worker and fetch it only when absent or altered."""

    @staticmethod
    def install(publication: ComputePublication, assets: RunAssets, scratch: Path) -> None:
        """Make the publication's import root resolvable; images that bake their source need nothing."""
        if publication.app is None:
            return
        files = JsonDocument.expect_dict(publication.app["files"])
        root = Path(os.environ.get("LABQOAT_CACHE_DIR", str(scratch))) / "source"
        if not DeliveredSource._intact(root, files):
            DeliveredSource._fetch(JsonDocument.expect_dict(publication.app["asset"]), assets, root, files)
        sys.path.insert(0, str(root / JsonDocument.expect_scalar(publication.app["tree"], str)))
        importlib.invalidate_caches()

    @staticmethod
    def _intact(root: Path, files: dict[str, JsonValue]) -> bool:
        """Trust retained bytes only while every declared file still matches its published hash."""
        try:
            return bool(files) and all(
                isinstance(declared, dict)
                and hashlib.sha256((root / name).read_bytes()).hexdigest() == declared["sha256"]
                for name, declared in files.items()
            )
        except OSError:
            return False

    @staticmethod
    def _fetch(reference: dict[str, JsonValue], assets: RunAssets, root: Path, files: dict[str, JsonValue]) -> None:
        """Extract exactly the declared files from the assignment-authorized archive."""
        with assets.local_file(reference) as archive, tarfile.open(archive, "r:gz") as source:
            written = [DeliveredSource._extract(source, member, files, root) for member in source]
        if sorted(written) != sorted(files):
            raise ValueError("Delivered application source does not match its publication")

    @staticmethod
    def _extract(source: tarfile.TarFile, member: tarfile.TarInfo, files: dict[str, JsonValue], root: Path) -> str:
        """Publish one declared regular file atomically, only after its bytes match the published hash."""
        confined = ".." not in PurePosixPath(member.name).parts and not member.name.startswith("/")
        declared = files.get(member.name) if confined else None
        content = source.extractfile(member) if member.isfile() and isinstance(declared, dict) else None
        data = b"" if content is None else content.read()
        if content is None or not isinstance(declared, dict) or hashlib.sha256(data).hexdigest() != declared["sha256"]:
            raise ValueError("Delivered application source does not match its publication")
        target = root / member.name
        target.parent.mkdir(parents=True, exist_ok=True)
        staged = target.with_name(f"{target.name}.{os.getpid()}.staged")
        staged.write_bytes(data)
        staged.chmod(0o755 if declared["mode"] == 0o755 else 0o644)
        staged.replace(target)
        return member.name
