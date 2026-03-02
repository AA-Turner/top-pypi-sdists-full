import os
from typing import Any, Dict, List
from ruamel.yaml import YAML

from dlt.common.configuration.providers import SecretsTomlProvider, ConfigTomlProvider
from dlt._workspace.cli import CliCommandException, echo as fmt
from dlt._workspace.cli.config_toml_writer import WritableConfigValue, write_values

from dlthub.project.project_context import ProjectRunContext, switch_context
from dlthub.common.constants import DEFAULT_PROJECT_CONFIG_FILE


class ProjectWriteState:
    def __init__(self, run_context: ProjectRunContext, read_project_yaml: bool = True) -> None:
        self.project_dir = run_context.run_dir
        self.settings_dir = run_context.settings_dir
        self.sources_dir = run_context.get_run_entity("sources")
        self.dlt_yaml: Dict[str, Any] = {}  # todo define type for this

        if read_project_yaml:
            self.dlt_yaml = self._read_project_yaml(self.project_dir)

        # Track new files to be added
        self.dirs_to_create: List[str] = []
        self.new_files: List[Dict[str, Any]] = []

        # Track secrets and config.toml
        self.secrets_provider = SecretsTomlProvider(self.settings_dir)
        self.config_provider = ConfigTomlProvider(self.settings_dir)
        # todo: not sure this intermediate step is really needed
        self.pending_secrets: List[WritableConfigValue] = []

    def add_new_file(self, path: str, content: str, accept_existing: bool = False) -> None:
        """Adds a new file to the list of files to be created."""
        self.new_files.append({
            "path": path,
            "content": content,
            "accept_existing": accept_existing,
        })

    def check_file_conflicts(self) -> None:
        """
        Validates the list of new files to be created.

        This method checks if any file in `self.new_files` already exists in the project directory.

        Raises:
            FileExistsError: If a file already exists and `accept_existing` is `False`.
        """
        for file in self.new_files:
            full_path = os.path.join(self.project_dir, file["path"])
            if not file["accept_existing"] and os.path.exists(full_path):
                fmt.error(
                    """
                File Conflict: <%s> already exists in project. Use --force to overwrite this
                and other existing files.
                """
                    % os.path.basename(file["path"])
                )
                raise CliCommandException(
                    docs_url="https://dlthub.com/docs/plus/getting-started/tutorial"
                )

    def commit(self, allow_overwrite: bool = False) -> None:
        """Writes all changes to disk atomically."""
        if not allow_overwrite:
            self.check_file_conflicts()

        # Create directories
        for dir in self.dirs_to_create:
            os.makedirs(dir, exist_ok=True)

        # Write new files
        for file in self.new_files:
            # full_path = os.path.join(self.project_dir, file["path"])
            if file["accept_existing"] and os.path.exists(file["path"]):
                continue
            with open(file["path"], "w", encoding="utf-8") as f:
                f.write(file["content"])

        # Save dlt.yml
        self._write_project_yaml(self.project_dir, self.dlt_yaml)

        # Call `reload` on `PluggableRunContext` to re-trigger plugin hook
        # Makes sure that Python modules within project are importable
        # creates .dlt/.var directory
        switch_context(self.project_dir)

        # Write secrets.toml
        if self.pending_secrets:
            write_values(
                self.secrets_provider._config_toml, self.pending_secrets, overwrite_existing=False
            )
        self.secrets_provider.write_toml()

    def add_secrets_value(self, value: WritableConfigValue) -> None:
        """Adds a WritableConfigValue to the pending secrets."""
        self.pending_secrets.append(value)

    def _read_project_yaml(self, run_dir: str) -> Any:
        """Read the project yaml file."""

        yaml = YAML()
        project_yaml_path = os.path.join(run_dir, DEFAULT_PROJECT_CONFIG_FILE)
        with open(project_yaml_path, "r", encoding="utf-8") as file:
            return yaml.load(file)

    def _write_project_yaml(self, project_dir: str, project_yaml: Any) -> None:
        """Write the project yaml file."""

        yaml = YAML()
        yaml.indent(mapping=2, sequence=4, offset=2)
        project_yaml_path = os.path.join(project_dir, DEFAULT_PROJECT_CONFIG_FILE)
        with open(project_yaml_path, "w", encoding="utf-8") as file:
            yaml.dump(project_yaml, file)

    @classmethod
    def from_run_context(cls, run_context: ProjectRunContext) -> "ProjectWriteState":
        """Creates a ProjectState instance from a ProjectRunContext, trying to read dlt.yaml"""
        return cls(run_context, read_project_yaml=True)
