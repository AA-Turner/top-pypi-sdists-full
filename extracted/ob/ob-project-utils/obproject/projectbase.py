import os
from metaflow import (
    FlowSpec,
    Config,
    config_expr,
    project,
    get_namespace,
    namespace,
    Task,
    pyproject_toml_parser,
    FlowMutator,
)

from subprocess import check_output

from .assets import Asset
from .evals_logger import EvalsLogger
from .project_events import ProjectEvent

project_ctx = None


def toml_parser(cfgstr):
    try:
        # python >= 3.11
        import tomllib as toml
    except ImportError:
        import toml
    return toml.loads(cfgstr)


def resolve_scope(project_config, project_spec, show_output=False):
    project = project_config["project"]
    read_only = True
    if project_spec:
        branch = project_spec["branch"]
        read_only = False
    elif project_config.get("dev-assets"):
        branch = project_config["dev-assets"].get("branch", "main")
        read_only = project_config["dev-assets"].get("read-only", True)
        if show_output:
            print(f"Using dev assets from branch {branch}")
    else:
        branch = "main"
        read_only = True
    return project, branch, read_only


class ProjectContext:
    def __init__(self, flow):
        self.flow = flow
        self.project_config = flow.project_config
        self.project_spec = flow.project_spec
        self.project, self.branch, self.read_only = resolve_scope(
            self.project_config, self.project_spec, show_output=True
        )
        print(
            f"Project initialized: {self.project}/{self.branch} | read-only: {self.read_only}"
        )
        self.asset = Asset(
            project=self.project, branch=self.branch, read_only=self.read_only
        )
        self.evals = EvalsLogger(project=self.project, branch=self.branch)

    def publish_event(self, name, payload=None):
        ProjectEvent(name, project=self.project, branch=self.branch).publish(payload)

    def safe_publish_event(self, name, payload=None):
        ProjectEvent(name, project=self.project, branch=self.branch).safe_publish(
            payload
        )

    def register_data(self, name, artifact):
        if hasattr(self.flow, artifact):
            self.asset.register_data_asset(
                name, kind="artifact", annotations={"artifact": artifact}
            )
        else:
            raise AttributeError(
                f"The flow doesn't have an artifact '{artifact}'. Is self.{artifact} set?"
            )

    def get_data(self, name):
        ref = self.asset.consume_data_asset(name)
        kind = ref["data_properties"]["data_kind"]
        if kind == "artifact":
            ns = get_namespace()
            try:
                namespace(None)
                task = Task(ref["created_by"]["entity_id"])
                artifact = ref["data_properties"]["annotations"]["artifact"]
                return task[artifact].data
            finally:
                namespace(ns)
        else:
            raise AttributeError(
                f"Data asset '{name}' doesn't seem like an artifact. It is of kind '{kind}'"
            )


class project_pypi(FlowMutator):
    def pre_mutate(self, mutable_flow):
        project_config = dict(mutable_flow.configs).get("project_config")
        project_deps = dict(mutable_flow.configs).get("project_deps")
        include_pyproject = project_config.get("dependencies", {}).get(
            "include_pyproject_toml", True
        )
        if include_pyproject and project_deps["packages"]:
            mutable_flow.add_decorator(
                "pypi_base", deco_kwargs=project_deps, duplicates=mutable_flow.ERROR
            )


@project_pypi
@project(name=config_expr("project_config.project"))
class ProjectFlow(FlowSpec):
    project_config = Config(
        "project_config", default="obproject.toml", parser=toml_parser
    )
    project_deps = Config(
        "project_deps", default_value="", parser=pyproject_toml_parser
    )
    project_spec = Config("project_spec", default_value="{}")

    @property
    def prj(self):
        global project_ctx
        if project_ctx is None:
            project_ctx = ProjectContext(self)
        return project_ctx
