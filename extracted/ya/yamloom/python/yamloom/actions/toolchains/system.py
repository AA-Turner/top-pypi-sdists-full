from __future__ import annotations
from yamloom.actions.utils import validate_choice, check_string

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

__all__ = ['SetupMPI']


class SetupMPI(ActionStep):
    """Set up a specific MPI implementation.

    Parameters
    ----------
    name
        The name of the step to display on GitHub.
    version
        The branch, ref, or SHA of the action's repository to use.
    mpi
        MPI implementation name.
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
        The generated setup-mpi step.

    See Also
    --------
    GitHub repository: https://github.com/mpi4py/setup-mpi
    """

    recommended_permissions = None

    @classmethod
    def mpi(cls, id: str) -> StringExpression:
        return context.steps[id].outputs['mpi']

    def __new__(
        cls,
        *,
        name: Ostrlike = None,
        version: str = 'v1',
        mpi: Ostrlike = None,
        args: Ostrlike = None,
        entrypoint: Ostrlike = None,
        condition: Oboolstr = None,
        id: Ostr = None,  # noqa: A002
        env: Mapping[str, StringLike] | None = None,
        continue_on_error: Oboollike = None,
        timeout_minutes: Ointlike = None,
        skip_recommended_permissions: bool = False,
    ) -> SetupMPI:
        options: dict[str, object] = {
            'mpi': validate_choice(
                'mpi', mpi, ['mpich', 'openmpi', 'intelmpi', 'msmpi']
            ),
        }

        options = {key: value for key, value in options.items() if value is not None}

        if name is None:
            mpi_str = check_string(options.get('mpi'))
            if mpi_str:
                name = f'Setup {mpi_str}'
            else:
                name = 'Setup MPI'

        return super().__new__(
            cls,
            name,
            'mpi-action/setup-mpi',
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
