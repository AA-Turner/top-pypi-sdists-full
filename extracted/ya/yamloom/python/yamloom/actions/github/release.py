from __future__ import annotations
from yamloom import Permissions
from yamloom.actions.utils import check_string

from typing import TYPE_CHECKING

from ...expressions import context, StringExpression
from ..._yamloom import ActionStep
from ..types import (
    Obool,
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

__all__ = [
    'Release',
    'ReleasePlease',
]


class Release(ActionStep):
    """Create a GitHub release.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    body
        Note-worthy description of changes in the release.
    body_path
        Path to load note-worthy description of changes in the release from.
    draft
        Creates a draft release.
    prerelease
        Identify the release as a prerelease.
    preserve_order
        Preserve the order of the artifacts when uploading.
    files
        Newline-delimited list of path globs for asset files to upload.
    working_directory
        Base directory to resolve ``files`` globs against (defaults to job
        working-directory).
    overwrite_files
        Overwrite existing files with the same name.
    release_name
        Gives the release a custom name. Defaults to tag name.
    tag_name
        Gives a tag name. Defaults to ``github.ref_name``.
    fail_on_unmatched_files
        Fail if any of the ``files`` globs match nothing.
    repository
        Repository to make releases against, in ``<owner>/<repo>`` format.
    target_commitish
        Commitish value that determines where the Git tag is created from. Can be
        any branch or commit SHA.
    token
        Authorized secret GitHub Personal Access Token.
    discussion_category_name
        If specified, a discussion of the specified category is created and linked
        to the release. The value must be a category that already exists in the
        repository.
    generate_release_notes
        Whether to automatically generate the name and body for this release. If
        name is specified, the specified name will be used; otherwise, a name will
        be automatically generated. If body is specified, the body will be
        pre-pended to the automatically generated notes.
    append_body
        Append to existing body instead of overwriting it.
    make_latest
        Specifies whether this release should be set as the latest release for the
        repository. Can be ``true``, ``false``, or ``legacy``. Uses GitHub API
        defaults if not provided.
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
        The generated release step.

    See Also
    --------
    GitHub repository: https://github.com/softprops/action-gh-release
    """

    recommended_permissions = Permissions(contents='write')

    @classmethod
    def url(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.url

    @classmethod
    def release_id(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.id

    @classmethod
    def upload_url(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.upload_url

    @classmethod
    def assets(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.assets

    def __new__(
        cls,
        *,
        name: Ostrlike = None,
        version: str = 'v2',
        body: Ostr = None,
        body_path: Ostr = None,
        draft: Obool = None,
        prerelease: Obool = None,
        preserve_order: Obool = None,
        files: Ostr = None,
        working_directory: Ostr = None,
        overwrite_files: Obool = None,
        release_name: Ostr = None,
        tag_name: Ostr = None,
        fail_on_unmatched_files: Obool = None,
        repository: Ostr = None,
        target_commitish: Ostr = None,
        token: Ostr = None,
        discussion_category_name: Ostr = None,
        generate_release_notes: Obool = None,
        append_body: Obool = None,
        make_latest: StringOrBoolLike | None = None,
        args: Ostrlike = None,
        entrypoint: Ostrlike = None,
        condition: Oboolstr = None,
        id: Ostr = None,  # noqa: A002
        env: Mapping[str, StringLike] | None = None,
        continue_on_error: Oboollike = None,
        timeout_minutes: Ointlike = None,
        skip_recommended_permissions: bool = False,
    ) -> Release:
        options: dict[str, object] = {
            'body': body,
            'body_path': body_path,
            'draft': draft,
            'prerelease': prerelease,
            'preserve_order': preserve_order,
            'files': files,
            'working_directory': working_directory,
            'overwrite_files': overwrite_files,
            'name': release_name,
            'tag_name': tag_name,
            'fail_on_unmatched_files': fail_on_unmatched_files,
            'repository': repository,
            'target_commitish': target_commitish,
            'token': token,
            'discussion_category_name': discussion_category_name,
            'generate_release_notes': generate_release_notes,
            'append_body': append_body,
            'make_latest': make_latest,
        }
        options = {key: value for key, value in options.items() if value is not None}

        if name is None:
            repository_str = check_string(options.get('repository'))
            if repository_str:
                name = f'Release {repository_str}'
            else:
                name = 'Create Release'

        recommended_permissions = (
            cls.recommended_permissions
            if discussion_category_name is None
            else Permissions(contents='write', discussions='write')
        )

        return super().__new__(
            cls,
            name,
            'softprops/action-gh-release',
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
            recommended_permissions=recommended_permissions if token is None else None,
        )


class ReleasePlease(ActionStep):
    """Automated releases based on conventional commits.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    token
        GitHub token for creating and grooming release PRs.
    release_type
        Defines the release strategy to use for the repository.
    path
        Create a release from a path other than the repository's root.
    target_branch
        Branch to open pull release PR against (detected by default).
    config_file
        Path to the release-please config in the repository.
    manifest_file
        Path to the release-please versions manifest.
    repo_url
        GitHub repository name in the form of ``<owner>/<repo>``.
    github_api_url
        Override the GitHub API URL.
    github_graphql_url
        Override the GitHub GraphQL URL.
    fork
        If true, send the PR from a fork. This requires the token to be a user
        that can create forks (not the default ``GITHUB_TOKEN``).
    include_component_in_tag
        If true, add prefix to tags and branches, allowing multiple libraries
        to be released from the same repository.
    proxy_server
        Configure a proxy server in the form of ``<host>:<port>``.
    skip_github_release
        If true, do not attempt to create releases.
    skip_github_pull_request
        If true, do not attempt to create release pull requests.
    skip_labeling
        If true, do not attempt to label the PR.
    changelog_host
        The proto://host where commits live.
    versioning_strategy
        The versioning strategy to use.
    release_as
        The version to release as.
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
        The generated release-please step.

    Notes
    -----
    Root component outputs are only present when the release-please action is
    configured for the root package. This means the ``path`` input is either
    omitted or set to ``"."``. If a non-root component path is used, access the
    path-prefixed outputs via the ``*_for`` methods instead.

    See Also
    --------
    GitHub repository: https://github.com/googleapis/release-please-action

    Notes
    -----
    You may have to adjust repository settings to allow GitHub actions to create pull requests: ``Settings > Actions > General``
    """

    recommended_permissions = Permissions(
        contents='write', issues='write', pull_requests='write'
    )

    @classmethod
    def releases_created(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.releases_created

    @classmethod
    def paths_released(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.paths_released

    @classmethod
    def prs_created(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.prs_created

    @classmethod
    def pr(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.pr

    @classmethod
    def prs(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.prs

    @classmethod
    def release_created(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.release_created

    @classmethod
    def upload_url(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.upload_url

    @classmethod
    def html_url(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.html_url

    @classmethod
    def tag_name(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.tag_name

    @classmethod
    def version(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.version

    @classmethod
    def major(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.major

    @classmethod
    def minor(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.minor

    @classmethod
    def patch(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.patch

    @classmethod
    def sha(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.sha

    @classmethod
    def body(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.body

    @classmethod
    def release_created_for(cls, id: str, path: str) -> StringExpression:
        """Return ``<path>--release_created`` output for a component path."""
        return context.steps[id].outputs[f'{path}--release_created']

    @classmethod
    def upload_url_for(cls, id: str, path: str) -> StringExpression:
        """Return ``<path>--upload_url`` output for a component path."""
        return context.steps[id].outputs[f'{path}--upload_url']

    @classmethod
    def html_url_for(cls, id: str, path: str) -> StringExpression:
        """Return ``<path>--html_url`` output for a component path."""
        return context.steps[id].outputs[f'{path}--html_url']

    @classmethod
    def tag_name_for(cls, id: str, path: str) -> StringExpression:
        """Return ``<path>--tag_name`` output for a component path."""
        return context.steps[id].outputs[f'{path}--tag_name']

    @classmethod
    def version_for(cls, id: str, path: str) -> StringExpression:
        """Return ``<path>--version`` output for a component path."""
        return context.steps[id].outputs[f'{path}--version']

    @classmethod
    def major_for(cls, id: str, path: str) -> StringExpression:
        """Return ``<path>--major`` output for a component path."""
        return context.steps[id].outputs[f'{path}--major']

    @classmethod
    def minor_for(cls, id: str, path: str) -> StringExpression:
        """Return ``<path>--minor`` output for a component path."""
        return context.steps[id].outputs[f'{path}--minor']

    @classmethod
    def patch_for(cls, id: str, path: str) -> StringExpression:
        """Return ``<path>--patch`` output for a component path."""
        return context.steps[id].outputs[f'{path}--patch']

    @classmethod
    def sha_for(cls, id: str, path: str) -> StringExpression:
        """Return ``<path>--sha`` output for a component path."""
        return context.steps[id].outputs[f'{path}--sha']

    @classmethod
    def body_for(cls, id: str, path: str) -> StringExpression:
        """Return ``<path>--body`` output for a component path."""
        return context.steps[id].outputs[f'{path}--body']

    def __new__(
        cls,
        *,
        name: Ostrlike = None,
        version: str = 'v4',
        token: Ostrlike = None,
        release_type: Ostrlike = None,
        path: Ostrlike = None,
        target_branch: Ostrlike = None,
        config_file: Ostrlike = None,
        manifest_file: Ostrlike = None,
        repo_url: Ostrlike = None,
        github_api_url: Ostrlike = None,
        github_graphql_url: Ostrlike = None,
        fork: Oboollike = None,
        include_component_in_tag: Oboollike = None,
        proxy_server: Ostrlike = None,
        skip_github_release: Oboollike = None,
        skip_github_pull_request: Oboollike = None,
        skip_labeling: Oboollike = None,
        changelog_host: Ostrlike = None,
        versioning_strategy: Ostrlike = None,
        release_as: Ostrlike = None,
        args: Ostrlike = None,
        entrypoint: Ostrlike = None,
        condition: Oboolstr = None,
        id: Ostr = None,  # noqa: A002
        env: Mapping[str, StringLike] | None = None,
        continue_on_error: Oboollike = None,
        timeout_minutes: Ointlike = None,
        skip_recommended_permissions: bool = False,
    ) -> ReleasePlease:
        options: dict[str, object] = {
            'token': token,
            'release-type': release_type,
            'path': path,
            'target-branch': target_branch,
            'config-file': config_file,
            'manifest-file': manifest_file,
            'repo-url': repo_url,
            'github-api-url': github_api_url,
            'github-graphql-url': github_graphql_url,
            'fork': fork,
            'include-component-in-tag': include_component_in_tag,
            'proxy-server': proxy_server,
            'skip-github-release': skip_github_release,
            'skip-github-pull-request': skip_github_pull_request,
            'skip-labeling': skip_labeling,
            'changelog-host': changelog_host,
            'versioning-strategy': versioning_strategy,
            'release-as': release_as,
        }
        options = {key: value for key, value in options.items() if value is not None}

        if name is None:
            name = 'Run release-please'

        return super().__new__(
            cls,
            name,
            'googleapis/release-please-action',
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
