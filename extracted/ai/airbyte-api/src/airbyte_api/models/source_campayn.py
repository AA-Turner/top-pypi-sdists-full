"""Code generated by Speakeasy (https://speakeasy.com). DO NOT EDIT."""

from __future__ import annotations
import dataclasses
from airbyte_api import utils
from dataclasses_json import Undefined, dataclass_json
from enum import Enum
from typing import Final


class Campayn(str, Enum):
    CAMPAYN = 'campayn'


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclasses.dataclass
class SourceCampayn:
    api_key: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('api_key') }})
    r"""API key to use. Find it in your Campayn account settings. Keep it secure as it grants access to your Campayn data."""
    sub_domain: str = dataclasses.field(metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('sub_domain') }})
    SOURCE_TYPE: Final[Campayn] = dataclasses.field(default=Campayn.CAMPAYN, metadata={'dataclasses_json': { 'letter_case': utils.get_field_name('sourceType') }})
    

