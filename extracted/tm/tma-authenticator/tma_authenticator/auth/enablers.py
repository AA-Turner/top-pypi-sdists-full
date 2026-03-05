from dataclasses import dataclass


@dataclass(frozen=True)
class AuthEnablers:
    keycloak: bool = True
    tma: bool = True
    service_token: bool = True
    web3_jwt: bool = True
    wallet_connect: bool = True
    # Enables the X-Service-Token + X-Wallet-Address path: validates the service token then
    # looks up (or creates) a user record by plain wallet address. Runs last and overrides
    # any previous auth result. Defaults to False to avoid breaking existing apps.
    wallet_address: bool = False
