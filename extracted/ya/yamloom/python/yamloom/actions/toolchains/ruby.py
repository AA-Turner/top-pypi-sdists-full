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

__all__ = ['SetupRuby']


class SetupRuby(ActionStep):
    """Set up Ruby, JRuby, or TruffleRuby and add it to the PATH.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    ruby_version
        Engine and version to use. If unset, reads from `.ruby-version`,
        `.tool-versions`, or `mise.toml`. Use ``default`` to let the action pick.
    rubygems
        RubyGems version to use: ``default``, ``latest``, or a version number.
    bundler
        Bundler version to install: ``Gemfile.lock`` (default), ``default``,
        ``latest``, ``none``, or a version number.
    bundler_cache
        Run ``bundle install`` and cache the result automatically.
    working_directory
        Working directory for resolving Ruby version files and `Gemfile.lock`.
    cache_version
        String added to the bundler cache key to force cache invalidation.
    self_hosted
        Treat the runner as self-hosted to avoid prebuilt binaries.
    windows_toolchain
        Override Windows toolchain setup. Allowed values: ``default`` or ``none``.
    token
        GitHub token used to authenticate downloads when required.
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
        The generated setup-ruby step.

    See Also
    --------
    GitHub repository: https://github.com/ruby/setup-ruby
    """

    recommended_permissions = None

    @classmethod
    def ruby_prefix(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['ruby-prefix']

    def __new__(
        cls,
        *,
        name: Ostrlike = None,
        version: str = 'v1',
        ruby_version: Ostrlike = None,
        rubygems: Ostrlike = None,
        bundler: Ostrlike = None,
        bundler_cache: Oboollike = None,
        working_directory: Ostrlike = None,
        cache_version: Ostrlike = None,
        self_hosted: Oboollike = None,
        windows_toolchain: Ostrlike = None,
        token: Ostrlike = None,
        args: Ostrlike = None,
        entrypoint: Ostrlike = None,
        condition: Oboolstr = None,
        id: Ostr = None,  # noqa: A002
        env: Mapping[str, StringLike] | None = None,
        continue_on_error: Oboollike = None,
        timeout_minutes: Ointlike = None,
        skip_recommended_permissions: bool = False,
    ) -> SetupRuby:
        options: dict[str, object] = {
            'ruby-version': ruby_version,
            'rubygems': rubygems,
            'bundler': bundler,
            'bundler-cache': bundler_cache,
            'working-directory': working_directory,
            'cache-version': cache_version,
            'self-hosted': self_hosted,
            'windows-toolchain': validate_choice(
                'windows-toolchain', windows_toolchain, ['default', 'none']
            ),
            'token': token,
        }
        options = {key: value for key, value in options.items() if value is not None}

        if name is None:
            name = 'Setup Ruby'

        return super().__new__(
            cls,
            name,
            'ruby/setup-ruby',
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
