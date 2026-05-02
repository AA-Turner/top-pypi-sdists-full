from abc import abstractmethod, ABC
from pydantic import BaseModel


class InvalidJobTypeException(Exception):
    pass


class BaseBackgroundJobData(BaseModel):
    """
    Background job data
    """


class BaseBackgroundJob(ABC):
    def __init__(self):
        super().__init__()

    @staticmethod
    def dumps(job_type: type, data: dict) -> dict:
        """
        @:param job_type type of the job, inherited from BaseBackgroundJob
        @:param job data
        """
        obj = {
            "job_type": job_type.__name__,
            "data": data
        }
        return obj

    @property
    @abstractmethod
    def job_data_type(self) -> type:
        """
       gets data type for this given job
       """

    @abstractmethod
    def exec(self, data: BaseBackgroundJobData):
        """
       @param data: job data
       """

    def run(self, data: dict):
        """
        @param data: job data
        """
        data_type = self.job_data_type
        if not issubclass(data_type, BaseBackgroundJobData):
            raise InvalidJobTypeException(f'{data_type} is not a subsclass of BaseBackgroundJobData')

        job_data: BaseBackgroundJobData = data_type(**data)
        return self.exec(job_data)
