from __future__ import annotations
from yamloom import Permissions
from yamloom.actions.utils import validate_choice

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

__all__ = ['SetupDotnet']


class SetupDotnet(ActionStep):
    """Set up a specific version of the .NET SDK and optional NuGet auth.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    dotnet_version
        Optional SDK version(s) to use. Examples: ``2.2.104``, ``3.1``, ``3.1.x``,
        ``3.x``, ``6.0.2xx``.
    dotnet_quality
        Optional quality of the build. Possible values are ``daily``, ``signed``,
        ``validated``, ``preview``, and ``ga``.
    global_json_file
        Optional global.json location, if your global.json isn't located in the
        root of the repo.
    source_url
        Optional package source for which to set up authentication.
    owner
        Optional owner for using packages from GitHub Package Registry
        organizations/users other than the current repository's owner. Only used
        if a GPR URL is also provided in ``source_url``.
    config_file
        Optional NuGet.config location, if your NuGet.config isn't located in the
        root of the repo.
    cache
        Enable caching of the NuGet global-packages folder.
    cache_dependency_path
        Path to a dependency file such as ``packages.lock.json``. Supports
        wildcards or a list of file names for caching multiple dependencies.
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
        The generated setup-dotnet step.

    See Also
    --------
    GitHub repository: https://github.com/actions/setup-dotnet
    """

    recommended_permissions = Permissions(contents='read')

    @classmethod
    def dotnet_version(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['dotnet-version']

    def __new__(
        cls,
        *,
        name: Ostrlike = None,
        version: str = 'v5',
        dotnet_version: Ostrlike = None,
        dotnet_quality: Ostrlike = None,
        global_json_file: Ostrlike = None,
        source_url: Ostrlike = None,
        owner: Ostrlike = None,
        config_file: Ostrlike = None,
        cache: Oboollike = None,
        cache_dependency_path: Ostrlike | list[StringLike] = None,
        args: Ostrlike = None,
        entrypoint: Ostrlike = None,
        condition: Oboolstr = None,
        id: Ostr = None,  # noqa: A002
        env: Mapping[str, StringLike] | None = None,
        continue_on_error: Oboollike = None,
        timeout_minutes: Ointlike = None,
        skip_recommended_permissions: bool = False,
    ) -> SetupDotnet:
        options: dict[str, object] = {
            'dotnet-version': dotnet_version,
            'dotnet-quality': validate_choice(
                'dotnet-quality',
                dotnet_quality,
                ['daily', 'signed', 'validated', 'preview', 'ga'],
            ),
            'global-json-file': global_json_file,
            'source-url': source_url,
            'owner': owner,
            'config-file': config_file,
            'cache': cache,
            'cache-dependency-path': cache_dependency_path,
        }
        options = {key: value for key, value in options.items() if value is not None}

        if name is None:
            name = 'Setup .NET'

        return super().__new__(
            cls,
            name,
            'actions/setup-dotnet',
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
