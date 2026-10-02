from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import fire
from vmodal.errors import FeatureDisabled


class GDriveResource:
    def __init__(self, http):
        self.http = http

    async def private_auth_url(self, **kw):
        raise FeatureDisabled("private google drive auth endpoint is disabled on server")

    async def private_download(self, **kw):
        raise FeatureDisabled("private google drive download endpoint is disabled on server")


if __name__ == "__main__":
    fire.Fire()
