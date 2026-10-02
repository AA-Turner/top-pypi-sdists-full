# flake8: noqa: I003

# from datetime import datetime, timedelta, timezone
# from azure.core.credentials import TokenCredential  # noqa: I900
# from azure.keyvault.secrets import SecretClient

# class KeyVaultClient:

#     # key, (value, expiration)
#     secret_cache = {}

#     def __init__(self, endpoint_uri:str, credential: TokenCredential):
#         self.client = SecretClient(vault_url=endpoint_uri, credential=credential)
#         self._expiration = credential.get_token().expires_on

#     def expired(self) -> bool:
#         return datetime.now(tz=timezone.utc) > datetime.fromtimestamp(self._expiration, tz=timezone.utc)

#     def get_secret(self, secret_name: str):
#         # check to see if secret is available in cache and not expired
#         if secret_name in self.secret_cache:
#             value, expiration = self.secret_cache[secret_name]
#             if datetime.now(tz=timezone.utc) < expiration:
#                 return value
        
#         # fetch from key vault
#         secret = self.client.get_secret(secret_name)
#         self.secret_cache[secret_name] = (secret.value, datetime.now(tz=timezone.utc) + timedelta(minutes=1))
#         return secret.value