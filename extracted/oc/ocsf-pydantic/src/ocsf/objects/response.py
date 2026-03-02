from pydantic import BaseModel

from .container import Container

class ResponseElements(BaseModel):
    """
    The Response Elements object describes characteristics of an API response.
    """

    # Recommended:
    code: int | None = None
    error: str | None = None
    error_message: str | None = None
    message: str | None = None

    # Optional:
    containers: list[Container] | None = None
    data: dict | None = None # The additional data that is associated with the api response.
    flags: list[str] | None = None
