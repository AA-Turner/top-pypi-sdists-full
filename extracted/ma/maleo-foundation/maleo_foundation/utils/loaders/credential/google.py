import json
import os
from google.auth import default
from google.oauth2.service_account import Credentials
from pathlib import Path
from typing import Optional, Union

class GoogleCredentialsLoader:
    @staticmethod
    def load(
        credentials_path: Optional[Union[Path, str]] = None
    ) -> Credentials:
        """
        Load Google service account credentials with guaranteed project_id.
        Priority:
        1. Explicit path argument
        2. GOOGLE_CREDENTIALS_PATH environment variable
        3. GOOGLE_APPLICATION_CREDENTIALS environment variable
        4. Service account from default credentials (if available)

        Always returns google.oauth2.service_account.Credentials with project_id.
        Raises ValueError if service account credentials cannot be loaded or project_id is missing.
        """
        # Try explicit path first
        if credentials_path is not None:
            credentials_path = Path(credentials_path)
            if credentials_path.exists() and credentials_path.is_file():
                return GoogleCredentialsLoader._load_from_file(credentials_path)

        # Try GOOGLE_CREDENTIALS_PATH environment variable
        env_credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
        if env_credentials_path:
            credentials_path = Path(env_credentials_path)
            if credentials_path.exists() and credentials_path.is_file():
                return GoogleCredentialsLoader._load_from_file(credentials_path)

        # Try GOOGLE_APPLICATION_CREDENTIALS environment variable
        app_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if app_credentials_path:
            credentials_path = Path(app_credentials_path)
            if credentials_path.exists() and credentials_path.is_file():
                return GoogleCredentialsLoader._load_from_file(credentials_path)

        # Try to get service account from default credentials
        return GoogleCredentialsLoader._load_from_default()

    @staticmethod
    def _load_from_file(credentials_path: Path) -> Credentials:
        """Load credentials from a service account file."""
        try:
            # First, read and validate the service account file
            with open(credentials_path, 'r') as f:
                service_account_info = json.load(f)

            # Ensure project_id is present in the file
            if 'project_id' not in service_account_info or not service_account_info['project_id']:
                raise ValueError(f"Service account file {credentials_path} does not contain project_id")

            # Load credentials from the file
            credentials = Credentials.from_service_account_file(str(credentials_path))

            # Double-check that project_id is available in the credentials object
            if not credentials.project_id:
                raise ValueError(f"Loaded credentials from {credentials_path} do not have project_id")

            return credentials

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in credentials file {credentials_path}: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to load credentials from file {credentials_path}: {str(e)}")

    @staticmethod
    def _load_from_default() -> Credentials:
        """Load service account credentials from default sources."""
        try:
            credentials, _ = default()

            # Check if the default credentials are service account credentials
            if isinstance(credentials, Credentials):
                # Already service account credentials
                if not credentials.project_id:
                    # For service account credentials, project_id should be available
                    # If not, the service account file is malformed
                    raise ValueError(
                        "Service account credentials loaded from default source do not have project_id. "
                        "Please ensure your service account key file contains the project_id field."
                    )

                return credentials
            else:
                # Default credentials are not service account credentials
                raise ValueError(
                    "Default credentials are not service account credentials. "
                    f"Found credentials of type: {type(credentials)}. "
                    "Please provide a service account key file via GOOGLE_CREDENTIALS_PATH, "
                    "GOOGLE_APPLICATION_CREDENTIALS, or the credentials_path parameter."
                )

        except Exception as e:
            if "service account" in str(e).lower() or "project_id" in str(e).lower():
                raise
            raise ValueError(
                f"Failed to load service account credentials from default sources: {str(e)}. "
                "Please provide a service account key file via GOOGLE_CREDENTIALS_PATH, "
                "GOOGLE_APPLICATION_CREDENTIALS, or the credentials_path parameter."
            )

    @staticmethod
    def _get_project_id_from_env() -> str:
        """Get project_id from environment variables."""
        project_id = (
            os.getenv("GOOGLE_CLOUD_PROJECT") or
            os.getenv("GCLOUD_PROJECT") or
            os.getenv("GCP_PROJECT") or
            os.getenv("PROJECT_ID")
        )

        if not project_id:
            raise RuntimeError(
                "project_id is required but not found. Please set one of the following environment variables: "
                "GOOGLE_CLOUD_PROJECT, GCLOUD_PROJECT, GCP_PROJECT, or PROJECT_ID, "
                "or ensure your service account key file contains the project_id field."
            )

        return project_id

    @staticmethod
    def validate_credentials(credentials: Credentials) -> None:
        """Validate that credentials are service account credentials with project_id."""
        if not isinstance(credentials, Credentials):
            raise ValueError("Credentials must be google.oauth2.service_account.Credentials")

        if not credentials.project_id:
            raise ValueError("Service account credentials must have project_id")

        if not credentials.service_account_email:
            raise ValueError("Service account credentials must have service_account_email")