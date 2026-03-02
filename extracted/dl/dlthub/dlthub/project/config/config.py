import os
from typing import Any, ClassVar, Dict, Iterable, Mapping, Optional

import dlt
from dlt.common.configuration import NotResolved, configspec
from dlt.common.configuration.specs import RuntimeConfiguration, BaseConfiguration
from dlt.common.configuration.providers import CustomLoaderDocProvider
from dlt.common.typing import Annotated
from dlt.common.utils import exclude_keys

from dlthub.cache.config import CacheConfig
from dlthub.project.config.typing import (
    ProjectConfig,
    SourceConfig,
    DestinationConfig,
    PipelineConfig,
    DatasetConfig,
    ProfileConfig,
    ProjectSettingsConfig,
)


def exclude_keys_from_nested(data: Mapping[str, Any], keys: Iterable[str]) -> Dict[str, Any]:
    return {
        nested_key: {
            key: value if not isinstance(value, Mapping) else exclude_keys(value, keys)
            for key, value in nested_mapping.items()
        }
        for nested_key, nested_mapping in data.items()
        if isinstance(nested_mapping, Mapping)
    }


class Project:
    DEFAULT_PROVIDER_NAME: ClassVar[str] = "dlt.yml"

    def __init__(
        self,
        config: ProjectConfig,
        settings: ProjectSettingsConfig,
    ):
        self._config = config
        self._settings = settings

    @property
    def settings(self) -> ProjectSettingsConfig:
        return self._settings

    @property
    def config(self) -> ProjectConfig:
        return self._config

    @property
    def current_profile(self) -> str:
        return self._settings["current_profile"]

    @property
    def project_dir(self) -> str:
        return self._settings["project_dir"]

    @property
    def name(self) -> str:
        return self._settings.get("name") or os.path.basename(self.project_dir.rstrip(os.path.sep))

    @property
    def default_profile(self) -> str:
        return self._settings.get("default_profile")

    def provider(self, provider_name: Optional[str] = None) -> CustomLoaderDocProvider:
        provider_name = provider_name or self.DEFAULT_PROVIDER_NAME
        return CustomLoaderDocProvider(
            provider_name,
            lambda: self._to_provider_config_doc(),
            supports_secrets=True,
            locations=[self.project_dir],
        )

    def register(self, provider_name: Optional[str] = None) -> None:
        dlt.config.register_provider(self.provider(provider_name))

    def _to_provider_config_doc(self) -> Dict[str, Any]:
        """Converts the ProjectConfig to document compatible with dlt configuration layout.
        ProjectConfig is a provider config doc with a few extra fields. We also
        rename "destinations" to "destination" (which we should do in OSS).
        """
        # this also clones the dictionary
        filtered = exclude_keys(self._config, ["profiles", "project"])
        # rename the destination to destinations
        if "destinations" in filtered:
            filtered["destination"] = filtered.pop("destinations")
        return exclude_keys_from_nested(filtered, {"type"})

    @property
    def sources(self) -> Dict[str, SourceConfig]:
        return self._config.get("sources") or {}

    @property
    def destinations(self) -> Dict[str, DestinationConfig]:
        return self._config.get("destinations") or {}

    @property
    def profiles(self) -> Dict[str, ProfileConfig]:
        return self._config.get("profiles") or {}

    @property
    def pipelines(self) -> Dict[str, PipelineConfig]:
        return self._config.get("pipelines") or {}

    @property
    def transformations(self) -> Dict[str, Any]:
        return self._config.get("transformations") or {}

    @property
    def caches(self) -> Dict[str, CacheConfig]:
        return self._config.get("caches") or {}

    @property
    def datasets(self) -> Dict[str, DatasetConfig]:
        return self._config.get("datasets") or {}


@configspec
class ProjectConfiguration(BaseConfiguration):
    """Wraps project typed dict config until we unify those"""

    project_config: Annotated[ProjectConfig, NotResolved()] = None
    runtime: RuntimeConfiguration = None

    # __recommended_sections__: ClassVar[Sequence[str]] = ("project",)
