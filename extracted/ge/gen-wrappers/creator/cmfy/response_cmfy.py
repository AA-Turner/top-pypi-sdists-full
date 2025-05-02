from typing import Dict, Any
from creator.base.base_response import BaseResponse, ResponseData, ResponseDataType


class ResponseCmfy(BaseResponse):
    @classmethod
    def parse_response(cls, response: Dict[str, Any]):
        data = response.get('images', [])
        if not data:
            return cls.error("No images found in response")
        response_data = ResponseData(data=data, data_type=ResponseDataType.IMAGE, total_count=len(data))
        return cls.success(response_data)
