from metaflow import FlowMutator
from metaflow.integrations import ArgoEvent


def event_name(name, project, branch):
    return f"prj.{project}.{branch}.{name}"


class ProjectEvent:
    def __init__(self, name, project, branch):
        self.project = project
        self.branch = branch
        self.event = event_name(name, project, branch)

    def publish(self, payload=None):
        ArgoEvent(self.event).publish(payload=payload)

    def safe_publish(self, payload=None):
        ArgoEvent(self.event).safe_publish(payload=payload)


class project_trigger(FlowMutator):
    def init(self, *args, **kwargs):
        self.event_suffix = kwargs.get("event")
        if self.event_suffix is None:
            raise AttributeError("Specify an event name: @project_trigger(event=NAME)")

    def pre_mutate(self, mutable_flow):
        from .projectbase import _detect_git_branch, _sanitize_branch_name

        project_config = dict(mutable_flow.configs).get("project_config")
        project_spec = dict(mutable_flow.configs).get("project_spec")
        if project_config is None:
            raise KeyError("You can apply @project_trigger only to ProjectFlows")

        project = project_config["project"]

        # Determine which branch to listen on (at decoration time, no 'current' available)
        # Priority: project_spec git branch → [dev-assets] config → local git → "main"
        branch = None

        # 1. Deployed: use git branch from project_spec
        if project_spec:
            spec = project_spec.get("spec", project_spec)
            branch = spec.get("project_branch") or project_spec.get("branch")

        # 2. Check [dev-assets] config (listen to events from configured branch)
        if not branch:
            dev_config = project_config.get("dev-assets", {})
            branch = dev_config.get("branch")

        # 3. Local with git: detect from repo
        if not branch:
            branch = _detect_git_branch()

        # 4. Fallback to main
        if not branch:
            branch = "main"

        branch = _sanitize_branch_name(branch)
        event = event_name(self.event_suffix, project, branch)
        mutable_flow.add_decorator(
            "trigger", deco_kwargs={"event": event}, duplicates=mutable_flow.ERROR
        )
