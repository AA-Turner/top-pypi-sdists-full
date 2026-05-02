from abc import ABC
import datetime
from typing import Optional, List
from pydantic import BaseModel, conlist
from pymongo import MongoClient
import logging as log
from lgt_jobs.basejobs import BaseBackgroundJob, BaseBackgroundJobData
from lgt_jobs.env import mongo_connection_string

"""
Track analytics
"""


class TrackAnalyticsJobData(BaseBackgroundJobData, BaseModel):
    data: str
    name: str
    event: str
    extra_ids: List[str] = []
    attributes: conlist(Optional[str])
    created_at: datetime.datetime


class TrackAnalyticsJob(BaseBackgroundJob, ABC):
    @property
    def job_data_type(self) -> type:
        return TrackAnalyticsJobData

    def exec(self, data: TrackAnalyticsJobData):
        with MongoClient(mongo_connection_string) as client:
            analytics_id = client.lgt_admin[data.event].insert_one(data.model_dump()).inserted_id
            log.info(f'[TrackAnalyticsJob]: Entry with id {analytics_id} has been recorded into {data.event}')
