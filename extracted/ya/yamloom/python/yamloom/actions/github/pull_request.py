from __future__ import annotations
from yamloom import Permissions
from yamloom.actions.utils import validate_choice

from typing import TYPE_CHECKING

from ...expressions import context, StringExpression, BooleanExpression
from ..._yamloom import ActionStep
from ..types import (
    Oboollike,
    Oboolstr,
    Ointlike,
    Ostr,
    Ostrlike,
    StringOrBoolLike,
    StringLike,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

__all__ = ['CreatePullRequest']


class CreatePullRequest(ActionStep):
    """Creates a pull request for changes to your repository in the actions workspace.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    token
        The token that the action will use to create and update the pull request.
    branch_token
        The token that the action will use to create and update the branch.
        Defaults to the value of ``token``.
    path
        Relative path under ``$GITHUB_WORKSPACE`` to the repository. Defaults to
        ``$GITHUB_WORKSPACE``.
    add_paths
        A comma or newline-separated list of file paths to commit. Paths should
        follow git's pathspec syntax. Defaults to adding all new and modified
        files.
    commit_message
        The message to use when committing changes.
    committer
        The committer name and email address in the format
        ``Display Name <email@address.com>``. Defaults to the GitHub Actions bot
        user.
    author
        The author name and email address in the format
        ``Display Name <email@address.com>``. Defaults to the user who triggered
        the workflow run.
    signoff
        Add ``Signed-off-by`` line by the committer at the end of the commit log
        message.
    branch
        The pull request branch name.
    delete_branch
        Delete ``branch`` if it doesn't have an active pull request associated
        with it.
    branch_suffix
        The branch suffix type when using the alternative branching strategy.
        Valid values are ``random``, ``timestamp`` and ``short-commit-hash``.
    base
        The pull request base branch. Defaults to the branch checked out in the
        workflow.
    push_to_fork
        A fork of the checked-out parent repository to which the pull request
        branch will be pushed (e.g. ``owner/repo-fork``). The pull request will be
        created to merge the fork's branch into the parent's base.
    sign_commits
        Sign commits as ``github-actions[bot]`` when using ``GITHUB_TOKEN``, or
        your own bot when using GitHub App tokens.
    title
        The title of the pull request.
    body
        The body of the pull request.
    body_path
        The path to a file containing the pull request body. Takes precedence
        over ``body``.
    labels
        A comma or newline separated list of labels.
    assignees
        A comma or newline separated list of assignees (GitHub usernames).
    reviewers
        A comma or newline separated list of reviewers (GitHub usernames) to
        request a review from.
    team_reviewers
        A comma or newline separated list of GitHub teams to request a review
        from. A ``repo`` scoped Personal Access Token (PAT) or equivalent GitHub
        App permissions may be required.
    milestone
        The number of the milestone to associate the pull request with.
    draft
        Create a draft pull request. Valid values are ``true`` (only on create),
        ``always-true`` (on create and update), and ``false``.
    maintainer_can_modify
        Indicates whether maintainers can modify the pull request.
    args
        The inputs for a Docker container which are passed to the container's entrypoint.
        This is a subkey of the ``with`` key of the generated step.
    entrypoint
        Overrides the Docker ENTRYPOINT in the action's Dockerfile or sets one if it was not
        specified. Accepts a single string defining the executable to run (note that this is
        different from Docker's ENTRYPOINT instruction which has both a shell and exec form).
        This is a subkey of the ``with`` key of the generated step.
    condition
        A boolean expression which must be met for the step to run. Note that this represents
        the ``if`` key in the actual YAML file.
    id
        A unique identifier for the step which can be referenced in expressions.
    env
        Used to specify environment variables for the step.
    continue_on_error
        Prevents the job from failing if this step fails.
    timeout_minutes
        The maximum number of minutes to let the step run before GitHub automatically
        cancels it (defaults to 360 if not specified).

    Returns
    -------
    Step
        The generated create pull request step.

    See Also
    --------
    GitHub repository: https://github.com/peter-evans/create-pull-request

    Notes
    -----
    This action requires you to explicitly allow GitHub Actions to create pull requests. This setting can be found in the repository's settings under ``Actions > General > Workflow permissions``.
    """

    recommended_permissions = Permissions(contents='write', pull_requests='write')

    @classmethod
    def pull_request_number(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['pull-request-number']

    @classmethod
    def pull_request_url(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['pull-request-url']

    @classmethod
    def pull_request_operation(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['pull-request-operation']

    @classmethod
    def pull_request_head_sha(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['pull-request-head-sha']

    @classmethod
    def pull_request_branch(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['pull-request-branch']

    @classmethod
    def pull_request_commits_verified(cls, id: str) -> BooleanExpression:
        return context.steps[id].outputs['pull-request-commits-verified'].as_bool()

    def __new__(
        cls,
        *,
        name: Ostrlike = None,
        version: str = 'v8',
        token: Ostrlike = None,
        branch_token: Ostrlike = None,
        path: Ostrlike = None,
        add_paths: Ostrlike = None,
        commit_message: Ostrlike = None,
        committer: Ostrlike = None,
        author: Ostrlike = None,
        signoff: Oboollike = None,
        branch: Ostrlike = None,
        delete_branch: Oboollike = None,
        branch_suffix: Ostrlike = None,
        base: Ostrlike = None,
        push_to_fork: Ostrlike = None,
        sign_commits: Oboollike = None,
        title: Ostrlike = None,
        body: Ostrlike = None,
        body_path: Ostrlike = None,
        labels: Ostrlike = None,
        assignees: Ostrlike = None,
        reviewers: Ostrlike = None,
        team_reviewers: Ostrlike = None,
        milestone: Ointlike = None,
        draft: StringOrBoolLike | None = None,
        maintainer_can_modify: Oboollike = None,
        args: Ostrlike = None,
        entrypoint: Ostrlike = None,
        condition: Oboolstr = None,
        id: Ostr = None,  # noqa: A002
        env: Mapping[str, StringLike] | None = None,
        continue_on_error: Oboollike = None,
        timeout_minutes: Ointlike = None,
        skip_recommended_permissions: bool = False,
    ) -> CreatePullRequest:
        options: dict[str, object] = {
            'token': token,
            'branch-token': branch_token,
            'path': path,
            'add-paths': add_paths,
            'commit-message': commit_message,
            'committer': committer,
            'author': author,
            'signoff': signoff,
            'branch': branch,
            'delete-branch': delete_branch,
            'branch-suffix': validate_choice(
                'branch_suffix',
                branch_suffix,
                ['random', 'timestamp', 'short-commit-hash'],
            ),
            'base': base,
            'push-to-fork': push_to_fork,
            'sign-commits': sign_commits,
            'title': title,
            'body': body,
            'body-path': body_path,
            'labels': labels,
            'assignees': assignees,
            'reviewers': reviewers,
            'team-reviewers': team_reviewers,
            'milestone': milestone,
            'draft': draft,
            'maintainer-can-modify': maintainer_can_modify,
        }
        options = {key: value for key, value in options.items() if value is not None}

        if name is None:
            name = 'Create Pull Request'

        return super().__new__(
            cls,
            name,
            'peter-evans/create-pull-request',
            ref=version,
            with_opts=options or None,
            args=args,
            entrypoint=entrypoint,
            condition=condition,
            id=id,
            env=env,
            continue_on_error=continue_on_error,
            timeout_minutes=timeout_minutes,
            skip_recommended_permissions=skip_recommended_permissions,
            recommended_permissions=cls.recommended_permissions
            if token is None
            else None,
        )
