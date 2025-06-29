from pathlib import Path
from maleo_foundation.models.transfers.general.configurations.cache.redis import (
    RedisCacheNamespaces,
    RedisCacheConfigurations
)
from maleo_foundation.models.transfers.general.configurations.cache \
    import CacheConfigurations
from maleo_foundation.models.transfers.general.configurations import (
    RuntimeConfigurations,
    StaticConfigurations,
    Configurations
)
from maleo_foundation.models.transfers.general.settings import Settings
from maleo_foundation.utils.loaders.yaml import YAMLLoader
from maleo_foundation.utils.merger import deep_merge
from .credential import CredentialManager

class ConfigurationManager:
    def __init__(
        self,
        settings: Settings,
        credential_manager: CredentialManager
    ):
        self._settings = settings
        self._credential_manager = credential_manager

        self._load_configurations()

    def _load_static_configurations(self) -> StaticConfigurations:
        use_local = self._settings.USE_LOCAL_STATIC_CONFIGURATIONS
        config_path = self._settings.STATIC_CONFIGURATIONS_PATH

        if use_local and config_path is not None and isinstance(config_path, str):
            config_path = Path(config_path)
            if config_path.exists() and config_path.is_file():
                data = YAMLLoader.load_from_path(config_path)
                return StaticConfigurations.model_validate(data)

        secret_data = (
            self
            ._credential_manager
            .secret_manager
            .get(f"maleo-static-configurations-{self._settings.ENVIRONMENT}")
        )
        data = YAMLLoader.load_from_string(secret_data)
        return StaticConfigurations.model_validate(data)

    def _load_runtime_configurations(self) -> RuntimeConfigurations:
        use_local = self._settings.USE_LOCAL_STATIC_CONFIGURATIONS
        config_path = self._settings.RUNTIME_CONFIGURATIONS_PATH

        if use_local and config_path is not None and isinstance(config_path, str):
            config_path = Path(config_path)
            if config_path.exists() and config_path.is_file():
                data = YAMLLoader.load_from_path(config_path)
                return RuntimeConfigurations.model_validate(data)

        secret_data = (
            self
            ._credential_manager
            .secret_manager
            .get(f"{self._settings.SERVICE_KEY}-runtime-configurations-{self._settings.ENVIRONMENT}")
        )
        data = YAMLLoader.load_from_string(secret_data)
        return RuntimeConfigurations.model_validate(data)

    def _load_cache_configurations(self) -> CacheConfigurations:
        namespaces = RedisCacheNamespaces(base=self._settings.SERVICE_KEY)
        host = self._credential_manager.secret_manager.get(
            f"maleo-redis-host-{self._settings.ENVIRONMENT}"
        )
        password = self._credential_manager.secret_manager.get(
            f"maleo-redis-password-{self._settings.ENVIRONMENT}"
        )
        redis = RedisCacheConfigurations(
            namespaces=namespaces, 
            host=host, 
            password=password
        )
        return CacheConfigurations(redis=redis)

    def _load_configurations(self) -> None:
        static_configurations = self._load_static_configurations()
        runtime_configurations = self._load_runtime_configurations()
        cache_configurations = self._load_cache_configurations()

        merged_configurations = deep_merge(
            static_configurations.model_dump(),
            runtime_configurations.model_dump(),
            {"cache": cache_configurations.model_dump()}
        )

        self._configurations = Configurations.model_validate(merged_configurations)

    @property
    def configurations(self) -> Configurations:
        return self._configurations