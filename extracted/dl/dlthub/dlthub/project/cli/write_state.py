import os
from typing import Any, Dict
from ruamel.yaml import YAML

from dlt.common.storages.file_storage import FileStorage
from dlt._workspace.cli._write_state import WorkspaceWriteState

from dlthub.project.project_context import ProjectRunContext, switch_context
from dlthub.common.constants import DEFAULT_PROJECT_CONFIG_FILE


class ProjectWriteState(WorkspaceWriteState):
    """Adds dlt.yml read/write and post-commit switch_context to the base."""

    def __init__(self, run_context: ProjectRunContext, read_project_yaml: bool = True) -> None:
        super().__init__(
            dest_storage=FileStorage(run_context.run_dir),
            settings_dir=run_context.settings_dir,
        )
        self.project_dir = run_context.run_dir
        self.sources_dir = run_context.get_run_entity("sources")
        self.dlt_yaml: Dict[str, Any] = {}
        if read_project_yaml:
            self.dlt_yaml = self._read_project_yaml(self.project_dir)

    @classmethod
    def from_run_context(cls, run_context: ProjectRunContext) -> "ProjectWriteState":
        return cls(run_context, read_project_yaml=True)

    def _after_files_hook(self) -> None:
        # writes dlt.yml, then re-plugs the run context so .dlt/state lands on disk
        self._write_project_yaml(self.project_dir, self.dlt_yaml)
        switch_context(self.project_dir)

    def _read_project_yaml(self, run_dir: str) -> Any:
        yaml = YAML()
        path = os.path.join(run_dir, DEFAULT_PROJECT_CONFIG_FILE)
        with open(path, "r", encoding="utf-8") as fh:
            return yaml.load(fh)

    def _write_project_yaml(self, project_dir: str, project_yaml: Any) -> None:
        yaml = YAML()
        yaml.indent(mapping=2, sequence=4, offset=2)
        path = os.path.join(project_dir, DEFAULT_PROJECT_CONFIG_FILE)
        with open(path, "w", encoding="utf-8") as fh:
            yaml.dump(project_yaml, fh)
