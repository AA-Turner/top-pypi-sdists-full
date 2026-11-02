"""Capture locked uv workspace metadata and only selected local dependency sources."""

import tomllib
from pathlib import Path

from labqoat.compute.context_files import ContextFiles
from labqoat.compute.images.input_tree import InputTree
from labqoat.compute.images.sync_step import SyncStep
from labqoat.json_document import JsonDocument


class UvProject:
    """Separate dependency metadata from source bytes so source edits preserve install layers."""

    def __init__(self, step: SyncStep) -> None:
        """Read validated local lock and project files only during explicit publication."""
        self.step = step
        self.root = step.project
        self.metadata = self._metadata()
        self.lock = self._document(self.root / "uv.lock")

    @staticmethod
    def _document(path: Path) -> JsonDocument:
        """Apply ordinary input-file boundaries before parsing TOML."""
        tree = InputTree.capture({"file": path})
        return JsonDocument.expect_dict(JsonDocument.expect_value(tomllib.loads(tree.entries[0][1].decode())))

    def _metadata(self) -> InputTree:
        """Capture root declarations plus workspace member manifests required by uv export."""
        files = {"pyproject.toml": self.root / "pyproject.toml", "uv.lock": self.root / "uv.lock"}
        project = self._document(files["pyproject.toml"])
        tool = JsonDocument.expect_dict(project.get("tool", {}))
        uv = JsonDocument.expect_dict(tool.get("uv", {}))
        workspace = JsonDocument.expect_dict(uv.get("workspace", {}))
        for pattern in JsonDocument.expect_list(workspace.get("members", [])):
            for member in self.root.glob(JsonDocument.expect_scalar(pattern, str)):
                path = member / "pyproject.toml"
                files[path.relative_to(self.root).as_posix()] = path
        return InputTree.capture(files)

    def sources(self) -> tuple[InputTree | None, tuple[str, ...]]:
        """Return selected src-layout or flat-layout packages and their relative import roots."""
        files: dict[str, Path] = {}
        paths: list[str] = []
        for package in self._selected():
            self._source(package, files, paths)
        return (InputTree.capture(files) if files else None), tuple(sorted(set(paths)))

    def _selected(self) -> list[JsonDocument]:
        """Traverse the retained lock's selected package graph without resolving mutable indexes."""
        records = [JsonDocument.expect_dict(value) for value in JsonDocument.expect_list(self.lock["package"])]
        project = JsonDocument.expect_dict(self._document(self.root / "pyproject.toml")["project"])
        selected = self.step.package or JsonDocument.expect_scalar(project["name"], str)
        pending = [selected]
        visited: set[str] = set()
        found: list[JsonDocument] = []
        while pending:
            name = pending.pop()
            if name in visited:
                continue
            visited.add(name)
            matches = [record for record in records if record["name"] == name]
            if not matches:
                raise ValueError(f"Package {name} is missing from the captured uv lock")
            for package in matches:
                pending.extend(self._dependencies(package))
                found.append(package)
        return found

    def _dependencies(self, package: JsonDocument) -> list[str]:
        """Include regular dependencies and explicitly selected optional groups."""
        dependencies = JsonDocument.expect_list(package.get("dependencies", []))
        extras = JsonDocument.expect_dict(package.get("optional-dependencies", {}))
        groups = JsonDocument.expect_dict(package.get("dev-dependencies", {}))
        for name in self.step.extras:
            dependencies.extend(JsonDocument.expect_list(extras.get(name, [])))
        for name in self.step.groups:
            dependencies.extend(JsonDocument.expect_list(groups.get(name, [])))
        return [JsonDocument.expect_scalar(JsonDocument.expect_dict(value)["name"], str) for value in dependencies]

    def _source(self, package: JsonDocument, files: dict[str, Path], paths: list[str]) -> None:
        """Ignore registry packages and use the managed SDK instead of a checkout-local SDK path."""
        source = JsonDocument.expect_dict(package["source"])
        local = source.get("editable", source.get("virtual"))
        if local is None or package["name"] == "labqoat":
            return
        path = Path(JsonDocument.expect_scalar(local, str))
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("uv workspace sources must remain inside the declared project")
        directory = self.root / path
        name = JsonDocument.expect_scalar(package["name"], str).replace("-", "_")
        if (directory / "src").is_dir():
            self._include(directory / "src", files, paths)
        elif (directory / name).is_dir():
            self._include(directory / name, files, paths, flat=True)

    def _include(self, directory: Path, files: dict[str, Path], paths: list[str], *, flat: bool = False) -> None:
        """Preserve workspace-relative locations while exposing import roots after source copying."""
        relative = directory.relative_to(self.root)
        files.update({(relative / name).as_posix(): path for name, path in ContextFiles.directory(directory).items()})
        paths.append((relative.parent if flat else relative).as_posix())
