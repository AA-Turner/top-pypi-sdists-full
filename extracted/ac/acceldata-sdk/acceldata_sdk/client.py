from abc import abstractmethod

from acceldata_sdk.models.create_asset import CreateAsset
from acceldata_sdk.models.datasource import DataSource
from acceldata_sdk.models.pipeline import Pipeline
from acceldata_sdk.models.job import Job


class TorchClientInterFace:
    """
    Description: TorchClientInterface is the interface that contains different methods that are supported to
    communicate with catalog-server
    """

    @abstractmethod
    def create_pipeline(self, pipeline: Pipeline): raise NotImplementedError

    @abstractmethod
    def delete_pipeline(self, pipeline: Pipeline): raise NotImplementedError

    @abstractmethod
    def create_job(self, job: {}, pipelineId: int): raise NotImplementedError

    @abstractmethod
    def delete_job(self, job: Job = None): raise NotImplementedError

    @abstractmethod
    def create_pipeline_run(self, pipeline_run): raise NotImplementedError

    @abstractmethod
    def update_pipeline_run(self, pipeline_run_id: int, pipeline_run): raise NotImplementedError

    @abstractmethod
    def create_span(self, pipeline_run_id: int, span: dict): raise NotImplementedError

    @abstractmethod
    def create_span_event(self, span_event): raise NotImplementedError
