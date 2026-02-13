import os

from metaflow import FlowMutator, current
from metaflow.integrations import ArgoEvent
from metaflow.exception import MetaflowException


def event_name(name, project, branch):
    return f"prj.{project}.{branch}.{name}"


def _extract_branch(metaflow_branch):
    """Extract git branch from Metaflow project branch name.

    Metaflow @project adds prefixes to branch names:
    - user.{username} → user's personal namespace (no git branch)
    - test.{git_branch} → test deployment of git branch
    - prod → production (defaults to "main")
    - prod.{git_branch} → production variant of git branch

    This is only used as a fallback when OB_BRANCH env var is not set.
    """

    if metaflow_branch.startswith("test."):
        resolved_branch = metaflow_branch[5:]
    elif metaflow_branch.startswith("prod."):
        resolved_branch = metaflow_branch[5:]
    elif metaflow_branch.startswith("user."):
        resolved_branch = metaflow_branch[5:]
    elif metaflow_branch == "prod":
        resolved_branch = "main"
    else:
        raise MetaflowException(f"[project_events._extract_branch] Unknown metaflow branch structure: {metaflow_branch}")

    print(f"metaflow branch {metaflow_branch} resolved to {resolved_branch}.")

    return resolved_branch


class ProjectEvent:
    """Publish events that can trigger flows with @project_trigger.

    Args:
        name: Event name (must match the event= in @project_trigger)
        project: Project name. If None, auto-detects from OB_PROJECT env var
                 or current.project_name
        branch: Branch name. If None, auto-detects from OB_BRANCH env var
                 or extracts from current.branch_name

    Example:
        # Auto-detect project and branch (recommended)
        ProjectEvent("my_event").publish(payload={"key": "value"})

        # Explicit (if needed)
        ProjectEvent("my_event", project="myproj", branch="main").publish()
    """
    def __init__(self, name, project=None, branch=None):
        # Auto-detect: prefer OB_PROJECT/OB_BRANCH env vars (set by obproject-deploy)
        # Fall back to current.project_name / current.branch_name for flows
        if project is None:
            project = os.environ.get("OB_PROJECT") or current.project_name
        if branch is None:
            branch = os.environ.get("OB_BRANCH") or _extract_branch(current.branch_name)

        print(f"ProjectEvent: project={project}, branch={branch}")
        self.project = project
        self.branch = branch
        self.event = event_name(name, project, branch)

    def publish(self, payload=None):
        return ArgoEvent(self.event).publish(payload=payload)

    def safe_publish(self, payload=None):
        return ArgoEvent(self.event).safe_publish(payload=payload)


class project_trigger(FlowMutator):
    def init(self, *args, **kwargs):
        self.event_suffix = kwargs.get("event")
        if self.event_suffix is None:
            raise AttributeError("Specify an event name: @project_trigger(event=NAME)")

    def pre_mutate(self, mutable_flow):
        from .projectbase import _sanitize_branch_name

        project_config = dict(mutable_flow.configs).get("project_config")
        project_spec = dict(mutable_flow.configs).get("project_spec")
        if project_config is None:
            raise KeyError("You can apply @project_trigger only to ProjectFlows")

        project = project_config["project"]

        # Get branch from project_spec (set by obproject-deploy) or [dev-assets] config
        branch = None

        # 1. Deployed via obproject-deploy: use git branch from project_spec
        if project_spec:
            spec = project_spec.get("spec", project_spec)
            branch = spec.get("project_branch") or project_spec.get("branch")

        # 2. Check [dev-assets] config (listen to events from configured branch)
        if not branch:
            dev_config = project_config.get("dev-assets", {})
            branch = dev_config.get("branch")

        if not branch:
            # raise ProjectTriggerException(
            #     f"No branch resolved for project {project}. "
            #     "Did you use obproject-deploy to deploy the project?"
            # )
            print(f"[@project_trigger] No branch resolved for project {project}.")
            return

        branch = _sanitize_branch_name(branch)
        event = event_name(self.event_suffix, project, branch)
        mutable_flow.add_decorator(
            "trigger", deco_kwargs={"event": event}, duplicates=mutable_flow.ERROR
        )


class ProjectTriggerException(MetaflowException):
    headline = "\nProject Trigger Exception"
    def __init__(self, msg):
        super().__init__(msg)