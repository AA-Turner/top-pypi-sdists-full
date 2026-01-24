from typing import Optional, Type
from snakemake_interface_scheduler_plugins.base import SchedulerBase
from snakemake_interface_scheduler_plugins.settings import SchedulerSettingsBase
from snakemake_interface_scheduler_plugins.tests import TestSchedulerBase


class TestGreedyScheduler(TestSchedulerBase):
    __test__ = True

    def get_scheduler_cls(self) -> Type[SchedulerBase]:
        from snakemake.scheduling.greedy import Scheduler

        return Scheduler

    def get_scheduler_settings(self) -> Optional[SchedulerSettingsBase]:
        from snakemake.scheduling.greedy import SchedulerSettings

        return SchedulerSettings()
