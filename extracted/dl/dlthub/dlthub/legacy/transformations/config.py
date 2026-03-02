from typing import Optional, Union

from typing_extensions import TypedDict

import dlt
from dlt.common.validation import validate_dict

from dlthub.cache.cache import Cache


class TransformationConfig(TypedDict, total=False):
    name: str
    engine: str
    package_name: str
    location: Optional[str]
    cache: Union[str, Cache]


def set_defaults_and_validate(config: TransformationConfig) -> TransformationConfig:
    config.setdefault("engine", "dbt")
    engine = config["engine"]
    config.setdefault("package_name", engine + "_" + config["name"])
    config.setdefault("location", dlt.current.run_context().get_run_entity("transformations"))

    validate_dict(TransformationConfig, config, ".")
    return config
