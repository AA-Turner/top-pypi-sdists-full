from typing import Any, Dict, Optional
from typing_extensions import TypedDict

from dlthub.cache.config import CacheConfig
from dlthub._runner.typing import PipelineRunConfig
from dlthub.destinations.dataset import DatasetConfig


# TODO: generate project typedicts from existing SPECs (dataclasses) and extend them if needed
# some of the configurations are dynamic and generated from signatures (ie. sources, destinations)
# for those we won't be able to generate typedicts fully but maybe we will be able to
# generate JSON SCHEMA
# and use this for validation. We can also extend our validator with custom

# TODO: all sources are derived from BaseConfiguration with `with_args`
# corresponding to SourceFactory protocol
#   source specific params are taken from source signature and not known in advance
#   we have an option to put those in a separate property ie
# github:
#  args: {}
#  type
SourceConfig = Dict[str, Any]
# TODO: all destinations are derived from DestinationClientConfiguration,
# we can use UNION to represent known
# destinations or put the dynamic part into args.
DestinationConfig = Dict[str, Any]


class ProfileProjectSettingsConfig(TypedDict, total=False):
    """Part of the project config that can be changed in the profile"""

    allow_undefined_entities: Optional[bool]
    data_dir: Optional[str]
    """Pipeline working dirs, other writable folders, local destination files (by default)"""
    local_dir: Optional[str]
    """Destination local files, by default it is within run_dir/_local"""


class ProjectSettingsConfig(ProfileProjectSettingsConfig, total=False):
    """Project settings in Config"""

    name: Optional[str]
    """Project will assume this name, note that project module is still the parent folder"""
    default_profile: Optional[str]
    project_dir: Optional[str]
    """Project will assume this folder, this allows to keep dlt.yml in a separate location"""

    # TODO: below split to internal class, those should not be validated!

    current_profile: Optional[str]
    """not to be set in config"""


# TODO: generate and extend from PipelineConfiguration
class PipelineConfig(TypedDict, total=False):
    source: Optional[str]
    destination: str
    dataset_name: Optional[str]
    progress: Optional[str]  # in fact this is enum
    run_config: Optional[PipelineRunConfig]


# TODO: we have several SPECs to add here: RUNTIME, NORMALIZE, LOAD, SCHEMA. all of them
#   must be derived from relevant SPECs.
class ProjectConfigBase(TypedDict, total=False):
    sources: Optional[Dict[str, Optional[SourceConfig]]]
    destinations: Optional[Dict[str, Optional[DestinationConfig]]]
    pipelines: Optional[Dict[str, PipelineConfig]]
    datasets: Optional[Dict[str, DatasetConfig]]
    caches: Optional[Dict[str, CacheConfig]]
    runtime: Optional[Dict[str, Any]]
    transformations: Optional[Any]


class ProfileConfig(ProjectConfigBase, total=False):
    project: Optional[ProfileProjectSettingsConfig]


class ProjectConfig(ProjectConfigBase, total=False):
    profiles: Optional[Dict[str, Optional[ProfileConfig]]]
    project: Optional[ProjectSettingsConfig]
