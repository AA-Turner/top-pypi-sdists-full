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
        Load Google credentials either from a service account file or from the default credentials.
        Priority:
        1. Explicit path argument
        2. GOOGLE_CREDENTIALS_PATH environment variable
        3. google.auth.default()
        """
        if credentials_path is None:
            credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")

        if credentials_path is not None:
            credentials_path = Path(credentials_path)
            if credentials_path.exists() and credentials_path.is_file():
                try:
                    return Credentials.from_service_account_file(str(credentials_path))
                except Exception as e:
                    raise ValueError(f"Failed to load credentials from file: {str(e)}")

        try:
            credentials, _ = default()
            return credentials
        except Exception as e:
            raise ValueError(f"Failed to load default credentials: {str(e)}")