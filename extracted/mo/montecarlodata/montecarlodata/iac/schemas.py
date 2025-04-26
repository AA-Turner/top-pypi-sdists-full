import json
from dataclasses import dataclass
from typing import List, Optional

from dataclasses_json import DataClassJsonMixin, LetterCase
from dataclasses_json.cfg import config
from marshmallow import fields

from montecarlodata.iac.utils import field_spec
from montecarlodata.settings import (
    DEFAULT_EXCLUDE_PATTERNS,
    DEFAULT_INCLUDE_PATTERNS,
    DEFAULT_MONTECARLO_MONITOR_CONFIG_VERSION,
)


@dataclass
class ProjectConfig(DataClassJsonMixin):
    version: Optional[int] = field_spec(
        fields.Int(required=False),
        default_factory=lambda: DEFAULT_MONTECARLO_MONITOR_CONFIG_VERSION,
    )
    default_resource: Optional[str] = field_spec(fields.Str(required=False))
    include_file_patterns: Optional[List[str]] = field_spec(
        fields.List(fields.Str(required=True)),
        default_factory=lambda: DEFAULT_INCLUDE_PATTERNS,
    )
    exclude_file_patterns: Optional[List[str]] = field_spec(
        fields.List(fields.Str(required=True)), default_factory=list
    )
    namespace: Optional[str] = None

    def __post_init__(self):
        self.exclude_file_patterns = list(
            set((self.exclude_file_patterns or []) + DEFAULT_EXCLUDE_PATTERNS)
        )


@dataclass
class ResourceModification(DataClassJsonMixin):
    dataclass_json_config = config(letter_case=LetterCase.CAMEL)["dataclasses_json"]

    type: str
    description: str
    is_significant_change: bool = False
    diff_string: Optional[str] = None
    resource_type: Optional[str] = None
    resource_index: Optional[int] = None


@dataclass
class ConfigTemplateUpdateAsyncResponse(DataClassJsonMixin):
    dataclass_json_config = config(letter_case=LetterCase.CAMEL)["dataclasses_json"]

    update_uuid: Optional[str] = None
    errors_as_json: Optional[str] = None
    warnings_as_json: Optional[str] = None

    def __post_init__(self):
        self.errors = json.loads(self.errors_as_json) if self.errors_as_json else {}


@dataclass
class ConfigTemplateUpdateState(DataClassJsonMixin):
    dataclass_json_config = config(letter_case=LetterCase.CAMEL)["dataclasses_json"]

    state: str
    resource_modifications: Optional[List[ResourceModification]] = None
    errors_as_json: Optional[str] = None
    warnings_as_json: Optional[str] = None
    changes_applied: bool = False

    def __post_init__(self):
        self.resource_modifications = self.resource_modifications or []
        self.errors = json.loads(self.errors_as_json) if self.errors_as_json else {}

    @property
    def warnings(self):
        return json.loads(self.warnings_as_json) if self.warnings_as_json else {}


@dataclass
class ConfigTemplateDeleteResponse(DataClassJsonMixin):
    dataclass_json_config = config(letter_case=LetterCase.CAMEL)["dataclasses_json"]

    num_deleted: int
    changes_applied: bool = False
