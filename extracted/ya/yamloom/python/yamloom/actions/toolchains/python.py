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

__all__ = ['SetupPython', 'SetupUV']


class SetupPython(ActionStep):
    """Set up a specific version of Python and add it to the PATH.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    python_version
        Version range or exact version of Python or PyPy to use.
    python_version_file
        File containing the Python version to use.
    cache
        Package manager for caching in the default directory. Supported values:
        ``pip``, ``pipenv``, ``poetry``.
    architecture
        The target architecture of the Python or PyPy interpreter.
    check_latest
        Check for the latest available version that satisfies the version spec.
    token
        Token used to authenticate when fetching Python distributions.
    cache_dependency_path
        Path to dependency files. Supports wildcards or a list of file names.
    update_environment
        Set this option to update environment variables.
    allow_prereleases
        Allow prerelease versions to satisfy version range.
    freethreaded
        Use the freethreaded version of Python.
    pip_versions
        The version of pip to install with Python.
    pip_install
        Packages to install with pip after setting up Python.
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
        The generated setup-python step.

    See Also
    --------
    GitHub repository: https://github.com/actions/setup-python
    """

    recommended_permissions = Permissions(contents='read')

    @classmethod
    def python_version(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['python-version']

    @classmethod
    def cache_hit(cls, id: str) -> BooleanExpression:
        return context.steps[id].outputs['cache-hit'].as_bool()

    @classmethod
    def python_path(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['python-version']

    def __new__(
        cls,
        *,
        name: Ostrlike = None,
        version: str = 'v6',
        python_version: StringLike | None = None,
        python_version_file: Ostrlike = None,
        check_latest: Oboollike = None,
        architecture: Ostrlike = None,
        update_environment: Oboollike = None,
        token: Ostrlike = None,
        cache: Ostrlike = None,
        cache_dependency_path: Ostrlike = None,
        allow_prereleases: Oboollike = None,
        freethreaded: Oboollike = None,
        pip_version: Ostrlike = None,
        pip_install: Ostrlike = None,
        args: Ostrlike = None,
        entrypoint: Ostrlike = None,
        condition: Oboolstr = None,
        id: Ostr = None,  # noqa: A002
        env: Mapping[str, StringLike] | None = None,
        continue_on_error: Oboollike = None,
        timeout_minutes: Ointlike = None,
        skip_recommended_permissions: bool = False,
    ) -> SetupPython:
        options: dict[str, object] = {
            'python-version': python_version,
            'python-version-file': python_version_file,
            'check-latest': check_latest,
            'architecture': architecture,
            'token': token,
            'cache': cache,
            'cache-dependency-path': cache_dependency_path,
            'update-environment': update_environment,
            'allow-prereleases': allow_prereleases,
            'freethreaded': freethreaded,
            'pip-version': pip_version,
            'pip-install': pip_install,
        }
        options = {key: value for key, value in options.items() if value is not None}

        if name is None:
            name = 'Setup Python'

        return super().__new__(
            cls,
            name,
            'actions/setup-python',
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


class SetupUV(ActionStep):
    """Set up a specific version of uv.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    uv_version
        The version of uv to install.
    uv_version_file
        Path to a file containing the version of uv to install.
    python_version
        The version of Python to set UV_PYTHON to.
    activate_environment
        Use uv venv to activate a venv ready to be used by later steps.
    working_directory
        The directory to execute all commands in and look for files.
    checksum
        The checksum of the uv version to install.
    github_token
        Used to increase the rate limit when retrieving versions and downloading uv.
    enable_cache
        Enable uploading of the uv cache. Accepts ``true``, ``false``, or ``auto``.
    cache_dependency_glob
        Glob pattern list to control the cache.
    restore_cache
        Whether to restore the cache if found.
    save_cache
        Whether to save the cache after the run.
    cache_suffix
        Suffix for the cache key.
    cache_local_path
        Local path to store the cache.
    prune_cache
        Prune cache before saving.
    cache_python
        Upload managed Python installations to the GitHub Actions cache.
    ignore_nothing_to_cache
        Ignore when nothing is found to cache.
    ignore_empty_workdir
        Ignore when the working directory is empty.
    tool_dir
        Custom path to set UV_TOOL_DIR to.
    tool_bin_dir
        Custom path to set UV_TOOL_BIN_DIR to.
    manifest_file
        URL to the manifest file containing available versions and download URLs.
    add_problem_matchers
        Add problem matchers.
    resolution_strategy
        Resolution strategy when resolving version ranges (``highest`` or
        ``lowest``).
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
        The generated setup-uv step.

    See Also
    --------
    GitHub repository: https://github.com/astral-sh/setup-uv
    """

    recommended_permissions = None

    @classmethod
    def uv_version(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['uv-version']

    @classmethod
    def uv_path(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['uv-path']

    @classmethod
    def uvx_path(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['uvx-path']

    @classmethod
    def cache_hit(cls, id: str) -> BooleanExpression:
        return context.steps[id].outputs['cache-hit'].as_bool()

    @classmethod
    def cache_key(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['cache-key']

    @classmethod
    def venv(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['venv']

    @classmethod
    def python_version(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['python-version']

    @classmethod
    def python_cache_hit(cls, id: str) -> BooleanExpression:
        return context.steps[id].outputs['python-cache-hit'].as_bool()

    def __new__(
        cls,
        *,
        name: Ostrlike = None,
        version: str = 'v7',
        uv_version: Ostrlike = None,
        uv_version_file: Ostrlike = None,
        resolution_strategy: Ostrlike = None,
        python_version: Ostrlike = None,
        activate_environment: Oboollike = None,
        working_directory: Ostrlike = None,
        checksum: Ostrlike = None,
        github_token: Ostrlike = None,
        enable_cache: StringOrBoolLike | None = None,
        cache_dependency_glob: list[StringLike] | None = None,
        restore_cache: Oboollike = None,
        save_cache: Oboollike = None,
        cache_suffix: Ostrlike = None,
        cache_local_path: Ostrlike = None,
        prune_cache: Oboollike = None,
        cache_python: Oboollike = None,
        ignore_nothing_to_cache: Oboollike = None,
        ignore_empty_workdir: Oboollike = None,
        tool_dir: Ostrlike = None,
        tool_bin_dir: Ostrlike = None,
        manifest_file: Ostrlike = None,
        add_problem_matchers: Oboollike = None,
        args: Ostrlike = None,
        entrypoint: Ostrlike = None,
        condition: Oboolstr = None,
        id: Ostr = None,  # noqa: A002
        env: Mapping[str, StringLike] | None = None,
        continue_on_error: Oboollike = None,
        timeout_minutes: Ointlike = None,
        skip_recommended_permissions: bool = False,
    ) -> SetupUV:
        options: dict[str, object] = {
            'version': uv_version,
            'version-file': uv_version_file,
            'resolution-strategy': validate_choice(
                'resolution_strategy', resolution_strategy, ['highest', 'lowest']
            ),
            'python-version': python_version,
            'activate-environment': activate_environment,
            'working-directory': working_directory,
            'checksum': checksum,
            'github-token': github_token,
            'enable-cache': enable_cache,
            'cache-dependency-glob': '\n'.join(str(s) for s in cache_dependency_glob)
            if cache_dependency_glob is not None
            else None,
            'restore-cache': restore_cache,
            'save-cache': save_cache,
            'cache-suffix': cache_suffix,
            'cache-local-path': cache_local_path,
            'prune-cache': prune_cache,
            'cache-python': cache_python,
            'ignore-nothing-to-cache': ignore_nothing_to_cache,
            'ignore-empty-workdir': ignore_empty_workdir,
            'tool-dir': tool_dir,
            'tool-bin-dir': tool_bin_dir,
            'manifest-file': manifest_file,
            'add-problem-matchers': add_problem_matchers,
        }
        if enable_cache is not None:
            if isinstance(enable_cache, str):
                if enable_cache.lower() != 'auto':
                    msg = "'enable_cache' must be 'auto', true or false"
                    raise ValueError(msg)
                options['enable-cache'] = 'auto'
            elif isinstance(enable_cache, bool):
                options['enable-cache'] = enable_cache
            else:
                raise TypeError('enable_cache must be a bool or a string')

        options = {key: value for key, value in options.items() if value is not None}

        if name is None:
            name = 'Setup uv'

        return super().__new__(
            cls,
            name,
            'astral-sh/setup-uv',
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
