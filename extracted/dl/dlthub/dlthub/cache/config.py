from typing import Any, Dict, Optional, List, Union
from typing_extensions import TypedDict


from dlt.common.schema.typing import TWriteDisposition
from dlt.common.validation import validate_dict


class CacheBinding(TypedDict, total=False):
    # Dataset[Relation] remove generic from dataset
    dataset: Union[Any, str]
    tables: Optional[Dict[str, str]]


class CacheInputBinding(CacheBinding):
    pass


class CacheOutputBinding(CacheBinding):
    write_disposition: Optional[TWriteDisposition]
    loader_file_format: Optional[str]


class CacheConfig(TypedDict, total=False):
    name: Optional[str]
    type: Optional[str]
    location: Optional[str]
    pipeline_name: Optional[str]
    dataset_name: Optional[str]
    transformed_dataset_name: Optional[str]
    inputs: List[CacheInputBinding]
    outputs: List[CacheOutputBinding]


def set_defaults_and_validate(config: CacheConfig) -> CacheConfig:
    # set some defaults
    config.setdefault("type", "duckdb")
    config.setdefault("pipeline_name", config["name"] + "_cache")
    config.setdefault("dataset_name", config["name"] + "_cache_dataset")
    config.setdefault(
        "transformed_dataset_name",
        config["dataset_name"] + "_transformed",
    )

    # relative location goes to local_dir, absolute to absolute
    if "location" not in config:
        # place in local files dir
        config["location"] = ""

    validate_dict(CacheConfig, config, ".")

    return config
