import fnmatch

from metaflow import FlowMutator
from metaflow.exception import MetaflowException

VALID_SCHEDULE_KEYS = {"cron", "daily", "weekly", "hourly", "timezone"}


class ProjectScheduleException(MetaflowException):
    headline = "\nProject Schedule Exception"

    def __init__(self, msg):
        super().__init__(msg)


class project_schedule(FlowMutator):
    """
    Branch-aware scheduling for ProjectFlow.

    Applies Metaflow's @schedule decorator based on which branch the flow
    is deployed to. Takes a dict mapping branch glob patterns to schedule
    specifications. First matching pattern wins (dict insertion order).

    If the deployed branch doesn't match any pattern, no schedule is applied.

    Example:
        @project_schedule({
            "main": {"cron": "0 8 * * 1-5", "timezone": "America/New_York"},
            "develop": {"daily": True},
            "release/*": {"hourly": True},
        })
        class MyFlow(ProjectFlow):
            ...
    """

    def init(self, schedule_map):
        if not isinstance(schedule_map, dict):
            raise ProjectScheduleException(
                "@project_schedule expects a dict mapping branch patterns to schedule specs. "
                "Example: @project_schedule({'main': {'daily': True}})"
            )
        if not schedule_map:
            raise ProjectScheduleException(
                "@project_schedule schedule map cannot be empty."
            )
        for pattern, spec in schedule_map.items():
            if not isinstance(spec, dict):
                raise ProjectScheduleException(
                    f"Schedule spec for pattern '{pattern}' must be a dict, "
                    f"got {type(spec).__name__}. "
                    f"Example: {{'{pattern}': {{'daily': True}}}}"
                )
            invalid_keys = set(spec.keys()) - VALID_SCHEDULE_KEYS
            if invalid_keys:
                raise ProjectScheduleException(
                    f"Invalid schedule keys {invalid_keys} for pattern '{pattern}'. "
                    f"Valid keys: {VALID_SCHEDULE_KEYS}"
                )
        self.schedule_map = schedule_map

    def pre_mutate(self, mutable_flow):
        project_config = dict(mutable_flow.configs).get("project_config")
        project_spec = dict(mutable_flow.configs).get("project_spec")
        if project_config is None:
            raise ProjectScheduleException(
                "You can apply @project_schedule only to ProjectFlows"
            )

        # Resolve branch -- same logic as project_trigger
        branch = None

        # 1. Deployed via obproject-deploy: use git branch from project_spec
        if project_spec:
            spec = project_spec.get("spec", project_spec)
            branch = spec.get("project_branch") or project_spec.get("branch")

        # 2. Check [dev-assets] config
        if not branch:
            dev_config = project_config.get("dev-assets", {})
            branch = dev_config.get("branch")

        if not branch:
            print("[@project_schedule] No branch resolved. Schedule not applied.")
            return

        # Match against patterns using the raw branch name (before sanitization)
        # so users can write patterns like "release/*" matching "release/v2"
        for pattern, spec in self.schedule_map.items():
            if fnmatch.fnmatch(branch, pattern):
                print(
                    f"[@project_schedule] Branch '{branch}' matched pattern "
                    f"'{pattern}'. Applying schedule: {spec}"
                )
                mutable_flow.add_decorator(
                    "schedule",
                    deco_kwargs=spec,
                    duplicates=mutable_flow.ERROR,
                )
                return

        print(
            f"[@project_schedule] Branch '{branch}' did not match any pattern "
            f"in {list(self.schedule_map.keys())}. No schedule applied."
        )
