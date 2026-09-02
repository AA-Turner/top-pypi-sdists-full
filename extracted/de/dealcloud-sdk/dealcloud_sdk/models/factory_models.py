from typing import Union

from pydantic import BaseModel


class DealCloudFactoryArgs(BaseModel):
    site_url: str
    client_id: Union[str, int]
    client_secret: str
