import base64
from enum import Enum
from typing import List, Optional, Any
from fastapi.responses import Response

from pydantic import BaseModel, Field

from creator.base.job_status import JobStatus


class ResponseDataType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    GIF = "gif"
    TEXT = "text"
    AUDIO = "audio"
    NONE = "none"


class ResponseData(BaseModel):
    data: List[Any] = Field(default_factory=list, description="The data to be returned.")
    data_type: ResponseDataType = Field(ResponseDataType.NONE, description="The type of data being returned.")
    total_count: int = 0


class BaseResponse(BaseModel):
    status: JobStatus = JobStatus.PENDING
    output: Optional[ResponseData] = None
    error_msg: Optional[str] = None
    job_id: Optional[str] = None

    # Override Pydantic's dict method to exclude methods
    def dict(self, **kwargs):
        return super().dict(
            **kwargs,
            exclude={
                "parse_response",
                "success",
                "error"
            }
        )

    @classmethod
    def parse_response(cls, response: dict, job_id: str = None):
        """Parse the response from the API."""
        return cls(**response, job_id=job_id)

    @classmethod
    def success(cls, data: ResponseData, job_id: str = None):
        """Return a successful response."""
        return cls(status=JobStatus.FINISHED, output=data, job_id=job_id)

    @classmethod
    def active(cls, job_id: str = None):
        return cls(status=JobStatus.READY, job_id=job_id)

    @classmethod
    def running(cls, job_id: str = None):
        """Return a pending response."""
        return cls(status=JobStatus.RUNNING, job_id=job_id)

    @classmethod
    def error(cls, error: str, job_id: str = None):
        """Return an error response."""
        return cls(status=JobStatus.FAILED, error_msg=error, job_id=job_id)

    def image_response(self, job_id: str = None):
        """Return a response containing images if output is image data."""
        if self.output and self.output.data_type == ResponseDataType.IMAGE:
            image_data_list = self.output.data
            if len(image_data_list) == 1:
                # If only one image, return a single image response
                image_data = base64.b64decode(image_data_list[0])
                return Response(content=image_data, media_type="image/png")
            else:
                # If multiple images, construct a multipart response
                boundary = "boundary_separator"
                content_type = f"multipart/mixed; boundary={boundary}"
                body_parts = []
                for image_data in image_data_list:
                    image_bytes = base64.b64decode(image_data)
                    image_part = (
                        f"\r\n--{boundary}\r\n"
                        f"Content-Type: image/png\r\n"
                        f"Content-Length: {len(image_bytes)}\r\n\r\n"
                    )
                    body_parts.append(image_part.encode("utf-8"))
                    body_parts.append(image_bytes)
                body = b"".join(body_parts) + f"\r\n--{boundary}--\r\n".encode("utf-8")
                return Response(content=body, media_type=content_type)
        else:
            return self
