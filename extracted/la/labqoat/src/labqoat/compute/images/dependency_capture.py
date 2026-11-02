"""Capture dependency operation inputs without executing a package installer on the submitting host."""

from collections.abc import Callable

from labqoat.compute.images.apt_step import AptStep
from labqoat.compute.images.input_tree import InputTree
from labqoat.compute.images.pip_step import PipStep
from labqoat.compute.images.sync_step import SyncStep
from labqoat.compute.images.uv_project import UvProject
from labqoat.json_document import JsonValue


class DependencyCapture:
    """Replace local dependency paths with content-addressed build inputs."""

    def __init__(self, capture: Callable[[InputTree], str]) -> None:
        """Use the owning image capture's bounded tree publisher."""
        self._tree = capture

    def capture(self, operation: PipStep | SyncStep | AptStep) -> dict[str, JsonValue]:
        """Preserve the typed package selection and exact authored operation order."""
        if isinstance(operation, AptStep):
            return {"kind": "apt", "packages": list(operation.packages)}
        if isinstance(operation, SyncStep):
            return self._sync(operation)
        return self._pip(operation)

    def _pip(self, operation: PipStep) -> dict[str, JsonValue]:
        """Keep direct pins unresolved for the service and snapshot supplied lockfiles immediately."""
        result: dict[str, JsonValue] = {
            "kind": "pip",
            "packages": list(operation.packages),
            "index_url": operation.index_url,
        }
        if operation.requirements is not None:
            result["requirements"] = (
                self._tree(InputTree.capture({"requirements.txt": operation.requirements})) + "/requirements.txt"
            )
        return result

    def _sync(self, operation: SyncStep) -> dict[str, JsonValue]:
        """Capture dependency metadata separately from selected workspace source files."""
        project = UvProject(operation)
        source, paths = project.sources()
        return {
            "kind": "uv_sync",
            "input": self._tree(project.metadata),
            "source": None if source is None else self._tree(source),
            "python_paths": list(paths),
            "package": operation.package,
            "groups": list(operation.groups),
            "extras": list(operation.extras),
        }
