from __future__ import annotations
from yamloom.actions.utils import validate_choice

from typing import TYPE_CHECKING

from ..._yamloom import ActionStep
from ..types import (
    Oboollike,
    Oboolstr,
    Ointlike,
    Ostr,
    Ostrlike,
    StringLike,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

__all__ = ['Codecov']


class Codecov(ActionStep):
    """Upload coverage reports to Codecov.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    base_sha
        The base SHA to select. Only used in the ``pr-base-picking`` run command.
    binary
        The file location of a pre-downloaded version of the CLI. If specified,
        integrity checking will be bypassed.
    codecov_yml_path
        The location of the codecov.yml file. This is currently only used for
        automated test selection.
    commit_parent
        SHA (with 40 chars) of what should be the parent of this commit.
    directory
        Folder to search for coverage files. Defaults to the current working
        directory.
    disable_file_fixes
        Disable file fixes to ignore common lines from coverage.
    disable_search
        Disable search for coverage files.
    disable_safe_directory
        Disable setting safe directory. Set to true to disable.
    disable_telem
        Disable sending telemetry data to Codecov. Set to true to disable.
    dry_run
        Do not upload files to Codecov.
    env_vars
        Environment variables to tag the upload with (e.g. ``PYTHON`` or
        ``OS,PYTHON``).
    exclude
        Comma-separated list of folders to exclude from search.
    fail_ci_if_error
        On error, exit with non-zero code.
    files
        Comma-separated list of explicit files to upload. These will be added to
        coverage files found for upload. Use ``disable_search`` to upload only
        the specified files.
    flags
        Comma-separated list of flags to upload to group coverage metrics.
    force
        Only used for the ``empty-upload`` run command.
    git_service
        Override the git_service (e.g. ``github_enterprise``).
    gcov_args
        Extra arguments to pass to gcov.
    gcov_executable
        gcov executable to run. Defaults to ``gcov``.
    gcov_ignore
        Paths to ignore during gcov gathering.
    gcov_include
        Paths to include during gcov gathering.
    handle_no_reports_found
        If no coverage reports are found, do not raise an exception.
    job_code
        Codecov job code.
    codecov_name
        Custom defined name of the upload. Visible in the Codecov UI.
    network_filter
        Filter files listed in the network section of the Codecov report. Only
        files whose path begin with the specified filter are included.
    network_prefix
        Prefix on files listed in the network section of the Codecov report.
    os
        Override the assumed OS. Options available at cli.codecov.io.
    override_branch
        Specify the branch to be displayed with this commit on Codecov.
    override_build
        Specify the build number manually.
    override_build_url
        The URL of the build where this is running.
    override_commit
        Commit SHA (with 40 chars).
    override_pr
        Specify the pull request number manually. Used to override pre-existing
        CI environment variables.
    plugins
        Comma-separated list of plugins to run. Specify ``noop`` to turn off all
        plugins.
    recurse_submodules
        Whether to enumerate files inside of submodules for path-fixing purposes.
    report_code
        The code of the report if using local upload.
    report_type
        The type of file to upload. Possible values are ``test_results`` and
        ``coverage``.
    root_dir
        Root folder from which to consider paths on the network section.
    run_command
        Choose which CLI command to run. Options are ``upload-coverage``,
        ``empty-upload``, ``pr-base-picking``, and ``send-notifications``.
    skip_validation
        Skip integrity checking of the CLI. This is not recommended.
    slug
        Required when using the org token. Set to the owner/repo slug used
        instead of the private repo token.
    swift_project
        Specify the swift project name. Useful for optimization.
    token
        Repository Codecov token. Used to authorize report uploads.
    url
        Set to the Codecov instance URL. Used by Dedicated Enterprise Cloud
        customers.
    use_legacy_upload_endpoint
        Use the legacy upload endpoint.
    use_oidc
        Use OIDC instead of token. This will ignore any token supplied.
    use_pypi
        Use the PyPI version of the CLI instead of from cli.codecov.io.
    verbose
        Enable verbose logging.
    codecov_version
        Which version of the Codecov CLI to use (defaults to ``latest``).
    working_directory
        Directory in which to execute codecov.sh.
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
        The generated codecov step.

    See Also
    --------
    GitHub repository: https://github.com/codecov/codecov-action
    """

    recommended_permissions = None

    def __new__(
        cls,
        *,
        name: Ostrlike = None,
        version: str = 'v5',
        base_sha: Ostrlike = None,
        binary: Ostrlike = None,
        codecov_yml_path: Ostrlike = None,
        commit_parent: Ostrlike = None,
        directory: Ostrlike = None,
        disable_file_fixes: Oboollike = None,
        disable_search: Oboollike = None,
        disable_safe_directory: Oboollike = None,
        disable_telem: Oboollike = None,
        dry_run: Oboollike = None,
        env_vars: Ostrlike = None,
        exclude: Ostrlike = None,
        fail_ci_if_error: Oboollike = None,
        files: Ostrlike = None,
        flags: Ostrlike = None,
        force: Oboollike = None,
        git_service: Ostrlike = None,
        gcov_args: Ostrlike = None,
        gcov_executable: Ostrlike = None,
        gcov_ignore: Ostrlike = None,
        gcov_include: Ostrlike = None,
        handle_no_reports_found: Oboollike = None,
        job_code: Ostrlike = None,
        codecov_name: Ostrlike = None,
        network_filter: Ostrlike = None,
        network_prefix: Ostrlike = None,
        os: Ostrlike = None,  #
        override_branch: Ostrlike = None,
        override_build: Ointlike = None,
        override_build_url: Ostrlike = None,
        override_commit: Ostrlike = None,
        override_pr: Ointlike = None,
        plugins: Ostrlike = None,
        recurse_submodules: Oboollike = None,
        report_code: Ostrlike = None,
        report_type: Ostrlike = None,
        root_dir: Ostrlike = None,
        run_command: Ostrlike = None,
        skip_validation: Oboollike = None,
        slug: Ostrlike = None,
        swift_project: Ostrlike = None,
        token: Ostrlike = None,
        url: Ostrlike = None,
        use_legacy_upload_endpoint: Oboollike = None,
        use_oidc: Oboollike = None,
        use_pypi: Oboollike = None,
        verbose: Oboollike = None,
        codecov_version: Ostrlike = None,
        working_directory: Ostrlike = None,
        args: Ostrlike = None,
        entrypoint: Ostrlike = None,
        condition: Oboolstr = None,
        id: Ostr = None,  # noqa: A002
        env: Mapping[str, StringLike] | None = None,
        continue_on_error: Oboollike = None,
        timeout_minutes: Ointlike = None,
        skip_recommended_permissions: bool = False,
    ) -> Codecov:
        options: dict[str, object] = {
            'base_sha': base_sha,
            'binary': binary,
            'codecov_yml_path': codecov_yml_path,
            'commit_parent': commit_parent,
            'directory': directory,
            'disable_file_fixes': disable_file_fixes,
            'disable_search': disable_search,
            'disable_safe_directory': disable_safe_directory,
            'disable_telem': disable_telem,
            'dry_run': dry_run,
            'env_vars': env_vars,
            'exclude': exclude,
            'fail_ci_if_error': fail_ci_if_error,
            'files': files,
            'flags': flags,
            'force': force,
            'git_service': git_service,
            'gcov_args': gcov_args,
            'gcov_executable': gcov_executable,
            'gcov_ignore': gcov_ignore,
            'gcov_include': gcov_include,
            'handle_no_reports_found': handle_no_reports_found,
            'job_code': job_code,
            'name': codecov_name,
            'network_filter': network_filter,
            'network_prefix': network_prefix,
            'os': validate_choice(
                'os',
                os,
                ['alpine', 'alpine-arm64', 'linux', 'linux-arm64', 'macos', 'windows'],
            ),
            'override_branch': override_branch,
            'override_build': override_build,
            'override_build_url': override_build_url,
            'override_commit': override_commit,
            'override_pr': override_pr,
            'plugins': plugins,
            'recurse_submodules': recurse_submodules,
            'report_code': report_code,
            'report_type': validate_choice(
                'report_type', report_type, ['test_results', 'coverage']
            ),
            'root_dir': root_dir,
            'run_command': validate_choice(
                'run_command',
                run_command,
                [
                    'upload-coverage',
                    'empty-upload',
                    'pr-base-picking',
                    'send-notifications',
                ],
            ),
            'skip_validation': skip_validation,
            'slug': slug,
            'swift_project': swift_project,
            'token': token,
            'url': url,
            'use_legacy_upload_endpoint': use_legacy_upload_endpoint,
            'use_oidc': use_oidc,
            'use_pypi': use_pypi,
            'verbose': verbose,
            'version': codecov_version,
            'working-directory': working_directory,
        }
        options = {key: value for key, value in options.items() if value is not None}

        if name is None:
            name = 'Upload coverage'

        return super().__new__(
            cls,
            name,
            'codecov/codecov-action',
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
            recommended_permissions=cls.recommended_permissions,
        )
