from typing import Dict, Any
from creator.base.base_response import BaseResponse, ResponseData, ResponseDataType


class ResponseAuto(BaseResponse):
    @classmethod
    def parse_response(cls, response: Dict[str, Any], job_id: str = None):
        data = response.get('images', [])
        if not data:
            print(f"No images found in response: {response}")
            return cls.error("No images found in response")
        print("Images found in response")
        response_data = ResponseData(data=data, data_type=ResponseDataType.IMAGE, total_count=len(data))
        return cls.success(response_data, job_id=job_id)
