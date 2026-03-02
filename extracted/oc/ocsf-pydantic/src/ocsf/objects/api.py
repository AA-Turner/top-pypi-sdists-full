from pydantic import BaseModel

from .service import Service
from .group import Group
from .response import ResponseElements
from .request import RequestElements


class API(BaseModel):
    """
    The API, or Application Programming Interface, object represents  information
    pertaining to an API request and response.
    """

    operation: str

    # Recommended:
    request: RequestElements | None = None # Details pertaining to the API request.
    response: ResponseElements | None = None # Details pertaining to the API response.

    # Optional:
    group: Group | None = None # The information pertaining to the API group.
    service: Service | None = None # The information pertaining to the API service.
    version: str | None = None # The version of the API service.
