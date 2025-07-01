from pathlib import Path
from maleo_foundation.models.transfers.general.configurations import Configurations
from maleo_foundation.models.transfers.general.settings import Settings
from maleo_foundation.utils.loaders.yaml import YAMLLoader
from .credential import CredentialManager

class ConfigurationManager:
    def __init__(
        self,
        settings: Settings,
        credential_manager: CredentialManager
    ) -> None:
        self._settings = settings
        self._credential_manager = credential_manager

        use_local = self._settings.USE_LOCAL_CONFIGURATIONS
        config_path = self._settings.CONFIGURATIONS_PATH

        if use_local and config_path is not None and isinstance(config_path, str):
            config_path = Path(config_path)
            if config_path.exists() and config_path.is_file():
                data = YAMLLoader.load_from_path(config_path)
                self._configurations = Configurations.model_validate(data)
                return

        secret_data = (
            self
            ._credential_manager
            .secret_manager
            .get(f"{self._settings.SERVICE_KEY}-configurations-{self._settings.ENVIRONMENT}")
        )
        data = YAMLLoader.load_from_string(secret_data)
        self._configurations = Configurations.model_validate(data)

    @property
    def configurations(self) -> Configurations:
        return self._configurations