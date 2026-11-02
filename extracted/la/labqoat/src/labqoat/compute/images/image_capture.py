"""Capture one image's selected local inputs into a portable retained recipe."""

from pathlib import Path

from labqoat.compute.context_files import ContextFiles
from labqoat.compute.image import Image
from labqoat.compute.images.command_step import CommandStep
from labqoat.compute.images.dependency_command_step import DependencyCommandStep
from labqoat.compute.images.copy_step import CopyStep
from labqoat.compute.images.env_step import EnvStep
from labqoat.compute.images.input_tree import InputTree
from labqoat.compute.images.operation import Operation
from labqoat.compute.images.workdir_step import WorkdirStep
from labqoat.compute.images.stage_step import StageStep
from labqoat.compute.images.dependency_capture import DependencyCapture
from labqoat.compute.images.copy_destinations import CopyDestinations
from labqoat.json_document import JsonValue
from labqoat.schemas.identity import Identity


class ImageCapture:
    """Stage content-addressed files while preserving the authored operation order."""

    def __init__(self, directory: Path) -> None:
        """Own the temporary publication directory and one selected image manifest."""
        self.directory = directory
        self.files: dict[str, JsonValue] = {}
        self._stages: list[JsonValue] = []
        self._indices: dict[str, int] = {}
        self._active: set[int] = set()

    def tree(self, tree: InputTree) -> str:
        """Retain a deduplicated immutable tree and bind all its bytes to this image."""
        self.files.update(tree.write(self.directory))
        return tree.prefix

    def capture(self, image: Image, runtime: dict[str, JsonValue]) -> dict[str, JsonValue]:
        """Return only portable recipe values; host paths never enter build identity."""
        self._stage(image)
        return {
            "version": "1",
            "platform": "linux/amd64",
            "stages": list(self._stages),
            "runtime": runtime,
            "files": dict(self.files),
        }

    def _step(self, operation: Operation) -> dict[str, JsonValue]:
        """Serialize typed operations after replacing local selections with immutable tree paths."""
        if isinstance(operation, CommandStep):
            return {"kind": "run", "commands": list(operation.commands)}
        if isinstance(operation, DependencyCommandStep):
            return {"kind": "dependency_run", "commands": list(operation.commands)}
        if isinstance(operation, EnvStep):
            return {"kind": "env", "values": dict(operation.values)}
        if isinstance(operation, WorkdirStep):
            return {"kind": "workdir", "path": operation.path}
        if isinstance(operation, CopyStep):
            return self._copy(operation)
        if isinstance(operation, StageStep):
            return {
                "kind": "copy_from",
                "stage": self._stage(operation.image),
                "source": operation.source,
                "destination": operation.destination,
            }
        return DependencyCapture(self.tree).capture(operation)

    def _stage(self, image: Image) -> int:
        """Derive a deterministic acyclic stage graph with content-based stage deduplication."""
        if id(image) in self._active or len(self._active) + len(self._stages) >= 32:
            raise ValueError("Image stages must form an acyclic graph of at most 32 stages")
        if not image.base:
            raise ValueError("Image stages require a digest-pinned registry base")
        self._active.add(id(image))
        CopyDestinations.validate(image.operations)
        steps: list[JsonValue] = [self._step(operation) for operation in image.operations]
        stage: dict[str, JsonValue] = {"base": image.base, "steps": steps}
        digest = Identity.digest(stage)
        self._active.remove(id(image))
        if digest not in self._indices:
            self._indices[digest] = len(self._stages)
            self._stages.append(stage)
        return self._indices[digest]

    def _copy(self, operation: CopyStep) -> dict[str, JsonValue]:
        """Keep file and directory destinations consistent with ordinary COPY semantics."""
        files = (
            ContextFiles.directory(operation.path, operation.ignore)
            if operation.directory
            else {"file": operation.path}
        )
        source = self.tree(InputTree.capture(files))
        if not operation.directory:
            source += "/file"
        return {"kind": "copy", "input": source, "destination": operation.destination}
