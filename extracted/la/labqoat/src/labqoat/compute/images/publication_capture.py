"""Automatically derive the complete retained App image closure for root publication."""

from dataclasses import dataclass
from pathlib import Path

from labqoat.compute.images.app_source import AppSource
from labqoat.compute.images.declared_image import DeclaredImage
from labqoat.compute.images.image_capture import ImageCapture
from labqoat.compute.images.input_tree import InputTree
from labqoat.compute.images.runtime_bundle import RuntimeBundle
from labqoat.compute.images.base_catalog import BaseCatalog
from labqoat.json_document import JsonDocument, JsonValue
from labqoat.schemas.identity import Identity


@dataclass(frozen=True)
class PublicationCapture:
    """Retain image recipes once and bind every registered callable to an exact image identity."""

    images: dict[str, JsonValue]
    bindings: dict[str, JsonValue]
    source: InputTree

    @classmethod
    def capture(
        cls, declarations: tuple[DeclaredImage, ...], directory: Path, application: InputTree | None = None
    ) -> "PublicationCapture":
        """Capture the managed runtime into every image; application source stays outside for delivery at start.

        The application is the declared modules' source unless one is given, as for functions the SDK itself
        defines, whose modules are imported from the runtime every image carries.
        """
        sdk = RuntimeBundle.source()
        metadata = RuntimeBundle.metadata()
        common = ImageCapture(directory)
        runtime: dict[str, JsonValue] = {
            "source": common.tree(sdk),
            "metadata": common.tree(metadata),
            "toolchain": cls._toolchain(),
        }
        images: dict[str, JsonValue] = {}
        bindings: dict[str, JsonValue] = {}
        captured: dict[int, str] = {}
        for declaration in declarations:
            identity = id(declaration.image)
            if identity not in captured:
                capture = ImageCapture(directory)
                capture.files.update(common.files)
                toolchain = JsonDocument.expect_dict(runtime["toolchain"])
                interpreter = {**toolchain, "python": declaration.image.python_version}
                recipe = capture.capture(declaration.image, {**runtime, "toolchain": interpreter})
                digest = Identity.digest(recipe)
                images[digest] = recipe
                captured[identity] = digest
            bindings[declaration.key] = captured[identity]
        return cls(images, bindings, AppSource.capture(declarations) if application is None else application)

    @staticmethod
    def _toolchain() -> dict[str, JsonValue]:
        """Retain the reproducibly pinned compiler identity once per publication."""
        return {
            "catalog": BaseCatalog.version,
            "python": "3.13",
            "uv": BaseCatalog.uv,
            "renderer": BaseCatalog.renderer,
            "apt_snapshot": BaseCatalog.snapshot,
        }
