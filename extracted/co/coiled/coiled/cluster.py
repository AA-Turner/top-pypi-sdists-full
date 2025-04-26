import enum
import logging
import time

import dask.config
from dask.distributed import Client
from dask.utils import parse_timedelta
from distributed.deploy.adaptive import Adaptive

from .utils import COILED_LOGGER_NAME

logger = logging.getLogger(COILED_LOGGER_NAME)


@enum.unique
class CredentialsPreferred(enum.Enum):
    LOCAL = "local"
    # USER = 'user'
    ACCOUNT = "account"  # doesn't work, should be fixed or deprecated/removed someday
    NONE = None


class CoiledAdaptive(Adaptive):
    def __init__(self, cluster, **kwargs):
        super().__init__(cluster, **kwargs)

        update_interval = dask.config.get("coiled.adaptive.update-plan-interval", None)
        self._update_plan_interval = parse_timedelta(update_interval) if update_interval else None  # in seconds
        self._last_plan_update = time.monotonic()

        target_duration = kwargs.get("target_duration")
        if target_duration:
            with Client(self.cluster, name="non-user-to-set-adaptive-target-duration") as client:
                client.run_on_scheduler(
                    lambda: dask.config.set({"distributed.adaptive.target-duration": target_duration})
                )

    def config_as_string(self):
        return (
            f"Config is maximum: {self.maximum}, minimum: {self.minimum}, wait_count: {self.wait_count}, "
            f"interval: {self.interval}, target_duration: {self.target_duration}."
        )

    async def scale_up(self, n):
        logger.info(f"Adaptive scaling up to {n} workers.")
        if self.cluster:
            if hasattr(self.cluster, "_submit_cluster_event"):
                await self.cluster._submit_cluster_event(
                    "adaptive",
                    f"scale up to {n} workers",
                    extra_data={"n": n},
                )
            await self.cluster.scale_up(
                n,
                reason=f"Adaptive scaling up to {n} workers. "
                f"Previous intended size was {len(self.cluster._plan)}. "
                f"{self.config_as_string()}",
            )

    async def scale_down(self, workers):
        if not workers:
            return
        logger.info(f"Adaptive is removing {len(workers)} workers.")
        if self.cluster:
            if hasattr(self.cluster, "_submit_cluster_event"):
                await self.cluster._submit_cluster_event(
                    "adaptive",
                    f"removing {len(workers)} workers",
                    extra_data={"workers": list(workers)},
                )

            await self.cluster.scale_down(
                workers,
                reason=f"Adaptive removing {len(workers)} workers. "
                f"Previous intended size was {len(self.cluster._plan)}. "
                f"{self.config_as_string()}",
                force_stop=False,
            )

    async def workers_to_close(self, target: int):
        if self.cluster and hasattr(self.cluster, "workers_to_close"):
            # use our logic for determining which workers to close
            # e.g., if there's an extra worker on scheduler VM, don't close that
            return await self.cluster.workers_to_close(target=target)

        # just in case, fall back to base class method
        return await super().workers_to_close(target=target)

    async def recommendations(self, target: int) -> dict:
        if self.cluster and hasattr(self.cluster, "_set_plan_requested"):
            # update current view of workers if running worker on scheduler
            # since we initially include fake worker in the set but this messes things up if we
            # don't remove later when actual worker has appeared.
            if "extra-worker-on-scheduler" in self.cluster.plan:
                await self.cluster._set_plan_requested()
                self._last_plan_update = time.monotonic()

            # update current view of workers at regular interval, so if prior adaptive requests failed to get desired
            # workers (e.g., there were availability limits which caused workers to go to `error` state), adaptive
            # will be aware that those workers failed and can request new workers.
            # the interval will effectively control how often adaptive will retry to get workers.
            elif self._update_plan_interval and time.monotonic() > self._last_plan_update + self._update_plan_interval:
                if hasattr(self.cluster, "_submit_cluster_event"):
                    await self.cluster._submit_cluster_event(
                        "adaptive",
                        "updating plan based on current state of workers",
                        extra_data={
                            "update_interval": self._update_plan_interval,
                            "last_update": time.monotonic() - self._last_plan_update,
                        },
                    )
                await self.cluster._set_plan_requested()
                self._last_plan_update = time.monotonic()

        return await super().recommendations(target=target)
