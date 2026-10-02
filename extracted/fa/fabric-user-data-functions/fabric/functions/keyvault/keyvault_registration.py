# flake8: noqa: I003

from fabric.functions.user_data_functions import UserDataFunctions
from .keyvault_provider import KeyVaultProvider
from azure.keyvault.secrets import SecretClient

def use_keyvault(udf: UserDataFunctions):
    udf.register_provider(SecretClient, KeyVaultProvider)
    pass
