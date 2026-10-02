from typing import List, Dict, Tuple, Optional, Any, Union
from dataclasses import dataclass
import os,sys
import fire
from vmodal.errors import FeatureDisabled


class SqlResource:
    def __init__(self, http):
        self.http = http

    async def query(self, **kw):
        raise FeatureDisabled("sql query endpoint is disabled on server")


if __name__ == "__main__":
    fire.Fire()
