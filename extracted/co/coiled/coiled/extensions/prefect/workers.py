import os

try:
    from prefect.client.schemas import FlowRun  # type: ignore
    from prefect.infrastructure.container import Optional, anyio  # type: ignore
    from prefect.workers.process import (  # type: ignore
        ProcessJobConfiguration,
        ProcessWorker,
    )
except ImportError:
    raise ImportError("`prefect` must be installed to use Coiled prefect extension module.") from None


class CoiledJobConfiguration(ProcessJobConfiguration):
    """CoiledJobConfiguration"""

    # TODO: Implement relavant fields


class CoiledWorker(ProcessWorker):
    """
    A PrefectWorker specific to Coiled.

    Can run flows on Coiled infrastructure either in combination with CoiledTaskRunner to
    map flow tasks to dask tasks, as done with ``DaskTaskRunner`` but will handle mapping
    flows to the existing cluster this worker is running on.

    Alternatively, can be used without ``CoiledTaskRunner`` if you are wanting to run flows
    normally on a single VM.
    """

    type = "coiled-worker"
    _block_type_name = "Coiled Worker"
    _block_type_slug = "coiled-worker"

    async def run(
        self,
        flow_run: FlowRun,
        configuration: CoiledJobConfiguration,
        task_status: Optional[anyio.abc.TaskStatus] = None,
    ):
        # Propagate cluster name to flow environment, which CoiledTaskRunner will pick up
        # to use as its cluster (which is the same this Worker is running on)
        envvar = "COILED__CLUSTER_NAME"
        if envvar in os.environ:
            configuration.env[envvar] = os.environ[envvar]

        return await super().run(flow_run, configuration, task_status)
