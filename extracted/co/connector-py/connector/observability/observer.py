from collections.abc import Generator
from contextlib import contextmanager
from contextvars import ContextVar
from typing import TypedDict, cast

OBSERVATIONS: ContextVar["Observations"] = ContextVar("observations", default={})


class DagsterObservations(TypedDict):
    """Contains information about an upstream dagster op."""

    run_id: str


class Observations(TypedDict, total=False):
    """Execution attributes which may be observed during execution of an ICS task."""

    flows_v2_execution_id: str
    dagster: DagsterObservations


class Observer:
    """Observes various contextual information as tasks are performed. These observations are available for monitoring and alerting.

    WARNING: Observations should NOT be used for critical business functions. This data is used for observability purposes only, which
    is inherently able to perform without certain observations. Since the underlying mechanisms for storing this data is a `ContextVar`
    there is a risk of the data not being copied properly across thread/event loop boundaries with improper care. If you find yourself
    needing data for business functions, please pass that data down through method/function calls.
    """

    @classmethod
    @contextmanager
    def observe(cls, observations: Observations) -> Generator[None, None, None]:
        """Observed attributes will be available for the entirety of this context."""
        reset_token = OBSERVATIONS.set(
            cls.observed()
            | cast(
                Observations,
                {attr: observation for attr, observation in observations.items() if observation},
            )
        )
        try:
            yield
        finally:
            OBSERVATIONS.reset(reset_token)

    @classmethod
    def observed(cls) -> Observations:
        """Returns a mapping of observations, if any."""
        return OBSERVATIONS.get()
