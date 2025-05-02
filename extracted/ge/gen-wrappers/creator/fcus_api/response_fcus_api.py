from typing import Dict, Any
from dataclasses import dataclass
from creator.base.base_response import BaseResponse, ResponseData, ResponseDataType


@dataclass
class FcusJobResult:
    base64: str
    url: str
    seed: int
    finish_reason: str


@dataclass
class FcusResult:
    job_id: str
    job_type: str
    job_stage: str
    job_progress: int
    job_status: str
    job_step_preview: str
    job_result: FcusJobResult


class ResponseFcusApi(BaseResponse):
    @classmethod
    def parse_response(cls, response: Dict[str, Any]):
        try:
            job_data = FcusResult(**response)
            if job_data.job_result.base64:
                response_data = ResponseData(data=[job_data.job_result.base64], data_type=ResponseDataType.IMAGE,
                                             total_count=1)
            else:
                response_data = ResponseData(data=[job_data.job_id], data_type=ResponseDataType.TEXT, total_count=1)
            return cls.success(response_data)
        except Exception as e:
            return cls.error("Error parsing response: " + str(e))
