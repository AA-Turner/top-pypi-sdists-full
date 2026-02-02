from __future__ import annotations
from yamloom import Permissions

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

__all__ = ['Maturin', 'PypiPublish']


class Maturin(ActionStep):
    """Install and run a custom maturin command.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    token
        Used to pull maturin distributions using GitHub API.
    command
        Maturin command to run. Defaults to ``build``.
    args
        Arguments to pass to the maturin subcommand.
    maturin_version
        The version of maturin to use.
    manylinux
        Control the manylinux platform tag on Linux.
    container
        Manylinux Docker container image name. Set to ``off`` to disable
        manylinux Docker build and build on the host instead.
    docker_options
        Additional Docker run options, for passing environment variables, etc.
    host_home_mount
        Host folder where the runner's home folder is mounted to. Used for
        building using Docker-in-Docker runners.
    target
        The ``--target`` option for Cargo.
    rust_toolchain
        Rust toolchain name.
    rustup_components
        Rustup components.
    working_directory
        Working directory to run maturin in.
    sccache
        Enable sccache for faster builds.
    before_script_linux
        Script to run before maturin command on Linux.
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
        The generated maturin step.

    See Also
    --------
    GitHub repository: https://github.com/PyO3/maturin-action
    """

    recommended_permissions = None

    def __new__(
        cls,
        *,
        name: Ostrlike = None,
        version: str = 'v1',
        token: Ostrlike = None,
        command: Ostrlike = None,
        args: Ostrlike = None,
        maturin_version: Ostrlike = None,
        manylinux: Ostrlike = None,
        container: Ostrlike = None,
        docker_options: Ostrlike = None,
        host_home_mount: Ostrlike = None,
        target: Ostrlike = None,
        rust_toolchain: Ostrlike = None,
        rustup_components: list[StringLike] | None = None,
        working_directory: Ostrlike = None,
        sccache: Oboollike = None,
        before_script_linux: Ostrlike = None,
        entrypoint: Ostrlike = None,
        condition: Oboolstr = None,
        id: Ostr = None,  # noqa: A002
        env: Mapping[str, StringLike] | None = None,
        continue_on_error: Oboollike = None,
        timeout_minutes: Ointlike = None,
        skip_recommended_permissions: bool = False,
    ) -> Maturin:
        options: dict[str, object] = {
            'token': token,
            'command': command,
            'maturin-version': maturin_version,
            'manylinux': manylinux,
            'target': target,
            'container': container,
            'docker-options': docker_options,
            'host-home-mount': host_home_mount,
            'rust-toolchain': rust_toolchain,
            'rustup-components': ','.join(str(s) for s in rustup_components)
            if rustup_components is not None
            else None,
            'working-directory': working_directory,
            'sccache': sccache,
            'before-script-linux': before_script_linux,
        }

        options = {key: value for key, value in options.items() if value is not None}

        if name is None:
            name = 'Maturin Action'

        return super().__new__(
            cls,
            name,
            'PyO3/maturin-action',
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


class PypiPublish(ActionStep):
    """Upload Python distribution packages to PyPI.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    user
        PyPI user. Defaults to ``__token__``.
    password
        Password for your PyPI user or an access token.
    repository_url
        The repository URL to use.
    packages_dir
        The target directory for distribution.
    verify_metadata
        Check metadata before uploading.
    skip_existing
        Do not fail if a Python package distribution exists in the target package
        index.
    verbose
        Show verbose output.
    print_hash
        Show hash values of files to be uploaded.
    attestations
        Enable support for PEP 740 attestations. Only works with PyPI and TestPyPI
        via Trusted Publishing.
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
        The generated PyPI publish step.

    See Also
    --------
    GitHub repository: https://github.com/pypa/gh-action-pypi-publish
    """

    recommended_permissions = Permissions(id_token='write')

    def __new__(
        cls,
        *,
        name: Ostrlike = None,
        version: str = 'release/v1',
        user: Ostrlike = None,
        password: Ostrlike = None,
        repository_url: Ostrlike = None,
        packages_dir: Ostrlike = None,
        verify_metadata: Oboollike = None,
        skip_existing: Oboollike = None,
        verbose: Oboollike = None,
        print_hash: Oboollike = None,
        attestations: Oboollike = None,
        args: Ostrlike = None,
        entrypoint: Ostrlike = None,
        condition: Oboolstr = None,
        id: Ostr = None,  # noqa: A002
        env: Mapping[str, StringLike] | None = None,
        continue_on_error: Oboollike = None,
        timeout_minutes: Ointlike = None,
        skip_recommended_permissions: bool = False,
    ) -> PypiPublish:
        options: dict[str, object] = {
            'user': user,
            'password': password,
            'repository-url': repository_url,
            'packages-dir': packages_dir,
            'verify-metadata': verify_metadata,
            'skip-existing': skip_existing,
            'verbose': verbose,
            'print-hash': print_hash,
            'attestations': attestations,
        }
        options = {key: value for key, value in options.items() if value is not None}

        if name is None:
            name = 'Publish to PyPI'

        return super().__new__(
            cls,
            name,
            'pypa/gh-action-pypi-publish',
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
