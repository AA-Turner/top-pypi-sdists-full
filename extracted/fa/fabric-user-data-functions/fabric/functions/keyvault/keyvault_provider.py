# flake8: noqa: I003

from fabric.functions.providers.base_fabricitem_provider import BaseFabricItemProvider
from fabric.functions.fabric_item import FabricItem
from azure.keyvault.secrets import SecretClient

class KeyVaultProvider(BaseFabricItemProvider):

    def __init__(self):
        pass

    def create(self, item: FabricItem, **kwargs):

        access_token = item.get_access_token()
        vault_url = kwargs.get("vault_url")

        if vault_url is None:
            raise ValueError("Vault URL must be provided in kwargs")

        return SecretClient(vault_url=vault_url, credential=access_token)
