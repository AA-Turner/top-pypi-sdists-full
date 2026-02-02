from __future__ import annotations
from yamloom import Permissions
from yamloom.actions.utils import check_string

from typing import TYPE_CHECKING

from ...expressions import context, StringExpression
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

__all__ = ['Checkout']


class Checkout(ActionStep):
    """Checkout a Git repository at a particular version.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    repository
        Repository name with owner. For example, ``actions/checkout``.
    ref
        The branch, tag or SHA to checkout. When checking out the repository that
        triggered a workflow, this defaults to the reference or SHA for that event.
        Otherwise, uses the default branch.
    token
        Personal access token (PAT) used to fetch the repository. The PAT is configured
        with the local git config, which enables your scripts to run authenticated git
        commands. The post-job step removes the PAT.

        We recommend using a service account with the least permissions necessary.
        Also when generating a new PAT, select the least scopes necessary.
    ssh_key
        SSH key used to fetch the repository. The SSH key is configured with the local
        git config, which enables your scripts to run authenticated git commands.
        The post-job step removes the SSH key.

        We recommend using a service account with the least permissions necessary.
    ssh_known_hosts
        Known hosts in addition to the user and global host key database. The public
        SSH keys for a host may be obtained using the utility ``ssh-keyscan``. For example,
        ``ssh-keyscan github.com``. The public key for github.com is always implicitly added.
    ssh_strict
        Whether to perform strict host key checking. When true, adds the options
        ``StrictHostKeyChecking=yes`` and ``CheckHostIP=no`` to the SSH command line.
        Use ``ssh_known_hosts`` to configure additional hosts.
    ssh_user
        The user to use when connecting to the remote SSH host. By default ``git`` is used.
    persist_credentials
        Whether to configure the token or SSH key with the local git config.
    path
        Relative path under ``$GITHUB_WORKSPACE`` to place the repository.
    clean
        Whether to execute ``git clean -ffdx && git reset --hard HEAD`` before fetching.
    filter
        Partially clone against a given filter. Overrides ``sparse_checkout`` if set.
    sparse_checkout
        Do a sparse checkout on given patterns. Each pattern should be separated with
        new lines.
    sparse_checkout_cone_mode
        Specifies whether to use cone-mode when doing a sparse checkout.
    fetch_depth
        Number of commits to fetch. ``0`` indicates all history for all branches and tags.
    fetch_tags
        Whether to fetch tags, even if ``fetch_depth > 0``.
    show_progress
        Whether to show progress status output when fetching.
    lfs
        Whether to download Git-LFS files.
    submodules
        Whether to checkout submodules: ``true`` to checkout submodules or ``recursive`` to
        recursively checkout submodules.

        When ``ssh_key`` is not provided, SSH URLs beginning with ``git@github.com:``
        are converted to HTTPS.
    get_safe_directory
        Add repository path as ``safe.directory`` for Git global config by running
        ``git config --global --add safe.directory <path>``.
    github_server_url
        The base URL for the GitHub instance that you are trying to clone from. Uses
        environment defaults to fetch from the same instance that the workflow is running
        from unless specified.
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
        The generated checkout step.

    See Also
    --------
    GitHub repository: https://github.com/actions/checkout
    """

    recommended_permissions = Permissions(contents='read')

    @classmethod
    def ref(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.ref

    @classmethod
    def commit(cls, id: str) -> StringExpression:
        return context.steps[id].outputs.commit

    def __new__(
        cls,
        *,
        name: Ostrlike = None,
        version: str = 'v6',
        repository: Ostrlike = None,
        ref: Ostrlike = None,
        token: Ostrlike = None,
        ssh_key: Ostrlike = None,
        ssh_known_hosts: Ostrlike = None,
        ssh_strict: Oboollike = None,
        ssh_user: Ostrlike = None,
        persist_credentials: Oboollike = None,
        path: Ostrlike = None,
        clean: Oboollike = None,
        filter: Ostrlike = None,  # noqa: A002
        sparse_checkout: Ostrlike = None,
        sparse_checkout_cone_mode: Oboollike = None,
        fetch_depth: Ointlike = None,
        fetch_tags: Oboollike = None,
        show_progress: Oboollike = None,
        lfs: Oboollike = None,
        submodules: Oboollike = None,
        get_safe_directory: Oboollike = None,
        github_server_url: Ostrlike = None,
        args: Ostrlike = None,
        entrypoint: Ostrlike = None,
        condition: Oboolstr = None,
        id: Ostr = None,  # noqa: A002
        env: Mapping[str, StringLike] | None = None,
        continue_on_error: Oboollike = None,
        timeout_minutes: Ointlike = None,
        skip_recommended_permissions: bool = False,
    ) -> Checkout:
        options: dict[str, object] = {
            'repository': repository,
            'ref': ref,
            'token': token,
            'ssh-key': ssh_key,
            'ssh-known-hosts': ssh_known_hosts,
            'ssh-strict': ssh_strict,
            'ssh-user': ssh_user,
            'persist-credentials': persist_credentials,
            'path': path,
            'clean': clean,
            'filter': filter,
            'sparse-checkout': sparse_checkout,
            'sparse-checkout-cone-mode': sparse_checkout_cone_mode,
            'fetch-depth': fetch_depth,
            'fetch-tags': fetch_tags,
            'show-progress': show_progress,
            'lfs': lfs,
            'submodules': submodules,
            'get-safe-directory': get_safe_directory,
            'github-server-url': github_server_url,
        }
        options = {key: value for key, value in options.items() if value is not None}

        if name is None:
            repository_str = check_string(options.get('repository'))
            if repository_str:
                name = f"Checkout '{repository_str}'"
            else:
                name = 'Checkout Repository'

        return super().__new__(
            cls,
            name,
            'actions/checkout',
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
