import os
from worker_automate_hub.api.client import get_worker_vault_token, read_secret
from worker_automate_hub.decorators.singleton import singleton


@singleton
class CredentialsManager:
    def __init__(self):
        self._secrets = {}
        self._load_credentials()

    def _load_credentials(self):
        """
        Loads credentials from vault
        """
        # collect vault token via api_automate
        try:
            vault_token = get_worker_vault_token()
            secrets = read_secret(
                path="v1/main-sim/data/worker-automate-hub/env",
                vault_token=vault_token["code"],
            )
            self._secrets = secrets if secrets else {}
            if not self._secrets:
                print("Warning: No credentials loaded from vault.")
        except Exception as e:
            self._secrets = {}
            print(f"Error to get credentials from vault, message: {e}")

    def get_by_key(self, key: str):
        """
        Gets a credential by key.
        """
        return self._secrets.get(key)

    # def get_user_bi(self):
    #     return self.get("SAP_USER_BI")

    # def get_password_bi(self):
    #     return self.get("SAP_PASSWORD_BI")

    # def get_credentials(self):
    #     return self.get_user_bi(), self.get_password_bi()

    def refresh_credentials(self):
        """
        Refreshes the credentials from the vault.
        """
        self._load_credentials()
        print("Credentials refreshed.")
