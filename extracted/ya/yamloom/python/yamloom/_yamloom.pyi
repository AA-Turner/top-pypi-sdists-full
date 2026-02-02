from pathlib import Path
from collections.abc import Mapping
from types import ModuleType
from typing import Any, Literal, TypeVar

from typing_extensions import TypeAlias

from .expressions import (
    BooleanExpression,
    NumberExpression,
    StringExpression,
)

Ostr: TypeAlias = str | None
Obool: TypeAlias = bool | None
Oint: TypeAlias = int | None
StringLike: TypeAlias = str | StringExpression
BoolLike: TypeAlias = bool | BooleanExpression
IntLike: TypeAlias = int | NumberExpression
Ostrlike: TypeAlias = StringLike | None
Oboolstr: TypeAlias = BooleanExpression | str | None
Oboollike: TypeAlias = BoolLike | None
Ointlike: TypeAlias = IntLike | None
StringOrBoolLike: TypeAlias = StringLike | BoolLike

expressions: ModuleType

class Step: ...

_TActionStep = TypeVar('_TActionStep', bound='ActionStep')

class ActionStep(Step):
    def __new__(
        cls: type[_TActionStep],
        name: Ostrlike,
        action: str,
        *,
        ref: Ostr = None,
        with_opts: Mapping | None = None,
        args: Ostrlike = None,
        entrypoint: Ostrlike = None,
        condition: Oboolstr = None,
        id: Ostr = None,  # noqa: A002
        env: Mapping[str, StringLike] | None = None,
        continue_on_error: Oboollike = None,
        timeout_minutes: Ointlike = None,
        skip_recommended_permissions: bool = False,
        recommended_permissions: Permissions | None = None,
    ) -> _TActionStep: ...

def script(
    *script: StringLike,
    name: Ostrlike = None,
    condition: Oboolstr = None,
    working_directory: Ostrlike = None,
    shell: Ostr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    permissions: Permissions | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
) -> Step: ...
def action(
    name: Ostrlike,
    action: str,
    *,
    ref: Ostr = None,
    with_opts: Mapping | None = None,
    args: Ostrlike = None,
    entrypoint: Ostrlike = None,
    condition: Oboolstr = None,
    id: Ostr = None,  # noqa: A002
    env: Mapping[str, StringLike] | None = None,
    continue_on_error: Oboollike = None,
    timeout_minutes: Ointlike = None,
    skip_recommended_permissions: bool = False,
    recommended_permissions: Permissions | None = None,
) -> Step: ...

RW: TypeAlias = Literal['read', 'write', 'none'] | None
RO: TypeAlias = Literal['read', 'none'] | None
WO: TypeAlias = Literal['write', 'none'] | None

class Permissions:
    def __init__(
        self,
        *,
        actions: RW = None,
        artifact_metadata: RW = None,
        attestations: RW = None,
        checks: RW = None,
        contents: RW = None,
        deployments: RW = None,
        id_token: WO = None,
        issues: RW = None,
        models: RO = None,
        discussions: RW = None,
        packages: RW = None,
        pages: RW = None,
        pull_requests: RW = None,
        security_events: RW = None,
        statuses: RW = None,
    ) -> None: ...
    @staticmethod
    def none() -> Permissions: ...
    @staticmethod
    def read_all() -> Permissions: ...
    @staticmethod
    def write_all() -> Permissions: ...

class RunsOnSpec:
    def __init__(self, group: StringLike, labels: StringLike) -> None: ...
    @staticmethod
    def group(group: StringLike) -> RunsOnSpec: ...
    @staticmethod
    def labels(labels: StringLike) -> RunsOnSpec: ...

class RunsOn:
    def __init__(self, *args: StringLike) -> None: ...
    @staticmethod
    def spec(spec: RunsOnSpec) -> RunsOn: ...

class Environment:
    def __init__(self, name: StringLike, url: Ostrlike = None) -> None: ...

class Concurrency:
    def __init__(
        self, group: StringLike, *, cancel_in_progress: Oboollike = None
    ) -> None: ...

class RunDefaults:
    def __init__(
        self, *, shell: Ostrlike = None, working_directory: Ostrlike = None
    ) -> None: ...

class Defaults:
    def __init__(
        self,
        *,
        defaults: Mapping[str, str] | None = None,
        run_defaults: RunDefaults | None = None,
    ) -> None: ...

class Matrix:
    def __init__(
        self,
        *,
        include: list | None = None,
        exclude: list | None = None,
        **matrix: Any,
    ) -> None: ...

class Strategy:
    def __init__(
        self,
        *,
        matrix: Matrix | None = None,
        fast_fail: Oboollike = None,
        max_parallel: Ointlike = None,
    ) -> None: ...

class Credentials:
    def __init__(self, username: StringLike, password: StringLike) -> None: ...

class Container:
    def __init__(
        self,
        image: StringLike,
        *,
        credentials: Credentials | None = None,
        env: Mapping[str, StringLike] | None = None,
        ports: list[IntLike] | None = None,
        volumes: list[StringLike] | None = None,
        options: Ostrlike = None,
    ) -> None: ...

class JobSecrets:
    def __init__(self, secrets: Mapping[str, StringLike]) -> None: ...
    @staticmethod
    def inherit() -> JobSecrets: ...

class Job:
    def __init__(
        self,
        *,
        steps: list[Step] | None = None,
        name: Ostrlike = None,
        permissions: Permissions | None = None,
        use_recommended_permissions: bool = True,
        needs: list[str] | None = None,
        condition: Oboolstr = None,
        runs_on: RunsOnSpec | list[StringLike] | StringLike | None = None,
        snapshot: Ostr = None,
        environment: Environment | None = None,
        concurrency: Concurrency | None = None,
        outputs: Mapping[str, StringLike] | None = None,
        env: Mapping[str, StringLike] | None = None,
        defaults: Defaults | None = None,
        timeout_minutes: Ointlike = None,
        strategy: Strategy | None = None,
        continue_on_error: StringOrBoolLike | None = None,
        container: Container | None = None,
        services: Mapping[str, Container] | None = None,
        uses: Ostr = None,
        with_opts: Mapping | None = None,
        secrets: JobSecrets | None = None,
    ) -> None: ...

class BranchProtectionRuleEvent:
    def __init__(
        self, *, created: bool = False, edited: bool = False, deleted: bool = False
    ) -> None: ...

class CheckRunEvent:
    def __init__(
        self,
        *,
        created: bool = False,
        rerequested: bool = False,
        completed: bool = False,
        requested_action: bool = False,
    ) -> None: ...

class CheckSuiteEvent:
    def __init__(self, *, created: bool = False) -> None: ...

class DiscussionEvent:
    def __init__(
        self,
        *,
        created: bool = False,
        edited: bool = False,
        deleted: bool = False,
        transferred: bool = False,
        pinned: bool = False,
        unpinned: bool = False,
        labeled: bool = False,
        unlabeled: bool = False,
        locked: bool = False,
        unlocked: bool = False,
        category_changed: bool = False,
        answered: bool = False,
        unanswered: bool = False,
    ) -> None: ...

class DiscussionCommentEvent:
    def __init__(
        self, *, created: bool = False, edited: bool = False, deleted: bool = False
    ) -> None: ...

class ImageVersionEvent:
    def __init__(
        self,
        *,
        names: list[str] | None = None,
        versions: list[str] | None = None,
    ) -> None: ...

class IssueCommentEvent:
    def __init__(
        self, *, created: bool = False, edited: bool = False, deleted: bool = False
    ) -> None: ...

class IssuesEvent:
    def __init__(
        self,
        *,
        created: bool = False,
        edited: bool = False,
        deleted: bool = False,
        transferred: bool = False,
        pinned: bool = False,
        unpinned: bool = False,
        closed: bool = False,
        reopened: bool = False,
        assigned: bool = False,
        unassigned: bool = False,
        labeled: bool = False,
        unlabeled: bool = False,
        locked: bool = False,
        unlocked: bool = False,
        milestoned: bool = False,
        demilestoned: bool = False,
        typed: bool = False,
        untyped: bool = False,
    ) -> None: ...

class LabelEvent:
    def __init__(
        self, *, created: bool = False, edited: bool = False, deleted: bool = False
    ) -> None: ...

class MergeGroupEvent:
    def __init__(self, *, checks_requested: bool = False) -> None: ...

class MilestoneEvent:
    def __init__(
        self,
        *,
        created: bool = False,
        closed: bool = False,
        opened: bool = False,
        edited: bool = False,
        deleted: bool = False,
    ) -> None: ...

class PullRequestEvent:
    def __init__(
        self,
        *,
        branches: list[str] | None = None,
        branches_ignore: list[str] | None = None,
        paths: list[str] | None = None,
        paths_ignore: list[str] | None = None,
        assigned: bool = False,
        unassigned: bool = False,
        labeled: bool = False,
        unlabeled: bool = False,
        opened: bool = False,
        edited: bool = False,
        closed: bool = False,
        reopened: bool = False,
        synchronize: bool = False,
        converted_to_draft: bool = False,
        locked: bool = False,
        unlocked: bool = False,
        enqueued: bool = False,
        dequeued: bool = False,
        milestoned: bool = False,
        demilestoned: bool = False,
        ready_for_review: bool = False,
        review_requested: bool = False,
        review_request_removed: bool = False,
        auto_merge_enabled: bool = False,
        auto_merge_disabled: bool = False,
    ) -> None: ...

class PullRequestReviewEvent:
    def __init__(
        self, *, submitted: bool = False, edited: bool = False, dismissed: bool = False
    ) -> None: ...

class PullRequestReviewCommentEvent:
    def __init__(
        self, *, created: bool = False, edited: bool = False, deleted: bool = False
    ) -> None: ...

class PushEvent:
    def __init__(
        self,
        *,
        branches: list[str] | None = None,
        branches_ignore: list[str] | None = None,
        tags: list[str] | None = None,
        tags_ignore: list[str] | None = None,
        paths: list[str] | None = None,
        paths_ignore: list[str] | None = None,
    ) -> None: ...

class RegistryPackageEvent:
    def __init__(self, *, published: bool = False, updated: bool = False) -> None: ...

class ReleaseEvent:
    def __init__(
        self,
        *,
        published: bool = False,
        unpublished: bool = False,
        created: bool = False,
        edited: bool = False,
        deleted: bool = False,
        prereleased: bool = False,
        released: bool = False,
    ) -> None: ...

class RepositoryDispatchEvent:
    def __init__(self, *, types: list[str] | None = None) -> None: ...

class Minute:
    def __init__(self, minute: int | list[int]) -> None: ...
    @staticmethod
    def between(start: int, end: int) -> Minute: ...
    @staticmethod
    def every(interval: int, *, start: Oint = None) -> Minute: ...

class Hour:
    def __init__(self, minute: int | list[int]) -> None: ...
    @staticmethod
    def between(start: int, end: int) -> Hour: ...
    @staticmethod
    def every(interval: int, *, start: Oint = None) -> Hour: ...

class Day:
    def __init__(self, minute: int | list[int]) -> None: ...
    @staticmethod
    def between(start: int, end: int) -> Day: ...
    @staticmethod
    def every(interval: int, *, start: Oint = None) -> Day: ...

class Month:
    def __init__(self, minute: int | list[int]) -> None: ...
    @staticmethod
    def between(start: int, end: int) -> Month: ...
    @staticmethod
    def every(interval: int, *, start: Oint = None) -> Month: ...

class DayOfWeek:
    def __init__(self, minute: int | list[int]) -> None: ...
    @staticmethod
    def between(start: int, end: int) -> DayOfWeek: ...
    @staticmethod
    def every(interval: int, *, start: Oint = None) -> DayOfWeek: ...

class Cron:
    def __init__(
        self,
        *,
        minute: Minute | None = None,
        hour: Hour | None = None,
        day: Day | None = None,
        month: Month | None = None,
        day_of_week: DayOfWeek | None = None,
    ) -> None: ...

class ScheduleEvent:
    def __init__(self, *, crons: list[Cron] | None = None) -> None: ...

class WatchEvent:
    def __init__(self, *, started: bool = False) -> None: ...

class WorkflowInput:
    @staticmethod
    def boolean(
        *, description: Ostr = None, default: Oboollike = None, required: Obool = None
    ) -> WorkflowInput: ...
    @staticmethod
    def number(
        *, description: Ostr = None, default: Ointlike = None, required: Obool = None
    ) -> WorkflowInput: ...
    @staticmethod
    def string(
        *, description: Ostr = None, default: Ostrlike = None, required: Obool = None
    ) -> WorkflowInput: ...

class WorkflowOutput:
    def __init__(self, value: StringLike, *, description: Ostr = None) -> None: ...

class WorkflowSecret:
    def __init__(self, *, description: Ostr = None, required: Obool = None) -> None: ...

class WorkflowCallEvent:
    def __init__(
        self,
        *,
        inputs: Mapping[str, WorkflowInput] | None = None,
        outputs: Mapping[str, WorkflowOutput] | None = None,
        secrets: Mapping[str, WorkflowSecret] | None = None,
    ) -> None: ...

class WorkflowDispatchInput:
    @staticmethod
    def boolean(
        *, description: Ostr = None, default: Obool = None, required: Obool = None
    ) -> WorkflowDispatchInput: ...
    @staticmethod
    def choice(
        options: list[str],
        *,
        description: Ostr = None,
        default: Ostr = None,
        required: Obool = None,
    ) -> WorkflowDispatchInput: ...
    @staticmethod
    def number(
        *, description: Ostr = None, default: Oint = None, required: Obool = None
    ) -> WorkflowDispatchInput: ...
    @staticmethod
    def environment(
        *, description: Ostr = None, required: Obool = None
    ) -> WorkflowDispatchInput: ...
    @staticmethod
    def string(
        *, description: Ostr = None, default: Ostr = None, required: Obool = None
    ) -> WorkflowDispatchInput: ...

class WorkflowDispatchEvent:
    def __init__(
        self, *, inputs: Mapping[str, WorkflowDispatchInput] | None = None
    ) -> None: ...

class WorkflowRunEvent:
    def __init__(
        self,
        *,
        workflows: list[str] | None = None,
        completed: bool = False,
        requested: bool = False,
        in_progress: bool = False,
        branches: list[str] | None = None,
        branches_ignore: list[str] | None = None,
    ) -> None: ...

class Events:
    def __init__(
        self,
        branch_protection_rule: BranchProtectionRuleEvent | None = None,
        check_run: CheckRunEvent | None = None,
        check_suite: CheckSuiteEvent | None = None,
        create: bool = False,
        delete: bool = False,
        deployment: bool = False,
        deployment_status: bool = False,
        discussion: DiscussionEvent | None = None,
        discussion_comment: DiscussionCommentEvent | None = None,
        fork: bool = False,
        gollum: bool = False,
        image_version: ImageVersionEvent | None = None,
        issue_comment: IssueCommentEvent | None = None,
        issues: IssuesEvent | None = None,
        label: LabelEvent | None = None,
        merge_group: MergeGroupEvent | None = None,
        milestone: MilestoneEvent | None = None,
        page_build: bool = False,
        public: bool = False,
        pull_request: PullRequestEvent | None = None,
        pull_request_review: PullRequestReviewEvent | None = None,
        pull_request_review_comment: PullRequestReviewCommentEvent | None = None,
        pull_request_target: PullRequestEvent | None = None,
        push: PushEvent | None = None,
        registry_package: RegistryPackageEvent | None = None,
        release: ReleaseEvent | None = None,
        schedule: ScheduleEvent | None = None,
        status: bool = False,
        watch: WatchEvent | None = None,
        workflow_call: WorkflowCallEvent | None = None,
        workflow_dispatch: WorkflowDispatchEvent | None = None,
        workflow_run: WorkflowRunEvent | None = None,
    ) -> None: ...

class Workflow:
    def __init__(
        self,
        *,
        jobs: Mapping[str, Job],
        on: Events,
        name: Ostr = None,
        run_name: Ostrlike = None,
        permissions: Permissions | None = None,
        env: Mapping[str, StringLike] | None = None,
        defaults: Defaults | None = None,
        concurrency: Concurrency | None = None,
    ) -> None: ...
    def is_valid(self) -> bool: ...
    def validate(self) -> None: ...
    def dump(
        self, path: Path | str, *, overwrite: bool = True, validate: bool = True
    ) -> None: ...

__all__ = [
    'BranchProtectionRuleEvent',
    'CheckRunEvent',
    'CheckSuiteEvent',
    'Concurrency',
    'Container',
    'Credentials',
    'Cron',
    'Day',
    'DayOfWeek',
    'Defaults',
    'DiscussionCommentEvent',
    'DiscussionEvent',
    'Environment',
    'Events',
    'Hour',
    'ImageVersionEvent',
    'IssueCommentEvent',
    'IssuesEvent',
    'Job',
    'JobSecrets',
    'LabelEvent',
    'Matrix',
    'MergeGroupEvent',
    'MilestoneEvent',
    'Minute',
    'Month',
    'Permissions',
    'PullRequestEvent',
    'PullRequestReviewCommentEvent',
    'PullRequestReviewEvent',
    'PushEvent',
    'RegistryPackageEvent',
    'ReleaseEvent',
    'RepositoryDispatchEvent',
    'RunDefaults',
    'RunsOn',
    'RunsOnSpec',
    'ScheduleEvent',
    'ActionStep',
    'Step',
    'Strategy',
    'WatchEvent',
    'Workflow',
    'WorkflowCallEvent',
    'WorkflowDispatchEvent',
    'WorkflowDispatchInput',
    'WorkflowInput',
    'WorkflowOutput',
    'WorkflowRunEvent',
    'WorkflowSecret',
    'action',
    'script',
]
