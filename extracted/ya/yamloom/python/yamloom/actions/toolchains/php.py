from __future__ import annotations
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

__all__ = ['SetupPhp']


class SetupPhp(ActionStep):
    """Set up PHP.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    php_version
        Setup PHP version.
    php_version_file
        Setup PHP version from a file.
    extensions
        Setup PHP extensions.
    ini_file
        Set base ini file.
    ini_values
        Add values to php.ini.
    coverage
        Setup code coverage driver.
    tools
        Setup popular tools globally.
    github_token
        GitHub token to use for authentication.
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
        The generated setup-php step.

    See Also
    --------
    GitHub repository: https://github.com/shivammathur/setup-php
    """

    recommended_permissions = None

    @classmethod
    def php_version(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['php-version']

    def __new__(
        cls,
        *,
        name: Ostrlike = None,
        version: str = 'v2',
        php_version: Ostrlike = None,
        php_version_file: Ostrlike = None,
        extensions: Ostrlike = None,
        coverage: Ostrlike = None,
        ini_file: Ostrlike = None,
        ini_values: Ostrlike = None,
        tools: Ostrlike = None,
        github_token: Ostrlike = None,
        args: Ostrlike = None,
        entrypoint: Ostrlike = None,
        condition: Oboolstr = None,
        id: Ostr = None,  # noqa: A002
        env: Mapping[str, StringLike] | None = None,
        continue_on_error: Oboollike = None,
        timeout_minutes: Ointlike = None,
        skip_recommended_permissions: bool = False,
    ) -> SetupPhp:
        options: dict[str, object] = {
            'php-version': php_version,
            'php-version-file': php_version_file,
            'extensions': extensions,
            'ini-file': validate_choice(
                'ini_file', ini_file, ['production', 'development', 'none']
            ),
            'ini-values': ini_values,
            'coverage': validate_choice(
                'coverage', coverage, ['xdebug', 'pcov', 'none']
            ),
            'tools': tools,
            'github-token': github_token,
        }
        options = {key: value for key, value in options.items() if value is not None}

        if name is None:
            name = 'Setup PHP'

        return super().__new__(
            cls,
            name,
            'shivammathur/setup-php',
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
