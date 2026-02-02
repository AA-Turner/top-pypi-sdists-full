from __future__ import annotations
from yamloom import Permissions

from typing import TYPE_CHECKING

from ...expressions import context, StringExpression, BooleanExpression
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

__all__ = ['SetupGo']


class SetupGo(ActionStep):
    """Set up a Go environment and add it to the PATH.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    go_version
        The Go version to download (if necessary) and use. Supports semver spec
        and ranges.
    go_version_file
        Path to the go.mod, go.work, .go-version, or .tool-versions file.
    check_latest
        Check for the latest available version that satisfies the version spec.
    token
        Used to pull Go distributions from go-versions.
    cache
        Enable caching for Go.
    cache_dependency_path
        Path to a dependency file (e.g., ``go.sum``).
    architecture
        Target architecture for Go to use.
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
        The generated setup-go step.

    See Also
    --------
    GitHub repository: https://github.com/actions/setup-go
    """

    recommended_permissions = Permissions(contents='read')

    @classmethod
    def go_version(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['go-version']

    @classmethod
    def cache_hit(cls, id: str) -> BooleanExpression:
        return context.steps[id].outputs['cache-hit'].as_bool()

    def __new__(
        cls,
        *,
        name: Ostrlike = None,
        version: str = 'v6',
        go_version: Ostrlike = None,
        go_version_file: Ostrlike = None,
        check_latest: Oboollike = None,
        architecture: Ostrlike = None,
        token: Ostrlike = None,
        cache: Oboollike = None,
        cache_dependency_path: Ostrlike = None,
        args: Ostrlike = None,
        entrypoint: Ostrlike = None,
        condition: Oboolstr = None,
        id: Ostr = None,  # noqa: A002
        env: Mapping[str, StringLike] | None = None,
        continue_on_error: Oboollike = None,
        timeout_minutes: Ointlike = None,
        skip_recommended_permissions: bool = False,
    ) -> SetupGo:
        options: dict[str, object] = {
            'go-version': go_version,
            'go-version-file': go_version_file,
            'check-latest': check_latest,
            'architecture': architecture,
            'token': token,
            'cache': cache,
            'cache-dependency-path': cache_dependency_path,
        }
        options = {key: value for key, value in options.items() if value is not None}

        if name is None:
            name = 'Setup Go'

        return super().__new__(
            cls,
            name,
            'actions/setup-go',
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
