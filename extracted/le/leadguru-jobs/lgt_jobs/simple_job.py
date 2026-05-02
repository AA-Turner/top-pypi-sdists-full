from abc import ABC
from typing import Optional
from pydantic import BaseModel
from lgt_jobs.basejobs import BaseBackgroundJobData, BaseBackgroundJob


class SimpleTestJobData(BaseBackgroundJobData, BaseModel):
    id: int
    name: Optional[str] = None


class SimpleTestJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return SimpleTestJobData

    def exec(self, data: SimpleTestJobData):
        print(f'id={data.id};name={data.name}')
        return f"id={data.id};name={data.name}"
