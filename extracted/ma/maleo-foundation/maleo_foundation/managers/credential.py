from google.oauth2.service_account import Credentials
from uuid import UUID
from maleo_foundation.enums import BaseEnums
from maleo_foundation.managers.client.google.secret import GoogleSecretManager
from maleo_foundation.models.transfers.general.credentials import MaleoCredentials
from maleo_foundation.models.transfers.general.settings import Settings
from maleo_foundation.utils.loaders.credential.google import GoogleCredentialsLoader
from maleo_foundation.utils.logging import SimpleConfig

class CredentialManager:
    def __init__(
        self,
        settings: Settings,
        log_config: SimpleConfig
    ):
        self.settings = settings
        self.log_config = log_config
        self._initialize()

    def _load_google_credentials(self) -> None:
        """Load Google service account credentials with validation."""
        try:
            self._google_credentials = GoogleCredentialsLoader.load(
                credentials_path=self.settings.GOOGLE_CREDENTIALS_PATH
            )

            # Validate the loaded credentials
            GoogleCredentialsLoader.validate_credentials(self._google_credentials)

        except Exception as e:
            raise RuntimeError(f"Failed to load Google credentials: {str(e)}")

    def _initialize_secret_manager(self) -> None:
        self._secret_manager = GoogleSecretManager(
            log_config=self.log_config,
            service_key=self.settings.SERVICE_KEY,
            credentials=self._google_credentials
        )

    def _get_environment_for_credentials(self) -> str:
        return (
            BaseEnums.EnvironmentType.STAGING
            if self.settings.ENVIRONMENT == BaseEnums.EnvironmentType.LOCAL
            else self.settings.ENVIRONMENT
        )

    def _load_maleo_credentials(self) -> None:
        environment = self._get_environment_for_credentials()

        try:
            id = int(self._secret_manager.get(f"maleo-service-account-id-{environment}"))
            uuid = UUID(self._secret_manager.get(f"maleo-service-account-uuid-{environment}"))
            email = self._secret_manager.get("maleo-service-account-email")
            username = self._secret_manager.get("maleo-service-account-username")
            password = self._secret_manager.get("maleo-service-account-password")
            
            self._maleo_credentials = MaleoCredentials(
                id=id,
                uuid=uuid,
                username=username,
                email=email,
                password=password
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load Maleo credentials: {str(e)}")

    def _initialize(self):
        self._load_google_credentials()
        self._initialize_secret_manager()
        self._load_maleo_credentials()

    @property
    def google_credentials(self) -> Credentials:
        return self._google_credentials
    
    @property
    def secret_manager(self) -> GoogleSecretManager:
        return self._secret_manager
    
    @property
    def maleo_credentials(self) -> MaleoCredentials:
        return self._maleo_credentials