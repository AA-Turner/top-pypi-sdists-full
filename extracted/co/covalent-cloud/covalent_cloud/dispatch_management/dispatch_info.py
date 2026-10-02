# Copyright 2024 Agnostiq Inc.

from typing import List, Union

from pydantic import BaseModel


class DispatchInfo(BaseModel):
    tags: Union[List[str], None] = None
