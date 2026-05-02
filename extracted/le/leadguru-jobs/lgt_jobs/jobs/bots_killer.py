from abc import ABC
from pydantic import BaseModel
from lgt_jobs.basejobs import BaseBackgroundJob, BaseBackgroundJobData
from lgt_jobs.services.k8_manager import K8Manager

"""
Kill bots
"""


class BotsKillerData(BaseBackgroundJobData, BaseModel):
    environment: str


class BotsKillerJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return BotsKillerData

    def exec(self, data: BotsKillerData):
        K8Manager().delete_bots(f'leadguru-{data.environment}')
