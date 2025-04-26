from typing import Union

from ..extensions import UnknownType
from ..models.manifest_boolean_scalar_config import ManifestBooleanScalarConfig
from ..models.manifest_date_scalar_config import ManifestDateScalarConfig
from ..models.manifest_datetime_scalar_config import ManifestDatetimeScalarConfig
from ..models.manifest_float_scalar_config import ManifestFloatScalarConfig
from ..models.manifest_integer_scalar_config import ManifestIntegerScalarConfig
from ..models.manifest_json_scalar_config import ManifestJsonScalarConfig
from ..models.manifest_secure_text_scalar_config import ManifestSecureTextScalarConfig
from ..models.manifest_text_scalar_config import ManifestTextScalarConfig

ManifestScalarConfig = Union[
    ManifestTextScalarConfig,
    ManifestFloatScalarConfig,
    ManifestIntegerScalarConfig,
    ManifestBooleanScalarConfig,
    ManifestDateScalarConfig,
    ManifestDatetimeScalarConfig,
    ManifestSecureTextScalarConfig,
    ManifestJsonScalarConfig,
    UnknownType,
]
